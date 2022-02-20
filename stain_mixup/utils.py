import cv2
import numpy as np

import spams


def get_foreground(image: np.ndarray, luminance_threshold: float = 0.8):
    """Get tissue area (foreground)
    Args:
        image: Image in RGB (H, W, C)
        luminance_threshold: cutoff for L

    Return:
        Tissue foreground mask (H, W)
    """
    image_lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
    L = image_lab[:, :, 0] / 255.
    return L < luminance_threshold


def rgb_to_od(image):
    od = -np.log(np.maximum(image.astype(np.float32), 1.0) / 255. + 1e-8)
    return od


def od_to_rgb(od):
    image = np.minimum(np.exp(-od) * 255, 255).astype(np.uint8)
    return image


def get_stain_matrix(
    image: np.ndarray,
    lambda1: float = 0.1
):
    """
    Stain matrix estimation via method of:
    A. Vahadane et al. 'Structure-Preserving Color Normalization and Sparse Stain Separation for Histological Images'
    Args:
        image: Image in RGB
        lambda1: lambda1 parameter

    Return:
        stain_matrix
    """
    tissue_mask = get_foreground(image).reshape((-1, ))

    # Convert image to OD (and remove background)
    optical_density = rgb_to_od(image).reshape((-1, 3))
    optical_density = optical_density[tissue_mask]

    stain_matrix = spams.trainDL(
        X=optical_density.T,
        K=2,
        lambda1=lambda1,
        mode=2,
        modeD=0,
        posAlpha=True,
        posD=True,
        verbose=False,
        batchsize=1024,
    ).T  # (N, 3)

    # Assure H on first row, E on second row
    if stain_matrix[0, 0] < stain_matrix[1, 0]:
        stain_matrix = stain_matrix[[1, 0], :]

    stain_matrix /= np.linalg.norm(stain_matrix, axis=1)[:, None]
    return stain_matrix


def get_concentration(
    image: np.ndarray,
    stain_matrix: np.ndarray,
    lambda1: float = 0.01,
):
    optical_density = rgb_to_od(image).reshape((-1, 3))
    concentration = spams.lasso(
        X=np.asfortranarray(optical_density.T),
        D=np.asfortranarray(stain_matrix.T),
        mode=2,
        lambda1=lambda1,
        pos=True,
        numThreads=1,
    ).toarray()
    concentration = concentration.T
    concentration = concentration.reshape(*image.shape[:-1], -1)
    return concentration
