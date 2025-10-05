import cv2
import numpy as np


def load_clothing(path):
    """Carga PNG con canal alpha y devuelve imagen BGR y máscara alpha (0/255)."""
    png = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if png is None:
        raise FileNotFoundError(path)
    if png.shape[2] == 4:
        bgr = png[:, :, :3]
        alpha = png[:, :, 3]
        mask = cv2.threshold(alpha, 1, 255, cv2.THRESH_BINARY)[1]
        return bgr, mask
    else:
        gray = cv2.cvtColor(png, cv2.COLOR_BGR2GRAY)
        mask = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)[1]
        return png, mask


def alpha_blend(bg, fg, mask, x, y):
    h, w = fg.shape[:2]
    H, W = bg.shape[:2]
    if x >= W or y >= H:
        return bg
    w_crop = min(w, W - x)
    h_crop = min(h, H - y)
    if w_crop <= 0 or h_crop <= 0:
        return bg
    roi = bg[y:y + h_crop, x:x + w_crop]
    fg_crop = fg[0:h_crop, 0:w_crop]
    mask_crop = mask[0:h_crop, 0:w_crop]
    alpha = (mask_crop.astype(float) / 255.0)[:, :, None]
    blended = (alpha * fg_crop.astype(float) + (1 - alpha) * roi.astype(float)).astype(np.uint8)
    bg[y:y + h_crop, x:x + w_crop] = blended
    return bg


def overlay_clothing(frame, clothing_img, clothing_mask, left, right, mid):
    # dimensiones de la prenda
    h_c, w_c = clothing_img.shape[:2]

    # puntos de referencia en la prenda (ajustables)
    src_left = np.array([int(0.2 * w_c), int(0.25 * h_c)])
    src_right = np.array([int(0.8 * w_c), int(0.25 * h_c)])
    src_mid = np.array([int(0.5 * w_c), int(0.7 * h_c)])

    src_tri = np.float32([src_left, src_right, src_mid])
    dst_tri = np.float32([left, right, mid])

    M = cv2.getAffineTransform(src_tri, dst_tri)
    warped = cv2.warpAffine(clothing_img, M, (frame.shape[1], frame.shape[0]),
                            flags=cv2.INTER_AREA, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0))
    warped_mask = cv2.warpAffine(clothing_mask, M, (frame.shape[1], frame.shape[0]),
                                 flags=cv2.INTER_NEAREST, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,))

    out = alpha_blend(frame, warped, warped_mask, 0, 0)
    return out
