#!/bin/bash
echo "we are taking the output from torscholar and will transform it into the
0/1 excel scheme for further human analysis..."

SCRIPT=$(readlink -f "$0")
# Absolute path this script is in, thus /home/user/bin
SCRIPTPATH=$(dirname "$SCRIPT")
cd $SCRIPTPATH

python3 excelizer.py

python3 excel_mover.py