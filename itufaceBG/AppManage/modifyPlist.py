#!usr/bin/python
# -*- coding:utf-8 -*-
from biplist import *
import os,sys
import sys
import plistlib
# try:
#     plist = str(readPlist("/Users/finup/Desktop/itufaceBG/static/plistfile/plistfile/store_manifest.plist")).encode('utf-8');
#
# except InvalidPlistException as e:
#     print("Not a Plist or Plist Invalid:", e)
#
#
#
# try:
#     writePlist(plist, "/Users/finup/Desktop/itufaceBG/static/store_manifest.plist")
# except (InvalidPlistException, NotBinaryPlistException) as e:
#     print("/Users/finup/Desktop/itufaceBG/static/plistfile/plistfile/store_manifest.plistSomething bad happened:", e)
DATA = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>items</key>
	<array>
		<dict>
			<key>assets</key>
			<array>
				<dict>
					<key>kind</key>
					<string>software-package</string>
					<key>url</key>
					<string>http://app.finupcredit.com/FinupLoanStore.ipa</string>
				</dict>
				<dict>
					<key>kind</key>
					<string>display-image</string>
					<key>url</key>
					<string>http://app.finupcredit.com/57x57.png</string>
				</dict>
				<dict>
					<key>kind</key>
					<string>full-size-image</string>
					<key>url</key>
					<string>http://app.finupcredit.com/512x512.png</string>
				</dict>
			</array>
			<key>metadata</key>
			<dict>
				<key>bundle-identifier</key>
				<string>com.finupironman.app</string>
				<key>bundle-version</key>
				<string>1.0.1</string>
				<key>kind</key>
				<string>software</string>
				<key>title</key>
				<string>FinupLoanStore</string>
			</dict>
		</dict>
	</array>
</dict>
</plist>

"""

plistlib.writePlist(DATA,'/Users/finup/Desktop/itufaceBG/static/storemanifest.plist')