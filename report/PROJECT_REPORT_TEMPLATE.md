# DS307 Computer Vision — Assignment 2 Project Report Template

> Replace all bracketed fields. Add screenshots and real results from your own runs. Do not submit claims or results you have not verified.

## Title Page
**Color-Based Object Recognition in Changing Illumination using Normalized Histograms**

Submitted by: [Student name]  
Registration number: [Registration number]  
Program: [Program]  
Faculty name: [Faculty name]  
Course: DS307 – Computer Vision  
Institution: [Institution]  
Date: [Submission date]

## Abstract
This project implements a color-based recognition prototype using normalized Hue–Saturation histograms. Input images are converted into HSV color space, and a two-dimensional histogram is computed over the Hue and Saturation channels. The histogram is normalized and compared with reference histograms using Bhattacharyya distance. The application ranks reference color categories and provides a simple similarity score. An illumination experiment compares predictions for dimmed, normal, and brightened images. The purpose is to study the strengths and limitations of histogram-based recognition under brightness variation. Results should be completed using measured experiments from the final implementation.

**Keywords:** Computer Vision, HSV, Color Histogram, Histogram Normalization, Bhattacharyya Distance, Illumination, OpenCV

## Table of Contents
1. Introduction  
2. Related Work / Background  
3. Proposed Methodology  
4. Implementation  
5. Results and Discussion  
6. Conclusion and Future Work  
7. References  
8. Appendix

## 1. Introduction
### 1.1 Background
Color is a useful low-cost visual feature for image analysis. A color histogram summarizes the distribution of color values without requiring pixel-by-pixel alignment. This makes histogram comparison useful for simple image retrieval and color-category recognition.

### 1.2 Problem Definition
The color values recorded by a camera can change with illumination, exposure, white balance, and background content. The project investigates whether normalized HSV histograms can provide useful color-category matching when brightness changes.

### 1.3 Objectives
- Implement normalized Hue–Saturation histogram extraction.
- Compare query and reference histograms using Bhattacharyya distance.
- Display ranked categories and histogram visualizations.
- Compare output under dim, normal, and bright conditions.
- Document limitations and propose improvements.

## 2. Related Work / Background
Explain HSV color representation, histogram features, histogram normalization, and distribution-distance measures. Add verified sources in IEEE style. Do not cite sources you have not read.

## 3. Proposed Methodology
### 3.1 System Workflow
Image input → HSV conversion → H–S histogram extraction → L1 normalization → Bhattacharyya comparison → category ranking → result display → lighting experiment.

### 3.2 Histogram Normalization
If `h(i,j)` is the count in bin `(i,j)`, the normalized bin is:
`H(i,j) = h(i,j) / sum(h(i,j))`.

### 3.3 Matching
The implementation uses OpenCV's Bhattacharyya histogram comparison. A smaller distance indicates a closer match. The UI score is `100 × (1 − distance)` clipped to 0–100 and is not a calibrated probability.

### 3.4 Tools
Python, OpenCV, NumPy, Matplotlib, Streamlit, and pandas.

## 4. Implementation
Describe the modules and functions in `src/color_histogram.py`, the Streamlit interface in `app.py`, and the optional webcam demo in `webcam_demo.py`. Insert a flowchart and screenshots from your own execution.

## 5. Results and Discussion
### 5.1 Test Setup
[Describe device, camera, sample count, categories, lighting, and reference/test split.]

### 5.2 Results Table
| Lighting condition | Number tested | Correct | Accuracy |
|---|---:|---:|---:|
| Dim | [ ] | [ ] | [ ] |
| Normal | [ ] | [ ] | [ ] |
| Bright | [ ] | [ ] | [ ] |

### 5.3 Discussion
[Discuss measured results, error cases, background effects, and why some categories were confused.]

### 5.4 Limitations
Color histogram matching does not encode spatial layout and does not fully compensate for illumination, white balance, or exposure changes. The starter synthetic references are not sufficient for claiming real-world accuracy.

## 6. Conclusion and Future Work
Summarize what was implemented and the actual measured findings. Future work may include multiple references per category, object segmentation, white-balance correction, color calibration, and shape/texture features.

## 7. References
Use IEEE style. Include only sources you have actually consulted, for example official documentation for OpenCV histogram functions and HSV conversion. Verify the title, URL, and access date before submission.

## 8. Appendix
Add selected code snippets, instructions for running the application, and any additional screenshots.
