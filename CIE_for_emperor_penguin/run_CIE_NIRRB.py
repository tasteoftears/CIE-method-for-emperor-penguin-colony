# Description: Detect emperor penguin colony in remote sensing imagery using B8-B3-B2 bands and chromaticity transformation

import numpy as np
import rasterio
import matplotlib.pyplot as plt
import os

# --------------------------- Configuration ---------------------------
# Please change your input file here
input_filename = 'Astrid20201018.tif'  # Input filename in data_image/)
input_path = os.path.join('data_image', input_filename)
base_name = os.path.splitext(input_filename)[0]
output_path = os.path.join('output', f'{base_name}_NIRRB_output.tif')

# --------------------------- Band Loading ---------------------------

# NOTE:
# The provided test image only contains the following bands:
# 'B1', 'B2', 'B3', 'B4', 'B8', 'B12'.
# Please ensure that any input image includes these specific bands for proper execution.
required_bands = ['B1', 'B2', 'B3', 'B4', 'B8', 'B12']
with rasterio.open(input_path) as src:
    band_names = src.descriptions
    bands = [src.read(band_names.index(band) + 1) for band in required_bands]
    transform, crs = src.transform, src.crs

image = np.stack(bands, axis=-1)

# Save a copy of the original RGB
original_rgb = image[:, :, [3, 2, 1]].copy()  # B4-B3-B2

# --------------------------- Preprocessing ---------------------------
# Remove overbright pixels
B4, B3, B2 = image[:, :, 3], image[:, :, 2], image[:, :, 1]
image[B4 > 1] = 0

# Remove rock pixels using Exposed Rock Index (ERI)
B8, B12 = image[:, :, 4], image[:, :, 5]
denominator = B8 + B12
denominator[denominator == 0] = np.nan
ERI = (B8 - B12) / denominator
image[(ERI >= -0.196) & (ERI <= 0.679)] = 0

# Remove shadowed pixels
image[B2 < 0.25] = 0

# --------------------------- CIE Chromaticity Transformation ---------------------------
rgb = image[:, :, [4, 3, 1]]  # B8-B4-B2 for RGB composite

def rgb_to_xyz(pixel):
    r, g, b = pixel
    x = 2.7689 * r + 1.7517 * g + 1.1302 * b
    y = 1.0000 * r + 4.5907 * g + 0.0601 * b
    z = 0.0000 * r + 0.0565 * g + 5.5943 * b
    return np.array([x, y, z])

xyz = np.apply_along_axis(rgb_to_xyz, 2, rgb)
xyz_sum = xyz.sum(axis=-1) + 1e-6
x = xyz[..., 0] / xyz_sum
y = xyz[..., 1] / xyz_sum

# Apply decision boundary in CIE space
def left_boundary(x_val):
    return -0.2622 * x_val + 0.4321

mask = (y > left_boundary(x)).astype(np.uint8)

# --------------------------- Visualization ---------------------------


# Normalize original RGB to [0,1]
rgb_vis = original_rgb.astype(float)
rgb_vis = rgb_vis / np.percentile(rgb_vis, 98)
rgb_vis = np.clip(rgb_vis, 0, 1)

plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.imshow(rgb_vis)
plt.title('Original image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(mask, cmap='gray')
plt.title('emperor penguin colony')
plt.axis('off')

plt.tight_layout()
plt.show()


# --------------------------- Save Result as GeoTIFF ---------------------------
os.makedirs('output', exist_ok=True)
with rasterio.open(output_path, 'w', driver='GTiff', height=mask.shape[0], width=mask.shape[1],
                   count=1, dtype='uint8', crs=crs, transform=transform) as dst:
    dst.write((mask * 255).astype(np.uint8), 1)

print(f'[NIR-R-B] Output saved: {output_path}')
