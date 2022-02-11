<p align="center">
  <a href="" rel="noopener">
    <img width=100px height=100px src="doc/logo_doc.png" alt="Project logo">
  </a>
</p>
<h2 align="center">Poricom</h2>

---
<p align="center"> Optical character recognition in manga images. Manga OCR desktop application</p>

## Contents
- [About](#about)
- [User Guide](#user_guide)
- [Installation](#installation)
- [Acknowledgments](#acknowledgements)
</br></br>

## About <a name = "about"></a>
---
Poricom is a desktop program for optical character recognition in manga images. Although it is a manga OCR application, it can recognize text on other type of images as well. The project is a GUI implementation of the [Manga OCR library](https://pypi.org/project/manga-ocr/0.1.5/) (supports Japanese only) and the Tesseract-API python wrapper [tesserocr](https://github.com/sirfz/tesserocr) (supports other languages).
</br></br>

## User Guide  <a name="user_guide"></a>
---
Follow the installation instructions [here](#installation). Load a directory with manga images and select text boxes with Japanese text. If you are not getting good results using the default settings, [use the MangaOcr model](#load_model) to improve text detection.

### Features

Listed below are some of the features of Poricom. Click the arrow to see how each implemented feature works.

<details>
  <summary>Open a directory with manga images and start scanning text bubbles.</summary>

</details>

<details>
  <summary>Load MangaOcr model to improve Japanese text recognition. <a name="load_model"></a> </summary> 

  
</details> 

<details>
  <summary>Change language and/or orientation (limited to the Tesseract API).</summary>

  
</details>

<details>
  <summary>Detect text on non-manga images.</summary>

  
</details>
</br>

## Installation <a name = "installation"></a>
---
Installer will be released soon.

For developers, clone this repo and install requirements: `pip install -r requirements.txt`. Run the app in the command line using `python main.py`.

### System Requirements

Recommended:
- Hard drive: 750 MB HD space
- RAM: at least 2 GB

Approximately 250 MB of free space and 200 MB of memory is needed to run the application using the Tesseract API. If using the Manga OCR model, an additional 450 MB of free space and 800 MB of memory is required.

For developers, the following Python versions are supported: 3.7, 3.8, and 3.9.
</br></br>

## Acknowledgements <a name = "acknowledgements"></a>
---
This project will not be possible without the MangaOcr model by [Maciej Budyś](https://github.com/kha-white) and the Tesseract python wrapper by [sirfz](https://github.com/sirfz) and [the tesserocr contributors](https://github.com/sirfz/tesserocr/graphs/contributors). 

The software is licensed under GPLv3 (see [LICENSE](LICENSE.md)) and uses third party libraries that are distributed under their own terms (see [LICENSE-3RD-PARTY](LICENSE-3RD-PARTY.md)).

The icons used in this project are from [Icons8](https://icons8.com).
</br></br>
