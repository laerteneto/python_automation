import os


class FilesManipulator:

    @staticmethod
    def SelectLastModifiedFileInPath(folder_path="C:\\Users\\lmesquit\\Downloads"):
        os.chdir(folder_path)
        files = filter(os.path.isfile, os.listdir(folder_path))
        files = [os.path.join(folder_path, f) for f in files]  # add path to each file
        files.sort(key=lambda x: os.path.getmtime(x))
        return files[-1]
