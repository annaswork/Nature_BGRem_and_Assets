import cv2
from environment.config import IMAGE_URL_PREFIX, STATIC_URL_PREFIX

def save_img_with_url(
    output_file,
    output_filename,
    output_filepath
):

    save_success = cv2.imwrite(
        output_filepath,
        output_file
    )

    if not save_success:
        raise ValueError(f"Failed to save image on {output_filepath}")

    print(f"File saved at path: {output_filepath}")

    image_url = f"{IMAGE_URL_PREFIX}/{output_filename}"

    return image_url