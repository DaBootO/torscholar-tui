#!/bin/sh

dir=$(date +%d_%m_%Y-%H%M%S)
#backup stuff
mkdir ./DataBackup/$dir
cp *.csv ./DataBackup/$dir
# Clear all Bullshit
rm ./SendToShared/*.csv
rm ./excel/*.xlsx
rm ./excel/backup/*.xlsx
rm ./excel/backup/finished/*.xlsx
