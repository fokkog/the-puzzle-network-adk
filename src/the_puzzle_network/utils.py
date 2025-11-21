"""Utility functions for The Puzzle Network."""

import os

from dotenv import load_dotenv
from google.adk.events import Event
from google.genai import types


def load_env():
    load_dotenv()
    app_name = os.getenv("APP_NAME")
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set.")
    print(
        f"✅ GOOGLE_API_KEY environment variable has been set, {app_name} can proceed."
    )
    return app_name


retry_options = types.HttpRetryOptions(
    attempts=3,
    exp_base=2,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)


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
