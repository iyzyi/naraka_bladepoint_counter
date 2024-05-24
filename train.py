from ultralytics import YOLO
import utils

yolo_model = 'model/yolov8n.pt'
custom_yaml = 'dataset/dataset.yaml'
custom_model = 'model/blue_focus.pt'
# model.save我用起来一直有bug，因此训练好模型后需要手动将
# runs\detect\trainN\weights\best.pt复制到上述路径


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
    #model = train()
    model = load(custom_model)

    @utils.timer
    def predict(model, image, target_class, confidence_threshold):
        results = model.predict(image)  # , save=True)

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
        return detected

    target_class = 'blue_focus'
    confidence_threshold = 0.25

    # 好像第一次预测会慢，后面就很快了
    image = r'D:\图片\steam\永劫无间\1203220_20240522144157_1.png'
    result = predict(model, image, target_class, confidence_threshold)
    print(result)

    image = r'D:\图片\steam\永劫无间\1203220_20240522144156_2.png'
    result = predict(model, image, target_class, confidence_threshold)
    print(result)