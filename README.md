# ![](media/logo.png) JNCFeed
An app that can notify you when the latest parts available of your followed series on J-Novel Club.

![Language](https://img.shields.io/badge/language-python-blue?style=flat-square&logo=python&logoColor=yellow)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)  
[![GitHub license](https://img.shields.io/github/license/Miracutor/JNCFeed?style=flat-square)](https://github.com/Miracutor/JNCFeed/blob/master/LICENSE)
[![GitHub release](https://img.shields.io/github/release/Miracutor/JNCFeed?include_prereleases&sort=semver&style=flat-square)](https://github.com/Miracutor/JNCFeed/releases/)
[![Github all releases](https://img.shields.io/github/downloads/Miracutor/JNCFeed/total?style=flat-square)](https://GitHub.com/Miracutor/JNCFeed/releases/)


## Disclaimer
JNCFeed is completely unaffiliated with J-Novel Club.
The logo that used in this program owned by J-Novel Club.
It is only used in this app as a visual aid for the user.
## Screenshots
![](media/screenshot-login-screen.png)
![](media/screenshot-settings.png)
## Installation
1. Make sure you have a J-Novel Club account and an active subscription (Free or Premium) on the site.
2. Download the Installer from the [Releases](https://github.com/Miracutor/JNCFeed/releases/) page.
3. Launch the installer and follow the instructions.
4. Enjoy!
## Features
- Notify the latest parts of your followed series on J-Novel Club.
- Adjustable notification frequency.
- Automatically start the app on startup.
## Usage
- (First time only) You will be prompted to enter your login credentials. When you successfully log in, you need to relaunch the application.
- Just launch JNCFeed.exe and when the icon appears on the system tray, the app successfully launched.
- You will receive the notification at the start of the application and in interval of 30 minutes after launch.
- Right-click the icon on the system tray and click "Exit" to quit the application.
## Tips
- You can reset the app data by deleting .jncfeed folder in Home directory. (For Windows, it is C:\Users\\[username])  
  Next time you launch the application again, you will be prompted to the login screen.
- You can change the notification frequency by changing the value of the "Interval" setting in the settings.
- You can see when the next RSS update on the settings page.
## Building
### Requirements
- Windows 10. (Other platforms may and may not work. Never tested, so I don't know.)
- Python 3.8 and above. I used Python 3.8.10 when developing and building this app.
- Pipenv tool (https://pypi.org/project/pipenv/)
- (For building installer) NSIS (https://nsis.sourceforge.io/). Make sure to put makensis in your PATH.
### Instructions
1. Rebuild the Pyinstaller bootloader.
   This step is required to reduce this program false positive detection as a virus. (It's not a virus!🤣)
   - Download the latest release of Pyinstaller archive [here](https://github.com/pyinstaller/pyinstaller/releases).
     Make sure it is the same version as the latest on PyPi.
   - Extract the archive.
   - Go to UnpackedFolder/bootloader and execute this command ```python ./waf all```.
   - Go back to UnpackedFolder and create a wheel using extra commands based on your platform not using the generic bdist_wheel command.
     Check out the extra commands using ```python setup.py --help-commands```.
   - Edit the pyinstaller path on Pipfile to your generated wheel.
2. Set up the development environment.  
   > pipenv install --dev
3. Update SQLite
   Because Python 3.8 on Windows used older SQLite dll, it needs to be updated to the latest version.
   - Download the dll [here](https://www.sqlite.org/download.html).
   - After that, make a backup of the original sqlite3.dll in Python37/dll and replace it with the new version.
4. Start building!
   - For clean build:  
   > pipenv run build-onefile
   - For dirty build  (if you make small changes and want to quickly rebuild):  
   > pipenv run dirty-build-onefile
5. Finished build on dist folder.
6. Build the installer.
   - Make sure you on the root of the project and execute this command:
   > pipenv run generate-setup
## License
JNCFeed is licensed under the GPLv3.0 license. Refer to [LICENSE](LICENSE) for more information.
```
JNCFeed is an app that can notify you when the latest parts available
of your followed series on J-Novel Club.

Copyright (C) 2022 Miracutor

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```
