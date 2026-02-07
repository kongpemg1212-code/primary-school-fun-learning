import os
import requests

IMAGE_DIR = 'assets/images'
os.makedirs(IMAGE_DIR, exist_ok=True)

IMAGES = {
    "spring_breeze.jpg": "https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=600",
    "summer_rain.jpg": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600",
    "autumn_frost.jpg": "https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?w=600",
    "winter_snow.jpg": "https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?w=600"
}

def download():
    for name, url in IMAGES.items():
        path = os.path.join(IMAGE_DIR, name)
        print(f"Downloading {name}...")
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                with open(path, 'wb') as f:
                    f.write(r.content)
                print(f"✅ Saved to {path} ({len(r.content)} bytes)")
            else:
                print(f"❌ Failed: Status {r.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    download()
