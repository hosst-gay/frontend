import os

class folder_control:

    def create(username):
        path = f'/mnt/volume_nyc1_02/imgs/{username}/'
        os.makedirs(path, exist_ok=True)

    def delete(username):
        path = f'/mnt/volume_nyc1_02/imgs/{username}/'
        os.removedirs(name=path)