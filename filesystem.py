import config
from config import FS_PATH
import os
from os.path import join

os.makedirs(FS_PATH, exist_ok=True)

def is_violating(user_id: int, rel_path: str):
    '''
    Check if the path is inside the user folder
    '''
    folder = join(config.FS_PATH, str(user_id))

    full_path = os.path.abspath(join(folder, rel_path))
    folder = os.path.abspath(folder)

    return not full_path.startswith(folder)

def path_from_id(user_id: int, rel_path: str):
    return join(FS_PATH, str(user_id), rel_path)

def ls(user_id: int, rel_path: str):
    results = []
    path = path_from_id(user_id, rel_path)

    with os.scandir(path) as entries:
        for entry in entries:
            file_path = join(rel_path, entry.name)
            is_file = entry.is_file()

            results.append({
                "filename": entry.name,
                "is_file": is_file
            })

    return sorted(results, key=lambda x: (x['is_file'], x['filename']))

if __name__ == "__main__":
    print(ls(1, '.'))
    pass