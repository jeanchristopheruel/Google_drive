import os
from os import listdir
from os.path import isfile, join
from google.colab import auth
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.client import GoogleCredentials


class Google_drive:
    def __init__(self, mycreds_file=None):
        self.mycreds_file = mycreds_file
        self.drive = None

        self.authenticate_pydrive__()

    def authenticate_pydrive__(self):
        if self.mycreds_file is None:
            mycreds_file = 'mycreds.json'
            with open(mycreds_file, 'w') as f:
                f.write('')
        else:
            mycreds_file = self.mycreds_file

        gauth = GoogleAuth()

        # https://stackoverflow.com/a/24542604/5096199
        # Try to load saved client credentials
        gauth.LoadCredentialsFile(mycreds_file)
        if gauth.credentials is None:
            # Authenticate if they're not there
            auth.authenticate_user()
            gauth.credentials = GoogleCredentials.get_application_default()
        elif gauth.access_token_expired:
            # Refresh them if expired
            gauth.Refresh()
        else:
            # Initialize the saved creds
            gauth.Authorize()
        # Save the current credentials to a file
        gauth.SaveCredentialsFile(mycreds_file)
        self.drive = GoogleDrive(gauth)

    def print_all_versions(self, name, drive_dir_ID):
        handle = drive_handle_model(self.drive, name, drive_dir_ID)
        handle.print_all_versions()

    def load_version(self, name, local_dir, drive_dir_ID, specific_version=None):
        handle = drive_handle_model(self.drive, name, drive_dir_ID)
        handle.load_saved_states(local_dir, specific_version=specific_version)

    def upload_model(self, name, local_file, drive_dir_ID):
        handle = drive_handle_model(self.drive, name, drive_dir_ID)
        handle.upload_model(local_file)

    def load_all(self, local_dir, drive_dir_ID, force=False):
        self.local_dir = local_dir
        self.drive_dir_ID = drive_dir_ID

        if not os.path.exists(self.local_dir):
            os.makedirs(self.local_dir)

        ID = "\'{}\' in parents".format(self.drive_dir_ID)
        file_list = self.drive.ListFile(
            {'q': ID}).GetList()

        print('Checking for new files...')
        already_down = [f for f in listdir(self.local_dir) if isfile(join(self.local_dir, f))]
        files = {f['title']: f['id'] for f in file_list}
        todownload = {keys for keys in files if keys not in already_down}

        number = 0
        if todownload:
            print('Downloading new files...')
            for name in todownload:
                local_file = os.path.join(self.local_dir, name)
                if force and os.path.isfile(local_file):
                    os.remove(local_file)
                file = self.drive.CreateFile({'id': files[name]})
                file_path = os.path.join(local_dir, file['title'])
                file.GetContentFile(file_path)
                number += 1
            print('{} new files dowloaded'.format(number))
        else:
            print('0 new files to download')

    def load_file(self, local_dir, file_ID):
        file = self.drive.CreateFile({'id': file_ID})
        file_path = os.path.join(local_dir, file['title'])

        if os.path.isfile(file_path):
            file.GetContentFile(file_path)
            print('{} loaded'.format(file['title']))
        else:
            print('{} already exists'.format(file['title']))

    def upload_file(self, local_path, drive_dir_ID):
        name = os.path.basename(local_path)
        file = self.drive.CreateFile({'parents': [{u'id': drive_dir_ID}], 'title': name})
        file.SetContentFile(local_path)
        file.Upload()


class drive_handle_model:
    def __init__(self, drive, name, drive_dir_ID):
        self.drive_dir_ID = drive_dir_ID
        self.name = name

        ID = "\'{}\' in parents".format(drive_dir_ID)
        file_list = drive.ListFile(
            {'q': ID}).GetList()
        self.get_specific_file = {f['title']: f['id'] for f in file_list if name in f['title']}
        self.versions = [int(s) for str in self.get_specific_file.keys() for s in str.split('__') if s.isdigit()]

    def print_all_versions(self):
        if len(self.versions) > 0:
            print('All versions available on Google drive: {}'.format(self.versions))
            print(self.versions)
        else:
            print('No previous version available on Google drive')

    def find_last_versions(self):
        if len(self.versions) > 0:
            return max(self.versions)
        else:
            return 0

    def load_saved_states(self, local_file, specific_version=None):
        self.print_all_versions()

        if len(self.versions) > 0:
            if not os.path.exists(os.path.dirname(local_file)):
                os.makedirs(os.path.dirname(local_file))

            if not os.path.isfile(local_file):
                if specific_version:
                    try:
                        version = specific_version
                        file_name = self.name + '_v__' + str(version) + '.state'
                        file_id = self.get_specific_file[file_name]
                        f_ = self.drive.CreateFile({'id': file_id})
                        f_.GetContentFile(local_file)
                        print('Version {} loaded from google Drive: {}'.format(specific_version, file_name))
                    except:
                        print('Model of specific_version {} not found on google Drive'.format(specific_version))
                else:
                    try:
                        version = self.find_last_versions()
                        file_name = self.name + '_v__' + str(version) + '.state'
                        file_id = self.get_specific_file[file_name]
                        f_ = self.drive.CreateFile({'id': file_id})
                        f_.GetContentFile(local_file)
                        print('Last version loaded from google Drive: {}'.format(file_name))
                    except:
                        print('Not able to load last version of the model from google Drive')
            else:
                print('No previous version available on Google drive')

    def upload_model(self, local_file):
        if os.path.isfile(local_file):
            last_version = self.find_last_versions()
            folder = self.drive.CreateFile({'parents': [{u'id': self.drive_dir_ID}],
                                            'title': self.name + '_v__' + str(last_version + 1) + '.state'})
            folder.SetContentFile(local_file)
            folder.Upload()
            print('Model uploaded under version {}'.format(last_version + 1))
        else:
            print('Model not saved: local_file does not exist')
