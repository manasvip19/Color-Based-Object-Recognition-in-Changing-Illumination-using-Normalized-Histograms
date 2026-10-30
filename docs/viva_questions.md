# Viva Voce Questions and Suggested Answers

1. **What is computer vision?**  
   Computer vision is a field that enables computers to extract useful information from images and videos.

2. **What is a color histogram?**  
   It counts how many pixels fall into specified color ranges or bins.

3. **Why use HSV instead of RGB?**  
   HSV separates hue and saturation from value (brightness), which can make color comparisons less sensitive to some brightness changes.

4. **What is histogram normalization?**  
   It rescales histogram values, here so their sum is 1, allowing comparison across images of different sizes.

5. **What is the Hue channel?**  
   Hue represents the basic color family.

6. **What does Saturation represent?**  
   Saturation describes color vividness or purity.

7. **What is the Value channel?**  
   Value represents brightness in HSV.

8. **What is Bhattacharyya distance?**  
   A measure used to compare two distributions. Lower values mean the distributions are more similar.

9. **What does a similarity score of 90 mean in this project?**  
   It means the transformed histogram-distance score is 90/100; it is not a 90% probability of correctness.

10. **Does histogram normalization remove illumination effects completely?**  
    No. It normalizes scale, not all color shifts caused by lighting, exposure, or white balance.

11. **What is the main limitation of a color histogram?**  
    It loses spatial information, so two different objects with similar colors may match.

12. **Why crop the object region?**  
    To reduce background pixels that can distort the histogram.

13. **What is a reference histogram?**  
    A normalized color distribution computed from a labelled example used for comparison.

14. **How do you measure accuracy?**  
    Divide the number of correct predictions by the total labelled test examples and multiply by 100.

15. **What is overfitting in the evaluation context?**  
    Reporting performance on the same samples used to construct the reference data can overestimate generalization.

16. **How can the project be improved?**  
    Use multiple reference images per category, object segmentation, color calibration, a larger test set, and additional features such as shape or texture.

17. **Why is this not a general object detector?**  
    It compares the color distribution of the whole input or crop; it does not locate arbitrary objects in a scene.

18. **What happens with a low-saturation gray object?**  
    Hue is unstable or less informative, so hue-based category matching may be unreliable.

19. **Why include a lighting experiment?**  
    To measure rather than assume how brightness changes affect the predictions.

20. **What should you discuss in the conclusion?**  
    What worked, measured results, failure cases, limitations, and practical improvements.
