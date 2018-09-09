#!/usr/bin/env python3
import os


class MagicImage:
    def get_size(self):
        if self.path is not None:
            return os.path.getsize(self.path)
        else:
            return None

    def get_dimensions(self):
        # TODO
        return (0,0)

    def __init__(self, path=None, local_id=None, image_type=None):
        self.path = path
        self.local_id = local_id
        self.tags = []
        self.sources = []
        self.image_type = image_type
        self.size = self.get_size()
        self.dimensions = self.get_dimensions()
        self.label = "no label"

    def sort_data(self):
        self.tags.sort()
        self.sources.sort()

    def return_save_string(self):
        if self.tags is not None:
            tags_printable = '[' + ','.join(self.tags) + ']'
        else:
            tags_printable = "EMPTY"

        if self.sources is not None:
            sources_printable = '[' + ','.join(self.sources) + ']'
        else:
            sources_printable = "EMPTY"

        inner_part = ','.join([self.path, str(self.local_id), tags_printable, sources_printable, self.image_type, self.label])
        result = self.__class__.__name__ + '<' + inner_part + '>'

        return result

    def load_from_save_string(self, save_string):
        content_start = save_string.find('<') + 1
        content_end = save_string.find('>')

        # stripping the extra bits, we only want what's between < and >. We move up based on the commas
        content = save_string[content_start : content_end]
        self.path = content[ :content.find(',')]
        content = content[(content.find(',')+1): ]
        self.local_id = content[ :content.find(',')]
        content = content[(content.find(',') + 1):]

        # make sure that EMPTY isn't replacing the place where the tags and sources should be. If not, read them -
        # -by splitting them by commas.
        if content.startswith("EMPTY"):
            self.tags = None
        else:
            self.tags = content[1:content.find(']')].split(",")
            content = content[content.find(']')+1:]
        content = content[(content.find(',') + 1):]
        if content.startswith("EMPTY"):
            self.sources = None
        else:
            self.sources = content[1:content.find(']')].split(",")
            content = content[content.find(']')+1:]
        content = content[(content.find(',') + 1):]

        # get the rest of the parameters and compute size, dimensions, then load the file
        self.image_type = content[ :content.find(',')]
        content = content[(content.find(',') + 1):]
        self.label = content[(content.find(',') + 1):]
        self.size = self.get_size()
        self.dimensions = self.get_dimensions()


class MagicGif(MagicImage):
    def __init__(self, path=None, local_id=None):
        MagicImage.__init__(self, path, local_id, ".gif")


class MagicDeletedImage(MagicImage):
    def __init__(self, local_id):
        self.path = None
        self.local_id = local_id
        self.tags = None
        self.sources = None
        self.image_type = None
        self.size = 0
        self.dimensions = (0,0)
        self.label = "deleted image."


class MagicTag:
    def __init__(self, name, parent_tag=None, child_tags=None):
        self.name = ''
        self.description = ''
        self.parent_tag = parent_tag
        self.child_tags = child_tags


class MagicSource:
    def __init__(self, URL=r"", website_name='', website_URL=r""):
        self.URL = URL
        self.website_name = website_name
        self.website_URL = website_URL

class MagicPool:
    def __init__(self, name="defaultPoolName"):
        self.name = name
        self.total_count = -1
        self.pool = {}

    # Returns an array of local ids of images containing the tag
    @staticmethod
    def search_by_tag(search_pool, tag):
        _result = []
        for local_id, image in search_pool:
            if(image.tags.contains(tag)):
                _result.append(local_id)
        return _result

    def insert(self, magic_image):
        self.pool[int(self.total_count)] = magic_image
        self.total_count += 1

    def insert_proper(self, magic_image, local_id):
        self.pool[int(local_id)] = magic_image
        self.total_count += 1

    def delete(self, local_id):
        self.pool[local_id] = MagicDeletedImage(local_id)

    def get(self, local_id):
        return self.pool.get(local_id, None)


class MagicSaveLoader:
    def __init__(self, cwd=os.getcwd(), folder_name="MagicCrumbs"):
        self.cwd = cwd
        self.folder_name = folder_name

    def set_cwd(self, cwd):
        self.cwd = cwd

    def save(self, input_MagicPool):
        files_at_cwd = glob.glob(self.cwd + "\\*")
        folder_path = self.cwd + "\\" + self.folder_name
        if folder_path not in files_at_cwd:
            try:
                os.mkdir(folder_path)
            except OSError:
                print("COULD NOT MAKE SAVE FOLDER")
                return False
        filename = datetime.datetime.today().strftime('%Y-%m-%d %H-%M-%S') + ' ' + input_MagicPool.name + ' MagicSave'
        file_path = folder_path + "\\" + filename
        try:
            savefile = open(file_path, "a")
        except OSError:
            return False

        for object_in_pool in input_MagicPool.pool.values():
            savefile.write(object_in_pool.return_save_string() + "\n")
        savefile.close()
        return True

    def load(self, input_MagicPool, input_savefile_path='', force_flag=False):
        if not force_flag:
            double_check = input("WARNING: This will CLEAR THE INPUT POOL and replace it! Type 'q' to quit!")
            if double_check == 'q':
                return False

        files_at_cwd = glob.glob(self.cwd + "\\*")
        folder_path = self.cwd + "\\" + self.folder_name
        if folder_path not in files_at_cwd:
            print("COULD NOT FIND SAVE FOLDER")
            return False

        if input_savefile_path != '':
            savefile_path = input_savefile_path
        else:
            files_at_folder = glob.glob(folder_path + "\\*")
            files_at_folder.sort()
            savefile_path = files_at_folder[0]

        with open(savefile_path) as savefile:
            lines = savefile.readlines()
            if len(lines) == 0:
                return False
            for line in lines:
                saved_object = None
                if line.startswith("MagicImage"):
                    saved_object = MagicImage()
                elif line.startswith("MagicGif"):
                    saved_object = MagicGif()
                saved_object.load_from_save_string(line)
                input_MagicPool.insert_proper(saved_object, saved_object.local_id)
        return True
