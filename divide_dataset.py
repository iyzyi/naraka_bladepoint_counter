# 将 dataset/image/target 和 dataset/label/target

import os, math
import random
import shutil

dataset_path = r'dataset'
images_path = rf'{dataset_path}\images'
images_target_path = rf'{images_path}\target'
images_background_path = rf'{images_path}\background'
labels_path = rf'{dataset_path}\labels'
labels_target_path = rf'{labels_path}\target'


def divide_dataset(train, val, test):
    # clean images/labels train/val/test set
    def clean_dir(path):
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)
    clean_dir(rf'{images_path}\train')
    clean_dir(rf'{images_path}\val')
    clean_dir(rf'{images_path}\test')
    clean_dir(rf'{labels_path}\train')
    clean_dir(rf'{labels_path}\val')
    clean_dir(rf'{labels_path}\test')

    # clean labels cache
    for file in os.listdir(labels_path):
        path = os.path.join(labels_path, file)
        if os.path.isfile(path) and file.split('.')[-1] == '.cache':
            os.remove(path)

    def divide(images, train, val, test):
        train_image_count = math.ceil(len(images) * (train / (train + val + test)))
        val_image_count = math.ceil(len(images) * (val / (train + val + test)))
        train_images = random.sample(images, train_image_count)
        val_images = random.sample(list(set(images) - set(train_images)), val_image_count)
        test_images = list(set(images) - set(train_images) - set(val_images))
        return train_images, val_images, test_images

    def copy(images, _class, type, need_label):
        cnt = 0
        for image in images:
            image_path = os.path.join(images_path, _class, image)
            shutil.copy(image_path, os.path.join(images_path, type, image))
            cnt += 1

            if need_label:
                label = '.'.join(image.split('.')[:-1]) + '.txt'
                label_path = os.path.join(labels_path, _class, label)
                if not os.path.exists(label_path):
                    print(f'未找到 {image_path} 对应的标签文件')
                    return
                shutil.copy(label_path, os.path.join(labels_path, type, label))
        print(f'{_class.ljust(12)}{type.ljust(8)}样本数量: {cnt}')

    target_images = os.listdir(images_target_path)
    target_labels = os.listdir(labels_target_path)

    if len(target_images) != len(target_labels):
        print('图像与标签数量不匹配')
        return

    target_train_images, target_val_images, target_test_images = divide(target_images, train, val, test)
    copy(target_train_images,  'target', 'train',True)
    copy(target_val_images, 'target', 'val', True)
    copy(target_test_images, 'target', 'test', True)

    background_images = os.listdir(images_background_path)
    background_train_images, background_val_images, background_test_images = divide(background_images, train, val, test)
    copy(background_train_images,  'background', 'train',False)
    copy(background_val_images, 'background', 'val', False)
    copy(background_test_images, 'background', 'test', False)


if __name__ == '__main__':
    divide_dataset(8, 2, 1)
