import shutil, os
import cv2


def check_output_path(s):
    for c in s:
        if (not (32 <= ord(c) <= 126)) or c == ' ':
            return False
    return True


def vedio2images(video_path, output_dir, image_prefix):
    if not check_output_path(output_dir):
        print('cv2库的图片输出路径不应含中文或空格')
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    vc = cv2.VideoCapture(video_path)
    
    if not vc.isOpened():
        print("无法打开视频文件:", video_path)
        return

    fps = vc.get(cv2.CAP_PROP_FPS)
    print(f'{video_path} 码率{fps}')

    cnt = 1
    while True:
        ret, frame = vc.read()
        if not ret:
            break
        output_path = os.path.join(output_dir, f'{image_prefix}_{cnt:08d}.jpg')
        cv2.imwrite(output_path, frame)
        cnt += 1

    vc.release()
    print(f'{video_path} 共计{cnt}帧\n')


if __name__ == '__main__':
    root_path = r'D:\Github\naraka_bladepoint_counter'

    video_dir = rf'{root_path}\videos'
    for file in os.listdir(video_dir):
        video_path = os.path.join(video_dir, file)
        if os.path.isfile(video_path):
            _, file_name = os.path.split(video_path)
            word = file_name.split('.')[0]
            output_dir = rf'{video_dir}\frames\{word}'
            image_prefix = word
            vedio2images(video_path, output_dir, image_prefix)