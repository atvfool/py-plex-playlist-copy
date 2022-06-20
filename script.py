from xml.dom import minidom
import constants

def GetSizeScript(files):
  # init $total variable
  '$total = 0 \r\n'
  script = ''
  # loop through parts
  for file in files:
    xmlParts = file.getElementsByTagName('Part')
    for elem in xmlParts:
      file = elem.attributes['file'].value
      script += "$total += (Get-Item \"" + constants.SERVER_SHARE + file.replace(constants.FILE_REPLACE, '').replace('/', '\\') + "\").length/1GB\r\n"  

  script += "Write-Host($total)\r\n"
  return script

def GetCopyScript(files):
  # init $total variable
  script = ''
  for file in files:
    xmlParts = file.getElementsByTagName('Part')
    # loop through parts
    for elem in xmlParts:
      id = elem.attributes["id"].value
      file = elem.attributes['file'].value
      script += 'Write-Host("Copying Part ID: ' + id + '")\r\n'
      script += copyCommand(file)
  script += 'Write-Host("Copying Complete")\r\n'
  return script

def copyCommand(file):
  return "Copy-Item \"" + constants.SERVER_SHARE  + file.replace(constants.FILE_REPLACE, '').replace('/', '\\') + "\"\r\n"

def __main__():
  # parse an xml file by name
  files = []
  for file in constants.FILES:
      files.append(minidom.parse(file))
  # init script variable
  script = ''
  # Create Get size script
  script += GetSizeScript(files)
  # write script to file
  scriptFile = open('GetSize.ps1', 'w') # overwrite
  scriptFile.write(script)
  scriptFile.close()
  # Create the copy files script
  # init script variable
  script = ''
  # Create copy script
  script += GetCopyScript(files)
  # write script to file
  scriptFile = open('CopyFiles.ps1', 'w') # overwrite
  scriptFile.write(script)
  scriptFile.close()


__main__()