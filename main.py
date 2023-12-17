#!/usr/bin/python3

import lcddriver
import requests
import json
import re
import os

from time import sleep

api_url = "http://localhost:80/admin/api.php"
token = "xxxxxxxxxxxxxxxxxxxxxxxxx"

lcd = lcddriver.lcd(0x27)

def get_data():
    r = requests.get(api_url + "?summary&auth=" + token)
    return r.json()

while(True):
    # get version info
    versions = os.popen("pihole -v").read().split("\n")
    version_pihole_re = re.search("version\sis\s(.*?)\s\(Latest:\s(.*?)\)", versions[0])
    version_pihole_current = version_pihole_re.group(1)
    version_pihole_latest = version_pihole_re.group(2)
    version_ftl_re = re.search("version\sis\s(.*?)\s\(Latest:\s(.*?)\)", versions[2])
    version_ftl_current = version_ftl_re.group(1)
    version_ftl_latest = version_ftl_re.group(2)
    lcd.clear()
    lcd.display_line("PiHole " + version_pihole_current, 1, "c", 16)
    lcd.display_line("FTL " + version_ftl_current, 2, "c", 16)

    sleep(15)

    # should we display the update message?
    available_updates = []
    if version_pihole_current != version_pihole_latest:
        available_updates.append("PiHole")
    if version_ftl_current != version_ftl_latest:
        available_updates.append("FTL")
    if available_updates != []:
        update_line = " + ".join(available_updates)
        lcd.clear()
        lcd.display_line("Update avail", 1, "c", 16)
        lcd.display_line(update_line, 2, "c", 16)
        sleep(30)

    # get some sysinfo
    sysstats = os.popen("uptime").read()
    uptime = "Up: " + re.search("up\s(.*?)\,", sysstats).group(1)
    load = "Load: " + re.search("load\saverage:\s.*?,\s(.*?)\,", sysstats).group(1)
    #memstats = os.popen("free -h").read().split("\n")
    #mem = "Mem: " + re.search("Mem:\s+.*?\s+(.*?)\s+", memstats[1]).group(1)

    lcd.clear()
    lcd.display_line(uptime, 1, "c", 16)
    #line = f"{load:<7}{mem:>7}"
    lcd.display_line(load, 2, "c", 16)

    sleep(15)

    # query the pihole api for info
    data = get_data()
    listed_domains = data["domains_being_blocked"].replace(",", ".")
    queries_today = data["dns_queries_today"].replace(",", ".")
    queries_forward = data["queries_forwarded"].replace(",", ".")
    ads_blocked = data["ads_blocked_today"].replace(",", ".")
    ads_percent = data["ads_percentage_today"] .replace(".", ",")+ "%"
    unique_clients = data["unique_clients"].replace(",", ".")
    total_clients = data["clients_ever_seen"].replace(",", ".")

    ga_raw = data["gravity_last_updated"]["relative"]
    gravity_age = str(ga_raw["days"]) + ":" + str(ga_raw["hours"]) + ":" + str(ga_raw["minutes"])

    lcd.clear()
    lcd.display_line("Domains", 1, "c", 16)
    lcd.display_line(listed_domains, 2, "c", 16)

    sleep(30)

    lcd.clear()
    lcd.display_line("Queries", 1, "c", 16)
    lcd.display_line(queries_today + "/" + queries_forward, 2, "c", 16)

    sleep(30)

    lcd.clear()
    lcd.display_line("Blocked", 1, "c", 16)
    line = ads_blocked+"  "+ads_percent
    lcd.display_line(line, 2, "c", 16)

    sleep(30)

    lcd.clear()
    lcd.display_line("Clients", 1, "c", 16)
    lcd.display_line(unique_clients + "/" + total_clients, 2, "c", 16)

    sleep(30)

    lcd.clear()
    lcd.display_line("Gravity", 1, "c", 16)
    lcd.display_line(gravity_age, 2, "c", 16)

    sleep(30)
