from bs4 import BeautifulSoup
import re

def extractOnlineDeviceInfo(html_page: str):
    soup = BeautifulSoup(html_page, "html.parser")
    online_table = soup.find(id="online-private").find("table")
    devices = []
    for row in online_table.findAll("tr"):
        hostname = row.find(class_=re.compile("device-name"))
        if hostname is not None:
            device = {}
            info = row.find(class_="device-info")
            device["hostname"] = hostname.string.strip()
            ip = re.search("(\d{1,3}\.){3}\d{1,3}", info.get_text())
            device["ip"] = ip.group() if (ip is not None) else ""
            mac = re.search("([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})", info.get_text())
            device["mac"] = mac.group().upper() if (mac is not None) else ""
            devices.append(device)
    return devices