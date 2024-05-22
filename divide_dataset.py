import os, math
import random
import shutil

dataset_path = r'dataset'
images_path = rf'{dataset_path}\images'
images_all_path = rf'{images_path}\all'
images_train_path = rf'{images_path}\train'
images_val_path = rf'{images_path}\val'
labels_path = rf'{dataset_path}\labels'
labels_all_path = rf'{labels_path}\all'
labels_train_path = rf'{labels_path}\train'
labels_val_path = rf'{labels_path}\val'

train_proportion = 0.8


def divide_dataset():
    shutil.rmtree(images_train_path)
    shutil.rmtree(images_val_path)
    shutil.rmtree(labels_train_path)
    shutil.rmtree(labels_val_path)
    os.makedirs(images_train_path)
    os.makedirs(images_val_path)
    os.makedirs(labels_train_path)
    os.makedirs(labels_val_path)

    images = os.listdir(images_all_path)
    labels = os.listdir(labels_all_path)

    if len(images) + 1!= len(labels):
        print('图像与标签不匹配')
        return

    train_image_count = math.ceil(len(images) * train_proportion)
    train_images = random.sample(images, train_image_count)
    val_images = list(set(images) - set(train_images))

    def copy(images, type):
        for image in images:
            image_path = os.path.join(images_all_path, image)
            label = '.'.join(image.split('.')[:-1]) + '.txt'
            label_path = os.path.join(labels_all_path, label)
            if not os.path.exists(label_path):
                print(f'未找到 {image_path} 对应的标签文件')
                return

            shutil.copy(image_path, os.path.join(images_path, type, image))
            shutil.copy(label_path, os.path.join(labels_path, type, label))

    copy(train_images, 'train')
    copy(val_images, 'val')


if __name__ == '__main__':
    divide_dataset()
