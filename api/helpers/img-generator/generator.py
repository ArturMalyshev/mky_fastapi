from PIL import ImageFile, Image
import hashlib
import calendar
import time

ImageFile.LOAD_TRUNCATED_IMAGES = True

item_im = "fon.jpeg"
design_im = "des.png"

#---center settings----
# design_w = 200
# design_h = 200
# design_l = 300
# design_t = 170

#---center big settings----
# design_w = 240
# design_h = 240
# design_l = 280
# design_t = 160


#----left settings-----
# design_w = 150
# design_h = 150
# design_l = 220
# design_t = 190


# ---right settings-----
design_w = 150
design_h = 150
design_l = 420
design_t = 190

def img_name_generator (d_name, item_name):
    return hashlib.sha256((d_name + item_name).encode('utf-8')).hexdigest() + str(calendar.timegm(time.gmtime())) + ".jpg"

def merge_images (item_image, design_image, design_height, design_width, design_left, design_top):
    """
        item_image - path to item image
        design_image - path to design image
        design_height - design height in px
        design_width - design width in px
        design_left - design margin from left in px
        design_top - design margin from top in px
    """

    im = Image.open(item_image)

    design = Image.open(design_image)
    design = design.resize((design_height, design_width))

    im.paste(design, (design_left, design_top), design)

    new_name = img_name_generator(design_image, item_image)

    im.save(new_name)

    return new_name



merge_images(item_im, design_im, design_h, design_w, design_l, design_t)