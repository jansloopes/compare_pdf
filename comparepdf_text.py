"""_summary_
jfh 28/06/2022 program to check similarities between pdf files in dir pdfdir1
The PDF files are converted to txt files and stored in a sperate  in a txt directory txtfile
All txt files are compared and the score is stored in two  result files:
-   all similarity scores
-   high similarity scores
The high scores is determined by the high score threshold score. It is the score above fraud is suspected.
Install
- pip install pdfminer

"""
import argparse
import csv
import getopt
import io
import os
import sys
from difflib import SequenceMatcher
from pathlib import Path

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage

# parse commandline
def convert_arg(args):
    """converts list of arguments to strings. 
    Args:
        args(args): command arguments pointer to
    return:
        dictionary with converted args to strings
    """

    args_dict = {}
    args_pdfdir1_str = ' '.join(args.pdfdir1)
    if Path(args_pdfdir1_str).exists():
        # args_pdfdir1_str = f"'{args_pdfdir1_str}'"
        args_dict.update({"pdfdir1": args_pdfdir1_str})
    else:
        print(f"the directory {args_pdfdir1_str} doesn't exists\n")
        sys.exit()


    #args_txtdir1_str =  ' '.join(args.txtdir1)
    #args_dict.update({"txtdir1": args_txtdir1_str})
    return args_dict

def csv_write_file(outfile,header):
    """
    function to write to csv_file 

    Args:
        outfile (_type_): _description_
        header 
   
    """
    try:
        with open(outfile, newline='', mode='w') as csvfile:
            try:
                scorewriter = csv.writer(csvfile, delimiter=';')
                scorewriter.writerow(header)
            except (IOError, OSError) as e:
                print(f"Error writing to file{e.errno} {e.strerror}\n")
                sys.exit()
    except (FileNotFoundError, PermissionError, OSError) as e:
        print(f"Error opening file{e.errno} {e.strerror}\n")
    else:
        csvfile.close()
      
# end of csv_write_file function

def check_dir(txtdir1):
    """check if dir exits if not create

    Args:
        txtdir1 (_str_): output dir for converted txt files

    Returns:
        _none
    """

    if not(os.path.exists(txtdir1)):
        try:
            os.mkdir(txtdir1)
        except OSError as error:
            print(f"Cann't create a directory {txtdir1} errors is {error}\n")
# end of function check_dir




def init_parser():
    """"
    parses the argument of the programm

    Returns:
        _sequence string : _arguments of the programm_
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i1", "--pdfdir1", nargs='+',
                        help="first pdf directory to check similarity", required=True, type=str)
    parser.add_argument(
        "-o1", "--txtdir1", help="Directory1 to store txt files to compare", required=True, type=str)
    parser.add_argument("-out", "--result_file",
                        help="File with similarity score", required=True, type=str)
    parser.add_argument("-sh", "--high_score", help="High score number 0,0-1,0",
                        required=True,  type=float)
    parser.add_argument("-o3", "--result_highscore_file",
                        help="File with high score similarity", required=True, type=str)
    return parser.parse_args()

# converts pdf, returns its text content as a string


def convert(fname, pages=None):
    """"
    concert pdf to text file. 
    function is called from convertMultiple
    
    Args:
        fname (_filepointer_): pdf file to convert
        pages (_type_, optional): _description_. Defaults to None.

    Returns:
        filepointer : txt file converted pdf
    """
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = io.StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text
# end of convert

# converts all pdfs in directory pdfDir, saves all resulting txt files to txtdir
def convertMultiple(pdfDir, txtDir):
    """
    walks through directories and sub directories
    calls convert function to convert pdf to txt files

    Args:
        pdfDir (_type_): dir with pdf files to convert
        txtDir (_type_): dir for converted txt file from pdf file.
    Returns:
        files_dict (dict) : filename txt and pdf.

    """
    pdfDir_path = Path(pdfDir)
    files_dict = {}
    if Path(pdfDir_path).exists():
        for pdf_sub_dir in pdfDir_path.rglob('*'):
            thelist = []       
            # iterate through pdfs in pdf directory
            thelist = list(pdf_sub_dir.rglob('*.pdf'))
    #       print(f"the list is {thelist}\n")
            for pdf in thelist:
             # call function convert(pdffile)
                text = convert(pdf)  # get string of text content of pdf
                pdf_str = str(pdf)
                textFilename = txtDir + pdf.stem + ".txt"
                # make text file
                textFile = open(textFilename, "w", encoding='utf-8')
                textFile.write(text)  # write text to text file
                textFile.close()
                files_dict[textFilename] = pdf_str
        return(files_dict)
    else:
        print(f"files path {pdfDir_path} doesn't exists\n")
#   
# compare txt fiels with matcher function
# https://iq.opengenus.org/difflib-module-in-python/
#


def compare_txt_file(txtDir1, result_file, result_highscore_file, high_score, files_dict):
    """_summary_

    Args:
        txtDir1 (_str_): _input directory converted pdf txtfiles_
    
        result_file (_str_): _file with result matching score_
        result_highscore_file (_str_): _file with result high matching score_
        high_score (_float_): _score above which fraud is suspected_
        files_dict (dict) : dictionary with filename txt and pdf to connect them
    """
    path1 = Path(txtDir1)
    #print(f"the path1 is {path1}\n")
    the_list1 = []
    the_list1 = list(path1.rglob('*.txt'))
    the_list2 = []
    the_list2 = list(path1.rglob('*.txt'))
    #print(f"the list1 and list 2 are {the_list1}")
    try:
        result_file_fp = open(result_file, mode= 'a')
    except (IOError, OSError) as e:
            print(f"Error writing to file{e.errno} {e.strerror}\n")
            sys.exit()     
    try:
        result_highscore_file_fp = open(result_highscore_file, mode ='a')
    except (IOError, OSError) as e:
            print(f"Error writing to file{e.errno} {e.strerror}\n")
            sys.exit()
    writer_score= csv.writer(result_file_fp, delimiter=';')
    writer_high_score = csv.writer(result_highscore_file_fp, delimiter=';')
    for file1 in the_list1:
        file1_content = Path(file1).read_text(encoding='utf-8')
        for file2 in the_list2:
            if (file1 != file2): # file are not equal. 
                file2_content = Path(file2).read_text(encoding='utf-8')
                seq = SequenceMatcher(None, file1_content, file2_content)
                score = seq.ratio()
#               print(f"difference of file {file1.stem} and {file2.stem} is {score}")
                list_csv=[]
                list_csv.append(files_dict[str(file1)])
                list_csv.append(files_dict[str(file2)])
                list_csv.append((round(score,2)))
                writer_score.writerow(list_csv)
                if score > high_score:
                    writer_high_score.writerow(list_csv)
                
    result_file_fp.close()
    result_highscore_file_fp.close()
# end of function compare_txt_files


def main():
    #
    # get all arguments
    #
    args = init_parser()
    #
    args_dict = {}
    args_dict = convert_arg(args)
    #print(f'dict is {args_dict}\n')
    #
    # check dir txt files
    check_dir(args.txtdir1)
    
    ## open csv files
    header = ['file1.pdf','file2.pdf' 'score']
    csv_write_file(args.result_file,header)
    csv_write_file(args.result_highscore_file,header)
    #
    # convert pdf to txt files in two dirs
    #
    files_dict= {}
    files_dict = convertMultiple(args_dict["pdfdir1"], args.txtdir1)
    # print(f" file type is {type(files_dict)}")     
    # check match ratio
    compare_txt_file(args.txtdir1, args.result_file,args.result_highscore_file, args.high_score,files_dict)

# Using the special variable 
# __name__
if __name__=="__main__":
    main()
