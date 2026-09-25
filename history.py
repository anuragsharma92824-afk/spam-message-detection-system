import os
import pandas as pd
from datetime import datetime
from config import HISTORY_FILE


def save_history(message, result, sender="", phishing_status="", phishing_reasons=None, url="", url_status="", url_details=""):

    if phishing_reasons is None:
        phishing_reasons = []

    new_record = pd.DataFrame([{
        "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sender": sender,
        "message": message,
        "result": result,
        "phishing_status": phishing_status,
        "phishing_reasons": "; ".join(phishing_reasons),
        "url": url,
        "url_status": url_status,
        "url_details": url_details
    }])

    if os.path.exists(HISTORY_FILE):

        new_record.to_csv(
            HISTORY_FILE,
            mode="a",
            header=False,
            index=False
        )

    else:

        new_record.to_csv(
            HISTORY_FILE,
            mode="w",
            header=True,
            index=False
        )

def load_history():
    """Load message history."""

    if os.path.exists(HISTORY_FILE):
        history = pd.read_csv(HISTORY_FILE)

        # Old history.csv compatibility
        if "phishing_status" not in history.columns:
            history["phishing_status"] = "Not available"

        if "phishing_reasons" not in history.columns:
            history["phishing_reasons"] = ""

        if "url" not in history.columns:
            history["url"] =""

        if "url_status" not in history.columns:
                    history["url_status"] =""

        if "url_details" not in history.columns:
                    history["url_details"] =""

        return history

    return pd.DataFrame(
        columns=[
            "date_time",
            "sender",
            "message",
            "result",
            "phishing_status",
            "phishing_reasons",
            "url",
            "url_status",
            "url_details"
        ]
    )


def clear_history():
    """Delete all saved history."""

    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)