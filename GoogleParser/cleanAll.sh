#!/bin/sh

echo "We are deleting everything in: \n./DataBackup \n./SendToShared \n./excel
and its subdirectories..."

echo "Backup will be created in ./DataBackup/\$Date"

dir=$(date +%d_%m_%Y-%H%M%S)
#backup stuff
mkdir ./DataBackup/$dir

if ls *.csv 1> /dev/null 2>&1; then
  echo "files exist!"
  cp *.csv ./DataBackup/$dir
else
  echo "no files..."
fi
# Clear all Bullshit
rm ./SendToShared/*.csv
rm ./excel/*.xlsx
rm ./excel/backup/*.xlsx
rm ./excel/backup/finished/*.xlsx

echo "finished!"
