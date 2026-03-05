"""
Download public domain historical photos from Wikimedia Commons for the
Lumarian and Scramble program guides.
"""

import urllib.request
import os

downloads = [
    # Lumarian: CRT phosphor coating, 1942, PD-Canada
    {
        "url": "https://upload.wikimedia.org/wikipedia/commons/4/49/Coating_CRTs_at_Research_Enterprises.jpg",
        "dest": os.path.join("static", "img", "instruments", "videomancer", "lumarian", "lumarian_historical_crt_coating.jpg"),
    },
    # Lumarian: CRT testing, 1942, PD-Canada
    {
        "url": "https://upload.wikimedia.org/wikipedia/commons/0/0b/Testing_CRTs_at_Research_Enterprises.jpg",
        "dest": os.path.join("static", "img", "instruments", "videomancer", "lumarian", "lumarian_historical_crt_testing.jpg"),
    },
    # Scramble: COMSTAR I communications satellite, 1976, PD-NASA/NARA
    {
        "url": "https://upload.wikimedia.org/wikipedia/commons/8/82/COMSTAR_I_SPACECRAFT_-_NARA_-_17446863.jpg",
        "dest": os.path.join("static", "img", "instruments", "videomancer", "scramble", "scramble_historical_comstar_satellite.jpg"),
    },
    # Scramble: 1982 satellite TV broadcast, CC0/Public Domain, Dutch National Archives
    {
        "url": "https://upload.wikimedia.org/wikipedia/commons/a/a2/De_Orbital_Test_Satellite_2_gericht_op_Europa._Reclameboodschap_via_Satellite_TV%2C_Bestanddeelnr_932-0135.jpg",
        "dest": os.path.join("static", "img", "instruments", "videomancer", "scramble", "scramble_historical_satellite_tv_1982.jpg"),
    },
]

for item in downloads:
    dest = item["dest"]
    if os.path.exists(dest):
        print(f"Skipping (already exists): {dest}")
        continue
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    print(f"Downloading: {item['url'][:80]}...")
    req = urllib.request.Request(item["url"], headers={"User-Agent": "Mozilla/5.0 (LZX docs bot)"})
    with urllib.request.urlopen(req) as resp, open(dest, "wb") as f:
        f.write(resp.read())
    size_kb = os.path.getsize(dest) / 1024
    print(f"  -> {dest} ({size_kb:.0f} KB)")

print("\nDone! All images downloaded.")
