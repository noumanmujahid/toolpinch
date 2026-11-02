#!/bin/sh
# Cloudflare Pages build: copy the static site into dist/, leaving out server code and config.
set -e
rm -rf dist && mkdir dist
tar --exclude=./dist --exclude=./.git --exclude=./api --exclude=./functions --exclude=./vercel.json \
    --exclude=./build.sh --exclude=./README.md --exclude=./node_modules -cf - . | tar -xf - -C dist
echo "Built $(find dist -name '*.html' | wc -l) HTML pages into dist/"
