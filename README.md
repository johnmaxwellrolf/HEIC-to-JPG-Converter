# HEIC to JPG Converter

A fast, user-friendly Windows desktop application for converting HEIC/HEIF photos to JPG format with professional branding and modern interface.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Features

✨ **Easy to Use**
- Drag & drop multiple HEIC files
- Modern, intuitive interface
- Professional branding

🖼️ **Image Processing**
- Convert HEIC/HEIF to JPG
- Adjustable quality (1-100%)
- Batch processing support
- Network drive & UNC path support

⚙️ **Flexible**
- Save to custom location or source folder
- Automatic duplicate handling
- Optimized file compression

🚀 **No Dependencies**
- Completely standalone (Python not required)
- All dependencies bundled
- Works on Windows 10 & 11 (64-bit)

## Installation

### Quick Start (Recommended)
1. Download the latest release from the [Releases](https://github.com/johnmaxwellrolf/HEIC-to-JPG-Converter/releases) page
2. Extract the ZIP file
3. Run `INSTALL.bat` as Administrator
4. Launch from Start Menu

### Manual Installation
1. Extract the ZIP file
2. Copy the `HEIC to JPG Converter` folder to `C:\Program Files\`
3. Run `HEIC to JPG Converter.exe`

### Run Directly (No Installation)
Simply extract and double-click `HEIC to JPG Converter.exe` to use immediately without installation.

## System Requirements

- Windows 10 or Windows 11 (64-bit)
- Administrator privileges (for installer)
- ~300MB disk space
- No additional software required

## Usage

1. Launch the application
2. Drag and drop HEIC files into the window OR click to browse
3. Adjust JPG quality slider if desired (default: 75%)
4. Optionally choose an output folder (default: same as source)
5. Click "Convert Files"
6. Files will be saved as JPG in the specified location

## Building from Source

### Requirements
- Python 3.13+
- Dependencies (install via pip):
  ```bash
  pip install pillow pillow-heif tkinterdnd2
  ```

### Build Steps
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `python src/heic_converter.py`
4. Build executable: `pyinstaller src/heic_converter.py --onefile --windowed --icon=src/heic_converter.ico`

## Project Structure

```
HEIC-to-JPG-Converter/
├── src/
│   ├── heic_converter.py      # Main application
│   ├── icon.jpg               # Professional branding icon
│   └── heic_converter.ico      # Window/taskbar icon
├── installer/
│   └── INSTALL.bat            # Automated installer script
├── docs/
│   └── README.txt             # User guide
├── releases/                  # Compiled executables
└── README.md                  # This file
```

## Troubleshooting

**Q: "Files not found" error**
A: Ensure the source HEIC files exist and are accessible. For network drives, use the Browse button instead of drag & drop.

**Q: Conversion takes a long time**
A: This is normal for large batches. The application processes each file individually to ensure quality.

**Q: Output file size is larger than expected**
A: Adjust the quality slider (lower = smaller file size). Quality 75% is recommended for most photos.

## Technical Details

- **Framework**: tkinter (Python's standard GUI library)
- **Image Processing**: Pillow + pillow-heif
- **Drag & Drop**: tkinterdnd2
- **Packaging**: PyInstaller
- **Platform**: Windows 10/11 (64-bit)

## License

MIT License - See LICENSE file for details

## Support

For issues, feature requests, or feedback, please visit the [Issues](https://github.com/johnmaxwellrolf/HEIC-to-JPG-Converter/issues) page.

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## Changelog

### Version 1.0.0
- Initial release
- HEIC/HEIF to JPG conversion
- Drag & drop support
- Adjustable quality settings
- Network drive support
- Professional branding interface

---

**Made with ❤️ for photographers and photo enthusiasts**
