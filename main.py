from ultralytics import YOLO
import utils

yolo_model = 'model/yolov8n.pt'
custom_yaml = 'dataset/dataset.yaml'
custom_model = 'model/blue_focus.pt'


@utils.timer
def train() -> YOLO:
    model = YOLO(yolo_model)

    model.train(data=custom_yaml, epochs=100)

    model.val(split='test')

    return model

@utils.timer
def load(path) -> YOLO:
    model = YOLO(path)
    return model


if __name__ == '__main__':
    model = train()
    # model = load(r"runs\detect\train9\weights\best.pt")

    # model.predict(r'D:\图片\steam\1203220_20240522144131_2.png', save=True)
