#!/usr/bin/env python

###############################################################################
#
# Steganography Online Codec allows you to hide a password encrypted message
# within the images & photos using AES encryption algorithm with a 256-bit
# PBKDF2 derived key.
#
# Version      : Steganography Online Codec v1.00
# Python       : Python v3
# Dependencies : requests (https://pypi.python.org/pypi/requests/)
# Author       : Bartosz Wójcik (support@pelock.com)
# Project      : https://www.pelock.com/products/steganography-online-codec
# Homepage     : https://www.pelock.com
#
###############################################################################

from enum import IntEnum
from typing import Optional, Dict

# required external package - install with "pip install requests" (if installing manually)
import requests
import base64
import os
import math


class Errors(IntEnum):
    """Errors returned by the Steganography Online Codec API interface"""

    # @var integer cannot connect to the Web API interface (network error)
    WEBAPI_CONNECTION: int = -1

    # @var integer success
    SUCCESS: int = 0

    # @var integer unknown error
    UNKNOWN: int = 1

    # @var integer message is too long for the selected image file (use larger image file)
    MESSAGE_TOO_LONG: int = 2

    # @var integer image file is too big (10 MB for full version, 50 kB for DEMO mode)
    IMAGE_TOO_BIG: int = 3

    # @var integer image file is invalid
    INVALID_INPUT: int = 4

    # @var integer image file format is not supported
    INVALID_IMAGE_FORMAT: int = 5

    # @var integer image file is malformed and cannot write or read the encoded message
    IMAGE_MALFORMED: int = 6

    # @var integer provided password is invalid (max. length 128 chars for full version, 8 for DEMO mode)
    INVALID_PASSWORD: int = 7

    # @var integer provided message is too long (unlimited size for the full version, 16 for DEMO mode)
    LIMIT_MESSAGE: int = 9

    # @var integer provided password is invalid (max. length 128 chars for full version, 8 for DEMO mode)
    LIMIT_PASSWORD: int = 10

    # @var integer error while writing output file
    OUTPUT_FILE: int = 99

    # @var integer license key is invalid or expired (no usage credits left)
    INVALID_LICENSE: int = 100


class SteganographyOnlineCodec(object):
    """Steganography Online Codec module"""

    #
    # @var string default Steganography Online Codec WebApi endpoint
    #
    API_URL = "https://www.pelock.com/api/steganography-online-codec/v1"

    #
    # @var string WebApi key for the service (leave empty for demo version)
    #
    _apiKey = ""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize SteganographyOnlineCodec class

        :param api_key: Activation key for the service (it can be empty for demo mode)
        """

        self._apiKey = api_key

    def login(self):
        """Login to the service and get the information about the current license limits

        :return: An array with the results or False on error
        :rtype: bool,dict
        """

        # parameters
        params = {"command": "login"}

        return self.post_request(params)

    def encode(self, input_image_path: str, message_to_hide: str, password: str, output_image_path: str):
        """Encrypt a message and hide it inside encoded output image file

        :param input_image_path: Input image path (supported formats PNG, JPG, GIF or BMP)
        :param message_to_hide: Message to encrypt & hide within the input image (will fail if message is too long for the selected image file)
        :param password: Message encryption password (max. 128 chars)
        :param output_image_path: Output file path (PNG format), will overwrite existing file

        :return: True on success, array with debug information on error
        :rtype: bool,dict
        """

        # additional parameters
        params_array = {"command": "encode",
                        "image": input_image_path,
                        "message": message_to_hide,
                        "password": password
                        }

        result = self.post_request(params_array)

        if result["error"] == Errors.SUCCESS:

            # write output file
            try:
                with open(output_image_path, "wb") as file:
                    binary_data = base64.b64decode(result["encodedImage"])
                    file.write(binary_data)

                return result

            except OSError:
                return {"error": Errors.OUTPUT_FILE}

        return result

    def decode(self, input_image_path: str, password: str) -> Dict:
        """Retrieve hidden message from the encoded image file (PNG format)

        :param input_image_path: Input image path (only PNG)
        :param password: Message decryption password (max. 128 chars)

        :return: Decoded string on success, array with debug information on error
        :rtype: str,dict
        """

        # additional parameters
        params_array = {"command": "decode",
                        "image": input_image_path,
                        "password": password
                        }

        result = self.post_request(params_array)

        return result

    def post_request(self, params_array: Dict[str, str]) -> Dict:
        """Send a POST request to the server

        :param params_array: An array with the parameters
        :return: An array with the results or false on error
        :rtype: bool,dict
        """

        # default error -> only returned by the SDK
        default_error = {"error": Errors.WEBAPI_CONNECTION}

        # add activation key to the parameters array
        if self._apiKey:
            params_array["key"] = self._apiKey

        try:
            # if there's an image parameter, send proper POST request including the image file
            if "image" in params_array:

                # does the file exists?
                image_path = params_array["image"]
                if not os.path.isfile(image_path):
                    return {"error": Errors.INVALID_INPUT}

                # read file and send it within the POST request
                with open(image_path, "rb") as image_file:
                    files = {"image": image_file}
                    params_array.pop("image", None)
                    response = requests.post(self.API_URL, files=files, data=params_array)
            else:
                response = requests.post(self.API_URL, data=params_array)

        except Exception as ex:

            return default_error

        # no response at all or an invalid response code
        if not response or not response.ok:
            return default_error

        # decode to JSON array
        try:
            result = response.json()
        except ValueError:
            return default_error

        # return original JSON response code
        return result

    def convert_size(self, size_bytes):
        if size_bytes == 0:
            return "0 bytes"

        size_name = ("bytes", "kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])
