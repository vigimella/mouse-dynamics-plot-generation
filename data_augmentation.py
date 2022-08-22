import os
from numpy import expand_dims
from tensorflow.keras.utils import load_img, img_to_array
from keras.preprocessing.image import ImageDataGenerator
import scipy.integrate as integrate

from matplotlib import pyplot


def augmentation(folder_path, augmentation_folder):

    files_list = []

    for root, directories, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.png'):
                files_list.append(os.path.join(root, file))

    for file in files_list:

        print("Augmentation of " + file + " file in progress...")
        img = load_img(file)
        # convert to numpy array
        data = img_to_array(img)
        # expand dimension to one sample
        samples = expand_dims(data, 0)
        # create image data augmentation generator
        datagen = ImageDataGenerator(width_shift_range=[-200, 200])
        # prepare iterator
        it = datagen.flow(samples, batch_size=1, save_to_dir=augmentation_folder, save_prefix='aug', save_format='png')
        # generate samples and plot
        for i in range(9):
            batch = it.next()
        datagen = ImageDataGenerator(height_shift_range=0.5)
        it = datagen.flow(samples, batch_size=1, save_to_dir=augmentation_folder, save_prefix='aug', save_format='png')
        for i in range(9):
            batch = it.next()
        datagen = ImageDataGenerator(horizontal_flip=True)
        it = datagen.flow(samples, batch_size=1, save_to_dir=augmentation_folder, save_prefix='aug', save_format='png')
        for i in range(9):
            batch = it.next()
        datagen = ImageDataGenerator(rotation_range=90)
        it = datagen.flow(samples, batch_size=1, save_to_dir=augmentation_folder, save_prefix='aug', save_format='png')
        for i in range(9):
            batch = it.next()
        datagen = ImageDataGenerator(brightness_range=[0.2, 1.0])
        it = datagen.flow(samples, batch_size=1, save_to_dir=augmentation_folder, save_prefix='aug', save_format='png')
        for i in range(9):
            batch = it.next()
        datagen = ImageDataGenerator(zoom_range=[0.5, 1.0])
        it = datagen.flow(samples, batch_size=1, save_to_dir=augmentation_folder, save_prefix='aug', save_format='png')
        for i in range(9):
            batch = it.next()
