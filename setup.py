import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(name='steganography_online_codec',

                 version='1.0.0',

                 description='Steganography Online Codec allows you to hide a password encrypted message within the '
                             'images & photos using AES encryption algorithm with a 256-bit PBKDF2 derived key.',
                 long_description=long_description,
                 long_description_content_type="text/markdown",

                 keywords="steganography stegano stego cryptography security image secret aes encryption",

                 url='https://www.pelock.com',

                 author='Bartosz Wójcik',
                 author_email='support@pelock.com',

                 license='Apache-2.0',

                 packages=['steganography_online_codec'],

                 install_requires=[
                     'requests',
                 ],

                 zip_safe=False,

                 classifiers=[
                     "Development Status :: 5 - Production/Stable",
                     "Topic :: Software Development :: Libraries :: Python Modules",
                     "Topic :: Security :: Cryptography",
                     "Natural Language :: English",
                     "License :: OSI Approved :: Apache Software License",
                     "Programming Language :: Python :: 3"
                 ],
                 )
