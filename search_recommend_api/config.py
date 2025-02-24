class Config:
    def __init__(self):
        pass

class ApiConfig(Config):
    def __init__(self):
        self.HOST: str = '0.0.0.0'
        self.PORT: int = 8080