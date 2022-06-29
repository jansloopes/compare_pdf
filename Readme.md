# Python 3.9 program to check similarity between pdf files.

It scans a directory for pdf  files and convert them into txt files.
These txt files are compared and the score is written to a csv file.
The PDF files are converted to txt files and stored in a seperate directory
All txt files are compared and the score is stored in two  result files:
1. all similarity scores
2. high similarity scores

The high scores is determined by the high score threshold score. It is the score above which fraud is suspected.
# Install:
*- pip install pdfminer*