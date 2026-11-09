import os

from dotenv import load_dotenv


load_dotenv()


AI_PROVIDER = os.getenv(
    "AI_PROVIDER",
    "mock"
)

AI_MODEL = os.getenv(
    "AI_MODEL",
    "mock-qa-model"
)