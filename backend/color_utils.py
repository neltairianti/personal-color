import cv2
import numpy as np


FACE_CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades
    + "haarcascade_frontalface_default.xml"
)


def detect_face(image):

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    faces = FACE_CASCADE.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(100, 100)
    )

    if len(faces) == 0:
        return None

    return max(
        faces,
        key=lambda f: f[2] * f[3]
    )


def extract_skin_pixels(image, face):

    x, y, w, h = face

    # Area pipi kiri
    left = image[
        int(y + 0.45 * h):
        int(y + 0.70 * h),

        int(x + 0.15 * w):
        int(x + 0.42 * w)
    ]

    # Area pipi kanan
    right = image[
        int(y + 0.45 * h):
        int(y + 0.70 * h),

        int(x + 0.58 * w):
        int(x + 0.85 * w)
    ]

    pixels = np.concatenate(
        [
            left.reshape(-1, 3),
            right.reshape(-1, 3)
        ],
        axis=0
    )

    return pixels


def extract_features(image):

    face = detect_face(image)

    if face is None:
        raise ValueError(
            "Wajah tidak ditemukan"
        )

    pixels = extract_skin_pixels(
        image,
        face
    )

    if len(pixels) == 0:
        raise ValueError(
            "Area kulit tidak ditemukan"
        )

    # BGR → RGB
    rgb = pixels[:, ::-1]

    rgb_mean = np.mean(
        rgb,
        axis=0
    )

    # BGR → LAB
    lab = cv2.cvtColor(
        pixels.reshape(-1, 1, 3),
        cv2.COLOR_BGR2LAB
    )

    lab = lab.reshape(-1, 3)

    lab_mean = np.mean(
        lab,
        axis=0
    )

    # =========================
    # HASIL FITUR
    # =========================

    return {
        "rgb_r": float(rgb_mean[0]),
        "rgb_g": float(rgb_mean[1]),
        "rgb_b": float(rgb_mean[2]),
        "lab_l": float(lab_mean[0]),
        "lab_a": float(lab_mean[1]),
        "lab_b": float(lab_mean[2])
    }