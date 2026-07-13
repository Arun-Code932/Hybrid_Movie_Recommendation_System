import os
import gdown

os.makedirs("models", exist_ok=True)

FILES = {
    "models/similarity.pkl": "1xh4YzKFBhaF7gvoljuBGUSrhl_ck9zWm",
    "models/collaborative_similarity.pkl": "1JS4lBp960Wm8PYNlgHloxKOa2CE3NmoY",
}

for path, file_id in FILES.items():

    if not os.path.exists(path):

        print(f"Downloading {os.path.basename(path)}...")

        url = f"https://drive.google.com/uc?id={file_id}"

        gdown.download(url, path, quiet=False)

print("✅ All models downloaded successfully.")