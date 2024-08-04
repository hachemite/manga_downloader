import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Base URL of the manga site
base_url = "https://lekmanga.net/manga/manga_name/" #the manga_name can be changed or you can change even the link or the website but there are probability not working I will fix next time


# Range of chapters to download
start_chapter = 1 # change the begining as you want 
end_chapter = 374  # change the ending as you want
# Directory to save the images
save_dir = "berserk_images"

# Create the directory if it doesn't exist
os.makedirs(save_dir, exist_ok=True)

def download_image(img_url, save_path):
    try:
        response = requests.get(img_url)
        response.raise_for_status()  # Check for HTTP request errors
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {img_url} to {save_path}")
    except Exception as e:
        print(f"Failed to download {img_url}: {e}")

def download_images_from_chapter(chapter_url, chapter):
    try:
        response = requests.get(chapter_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find all image tags
        img_tags = soup.find_all('img')
        for img_tag in img_tags:
            img_url = img_tag.get('src')
            if img_url and (img_url.endswith('.png') or img_url.endswith('.jpg')):
                # Create a full URL if the image URL is relative
                full_img_url = urljoin(base_url, img_url)
                img_name = os.path.basename(full_img_url)
                save_path = os.path.join(save_dir, f"chapter_{chapter}_{img_name}")
                download_image(full_img_url, save_path)
    except Exception as e:
        print(f"Failed to process chapter {chapter}: {e}")

for chapter in range(start_chapter, end_chapter + 1):
    chapter_url = f"{base_url}{chapter}/"
    try:
        response = requests.get(chapter_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find all sub-chapter links
        sub_chapter_links = soup.select('a[href*="{}/"]'.format(chapter))
        for link in sub_chapter_links:
            sub_chapter_url = urljoin(base_url, link.get('href'))
            print(f'Crawling sub-chapter: {sub_chapter_url}')
            download_images_from_chapter(sub_chapter_url, chapter)
    except Exception as e:
        print(f"Failed to process chapter {chapter}: {e}")

print('Done!')
