# torscholar / GoogleParser
# How to use
For the manual use of the torscholar parser there are 3 important scripts:

- `torscholar.py`

    Backbone of the parsing of scientific articles on GoogleScholar. We are using tor to mask our identity and to parse the database without having to cut down on "parses per hour". If we get flagged we simply change our identity.

- `automator.py`

    Automatization of the parsing process by calling subprocesses which are easily managed by 2 simple lists (`years` and `queries`). Has to be hardcoded into the `automator.py` file.

    To Do:\
    &#x25EF; load of years and queries via external config file

- `csv2excel.sh`

    `torscholar.py` outputs simple .csv files. To further process this data via a human we need to change the format of the files. The script automates the process of transforming to an `.xlsx` and further add 2 columns to the left of the excel-file (`"0/1"` to mark articles as fitting to the query and `"comment"` to mark doubles etc.)

- `data_farm.py`

    This script parses the human coded excel-files and counts the fitting and non-fitting articles.

Using this software is pretty easy:
1. Input the wanted data into the `automator.py` via the lists
2. Start the `automator.py` script
3. After the script finished just start `csv2excel.sh` and export the files from `./excel/finished` to your local machine.
4. Manually identify fitting `"1"` or non-fitting `"0"` articles
5. Push the marked excel-files back to the Linux-machine into the `/data` directory and start `data_farm.py`. The output can be taken from `/data/output`

## torscholar
---
If you are interested in every argument for the torscholar script just invoke the help messages by supplying the `-h` flag.

The most important arguments for the `torscholar` script are:

- `-t`\
 This will make the scraper only look in the titles of the articles ("allintitle: XXX")

- `-A` => `-A "material selection"`\
The words inside the quotation marks will be searched for in the articles.

- `-p` => `-p "material selection"`\
The words inside the quotation marks will be searched for in the articles as phrases. This means they need to be spelled and in exctly this order.
