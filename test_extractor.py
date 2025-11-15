#!/usr/bin/env python3
"""
Test script for Berkshire Hathaway Extractor
Runs a limited crawl to verify functionality
"""

from berkshire_extractor import BerkshireExtractor

def main():
    print("Running test with limited crawl (3 pages)...")
    print("-" * 60)

    # Initialize extractor
    extractor = BerkshireExtractor(
        base_url="https://www.berkshirehathaway.com/",
        output_dir="berkshire_materials_test"
    )

    # Run limited crawl for testing
    extractor.crawl(max_pages=3)

    print("\n" + "=" * 60)
    print("Test completed!")
    print("Check the 'berkshire_materials_test' directory for results.")
    print("=" * 60)

if __name__ == "__main__":
    main()
