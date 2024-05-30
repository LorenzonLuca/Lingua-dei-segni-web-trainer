import re
import base64
import json
import random
import db.database as db_models
import models.Utils as utils
from io import BytesIO
from PIL import Image
from flask_socketio import SocketIO, emit
from flask import request

MAX_BUFFER_SIZE = 50 * 1000 * 1000
signs = None
languages = None
categories = None

def get_socket_manager(app, db, logger, hr):
    socketio = SocketIO(app, cors_allowed_origins="*", max_http_buffer_size=MAX_BUFFER_SIZE)

    @socketio.on('start_recognization')
    def handle_start_recognization():
        global signs
        global languages
        global categories
        signs = db_models.Sign.query.all()
        languages = db_models.Language.query.all()
        categories = db_models.Category.query.all()

        logger.info(f"Loaded data from database or recognization", request.remote_addr)


    @socketio.on('stream')
    def handle_webcam_stream(data):
        try:
            image_data = re.sub('^data:image/.+;base64,', '', data['img'])
            img = Image.open(BytesIO(base64.b64decode(image_data)), mode='r')
            pos = hr.detect_hand(img)
            threshold = data['threshold']

            try:
                json_pos = utils.cord_to_json(pos.hand_world_landmarks)
            except:
                logger.warning(f"No hand found while trying to recognize sign", request.remote_addr)
                return 

            results = []
            for s in signs:
                saved_map = json.loads(s.map)
                if utils.validate_maps(json_pos, saved_map, threshold):
                    data = collect_sign_data(s.id)
                    results.append({'base_position': s.base_position,'sign_position': s.sign_position,'words': data})

            emit('real_time_recognization', {'data': results})
        except:
            # Logging anything beacause this expeption is throwed a lot of time at the start of the stream
            emit('real_time_recognization', {'data': []})

    @socketio.on('stream_learn')
    def handle_webcam_learn(data):
        try:
            if data['id'] == 0:
                emit('real_time_learn_msg', {'msg': ''})
                return
            
            image_data = re.sub('^data:image/.+;base64,', '', data['img'])
            img = Image.open(BytesIO(base64.b64decode(image_data)), mode='r')
            pos = hr.detect_hand(img)

            json_pos = utils.cord_to_json(pos.hand_world_landmarks)
            saved_map = json.loads(signs[data['id']-1].map)

            if utils.validate_maps(json_pos, saved_map):
                emit('real_time_learn_msg', {'msg': 'OK'})
            else:
                emit('real_time_learn_msg', {'msg': 'NOK'})
        except:
            # Logging anything beacause this expeption is throwed a lot of time at the start of the stream
            emit('real_time_learn_msg', {'msg': ''})

    @socketio.on('stream_quiz')
    def handle_webcam_quiz(data):
        try:
            if data['id'] == 0:
                emit('real_time_learn_msg', {'msg': ''})
                return
            
            image_data = re.sub('^data:image/.+;base64,', '', data['img'])
            img = Image.open(BytesIO(base64.b64decode(image_data)), mode='r')
            pos = hr.detect_hand(img)

            json_pos = utils.cord_to_json(pos.hand_world_landmarks)
            saved_map = json.loads(signs[data['id']-1].map)

            delta = utils.calc_deltas(json_pos, saved_map)
            emit('real_time_delta', {'delta': delta})
        except:
            # Logging anything beacause this expeption is throwed a lot of time at the start of the stream
            emit('real_time_delta', {'delta': 0.04})

    
    @socketio.on('learn_next_word')
    def handle_learn_next_learn(data):
        words = db_models.Word.query.all()
        diff_index = True
        logger.info(f"Getting next word", request.remote_addr)
        while diff_index:
            w_index = random.randint(0, len(words)-1)
            diff_index = w_index == data['wordId']-1
        word = words[w_index]
        w_data = collect_word_data(word)
        
        datas = {'word': word.word, 'word_id': word.id,'category': w_data['category']
                , 'language': w_data['language'], 'sign_pos': w_data['sign_pos']
                , 'base_pos': w_data['base_pos'], 'sign_id':word.sign_fk}

        if 'qNumber' in data:
            datas['qNumber'] = data['qNumber'] + 1

        emit('new_word', datas)
            
    def collect_sign_data(id):
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
    
    def collect_word_data(word):
        category_name = ""
        for c in categories:
            if c.id == word.category_fk:
                category_name = c.name

        language_name = ""
        for l in languages:
            if l.id == word.language_fk:
                language_name = l.name

        sign_pos = 0
        base_pos = 0
        for s in signs:
            if s.id == word.sign_fk:
                sign_pos = s.sign_position
                base_pos = s.base_position

        return {'category': category_name, 'language': language_name, 'sign_pos': sign_pos, 'base_pos': base_pos}


    return socketio