Python program to check similarity betwoon pdf files.
It scan a directory for pdf  files and convert them into txt files.
these txt files are compared and the score is writen to a csv file.
The PDF files are converted to txt files and stored in a sperate  in a txt directory txtfile
All txt files are compared and the score is stored in two  result files:
-   all similarity scores
-   high similarity scores
The high scores is determined by the high score threshold score. It is the score above fraud is suspected.
Install
- pip install pdfminer