# Color-Based Object Recognition in Changing Illumination using Normalized Histograms

**Course:** DS307 – Computer Vision  
**Assignment topic:** Project No. 14 — Class Histograms  
**Language:** Python

This project demonstrates histogram-based color recognition and evaluates how lighting changes affect recognition. It is designed as a student project with an image-based Streamlit interface and an optional live webcam script.

## What it does
- Compares a selected image region with saved reference color histograms.
- Uses HSV color space and normalized 2D Hue–Saturation histograms.
- Displays similarity scores and histogram visualizations.
- Lets you run a controlled experiment on normal, dim, and brightened images.
- Exports experiment results as CSV.
- Includes an optional OpenCV webcam demo.

> **Important scope note:** The core approach recognizes a color-distribution category, not arbitrary object identity. A red cup and a red ball may be confused if their color distributions are similar. The lighting experiment is included to measure robustness; histogram normalization does not guarantee illumination invariance.

## Project structure
```text
Color_Based_Object_Recognition_Project/
├── app.py                         # Streamlit application
├── webcam_demo.py                 # Optional live webcam demo
├── requirements.txt
├── README.md
├── report/
│   └── PROJECT_REPORT_TEMPLATE.md # Report structure and editable draft guidance
├── docs/
│   ├── methodology.md
│   └── viva_questions.md
├── src/
│   └── color_histogram.py          # Core histogram functions
├── data/
│   └── reference_images/           # Starter synthetic color reference images
└── results/                        # CSV output location
```

## Quick start on Windows
For a simple setup, double-click `setup_and_run.bat`. It creates a local virtual environment, installs dependencies, and starts the app. On later runs, double-click `run_app.bat`.

## Setup (Windows)
1. Install Python 3.10 or newer.
2. Extract the ZIP to a normal folder.
3. Open Command Prompt or the VS Code terminal in the extracted folder.
4. Create a virtual environment:
   ```bash
   py -m venv .venv
   .venv\Scripts\activate
   ```
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Launch the app:
   ```bash
   streamlit run app.py
   ```
7. Your browser should open the local app. If not, open the local address printed in the terminal.

## Camera input in Streamlit (important)
The **Recognize an image** tab contains `st.camera_input()`, which asks the browser to take a photo. The browser will not open the camera automatically; permission must be granted.

1. Open the app using the local URL printed by Streamlit, normally `http://localhost:8501`.
2. In Chrome, click the site-controls icon beside the address bar → **Site settings** → **Camera** → **Allow**.
3. Reload the app. Click the camera input and choose **Take photo** when prompted.
4. In Windows, open **Settings → Privacy & security → Camera** and enable **Camera access** and **Let desktop apps access your camera** if available.
5. Close apps that may be using the camera (Teams, Zoom, Camera app), then restart Chrome and Streamlit.

If the setting says **“Blocked to protect your privacy”**, check Windows camera privacy settings and any organization-managed Chrome policy. Do not expect the camera to work if the device has no webcam or it is disabled by a physical privacy switch.

**Note:** `st.camera_input()` takes a still photo; it is not a continuous live-video stream. Use the separate `webcam_demo.py` for continuous webcam preview.

## Run the webcam demo
With a webcam connected:
```bash
python webcam_demo.py
```
Place a single, mostly solid-colored object in the center of the frame. Press **Q** to quit. The webcam demo uses the included reference images and compares the center region; it is a simple demonstration, not a general-purpose object detector.

## How to use the Streamlit app
1. Open **Recognize an image** and upload a photo containing a mostly solid-colored object.
2. Crop/choose a region around the object using the displayed instructions or use a tightly framed image.
3. Select a reference category and review the similarity scores.
4. Open **Lighting experiment** to compare original, dimmed, and brightened versions.
5. Save the experiment CSV and use your actual measured results in the report.

## Dataset
The included starter references are synthetic solid-color patches with slight texture. They are for verifying the pipeline only. For a stronger evaluation:
- Capture 10–20 images per category (for example red, green, blue, yellow) under each lighting condition.
- Keep the object and camera distance approximately fixed.
- Record actual predictions and compute accuracy using labelled samples.
- Do not report synthetic demo results as real-world performance.

## Method summary
1. Convert BGR/RGB image to HSV.
2. Compute a 2D histogram over Hue and Saturation.
3. Normalize the histogram so its bins are comparable across image sizes.
4. Compare query and reference histograms using OpenCV's Bhattacharyya distance.
5. Convert distance to an intuitive similarity score for display: `100 × (1 − distance)`, clipped to 0–100. This is a presentation score, not a calibrated probability.

## Troubleshooting
- `streamlit is not recognized`: run `python -m streamlit run app.py`.
- Webcam not opening: close other camera apps; try changing camera index from `0` to `1` in `webcam_demo.py`.
- Poor recognition: use a tight crop with one dominant color, avoid mixed-color backgrounds, and collect better reference samples.
- Similarity is not accuracy: use labelled test images to calculate accuracy.

## Academic integrity
Use this package as a working starter implementation. Run it yourself, capture your own outputs, collect test data, and edit the report template to reflect what you actually did. Do not claim experiments or results that you have not run.
