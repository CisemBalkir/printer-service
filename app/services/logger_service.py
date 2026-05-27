import json
from datetime import datetime
import os

LOG_FILE = "app/logs/logs.json"


def write_log(data: dict):

    # dosya yoksa oluştur
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([], f)

    # mevcut logları oku
    with open(LOG_FILE, "r") as f:
        logs = json.load(f)

    # yeni log ekle
    log_entry = {
        "ts": datetime.utcnow().isoformat(),
        **data
    }

    logs.append(log_entry)

    # geri yaz
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)