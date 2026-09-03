import os

class Settings:
    def __init__(self):
        self.MODEL: str = os.getenv("MODEL", "default_model")
        self.SUPPORTED_EXTENSIONS: list[str] = [
            ext.strip()
            for ext in os.getenv("SUPPORTED_EXTENSIONS").split(",")
        ]


    def __repr__(self):
        return f"Settings(MODEL={self.MODEL}, SUPPORTED_EXTENSIONS={self.SUPPORTED_EXTENSIONS})"
settings = Settings()