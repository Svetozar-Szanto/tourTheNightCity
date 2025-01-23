from PIL import Image, ExifTags
import os
import pillow_avif

def correct_orientation(jpgImage):
    try:
        # Check for EXIF data
        exif = jpgImage._getexif()
        if exif is not None:
            # Look for orientation tag (key 274 is the EXIF orientation tag)
            for tag, value in exif.items():
                if tag == 274:  # Orientation tag
                    if value == 3:
                        jpgImage = jpgImage.rotate(180, expand=True)
                    elif value == 6:
                        jpgImage = jpgImage.rotate(270, expand=True)
                    elif value == 8:
                        jpgImage = jpgImage.rotate(90, expand=True)
                    break
    except (AttributeError, KeyError, IndexError):
        # In case no EXIF data exists or it's in an unexpected format, do nothing
        pass
    return jpgImage

def resize(jpgImage):
    PCResize = 256
    phoneResize = 512
    fullHDResize = 1920

    # Correct the image orientation first
    jpgImage = correct_orientation(jpgImage)

    # Resize for PC thumbnail
    width, height = jpgImage.size
    if width < height:
        ratio = width / height
        PCWidth = int(ratio * PCResize)
        PCHeight = PCResize
    else:
        ratio = height / width
        PCHeight = int(ratio * PCResize)
        PCWidth = PCResize
    PCResizedJPGImage = jpgImage.resize((PCWidth, PCHeight))

    # Resize for mobile phone thumbnail
    width, height = jpgImage.size
    if width < height:
        ratio = width / height
        phoneWidth = int(ratio * phoneResize)
        phoneHeight = phoneResize
    else:
        ratio = height / width
        phoneHeight = int(ratio * phoneResize)
        phoneWidth = phoneResize
    phoneResizedJPGImage = jpgImage.resize((phoneWidth, phoneHeight))

    # Resize for full HD
    width, height = jpgImage.size
    if width < height:
        ratio = width / height
        fullHDWidth = int(ratio * fullHDResize)
        fullHDHeight = fullHDResize
    else:
        ratio = height / width
        fullHDHeight = int(ratio * fullHDResize)
        fullHDWidth = fullHDResize
    fullHDResizedJPGImage = jpgImage.resize((fullHDWidth, fullHDHeight))

    return PCResizedJPGImage, phoneResizedJPGImage, fullHDResizedJPGImage


files = os.listdir("img\\galleryImages\\")
for file in files:
    if file.split(".")[-1].lower() == "jpg":
        jpgImage = Image.open("img\\galleryImages\\" + file)
        PCResizedJPGImage, phoneResizedJPGImage, fullHDResizedJPGImage = resize(jpgImage)

        PCResizedJPGImage.save(f"img\\resized\\256_{file}")
        PCResizedJPGImage.save(f"img\\resized\\256_{file.split('.')[0]}.avif", format = "AVIF")

        phoneResizedJPGImage.save(f"img\\resized\\521_{file}")
        phoneResizedJPGImage.save(f"img\\resized\\521_{file.split('.')[0]}.avif", format = "AVIF")

        fullHDResizedJPGImage.save(f"img\\resized\\1920_{file}")
