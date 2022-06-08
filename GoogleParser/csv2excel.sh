#!/bin/bash
echo "we are taking the output from torscholar and will transform it into the
0/1 excel scheme for further human analysis..."

python3 excelizer.py

python3 excel_mover.py
