import os


class FilesManipulator:

    @staticmethod
    def SelectLastModifiedFileInPath():
        path = os.path.abspath('temp/')
        files = os.listdir(path)
        paths = [os.path.join(path, basename) for basename in files]
        return max(paths, key=os.path.getctime)
