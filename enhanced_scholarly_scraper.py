import os
import time
import requests
import json
import random
import re
from datetime import datetime
from urllib.parse import quote_plus, urlencode
from bs4 import BeautifulSoup
import importlib.util

class EnhancedScholarlyArticleScraper:
    def __init__(self, base_path='Academic_Papers'):
        self.base_path = os.path.join(os.getcwd(), base_path)
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
        
        # Load search terms
        self.load_search_terms()
        
        # Academic APIs and sources
        self.academic_sources = {
            'arxiv': {
                'name': 'ArXiv',
                'api_url': 'http://export.arxiv.org/api/query',
                'search_function': self.search_arxiv,
                'rate_limit': 3  # seconds between requests
            },
            'semantic_scholar': {
                'name': 'Semantic Scholar',
                'api_url': 'https://api.semanticscholar.org/graph/v1/paper/search',
                'search_function': self.search_semantic_scholar,
                'rate_limit': 1
            },
            'crossref': {
                'name': 'CrossRef',
                'api_url': 'https://api.crossref.org/works',
                'search_function': self.search_crossref,
                'rate_limit': 1
            },
            'google_scholar': {
                'name': 'Google Scholar (Web)',
                'search_function': self.search_google_scholar_web,
                'rate_limit': 5
            },
            'ieee': {
                'name': 'IEEE Xplore (Web)',
                'search_function': self.search_ieee_web,
                'rate_limit': 3
            }
        }
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        })
    
    def load_search_terms(self):
        """Load search terms from AcademicSearchTerms.py if available."""
        try:
            spec = importlib.util.spec_from_file_location("AcademicSearchTerms", "AcademicSearchTerms.py")
            search_terms_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(search_terms_module)
            
            if hasattr(search_terms_module, 'get_all_academic_categories'):
                self.search_categories = search_terms_module.get_all_academic_categories()
                print(f"Loaded {len(self.search_categories)} academic categories")
            else:
                self.search_categories = self.get_default_categories()
                print("Using default academic categories")
                
        except Exception as e:
            print(f"Could not load AcademicSearchTerms.py: {e}")
            self.search_categories = self.get_default_categories()
    
    def get_default_categories(self):
        """Default academic categories if external file not available."""
        return {
            'machine_learning': [
                'transformer neural networks',
                'deep learning optimization',
                'computer vision CNN',
                'natural language processing',
                'reinforcement learning algorithms'
            ],
            'systems': [
                'distributed systems architecture',
                'cloud computing performance',
                'database systems optimization',
                'network protocols design',
                'operating systems kernels'
            ]
        }
    
    def search_arxiv(self, query, max_results=10):
        """Search ArXiv using their API."""
        papers = []
        try:
            params = {
                'search_query': f'all:{query}',
                'start': 0,
                'max_results': max_results,
                'sortBy': 'relevance',
                'sortOrder': 'descending'
            }
            
            url = f"{self.academic_sources['arxiv']['api_url']}?{urlencode(params)}"
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                # Parse XML response
                from xml.etree import ElementTree as ET
                root = ET.fromstring(response.content)
                
                # Extract papers
                for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                    title_elem = entry.find('{http://www.w3.org/2005/Atom}title')
                    summary_elem = entry.find('{http://www.w3.org/2005/Atom}summary')
                    
                    authors = []
                    for author in entry.findall('{http://www.w3.org/2005/Atom}author'):
                        name_elem = author.find('{http://www.w3.org/2005/Atom}name')
                        if name_elem is not None:
                            authors.append(name_elem.text)
                    
                    # Get PDF link
                    pdf_link = None
                    for link in entry.findall('{http://www.w3.org/2005/Atom}link'):
                        if link.get('type') == 'application/pdf':
                            pdf_link = link.get('href')
                            break
                    
                    if title_elem is not None and pdf_link:
                        paper = {
                            'title': title_elem.text.strip(),
                            'authors': ', '.join(authors),
                            'abstract': summary_elem.text.strip() if summary_elem is not None else '',
                            'pdf_url': pdf_link,
                            'source': 'ArXiv',
                            'query': query
                        }
                        papers.append(paper)
                
                print(f"  ArXiv: Found {len(papers)} papers")
        
        except Exception as e:
            print(f"  Error searching ArXiv: {str(e)}")
        
        return papers
    
    def search_semantic_scholar(self, query, max_results=10):
        """Search Semantic Scholar API."""
        papers = []
        try:
            params = {
                'query': query,
                'limit': max_results,
                'fields': 'title,authors,abstract,url,venue,year,citationCount,openAccessPdf'
            }
            
            response = self.session.get(
                self.academic_sources['semantic_scholar']['api_url'],
                params=params,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                
                for paper_data in data.get('data', []):
                    authors = [author.get('name', '') for author in paper_data.get('authors', [])]
                    
                    pdf_url = None
                    if paper_data.get('openAccessPdf'):
                        pdf_url = paper_data['openAccessPdf'].get('url')
                    
                    paper = {
                        'title': paper_data.get('title', ''),
                        'authors': ', '.join(authors),
                        'abstract': paper_data.get('abstract', ''),
                        'pdf_url': pdf_url,
                        'venue': paper_data.get('venue', ''),
                        'year': paper_data.get('year'),
                        'citations': paper_data.get('citationCount', 0),
                        'source': 'Semantic Scholar',
                        'query': query
                    }
                    papers.append(paper)
                
                print(f"  Semantic Scholar: Found {len(papers)} papers")
        
        except Exception as e:
            print(f"  Error searching Semantic Scholar: {str(e)}")
        
        return papers
    
    def search_crossref(self, query, max_results=10):
        """Search CrossRef API for academic papers."""
        papers = []
        try:
            params = {
                'query': query,
                'rows': max_results,
                'sort': 'relevance',
                'select': 'DOI,title,author,abstract,publisher,published-print,URL'
            }
            
            response = self.session.get(
                self.academic_sources['crossref']['api_url'],
                params=params,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                
                for item in data.get('message', {}).get('items', []):
                    title = ''
                    if 'title' in item and item['title']:
                        title = item['title'][0]
                    
                    authors = []
                    if 'author' in item:
                        for author in item['author']:
                            name_parts = []
                            if 'given' in author:
                                name_parts.append(author['given'])
                            if 'family' in author:
                                name_parts.append(author['family'])
                            if name_parts:
                                authors.append(' '.join(name_parts))
                    
                    paper = {
                        'title': title,
                        'authors': ', '.join(authors),
                        'abstract': item.get('abstract', ''),
                        'doi': item.get('DOI', ''),
                        'publisher': item.get('publisher', ''),
                        'year': item.get('published-print', {}).get('date-parts', [[None]])[0][0],
                        'url': item.get('URL', ''),
                        'source': 'CrossRef',
                        'query': query
                    }
                    papers.append(paper)
                
                print(f"  CrossRef: Found {len(papers)} papers")
        
        except Exception as e:
            print(f"  Error searching CrossRef: {str(e)}")
        
        return papers
    
    def search_google_scholar_web(self, query, max_results=10):
        """Search Google Scholar via web scraping."""
        papers = []
        try:
            search_url = f"https://scholar.google.com/scholar?q={quote_plus(query)}&num={max_results}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
            }
            
            response = self.session.get(search_url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                for result in soup.select('.gs_r.gs_or.gs_scl'):
                    title_elem = result.select_one('h3.gs_rt a')
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    url = title_elem.get('href', '')
                    
                    # Extract authors and venue
                    authors_elem = result.select_one('.gs_a')
                    authors_text = authors_elem.get_text(strip=True) if authors_elem else ''
                    
                    # Extract abstract
                    abstract_elem = result.select_one('.gs_rs')
                    abstract = abstract_elem.get_text(strip=True) if abstract_elem else ''
                    
                    # Check for PDF links
                    pdf_link = None
                    pdf_elem = result.select_one('a[href$=".pdf"]')
                    if pdf_elem:
                        pdf_link = pdf_elem.get('href')
                    
                    paper = {
                        'title': title,
                        'authors': authors_text.split(' - ')[0] if ' - ' in authors_text else authors_text,
                        'abstract': abstract,
                        'url': url,
                        'pdf_url': pdf_link,
                        'source': 'Google Scholar',
                        'query': query
                    }
                    papers.append(paper)
                
                print(f"  Google Scholar: Found {len(papers)} papers")
        
        except Exception as e:
            print(f"  Error searching Google Scholar: {str(e)}")
        
        return papers
    
    def search_ieee_web(self, query, max_results=10):
        """Search IEEE Xplore via web scraping."""
        papers = []
        try:
            search_url = f"https://ieeexplore.ieee.org/search/searchresult.jsp?queryText={quote_plus(query)}&highlight=true&returnType=SEARCH"
            
            response = self.session.get(search_url, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                for result in soup.select('.List-results-items')[:max_results]:
                    title_elem = result.select_one('h2 a')
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    url = f"https://ieeexplore.ieee.org{title_elem.get('href', '')}"
                    
                    # Extract authors
                    authors_elem = result.select_one('.author')
                    authors = authors_elem.get_text(strip=True) if authors_elem else ''
                    
                    # Extract abstract
                    abstract_elem = result.select_one('.description')
                    abstract = abstract_elem.get_text(strip=True) if abstract_elem else ''
                    
                    paper = {
                        'title': title,
                        'authors': authors,
                        'abstract': abstract,
                        'url': url,
                        'source': 'IEEE Xplore',
                        'query': query
                    }
                    papers.append(paper)
                
                print(f"  IEEE Xplore: Found {len(papers)} papers")
        
        except Exception as e:
            print(f"  Error searching IEEE Xplore: {str(e)}")
        
        return papers
    
    def download_pdf(self, paper, save_path):
        """Download PDF if available."""
        if not paper.get('pdf_url'):
            return None
        
        try:
            # Clean filename
            clean_title = re.sub(r'[\\/*?:"<>|]', '_', paper['title'])
            clean_title = clean_title[:80]  # Limit length
            filename = f"{clean_title}.pdf"
            
            file_path = os.path.join(save_path, filename)
            
            print(f"    Downloading PDF: {filename}")
            
            # Download with academic headers
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/pdf,*/*'
            }
            
            response = self.session.get(paper['pdf_url'], headers=headers, timeout=30, stream=True)
            response.raise_for_status()
            
            # Save PDF
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            file_size = os.path.getsize(file_path)
            print(f"      Downloaded: {file_size/1024:.1f} KB")
            
            return file_path
            
        except Exception as e:
            print(f"      Error downloading PDF: {str(e)}")
            return None
    
    def save_paper_metadata(self, paper, save_path):
        """Save paper metadata as JSON."""
        try:
            clean_title = re.sub(r'[\\/*?:"<>|]', '_', paper['title'])
            clean_title = clean_title[:80]
            metadata_file = os.path.join(save_path, f"{clean_title}_metadata.json")
            
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(paper, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"      Error saving metadata: {str(e)}")
    
    def search_all_sources(self, query, max_results_per_source=5):
        """Search all available academic sources."""
        all_papers = []
        
        print(f"\nSearching for: '{query}'")
        print("-" * 50)
        
        for source_key, source_info in self.academic_sources.items():
            try:
                papers = source_info['search_function'](query, max_results_per_source)
                all_papers.extend(papers)
                
                # Respectful delay
                time.sleep(source_info['rate_limit'])
                
            except Exception as e:
                print(f"  Error with {source_info['name']}: {str(e)}")
        
        # Remove duplicates based on title similarity
        unique_papers = self.deduplicate_papers(all_papers)
        
        print(f"\nTotal unique papers found: {len(unique_papers)}")
        return unique_papers
    
    def deduplicate_papers(self, papers):
        """Remove duplicate papers based on title similarity."""
        unique_papers = []
        
        for paper in papers:
            is_duplicate = False
            paper_title = paper['title'].lower().strip()
            
            for existing in unique_papers:
                existing_title = existing['title'].lower().strip()
                
                # Simple similarity check
                if abs(len(paper_title) - len(existing_title)) / max(len(paper_title), 1) < 0.2:
                    # Check for significant word overlap
                    paper_words = set(paper_title.split())
                    existing_words = set(existing_title.split())
                    
                    overlap = len(paper_words.intersection(existing_words))
                    total_words = len(paper_words.union(existing_words))
                    
                    if overlap / max(total_words, 1) > 0.7:
                        is_duplicate = True
                        break
            
            if not is_duplicate:
                unique_papers.append(paper)
        
        return unique_papers
    
    def search_and_download_category(self, category_name, max_papers_per_query=3):
        """Search and download papers for a specific category."""
        if category_name not in self.search_categories:
            print(f"Category '{category_name}' not found!")
            return 0
        
        queries = self.search_categories[category_name]
        total_downloads = 0
        
        # Create category folder
        category_path = os.path.join(self.base_path, category_name)
        if not os.path.exists(category_path):
            os.makedirs(category_path)
        
        print(f"\n{'='*60}")
        print(f"Processing category: {category_name.replace('_', ' ').title()}")
        print(f"Queries to process: {len(queries)}")
        print('='*60)
        
        for i, query in enumerate(queries, 1):
            print(f"\n[{i}/{len(queries)}] Processing query: {query}")
            
            # Search all sources
            papers = self.search_all_sources(query, max_results_per_source=5)
            
            if not papers:
                print("No papers found for this query.")
                continue
            
            # Create query subfolder
            clean_query = re.sub(r'[\\/*?:"<>|]', '_', query)
            query_path = os.path.join(category_path, f"{i:02d}_{clean_query[:30]}")
            if not os.path.exists(query_path):
                os.makedirs(query_path)
            
            # Download top papers
            papers_to_download = papers[:max_papers_per_query]
            downloaded_count = 0
            
            for j, paper in enumerate(papers_to_download, 1):
                print(f"  [{j}/{len(papers_to_download)}] {paper['title'][:50]}...")
                
                # Save metadata
                self.save_paper_metadata(paper, query_path)
                
                # Try to download PDF
                if self.download_pdf(paper, query_path):
                    downloaded_count += 1
                    total_downloads += 1
                
                # Brief delay between downloads
                time.sleep(random.uniform(1, 3))
            
            print(f"  Downloaded {downloaded_count} papers for this query")
            
            # Save query summary
            summary = {
                'query': query,
                'timestamp': datetime.now().isoformat(),
                'total_found': len(papers),
                'downloaded': downloaded_count,
                'papers': papers
            }
            
            summary_file = os.path.join(query_path, 'query_summary.json')
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            
            # Delay between queries
            time.sleep(random.uniform(3, 6))
        
        return total_downloads

def main():
    """Main function to run the scholarly article scraper."""
    scraper = EnhancedScholarlyArticleScraper()
    
    print("Enhanced Scholarly Article Scraper")
    print("=" * 50)
    
    # Show available categories
    categories = list(scraper.search_categories.keys())
    print(f"\nAvailable categories ({len(categories)}):")
    for i, category in enumerate(categories, 1):
        num_queries = len(scraper.search_categories[category])
        print(f"{i:2d}. {category.replace('_', ' ').title()} ({num_queries} queries)")
    
    try:
        # Get user selection
        choice = input(f"\nSelect category (1-{len(categories)}) or 'all' for all categories: ").strip()
        
        if choice.lower() == 'all':
            selected_categories = categories
        else:
            choice_num = int(choice) - 1
            if 0 <= choice_num < len(categories):
                selected_categories = [categories[choice_num]]
            else:
                print("Invalid choice. Exiting.")
                return
        
        # Get max papers per query
        max_papers = input("\nMax papers per query (default: 3): ").strip()
        max_papers = int(max_papers) if max_papers.isdigit() else 3
        
        # Start processing
        total_papers = 0
        for category in selected_categories:
            papers_downloaded = scraper.search_and_download_category(category, max_papers)
            total_papers += papers_downloaded
            
            if len(selected_categories) > 1:
                print(f"\nCompleted {category}: {papers_downloaded} papers downloaded")
                time.sleep(5)  # Longer delay between categories
        
        print(f"\n{'='*60}")
        print(f"Scraping complete!")
        print(f"Total papers downloaded: {total_papers}")
        print(f"Files saved to: {scraper.base_path}")
        
    except KeyboardInterrupt:
        print("\nScraping interrupted by user.")
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()
