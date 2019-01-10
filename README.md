# Google_drive
A simple Class for uploading and downloading files and handling file versions from Google drive  
  
It was made essentially to make data sharing easier between Google Colaboratory and Google Drive so I can make sure my model is saved properly after a few hours of training even if the process is being killed for inactivity.  


# Requirements
!pip install - U - q PyDrive  


# methods
```Gd = Google_drive()```   
Call main class

```Gd.upload_version(local_file, drive_dir_ID)```    
This method uploads the file called by __os.path.basename(local_file)__ available inside the local directory path __local_file__ to the Google Drive directory provided by its ID __drive_dir_ID__*. Basename of local_file must be the same as used in load_version().

```Gd.load_version(local_file, drive_dir_ID, specific_version=None)```     
This method import file called by __os.path.basename(local_file)__ (if possible) available inside the Google Drive directory provided by its ID __drive_dir_ID__* and save it under the path __local_file__. Basename of local_file must be the same as used in upload_version().
If specific_version is None, default version is the highest version.

```Gd.print_all_versions(filename, drive_dir_ID) ```   
This method prints all current versions of a file called __filename__ available inside the Google Drive directory provided by its ID __drive_dir_ID__*.

```Gd.load_all(local_dir, drive_dir_ID, force=False)```     
This method import all files available inside the Google Drive directory provided by its ID __drive_dir_ID__* to the local directory path. Also, __local_dir__. __force__ allows overwriting. The Google Drive directory must exclusively gather files.

```Gd.load_file(local_dir, file_ID)```   
This method import file provided by its ID __file_ID__* into the the local directory path __local_dir__.

```Gd.upload_file(local_path, drive_dir_ID)```    
This method upload a file available inside the local path __local_file__ into the Google Drive directory provided by its ID __drive_dir_ID__*.

\* The shared link of google directory/file provided by its __ID__ must be activated. 

# featured function 
```loadURL(local_dir, URL)```     
This method download a file from arbitrary URL inside the local directory path __local_dir__. If the file is zipped, it will unzip it (based on URL basename).


# Exemple for Google colaboratory
```
!pip install - U - q PyDrive  
import os  
os.chdir('/content/')  
!git clone https://github.com/ruelj2/Google_drive.git  
  
from Google_drive.handle import *
Gd = Google_drive()  
  
#This is a Google directory link: https://drive.google.com/drive/folders/1TcMSKVAgRXZXymxfBv3WouPkauSIIpDX  
#This is its ID: '1TcMSKVAgRXZXymxfBv3WouPkauSIIpDX'  
Gd.load_all('/content/projet/dataset', '1TcMSKVAgRXZXymxfBv3WouPkauSIIpDX')  
  
local_file = 'path/to/local/file'
drive_dir_ID = '1TcMSKVAgRXZXymxfBv3WouPkauSIIpDX'  
Gd.load_version(local_file, drive_dir_ID)  
  
'''
Loading Model from local file;
Training Model;
Saving Model to local file.
'''
  
Gd.upload_version(local_file, drive_dir_ID)  
```

# Use on local machine:
For a local machine, colabtools repo must be installed  
```
$ git clone https://github.com/googlecolab/colabtools.git  
$ cd colabtools  
$ python setup.py install  
```
  
To learn more: https://stackoverflow.com/questions/50194637/colaboratory-how-to-install-and-use-on-local-machine  
