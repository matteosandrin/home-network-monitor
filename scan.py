import os.path
import configparser
import csv
import datetime
import json
import requests
from scrape import extractOnlineDeviceInfo

dir_path = os.path.dirname(os.path.abspath(__file__))
config = configparser.ConfigParser()
config.read(os.path.join(dir_path, "config.ini"))

def scanNetworkDevices():
    session = requests.Session()
    session.post(
        "http://10.0.0.1/check.jst",
        data={
            "username" : config["DEFAULT"]["router_username"],
            "password" : config["DEFAULT"]["router_password"],
        }
    )
    result = session.get("http://10.0.0.1/connected_devices_computers.jst")
    return extractOnlineDeviceInfo(result.text)

def loadDeviceList(path="./devices.json"):
    if os.path.exists(path):
        return json.load(open(path))
    return []

def writeDeviceList(data, path="./devices.json"):
    devices = {d["hostname"] : d for d in loadDeviceList(path=path)}
    new_devices = {d["hostname"] : d for d in data}
    for hostname, d in new_devices.items():
        devices[hostname] = d
    file = open(path, "w")
    json.dump(
        sorted(devices.values(), key=lambda x: x["hostname"]),
        file, indent=4, sort_keys=True)

def writeStatus(devices, path="./status.csv"):
    exists = os.path.exists(path)
    f = open(path, "a+")
    writer = csv.DictWriter(
        f,
        fieldnames=["date", "devices"],
        quotechar="\"",
        quoting=csv.QUOTE_NONNUMERIC,
    )
    if not exists:
        writer.writeheader()
    writer.writerow({
        "date" : datetime.datetime.now().isoformat(),
        "devices" : '||'.join(sorted(d["hostname"] for d in devices)),
    })


devices_path = os.path.join(dir_path, "devices.json")
status_path = os.path.join(dir_path, "status.csv")

devices = scanNetworkDevices()
writeDeviceList(devices, path=devices_path)
writeStatus(devices, path=status_path)
