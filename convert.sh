#!/bin/bash
#
# Convert all images in a directory to size 800x600 px
#
convert '*.JPG' -resize 800x600 photo%03d.JPG
