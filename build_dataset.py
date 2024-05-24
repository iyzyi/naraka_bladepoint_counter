# 从videos/frames/{name}目录下的target文件夹中获取含有检测目标的图像及其对应的标签数据；
# 从videos/frames/{name}目录下的background文件夹中获取不含检测目标的图像数据。
# 然后将其合并到:
#  1) dataset/images/target
#  2) dataset/labels/target
#  3) dataset/images/background

import os, shutil
import divide_dataset

frams_path = r'videos\frames'


def build_dataset():
    if not os.path.exists(divide_dataset.images_target_path):
        os.makedirs(divide_dataset.images_target_path)
    if not os.path.exists(divide_dataset.images_background_path):
        os.makedirs(divide_dataset.images_background_path)
    if not os.path.exists(divide_dataset.labels_target_path):
        os.makedirs(divide_dataset.labels_target_path)

    for item in os.listdir(frams_path):
        print(f'************** {item} **************')
        target_path = os.path.join(frams_path, item, 'target')
        background_path = os.path.join(frams_path, item, 'background')
        assert os.path.exists(target_path)
        assert os.path.exists(background_path)

        target_cnt = 0
        for file in os.listdir(target_path):
            if file.split('.')[-1] == 'jpg':
                image = file
                image_path = os.path.join(target_path, image)
                shutil.copy(image_path, os.path.join(divide_dataset.images_target_path, image))
                target_cnt += 1

                label = '.'.join(image.split('.')[:-1]) + '.txt'
                label_path = os.path.join(target_path, label)
                if not os.path.exists(label_path):
                    print(f'未找到 {image_path} 对应的标签文件')
                    return
                shutil.copy(label_path, os.path.join(divide_dataset.labels_target_path, label))
        print(f'target: {target_cnt}')

        background_cnt = 0
        for file in os.listdir(background_path):
            image_path = os.path.join(background_path, file)
            shutil.copy(image_path, os.path.join(divide_dataset.images_background_path, file))
            background_cnt += 1
        print(f'background: {background_cnt}')
        print()


if __name__ == '__main__':
    build_dataset()
