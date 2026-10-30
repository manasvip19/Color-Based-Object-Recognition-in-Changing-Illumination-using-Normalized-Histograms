"""Optional live webcam demo: compares the center crop to reference histograms."""
from pathlib import Path
import cv2
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from src.color_histogram import normalized_hs_histogram, compare_to_references

REF_DIR = ROOT / "data" / "reference_images"

def main():
    references = {}
    for path in sorted(REF_DIR.glob("*.png")):
        img = cv2.imread(str(path))
        if img is not None:
            references[path.stem.replace("_", " ").title()] = normalized_hs_histogram(img)
    if not references:
        raise SystemExit("No reference images found in data/reference_images/.")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise SystemExit("Could not open webcam. Try changing camera index 0 to 1.")
    print("Place a mostly solid-colored object in the center box. Press Q to quit.")
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        h, w = frame.shape[:2]
        box_w, box_h = max(80, w // 3), max(80, h // 3)
        x1, y1 = (w - box_w) // 2, (h - box_h) // 2
        crop = frame[y1:y1 + box_h, x1:x1 + box_w]
        results = compare_to_references(crop, references)
        best = results[0]
        cv2.rectangle(frame, (x1, y1), (x1 + box_w, y1 + box_h), (0, 255, 0), 2)
        label = f"{best['label']} | similarity {best['similarity']:.1f}/100"
        cv2.putText(frame, label, (15, 35), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, "Q: quit | Center crop is compared (not object detection)",
                    (15, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (255, 255, 255), 1, cv2.LINE_AA)
        cv2.imshow("Color Histogram Recognition", frame)
        if cv2.waitKey(1) & 0xFF in (ord("q"), ord("Q")):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
