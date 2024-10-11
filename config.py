import os

class Config:
    DEBUG = os.getenv("DEBUG", True)
    PORT = os.getenv("PORT", 5000)

config = Config()
