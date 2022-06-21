from asyncore import loop
from copy import copy
import os
import shutil
from urllib import response
from xml.dom import minidom
import constants
import requests
import time

###
# gets the size of the selected playlists
###
def getSize(playlists):
  total = 0
  
  for playlist in playlists:
    response = requests.get(constants.PLEX_ADDR + playlist["path"])
    xmlParts = minidom.parseString(response.text).getElementsByTagName("Part")
    for elem in xmlParts:
      file = elem.attributes['file'].value.replace(constants.FILE_REPLACE, '').replace('/', '\\')
      if constants.PRINT_FILES:
        print(file)
      size = os.stat(constants.SERVER_SHARE + file).st_size
      total += size

  return round(total/1000000000, 3)

###
# copies the playlists selected to the destination 
###
def copyFiles(playlists):
  print('**************************Copying Files Start**************************')
  for playlist in playlists:
    response = requests.get(constants.PLEX_ADDR + playlist["path"])
    xmlParts = minidom.parseString(response.text).getElementsByTagName("Part")
    for elem in xmlParts:
      id = elem.attributes["id"].value
      file = constants.SERVER_SHARE + elem.attributes['file'].value.replace(constants.FILE_REPLACE, '').replace('/', '\\')
      print("copying ID: " + id + " file: " + file)
      shutil.copy(file, constants.DESTINATION)
  print("**************************Copying Files Complete**************************")

###
# Selects the playlists
###
def selectPlaylists():
  playlistsToCopy = []
  response = requests.get(constants.PLEX_ADDR + "/playlists/")
  playlistsXML = minidom.parseString(response.text).getElementsByTagName("Playlist")
  playlist = {}
  i=1
  for playlistXML in playlistsXML:
    playlist[i] = {'name':playlistXML.attributes["title"].value, 'path':playlistXML.attributes["key"].value.replace(constants.FILE_REPLACE, '')}
    i+=1
  for item in playlist:
    print("[" + str(item) + "]: " + playlist[item]["name"])
  
  temp = input("Enter playlists separated by commas: ")
  ids = temp.split(',')
  for id in ids:
    playlistsToCopy.append(playlist[int(id)])
  return playlistsToCopy

###
# prints the menu
###
def printMenu():
  print("Select an options below:")
  print("[1]: Select Playlists")
  print("[2]: Set Options (Not implemented yet, set constants.py)")
  print("[3]: Get Size of selected playlist")
  print('[4]: Copy Playlists')
  print('[5]: Exit')

def __main__():
  option = 0
  playlistsToCopy = []
  while(option != 5):
    printMenu()
    selectedOption = input("Enter option: ")
    option = int(selectedOption)
    if(option == 1):
      playlistsToCopy = selectPlaylists()
      for playlist in playlistsToCopy:
        print(playlist["name"])
    elif(option == 2):
      print("set options")
      print("This feature isn't working yet, set options via constants.py")
    elif(option == 3):
      if(len(playlistsToCopy) <= 0):
        print("Select playlists first")
      else:
        size = getSize(playlistsToCopy)
        print("File size of the following playlists in GB: " + str(size))
        for playlist in playlistsToCopy:
          print(playlist["name"])
    elif(option == 4):
      if(len(playlistsToCopy) <= 0):
        print("Select playlists first")
      else:
        copyFiles(playlistsToCopy)
    time.sleep(1.5)

__main__()