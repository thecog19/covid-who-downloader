# covid-who-downloader

The WHO website provdies a [database of current research](https://www.who.int/emergencies/diseases/novel-coronavirus-2019/global-research-on-novel-coronavirus-2019-ncov), but no good way to agregate the papers into a database like enviorment. This repo provides the tooling to download as many of these papers as possible, either into document form, or directly into a database

# Requirements
We use beautiful soup for parsing and crossrefapi for resolving the DOI. 

`pip3 install bf4`
`pip3 install crossrefapi`

We use pdfkit to convert websites that do not offer pdf downloads into pdfs.
`sudo apt-get install wkhtmltopdf`
`pip3 install pdfkit`