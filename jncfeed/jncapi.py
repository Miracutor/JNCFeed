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
import requests
import json

login_endpoint = "https://api.j-novel.club/api/users/login?include=user"


def jnc_login(user, password):
    return requests.post(
        login_endpoint, data={"email": user, "password": password}, timeout=15
    )


new_login_endpoint = "https://labs.j-novel.club/app/v1/auth/login"


def new_jnc_login(user, password):
    return requests.post(
        new_login_endpoint,
        json={"login": user, "password": password},
        timeout=15,
        headers={"accept": "application/json", "content-type": "application/json"},
        params={"format": "json"},
    )


def get_user(user, password):
    data = jnc_login(user, password)
    print(data.json())

    if "error" in data.json():
        user_data = {"LOGIN_FAILED"}
    else:
        user_data = json.dumps(
            {
                "userName": data.json()["user"]["username"],
                "userId": data.json()["userId"],
                "interval": 3600,
            }
        )
    return user_data
