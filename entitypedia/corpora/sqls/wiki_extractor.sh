#!/bin/sh

echo "Cloning WikiExtractor."
git clone https://github.com/attardi/wikiextractor.git
cd wikiextractor

echo "Downloading Wikipedia articles. Wait a minutes."
wget https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2

echo "Extracting and Cleaning text from a Wikipedia dump file."
nohup python WikiExtractor.py -b 500K -o extracted --links --json jawiki-latest-pages-articles.xml.bz2