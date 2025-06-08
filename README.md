# 🐧 CIE-Based Extraction of Emperor Penguin Colonies from Sentinel-2 Imagery

**Distinguishing Emperor Penguin Colonies from Space: A Novel Method Using the CIE 1931 Chromaticity Diagram**

This repository presents a novel image classification method for extracting emperor penguin colonies in Antarctica from satellite imagery. The approach leverages the **CIE 1931 chromaticity diagram** to identify guano stains (feces) as ecological proxies of colony activity. It is based on a physical transformation of reflectance data rather than conventional spectral indices.

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
   - Removal of exposed rock surfaces using the **Exposed Rock Index (ERI)**
   - Filtering of low-reflectance shadow regions

2. **Color Space Transformation**
   - Selected band combinations (e.g., B4-B3-B2 or B8-B4-B2) are mapped from RGB to CIE XYZ space
   - Chromaticity coordinates (x, y) are derived according to the **CIE 1931 color model**

3. **Classification via Chromaticity Boundary**
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

## 📄 The associated manuscript describing this method is currently under revision.
Citation details will be added here upon official publication.
