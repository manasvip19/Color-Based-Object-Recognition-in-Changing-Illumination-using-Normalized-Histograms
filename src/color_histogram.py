"""Core functions for normalized HSV histogram comparison."""
from __future__ import annotations
import cv2
import numpy as np

H_BINS = 30
S_BINS = 32

def as_bgr(image: np.ndarray, input_order: str = "RGB") -> np.ndarray:
    """Return a BGR uint8 image from RGB or BGR input."""
    if image is None or image.size == 0:
        raise ValueError("Image is empty.")
    arr = np.asarray(image)
    if arr.dtype != np.uint8:
        arr = np.clip(arr, 0, 255).astype(np.uint8)
    if input_order.upper() == "RGB":
        return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
    return arr.copy()

def normalized_hs_histogram(image_bgr: np.ndarray) -> np.ndarray:
    """Compute a normalized 2D histogram over Hue and Saturation."""
    if image_bgr is None or image_bgr.size == 0:
        raise ValueError("Image is empty.")
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv], [0, 1], None, [H_BINS, S_BINS],
                        [0, 180, 0, 256])
    hist = cv2.normalize(hist, None, alpha=1.0, norm_type=cv2.NORM_L1)
    return hist.astype(np.float32)

def bhattacharyya_distance(hist_a: np.ndarray, hist_b: np.ndarray) -> float:
    """Return OpenCV's Bhattacharyya distance; lower is more similar."""
    return float(cv2.compareHist(hist_a.astype(np.float32),
                                 hist_b.astype(np.float32),
                                 cv2.HISTCMP_BHATTACHARYYA))

def similarity_score(distance: float) -> float:
    """Map distance to a simple 0–100 display score (not a probability)."""
    return float(np.clip((1.0 - distance) * 100.0, 0.0, 100.0))

def compare_to_references(query_bgr: np.ndarray,
                          references: dict[str, np.ndarray]) -> list[dict]:
    """Rank reference histograms against a query image."""
    query_hist = normalized_hs_histogram(query_bgr)
    ranked = []
    for label, reference_hist in references.items():
        distance = bhattacharyya_distance(query_hist, reference_hist)
        ranked.append({
            "label": label,
            "distance": distance,
            "similarity": similarity_score(distance),
        })
    return sorted(ranked, key=lambda item: item["distance"])

def adjust_brightness(image_bgr: np.ndarray, factor: float) -> np.ndarray:
    """Scale V (brightness) in HSV while keeping H and S unchanged."""
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 2] = np.clip(hsv[:, :, 2] * factor, 0, 255)
    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
