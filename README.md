# 🐧 CIE-Based Identification of Emperor Penguin Colonies from Sentinel-2 Imagery

**Distinguishing Emperor Penguin Colonies from Space: A Novel Method Using the CIE 1931 Chromaticity Diagram**

A novel method using the Commission Internationale de l’Éclairage (CIE) chromaticity diagram to identify emperor penguin colonies in Antarctica from space. This approach provides a convenient, accurate, and innovative method to distinguish emperor penguin guano at a large scale.


📄 The associated manuscript describing this method is currently under review.  
Citation details will be added here upon publication.

---

## 📡 Data Source

The input images are **cropped Sentinel-2 Level-2A surface reflectance products**, which contain the following spectral bands:

- `B1`, `B2`, `B3`, `B4`, `B8`, and `B12`

A sample image is provided in the `data_image/` folder, corresponding to a real-world emperor penguin colony.

> **Note**: If you wish to apply the method to your own Sentinel-2 image, ensure that these six bands are included and properly described in the image metadata.

---

## 🧠 Method Overview

This method involves the following key steps:

1. **Preprocessing**
   - Removal of overbright pixels
   - Removal of exposed rock pixels using the **Exposed Rock Index (ERI)**
   - Removal of shadowed pixels

2. **CIE 1931 Transformation**
   - Selected band combinations (e.g., B4-B3-B2 or B8-B4-B2) are mapped from RGB to CIE XYZ space
   - Chromaticity coordinates (x, y) are derived according to the **CIE 1931 chromaticity diagram **

3. **Classification via Decision Boundary**
   - Empirical decision boundaries in CIE space are applied to isolate guano-affected pixels
   - Boundary parameters are derived from visual analysis of chromaticity distributions

4. **Visualization and Output**
   - The original RGB composite and binary classification mask are visualized side-by-side
   - A binary GeoTIFF result is exported to the `output/` directory

---

## 💻 Requirements

- Python ≥ 3.9
- `numpy`
- `matplotlib`
- `rasterio`

These can be installed via your preferred package manager (e.g., `pip`, `conda`).

---

## 🚀 Usage Instructions

1. Place a `.tif` image (with the required six bands) in the `data_image/` directory.
2. Run one of the classification scripts:

```bash
python run_rgb.py      # Uses B4-B3-B2 (true-color composite)
python run_nirrb.py    # Uses B8-B4-B2 (pseudo-color composite)


