import copy
import os
import random
from PIL import Image
from PIL import GifImagePlugin
import numpy
import math

numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
hexdec_char = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
letters = ["a", "b", "c", "d", "e",
           "f", "g", "h", "i", "j",
           "k", "l", "m", "n", "o",
           "p", "q", "r", "s", "t",
           "u", "v", "w", "x", "y",
           "z"]
consonants = letters
punctuation = ['.', '...', '?', '!']
vowels = ["a", "e", "i", "o", "u", "y"]

# Text/Strings

def generate_name(min_syl=2, max_syl=7):
    name = ""
    syllables = random.randint(min_syl, max_syl)
    for syl in range(syllables):
        syl_patterns = [f'{random.choice(letters)}{random.choice(vowels)}', f'{random.choice(vowels)}{random.choice(letters)}']
        name += random.choice(syl_patterns)
    return name.capitalize()


def combine_strs(str1, str2):
    strlen = len(str1)
    if len(str2) < len(str1):
        strlen = len(str2)
    splithere = random.randint(1, strlen - 2)
    return str1[:splithere] + str2[splithere:]


# Numbers/Probability

def sign(num):
    if num > 0:
        return 1
    elif num < 0:
        return -1
    else:
        return 0


def ovl_from_dict(dictionary):
    ovl = []
    for ki in dictionary.keys():
        ovl.append((ki, dictionary[ki]))
    return ovl


def weighted_random(option__value__list):  # (option, value)
    total_chances = 0
    option_value_list = option__value__list
    count = 0
    used_option_values = []
    option_ranges = {}
    while count < len(option_value_list):
        option_value = random.choice(option_value_list)
        while option_value in used_option_values:
            option_value = random.choice(option_value_list)
        used_option_values.append(option_value)

        count += 1
        if option_value[1] <= 0:
            continue
        option_ranges[option_value[0]] = (total_chances + 1, None)
        total_chances += option_value[1]
        option_ranges[option_value[0]] = (option_ranges[option_value[0]][0], total_chances)
    if total_chances <= 1:
        total_chances = 2
    choice_value = random.randint(1, total_chances)
    for option in option_ranges.keys():
        if option_ranges[option][0] <= choice_value <= option_ranges[option][1]:
            return option


def bind_int(val, upr=255, lwr=0):
    if val < lwr:
        return lwr
    elif val > upr:
        return upr
    else:
        return val


def vary(val, var, extra=825, deev_mag=1.05, right_bias=1, left_bias=1, opps_ok=False, summary=False):
    min_bon = round(val*var*-1*left_bias)
    max_bon = round(val*var*right_bias)
    if min_bon < max_bon:
        bonus = random.randint(min_bon, max_bon)
    elif max_bon < min_bon:
        bonus = random.randint(max_bon, min_bon)
    else:
        bonus = max_bon
    if summary:
        print(f'~~~~~\nOriginal: {val}\nVariation: {var} (Initial Range: {round(val*var)})\nInitial Bonus: {bonus}')
    dvcount = 0
    opp_avgs = 0
    while random.randint(1, 1000) <= extra:  # prevents the possible values from being uniform :3
        bonus = bonus*deev_mag
        dvcount += 1
    bonus = round(bonus)
    result = val + bonus
    while not opps_ok and abs(sign(val)-sign(result)) > 1:  # if receiving the opposite result is unacceptable, average between original and result
        opp_avgs += 1
        result = round((val + result) * 0.5)
    if summary:
        print(f'Deev\'d: {dvcount} (Mag.:{deev_mag})\nFinal Bonus: {bonus}\nResult: {result} (Averages: {opp_avgs})')
    return result


# Image/Animation

def img_2_rgba(img):
    """
    Returns from a PIL Image a list of lists (rows) of lists (columns/pixels) of numbers
    cell format: [Red, Green, Blue, Alpha]
    """
    temp_arr = numpy.array(img)
    temp_arr = Image.fromarray(temp_arr, mode='RGBA')
    temp_arr = numpy.array(temp_arr)
    return numpy.array(temp_arr)


def split_sprites(fpa, fpb, saveto, vert=True):
    fp1 = '/home/sludge/pycharm/projects/AmbOfInf/AofI/images/' + fpa
    fp2 = '/home/sludge/pycharm/projects/AmbOfInf/AofI/images/' + fpb
    save_to = '/home/sludge/pycharm/projects/AmbOfInf/AofI/images/' + saveto
    pre_img1 = Image.open(fp1)
    pre_img2 = Image.open(fp2)

    img_gb1 = pre_img1.getbbox()
    img_gb2 = pre_img2.getbbox()
    if vert:
        imgh1 = pre_img1.crop((img_gb1[0], img_gb1[1], round(img_gb1[2] / 2), img_gb1[3]))
        imgh2 = pre_img2.crop((round(img_gb2[2] / 2) + 1, img_gb2[1], img_gb2[2], img_gb2[3]))
    else:
        imgh1 = pre_img1.crop((img_gb1[0], img_gb1[1], img_gb1[2], round(img_gb1[3] / 2)))
        imgh2 = pre_img2.crop((img_gb1[0], round(img_gb2[3] / 2)+1, img_gb2[2], img_gb2[3]))

    imgh2 = imgh2.resize(imgh1.size)

    imgh1_ar = numpy.array(imgh1)
    imgh2_ar = numpy.array(imgh2)

    try:
        if vert:
            img_ar = numpy.append(imgh1_ar, imgh2_ar, 1)
        else:
            img_ar = numpy.append(imgh1_ar, imgh2_ar, 0)
    except ValueError as e:
        print(e)
        img_ar = numpy.append(imgh1_ar, imgh2_ar, 2)

    try:
        post_img = Image.fromarray(img_ar)
    except TypeError:
        if random.randint(0, 1):
            post_img = Image.open(fp1)
        else:
            post_img = Image.open(fp2)

    if saveto:
        pi_fp = save_to
        post_img.save(pi_fp)
        return pi_fp
    else:
        return post_img


def blend_color(front, back):
    colorRGBA2 = front
    colorRGBA1 = back
    alpha = 255 - ((255 - colorRGBA1[3]) * (255 - colorRGBA2[3]) / 255)
    red = (int(colorRGBA1[0]) * (255 - int(colorRGBA2[3])) + int(colorRGBA2[0]) * int(colorRGBA2[3])) / 255
    green = (int(colorRGBA1[1]) * (255 - int(colorRGBA2[3])) + int(colorRGBA2[1]) * int(colorRGBA2[3])) / 255
    blue = (int(colorRGBA1[2]) * (255 - int(colorRGBA2[3])) + int(colorRGBA2[2]) * int(colorRGBA2[3])) / 255
    return [numpy.uint8(red), numpy.uint8(green), numpy.uint8(blue), numpy.uint8(alpha)]


def color_shift(filename, saveto, r_delta=0, g_delta=0, b_delta=0, a_delta=0):
    filepath = '/home/sludge/pycharm/projects/AmbOfInf/AofI/images/' + filename
    save_to = '/home/sludge/pycharm/projects/AmbOfInf/AofI/images/' + saveto
    r_delta = r_delta
    g_delta = g_delta
    b_delta = b_delta
    a_delta = a_delta
    pre_img = Image.open(filepath)
    pre_ar = img_2_rgba(pre_img)
    post_ar = []

    for pre_row in pre_ar:
        post_row = []
        for pre_col in pre_row:
            post_r = numpy.uint8(bind_int(pre_col[0] + r_delta))
            post_g = numpy.uint8(bind_int(pre_col[1] + g_delta))
            post_b = numpy.uint8(bind_int(pre_col[2] + b_delta))
            post_a = numpy.uint8(bind_int(pre_col[3] + a_delta))
            post_col = [post_r, post_g, post_b, post_a]  # MUST ALL BE UINT8
            post_row.append(post_col)
        post_ar.append(post_row)

    post_img = Image.fromarray(numpy.array(post_ar), mode='RGBA')
    if saveto:
        pi_fp = save_to
        post_img.save(pi_fp)
        return pi_fp
    else:
        return post_img


def gif_from_imgs(frame_list: list[Image], gif_name='ani.gif', dur=100):
    frams = []
    for fr in frame_list:
        frams.append(fr)

    fram1 = frams.pop(0)
    fram1.save(gif_name, format='GIF', append_images=frams, save_all=True, duration=dur, loop=1, disposal=2)
    return fram1


def play_gif_over_img(main_img, gif_img, gifname='gif.gif', frame_duration=100):
    new_seq = []
    for frame_no in range(gif_img.n_frames):
        gif_img.seek(frame_no)
        main_copy = copy.copy(main_img)
        main_copy.paste(gif_img)

        new_seq.append(main_copy)
    leading_frame = new_seq.pop(0)
    leading_frame.save(f'AofI/gifs/{gifname}', include_color_table=False, save_all=True, append_images=new_seq, duration=frame_duration, loop=0)

    return leading_frame

