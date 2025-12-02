#!/usr/bin/env python

###############################################################################
#
# Steganography Online Codec WebApi interface usage example.
#
# In this example, we will see how to extract a previously encrypted & hidden
# secret message from an image file.
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
# extract a hidden message from the previously encoded image file
#

# full version image size limit is set to 10 MB (demo 50 kB max)
# supported image format is PNG and only PNG!
input_file_path = "output_file_with_hidden_secret_message.png"

# full version password length is 128 characters max (demo 8 chars max)
password = "Pa$$word"

# extract a hidden message from the image (PNG files only)
result = mySteganographyOnlineCodec.decode(input_file_path, password)

#
# result[] Dict holds the decoding results as well as other information
#
if result and "error" in result:

	print(f'You are running in {"full" if result["license"]["activationStatus"] is True else "demo"} version')

	if result["error"] == Errors.SUCCESS:
		print(f'Secret message is "{result["message"]}"')
		print(f'Remaining number of usage credits - {result["license"]["usagesCount"]}')
	elif result["error"] == Errors.INVALID_INPUT:
		print(f'Invalid input file {input_file_path} or file doesn''t exist')
	elif result["error"] == Errors.IMAGE_TOO_BIG:
		print(f'Image file is too big, current limit is set to {mySteganographyOnlineCodec.convert_size(result["limits"]["maxFileSize"])}')
	elif result["error"] == Errors.LIMIT_MESSAGE:
		print(f'Extracted message is too long, current limit is set to {result["limits"]["maxMessageLen"]}')
	elif result["error"] == Errors.LIMIT_PASSWORD:
		print(f'Password is too long, current limit is set to {result["limits"]["maxPasswordLen"]}')
	elif result["error"] == Errors.INVALID_PASSWORD:
		print(f'Invalid password')
	else:
		print(f'An unknown error occurred, error code: {result["error"]}')
else:
	print("Something unexpected happen while trying to extract the secret message.")
