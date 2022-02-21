import numpy as np
from .utils import get_concentration, od_to_rgb


def stain_mixup(
    image: np.ndarray,
    source_stain_matrix: np.ndarray,
    target_stain_matrix: np.ndarray,
    intensity_range: list = [0.95, 1.05],
    alpha: float = 0.6
) -> np.ndarray:
    """Stain Mix-Up

    Args:
        image: Image array in RGB (H, W, 3)
        source_stain_matrix: Stain matrix of source domain (N, 3)
        target_stain_matrix: Stain matrix of target domain (N, 3)
        intensity_range: The lower bound and upper bound of concentration flucutation
        alpha: The weight of soruce_stain_matrix

    Return:
        Augmented image (H, W, 3)
    """
    n_stains, *_ = source_stain_matrix.shape
    # Intensity pertubation
    random_intensity = np.random.uniform(size=(1, 1, n_stains), *intensity_range)  # (1, 1, n_stains)
    src_concentration = get_concentration(
        image,
        source_stain_matrix,
    )  # (H, W, n_stains)
    augmented_concentration = src_concentration * random_intensity

    # Stain matrix intepolation
    interpolated_stain_matrix = source_stain_matrix * alpha + target_stain_matrix * (1. - alpha)
    interpolated_stain_matrix /= np.linalg.norm(
        interpolated_stain_matrix,
        axis=-1,
        keepdims=True,
    )  # (n_stains, 3)

    # Composite
    augmented_image = od_to_rgb(augmented_concentration @ interpolated_stain_matrix)
    return augmented_image
