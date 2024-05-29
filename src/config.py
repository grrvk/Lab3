from dotenv import load_dotenv
import os

load_dotenv()


class Settings():
    url: str = str(os.getenv("URL"))


settings = Settings()