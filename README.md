<p align="center">
  <a href="" rel="noopener">
    <img width=100px height=100px src="doc/logo_doc.png" alt="Project logo">
  </a>
</p>
<h2 align="center">Poricom</h2>

<p align="center"> Optical character recognition in manga images. Manga OCR desktop application</p>

## Contents
- [About](#about)
- [User Guide](#user_guide)
- [Installation](#installation)
- [Acknowledgments](#acknowledgements)
</br></br>

## About <a name = "about"></a>
Poricom is a desktop program for optical character recognition in manga images. Although it is a manga OCR application, it can recognize text on other type of images as well. The project is a GUI implementation of the [Manga OCR library](https://pypi.org/project/manga-ocr/0.1.5/) (supports Japanese only) and the Tesseract-API python wrapper [tesserocr](https://github.com/sirfz/tesserocr) (supports other languages). See demo below to see how it works.

Detect text on locally stored manga images:

https://user-images.githubusercontent.com/45705751/164592647-bf6dab41-fb07-4151-8f8f-e7210f562498.mp4

Perform OCR on the current screen by pressing `Alt+Q`:

https://user-images.githubusercontent.com/45705751/161961152-29070fde-03f6-42a7-8569-0ff22ae9b014.mp4

## User Guide  <a name="user_guide"></a>
Follow the installation instructions [here](#installation). Load a directory with manga images and select text boxes with Japanese text. If you are not getting good results using the default settings, [use the MangaOcr model](#load_model) to improve text detection.

### Features

Listed below are some of the features of Poricom. Smaller features that are not covered in this section are mentioned in the [changelog](https://github.com/bluaxees/Poricom/blob/main/CHANGELOG.md). Click the arrow to see how each implemented feature works.

<details>
  <summary>Open a directory with manga images or a supported manga file (cbz, cbr, pdf) and start scanning text bubbles.</summary>

  https://user-images.githubusercontent.com/45705751/153531522-fc592533-bd97-41b7-a1e5-84c80cf2cc40.mp4
  
</details>

<details>
  <summary> Capture images outside the application using the shortcut `Alt+Q`.</summary>

  https://user-images.githubusercontent.com/45705751/161961152-29070fde-03f6-42a7-8569-0ff22ae9b014.mp4
  
</details>

<a name="load_model">
<details> 
  <summary>Load MangaOcr model to improve Japanese text recognition.</a> </summary> 

  https://user-images.githubusercontent.com/45705751/153531613-330cf185-fb0a-4a82-8b52-ee653aeee7d9.mp4
  
</details>
</a>

<details>
  <summary>Change language and/or orientation (limited to the Tesseract API).</summary>

  https://user-images.githubusercontent.com/45705751/153531632-cf39a13b-20d9-4879-9ea3-1a5d6c5aba5f.mp4
  
</details>

<details>
  <summary>Detect text on non-manga images.</summary>

  https://user-images.githubusercontent.com/45705751/153531661-7c93e51c-4871-4b84-b391-6295f8f0889e.mp4
  
</details>

## Installation <a name = "installation"></a>
Download the latest zip file [here](https://github.com/bluaxees/Poricom/releases/latest/). Decompress the file in the desired directory. Make sure that the `app` folder is in the same folder as the shortcut `Poricom`.

For developers, clone this repo and install requirements: `pip install -r requirements.txt`. Run the app in the command line using `python main.py`. 

### System Requirements

Recommended:
- Hard drive: at least 800 MB HD space
- RAM: at least 2 GB

Approximately 250 MB of free space and 200 MB of memory is needed to run the application using the Tesseract API. If using the Manga OCR model, an additional 450 MB of free space and 800 MB of memory is required.

For developers, the following Python versions are supported: 3.7, 3.8, 3.9, and 3.10.

## Acknowledgements <a name = "acknowledgements"></a>
This project will not be possible without the MangaOcr model by [Maciej Budyś](https://github.com/kha-white) and the Tesseract python wrapper by [sirfz](https://github.com/sirfz) and [the tesserocr contributors](https://github.com/sirfz/tesserocr/graphs/contributors). 

The software is licensed under GPLv3 (see [LICENSE](LICENSE.md)) and uses third party libraries that are distributed under their own terms (see [LICENSE-3RD-PARTY](LICENSE-3RD-PARTY.md)).

The icons used in this project are from [Icons8](https://icons8.com).
