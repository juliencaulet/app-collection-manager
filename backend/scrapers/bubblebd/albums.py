"""
Bubble BD Album Scraper.

This script provides functionality to scrape album information from bubblebd.com.
It extracts details like title, authors, publication info, and cover images.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from pathlib import Path
import logging
import json
import os
from PIL import Image
from io import BytesIO
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class BubbleBDAlbum:
    """Data class to store album information."""
    title: str
    isbn: str
    authors: List[str]
    publisher: str
    publication_date: str
    pages: int
    genre: List[str]
    language: str
    series_number: Optional[int]
    status: str
    notes: str
    cover_url: str
    cover_path: Optional[str]  # Local path to the cover image
    synopsis: str
    series_title: str
    total_volumes: Optional[int]

class BubbleBDScraper:
    """Scraper for Bubble BD albums."""
    
    def __init__(self, covers_dir: Optional[Path] = None):
        """
        Initialize the scraper with default headers and covers directory.
        
        Args:
            covers_dir: Directory to store cover images. If None, uses default path.
        """
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.base_url = "https://www.bubblebd.com"
        
        # Set up covers directory - now relative to backend root
        if covers_dir is None:
            self.covers_dir = Path(__file__).parent.parent.parent / "static" / "covers" / "books"
        else:
            self.covers_dir = covers_dir
        self.covers_dir.mkdir(parents=True, exist_ok=True)

    def _download_cover(self, url: str, isbn: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Download and save a cover image.
        
        Args:
            url: URL of the cover image
            isbn: ISBN of the book for filename
            
        Returns:
            Tuple of (relative_path, absolute_path) to the saved image, or (None, None) if failed
        """
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            # Generate a unique filename using ISBN and URL hash
            url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
            filename = f"{isbn}_{url_hash}.jpg"
            relative_path = f"static/covers/books/{filename}"  # Path relative to backend root
            absolute_path = self.covers_dir / filename
            
            # Process and save the image
            img = Image.open(BytesIO(response.content))
            img.save(absolute_path, "JPEG", quality=85, optimize=True)
            
            logger.info(f"Saved cover image to {absolute_path}")
            return relative_path, str(absolute_path)
            
        except Exception as e:
            logger.error(f"Error downloading cover image: {e}")
            return None, None

    def _parse_date(self, date_str: str) -> str:
        """Convert French date to ISO format."""
        months_fr = {
            'janv.': '01', 'févr.': '02', 'mars': '03', 'avr.': '04',
            'mai': '05', 'juin': '06', 'juil.': '07', 'août': '08',
            'sept.': '09', 'oct.': '10', 'nov.': '11', 'déc.': '12'
        }
        
        parts = date_str.split()
        day = parts[0].zfill(2)
        month = months_fr[parts[1]]
        year = parts[2]
        
        return f"{year}-{month}-{day}"

    def _extract_series_info(self, soup: BeautifulSoup) -> tuple[str, Optional[int]]:
        """Extract series title and total volumes."""
        series_info = soup.find('h1', class_='series-title')
        if not series_info:
            return "", None
            
        # Try to find total volumes info
        volume_info = soup.find(text=re.compile(r'Tome \d+/\d+'))
        total_volumes = None
        if volume_info:
            match = re.search(r'Tome \d+/(\d+)', volume_info)
            if match:
                total_volumes = int(match.group(1))
                
        return series_info.text.strip(), total_volumes

    def _extract_series_number(self, soup: BeautifulSoup) -> Optional[int]:
        """Extract the volume number from the title or breadcrumb."""
        volume_info = soup.find(text=re.compile(r'Tome (\d+)'))
        if volume_info:
            match = re.search(r'Tome (\d+)', volume_info)
            if match:
                return int(match.group(1))
        return None

    def scrape_album(self, url: str, download_cover: bool = True) -> BubbleBDAlbum:
        """
        Scrape album information from a Bubble BD album page.
        
        Args:
            url: The URL of the album page
            download_cover: Whether to download and save the cover image
            
        Returns:
            BubbleBDAlbum: Object containing the scraped album information
            
        Raises:
            requests.RequestException: If the page cannot be fetched
            ValueError: If required information cannot be found
        """
        logger.info(f"Scraping album from URL: {url}")
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract basic information
            title = soup.find('h1').text.strip()
            
            # Extract characteristics table information
            char_table = soup.find('table', {'class': 'characteristics'})
            char_data = {}
            if char_table:
                for row in char_table.find_all('tr'):
                    key = row.find('td').text.strip()
                    value = row.find_all('td')[1].text.strip()
                    char_data[key] = value
            
            # Extract authors
            authors = []
            authors_section = soup.find(text=re.compile(r'Auteurs'))
            if authors_section:
                author_links = authors_section.find_next('td').find_all('a')
                authors = [a.text.strip() for a in author_links]
            
            # Extract ISBN and other details
            isbn = char_data.get('ISBN/EAN', '')
            publisher = char_data.get('Editeur', 'Delcourt')  # Default to Delcourt if not found
            publication_date = self._parse_date(char_data.get('Date de parution', ''))
            pages = int(char_data.get('Nombre de pages', '0'))
            
            # Extract genres/themes
            genres = []
            themes_section = soup.find(text=re.compile(r'Thèmes'))
            if themes_section:
                genre_links = themes_section.find_next('td').find_all('a')
                genres = [g.text.strip() for g in genre_links]
            
            # Extract series information
            series_title, total_volumes = self._extract_series_info(soup)
            series_number = self._extract_series_number(soup)
            
            # Extract synopsis
            synopsis = ""
            synopsis_section = soup.find('h2', text=re.compile(r'Résumé'))
            if synopsis_section:
                synopsis = synopsis_section.find_next('div').text.strip()
            
            # Extract cover URL and download if requested
            cover_url = ""
            cover_path = None
            cover_img = soup.find('img', {'class': 'cover'})
            if cover_img and 'src' in cover_img.attrs:
                cover_url = cover_img['src']
                if not cover_url.startswith('http'):
                    cover_url = f"{self.base_url}{cover_url}"
                
                if download_cover and isbn:
                    relative_path, _ = self._download_cover(cover_url, isbn)
                    if relative_path:
                        cover_path = relative_path
            
            return BubbleBDAlbum(
                title=title,
                isbn=isbn,
                authors=authors,
                publisher=publisher,
                publication_date=publication_date,
                pages=pages,
                genre=genres,
                language='fr',  # Default to French for Bubble BD
                series_number=series_number,
                status='wanted',  # Default status
                notes=f"Tome {series_number}/{total_volumes if total_volumes else '?'} de la série {series_title}",
                cover_url=cover_url,
                cover_path=cover_path,
                synopsis=synopsis,
                series_title=series_title,
                total_volumes=total_volumes
            )
            
        except requests.RequestException as e:
            logger.error(f"Error fetching page: {e}")
            raise
        except Exception as e:
            logger.error(f"Error parsing page: {e}")
            raise ValueError(f"Could not parse album information: {e}")

    def save_to_json(self, album: BubbleBDAlbum, output_path: Path) -> None:
        """Save album information to a JSON file."""
        data = {
            "title": album.title,
            "isbn": album.isbn,
            "authors": album.authors,
            "publisher": album.publisher,
            "publication_date": album.publication_date,
            "pages": album.pages,
            "genre": album.genre,
            "language": album.language,
            "series_number": album.series_number,
            "status": album.status,
            "notes": album.notes,
            "cover_url": album.cover_url,
            "cover_path": album.cover_path,
            "synopsis": album.synopsis,
            "series_title": album.series_title,
            "total_volumes": album.total_volumes
        }
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"Saved album information to {output_path}")

def main():
    """Main function to demonstrate scraper usage."""
    # Example usage
    url = "https://www.bubblebd.com/arctica-tome-1-dix-mille-ans-sous-les-glaces/album/VPjKblGEza/OWCJBUiO7t"
    scraper = BubbleBDScraper()
    
    try:
        album = scraper.scrape_album(url, download_cover=True)
        # Update output path to use the backend's data directory
        output_path = Path(__file__).parent.parent.parent / "static" / "scraped" / "bubblebd" / f"{album.isbn}.json"
        scraper.save_to_json(album, output_path)
        logger.info("Scraping completed successfully!")
        
        if album.cover_path:
            logger.info(f"Cover image saved to: {album.cover_path}")
        
    except Exception as e:
        logger.error(f"Error during scraping: {e}")

if __name__ == "__main__":
    main() 