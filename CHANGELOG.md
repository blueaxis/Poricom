# Changelog

## [0.3.0](https://github.com/bluaxees/Poricom/releases/tag/v0.3.0) - 2022-04-22

### Added
- Navigate through images using the scroll wheel (This was accidentally included in [v0.2.2](https://github.com/bluaxees/Poricom/releases/tag/v0.2.2))
- Add image scaling in view settings (fit to width, fit to height, fit to screen)
- Implement split view mode
- Add option to adjust preview text font size and font style
- Customize the external capture shortcut

### Changed
- Revamp ribbon button arrangement
- Improve app responsiveness when selecting text in an image
- Set default font to Helvetica

## [0.2.2](https://github.com/bluaxees/Poricom/releases/tag/v0.2.2) - 2022-04-17

### Fixed
- Copy detected text to clipboard for external captures

## [0.2.1](https://github.com/bluaxees/Poricom/releases/tag/v0.2.1) - 2022-04-15

### Fixed
- Implement error message when MangaOCR model is loaded while not connected to the internet
- Load the correct configuration (theme) when the application is launched
- Address poppler path error when opening a pdf file

### Changed
- Log detected text only after the left mouse button is released

## [0.2.0](https://github.com/bluaxees/Poricom/releases/tag/v0.2.0) - 2022-04-07

### Added
- Allow capturing images outside the application using a shortcut (`Alt+Q`)
- Implement zooming and panning function
- Support for the following manga file formats: cbr, cbz, pdf

### Changed
- Improve threading when loading detection models or when converting a manga file
- Restore access to dark theme
- Tooltip when hovering buttons are more informative
- Faster startup when launching the application

## [0.1.0](https://github.com/bluaxees/Poricom/releases/tag/v0.1.0) - 2022-02-12

- Initial Release
