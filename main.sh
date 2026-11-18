#!/bin/sh
cd "$(dirname "$0")" || exit
python3 -m src.main

cd public && python3 -m http.server 8888