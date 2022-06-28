
import os

"""
    PS D:\Surfdrive\MyWork\Leiden\Python> & C:/Users/jan/AppData/Local/Microsoft/WindowsApps/python3.9.exe d:/Surfdrive/MyWork/Leiden/Python/comparepdf_text.py -h
    usage: comparepdf_text.py [-h] -i1 PDFDIR1 -o1 TXTDIR1 -out OUTFILE -sh SIMHIGHSCORE -o3 OUTFILEHIGHSCORE

optional arguments:
  -h, --help            show this help message and exit
  -i1 PDFDIR1, --pdfdir1 PDFDIR1
                        first pdf directory to check similarity
  -o1 TXTDIR1, --txtdir1 TXTDIR1
                        Directory1 to store txt files to compare
  -out RESULTFILE --resultfile RESULTFILE
                        File with similarity score
  -sh SIMHIGHSCORE, --SimHighScore SIMHIGHSCORE
                        High score number 0,0-1,0
  -o3 resultfileHIGHSCORE, --resultfileHighScore resultfileHIGHSCORE
                        File with high score similarity

"""


run_string = ' "F:/Program Files/Python39/python.exe" ' \
    + ' d:\\users\\jan\\Surfdrive\\MyWork\\Leiden\\Python\\comparepdf_text.py' \
    + ' -i1 D:\\Users\\jan\\Surfdrive\\MyWork\\Leiden\\FICT\\Ipfond\\21-22\\controle_oplevering\\'\
    + ' -o1 d:\\users\\jan\\Surfdrive\\MyWork\\Leiden\\FICT\\Ipfond\\21-22\\Run02\\Samed_txt\\ '\
    +  ' -out d:\\users\\jan\\Surfdrive\\MyWork\\Leiden\\FICT\\Ipfond\\21-22\\Run02\\samed_score.csv\\' \
    +  ' -sh 0.4' \
    +  ' -o3 d:\\users\\jan\\Surfdrive\\MyWork\\Leiden\\FICT\\Ipfond\\21-22\\Run02\\samed_highscore.csv'

print (run_string)
os.system(run_string)
