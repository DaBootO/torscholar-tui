#!/bin/sh

echo "starting work on the pure data..."

#copy files
cp *.csv ./SendToShared/
python excelizer.py

#copy excel files
cp ./excel/*.xlsx ./excel/backup/
python excel_mover.py
