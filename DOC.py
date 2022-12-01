import re
import time
from urllib import request
import wget
import os
import docx2txt 
import zipfile
import subprocess
homepath = ""


if __name__ == '__main__':
  f = open("log.txt", 'a',encoding='utf-8')
  homepath = os.getcwd()
  mylist = os.listdir("zips/")
  for zipdir in mylist:
    path = homepath + "/zips/" + zipdir + "/"
    outpath = homepath + "/txts/" + zipdir + "/"
    docpath = homepath + "/Docs/" + zipdir + "/"
    ziplist = os.listdir(path)
    for filename in ziplist:
      try:
        with zipfile.ZipFile(path + filename, 'r') as zipObj:
          listOfFileNames = zipObj.namelist()
          for tmpfile in listOfFileNames:
            if tmpfile.endswith("DOC") or tmpfile.endswith("DOCX"):
              print("[*] Find : " + docpath + "/" + tmpfile)
              zipObj.extract(tmpfile, path=docpath)
              subprocess.call(['soffice', '--headless', '--convert-to', 'txt:Text', docpath + tmpfile,'-outdir', outpath])
      except:
        f.write(path + filename + " : unzip error" + "\n")
  f.close()
      