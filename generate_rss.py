import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from email.utils import format_datetime

url = "https://data.cabq.gov/publicsafety/policeincidents/policeincidentsJSON_ALL"
items = []

print(f"🔄 Fetching from {url}...")

try:
    resp = requests.get(url, timeout=15)
    status = resp.status_code
    content = resp.text.strip()
    content_type = resp.headers.get('Content-Type', '')

    print(f"➡️ HTTP Status: {status}")
    print(f"➡️ Content-Type: {content_type}")
    print(f"➡️ Response length: {len(content)}")

    if status == 200 and content and 'json' in content_type.lower():
        try:
            items = resp.json()
            print(f"✅ Parsed {len(items)} items.")
        except Exception as e:
            print("❌ Failed to parse JSON:", e)
    else:
        print("❌ Invalid response. Skipping JSON parse.")

except Exception as e:
    print("❌ Request failed:", e)

# Create RSS feed
rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "title").text = "Albuquerque Police Incidents"
ET.SubElement(channel, "link").text = url
ET.SubElement(channel, "description").text = "Latest police incidents from ABQ open data"
ET.SubElement(channel, "lastBuildDate").text = format_datetime(datetime.utcnow())

for entry in items[:50]:
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
    ET.SubElement(item, "link").text = url

ET.ElementTree(rss).write("police_incidents.rss", encoding="utf-8", xml_declaration=True)
print("✅ RSS file written: police_incidents.rss")
