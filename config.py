import os

dirname = os.path.dirname(__file__)


class Config:
    UPLOAD_DIRECTORY = os.path.join(dirname, 'uploads')
    SECRET_KEY = os.environ.get("SECRET_KEY", "8rxJdeSt8xwYHlDYwAwxZvbnBNNuQipIy6hrCgOFvFmaX8qyA9")
    RECAPTHCA_PUBLIC_KEY = os.environ.get("RECAPTCHA_PUBLIC_KEY") or "recaptcha_public_key"
    RECAPTHCA_PRIVATE_KEY = os.environ.get("RECAPTCHA_PRIVATE_KEY") or "recaptcha_private_key"
    INITIAL_PAGE_LOAD = 4
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL") or "sqlite:///" + os.path.join(dirname, "test.sqlite")


class ProdutionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("PROD_DATABASE_URL") or "sqlite:///" + os.path.join(dirname, "test.sqlite")


configs = {"testing": TestingConfig,
           "production": ProdutionConfig}
