#!/bin/bash

mkdir -p newsletter_src
url_list="newsletter_urls.txt"
index=1
while IFS= read -r url || [[ -n "$url" ]]; do
    echo "Downloading newsletter $index from: $url"
    curl -L -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36" \
         "$url" \
         -o "newsletter_src/newsletter$index.html"
    ((index++))
done < "$url_list"