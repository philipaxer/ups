# Introduction
Universal plotting sheet for marine navigation

This generates a plotting sheet as svg printable on A4 format.

# Requirements
You need to install pysvg.

# Setup
Download package. Execute 'setup.py install'

# Run
Make sure your Script directory in in your path and run
'upc -pg a4 -f myupc.svg'
or
'python -m pyups.ups -pg a4 -f myupc.svg'

The script tries to locate your inkscape installation to generate a PDF from the svg.