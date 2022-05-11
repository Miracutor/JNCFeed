# JNCFeed is a Python application that can inform you the latest parts availability of your followed series on
# J-Novel Club.

# Copyright (C) 2021 Miracutor

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import json
import shutil
import sys
from pathlib import Path

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from reader import make_reader

from jncfeed.setup import configure_setup
from jncfeed.ui import system_tray, login_window, error_window
from jncfeed.notifywin import identify_app_id, toast_notification

path_config_dir = Path.home() / Path(".jncfeed")
path_config = path_config_dir / Path("config")
path_database = path_config_dir / Path("db.sqlite")
rss_reader = None
jnc_username = None
appId = None


def check_setup():
    if (
        not path_config_dir.exists()
        or not path_config.exists()
        or not path_database.exists()
    ):
        if path_config_dir.exists():
            shutil.rmtree(path_config_dir)
        return False
    else:
        return True


def generate_jnc_notification(message: str):
    toast_notification(appId, f"{jnc_username}'s Followed Series", message, "logo.ico")


def load_reader():
    global rss_reader
    if not path_config.exists():
        print("You still have not set up your account. Please run setup once.")
        sys.exit(2)
    else:
        rss_reader = make_reader(str(path_database.resolve()))
        update_jnc_feed(rss_reader)


def update_jnc_feed(jnc_reader):
    jnc_reader.update_feeds()
    for entry in jnc_reader.get_entries(read=False, limit=15):
        jnc_reader.mark_entry_as_read(entry)
        generate_jnc_notification(entry.title)
    print(jnc_reader.get_entry_counts())
    jnc_reader.close()


def main():
    global jnc_username, appId

    if check_setup() is True:
        appId = identify_app_id("JNCFeed")
        if appId == "":
            appId = "{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\\WindowsPowerShell\\v1.0\\powershell.exe"

        # check the existence of the logo.ico file
        if not (Path(sys.executable).parent / Path("logo.ico")).exists():
            # if not, display error_window with error message
            error_window(
                "Error",
                "logo.ico not found. Please put logo.ico in the same directory as this file.",
            )
            sys.exit(2)

        scheduler = BackgroundScheduler()
        jnc_username = json.loads(path_config.read_text())["userName"]
        job = scheduler.add_job(
            load_reader,
            IntervalTrigger(seconds=json.loads(path_config.read_text())["interval"]),
        )

        load_reader()
        scheduler.start()
        system_tray(job, path_config)
        job.remove()
        scheduler.shutdown(wait=False)
    else:
        jnc_email, jnc_password, status = login_window()
        if status == "OK":
            setup_status = configure_setup(jnc_email, jnc_password)
            if setup_status is True:
                error_window(
                    "Success", "Login Successful. Please relaunch the application."
                )
                sys.exit(2)
            else:
                error_window("Error", "Login Failed. Please try again.")
                sys.exit(3)


if __name__ == "__main__":
    main()
