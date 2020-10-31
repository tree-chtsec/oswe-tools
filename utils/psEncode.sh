#!/bin/sh
psfile="$1";
iconv -f ASCII -t UTF-16LE $psfile | base64 | tr -d "\n"
