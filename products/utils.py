import os
from uuid import uuid4

class FileUpload:
    
    def __init__(self, dir, perfix):
        self.dir = dir
        self.perfix = perfix
        
    def upload_to(self, instance, filename):
        filename, ext = os.path.splitext(filename)
        return f"{self.dir}/{self.perfix}/{uuid4()}{ext}"
    