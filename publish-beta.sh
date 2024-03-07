#!/bin/bash

yarn build || exit
rm -r /opt/nginx/www/beta.wasabipesto.com/*
cp -r dist/* /opt/nginx/www/beta.wasabipesto.com/
