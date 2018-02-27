#!/bin/sh

if [ ! -d "segments" ] 
then
    echo creating segments folder
    mkdir segments
fi
ffmpeg -i $1 -f segment -segment_time 10 -c copy segments/$1_out%03d.wav

