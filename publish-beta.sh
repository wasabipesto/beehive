#!/bin/bash

# build it
rm -rf dist
yarn observable build || exit

# copy to beta site
rm -r /opt/nginx/www/beta.wasabipesto.com/*
cp -r dist/* /opt/nginx/www/beta.wasabipesto.com/
