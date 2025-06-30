import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from email.utils import format_datetime

# Fetch JSON data
url = "https://data.cabq.gov/publicsafety/policeincidents/policeincidentsJSON_ALL"
resp = requests.get(url)
resp.raise_for_status()
items = resp.json()

# Build RSS feed
rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "title").text = "Albuquerque Police Incidents"
ET.SubElement(channel, "link").text = url
ET.SubElement(channel, "description").text = "Latest police incidents from ABQ open data"
ET.SubElement(channel, "lastBuildDate").text = format_datetime(datetime.utcnow())

for entry in items[:50]:  # limit to 50 most recent
    title = entry.get("offense", "Police Incident")
    desc = entry.get("address", "No description")
    date_str = entry.get("report_date") or entry.get("date")
    try:
        pub_date = format_datetime(datetime.fromisoformat(date_str))
    except:
        pub_date = format_datetime(datetime.utcnow())

    item = ET.SubElement(channel, "item")
    ET.SubElement(item, "title").text = title
    ET.SubElement(item, "description").text = desc
    ET.SubElement(item, "pubDate").text = pub_date
    ET.SubElement(item, "link").text = url  # Replace with actual link if available

ET.ElementTree(rss).write("police_incidents.rss", encoding="utf-8", xml_declaration=True)
