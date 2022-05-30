# Changelog

## v1.1.0
- Change PySimpleGUIQt to normal PySimpleGUI.
- Using psgtray as a replacement for QtSystemTray.
- Using NSIS Setup instead of Advanced Installer.
- Add About and Settings.
- Add support for changing RSS update interval in Settings.
- Add a new logo.
- Switch using pyinstaller onefile instead of onedir for ease of setting up NSIS script.
- Redesigned UI layout.
- Update all libraries and SQLite DLL to the latest version.

## v1.0.1
- Upgraded build using Python 3.8.10 instead of 3.7.9.
- Dropped any support to other platforms. For now, only will support Windows x64.
- Removed notify-py dependency.
- Implemented support to Windows notification directly using winRT Python library.
- Rearranged tray menu items.
- Removed custom notification sound.
- Updated reader library usage to match the latest version.
- Added version file into exe.
- Created installer using Advanced Installer.

## v1.0.0
- Initial release.
