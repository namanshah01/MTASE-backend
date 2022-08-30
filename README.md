# MTASE (Multilingual Text Analyzer and Summarization Engine) Backend

_This project serves as backend for [MTASE frontend](https://github.com/VirajPatidar/MTASE-frontend)._

The objective of this project is to build a Multilingual Text Analyzer and Summarization Engine that can analyze, translate and summarize a piece of unlabeled/unidentified/unknown text provided by the user as input and make its services available via a web application.

### Tech Stack ###
* Django REST Framework v3.13.1
* Django v4.0.1
* PyTorch v1.8.2+cpu
* SQLite

### API Endpoints ###
`POST /api/summarise` <br>
Input: Piece of text desired to be summarised <br>
Output: Meta data, Translated Text, Abstractive Summary, Extractive Summary and Keywords of original text blob
