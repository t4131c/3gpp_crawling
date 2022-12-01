import re
import time
from urllib import request
import wget
import os
import docx2txt 
import zipfile
import subprocess
homepath = ""
blacklist = []

def downloadzip(url, name):
  path = homepath + "/zips/" + name + "/"
  docpath = homepath + "/Docs/" + name + "/"
  print(path)
  if (not os.path.isdir(path)):
    os.mkdir(path)
  if (not os.path.isdir(docpath)):
    os.mkdir(docpath)
  mylist = os.listdir("zips/" + name)
  html=request.urlopen(url) 
  try:
    html_contents=str(html.read().decode("cp949"))
  except:
    html_contents=str(html.read().decode("utf-8"))
  series_list = re.findall(r"(https)(.+)(.zip\">)", html_contents) 

  for url in series_list: 
    tmp_url="".join(url) 
    final_url = tmp_url[:tmp_url.find('"')]
    nowzip = final_url[final_url.find("/Docs/") + len("/Docs/"):]
    if nowzip not in mylist and nowzip not in blacklist:
      if "%20" in final_url:
        final_url = final_url.replace("%20", " ")
      print("redownloading : " + final_url)
      zipname = wget.download(final_url, out=path)
      time.sleep(0.1)
      unzip(zipname, name);
      

    


def unzip(filename, name):

  path = homepath + "/Docs/" + name + "/"
  print(path)
  try:

    with zipfile.ZipFile(filename, 'r') as zipObj:
      listOfFileNames = zipObj.namelist()
      for tmpfile in listOfFileNames:
        if (tmpfile.lower()).endswith("doc") or (tmpfile.lower()).endswith("docx"):
           zipObj.extract(tmpfile, path=path)
           subprocess.call(['soffice', '--headless', '--convert-to', 'txt:Text', path + tmpfile,'-outdir', homepath + "/txts/" + name + "/"])
        elif tmpfile.endswith("zip"):
          zipObj.extract(tmpfile)
          with zipfile.ZipFile(tmpfile, 'r') as test:
            tmplist = test.namelist()
            for tmp in tmplist:
              if (tmp.lower()).endswith("doc") or (tmp.lower()).endswith("docx"):
                test.extract(tmp, path=path)
                subprocess.call(['soffice', '--headless', '--convert-to', 'txt:Text', path + tmp,'-outdir', homepath + "/txts/" + name + "/"]) 
  except:
    f = open("log.txt", 'a',encoding='utf-8')
    f.write(name + " : unzip error" + "\n")
    f.close()
    return


   



if __name__ == '__main__':
  homepath = os.getcwd()
  if (not os.path.isdir(homepath + "/Docs")):
    os.mkdir(homepath + "/Docs")
  if (not os.path.isdir(homepath + "/txts")):
    os.mkdir(homepath + "/txts")
  if (not os.path.isdir(homepath + "/zips")):
    os.mkdir(homepath + "/zips")
  url="https://www.3gpp.org/ftp/tsg_sa/WG3_Security/"
  html=request.urlopen(url) 
  html_contents=str(html.read().decode("cp949"))
  series_list = re.findall(r"(https)(.+)(>TSGS3)", html_contents) 

  for url in series_list: 
    tmp_url="".join(url) 
    final_url = tmp_url[:tmp_url.find('"')] + "/Docs"

    try:
      version = int(re.findall(r'\d+',final_url[final_url.find("TSGS3_") + len("TSGS3_"):])[0])
      if not version >=74:
        continue
    except:
      break
    print("Downloading : " + final_url)

    name = final_url[final_url.find("TSGS3_"):final_url.find("/Docs")]
    downloadzip(final_url, name)