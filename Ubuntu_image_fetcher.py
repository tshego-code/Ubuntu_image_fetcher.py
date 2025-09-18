"""
Ubuntu-Inspired Image Fetcher
---------------------------------
"I am because we are." – Ubuntu philosophy

This program lives by Ubuntu’s values:
🤝 Community – connecting to the web and sharing resources
🙏 Respect – handling errors with care, not crashes
📂 Sharing – organizing images for others to enjoy
⚡ Practicality – building a tool that serves a real need
"""

import os
import requests
from urllib.parse import urlparse
import hashlib

def fetch_images():
    print("🌍 Welcome to the Ubuntu Image Fetcher 🌍")
    print("In Ubuntu spirit, we connect, share, and respect.")
    print("👉 Enter multiple image URLs separated by commas (,)\n")

    # Ask user for URLs
    urls = input("Please enter image URLs: ").split(",")

    # Create a shared space for our fetched images
    save_dir = "Fetched_Images"
    os.makedirs(save_dir, exist_ok=True)

    # Keep track of downloaded images (avoid duplicates)
    downloaded_hashes = set()

    for url in urls:
        url = url.strip()
        if not url:
            continue

        try:
            # Reach out to the wider community (the web)
            response = requests.get(url, timeout=10, stream=True)
            response.raise_for_status()

            # --- Show Respect: check the file before trusting ---
            content_type = response.headers.get("Content-Type", "")
            content_length = response.headers.get("Content-Length", None)

            if "image" not in content_type:
                print(f"⚠️ With respect, skipping {url} (not an image)")
                continue

            if content_length and int(content_length) > 5 * 1024 * 1024:  # >5MB
                print(f"⚠️ With care, skipping {url} (too large: {content_length} bytes)")
                continue

            # Create a filename from the URL
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path) or "downloaded_image.jpg"
            filepath = os.path.join(save_dir, filename)

            # --- Sharing responsibly: avoid duplicates ---
            file_hash = hashlib.md5(response.content).hexdigest()
            if file_hash in downloaded_hashes:
                print(f"⚠️ Duplicate found, skipping {url}")
                continue
            downloaded_hashes.add(file_hash)

            # Save the image into our community folder
            with open(filepath, "wb") as f:
                f.write(response.content)

            print(f"✅ Shared successfully! Image saved as: {filepath}")

        # --- Respectful error handling ---
        except requests.exceptions.MissingSchema:
            print(f"⚠️ Invalid URL: {url}. Please include 'http://' or 'https://'.")
        except requests.exceptions.HTTPError as http_err:
            print(f"⚠️ HTTP error for {url}: {http_err}")
        except requests.exceptions.ConnectionError:
            print(f"⚠️ Could not connect to {url}.")
        except requests.exceptions.Timeout:
            print(f"⚠️ Connection timed out for {url}.")
        except Exception as e:
            print(f"⚠️ An unexpected issue occurred with {url}: {e}")

if __name__ == "__main__":
    fetch_images()
