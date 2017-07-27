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


if __name__ == '__main__':

  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="Upload data to SciDrive")

 # subparsers = parser.add_subparsers(help='commands')
  
  parser.add_argument('-u', '--username', type=Username, help='Specify username', default=Username.DEFAULT)
  parser.add_argument('-p', '--password', type=Password, help='Specify password', default=Password.DEFAULT)

  parser.add_argument('-f', '--folderpath', type=ToUploadPath, help='Specify path to folder containing file(s) to upload', default=ToUploadPath.DEFAULT)  

  args = parser.parse_args()

  token1 = Authentication.login(str(args.username), str(args.password))
 

  SciDrive.upload('/ScriptTest/uploaded', localFilePath=str(args.folderpath))

 
  print('{0}, {1}, {2}, {3}'.format(args.username, args.password, args.folderpath, token1))


