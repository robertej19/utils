#****************************************************************
"""
### THE BELOW TEXT IS OUTDATED and needs to be updated

#This replaces a previous version of gcard_helper.py by using the HTMLParser class
#This allows for more robust parsing of the html mother directory to find gcard files
#Even better would be to use BeautifulSoup, which would allow for the code to be condensed as:
#```import requests
#from bs4 import BeautifulSoup
#page = requests.get('http://www.website.com')
#bs = BeautifulSoup(page.content, features='lxml')
#for link in bs.findAll('a'):
#    print(link.get('href'))```
#Unfortunately, this module must be imported and cannot be gaurannted that it will be on whatever
#server this software will live on, so it is safer to instead use HTMLParser which is more common
####
#This file takes in a BatchID and gcard url from db_batch_entry and passes it through
#a few functions to download the gcards from the specified location and to enter them into the
#appropriate gcard table in the database.
# Some effort should be developed to sanitize the gcard files to prevent
# against sql injection attacks
"""
#***************************************************************
from __future__ import print_function
import argparse, subprocess, os
import utils, file_struct, html_reader

def Lund_Downloader(url_dir,lund_urls,lund_dir):
    if len(lund_urls) == 0:
      print("No Lund files found (they must end in '{0}'). Is the online repository correct?".format(file_struct.lund_identifying_text ))
      exit()
    else:
      for url_ending in lund_urls:
        utils.printer('Lund URL name is: '+url_ending)
        lund_text = html_reader.html_reader(url_dir+'/'+url_ending,'')[0]#This returns a tuple, we need the contents of the tuple
        utils.printer2('HTML from lund link is: {0}'.format(lund_text))
        lund_text_db = lund_text.replace('"',"'") #This isn't strictly needed but SQLite can't read " into data fields, only ' characters
        print("\t Gathered lund file '{0}'".format(url_ending))
        filename = lund_dir+"/"+url_ending
        with open(filename,"a") as file: file.write(lund_text_db)

def Lund_Entry(url_dir):
  print("Gathering lund files from {0} ".format(url_dir))
  if url_dir == file_struct.lund_default:
    utils.printer('Using default lund file')
  elif 'https://' in url_dir:
    utils.printer('Trying to download lund files from online repository')
    raw_html, lund_urls = html_reader.html_reader(url_dir,file_struct.lund_identifying_text)
    lund_dir_unformatted = url_dir.split("//")[1]
    lund_dir = lund_dir_unformatted.replace(".","_").replace("/","_").replace("~","_")
    if os.path.exists(lund_dir):
      print("Directory of LUND files already has been downloaded, not downloading again")
    else:
      subprocess.call(['mkdir','-p',lund_dir])
      Lund_Downloader(url_dir,lund_urls,lund_dir)
  else:
    print('generator not recognized as default option or valid online repository, please inspect scard')
    exit()

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument(file_struct.debug_short,file_struct.debug_longdash, default = file_struct.debug_default,help = file_struct.debug_help)
    args = argparser.parse_args()

    file_struct.DEBUG = getattr(args,file_struct.debug_long)
    url_dir = "https://userweb.jlab.org/~ungaro/lund/"
    Lund_Entry(url_dir)
