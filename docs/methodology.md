# Methodology and Experimental Plan

## Aim
Implement a color-based recognition prototype using normalized HSV histograms and evaluate its behavior under changing illumination.

## Research question
How does brightness variation affect the histogram similarity and predicted color category of a selected image region?

## Hypothesis
Using Hue and Saturation can reduce some effects of brightness changes compared with raw RGB histograms, but performance can still degrade when the image becomes very dark, clipped, desaturated, or mixed with background colors.

## Algorithm
1. Read query image.
2. Convert RGB/BGR image to HSV.
3. Compute a 2D histogram with 30 Hue bins and 32 Saturation bins.
4. Normalize histogram using L1 normalization.
5. Compute the Bhattacharyya distance between the query and each reference histogram.
6. Select the reference with the lowest distance.
7. Transform distance into a display similarity score: `max(0, min(100, (1 - distance) * 100))`.
8. Repeat for different lighting conditions and record results.

## Controlled evaluation
Recommended protocol:
- Select 4 categories: red, green, blue, yellow.
- Capture at least 10 images per category in each of three physical lighting conditions.
- Keep object, background, distance, and camera angle as consistent as possible.
- Label each image with its true category.
- Record predicted category, distance, and whether prediction was correct.
- Calculate accuracy as `(correct predictions / total test images) * 100`.
- Include a confusion matrix if enough samples are collected.

Do not use the same images to build reference histograms and evaluate final accuracy. Keep a separate test set.

## Limitations
- Color histograms discard spatial layout.
- Different objects with similar color distributions can match.
- Background pixels affect the histogram unless the object is cropped or masked.
- Automatic exposure and white balance can affect measured color.
- The software brightness simulation is not a substitute for capturing real lighting conditions.
