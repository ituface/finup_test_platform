from plistlib import writePlist
import os
import configparser
cfg=configparser.ConfigParser()
cfg.read('./public/config.ini')
host = cfg.get('URL','host')

def  createplist(app_url,fileName):
    plist = {
             'items': [
                 {'assets':
                     [
                         {'kind': 'software-package', 'url': host+app_url},
                         {'kind': 'display-image', 'url': 'http://app.finupcredit.com/57x57.png'},
                         {'kind': 'full-size-image', 'url': 'http://app.finupcredit.com/512x512.png'},

                     ],
                     'metadata': {'bundle-identifier': 'com.finupironman.app', 'bundle-version': '1.0.1',
                                  'kind': 'software', 'title': 'FinupLoanStore'}
                 },

             ]
             }

    path='%s.plist'%fileName

    writePlist(plist, '/root/data/plistfile/%s'%path)
    return upload_git()

def upload_git():
    #os.system('git clone https://gitee.com/ituface/plistFile.git ./static/plistFile')
    os.system("cd /root/data/plistfile;git add .;git commit -m 'firs';git push origin master")
    # os.system('git add .')
    # os.system("git commit -m 'first commit'")
    # os.system('git push origin master')
    return '1'

#path=createplist('/ss/sdada/dada','223s2')
upload_git()



