import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io
from dotenv import load_dotenv

load_dotenv()
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")
DRIVE_FOLDER_ID = os.getenv("DRIVE_FOLDER_ID")

credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=["https://www.googleapis.com/auth/drive"])
drive_service = build("drive", "v3", credentials=credentials)

def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and parsed.scheme in {"http", "https"}

async def fetch(session, url):
    try:
        async with session.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"}) as response:
            return await response.text()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

async def get_links_and_images(html, base_url):
    """Extracts all valid links and images from a webpage."""
    soup = BeautifulSoup(html, "html.parser")
    links, images = set(), set()
    
    for a_tag in soup.find_all("a", href=True):
        link = urljoin(base_url, a_tag["href"])
        if is_valid_url(link):
            links.add(link)
    
    for img_tag in soup.find_all("img", src=True):
        img_url = urljoin(base_url, img_tag["src"])
        if is_valid_url(img_url):
            images.add(img_url)
    
    return links, images

async def save_to_drive(data, file_name, mime_type):
    file_metadata = {"name": file_name, "parents": [DRIVE_FOLDER_ID]}
    media = MediaIoBaseUpload(io.BytesIO(data.encode("utf-8")), mimetype=mime_type)
    drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()

async def save_data(url, text, images, session):
    domain = urlparse(url).netloc.replace(".", "_")
    
    await save_to_drive(text, f"{domain}_content.txt", "text/plain")
    
    for img_url in images:
        img_name = os.path.basename(urlparse(img_url).path)
        try:
            async with session.get(img_url) as img_resp:
                img_data = await img_resp.read()
                media = MediaIoBaseUpload(io.BytesIO(img_data), mimetype="image/jpeg")
                file_metadata = {"name": img_name, "parents": [DRIVE_FOLDER_ID]}
                drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        except Exception as e:
            print(f"Error downloading image {img_url}: {e}")

async def crawl(start_url, max_depth=2, visited=None, session=None):
    """Recursively crawls web pages up to a max depth asynchronously."""
    if visited is None:
        visited = set()
    
    if max_depth < 0 or start_url in visited:
        return
    
    print(f"Crawling: {start_url}")
    visited.add(start_url)
    
    html = await fetch(session, start_url)
    if not html:
        return
    
    links, images = await get_links_and_images(html, start_url)
    await save_data(start_url, html, images, session)
    
    tasks = [crawl(link, max_depth - 1, visited, session) for link in links]
    await asyncio.gather(*tasks)

async def main():
    start_url = "https://www.harvard.edu/"  
    async with aiohttp.ClientSession() as session:
        await crawl(start_url, max_depth=2, visited=set(), session=session)

if __name__ == "__main__":
    asyncio.run(main())