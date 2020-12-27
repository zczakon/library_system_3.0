class Config(object):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    DEBUG = False


class TestConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    TESTING = True


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
