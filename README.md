# DRM & Media Tool

Utility To Get Keys, Decryption, and File Merging

# Setup

- Install Python (above 3.5 is Recommended)
- Upgrade Pip and install setuptools, wheel and py2exe

```
 python -m pip install --upgrade pip
 python -m pip install -U pip setuptools wheel py2exe
```

- Install all required Packages from requirements.txt

```
pip install -U "https://rajeshwaran2001.github.io/Pyinstaller/x86_64/pyinstaller-6.3.0-py3-none-any.whl" -r requirements.txt
pip install -r requirements.txt
```

> If You Don't want Firebase in your Version ( Reduce 10 MB of exe) Remove firebase-admin from requirements.txt and Follow Instructions to Remove Firebase Code

# Build EXE

- Create a .env File under assets dir with the below values

```
API_URL = < API URL >
X_API_KEY = < API KEY >
```

> Firebase Is Added in the original Version to create a new service account key from the Firebase console and Store that file inside the assets dir

- Run update_version.py to update the version

```
python update_version.py -c < Channel Name>
```

- To Build Exe

```
pyinstaller --onefile --add-data "assets;assets" --name="DRM & Media Tool" --windowed --icon=assets\\logo.ico main.py --noconsole
```

# Instructions to Remove Firebase Code

To remove the Firebase-related code from DRM & Media Tool application, follow these steps:

- Remove the import statements for Firebase:

```
# Remove these lines

from firebase_admin import credentials, firestore, initialize_app
from datetime import datetime

```

- Remove the following lines where Firebase is initialized and the event data is added to the Firestore database:

```
key_path = os.path.join(current_dir, 'assets', 'serviceAccountKey.json')
cred = credentials.Certificate(key_path)
firebase_app = initialize_app(cred)
db = firestore.client()

current_datetime = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
event_data = {
    'pssh': pssh,
    'license_url': license_url,
    'movie_name': name,
    'keys': keys if "keys" in data else [],
    'datetime': current_datetime,
}

events_ref = db.collection('events')
events_ref.add(event_data)

self.info_logger.info("Key Added to Global Db")

```

# Future Plans

We have exciting plans for the future development of this project. Here's a glimpse of what's coming:

- **Feature:** Include Support to decrypt Webm Files.
- **Enhancement:** Include FFmpeg, mp4decrypt and Shaka packager.
- **Upcoming:** Include Yt-dlp to Download files.

I welcome contributions and feedback on these future plans. If you'd like to get involved or share your thoughts, please [open an issue](https://github.com/Rajeshwaran2001/DRM-Media-Tool/issues) or [reach out to me](discordapp.com/users/1138389183451381803).

# Reference

https://stackoverflow.com/questions/9913032/how-can-i-extract-audio-from-video-with-ffmpeg

https://plainenglish.io/blog/pyinstaller-exe-false-positive-trojan-virus-resolved-b33842bd3184

https://github.com/joeldcosta/pyinstaller
