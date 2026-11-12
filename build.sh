#!/bin/sh
# Cloudflare Pages build: copy the static site into dist/, leaving out server code and config.
set -e
rm -rf dist && mkdir dist
tar --exclude=./dist --exclude=./.git --exclude=./functions \
    --exclude=./build.sh --exclude=./scripts --exclude=./README.md --exclude=./node_modules -cf - . | tar -xf - -C dist
echo "Built $(find dist -name '*.html' | wc -l) HTML pages into dist/"
