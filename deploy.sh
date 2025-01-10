#!/bin/bash

# get vars
source .env || exit
echo Starting beehive deployment...

if [ "$1" = "--invalidate-all" ]; then
    find src/.observablehq/cache -type f \( -name "*.json" -o -name "*.csv" \) -exec sh -c '
        for file; do
            mv "$file" "$file.bak" && echo "Moved: $file"
        done
    ' sh '{}' + || exit
fi

if [ "$1" = "--invalidate" ]; then
    find src/.observablehq/cache -type f \( -name "*.json" -o -name "*.csv" \) -path "*$2*" -exec sh -c '
        for file; do
            mv "$file" "$file.bak" && echo "Moved: $file"
        done
    ' sh '{}' + || exit
fi

# build it
rm -rf dist
yarn observable build || exit

echo Copying static assets...
mkdir dist/assets
cp -r src/assets/* dist/assets/

# copy to beta site
rm -r ${DEPLOY_PATH}/${DEV_SITE}/*
cp -r dist/* ${DEPLOY_PATH}/${DEV_SITE}/
echo Deployed to https://${DEV_SITE}

echo -n "Type \"prod\" to proceed to prod: "
read input
if [[ "$input" != "prod" ]]; then
    echo "Deployment terminated."
    exit
fi

# copy to prod site
rm -r ${DEPLOY_PATH}/${PROD_SITE}/*
cp -r dist/* ${DEPLOY_PATH}/${PROD_SITE}/
echo Deployed to https://${PROD_SITE}
