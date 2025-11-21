"""Utility functions for The Puzzle Network."""

import os

from dotenv import load_dotenv
from google.adk.events import Event

from .logging import get_logger


logger = get_logger(__name__)


def load_env():
    load_dotenv()
    app_name = os.getenv("APP_NAME")
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set.")
    logger.info(
        "✅ GOOGLE_API_KEY environment variable has been set, %s can proceed.", app_name
    )
    return app_name


def extract_textpart(response: list[Event]) -> str:
    textpart = "N/A"
    if (
        len(response) > 0
        and response[0].content
        and response[0].content.parts
        and len(response[0].content.parts) > 0
        and response[0].content.parts[0].text
    ):
        textpart = response[0].content.parts[0].text
    return textpart
