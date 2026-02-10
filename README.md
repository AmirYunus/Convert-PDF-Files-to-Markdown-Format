# PDF / EPUB / HTML to Markdown Converter

A Python script to convert PDFs, EPUBs, and HTML files to Markdown format using the [Datalab.to](https://datalab.to) Conversion API. The script processes multiple files asynchronously with progress tracking and error handling.

## Features

- ✅ Convert PDFs, EPUBs, and HTML files to Markdown
- ✅ Asynchronous processing for faster batch conversions
- ✅ Progress bar with real-time status updates
- ✅ Automatic skipping of already converted files
- ✅ Comprehensive error handling and reporting
- ✅ Support for custom input and output directories
- ✅ Uses Datalab.to API for high-quality document conversion

## Prerequisites

- Python 3.8 or higher
- A Datalab.to API key ([Get one here](https://datalab.to))

## Installation

1. **Clone or download this repository**

2. **Create a virtual environment** (recommended):
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up your API key**:
   - Create a `.env` file in the project root
   - Add your Datalab API key:
```bash
DATALAB_API_KEY=your_api_key_here
```

   Alternatively, you can use the legacy variable name:
```bash
MARKER_PDF_KEY=your_api_key_here
```

## Usage

### Basic Usage

Convert all PDFs in a directory (output will be saved to `<input_directory>_Markdown`):

```bash
python convert_pdfs_to_markdown.py -i path/to/pdf/directory
```

### Specify Output Directory

Convert PDFs and save to a custom output directory:

```bash
python convert_pdfs_to_markdown.py -i path/to/pdf/directory -o path/to/output/directory
```

### Convert Different File Types

Convert EPUB files:
```bash
python convert_pdfs_to_markdown.py -i path/to/epub/directory -f epub
```

Convert HTML files:
```bash
python convert_pdfs_to_markdown.py -i path/to/html/directory -f html
```

Convert all supported formats (PDF, EPUB, HTML):
```bash
python convert_pdfs_to_markdown.py -i path/to/mixed/directory -f all
```

## Command-Line Arguments

| Argument | Short | Required | Description |
|----------|-------|----------|-------------|
| `--input` | `-i` | Yes | Input directory containing files to convert |
| `--output` | `-o` | No | Output directory for Markdown files (default: `<input>_Markdown`) |
| `--format` | `-f` | No | File format to convert: `pdf`, `epub`, `html`, or `all` (default: `pdf`) |

## Examples

### Example 1: Convert PDFs in current directory
```bash
python convert_pdfs_to_markdown.py -i ./PDFs
```
Output: Creates `PDFs_Markdown/` directory with converted files

### Example 2: Convert with custom output location
```bash
python convert_pdfs_to_markdown.py -i ./documents -o ./markdown_output
```

### Example 3: Convert EPUB files
```bash
python convert_pdfs_to_markdown.py -i ./ebooks -f epub -o ./ebooks_markdown
```

## How It Works

1. **File Discovery**: The script scans the input directory for files matching the specified format(s)
2. **Async Processing**: Files are processed asynchronously (up to 10 concurrent conversions) using the Datalab.to API
3. **Progress Tracking**: Real-time progress bar shows conversion status for each file
4. **Error Handling**: Failed conversions are tracked and reported in the summary
5. **Skip Existing**: Already converted files (existing `.md` files) are automatically skipped

## Output

- Each converted file is saved as `<filename>.md` in the output directory
- The script prints a summary showing:
  - Number of successful conversions
  - Number of failed conversions
  - Location of output files
  - Error messages for any failures

## Error Handling

If a conversion fails, the script will:
- Continue processing other files
- Display an error message in the progress bar
- Include the error in the final summary report
- Preserve any successfully converted files

## API Rate Limits

The script uses a semaphore to limit concurrent requests to 10 at a time to avoid overwhelming the API. If you encounter rate limit errors, you can modify the `semaphore = asyncio.Semaphore(10)` line in the script to reduce concurrency.

## Troubleshooting

### "API key not found" error
- Ensure your `.env` file exists in the project root
- Verify the API key is set correctly: `DATALAB_API_KEY=your_key_here`
- Make sure `python-dotenv` is installed

### "No files found" message
- Check that the input directory path is correct
- Verify files have the correct extension (`.pdf`, `.epub`, `.html`, etc.)
- Ensure the `--format` flag matches your file types

### Conversion failures
- Check your API key is valid and has sufficient credits
- Verify the input files are not corrupted
- Review error messages in the summary output

## Dependencies

- `datalab-python-sdk`: Official Datalab.to Python SDK for API integration
- `python-dotenv`: Load environment variables from `.env` file
- `tqdm`: Progress bar for visual feedback

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed list of changes and version history.

## Support

For issues related to:
- **This script**: Open an issue in this repository
- **Datalab.to API**: Visit [Datalab.to Documentation](https://documentation.datalab.to/)
- **API Key issues**: Contact Datalab.to support

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.
