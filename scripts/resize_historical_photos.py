"""
Resize downloaded historical photos to web-appropriate sizes.
"""
from PIL import Image
import os

files = [
    ("static/img/instruments/videomancer/scramble/scramble_historical_comstar_satellite.jpg", 800),
    ("static/img/instruments/videomancer/scramble/scramble_historical_satellite_tv_1982.jpg", 800),
    ("static/img/instruments/videomancer/lumarian/lumarian_historical_crt_coating.jpg", 800),
    ("static/img/instruments/videomancer/lumarian/lumarian_historical_crt_testing.jpg", 800),
]

for path, max_dim in files:
    if not os.path.exists(path):
        print(f"Not found: {path}")
        continue
    img = Image.open(path)
    orig_size = os.path.getsize(path)
    w, h = img.size
    if max(w, h) > max_dim:
        if w > h:
            new_w = max_dim
            new_h = int(h * max_dim / w)
        else:
            new_h = max_dim
            new_w = int(w * max_dim / h)
        img = img.resize((new_w, new_h), Image.LANCZOS)
    img.save(path, quality=85, optimize=True)
    new_size = os.path.getsize(path)
    print(f"{path}: {orig_size//1024}KB -> {new_size//1024}KB ({img.size[0]}x{img.size[1]})")

print("\nDone!")
