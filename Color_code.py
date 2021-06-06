# python
# coding: utf-8

import time  # Calculate execution time

from lark import Lark, Transformer  # Lark parser simple and efficient
from enum import Enum  # enum is used to specify the code value to the respective color name

start_time = time.time()    # start the time for the calculation of the execution time

color_parser = Lark(r"""                    // parsing syntax condition grammers
    ?color : achromatic | chromatic         // check color whether it is chromatic or achromatic
    achromatic : [lightness] "gray" | monochrome             // if achromatic then check whether it is gray or monochromatic with lightness checking
    chromatic : lightness saturation hue | [lightness] [saturation] hue    // if chromatic then check for how light it is then saturation and then hue
    hue : generic_hue | halfway_hue | quarterway_hue                       // hue have three things generic, halfway and quaterway
    halfway_hue : generic_hue " " generic_hue        // halfway hue check whether the color name have two same word seperated by '-'. e.g, red-red, blue-blue.
    quarterway_hue : ish_form generic_hue            // quarterway is the checking of ish_form in the name of the color, e.g, reddish, yellowish

    monochrome : MONOCHROME                          // checking of black or white color
    MONOCHROME : "black" | "white"

    lightness : LIGHTNESS                            // lightness is like brighness checking
    LIGHTNESS : "extreme dark" | "very dark" | "dark" | "medium" | "light" | "very light" | "extreme light"
    saturation : SATURATION                          // Saturation check the clarity of color
    SATURATION : "grayish" | "bit" | "moderate" | "strong" | "vivid"

    generic_hue : GENERIC_HUE                        // check general color name
    GENERIC_HUE : "red" | "orange" | "brown" | "yellow" | "green" | "blue" | "purple"

    ish_form : ISH_FORM                              // check ish form of the color
    ISH_FORM : "reddish" | "orangish" | "brownish" | "yellowish" | "greenish" | "bluish" | "purplish"
    %import common.WS
    %ignore WS
    """, start='color')


# Giving values to fundamental colors
# for creating the color-code of given color

class Mono(Enum):  # Given code value to Mono part
    black = [0, 0, 0]
    white = [255, 255, 255]
    gray = [128, 128, 128]


class Lightness(Enum):  # Given code value to lightness part
    exdark = 10
    vdark = 25
    dark = 37.5
    medium = 50
    light = 62.5
    vlight = 75
    exlight = 90


class Saturation(Enum):  # Given code value to saturation part
    grayish = 0
    bit = 25
    moderate = 50
    strong = 75
    vivid = 100


class Ghue(Enum):  # Given code value to general hue part
    red = [255, 0, 0]
    orange = [255, 128, 0]
    yellow = [255, 255, 0]
    green = [0, 255, 0]
    blue = [0, 0, 255]
    purple = [128, 0, 128]


class Hhue(Enum):  # Given code value to halfway hue part
    red_orange = [255, 64, 0]
    orange_yellow = [255, 192, 0]
    yellow_green = [128, 255, 0]
    green_blue = [0, 128, 128]
    blue_purple = [64, 0, 192]
    purple_red = [192, 0, 64]


class Qhue(Enum):  # Given code value to quarterway hue part
    orangish_red = [223, 32, 0]
    reddish_orange = [255, 96, 0]
    yellowish_orange = [255, 160, 0]
    orangish_yellow = [255, 224, 0]
    greenish_yellow = [192, 255, 0]
    yellowish_green = [64, 255, 0]
    bluish_green = [0, 192, 64]
    greenish_blue = [0, 64, 192]
    purplish_blue = [32, 0, 224]
    bluish_purple = [96, 0, 160]
    reddish_purple = [160, 0, 96]
    purplish_red = [224, 0, 32]


class IshForm(Enum):  # Given code value to isf_form part
    reddish = [255, 0, 0]
    orangish = [255, 128, 0]
    yellowish = [255, 255, 0]
    greenish = [0, 255, 0]
    bluish = [0, 0, 255]
    purplish = [128, 0, 128]


class ColorTransformer(Transformer):  # transform color name and generate color code
    MONOCHROME = lambda self, s: Mono[s]
    SATURATION = lambda self, s: Saturation[s]
    GENERIC_HUE = lambda self, s: Ghue[s]
    ISH_FORM = lambda self, s: IshForm[s]

    def LIGHTNESS(self, s):  # ligthness function that generates color code, this return lightness value of color
        return Lightness[s.replace("very ", "v").replace("extreme ", "ex")]

    monochrome = lambda self, s: s
    lightness = lambda self, s: s
    saturation = lambda self, s: s
    generic_hue = lambda self, s: s
    ish_form = lambda self, s: s

    def hue(self, s):  # hue function for the generation color code
        (s,) = s
        return s

    def halfway_hue(self, s):  # halfway function for the generation of color code e.g., red-red
        x, y = s
        try:
            name = x[0].name + "_" + y[0].name
            return [Hhue[name]]
        except KeyError:
            print("Wrong halfway_hue", x[0].name + "_" + y[0].name)
            return None

    def quarterway_hue(self, s):  # quaterway function, ish_form of color, for the generation of color code
        x, y = s
        try:
            name = x[0].name + "_" + y[0].name
            return [Qhue[name]]
        except KeyError:
            print("Wrong quarterway_hue", x[0].name + "_" + y[0].name)
            return None

    def achromatic(self, s):  # achromatic function to generate color code
        if len(s) == 0:
            return [Lightness["medium"], Mono["gray"]]#[Lightness["medium"], Mono["gray"]]
        else:
            (s,) = s
            if isinstance(s[0], Lightness):  # check for lightness
                s.append(Mono["gray"])
            return s

    def chromatic(self, s):  # chromatic function generate color code.
        if None in s:
            print("Error")
        elif len(s) == 1:
            return s[0]
        else:
            return [x[0] for x in s]


def hue_call(x):        # calculate hue from R,G,B values
    r,g,b = x
    R = r/255
    G = g/255
    B = b/255
    H = None
    if R == G == B:
        H = 0
    elif R >= G >= B:
        H = 60 * ((G - B) / (R - B))
    elif G > R >= B:
        H = 60 * (2 - (R - B) / (G - B))
    elif G >= B > R:
        H = 60 * (2 + (B - R) / (G - R))
    elif B > G > R:
        H = 60 * (4 - (G - R) / (B - R))
    elif B > R >= G:
        H = 60 * (4 + (R - G) / (B - G))
    elif R >= B > G:
        H = 60 * (6 - (B - G) / (R - G))
    return H


def hsl_to_rgb(H,S,L):          # convert HSL system into RGB system
    C = (1 - abs(2*L - 1)) * S
    X = C * (1 - abs((H / 60) % 2 - 1))
    m = L - C / 2

    def cal(H):
        if 0 <= H < 60:
            return C, X, 0
        elif 60 <= H < 120:
            return X, C, 0
        elif 120 <= H < 180:
            return 0, C, X
        elif 180 <= H < 240:
            return 0, X, C
        elif 240 <= H < 300:
            return X, 0, C
        elif 300 <= H < 360:
            return C, 0, X

    R1,G1,B1 = cal(H)
    R,G,B = (R1 + m) * 255, (G1 + m) * 255,(B1 + m)*255
    return R,G,B


def rgb_to_hex(rgb):            # convert RGB system to HEX system
    a=[]
    for i in rgb:
        hx = hex(round(i)).split('x')[-1]
        if len(hx) == 1:
            a.append('0' + hx)          # used to create six letters in hex code
            continue
        a.append(hx)

    print(rgb, ", hsl=>", [h, s, l], ", hex" , end='=>  ')
    hex_code = ''.join(a)
    return hex_code


# Here the mains begin
import itertools  # used to make multiple variant of color name
import mplcursors  # used to show the hovering with color name and codes
import matplotlib.pyplot as plt  # used to show colors in a graph

# Here making multiple color names using below conditions
t1 = ["extreme dark", "very dark", "dark", "medium", "light", "very light", "extreme light"]  # define a list of ligthness name
t2 = ["grayish", "bit", "moderate", "strong", "vivid"]  # define a list of saturation in the color name
t3 = ["red", "orange", "yellow", "green", "blue", "purple"]  # define a list of general color name
t4 = [' '.join(x) for x in zip(t3, t3[1:])] + ['purple red']  # define a list that join two general color name
t5 = ["reddish", "orangish", "yellowish", "greenish", "bluish", "purplish"]  # define a list of ish form of color
t6 = [' '.join(x) for x in zip(t5, t3[1:])] + [
    'purplish red']  # define a list that join two name, first ish form + second general color name
t7 = [' '.join(x) for x in zip(t5[1:], t3)] + [
    'reddish purple']  # define a list that join two name, first genral color + second ish form

# Here above list is used to join together for the generation of multiple color names
texts = ['white', 'black', 'red', 'orange', 'yellow', 'green', 'blue', 'purple']
texts += ['gray', "extreme dark gray", "very dark gray", "dark gray", "medium gray", "light gray",
          "very light gray", "extreme light gray"]  # define a list for the lightness in color name
texts += [' '.join(x) for x in itertools.product(t1, t2,
                                                 t3)]  # generate multiple color name with lightness + saturation + general color name
texts += [' '.join(x) for x in itertools.product(t1, t2,
                                                 t4)]  # generate multiple color name with lightness + saturation + join two general color name
texts += [' '.join(x) for x in itertools.product(t1, t2,
                                                 t6)]  # genarate multiple color name with lightness + saturation + join two name, first ish form + second general color name
texts += [' '.join(x) for x in itertools.product(t1, t2,
                                                 t7)]  # generate multiple color name with lightness + saturation + join two name, first genral color + second ish form

# choice for entries of the colors
times = 'yes'
tets = []
choices = input("Do wanna enter color names or see all colors. (?custom/all):   ")
if choices in ['all', 'All', 'ALL']:    # Here color codes generated for the above multiple color names
    tets = texts[:]
elif choices in ['custom', 'Custom', 'CUSTOM']:     # enter color names
    while times in ['yes', 'Yes', 'y', 'Y', 'YES']:
        tets.append(input("Enter the color name:  "))
        times = input("Do wanna enter more enter more color names. (?y/n): ")

count = 0       # count number of color code generated
hox = []        # list of all different color code
hox_name = []   # list of all color names
for text in tets:  # loop through all names
    count += 1
    # parse the name to color_parser and get all the condition present in the name then store it into tree variable
    tree = color_parser.parse(text)
    # transform the color condition which present in tree into color code, accordingly.
    obj = ColorTransformer().transform(tree)


    lit = ['exdark', 'vdark', 'dark', 'medium', 'light', 'vlight', 'exlight']   # all lightness levels
    sat = ['grayish', 'bit', 'moderate', 'strong', 'vivid']     # all saturation levels

    lt = len(obj)
    l = 50          # default value of lightness
    s = 100         # default value of saturation
    names = []      # list of
    list_of_name = []
    # here calculate the saturation and lightness according to the entry
    for i in range(lt):
        name = obj[i].name
        names.append(name)

        if 'gray' is name:
            s = 0

        if name in lit:
            l = obj[i].value
            list_of_name.append(name.replace("v", "very ").replace("ex", "extreme "))

        if name in sat:
            s = obj[i].value
            list_of_name.append(name)

    list_of_name.append(obj[lt - 1].name)
    color_name = ' '.join(list_of_name)     # make list of names

    # calculate the saturation and lightness, whose both levels not mentioned
    if names[0] not in lit:
        r, g, b = obj[lt - 1].value
        val = [r / 255, g / 255, b / 255]
        l = round((1 / 2) * (max(val) + min(val)), 4) * 100

        lh = l / 100
        if len(names) > 1 and names[1] not in sat:
            if 0 < lh < 1:
                s = round((max(val) - min(val)) / (1 - abs(2 * lh - 1)), 4) * 100
            elif lh == 1:
                s = 0

    # saturation(s) and lightness(l) values passes to the hue_call for hue(h) calculation
    h = round(hue_call(obj[lt - 1].value), 4)
    print(color_name + ", rgb=>", end=' ')
    # hue(h), saturation(s) and lightness(l) values passes to the hsl to rgb conversion
    rgb = [round(x) for x in hsl_to_rgb(h, s/100, l/100)]
    # RGB values passes to the rgb to hex conversion
    Hex_code = "#" + rgb_to_hex(rgb)
    print(Hex_code)
    # store all different hex codes with there respective names
    if Hex_code not in hox:
        hox.append(Hex_code)        # store color codes
        hox_name.append(color_name) # store color names

# calculate the coordinates for the grapgh
def calc_axis(low=1,high=30):
    number = 0
    coordinates = []
    while number < len(hox):
        for j in range(low,high):
            if number < len(hox):
                coordinates.append(j)
                number = number + 1
            else: break
    return coordinates

fig, ax = plt.subplots()
# scatter graph for the color to display
ax.scatter(calc_axis(), calc_axis(5,30), c=hox, s=100)
ax.set_title("Mouse over color point")
# hover and display the colors with their name and code
mplcursors.cursor(ax, hover=True).connect("add", lambda sel: sel.annotation.set_text(hox_name[sel.target.index]+" ("+hox[sel.target.index]+") "))
start_time1 = time.time()
plt.show()
# print total number of colors and execution time
print("  Total number of different color codes generated: ", len(hox))
print("  Total number of all color codes generated: ", count)
print(" Total time before graph display: ", round(time.time() - start_time1, 4), " seconds")
print(" Execution time: ", round(time.time() - start_time, 4), " seconds")
