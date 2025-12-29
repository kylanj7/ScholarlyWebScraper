#!/usr/bin/env python3
"""
Setup script for Scholarly Article Scraper
Handles installation and initial configuration
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 7):
        print("ERROR: Python 3.7+ is required")
        print(f"   Current version: {platform.python_version()}")
        return False
    print(f"Python {platform.python_version()} detected")
    return True

def install_requirements():
    """Install required Python packages."""
    print("\nInstalling Python dependencies...")
    
    # Try minimal requirements first
    requirements_files = [
        'requirements-minimal.txt',
        'requirements.txt'
    ]
    
    for req_file in requirements_files:
        if os.path.exists(req_file):
            try:
                print(f"   Installing from {req_file}...")
                subprocess.check_call([
                    sys.executable, '-m', 'pip', 'install', '-r', req_file
                ])
                print(f"Successfully installed dependencies from {req_file}")
                return True
            except subprocess.CalledProcessError:
                print(f"Failed to install from {req_file}")
                continue
    
    print("Could not install dependencies from any requirements file")
    return False

def create_directories():
    """Create necessary output directories."""
    print("\nCreating output directories...")
    
    directories = [
        'Academic_Papers',
        'Academic_Papers/downloads',
        'Academic_Papers/metadata'
    ]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"Created directory: {directory}")
        except Exception as e:
            print(f"Failed to create directory {directory}: {e}")
            return False
    
    return True

def verify_installation():
    """Verify that all required modules can be imported."""
    print("\nVerifying installation...")
    
    required_modules = [
        'requests',
        'bs4',
        'lxml'
    ]
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"{module} imported successfully")
        except ImportError:
            print(f"Failed to import {module}")
            return False
    
    return True

def run_test_search():
    """Run a quick test search to verify functionality."""
    print("\nRunning test search...")
    
    try:
        # Import the scraper
        from enhanced_scholarly_scraper import EnhancedScholarlyArticleScraper
        
        # Create scraper instance
        scraper = EnhancedScholarlyArticleScraper(base_path='test_output')
        
        # Run a simple search
        papers = scraper.search_all_sources('machine learning', max_results_per_source=2)
        
        if papers:
            print(f"Test search successful - found {len(papers)} papers")
            
            # Clean up test output
            import shutil
            if os.path.exists('test_output'):
                shutil.rmtree('test_output')
                
            return True
        else:
            print("Test search returned no results (this may be normal)")
            return True
            
    except Exception as e:
        print(f"Test search failed: {e}")
        return False

def main():
    """Main setup function."""
    print("Scholarly Article Scraper Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("\nSetup failed during dependency installation")
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        print("\nSetup failed during directory creation")
        sys.exit(1)
    
    # Verify installation
    if not verify_installation():
        print("\nSetup failed during verification")
        sys.exit(1)
    
    # Run test search
    if not run_test_search():
        print("\nSetup completed with warnings")
    else:
        print("\nSetup completed successfully!")
    
    print("\nReady to use!")
    print("   Run: python enhanced_scholarly_scraper.py")
    print("   Or:  python scholarly_article_scraper.py")
    
    # Show next steps
    print("\nNext Steps:")
    print("   1. Review README.md for detailed usage")
    print("   2. Edit AcademicSearchTerms.py to customize search terms")
    print("   3. Run the scraper and select your research domain")

if __name__ == "__main__":
    main()
