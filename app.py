from pathlib import Path
import sys
import cv2
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from src.color_histogram import (
    as_bgr, normalized_hs_histogram, compare_to_references,
    adjust_brightness, H_BINS, S_BINS
)

REF_DIR = ROOT / "data" / "reference_images"
st.set_page_config(page_title="Color Histogram Recognition", page_icon="🎨", layout="wide")
st.title("🎨 Color-Based Object Recognition")
st.caption("DS307 Computer Vision • Normalized HSV Histograms • Illumination Robustness")

st.info(
    "This educational prototype compares the color distribution of an image region "
    "with reference histograms. It recognizes color-distribution categories, not arbitrary "
    "object identities. Similarity scores are not calibrated probabilities."
)

def load_references():
    refs = {}
    for path in sorted(REF_DIR.glob("*.png")):
        img = cv2.imread(str(path))
        if img is not None:
            refs[path.stem.replace("_", " ").title()] = normalized_hs_histogram(img)
    return refs

references = load_references()
if not references:
    st.error("No reference images found in data/reference_images/.")
    st.stop()

def show_histogram(image_bgr, title):
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv], [0, 1], None, [H_BINS, S_BINS], [0, 180, 0, 256])
    hist = cv2.normalize(hist, None, alpha=1, norm_type=cv2.NORM_L1)
    fig, ax = plt.subplots(figsize=(5, 2.6))
    im = ax.imshow(hist.T, origin="lower", aspect="auto")
    ax.set_title(title)
    ax.set_xlabel("Hue bins")
    ax.set_ylabel("Saturation bins")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    st.pyplot(fig, clear_figure=True)
    plt.close(fig)

tab1, tab2, tab3 = st.tabs(["Recognize an image", "Lighting experiment", "About the method"])

with tab1:
    st.subheader("Upload an image")
    uploaded = st.file_uploader("Upload a JPG or PNG image", type=["jpg", "jpeg", "png"], key="query")
    camera = st.camera_input("Or take a photo with your camera")
    chosen = uploaded if uploaded is not None else camera
    if chosen:
        pil = Image.open(chosen).convert("RGB")
        rgb = np.array(pil)
        bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
        col1, col2 = st.columns([1, 1])
        with col1:
            st.image(rgb, caption="Query image", use_container_width=True)
        ranked = compare_to_references(bgr, references)
        with col2:
            st.subheader("Ranked matches")
            result_df = pd.DataFrame(ranked)
            result_df["distance"] = result_df["distance"].map(lambda x: round(x, 4))
            result_df["similarity"] = result_df["similarity"].map(lambda x: round(x, 1))
            st.dataframe(result_df, hide_index=True, use_container_width=True)
            best = ranked[0]
            st.success(f"Closest color category: **{best['label']}**")
            st.metric("Histogram similarity score", f"{best['similarity']:.1f}/100")
            st.caption("A higher score means more similar histograms; it is not a probability.")
        show_histogram(bgr, "Query: normalized H–S histogram")
        st.download_button(
            "Download comparison as CSV",
            pd.DataFrame(ranked).to_csv(index=False).encode("utf-8"),
            file_name="recognition_comparison.csv",
            mime="text/csv"
        )
    else:
        st.write("Upload or capture a tightly framed image with one dominant color for the clearest demo.")
        st.image(str(REF_DIR / "red.png"), caption="Example reference patch", width=220)

with tab2:
    st.subheader("Lighting robustness experiment")
    st.write("Choose a query image, then compare its histogram against the reference classes after changing brightness.")
    experiment_upload = st.file_uploader("Upload a test image", type=["jpg", "jpeg", "png"], key="experiment")
    if experiment_upload:
        rgb = np.array(Image.open(experiment_upload).convert("RGB"))
        original = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
        factors = [("Dim (0.45×)", 0.45), ("Normal (1.00×)", 1.0), ("Bright (1.45×)", 1.45)]
        rows = []
        cols = st.columns(3)
        for col, (condition, factor) in zip(cols, factors):
            variant = adjust_brightness(original, factor)
            result = compare_to_references(variant, references)
            with col:
                st.image(cv2.cvtColor(variant, cv2.COLOR_BGR2RGB), caption=condition, use_container_width=True)
                st.write(f"**Prediction:** {result[0]['label']}")
                st.write(f"Similarity: {result[0]['similarity']:.1f}/100")
            rows.append({
                "condition": condition,
                "brightness_factor": factor,
                "predicted_category": result[0]["label"],
                "top_similarity_score": round(result[0]["similarity"], 3),
                "top_distance": round(result[0]["distance"], 5),
            })
        df = pd.DataFrame(rows)
        st.dataframe(df, hide_index=True, use_container_width=True)
        st.download_button("Download lighting experiment CSV", df.to_csv(index=False).encode("utf-8"),
                           "lighting_experiment.csv", "text/csv")
        st.warning("This experiment changes brightness in software. For a real-world study, also capture physical samples under different lamps and exposure settings.")
    else:
        st.write("Upload a test image to run the dim/normal/bright comparison.")

with tab3:
    st.subheader("Methodology")
    st.markdown("""
    1. **Color conversion:** Convert the image to HSV.
    2. **Feature extraction:** Calculate a two-dimensional histogram over Hue and Saturation.
    3. **Normalization:** Normalize histogram values so the total mass is 1.
    4. **Matching:** Compare query and reference histograms using Bhattacharyya distance.
    5. **Decision:** Rank the reference categories by smallest distance.
    6. **Evaluation:** Repeat under different brightness conditions and record actual predictions.
    """)
    st.latex(r"H(i,j) = \\frac{h(i,j)}{\\sum_{i,j} h(i,j)}")
    st.latex(r"D_B(H_1,H_2)=\\sqrt{1-\\sum_i\\sqrt{H_1(i)H_2(i)}}")
    st.markdown("""
    **Limitations**
    - Histogram matching ignores spatial arrangement.
    - A crop containing multiple colors can reduce reliability.
    - Hue becomes unreliable for very low-saturation pixels.
    - Normalization controls histogram scale but does not fully solve illumination changes.
    - The similarity display score is only a transformed distance, not a statistical confidence probability.
    """)
    st.subheader("Reference categories")
    st.write(", ".join(references.keys()))
    st.caption("Starter references are synthetic color patches. Replace or supplement them with your own captured samples for a valid evaluation.")
