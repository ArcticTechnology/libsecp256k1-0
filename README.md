# Libsecp256k1-0

This is a compiled libsecp256k1 python package that allows you to use secp256k1 in your python projects. Secp256k1 is an optimized C library for ECDSA signatures and secret/public key operations. This library is intended to be the highest quality publicly available library for cryptography on the secp256k1 curve. See this for more details on secp256k1: https://github.com/bitcoin-core/secp256k1. Libsecp256k1-0 contains the pre-compiled modules of secp256k1 compatible for multiple platforms (unix, windows 32 and 64 bits). Most importantly, you can use the dockerized compiler in this package to compile these modules directly from source. That way you don't need to put your trust the pre-compiled versions in this package or anyone else's versions of libsecp256k1.
* Github repo: https://github.com/ArcticTechnology/libsecp256k1-0
* PyPi: https://pypi.org/project/libsecp256k1-0/

## Prerequisites
* Python3 (version >= 3.10) - Install Python3 here: https://www.python.org/downloads/. Check version with: ```python3 --version```
* Pip3 (version >= 23.0) - Python3 should come with pip3. Check version with: ```pip3 --version```
* Docker (version >= 20.10.7) - Docker is only required if you wish to use the compiler in this package to compile libsecp256k1 for yourself.
* Linux or Windows - This application works out of the box for Linux and is compatible with Windows.
* MacOS - This application works for MacOS using the pre-compiled binary that comes with the app. However, this app is not able compile a new binary for MacOS. If you wish to compile your own, the Electrum wallet has a compiler that can be used. The simpliest way is to install the Electrum wallet and access the ```libsecp256k1.0.dylib``` binary file located in the app: ```~/Applications/Electrum.app/Contents/MacOS/libsecp256k1.0.dylib```. Then replace the ```../compiled/darwin/libsecp256k1.0.dylib``` file with your new binary.

## Installation
There are a couple of options to install this package:
* Pip Install - This package is hosted on PyPi and can be installed with the following command:
```
pip3 install libsecp256k1-0
```
* Local Install - Alternatively, you can download or git clone the Github repo and install it locally with the following:
```
git clone https://github.com/ArcticTechnology/libsecp256k1-0.git
cd libsecp256k1-0
pip3 install -e .
```

## Usage
After installation, you can simply import the package resources and use them in your own project:
```
from libsecp256k1_0 import *
```
Once imported, you should be able to all the modules in the package. For example, this is how you verify ecdsa with secp256k1:
```
Secp256k1._libsecp256k1.secp256k1_ecdsa_verify(<ctx>, <sig>, <msg_hash>, <pubkey>)
```

## Compile
You can use the dockerized compiler of this package to compile libsecp256k1 for yourself. The compiler builds directly from this source: https://github.com/bitcoin-core/secp256k1.git. It is recommended that you build libsecp256k1 for yourself that way you don't need to put your trust the pre-compiled versions in this package or any other versions of libsecp256k1. By default, running the compiler will overwrite the pre-compiled modules with the newly compiled ones. In order to use the compiler you will need to have Docker (version >= 20.10.7), see "Instructions for Docker" section for more details.

There are a couple ways you can run the compiler:
* Simply use the following command in Docker:
```
libsecp-compile
```
* You can also run it with the python command ```python3 -m```:
```
python3 -m libsecp-compile
```
* You can also access the compiler in the package resources. Here you have the option to specify where you want the compiled files to output to.
```
from libsecp256k1_0 import Libsecp256k1
Libsecp256k1.docker_compile(outpath='/home/example')
```
* You can also run the compiler from a Linux terminal without Docker by calling the "local_compiler.sh" file. This will automatically compile to your working directory.
```
./local_compiler.sh
```

## Troubleshooting
This section goes over some of the common issues found and how to resolve them.

### "Command Not Found" Error When Running the Compiler
On Linux, if you are getting a ```command not found``` error when trying to run the compiler, you may need to add ```~/.local/bin/``` to PATH. See this thread for details: https://stackoverflow.com/a/34947489. To add ```~/.local/bin/``` to PATH do the following:

1. Add ```export PATH=~/.local/bin:$PATH``` to ```~/.bash_profile```.
```
echo export PATH=~/.local/bin:$PATH > ~/.bash_profile
```
2. Execute command.
```
source ~/.bash_profile
```

### Instructions for Docker
1. To install Docker, use the following command:
```
sudo apt-get update
sudo apt install docker.io
sudo docker version
```
2. Make sure you are able to run docker will the following command:
```
sudo docker run --name test-docker-instance test-docker
sudo docker images
```
3. To remove the docker image use:
```
sudo docker stop test-docker-instance
sudo docker kill --signal=9 test-docker-instance
sudo docker rmi test-docker
```

## Support and Contributions
Our software is open source and free for public use. If you found any of these repos useful and would like to support this project financially, feel free to donate to our bitcoin address.

Bitcoin Address 1: 1GZQY6hMwszqxCmbC6uGxkyD5HKPhK1Pmf

![alt text](https://github.com/ArcticTechnology/BitcoinAddresses/blob/main/btcaddr1.png?raw=true)
