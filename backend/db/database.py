import bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import CHAR, TINYINT, LONGTEXT
from hashlib import sha256
from datetime import datetime, timedelta

db = SQLAlchemy()

#function that define database structure
def init_database(app, log):
    global logger
    logger = log
    db.init_app(app)
    return db

#tables defination

class User(db.Model):
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(64).with_variant(CHAR(64),"mysql", "mariadb"))
    token = db.Column(db.String(72).with_variant(CHAR(72),"mysql", "mariadb"))
    token_creation = db.Column(db.DateTime)
    admin = db.Column(db.Integer().with_variant(TINYINT(),"mysql", "mariadb"))
    histories = db.relationship('History', backref='user')

    def __repr__(self):
        return f'<User username: {self.username}>'
    
    # function for verify password of user
    def verify_password(self, password):
        password = sha256(password.encode('utf-8')).hexdigest()
        return password == self.password
    
    # function for create a token for user
    def create_auth_token(self):
        salt = bcrypt.gensalt()
        token = bcrypt.hashpw(self.username.encode('utf-8'), salt)
        self.token = token
        self.token_creation = datetime.now()
        db.session.commit()

        logger.info(f'created token for user {self.username}')

    # static function for check token validity
    @staticmethod
    def verify_auth_token(token):
        user = User.query.filter_by(token=token).first()
        if not user:
            logger.info(f'token {token} is not valid')
            return False

        if user.token_creation < datetime.today() - timedelta(days=30):
            logger.info(f'token for user {user.username} expired, need to login')
            return False
        
        return user
    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    words = db.relationship("Word", backref='category')

    def __repr__(self):
        return f'<Category name: {self.name} id: {self.id}>'

class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    words = db.relationship("Word", backref='language')

    def __repr__(self):
        return f'<Language name: {self.name} id: {self.id}>'
    
class Sign(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    base_position = db.Column(db.Integer())
    sign_position = db.Column(db.Integer())
    map = db.Column(LONGTEXT)
    words = db.relationship("Word", backref='sign')

    def __repr__(self):
        return f'<Sign id: {self.id} base pos: {self.base_position} sign pos: {self.sign_position}>'
    
class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    word = db.Column(db.String(20))
    category_fk = db.Column(db.Integer, db.ForeignKey('category.id'))
    language_fk = db.Column(db.Integer, db.ForeignKey('language.id'))
    sign_fk = db.Column(db.Integer, db.ForeignKey('sign.id'))
    histories = db.relationship('History', backref='word')

    def __repr__(self):
        return f'<Word id: {self.id} word: {self.word}>'
    
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.Float)
    date = db.Column(db.DateTime)
    user_fk = db.Column(db.String(20), db.ForeignKey('user.username'))
    word_fk = db.Column(db.Integer, db.ForeignKey('word.id'))

    def __repr__(self):
        return f'<History id: {self.id}>'
    
def init_db_values(psw):
    admin_user = bool(User.query.filter_by(username="admin").first())
    if not admin_user:
        password = sha256(psw.encode('utf-8')).hexdigest()
        new_user = User(username = "admin", password = password, admin = 1)
        db.session.add(new_user)
        db.session.commit()
        logger.info(f"User admin created")
