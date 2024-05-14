from PIL import Image, ImageFilter, ImageEnhance
from collections import namedtuple
import numpy as np
import constants
import requests
import model
import io

# --------------------------------------------------------------------------------
# Definitions
# --------------------------------------------------------------------------------

# a label and all meta information
Label = namedtuple('Label', [

    'name',  # The identifier of this label, e.g. 'car', 'person', ... .
    # We use them to uniquely name a class

    'id',  # An integer ID that is associated with this label.
    # The IDs are used to represent the label in ground truth images
    # An ID of -1 means that this label does not have an ID and thus
    # is ignored when creating ground truth images (e.g. license plate).

    'trainId',  # An integer ID that overwrites the ID above, when creating ground truth
    # images for training.
    # For training, multiple labels might have the same ID. Then, these labels
    # are mapped to the same class in the ground truth images. For the inverse
    # mapping, we use the label that is defined first in the list below.
    # For example, mapping all void-type classes to the same ID in training,
    # might make sense for some approaches.

    'category',  # The name of the category that this label belongs to

    'categoryId',  # The ID of this category. Used to create ground truth images
    # on category level.

    'hasInstances',  # Whether this label distinguishes between single instances or not

    'ignoreInEval',  # Whether pixels having this class as ground truth label are ignored
    # during evaluations or not

    'color',  # The color of this label
])

labels = [
    #       name                     id    trainId   category            catId     hasInstances   ignoreInEval   color
    Label('unlabeled', 0, 255, 'void', 0, False, True, (0, 0, 0)),
    Label('ego vehicle', 1, 255, 'void', 0, False, True, (0, 0, 0)),
    Label('rectification border', 2, 255, 'void', 0, False, True, (0, 0, 0)),
    Label('out of roi', 3, 255, 'void', 0, False, True, (0, 0, 0)),
    Label('static', 4, 255, 'void', 0, False, True, (0, 0, 0)),
    Label('dynamic', 5, 255, 'void', 0, False, True, (111, 74, 0)),
    Label('ground', 6, 255, 'void', 0, False, True, (81, 0, 81)),
    Label('road', 7, 0, 'ground', 1, False, False, (128, 64, 128)),
    Label('sidewalk', 8, 1, 'ground', 1, False, False, (244, 35, 232)),
    Label('parking', 9, 255, 'ground', 1, False, True, (250, 170, 160)),
    Label('rail track', 10, 255, 'ground', 1, False, True, (230, 150, 140)),
    Label('building', 11, 2, 'construction', 2, False, False, (70, 70, 70)),
    Label('wall', 12, 3, 'construction', 2, False, False, (102, 102, 156)),
    Label('fence', 13, 4, 'construction', 2, False, False, (190, 153, 153)),
    Label('guard rail', 14, 255, 'construction', 2, False, True, (180, 165, 180)),
    Label('bridge', 15, 255, 'construction', 2, False, True, (150, 100, 100)),
    Label('tunnel', 16, 255, 'construction', 2, False, True, (150, 120, 90)),
    Label('pole', 17, 5, 'object', 3, False, False, (153, 153, 153)),
    Label('polegroup', 18, 255, 'object', 3, False, True, (153, 153, 153)),
    Label('traffic light', 19, 6, 'object', 3, False, False, (250, 170, 30)),
    Label('traffic sign', 20, 7, 'object', 3, False, False, (220, 220, 0)),
    Label('vegetation', 21, 8, 'nature', 4, False, False, (107, 142, 35)),
    Label('terrain', 22, 9, 'nature', 4, False, False, (152, 251, 152)),
    Label('sky', 23, 10, 'sky', 5, False, False, (70, 130, 180)),
    Label('person', 24, 11, 'human', 6, True, False, (220, 20, 60)),
    Label('rider', 25, 12, 'human', 6, True, False, (255, 0, 0)),
    Label('car', 26, 13, 'vehicle', 7, True, False, (0, 0, 142)),
    Label('truck', 27, 14, 'vehicle', 7, True, False, (0, 0, 70)),
    Label('bus', 28, 15, 'vehicle', 7, True, False, (0, 60, 100)),
    Label('caravan', 29, 255, 'vehicle', 7, True, True, (0, 0, 90)),
    Label('trailer', 30, 255, 'vehicle', 7, True, True, (0, 0, 110)),
    Label('train', 31, 16, 'vehicle', 7, True, False, (0, 80, 100)),
    Label('motorcycle', 32, 17, 'vehicle', 7, True, False, (0, 0, 230)),
    Label('bicycle', 33, 18, 'vehicle', 7, True, False, (119, 11, 32)),
    Label('license plate', 34, 19, 'vehicle', 7, False, True, (0, 0, 142)),
]

id2color = {label.id: np.asarray(label.color) for label in labels}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in constants.ALLOWED_EXTENSIONS


def read_image_from_url(url):
    try:
        # Tải hình ảnh từ URL
        response = requests.get(url)

        # Đảm bảo request thành công
        if response.status_code == 200:
            # Đọc dữ liệu hình ảnh từ response
            image_data = response.content
            # # Tạo đối tượng hình ảnh từ dữ liệu nhận được
            img = Image.open(io.BytesIO(image_data))
            # # Lưu hình ảnh xuống thư mục với tên cụ thể
            img.save(constants.SAVE_PATH)

        return 'SUCCESS'

    except:
        return 'FAILED'


def preprocess_image(image_path):
    # Read Image
    image = Image.open(image_path)

    # IMAGE display
    image_display = image

    # Resize image
    image = image.resize(constants.IMAGE_SIZE)
    sharpness_factor = 3.0
    image = ImageEnhance.Sharpness(image)
    image = image.enhance(sharpness_factor)

    # Norm Image
    image = np.array(image) / 255

    return image, image_display


# def display_result(image_display, image_result):
#     # Chuyển đổi mảng numpy về định dạng hình ảnh PIL
#     image_display_pil = Image.fromarray(np.uint8(image_display))
#     image_result_pil = Image.fromarray(np.uint8(image_result))
#
#     # Resize hình ảnh nếu được chỉ định
#     image_display_pil = image_display_pil.resize(constants.DISPLAY_SIZE)
#     image_result_pil = image_result_pil.resize(constants.DISPLAY_SIZE)
#
#     # Tạo một hình ảnh mới có kích thước phù hợp để chứa cả hai hình ảnh cùng một dòng
#     width = image_display_pil.width + image_result_pil.width
#     height = max(image_display_pil.height, image_result_pil.height)
#     combined_image = Image.new('RGB', (width, height))
#
#     # Đặt hình ảnh hiển thị vào vị trí bên trái của hình ảnh kết quả
#     combined_image.paste(image_display_pil, (0, 0))
#
#     # Đặt hình ảnh kết quả vào vị trí bên phải của hình ảnh hiển thị
#     combined_image.paste(image_result_pil, (image_display_pil.width, 0))
#
#     # Nếu được chỉ định đường dẫn lưu, lưu hình ảnh xuống đường dẫn
#     combined_image.save(constants.SAVE_PATH)

def display_result(image_display, image_result, name=None):
    # Chuyển đổi mảng numpy về định dạng hình ảnh PIL
    image_display_pil = Image.fromarray(np.uint8(image_display))
    image_result_pil = Image.fromarray(np.uint8(image_result))

    # Resize hình ảnh nếu được chỉ định
    image_display_pil = image_display_pil.resize(constants.DISPLAY_SIZE)
    image_result_pil = image_result_pil.resize(constants.DISPLAY_SIZE)

    # Tăng cường độ sắc nét của hình ảnh kết quả
    image_result_pil = image_result_pil.filter(ImageFilter.SHARPEN)

    # Tạo một hình ảnh mới có kích thước phù hợp để chứa cả hai hình ảnh cùng một dòng
    width = image_display_pil.width + image_result_pil.width
    height = max(image_display_pil.height, image_result_pil.height)
    combined_image = Image.new('RGB', (width, height))

    # Đặt hình ảnh hiển thị vào vị trí bên trái của hình ảnh kết quả
    combined_image.paste(image_display_pil, (0, 0))

    # Đặt hình ảnh kết quả vào vị trí bên phải của hình ảnh hiển thị
    combined_image.paste(image_result_pil, (image_display_pil.width, 0))

    # Nếu được chỉ định đường dẫn lưu, lưu hình ảnh xuống đường dẫn
    combined_image.save(constants.SAVE_PATH if name is None else constants.UPLOAD_FOLDER + name)


def predict_image(image_path, name=None):
    image_np, image_display = preprocess_image(image_path)

    # Predict and reshape for segmentation
    prediction = model.app_model.predict(image_np.reshape([1] + list(constants.IMAGE_SHAPE)))
    prediction = np.argmax(prediction, axis=-1).squeeze()

    # Create an empty array for the result with the same height and width as the prediction and three channels for RGB
    image_result = np.zeros((prediction.shape[0], prediction.shape[1], 3), dtype='uint8')

    # Map each class ID to its corresponding color
    for class_id, color in id2color.items():
        image_result[prediction == class_id] = color

    display_result(image_display, image_result, name)
