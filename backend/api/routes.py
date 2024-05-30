import re
import datetime
from cv2 import log
from sqlalchemy import desc
import models.Utils as utils
from PIL import Image
import db.database as db_models
from flask import request, g, request
from flask_httpauth import HTTPBasicAuth
from hashlib import sha256
import json

PSW_PATTERN = re.compile("^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{6,}$")

def create_routes(app, db, logger, hr):
    auth = HTTPBasicAuth()
    
    # method for check user authentication
    @auth.verify_password
    def verify_password(usr_or_tkn, psw):
        # check token validity
        user = db_models.User.verify_auth_token(usr_or_tkn)
        if not user:
            # check password validity
            user = db_models.User.query.filter_by(username = usr_or_tkn).first()
            if not user or not user.verify_password(psw):
                return False
        g.user = user
        logger.info(f"Authentication valid for user {g.user.username}")
        return True
    
    @app.route('/api/login', methods=['GET'])
    @auth.login_required
    def login():
        logger.info("Request for /api/login", request.remote_addr)
        token = get_token(g.user.username)
        if token:
            logger.info(f'user {g.user.username} logged in', request.remote_addr)
            return {'token': token}, 200
        return {}, 500
    
    @app.route('/api/register', methods=['POST'])
    def register():
        logger.info(f'Request for /api/register', request.remote_addr)
        username = request.form['username']
        psw = request.form['password']

        if len(username) < 4 or len(username) > 20:
            return {'msg': 'username-length-invalid'}, 400
        if not PSW_PATTERN.match(psw):
            return {'msg': 'password-invalid'}, 400
        user = bool(db_models.User.query.filter_by(username=username).first())
        if user:
            return {'msg': 'user-exist'}, 400

        password = sha256(psw.encode('utf-8')).hexdigest()
        new_user = db_models.User(username = username.strip(), password = password, admin = 0)
        db.session.add(new_user)
        db.session.commit()

        logger.info(f'user {username} created')

        token = get_token(username)
        if token:
            return {'token': token}, 201
        return {}, 201

    # route for get username from token
    @app.route('/api/user', methods=['GET'])
    @auth.login_required
    def get_user():
        logger.info("Request for /api/user", request.remote_addr)
        return {'username': g.user.username, 'admin': g.user.admin}, 201
    
    @app.route('/api/history', methods=['GET'])
    @auth.login_required
    def get_history():
        logger.info("Request for /api/history", request.remote_addr)

        def history_performance():
            res = []
            history = db_models.History.query.filter_by(user_fk=g.user.username).order_by(desc(db_models.History.value))
            for h in history:
                word = db_models.Word.query.filter_by(id=h.word_fk).first()
                sign = db_models.Sign.query.filter_by(id=word.sign_fk).first()
                category = db_models.Category.query.filter_by(id=word.category_fk).first()
                language = db_models.Language.query.filter_by(id=word.language_fk).first()
                res.append({'id': h.id, 'value': h.value, 'date': h.date, 'word': word.word, 'base_pos': sign.base_position,
                            'sign_pos': sign.sign_position, 'category': category.name, 'language': language.name})
            
            logger.info(f"History collected for user {g.user.username}")

            return {'history': res}, 200
        
        history = logger.performance(f"Time for get all history data", history_performance)
        return history

    @app.route('/api/history/add', methods=['POST'])
    @auth.login_required
    def add_history_value():
        logger.info("Request for /api/history/add", request.remote_addr)

        word = int(request.form['word'])
        value = float(request.form['value'])

        def history_add_performance():
            perc = utils.convert_delta(value)
            date = datetime.datetime.now()
            history_v = db_models.History.query.filter_by(user_fk=g.user.username, word_fk=word).first()

            if history_v:
                if history_v.value < perc:
                    history_v.date = date
                    history_v.value = perc
                    db.session.commit()
                    logger.info(f"Percentage {perc} updated for user {g.user.username}, word: {word}", request.remote_addr)
            else:
                new_history_v = db_models.History(value=perc, date=date, user_fk=g.user.username, word_fk=word)
                db.session.add(new_history_v)
                db.session.commit()
                logger.info(f"No data for user {g.user.username}, word: {word}. Added Percentage {perc}", request.remote_addr)
        
        logger.performance(f"Time for saving element in history", history_add_performance)

        return {}, 200

    @app.route('/api/recognize', methods=['POST'])
    def recognize_image():
        logger.info("Request for /api/recognize", request.remote_addr)

        img = request.files['img']
        try:
            img = Image.open(img, mode='r')
        except:
            logger.error(f"File format is not valid", request.remote_addr)
            return {'error': 'wrong-format'},400
        img = img.convert('RGB')

        def recognize_performance():
            pos = hr.detect_hand(img)

            signs = db_models.Sign.query.all()
            languages = db_models.Language.query.all()
            categories = db_models.Category.query.all()
            try:
                json_pos = utils.cord_to_json(pos.hand_world_landmarks)
            except:
                logger.warning(f"No hand found while trying to recognize sign", request.remote_addr)
                return {'error': 'no-hand'},400

            results = []

            for s in signs:
                saved_map = json.loads(s.map)
                if utils.validate_maps(json_pos, saved_map):
                    logger.info(f"Sign recognized, collecting data from database", request.remote_addr)
                    data = collect_sign_data(s.id, categories, languages)
                    results.append({'base_position': s.base_position,'sign_position': s.sign_position,'words': data})

            if len(results) > 0:
                return {'data': results}, 200
            else:
                logger.warning(f"No sign match with user's sign", request.remote_addr)
                return {'error': 'sign-unrecognized'},400
        
        res = logger.performance(f"Time for recognize sign", recognize_performance)
        return res

    @app.route('/api/insert', methods=['POST'])
    @auth.login_required
    def insert_sign():
        if g.user.admin != 1:
            logger.warning(f"User {g.user.username} tried to insert a new sign without permission", request.remote_addr)
            return
        logger.info("Request for /api/insert", request.remote_addr)

        img = request.files['img']
        sign_pos = request.form['sign_position']
        base_pos = request.form['base_position']
        words = request.form['words']
        words_dict = json.loads(words)

        try:
            img = Image.open(img, mode='r')
        except:
            logger.error(f"File format is not valid", request.remote_addr)
            return {'error': 'wrong-format'},400

        def insert_performance():
            hand_pos_data = hr.detect_hand(img)
            
            try:
                string_cord = utils.cord_to_string(hand_pos_data.hand_world_landmarks)
            except:
                logger.warning(f"No hand found while trying to insert new sign", request.remote_addr)
                return {'error': 'no-hand'},400

            new_sign = db_models.Sign(sign_position=sign_pos, base_position=base_pos, map=string_cord)
            db.session.add(new_sign)
            db.session.commit()

            for w in words_dict:
                category = check_category_exists(w['category'])
                if not category:
                    category = db_models.Category(name=w['category'])
                    db.session.add(category)
                
                language = check_language_exists(w['language'])
                if not language:
                    language = db_models.Language(name=w['language'])
                    db.session.add(language)

                db.session.commit()

                new_word = db_models.Word(word=w['word'], category_fk=category.id, language_fk=language.id, sign_fk=new_sign.id)
                db.session.add(new_word)
                db.session.commit()

            logger.info(f"New sign with id {new_sign.id} registered in database")
            return {},201
        
        res = logger.performance(f"Time for insert new sign", insert_performance)
        return res



    # function for get token from username
    def get_token(username):
        user = db_models.User.query.filter_by(username = username).first()
        if not user:
            return
        if user.token == None:
            user.create_auth_token()
        return user.token
    
    def check_category_exists(cat_name):
        category = db_models.Category.query.filter_by(name=cat_name).first()
        return category
    
    def check_language_exists(lang_name):
        language = db_models.Language.query.filter_by(name=lang_name).first()
        return language
    
    def collect_sign_data(id, categories, languages):
        data = []

        words = db_models.Word.query.filter_by(sign_fk=id)
        for w in words:
            category_name = ""
            for c in categories:
                if c.id == w.category_fk:
                    category_name = c.name

            language_name = ""
            for l in languages:
                if l.id == w.language_fk:
                    language_name = l.name
            
            data.append({'word': w.word, 'language': language_name, 'category': category_name})

        return data