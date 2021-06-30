from mitmproxy import http
from mitmproxy.script import concurrent
from nudenet import NudeDetector
from PIL import Image, ImageDraw
import os
import base64
import cv2
import uuid

config = {
    # If enabled, only parts that are identified will be visible, and the rest of the image
    # will be blurred. This still takes `blocked_labels` into consideration, and parts matching
    # those labels will be visible.
    "invert": True,

    # Labels included in this list will be censored. Or, if `invert` is set to true, only these
    # labels will be visible in an image, and the rest will be blurred. Available labels can be
    # found in NudeNet's documentation: https://github.com/notAI-tech/NudeNet
    "blocked_labels": [
        # "EXPOSED_ANUS",
        # "EXPOSED_ARMPITS",
        "COVERED_BELLY",
        # "EXPOSED_BELLY",
        # "COVERED_BUTTOCKS",
        # "EXPOSED_BUTTOCKS",
        "FACE_F",
        # "FACE_M",
        "COVERED_FEET",
        "EXPOSED_FEET",
        # "COVERED_BREAST_F",
        # "EXPOSED_BREAST_F",
        # "COVERED_GENITALIA_F",
        # "EXPOSED_GENITALIA_F",
        # "EXPOSED_BREAST_M",
        # "EXPOSED_GENITALIA_M"
    ],

    # The directory that cached image files should be stored in
    "cache_dir": "cache",

    # The minimum content size for an image to be considered for censorship.
    # This filters out small images like icons, thumbnails, etc.
    "min_content_size": 25000,

    # The proxy will only pay attention to responses with a Content-Type included in the list below.
    # This allows you to filter out non-image types, or types of images that aren't relevant (e.g. SVGs).
    "image_content_types": [
        "image/jpeg",
        "image/png",
        "image/webp"
    ],

    # This is a mapping of the above content types to their relevant extensions. Eventually
    # this could probably be automated.
    "image_extensions": {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp"
    },

    # This is a mapping of the above content types to their relevant pillow/PIL types. When
    # we call image.save() we pass it one of these values. Eventually this could probably be
    # automated.
    "image_pil_types": {
        "image/jpeg": "JPEG",
        "image/png": "PNG",
        "image/webp": "WEBP"
    }
}

# Initialize NudeNet
detector = NudeDetector()

# Create the cache dir if necessary
if not os.path.isdir(config["cache_dir"]):
    os.mkdir(config["cache_dir"])


@concurrent
def response(flow):
    if flow.request.method != "GET":
        print("Ignoring " + flow.request.method + " request")
        return

    content_type = flow.response.headers.get("Content-Type")
    content_size = flow.response.headers.get("Content-Length")

    # Ignore non-image content types completely
    if not is_valid_content_type(content_type):
        print("Ignoring content type")
        return

    # Ignore images with small file sizes
    if not is_large_enough_file(content_size):
        print("Ignoring small image: " + content_size)
        return

    tmp_file_name = get_temp_file_name(flow.request.url, content_type)

    # Write the image file to a temporary location
    # TODO: Ideally we could do more processing in-memory rather than relying on the filesystem
    if os.path.isfile(tmp_file_name):
        os.remove(tmp_file_name)

    with open(tmp_file_name, "xb") as file:
        file.write(flow.response.content)

    # Detect any censor-able parts in the image and initialize it with PIL
    results = detector.detect(tmp_file_name, mode='fast')

    # Censor the image
    if config["invert"] and len(results) > 0:
        censor_inverted(tmp_file_name, results)
    else:
        censor(tmp_file_name, results, content_type)

    # Respond with the censored image
    with open(tmp_file_name, 'rb') as f:
        content = f.read()
        flow.response = http.HTTPResponse.make(200, content, flow.response.headers)


def is_valid_content_type(content_type):
    if content_type is None or content_type not in config["image_content_types"]:
        return False

    return True


def get_temp_file_name(url, content_type):
    random_name = str(uuid.uuid4())
    extension = config["image_extensions"][content_type]
    return config["cache_dir"] + "/" + random_name + extension


def censor_inverted(tmp_file_name, results):
    image = cv2.imread(tmp_file_name)
    temp = image.copy()
    factor = 5.0

    (h, w) = image.shape[:2]

    k_w = int(w / factor)
    k_h = int(h / factor)

    # ensure the width of the kernel is odd
    if k_w % 2 == 0:
        k_w -= 1
    # ensure the height of the kernel is odd
    if k_h % 2 == 0:
        k_h -= 1

    image = cv2.GaussianBlur(image, (k_w, k_h), 0)

    for result in results:
        label = result['label']

        if label not in config["blocked_labels"]:
            continue

        x = result['box'][0]
        y = result['box'][1]
        w = result['box'][2]
        h = result['box'][3]

        part = temp[y:h, x:w]
        image[y:h, x:w] = part

    cv2.imwrite(tmp_file_name, image)


def censor(tmp_file_name, results, content_type):
    image = Image.open(tmp_file_name)
    draw = ImageDraw.Draw(image)

    # Draw rectangles over each censor result
    for result in results:
        label = result['label']

        if label not in config["blocked_labels"]:
            continue

        x = result['box'][0]
        y = result['box'][1]
        w = result['box'][2]
        h = result['box'][3]

        draw.rectangle(
            ((x, y), (w, h)),
            fill="black"
        )

    # Write the censored image back to the temp location
    image.save(tmp_file_name, config["image_pil_types"][content_type])


def is_large_enough_file(content_size):
    return int(content_size) > config["min_content_size"]
