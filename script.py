import os
import shutil
from urllib import response
from xml.dom import minidom
import constants

def GetSize(files):
  # init $total variable
  total = 0
  # loop through parts
  for file in files:
    xmlParts = file.getElementsByTagName('Part')
    for elem in xmlParts:
      file = elem.attributes['file'].value.replace(constants.FILE_REPLACE, '').replace('/', '\\')
      if constants.PRINT_FILES:
        print(file)
      size = os.stat(constants.SERVER_SHARE + file).st_size
      total += size

  return round(total/1000000000, 3)

def CopyFiles(files):
  print('**************************Copying Files Start**************************')
  for file in files:
    xmlParts = file.getElementsByTagName('Part')
    # loop through parts
    for elem in xmlParts:
      id = elem.attributes["id"].value
      file = constants.SERVER_SHARE + elem.attributes['file'].value.replace(constants.FILE_REPLACE, '').replace('/', '\\')
      print("copying ID: " + id + " file: " + file)
      shutil.copy(file, constants.DESTINATION)
  print("**************************Copying Files Complete**************************")

def __main__():
  # parse an xml file by name
  files = []
  for file in constants.FILES:
      files.append(minidom.parse(file))
  size = GetSize(files)
  print("Total Size:" + str(size) + " GB")

  response = input("Do you want to start copying? (Y/N): ")

  if(response.upper() == 'Y'):
    CopyFiles(files)
  else:
    print("Exiting script")

__main__()