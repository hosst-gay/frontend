import os

class create_folder:

    def folder(username):
        path = f'/mnt/volume_nyc1_02/imgs/{username}/'
        os.makedirs(path, exist_ok=True)



