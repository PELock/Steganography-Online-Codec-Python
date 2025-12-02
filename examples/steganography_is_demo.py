#!/usr/bin/env python

###############################################################################
#
# Steganography Online Codec WebApi interface usage example.
#
# In this example we will verify our activation key status.
#
# Version      : v1.00
# Language     : Python
# Author       : Bartosz Wójcik
# Project      : https://www.pelock.com/products/steganography-online-codec
# Homepage     : https://www.pelock.com
#
###############################################################################

#
# include Steganography Online Codec module
#
from steganography_online_codec import *

#
# if you don't want to use Python module, you can import directly from the file
#
#from pelock.steganography_online_codec import *

#
# create Steganography Online Codec class instance (we are using our activation key)
#
mySteganographyOnlineCodec = SteganographyOnlineCodec("YOUR-WEB-API-KEY")

#
# login to the service
#
result = mySteganographyOnlineCodec.login()

#
# result[] Dict holds the information about the license & current limits
#
if result:

	print(f'You are running in {"full" if result["license"]["activationStatus"] is True else "demo"} version')

	# information about the current license
	if result["license"]["activationStatus"] is True:
		print(f'Registered for - {result["license"]["userName"]}')
		print(f'License type - {"personal" if result["license"]["type"] == 0 else "company"}')
		print(f'Total number of purchased usage credits - {result["license"]["usagesTotal"]}')
		print(f'Remaining number of usage credits - {result["license"]["usagesCount"]}')

	# current limits (different for DEMO and FULL versions)
	print(f'Max. password length - {result["limits"]["maxPasswordLen"]}')
	print(f'Max. message length - {"unlimited" if result["limits"]["maxMessageLen"] == -1 else result["limits"]["maxMessageLen"]}')
	print(f'Max. input image file size - {mySteganographyOnlineCodec.convert_size(result["limits"]["maxFileSize"])}')
else:
	print("Something unexpected happen while trying to login to the service.")
