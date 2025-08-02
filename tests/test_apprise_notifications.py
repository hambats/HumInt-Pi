import os
import sqlite3
import pytest
from datetime import datetime
from scripts.utils.notifications import sendAppriseNotifications


def create_test_db(db_file):
    conn = sqlite3.connect(db_file)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS detections (id integer PRIMARY KEY, Com_Name text, Date date NULL, Time time NULL);"
    )
    conn.close()


@pytest.fixture(autouse=True)
def clean_up_after_each_test():
    yield
    if os.path.exists("test.db"):
        os.remove("test.db")


def test_notifications(mocker):
    notify_call = mocker.patch('scripts.utils.notifications.notify')
    create_test_db("test.db")
    settings_dict = {
        "APPRISE_NOTIFICATION_TITLE": "New event",
        "APPRISE_NOTIFICATION_BODY": "$transcript",
        "APPRISE_NOTIFY_EACH_DETECTION": "0",
        "APPRISE_NOTIFY_NEW_SPECIES": "0",
        "APPRISE_NOTIFY_NEW_SPECIES_EACH_DAY": "0"
    }
    sendAppriseNotifications("id_transcript",
                             "0.91",
                             "91",
                             "filename",
                             datetime.now().strftime("%Y-%m-%d"),
                             "06:06:06",
                             "06",
                             "-1",
                             "-1",
                             "0.7",
                             "1.25",
                             "0.0",
                             settings_dict,
                             "test.db")
    assert notify_call.call_count == 0
