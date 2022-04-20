import os
from PIL import Image
from PIL.ExifTags import TAGS

class get_metadata:
    def metadata(filename, path, username=None):
        extensions = ['.png', '.jpeg', '.jpg', '.gif']

        monkey = os.path.join(path, filename)

        image = Image.open(monkey)

        exifdata = image.getexif()

        for tagid in exifdata:

            tagname = TAGS.get(tagid, tagid)

            value = exifdata.get