# Scholarly Article Scraper

A comprehensive Python-based tool for searching and downloading academic papers from multiple scholarly sources including ArXiv, Semantic Scholar, IEEE Xplore, Google Scholar, and CrossRef.

## Features

- **Multiple Academic Sources**: Integrates with 5+ major academic databases and search engines
- **API-First Approach**: Uses official APIs when available for better reliability and data quality
- **Intelligent Organization**: Creates structured folders by research category and query
- **PDF Download**: Automatically downloads available PDFs with metadata
- **Duplicate Detection**: Removes duplicate papers based on title similarity
- **Rate Limiting**: Respects API limits and implements proper delays
- **Rich Metadata**: Saves comprehensive paper information (authors, abstracts, citations, venues)
- **Academic Focus**: Curated search terms for computer science, AI, and engineering domains

## Project Structure

```
scholarly-article-scraper/
├── enhanced_scholarly_scraper.py    # Main enhanced scraper with API integrations
├── scholarly_article_scraper.py     # Basic version with web scraping
├── AcademicSearchTerms.py           # Curated academic search terms by domain
├── requirements.txt                 # Python dependencies
├── README.md                       # This file
└── Academic_Papers/                # Output directory (created on first run)
    ├── machine_learning/
    ├── systems_computing/
    ├── cybersecurity/
    └── ...
```

## Quick Start

### Installation

1. **Clone or download the project files**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the enhanced scraper:**
   ```bash
   python enhanced_scholarly_scraper.py
   ```

### Basic Usage

1. **Select a research category** from the menu:
   - Machine Learning & AI
   - Systems Computing
   - Cybersecurity
   - Data Science
   - Hardware Systems
   - Software Engineering
   - Quantum Computing
   - Human-Computer Interaction

2. **Set download limits** (default: 3 papers per query)

3. **Wait for results** - the scraper will:
   - Search multiple academic sources
   - Download PDFs when available
   - Save metadata as JSON files
   - Organize everything in structured folders

## Configuration

### Custom Search Terms

Edit `AcademicSearchTerms.py` to add your own research domains:

```python
def get_custom_categories():
    return {
        'my_research_area': [
            'specific topic query 1',
            'specific topic query 2',
            # Add more queries...
        ]
    }
```

### API Configuration

The scraper works out-of-the-box with public APIs, but you can enhance it by:

- Adding API keys for higher rate limits (Semantic Scholar, etc.)
- Configuring institutional access for IEEE, ACM
- Adding proxy settings if needed

## Academic Sources

### API-Based Sources
- **ArXiv**: Open access preprints (CS, AI, Physics, Math)
- **Semantic Scholar**: AI-powered academic search with citation data
- **CrossRef**: Comprehensive DOI registry

### Web-Based Sources  
- **Google Scholar**: Comprehensive academic search
- **IEEE Xplore**: Engineering and computer science papers

## Output Structure

For each search query, the scraper creates:

```
Academic_Papers/
└── category_name/
    └── 01_query_description/
        ├── paper1.pdf
        ├── paper1_metadata.json
        ├── paper2.pdf
        ├── paper2_metadata.json
        └── query_summary.json
```

### Metadata Format

Each paper's metadata includes:
```json
{
  "title": "Paper Title",
  "authors": "Author1, Author2",
  "abstract": "Paper abstract...",
  "pdf_url": "Direct PDF link",
  "venue": "Conference/Journal",
  "year": 2024,
  "citations": 42,
  "source": "ArXiv",
  "query": "search query used"
}
```

## Research Domains

The scraper includes curated search terms for:

### Core Computer Science
- **Artificial Intelligence**: Deep learning, neural networks, computer vision, NLP
- **Machine Learning**: Optimization, reinforcement learning, generative models
- **Systems**: Distributed systems, cloud computing, databases, networks
- **Security**: Cryptography, intrusion detection, privacy technologies

### Specialized Areas
- **Quantum Computing**: Algorithms, hardware, error correction
- **Data Science**: Analytics, statistics, visualization
- **HCI**: User interfaces, accessibility, VR/AR
- **Hardware**: Computer architecture, processors, embedded systems

## Advanced Usage

### Command Line Options

```bash
# Run with specific category
python enhanced_scholarly_scraper.py --category machine_learning

# Set custom limits
python enhanced_scholarly_scraper.py --max-papers 5

# Custom search query
python enhanced_scholarly_scraper.py --query "transformer neural networks"
```

### Programmatic Usage

```python
from enhanced_scholarly_scraper import EnhancedScholarlyArticleScraper

scraper = EnhancedScholarlyArticleScraper(base_path='My_Papers')

# Search specific query
papers = scraper.search_all_sources('quantum machine learning', max_results_per_source=10)

# Download papers for a category
total_downloads = scraper.search_and_download_category('machine_learning', max_papers_per_query=5)
```

## Rate Limiting & Ethics

The scraper implements responsible practices:

- **API Rate Limits**: Respects official rate limits for each source
- **Random Delays**: Implements random delays between requests (1-10 seconds)
- **User-Agent Rotation**: Uses academic user agents
- **Respectful Scraping**: Only downloads openly available content
- **No Paywall Bypass**: Does not attempt to access paid content

## 🐛 Troubleshooting

### Common Issues

1. **Connection Errors**
   ```bash
   # Check network connectivity
   ping scholar.google.com
   ```

2. **Missing Dependencies**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **API Limits Exceeded**
   - Increase delays between requests
   - Use fewer concurrent searches
   - Try again later

4. **Empty Results**
   - Check search terms relevance
   - Verify academic source availability
   - Try broader search queries

### Debug Mode

Enable verbose logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- **New Academic Sources**: Add more APIs (PubMed, DBLP, etc.)
- **Better Parsing**: Improve metadata extraction
- **Search Optimization**: Enhance query generation
- **UI Interface**: Add web interface or GUI
- **Citation Analysis**: Add citation network features

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Format code
black *.py
```

## 📄 License

MIT License - feel free to use for academic and research purposes.

## 🙏 Acknowledgments

- **ArXiv** for providing open access preprints
- **Semantic Scholar** for AI-powered academic search
- **CrossRef** for DOI registry services
- **Academic Community** for open science initiatives

## 📞 Support

For issues or questions:
- Check the troubleshooting section
- Review API documentation for individual sources
- Ensure compliance with institutional policies
- Respect academic source terms of service

---

**Note**: This tool is for academic research purposes. Always respect copyright, terms of service, and institutional policies when downloading academic content.
