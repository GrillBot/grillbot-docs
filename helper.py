import requests
import os
from datetime import datetime, timezone
from dateutil import tz
import logging


def is_grillbot_online() -> bool:
    logging.info('Checking GrillBot status.')
    return requests.get("https://grillbot.cloud/health").status_code == 200


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
