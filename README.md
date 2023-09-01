# Welcome to this Tutorial on gcp_api_kit

Welcome to this tutorial, where you'll learn how to use the **gcp_api_kit** for interacting with Google Cloud APIs using Python and Google Colab. This toolkit supports a variety of functionalities, including but not limited to:

- Managing Google Cloud Storage buckets
- Utilizing Google Custom Search for web searches
- Converting text to speech
- Translating text between multiple languages
- Extracting text from images using OCR (Optical Character Recognition)
- Interfacing with Google BigQuery

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Fork or Clone the Repository](#fork-or-clone-the-repository)
3. [Modify Files](#modify-files)
4. [Open Main File in Google Colab](#open-main-file-in-google-colab)
5. [Fill in Required Information](#fill-in-required-information)
6. [Clone Repository in Colab](#clone-repository-in-colab)
7. [Execute All Cells](#execute-all-cells)

## Prerequisites

- You need an active Google Cloud Platform account.
- You need a GitHub account and a personal access token.

## Fork or Clone the Repository

Fork or clone the **gcp_api_kit** repository into a private GitHub repo.

## Modify Files

- Follow the diagram to change `googleapis_auth.py`.
- Update `service_account_credentials.json` according to the diagram.

## Open Main File in Google Colab

Navigate to the main file and open it in Google Colab.

## Fill in Required Information

Fill in the following:
```python
PROJECT_ID = '' #https://console.cloud.google.com
GITHUB_TOKEN = '' #https://github.com/settings/tokens
GITHUB_USER = '' #https://github.com/
```

## Clone Repository in Colab

Run the code to clone your private GitHub repository into Colab.

```python
!git clone https://{GITHUB_TOKEN}@github.com/{GITHUB_USER}/gcp_api_kit.git
```

## Execute All Cells

Run all cells in the Colab notebook.
