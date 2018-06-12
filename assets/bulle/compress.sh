#!/usr/bin/env bash

mkdir -p "compressed"
mogrify -path "compressed" -resize 1000 -quality 80 "*.jpg"
