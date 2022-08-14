# MalwareDetector

Create virtual env (as long you didn't deleted it, run it on time):

```
python3 -m venv ./venv/ && ./venv/Scripts/activate.bat
```

Install dependencies:

```
pip3 install -r requirements.txt
```

To destroy virtual env:

```
deactivate && rm venv
```



for using pyvbox properly:

Go to VirtualBox’s downloads page (https://www.virtualbox.org/wiki/Downloads) and download the VirtualBox SDK.
Within the extracted ZIP file there is a directory called “installer".
Open a console within the installer directory and run "python vboxapisetup.py install" using your system Python. 
This installs vboxapi which is the interface that talks to VirtualBox via COM.

(vboxapi will be installed on your regular python modules and not on your venv, and its fine)