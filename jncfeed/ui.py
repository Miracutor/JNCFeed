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
import PySimpleGUI as sg
from apscheduler.job import Job
from psgtray import SystemTray
from apscheduler.triggers.interval import IntervalTrigger
import json
import re
import textwrap
from pathlib import Path
from jncfeed import __version__

sg.theme("Dark Blue 16")

icon = b"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"
jnc_logo = b"iVBORw0KGgoAAAANSUhEUgAAAD4AAABYCAYAAACtbEQDAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAARXSURBVHhe7ZxbiFVVHIenmWw0H2TKYGgGUwmnoRH1xSkaxyFwRCQpsmB8kErMS5aISK+R0EOhKEJQL70oiA/eQEPwLbr5JhQRQd6CiorAUrw2fr911hr2nNn77H3OGXdnn/l/8HFm9rrs9Tv7cs7I/ttiGIZhGMakMzo6+iAexT6/aWpA4OdQrPCbmh/CtuERF3uKBR/A6y72VAlO0Hb80kUu0fzBCfkAfoT/KbHn/w/OIrSwR3EI38BNdfoKtvq5W3ED3sYoLjivs3A9xs0T3IircQ66eeuGiWbiB/g71ouO6DHsx/CG7sQbWE4Ivrv0ayb+xYP4hFt8rTBBN36F4i5ewHP4TUa/xlO4D7fg2BHhtRO1SM0bRwjeh2cxbv7gt/gD3kTxCz6r8VXDwGl4WrPAn/gadqBOTR2pTPrpHPyusV34Ll7GSoxd4/wsY+ePqDNTl+J5FDpIXX6K7DBoLd5BnT4Dfpt2sAAXZ3QJLseXcQd+jlcxC6k3N/o8hdrPQmz322bjjygO4Lg3vyLqjOFo70Vt02n6Bep6vFWFevNqoWJw2p9HfeZrHzrFf8ZB3/Yi6hL6C2e4AVmgs07z31A3oyG/7WPMk7TgL2D04098j/r2p0vyijbAEj8kHTo/hDpS17DXb9PNI09qCf43PoI6cD9pA6z0Q9Khcwj+D/b4beG6yYtag+sat+BgwVOhc8ME53U69uLTZb6FzRkctd/3UB9Z+i4fNe4bX9ME1/eJ4+63bDTVEdc3P/1hc7JMfT8vx25uaMH9kHTobMHRgmOeWPA4aLfgESw4WnA/JB06W3C04JgnFjwO2i14BAuOFtwPSYfOFhwtOOaJBY+DdgsewYKjBfdD0qGzBUcLjnliweOg3YJHsOBowf2QdOjcCMGH3WISoL1pg/e7xSRA+0ulbuNoiuDz3WISoP31UrdxFD64C+AWkwDterC/nMIHP4OJD9zTJkPRTpTCB3/HLSQB2lW/8p3rOZ5CB9dj3Z1uIQnQ/rjrOZFCB9/jFlEB+mwtdZ1AYYNfwm63iARo12PZugfEUcjgenpxjVtABeijGhVVTcRRuODal+pUUkun6LNfAxIoVHAd6fexze28AvSZhwqXxKQE10OyOqXuZ/A/cMTtNAX6qYLpMw2qQN3BNVAfK3pKeKnfpudHJwuVfBzGuej2mQb9VqHOwkr8ivqMfxhVnCOW+SnSobPeXRWyie1+2yCq/qxWVCmkApkPUSVTmUsh6avP7XAEk9Als833VyWjqqW0zw43SVYYsAuFFuu+N/P6JKoOdHMV6o+JEezB7DVgERinurK4uYNvogru1Vdnazg79VpdrSkDVEQbrmvVm9W88DxgbfIx/BTD/ekZ31wdDNS7GE5vFa8dQhXBqmqw0dTHXLiudW96G32SGmDwIlRxbPm/djQqF/FVrO/sZAKpgphh1N/A+h87TjSYKt/4BNehCu786g3DMAzDMIyi09JyD0xzjppl8xljAAAAAElFTkSuQmCC"
jnc_title = b"iVBORw0KGgoAAAANSUhEUgAAAVIAAABYCAMAAACQ548PAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAL9UExURQAAAP///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////4bU3HAAAAD+dFJOUwAAAQIDBAUGBwgJCgsMDQ4PEBESExQVFhcYGRobHB0e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"


# Create UI Error Message
def error_window(title, message):
    window = sg.Window(
        title,
        [
            [sg.Text(message, font=("Roboto", 12))],
            [sg.OK(font=("Roboto", 12), size=(8, 1))],
        ],
        element_justification="center",
        keep_on_top=True,
        icon=icon,
    )
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "OK"):
            break
    window.close()


# Create UI SystemTray
def system_tray(job_instance: Job, path_config: Path):
    menu_def = [
        "",
        [
            "About",
            "Settings",
            "---",
            "Exit",
        ],
    ]

    layout = [[sg.T("Empty Window", key="-T-")]]

    window = sg.Window(
        "Window Title",
        layout,
        finalize=True,
        enable_close_attempted_event=True,
        alpha_channel=0,
    )
    window.hide()

    tray = SystemTray(
        menu_def, tooltip="JNCFeed", icon=icon, window=window, key="-SYSTRAY-"
    )

    while True:  # The event loop
        event, values = window.read()

        if event in tray.key:
            event = values[event]

        if event == "Exit":
            break

        if event == "About":
            about_window()

        if event == "Settings":
            settings_window(job_instance, path_config)

    tray.close()
    window.close()


# Create UI Main Window
def login_window():
    layout = [
        [sg.Image(data=jnc_logo), sg.Image(data=jnc_title)],
        [
            sg.T("Email", size=10, font="Roboto"),
            sg.In(key="-email-", size=30, font="Roboto"),
        ],
        [
            sg.T("Password", size=10, font="Roboto"),
            sg.In(key="-password-", password_char="*", size=30, font="Roboto"),
        ],
        [sg.T("")],
        [
            sg.OK(font="Roboto"),
            sg.Cancel(font="Roboto"),
        ],
    ]
    # Create the window
    window = sg.Window(
        "JNCFeed Login",
        layout,
        element_justification="center",
        icon=icon,
    )
    email_regex = re.compile("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if event == "OK":
            if values["-email-"] == "" or values["-password-"] == "":
                error_window("Error", "Empty email or password.")
            elif not email_regex.match(str(values["-email-"])):
                error_window("Error", "Invalid email.")
            else:
                status = "OK"
                break

        if event in (sg.WIN_CLOSED, "Cancel"):
            status = "Cancel"
            break
    window.close()
    return values["-email-"], values["-password-"], status


# function to change combo text to second equivalent
def combo_to_seconds(combo_text):
    if combo_text == "30 minutes":
        return 1800
    if combo_text == "1 hour":
        return 3600
    if combo_text == "3 hours":
        return 10800
    if combo_text == "6 hours":
        return 21600
    if combo_text == "A day":
        return 86400


# function to change seconds to combo text
def seconds_to_combo(seconds):
    if seconds == 1800:
        return "30 minutes"
    if seconds == 3600:
        return "1 hour"
    if seconds == 10800:
        return "3 hours"
    if seconds == 21600:
        return "6 hours"
    if seconds == 86400:
        return "A day"


# Create UI Settings Window
def settings_window(job_instance: Job, path_config: Path):
    user_data = json.loads(path_config.read_text())
    layout = [
        [sg.Im(data=icon), sg.T("JNCFeed Settings", font=("Roboto", 18))],
        [sg.Text("_" * 100, size=(65, 1))],
        [sg.Text("User Information", font=("Roboto", 14), justification="left")],
        [
            [
                sg.T("User Name", font="Roboto", size=10),
                sg.Input(
                    user_data["userName"],
                    key="-user-",
                    disabled=True,
                    disabled_readonly_background_color="gray",
                    font="Roboto",
                    size=30,
                ),
            ]
        ],
        [
            [
                sg.T("User ID", font="Roboto", size=10),
                sg.Input(
                    user_data["userId"],
                    key="-id-",
                    disabled=True,
                    disabled_readonly_background_color="gray",
                    font="Roboto",
                    size=30,
                ),
            ]
        ],
        [sg.Text("_" * 100, size=(65, 1))],
        [sg.Text("RSS Settings", font=("Roboto", 14), justification="left")],
        [
            sg.T("Interval", font="Roboto", size=6),
            sg.Combo(
                ["30 minutes", "1 hour", "3 hours", "6 hours", "A day"],
                key="-interval-",
                default_value=seconds_to_combo(user_data["interval"]),
                font="Roboto",
                size=13,
            ),
            sg.T("Next Update", font="Roboto", size=10),
            sg.Input(
                job_instance.next_run_time.strftime("%A - %H:%M:%S"),
                key="-time-",
                font="Roboto",
                disabled=True,
                size=16,
                disabled_readonly_background_color="gray",
                justification="center",
            ),
        ],
        [sg.T("")],
        [sg.Save(font="Roboto"), sg.Cancel(font="Roboto")],
    ]
    # Create the window
    window = sg.Window(
        "JNCFeed Settings",
        layout,
        element_justification="center",
        icon=icon,
    )
    # Create an event loop
    while True:
        event, values = window.read()

        # End program if user closes window or
        # presses the OK button
        if event == "Save":
            if not job_instance.trigger.interval_length == combo_to_seconds(
                values["-interval-"]
            ):
                job_instance.reschedule(
                    IntervalTrigger(seconds=combo_to_seconds(values["-interval-"]))
                )
                path_config.write_text(
                    json.dumps(
                        {
                            "userName": user_data["userName"],
                            "userId": user_data["userId"],
                            "interval": combo_to_seconds(values["-interval-"]),
                        }
                    )
                )

            break

        if event in (sg.WIN_CLOSED, "Cancel"):
            break

    window.close()


# Create UI About Window
def about_window():
    layout = [
        [sg.Im(data=icon), sg.T(f"JNCFeed v{__version__}", font=("Roboto", 18))],
        [sg.T("_" * 50)],
        [
            sg.T(
                textwrap.fill(
                    "An app that can notify you when the latest parts available of your followed series on J-Novel "
                    "Club.",
                    width=60,
                ),
                justification="center",
                font="Roboto",
            )
        ],
        [sg.T(textwrap.fill("Copyright (C) 2021 Miracutor", width=60), font="Roboto")],
        [sg.T("License: GPL v3", font="Roboto")],
        [sg.B("Close", font="Roboto")],
    ]
    # Create the window
    window = sg.Window(
        "JNCFeed About",
        layout,
        element_justification="center",
        icon=icon,
    )
    # Create an event loop
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Close"):
            break
    window.close()
