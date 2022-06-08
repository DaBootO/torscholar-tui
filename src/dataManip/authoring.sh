#!/bin/bash
echo "performing author analysis on the data..."

SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
cd $SCRIPTPATH

echo "starting undoubler..."
python3 ../../authoring/undoubler.py
echo "starting main..."
python3 ../../authoring/main_undoubled.py
echo "starting data manipulation..."
python3 ../../authoring/manip_undoubled.py

# python3 excel_mover.py