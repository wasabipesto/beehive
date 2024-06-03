#!/bin/bash

# get vars
source .env || exit
echo Starting beehive deployment...

if [ "$1" = "--invalidate-all" ]; then
    find src/.observablehq/cache -type f -name '*.json' -exec mv '{}' '{}.bak' \; || exit
    echo Invalidated cached data loaders.
fi

if [ "$1" = "--invalidate" ]; then
    find src/.observablehq/cache -type f -name '$2.json' -exec mv '{}' '{}.bak' \; || exit
    echo Invalidated data loader $2.
fi

# build it
rm -rf dist
yarn observable build || exit

echo Building RSS feed...
python3 src/feed/generate_feed.py src/assets/feed

echo Copying static assets...
mkdir dist/_file/assets
cp -r src/assets/* dist/_file/assets/

# copy to beta site
rm -r ${DEPLOY_PATH}/${DEV_SITE}/*
cp -r dist/* ${DEPLOY_PATH}/${DEV_SITE}/
echo Deployed to https://${DEV_SITE}
read -rsp $'Press any key to proceed to prod...\n' -n1 key

# copy to beta site
rm -r ${DEPLOY_PATH}/${PROD_SITE}/*
cp -r dist/* ${DEPLOY_PATH}/${PROD_SITE}/
echo Deployed to https://${PROD_SITE}