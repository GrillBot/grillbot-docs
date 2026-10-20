import requests
import os
from datetime import datetime, timezone
from dateutil import tz
import logging
from src.source.cache import cache, HEALTH_TTL_SECONDS


def is_online(health_url: str) -> bool:
    """Whether the health endpoint answers 200. Cached briefly, since it is asked for on every page render."""

    def check() -> bool:
        logging.info(f"Checking online status of {health_url}")
        try:
            return requests.head(health_url, timeout=3).status_code == 200
        except requests.RequestException:
            return False

    return cache.get_or_load(f"health_{health_url}", check, HEALTH_TTL_SECONDS)


def is_grillbot_online() -> bool:
    return is_online("https://health.grillbot.eu/bot")


def get_modification_date(
    template_root: str, filename: str, datetime_format: str
) -> str:
    base_file_date = os.path.getmtime(os.path.join(template_root, "base.html"))
    file_date = os.path.getmtime(os.path.join(template_root, filename))
    time = base_file_date if base_file_date > file_date else file_date
    return (
        datetime.fromtimestamp(time, tz=timezone.utc)
        .astimezone(tz.gettz("Europe/Prague"))
        .strftime(datetime_format)
    )
