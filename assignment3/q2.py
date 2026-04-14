import numpy as np
from PIL import Image


def get_radial_distances(shape: tuple[int, ...]) -> np.ndarray:
    """
    Generates a 2D spatial map of Euclidean distances from the image center.
    """
    height = shape[0]
    width = shape[1]
    center_y = height / 2
    center_x = width / 2
    cols = np.arange(width)
    rows = np.arange(height)
    x, y = np.meshgrid(cols, rows)
    dist = np.sqrt(np.square(x - center_x) + np.square(y - center_y))
    return dist


def create_feathered_mask(
    dist: np.ndarray, inner_radius: int, outer_radius: int
) -> np.ndarray:
    """
    Generates a normalized radial alpha mask using linear interpolation.
    """
    normalized_dist = (dist - inner_radius) / (outer_radius - inner_radius)
    alpha = 1 - normalized_dist
    alpha = np.clip(alpha, 0.0, 1.0)
    return alpha


def apply_alpha_mask(image: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """
    Applies a 2D transparency mask to an image array by adding or replacing
    the alpha channel.
    """
    if image.shape[2] == 3:
        alpha = np.zeros(image.shape[:2])
        aug_image = np.dstack([image, alpha])
    else:
        aug_image = image.copy()

    scaled_mask = mask * 255
    aug_image[..., -1] = scaled_mask
    cast_image = aug_image.astype(np.uint8)

    return cast_image


def apply_vignette(
    image_path: str, out_path: str,
    inner_ratio: float = 0.7, outer_ratio: float = 0.95
) -> None:
    # Load the input image file
    try:
        print("Input path:  ", image_path)
        input_image = Image.open(image_path)
    except FileNotFoundError as e:
        print(e)
        return None  # Skip image processing

    # Convert to RGBA if it already has transparency/alpha info
    if input_image.mode in ("RGBA", "LA", "P"):
        input_image = input_image.convert("RGBA")  # 4 channels
    else:
        input_image = input_image.convert("RGB")  # 3 channels

    # Convert the input image to a NumPy array
    image = np.array(input_image, dtype=np.float32)
    print("Input shape: ", image.shape)

    # Find the maximum radius, which is half of min(height, width)
    max_radius = min(image.shape[:2]) / 2
    inner_radius = max_radius * inner_ratio
    outer_radius = max_radius * outer_ratio

    # Apply the mask to the image array
    distances = get_radial_distances(image.shape)
    mask = create_feathered_mask(distances, inner_radius, outer_radius)
    masked_image = apply_alpha_mask(image, mask)

    # Save the output array as a PNG file
    Image.fromarray(masked_image).save(out_path, "PNG")
    print("Output shape:", masked_image.shape)
    print("Output path: ", out_path)


# Sample client
if __name__ == "__main__":
    apply_vignette("cat1.jpg", "cat1_cropped.png")
    apply_vignette("cat2.jpg", "cat2_cropped.png")
    apply_vignette("cat3.png", "cat3_cropped.png")
    apply_vignette("cat4.png", "cat4_cropped.png")
    apply_vignette("heart1.jpg", "heart1_cropped.png")
    apply_vignette("heart2.jpg", "heart2_cropped.png")
