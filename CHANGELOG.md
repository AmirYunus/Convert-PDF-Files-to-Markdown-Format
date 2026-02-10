# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] - 2026-02-10

Enhanced API key configuration with legacy variable support and improved error messaging.

### Added
- Support for legacy `MARKER_PDF_KEY` environment variable alongside `DATALAB_API_KEY`
- Improved error messages with API key configuration guidance
- Enhanced file discovery with case-insensitive extension matching

### Changed
- Improved error handling for missing API keys
- Better validation of API key configuration

### Fixed
- N/A

## [1.1.0] - 2026-01-30

Added support for EPUB and HTML file formats, expanding conversion capabilities beyond PDFs.

### Added
- Support for EPUB file conversion
- Support for HTML file conversion
- Format selection via `--format` flag (pdf, epub, html, or all)
- Support for both `.html` and `.htm` file extensions
- Case-insensitive file extension matching

### Changed
- Updated README to reflect multi-format support
- Enhanced command-line help with format examples

### Fixed
- N/A

## [1.0.0] - 2026-01-25

Initial release with PDF to Markdown conversion support and asynchronous batch processing.

### Added
- Initial release of PDF to Markdown converter
- Support for converting PDF files to Markdown format using Datalab.to API
- Asynchronous processing with up to 10 concurrent conversions
- Progress bar with real-time status updates using tqdm
- Automatic skipping of already converted files
- Command-line interface with input and output directory options
- Comprehensive error handling and reporting
- Support for custom output directories
- Summary report showing successful and failed conversions

### Changed
- N/A

### Fixed
- N/A

[Unreleased]: https://github.com/AmirYunus/Convert-PDF-Files-to-Markdown-Format/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/AmirYunus/Convert-PDF-Files-to-Markdown-Format/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/AmirYunus/Convert-PDF-Files-to-Markdown-Format/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/AmirYunus/Convert-PDF-Files-to-Markdown-Format/releases/tag/v1.0.0
