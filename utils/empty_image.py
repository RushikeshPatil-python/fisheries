# utils/empty_image.py
from PIL import Image
import io

def create_empty_image_stream():
    """
    Returns a NEW BytesIO stream containing a valid 1x1 PNG image.
    """
    img = Image.new("RGBA", (1, 1), (255, 255, 255, 0))
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer
