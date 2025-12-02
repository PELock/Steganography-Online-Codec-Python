#!/usr/bin/env python

###############################################################################
#
# Steganography Online Codec WebApi interface usage example.
#
# In this example, we will see how to hide an encrypted message in an
# image file using our codec.
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
# encode a hidden message within the source image file
#

# full version image size limit is set to 10 MB (demo 50 kB max)
# supported image formats are PNG, JPG, GIF, BMP, WBMP, GD2, AVIF, WEBP (mail me for more)
input_file_path = "input_file.webp"

# full version message size is unlimited (demo 16 chars max)
secret_message = "Secret message"

# full version password length is 128 characters max (demo 8 chars max)
password = "Pa$$word"

# where to save encoded image with the secret message
output_file_path = "output_file_with_hidden_secret_message.png"

# encode a hidden message (encrypted with your password) within an image file
result = mySteganographyOnlineCodec.encode(input_file_path, secret_message, password, output_file_path)

#
# result[] array holds the encoding results as well as other information
#
if result and "error" in result:

	print(f'You are running in {"full" if result["license"]["activationStatus"] is True else "demo"} version')

	if result["error"] == Errors.SUCCESS:
		print(f'Secret messaged encoded and saved to {output_file_path}')
		print(f'Remaining number of usage credits - {result["license"]["usagesCount"]}')
	elif result["error"] == Errors.INVALID_INPUT:
		print(f'Invalid input file {input_file_path} or file doesn''t exist')
	elif result["error"] == Errors.MESSAGE_TOO_LONG:
		print(f'Message is too long for the provided image file, use larger file')
	elif result["error"] == Errors.IMAGE_TOO_BIG:
		print(f'Image file is too big, current limit is set to {mySteganographyOnlineCodec.convert_size(result["limits"]["maxFileSize"])}')
	elif result["error"] == Errors.LIMIT_MESSAGE:
		print(f'Message is too long, current limit is set to {result["limits"]["maxMessageLen"]}')
	elif result["error"] == Errors.LIMIT_PASSWORD:
		print(f'Password is too long, current limit is set to {result["limits"]["maxPasswordLen"]}')
	elif result["error"] == Errors.INVALID_PASSWORD:
		print(f'Invalid password')
	else:
		print(f'An unknown error occurred, error code: {result["error"]}')
else:
	print("Something unexpected happen while trying to encode the message.")
