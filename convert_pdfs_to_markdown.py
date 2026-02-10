#!/usr/bin/env python3
"""
Script to convert downloaded PDFs to markdown using Datalab.to Python SDK.
Based on: https://documentation.datalab.to/
"""

import os
import sys
import argparse
import asyncio
from pathlib import Path
from tqdm.asyncio import tqdm
from dotenv import load_dotenv
from datalab_sdk import ConvertOptions
from datalab_sdk.client import AsyncDatalabClient

# Load environment variables
load_dotenv()


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Convert documents (PDF, epub, html) to Markdown using Datalab.to API.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert PDFs (default)
  python convert_pdfs_to_markdown.py -i path/to/files

  # Convert ePubs
  python convert_pdfs_to_markdown.py -i path/to/epubs -f epub
  
  # Convert all supported formats
  python convert_pdfs_to_markdown.py -i path/to/files -f all
        """
    )
    
    parser.add_argument(
        '-i', '--input',
        required=True,
        help='Input directory containing files'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output directory for Markdown files (default: input directory with "_Markdown" suffix)'
    )

    parser.add_argument(
        '-f', '--format',
        default='pdf',
        choices=['pdf', 'epub', 'html', 'all'],
        help='Input file format to convert (default: pdf)'
    )
    
    args = parser.parse_args()
    
    # Set up default output path based on input directory
    input_path = Path(args.input)
    
    if not args.output:
        # Remove trailing slash and get parent + name
        if input_path.name:
            args.output = str(input_path.parent / f"{input_path.name}_Markdown")
        else:
            args.output = str(input_path / "Markdown")
    
    return args


async def process_file(file_path, args, pbar, semaphore, client):
    """Process a single file asynchronously using the Datalab.to SDK."""
    async with semaphore:
        file_name = file_path.stem
        markdown_file = Path(args.output) / f"{file_name}.md"
        
        # Skip if already converted
        if markdown_file.exists():
            pbar.set_description(f"Skipping (exists): {file_name[:40]}")
            pbar.update(1)
            return (True, file_path.name, "Skipped (exists)")
        
        try:
            pbar.set_description(f"Processing: {file_name[:40]}")

            # Use Datalab async SDK client to convert the document to markdown
            options = ConvertOptions(
                output_format="markdown",
                mode="balanced",
            )

            result = await client.convert(
                file_path=str(file_path),
                options=options,
            )

            markdown_content = getattr(result, "markdown", None)
            if not markdown_content:
                raise RuntimeError("No markdown content returned from Datalab API")

            # Ensure output directory exists and write markdown file
            markdown_file.parent.mkdir(parents=True, exist_ok=True)
            markdown_file.write_text(markdown_content, encoding="utf-8")

            pbar.set_description(f"✓ Converted: {file_name[:40]}")
            pbar.update(1)
            return (True, file_path.name, "Converted")

        except Exception as e:
            error_msg = str(e)[:200]  # Truncate long error messages
            pbar.set_description(f"✗ Failed: {file_name[:40]}")
            pbar.update(1)
            return (False, file_path.name, error_msg)


async def main():
    """Main function to convert files to markdown."""
    args = parse_args()

    # Get API key from environment (support both DATALAB_API_KEY and legacy MARKER_PDF_KEY)
    api_key = os.getenv("DATALAB_API_KEY") or os.getenv("MARKER_PDF_KEY")

    if not api_key or api_key in ("your_api_key_here", ""):
        print("ERROR: API key not found or not configured in .env file")
        print("Please:")
        print("  1. Create a .env file with your Datalab API credentials")
        print("  2. Add either:")
        print("       DATALAB_API_KEY=your_actual_api_key_here")
        print("     or")
        print("       MARKER_PDF_KEY=your_actual_api_key_here")
        sys.exit(1)

    # Ensure DATALAB_API_KEY is set for the Datalab SDK
    os.environ["DATALAB_API_KEY"] = api_key

    # Create output directory
    os.makedirs(args.output, exist_ok=True)

    print(f"Input directory: {args.input}")
    print(f"Output directory: {args.output}")
    print(f"Format: {args.format}")
    print("Using Datalab.to Conversion API for conversion...")
    
    # Get files based on format
    input_path = Path(args.input)
    files_to_convert = []
    
    extensions = []
    if args.format == 'all':
        extensions = ['.pdf', '.epub', '.html', '.htm']
    elif args.format == 'epub':
        extensions = ['.epub']
    elif args.format == 'html':
        extensions = ['.html', '.htm']
    else:  # pdf
        extensions = ['.pdf']
        
    for ext in extensions:
        files_to_convert.extend(list(input_path.glob(f"*{ext}")))
        files_to_convert.extend(list(input_path.glob(f"*{ext.upper()}")))
    
    # Deduplicate in case of case overlap
    files_to_convert = list(set(files_to_convert))
    
    print(f"\nFound {len(files_to_convert)} files to convert\n")
    
    if not files_to_convert:
        print(f"No {args.format} files found in the input directory")
        return
    
    # Limit concurrency prevents overwhelming the API or local resources
    # Using 10 concurrent requests
    semaphore = asyncio.Semaphore(10)
    
    # Create progress bar
    pbar = tqdm(total=len(files_to_convert), desc="Converting files", unit="file")

    # Use a single shared AsyncDatalabClient for all conversions
    async with AsyncDatalabClient(api_key=api_key) as client:
        tasks = [
            process_file(file_path, args, pbar, semaphore, client)
            for file_path in files_to_convert
        ]
        
        results = await asyncio.gather(*tasks)
    
    pbar.close()
    
    successful = [name for success, name, _ in results if success]
    failed = [(name, msg) for success, name, msg in results if not success]
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"Conversion Summary:")
    print(f"  Successful: {len(successful)}")
    print(f"  Failed: {len(failed)}")
    print(f"  Total: {len(files_to_convert)}")
    print(f"  Markdown files saved to: {args.output}")
    
    if failed:
        print(f"\nFailed conversions (first 10):")
        for filename, error in failed[:10]:
            print(f"  - {filename[:60]}")
            print(f"    Error: {error[:100]}")
        if len(failed) > 10:
            print(f"  ... and {len(failed) - 10} more failures")

if __name__ == "__main__":
    asyncio.run(main())
