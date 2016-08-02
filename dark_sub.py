import os
import tifffile as tif

def dark_sub(dark_img_f, data_dir=os.getcwd()):
    un_sub_list = [f for f in os.listdir() if not f.startswith('sub')
                   and f.endswith('.tif')]
    if dark_img_f in un_sub_list:
        un_sub_list -= dark_img_f
    dark_img = tif.imread(dark_img_f)
    for el in un_sub_list:
        sub_name = 'sub_'+el
        sub_img = tif.imread(el) - dark_img
        tif.imsave(sub_name, sub_img)
