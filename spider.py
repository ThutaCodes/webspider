import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import aiofiles
import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv
from googleapiclient.http import MediaFileUpload

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

async def save_to_drive(file_path, file_name, mime_type):
    """Uploads a file to Google Drive."""
    file_metadata = {"name": file_name, "parents": [DRIVE_FOLDER_ID]}
    media = MediaFileUpload(file_path, mimetype=mime_type)
    drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()

async def save_data(url, text, images):
    domain = urlparse(url).netloc.replace(".", "_")
    folder = f"data/{domain}"
    os.makedirs(folder, exist_ok=True)
    
    text_file = f"{folder}/content.txt"
    async with aiofiles.open(text_file, "w", encoding="utf-8") as f:
        await f.write(text)
    await save_to_drive(text_file, f"{domain}_content.txt", "text/plain")
    
    for img_url in images:
        img_name = os.path.basename(urlparse(img_url).path)
        img_path = f"{folder}/{img_name}"
        async with aiofiles.open(img_path, "wb") as f:
            async with aiohttp.ClientSession() as session:
                async with session.get(img_url) as img_resp:
                    await f.write(await img_resp.read())
        await save_to_drive(img_path, img_name, "image/jpeg")

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
    await save_data(start_url, html, images)
    
    tasks = [crawl(link, max_depth - 1, visited, session) for link in links]
    await asyncio.gather(*tasks)

async def main():
    start_url = "https://www.icrc.org/en/where-we-work/myanmar"  
    async with aiohttp.ClientSession() as session:
        await crawl(start_url, max_depth=2, visited=set(), session=session)

if __name__ == "__main__":
    asyncio.run(main())
