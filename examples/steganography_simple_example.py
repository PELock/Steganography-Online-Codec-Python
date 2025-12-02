#!/usr/bin/env python

###############################################################################
#
# Steganography Online Codec WebApi interface usage example.
#
# This example shows how to hide an encrypted secret message in an image file.
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
# create Steganography Online Codec class instance (we are using our activation key)
#
mySteganographyOnlineCodec = SteganographyOnlineCodec("YOUR-WEB-API-KEY")

#
# encode a hidden message (encrypted with your password) within an image file
#
result = mySteganographyOnlineCodec.encode("input_file.jpg", "Secret message", "Pa$$word", "output_file_with_hidden_secret_message.png")

#
# result[] array holds the encoding results as well as other information
#
if result and "error" in result:
	if result["error"] == Errors.SUCCESS:
		print(f'Secret messaged encoded and saved to the output PNG file.')
	else:
		print(f'Error code {result["error"]}')
else:
	print("Something unexpected happen while trying to encode the message.")
