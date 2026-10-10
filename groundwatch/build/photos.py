# 위키미디어 커먼즈에서 사진을 받아 images/photos/에 저장하고 출처·라이선스를 credits.json에 남긴다
import json, sys, urllib.parse, urllib.request, os, re, html, time
OUT = os.path.join(os.path.dirname(__file__), "..", "images", "photos")
TITLES = {
  "pv5_cargo_a": "Kia PV5 (SW1) Cargo – Seoul Mobility Show 2025 (04).jpg",
  "pv5_cargo_b": "Kia PV5 (SW1) Cargo – Seoul Mobility Show 2025 (08).jpg",
  "pv5_cargo_c": "Kia PV5 Cargo IMG 7825.jpg",
  "pv5_cargo_d": "Kia PV5 Cargo IMG 7829.jpg",
  "pv5_iaa": "Kia PV5 IAA Transportation 2024 (DSC02576).jpg",
  "pv5_highroof": "Kia PV5 High-Roof IAA Transportation 2024 (DSC02562).jpg",
  "pv5_passenger_jms": "Kia PV5 Passenger JMS 2025.jpg",
  "pv5_hanover": "Kia PV5, IAA 2024, Hanover (P1200020).jpg",
  "seoul_alley_night": "Night of Euljiro Alley.jpg",
  "seoul_jongno_night": "Night view of Downtown Seoul along Jongno Street in 2020.jpg",
  "seoul_traffic_1": "View of Night Traffic from Above in Seoul-1.jpg",
  "seoul_traffic_3": "View of Night Traffic from Above in Seoul-3.jpg",
  "seoul_night_city": "Seoul cityscape by night (02).jpg",
  "seoul_station_night": "Seoul Station, Seoul, South Korea - night view 2023-03-31.jpg",
  "sinkhole_no_05": "Sinkhole de Mayo 2016 New Orleans 05.jpg",
  "sinkhole_no_42": "Sinkhole de Mayo 2016 New Orleans 42.jpg",
  "gpr_in_use": "Ground Penetrating Radar in use.jpg",
  "gpr_ctbto": "Using ground-penetrating radar - Flickr - The Official CTBTO Photostream.jpg",
  "gpr_photo": "Ground-penetrating radar (GPR).jpg",
  "seoul_hapjeong": "Hapjeong (197719473).jpeg",
  "seoul_nowon_1": "Nowon Cultural Street at Night 01.jpg",
  "seoul_nowon_2": "Nowon Cultural Street at Night 02.jpg",
  "seoul_nowon_3": "Nowon Cultural Street at Night 03.jpg",
  "night_street_empty": "DZ6 1685 Quiet city street at night lined with glowing streetlights and empty lanes stretching toward distant buildings.jpg",
  "sinkhole_patched": "2022-07-14 06 00 46 A recently patched sinkhole along Lochatong Road in the Mountainview section of Ewing Township, Mercer County, New Jersey.jpg",
  "sinkhole_driveway": "2020-07-25 08 07 04 A small sink hole in a driveway along Old Dairy Road in the Franklin Farm section of Oak Hill, Fairfax County, Virginia.jpg",
  "manhole_cityhall": "Seoul-City.Hall-Manhole.cover.jpg",
  "manhole_namdaemun": "Seoul-Namdaemun Market-Manhole-01.jpg",
  "gpr_pd": "Ground Penetrating Radar (GPR) is a popular technique that is used in archeology to identiy areas of interest and potential (dcf1debf-6d1d-4557-a61f-a965091ed8a6).JPG",
}
def strip(s): return html.unescape(re.sub("<[^>]+>", "", s or "")).strip()
credits = {}
cp = os.path.join(OUT, "credits.json")
if os.path.exists(cp): credits = json.load(open(cp))
for key, title in TITLES.items():
    if len(sys.argv) > 1 and key not in sys.argv[1:]: continue
    if key in credits and os.path.exists(os.path.join(OUT, key + ".jpg")): continue
    q = urllib.parse.urlencode({"action": "query", "format": "json", "titles": "File:" + title, "prop": "imageinfo", "iiprop": "url|extmetadata", "iiurlwidth": 2400})
    req = urllib.request.Request("https://commons.wikimedia.org/w/api.php?" + q, headers={"User-Agent": "GroundWatchDeck/1.0 (contest proposal)"})
    for attempt in range(6):
        try:
            page = list(json.load(urllib.request.urlopen(req))["query"]["pages"].values())[0]; break
        except urllib.error.HTTPError as e:
            if e.code != 429: raise
            time.sleep(15 * (attempt + 1))
    ii = page["imageinfo"][0]; m = ii["extmetadata"]
    url = ii.get("thumburl") or ii["url"]
    for attempt in range(6):
        try:
            data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "GroundWatchDeck/1.0"})).read(); break
        except urllib.error.HTTPError as e:
            if e.code != 429: raise
            time.sleep(10 * (attempt + 1))
    time.sleep(3)
    open(os.path.join(OUT, key + ".jpg"), "wb").write(data)
    credits[key] = {"title": title, "page": ii["descriptionurl"], "artist": strip(m.get("Artist", {}).get("value")), "license": strip(m.get("LicenseShortName", {}).get("value"))}
    print(key, credits[key]["license"], "|", credits[key]["artist"][:40])
    json.dump(credits, open(cp, "w"), ensure_ascii=False, indent=2)
json.dump(credits, open(cp, "w"), ensure_ascii=False, indent=2)
