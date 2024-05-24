import threading, queue, time, os, shutil
import cv2
import numpy as np
import pyautogui
os.environ['YOLO_VERBOSE'] = str(False)
from ultralytics import YOLO
import win32api, win32con
import utils
import train
import mouse_focus

model = YOLO(train.custom_model)
print(f'模型{train.custom_model}加载完成')

fps = 20
target_class = 'blue_focus'
confidence_threshold = 0.5
queue_get_timeout = 1
is_running = False
process_name = 'NarakaBladepoint.exe'
temp_dir = r'd:\temp'

images_queue = queue.Queue()
result_queue = queue.Queue()
target_pid = mouse_focus.get_pid_by_name(process_name)
if os.path.exists(temp_dir):
    shutil.rmtree(temp_dir)
os.makedirs(temp_dir)


def screenshot_thread_func():
    frame_interval = 1.0 / fps
    frame_index = 0

    while is_running:
        begin = time.time()
        screenshot = pyautogui.screenshot()
        image = screenshot
        images_queue.put((frame_index, begin, image))
        frame_index += 1
        end = time.time()
        if (end - begin) < frame_interval:
            time.sleep(frame_interval - (end - begin))


def detect_thread_func():
    while is_running:
        try:
            frame_index, timestamp, image = images_queue.get(timeout=queue_get_timeout)
        except queue.Empty:
            continue
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        time_str = utils.time2str(timestamp)

        #@utils.timer
        def predict(model, image, target_class, confidence_threshold):
            results = model.predict(image)# , save=True)

            reverse_dict = {v: k for k, v in model.names.items()}
            target_class_index = reverse_dict.get(target_class)

            detected = False
            for result in results:
                for box in result.boxes:
                    cls_index = int(box.cls.item())
                    confidence = float(box.conf.item())
                    if cls_index == target_class_index and confidence >= confidence_threshold:
                        detected = True
                        break
                if detected:
                    break

            if detected:
                return results[0]
            return None

        result = predict(model, image, target_class, confidence_threshold)
        if result:
            result_queue.put((frame_index, time_str))
            result.save(f'{temp_dir}/{frame_index}_{time_str}.jpg')


def keypress_thread_func(counter_key):
    last_index = -1

    while is_running:
        try:
            result = result_queue.get(timeout=queue_get_timeout)
        except queue.Empty:
            continue
        frame_index, timestamp = result

        def on_mouse_focus(func):
            def wrapper(*args, **kwargs):
                if mouse_focus.is_mouse_focus_on(target_pid):
                    return func(*args, **kwargs)
            return wrapper

        @on_mouse_focus
        def keypress(key, delay_seconds=0.01):
            # key实际上应为VK_CODE
            # https://learn.microsoft.com/zh-cn/windows/win32/inputdev/virtual-key-codes
            assert isinstance(key, int) or isinstance(key, str)
            if isinstance(key, str):
                key = ord(key)
            win32api.keybd_event(key, win32api.MapVirtualKey(key, 0), 0, 0)
            time.sleep(delay_seconds)
            win32api.keybd_event(key, win32api.MapVirtualKey(key, 0), win32con.KEYEVENTF_KEYUP, 0)

        if frame_index > last_index:
            print(f'{frame_index} {timestamp} keypress {counter_key}')
            keypress(counter_key)
            last_index = frame_index


def start(counter_key):
    global is_running
    if is_running:
        print('[ERROR] 不允许并发运行')
        return
    is_running = True

    # 截图线程
    screenshot_thread = threading.Thread(target=screenshot_thread_func)
    screenshot_thread.daemon = True
    screenshot_thread.start()

    # 识别线程
    recognize_threads = []
    for i in range(8):
        recognize_thread = threading.Thread(target=detect_thread_func)
        recognize_thread.daemon = True
        recognize_threads.append(recognize_thread)
        recognize_thread.start()

    # 按键线程
    keypress_thread = threading.Thread(target=keypress_thread_func, args=(counter_key,))
    keypress_thread.daemon = True
    keypress_thread.start()

    # 阻塞主线程
    screenshot_thread.join()
    for recognize_thread in recognize_threads:
        recognize_thread.join()
    keypress_thread.join()

    is_running = False


def stop():
    global is_running
    is_running = False



if __name__ == '__main__':
    counter_key = 'R'   # 默认是G，我改过键位
    start(counter_key)
