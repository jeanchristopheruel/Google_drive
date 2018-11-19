# Google_drive
Class for uploading and downloading files and handling file versions from Google drive

It was made essentially to make data sharing easier between Google Colaboratory and Google Drive so I can make sure my model is saved properly after a few hours of training even if the process is being killed for inactivity.


# Requirements
!pip install - U - q PyDrive


# methods
__Gd.upload_version(name, local_file, drive_dir_ID)__
This method uploads the file called __name__ available inside the local directory path __local_file__ to the Google Drive directory provided by its ID __drive_dir_ID__..

__Gd.print_all_versions(name, drive_dir_ID)__
Thsi method prints all current versions of a file called __name__ available inside the Google Drive directory provided by its ID __drive_dir_ID__.

__Gd.load_version(name, local_file, drive_dir_ID, specific_version=None)__
This method import file called __name__ available inside the Google Drive directory provided by its ID __drive_dir_ID__ and save it under the path __local_file__.
If specific_version is None, default version is the highest version.

__Gd.load_all(local_dir, drive_dir_ID, force=False)__
This method import all files available inside the Google Drive directory provided by its ID __drive_dir_ID__ to the local directory __local_dir__. __force__ allows overwriting 

__Gd.load_file(local_dir, file_ID)__
This method import file provided by its ID __file_ID__ into the the local directory __local_dir__.

__Gd.upload_file(local_path, drive_dir_ID)__
This method upload a file available inside the local directory path __local_file__ into the Google Drive directory provided by its ID __drive_dir_ID__.


# Exemple for Google colaboratory
!pip install - U - q PyDrive
import os
os.chdir('/content/')
!git clone https://github.com/ruelj2/Google_drive.git

from Google_drive.handle import Google_drive
Gd = Google_drive()

#This is a Google directory link: https://drive.google.com/drive/folders/1TcMSKVAgRXZXymxfBv3WouPkauSIIpDX
#This is its ID: '1TcMSKVAgRXZXymxfBv3WouPkauSIIpDX'
Gd.load_all('/content/projet/dataset', '1TcMSKVAgRXZXymxfBv3WouPkauSIIpDX')

local_file = os.path.join('project/networks/saved_models/', 'saved_state.state')
drive_dir_ID = '1TcMSKVAgRXZXymxfBv3WouPkauSIIpDX'
Gd.load_version(local_file, drive_dir_ID)

state = torch.load(local_file, map_location=lambda storage, loc: storage)
net.load_state_dict(state['state_dict'])
#Training...
state['state_dict'] = net.state_dict()
torch.save(state, local_file)

Gd.upload_model(local_file, drive_dir_ID)
