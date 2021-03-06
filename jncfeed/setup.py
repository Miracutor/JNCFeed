# JNCFeed is an app that can notify you when the latest parts available
# of your followed series on J-Novel Club.

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
from pathlib import Path

from jncfeed.constants import get_config_dir_path
from jncfeed.jncapi import get_user
from reader import make_reader

path_config_dir = get_config_dir_path()
path_config = path_config_dir / Path("config")
path_database = path_config_dir / Path("db.sqlite")


def generate_jnc_rss_link(user_id):
    return f"https://labs.j-novel.club/feed/user/{user_id}.rss"


def configure_setup(jnc_email, jnc_password):
    path_config_dir.mkdir(exist_ok=True)
    user_data = get_user(jnc_email, jnc_password)
    if "LOGIN_FAILED" in user_data:
        return False
    else:
        path_config.write_text(user_data)
        reader = make_reader(str(path_database.resolve()))
        reader.add_feed(generate_jnc_rss_link(json.loads(user_data)["userId"]))
        reader.update_feeds()
        for entry in reader.get_entries():
            reader.mark_entry_as_read(entry)
            # Mark all entries as read at the time of setup.
        return True
