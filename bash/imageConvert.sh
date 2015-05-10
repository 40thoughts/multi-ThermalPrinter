#!/bin/bash

tmpDir=/tmp/printer
tmpFile=$tmpDir/tmp
output=$tmpDir/output.jpg

mkdir $tmpDir

wid=$(identify $1 | cut -d ' ' -f3 | cut -d 'x' -f1)
hei=$(identify $1 | cut -d ' ' -f3 | cut -d 'x' -f2)

if [ $wid -gt $hei ]
then
    convert $1 -rotate 90 $tmpDir/.pictmp
    convert $tmpDir/.pictmp -resize 384x -normalize -auto-level -level 5%,80%,1.3 -dither FloydSteinberg -gamma 1.3 -colors 2 -colorspace gray -normalize $output
else
    convert $1 -resize 384x -normalize -auto-level -level 5%,80%,1.3 -dither FloydSteinberg -gamma 1.3 -colors 2 -colorspace gray -normalize $output
fi
