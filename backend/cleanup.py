import os
import time

folder = "storage"

def cleanup():

    now = time.time()

    for file in os.listdir(folder):

        path = os.path.join(folder, file)

        if os.stat(path).st_mtime < now - 3600:
            os.remove(path)