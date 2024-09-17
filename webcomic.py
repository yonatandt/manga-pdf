import requests
from bs4 import BeautifulSoup
import img2pdf
import os

def download_images_to_pdf(url, chapter):
  """
  Downloads images from a web page and groups them into a PDF file.

  Args:
    url: The URL of the web page.
    chapter: The string name of the chapter.
  """

  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')

  image_urls = []
  for img in soup.find_all('img', class_="pages__img"):
    src = img['src']
    if src and src[-1]=='\r':
      src = src[:-1]
    image_urls.append(src)

  if not image_urls:
    print(f"No images found for chapter: {chapter}")
    return

  images = []
  print(f"Downloading {len(image_urls)} images...")
  try:
    for url in image_urls:
        if not url:
          continue
        response = requests.get(url)
        images.append(response.content)
  except Exception as e:
    print(f"Failed to download image: {e}")
    return

  pdf_bytes = img2pdf.convert(images)

  print("Creating PDF...")

  with open(f"webcomic/{chapter}.pdf", "wb") as f:
    f.write(pdf_bytes)

  print(f"PDF created successfully: {chapter}.pdf")

if __name__ == "__main__":
  with open("chapters-w.json", "r") as f:
    chapters = f.readlines()

  for line in chapters:
    try:
      if line.startswith('//'):
        print(f"skipping {line}")
        continue
      url, chapter = line.strip().split(">")
      url = url[1:-1]
      print(f"Downloading url: {url}, chapter: {chapter}")
      download_images_to_pdf(url, chapter)
    except ValueError:
      print(f"Invalid line format: {line.strip()}")
