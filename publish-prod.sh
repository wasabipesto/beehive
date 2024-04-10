#!/bin/bash

# reset evergreen loaders
touch pages/blogroll/*
touch pages/hardware/*
touch pages/software/*
touch pages/media/*
touch pages/plex/*

# build it
rm -rf dist
yarn observable build || exit

# copy to beta site
rm -r /opt/nginx/www/wasabipesto.com/*
cp -r dist/* /opt/nginx/www/wasabipesto.com/
