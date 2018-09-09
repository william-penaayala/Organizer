#!/usr/bin/env python3

# avoid using this file.

import os, glob, datetime

from ImageSpells import *
from SpellReference import *


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
                #print(saved_object)
                input_MagicPool.insert_proper(saved_object, saved_object.local_id)
        return True







#test = MagicImage(r"C:\Users\Admin\Desktop\Python\Organizer\Source_Images\7UwGxc_NKC6MLYhCvac-UoPjvCHS5cUC4Av4iEYKy48.jpg", 0, r".jpg")
#test2 = MagicGif(r"C:\Users\Admin\Desktop\Python\Organizer\Source_Images\pose.gif", 1)

#test.tags.extend(["german_shepherd", "brick", "day", "dog", "canine"])
#test2.tags.extend(["border_collie", "animated", "dog", "canine", "hug"])
#test.tags.sort()
#test2.tags.sort()

#print(test.tags)
#print(test2.tags)

#test_pool = MagicPool()
#test_pool.insert(test)
#test_pool.insert(test2)

#print(test_pool.pool)
#print(test_pool.get(0), test_pool.get(1))



#test_saver = MagicSaveLoader()
#test_saver.save(test_pool)
#test_saver.load(test_pool,'',True)

#print(test_pool.pool)
#print(test_pool.get(0).return_save_string())
#print(test_pool.get(1).return_save_string())

#a = input("hello there") '''
