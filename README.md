# Python Starter Package
This is a basic python starter package to be used as a template for creating your own python packages. See "PythonStarterPackage Setup Guide.md" in ```doc/``` for a detailed explanation of the package resources.
* Github repo: https://github.com/ArcticTechnology/PythonStarterPackage
* PyPi: https://pypi.org/project/PythonStarterPackage/

## Prerequisites
This app should would out of the box for Linux on a Linux terminal. For Windows and Mac, it is recommended to run this app on a linux emulation layer such as the Git Bash terminal. See the "Instructions for Git Bash" section for details.

In addition to the above, this app also requires the following:
* Python3 (version >= 3.8) - Install Python3 here: https://www.python.org/downloads/. Check version with: ```python3 --version```
* Pip3 (version >= 20.2.1) - Python3 should come with pip3. Check version with: ```pip3 --version```

## Installation
There are a couple of options to install this app:
* Pip Install - This app is hosted on PyPi and can be installed with the following command:
```
pip3 install PythonStarterPackage
```
* Local Install - Alternatively, you can download or git clone the Github repo and install it locally with the following:
```
git clone https://github.com/ArcticTechnology/PythonStarterPackage.git
cd PythonStarterPackage
pip3 install -e .
```

## Usage
After installation, you can run this app in your terminal with this command:
```
pythonstarterpackage
```
You can also run with the python command ```python3 -m```:
```
python3 -m pythonstarterpackage
```
You can also import the package resources and run them in your own project:
```
from pythonstarterpackage import *
starter = StarterPkg()
starter.run()
```

## Documentation
The purpose of this project is to show you how to create a standard python package from scratch. This project is inspired by this excellent getmyip package by @iamtennislover: https://github.com/iamtennislover/getmyip and this great guide on deploying python packages by @sigma-coding: https://github.com/areed1192/sigma-coding.

### Setup
See "PythonStarterPackage Setup Guide.md" in ```doc/``` for a detailed walkthrough of what each of the package resources do. Once you have an understanding of this package, you can clone this package to your local directory and proceed to testing and deployment.

### Testing
In the directory containing the ```setup.py``` file, you can test the package by installing it in ```pip3``` editable mode. This will allow you make changes to it and test it without having to push the changes each time.
1. Use ```pip3``` to install the package in editable mode:
```
pip3 install -e .
```
2. Run the package by calling the package directly:
```
pythonstarterpackage
```
Or use ```python3 -m```:
```
python3 -m pythonstarterpackage
```
3. Testing the import. Run the ```test_main.py``` file:
```
python3 ./test/test_main.py
```
4. Once finished, delete the pythonstarterpackage.egg-info file and uninstall the package with:
```
pip3 uninstall pythonstarterpackage
```

Note: It is recommended that you use a virtual environment when testing your package.
1. To create a virtual environment:
```
virtualenv venv
```
2. Activate the environment use: ```. venv/bin/activate```. On Windows it may be: ```. venv/Script/activate```.

### Dependency Mapping
Next, make sure to check the package dependencies and update the setup.cfg file as needed. To do this:
1. Create (or overwrite) the requirements.txt document with ```pipreqs```. This is an extremely useful tool because it automatically finds all of the relevant versions of dependencies your package relies on and puts them into the ```requirements.txt``` file. If you don't have ```pipreqs```, install it with ```pip install pipreqs```.
```
pipreqs --force --encoding utf-8
```
2. Once the ```requirements.txt``` is updated, check to see if there is any additional dependencies that need to be added or updated in setup.cfg under the ```install_requires =```. If so, add or update it.

### Deployment
Once the package is ready, we can work on deploying the package.

1. Upgrade ```setuptools```, ```wheel```, and ```twine``` (```twine``` will be used in the next part).
```
pip3 install --upgrade setuptools wheel twine
```
2. Build the package with ```setup.py```.
```
python3 setup.py sdist bdist_wheel
```
3. Check the contents of the .whl and .tar.gz distributions. The key things to look for are: (1) all of your package subdirectories like utils are added to both distributions, (2) your config and package data are included in both distributions.
```
unzip -l dist/*.whl && tar --list -f dist/*.tar.gz
```
4. Test a local install of the package and run it to make sure it is working.
```
pip3 install .
pythonstarterpackage
```
5. After testing that it is working, uninstall the package from pip3.
```
pip3 uninstall pythonstarterpackage
```
If there are any issues in the above you can always uninstall the package and delete the distributions then proceed to troubleshoot the issue. Once complete start over from the beginning. The commands below allows you to delete the distributions.
```
rm -rf build dist src/*.egg-info
```
BE CAREFUL not to miss copy the above command, as if you delete something you didn't intend you will not be able to retrieve.

### Upload to PyPi
In order to upload to PyPi make sure to setup your PyPi account first. See "PyPi Setup Guide.md" in ```doc/``` for more details. You will also need to have ```twine``` installed and upgraded. Once you have all of this setup do the following:

1. Upload using ```twine```.
```
twine upload dist/*
```
2. Install your package with ```pip```.
```
pip3 install pythonstarterpackage
```
Note: If you get a "Requirements already satisfied..." for pythonstarterpackage when trying to install, it may be because ```pip``` still thinks you have the package already installed from the testing earlier. To cleanly break that connection, simply delete the ```./src/PythonStarterPackage.egg-info```. Then try uninstalling and reinstalling again.

3. Finally, run the app with: ```pythonstarterpackage```.
4. Uninstall with: ```pip3 uninstall pythonstarterpackage```.

## Troubleshooting
This section goes over some of the common issues found and how to resolve them.

### "Command Not Found" Error When Running the App
On Linux, if you are getting a ```command not found``` error when trying to run the app, you may need to add ```~/.local/bin/``` to PATH. See this thread for details: https://stackoverflow.com/a/34947489. To add ```~/.local/bin/``` to PATH do the following:

1. Add ```export PATH=~/.local/bin:$PATH``` to ```~/.bash_profile```.
```
echo export PATH=~/.local/bin:$PATH > ~/.bash_profile
```
2. Execute command.
```
source ~/.bash_profile
```

### Instructions for Git Bash
For Windows and Mac, it is recommended to run this app on a linux emulation layer like the Git Bash terminal. Here are the instructions for installing and setting up Git Bash:
1. Go to https://git-scm.com/downloads and click download.
```
Version >= 2.34.1
```
2. During the installation setup, make sure to include OpenSSH. Recommenced setting should be fine:
```
Use bundled OpenSSH - This uses ssh.exe that comes with Git.
```
3. Leave the other settings as default, click through, and install.
4. Open ```bash.exe``` and install Python3 https://www.python.org/downloads/.
5. Proceed to the "Installation" section to install this app.

IMPORTANT: For Windows, use the ```bash.exe``` terminal rather ```git-bash.exe```. There is a known issue with ```git-bash.exe``` messing up Python ```os``` commands in ```import os```. See this thread for details: https://stackoverflow.com/a/33623136.
* You can find ```bash.exe``` Git folder in the ```bin/``` directory. For example: If ```git-bash.exe``` is here ```C:\Program Files\Git\git-bash.exe``` then you should find ```bash.exe``` here ```C:\Program Files\Git\bin\bash.exe```.

## Support and Contributions
Our software is open source and free for public use. If you found any of these repos useful and would like to support this project financially, feel free to donate to our bitcoin address.

Bitcoin Address 1: 1GZQY6hMwszqxCmbC6uGxkyD5HKPhK1Pmf

![alt text](https://github.com/ArcticTechnology/BitcoinAddresses/blob/master/btcaddr1.png?raw=true)
