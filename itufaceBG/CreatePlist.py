from biplist import *
from datetime import datetime
import os
import time
def  createplist(app_url):
    plist = {
             'items': [
                 {'assets':
                     [
                         {'kind': 'software-package', 'url': app_url},
                         {'kind': 'display-image', 'url': 'http://app.finupcredit.com/57x57.png'},
                         {'kind': 'full-size-image', 'url': 'http://app.finupcredit.com/512x512.png'},

                     ],
                     'metadata': {'bundle-identifier': 'com.finupironman.app', 'bundle-version': '1.0.1',
                                  'kind': 'software', 'title': 'FinupLoanStore'}
                 },

             ]
             }

    try:
        writePlist(plist, "./static/plistFile/examplea.plist")
    except (InvalidPlistException, NotBinaryPlistException) as e:
        print("Something bad happened:", e)



def upload_git(app_path):
    os.system('git clone https://gitee.com/ituface/plistFile.git /Users/finup/Desktop/itufaceBG/static/plistFile')
    os.system('git add .')
    os.system("git commit -m 'first commit'")
    os.system('git push origin master')

createplist('sad')