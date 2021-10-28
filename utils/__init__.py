from datetime import datetime
from io import BytesIO
import asyncio

def time():
    """Returns a formatted timestamp suitable for use in log functions"""
    return datetime.now().strftime("%m/%d %H:%M:%S ")

@asyncio.coroutine
async def PillowImageToBytesIO(self, image):
    """Converts a Pillow Image object into a ByteIO object in PNG format.
This operation is required for sending images to Discord's API"""
    image_binary = BytesIO()
    image.save(image_binary, "PNG")
    image_binary.seek(0)
    return image_binary
