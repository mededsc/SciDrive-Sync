
from SciServer import Authentication, SciDrive

import getpass
import argparse
import os

class Password:

    DEFAULT = 'Prompt if not specified'

    def __init__(self, value):
        if value == self.DEFAULT:
            value = getpass.getpass('SciServer Password: ')
        self.value = value

    def __str__(self):
        return self.value

class Username:

    DEFAULT = 'tmp'

    def __init__(self, value):
        if value == self.DEFAULT:
            value = '{0}'.format(input("SciServer Username: "))
        self.value = value

    def __str__(self):
        return self.value

class ToUploadPath:

#TODO verify path, windows/linux compat

    DEFAULT = 'NotAPath'

    def __init__(self, value):
        if value == self.DEFAULT:
            value = '{0}'.format(input("Local Path to folder to sync with SciDrive: "))
        self.value = value
 
        try:

            if not os.path.exists(value):
                raise ValueError('Specified path {0} does not exist on your machine'.format(value))
            elif os.path.isdir(value):
                print('Directory {0} verified'.format(value))
            elif os.path.isfile(value):
                print('File {0} verified'.format(value))
            else:
                raise ValueError('Path {0} is not a directory or filename'.format(value))
        except ValueError as err:
            print(err.args)
            exit()

    def __str__(self):
        return self.value


class SciDrivePath:

#TODO verify path, windows/linux compat

    DEFAULT = "/Sync/"

    def __init__(self, value):
        if value == self.DEFAULT:
            print("Using default upload path {0}".format(value))
        self.value = value

    def ensureDirExists(self, targetPath):
        #This throws an error if parent directory does not exist
        #This also throws an error if directory already exists...
        print('TODO ensureDirExists')
        #SciDrive.createContainer(targetPath)

    def __str__(self):
        return self.value


def recursiveDirSync(payload, target):
  if os.path.isfile(str(payload)):
    print('Error: the directory upload function has been called on a file path {0}'.format(payload))
    exit()
  
  elif os.path.isdir(str(payload)):
    #target.ensureDirExists(str(target))
    
    dirpath, dirname, filename = next(os.walk(str(payload)))
    current = os.path.join(str(target),os.path.basename(dirpath))
    if len(filename) == 0:
      # problem: this is the most obvious reason for SciDrive.createContainer to fail
      # however it could also fail for authentication reasons, connection reasons, etc.
      # this problem can be solved when ensureDirExists is functional
      try:
        SciDrive.createContainer(current)
      except:
        print("The folder {0} already exists in SciDrive".format(current))
    else:
      for local_file in filename:
        SciDrive.upload(os.path.join(str(current), local_file), localFilePath=os.path.join(dirpath,local_file))
    
    for sub_dir in dirname:
      recursiveDirSync(os.path.join(dirpath, sub_dir), current)
  else:
    print('Input path {0} could not properly be checked'.format(payload))
    exit()

def uploadSync(payload, target):

  if os.path.isfile(str(payload)):
    target.ensureDirExists(str(target))

    SciDrive.upload(os.path.join(str(target), os.path.basename(str(payload))), localFilePath=str(payload))
    print("uploading {0} to {1}".format(os.path.join(str(target),os.path.basename(str(payload))),str(target)))

  elif os.path.isdir(str(payload)):
    recursiveDirSync(payload, target)
    

  else:
    print('This is supposed to be unreachable code - toUploadPath failed in checking input path')
    exit()



if __name__ == '__main__':

  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="Upload data to SciDrive")

 # subparsers = parser.add_subparsers(help='commands')
  
  parser.add_argument('-u', '--username', type=Username, help='Specify username', default=Username.DEFAULT)
  parser.add_argument('-p', '--password', type=Password, help='Specify password', default=Password.DEFAULT)

  parser.add_argument('-l', '--localpath', type=ToUploadPath, help='Specify path to file or folder to upload', default=ToUploadPath.DEFAULT)  

  parser.add_argument('-r', '--remotepath', type=SciDrivePath, help='Specify destination folderpath on SciDrive to upload files/folder to', default=SciDrivePath.DEFAULT)  


  args = parser.parse_args()

  token1 = Authentication.login(str(args.username), str(args.password))
 
  uploadSync(args.localpath, args.remotepath)
