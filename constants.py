UPLOAD_FOLDER = 'static/uploads/'
SAVE_PATH = UPLOAD_FOLDER + 'downloaded.jpg'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
# 5 GB
MAX_CONTENT_LENGTH = 5 * 1024 * 1024 * 1024

# IMAGEE SIZE AND SHAPE
IMAGE_SIZE = [128, 128]
IMAGE_SHAPE = IMAGE_SIZE + [3,]

DISPLAY_SIZE = [512, 512]