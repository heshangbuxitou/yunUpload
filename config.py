import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'heshangbuxitou'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost:3306/day11'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    UPLOAD_FOLDER =  os.path.join(os.path.abspath(''),'upload')
    ALLOWED_EXTENSIONS = set(['txt','pdf','png','jpg','jpeg','gif','doc','docx','zip','rar','ppt'])
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024    #支持最大20M文件上传

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    pass

config = {
    'development':DevelopmentConfig,
    'production':ProductionConfig,
    
    'default':DevelopmentConfig
}