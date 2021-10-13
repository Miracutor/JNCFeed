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
from winrt.windows.ui.notifications import (
    ToastNotificationManager,
    ToastNotification,
)
from winrt.windows.data.xml.dom import XmlDocument
import subprocess
from pathlib import Path
from xml.etree import ElementTree


def toast_notification(AppID, title, text, image_src):
    top = ElementTree.Element("toast")
    top.set("duration", "short")
    visual = ElementTree.SubElement(top, "visual")

    binding = ElementTree.SubElement(visual, "binding")
    binding.set("template", "ToastGeneric")
    image_tag = ElementTree.SubElement(binding, "image")
    image_tag.set("id", "1")
    image_tag.set("placement", "appLogoOverride")
    image_tag.set("src", str(Path(image_src).absolute()))
    title_tag = ElementTree.SubElement(binding, "text")
    title_tag.set("id", "1")
    title_tag.text = title
    text_tag = ElementTree.SubElement(binding, "text")
    text_tag.text = text
    text_tag.set("id", "2")

    doc = XmlDocument()
    doc.load_xml(ElementTree.tostring(top, encoding="utf-8").decode("utf-8"))
    notifier = ToastNotificationManager.create_toast_notifier(AppID)
    notifier.show(ToastNotification(doc))


def identify_app_id(appName: str):
    command = "& {(Get-StartApps " + appName + ")[0].AppId}"
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    i, _ = subprocess.Popen(
        ["Powershell", "-Command", command],
        stdout=subprocess.PIPE,
        startupinfo=startupinfo,
    ).communicate()
    return i.decode("utf-8").replace("\r\n", "")
