class Config:
    SECRET_KEY = 'your_secret_key'
    JWT_SECRET_KEY = 'your_jwt_secret_key'
    JWT_TOKEN_LOCATION = ['headers']
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@db:5432/carford'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
