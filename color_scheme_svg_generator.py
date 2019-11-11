#!/usr/bin/python3

# This is a simple tool to generate all the unique cube color schemes based on the
# standard stickerless colors (white, red, green, orange, blue, yellow)

import os
from lxml import etree

# all the unique color schemes for the cube
UNIQUE_COLOR_SCHEME = [
    (1, "WYGBOR", "standard"),
    (2, "WYGBRO", ""),
    (3, "WYGOBR", ""),
    (4, "WYGORB", ""),
    (5, "WYGRBO", ""),
    (6, "WYGROB", ""),
    (7, "WGYBOR", ""),
    (8, "WGYBRO", ""),
    (9, "WGYOBR", ""),
    (10, "WGYORB", ""),
    (11, "WGYRBO", ""),
    (12, "WGYROB", ""),
    (13, "WBYGOR", ""),
    (14, "WBYGRO", "Japanese"),
    (15, "WBYOGR", ""),
    (16, "WBYORG", ""),
    (17, "WBYRGO", ""),
    (18, "WBYROG", ""),
    (19, "WOYGBR", ""),
    (20, "WOYGRB", ""),
    (21, "WOYBGR", ""),
    (22, "WOYBRG", ""),
    (23, "WOYRGB", ""),
    (24, "WOYRBG", ""),
    (25, "WRYGBO", ""),
    (26, "WRYGOB", ""),
    (27, "WRYBGO", ""),
    (28, "WRYBOG", ""),
    (29, "WRYOGB", ""),
    (30, "WRYOBG", ""),
]

# basic colours in the order: up, down, front, back, left, right
BASIC_COLORS = "WYGBOR"

# colors of the pieces
STICKERLESS_COLORS = {
    "W": "white",
    "R": "red",
    "G": "green",
    "O": "orange",
    "B": "blue",
    "Y": "yellow",
}


def generate_basic_unique_color_schemes_WYGBOR():
    """Generate the unique color schemes for the cube
    Returns: 
       A list of strings which represents the colors
       The result of this function was used to generate UNIQUE_COLOR_SCHEME constant
    """
    up_c, remaining_5_cols = BASIC_COLORS[0], BASIC_COLORS[1:]

    all_unique_colors_schemes = []
    for down_c in remaining_5_cols:
        front_c, * \
            remaining_face_cols = [
                m for m in remaining_5_cols if m != down_c]
        for back_c in remaining_face_cols:
            left_c, right_c = [
                m for m in remaining_face_cols if m != back_c]
            all_unique_colors_schemes.append(
                f"{up_c}{down_c}{front_c}{back_c}{left_c}{right_c}")
            all_unique_colors_schemes.append(
                f"{up_c}{down_c}{front_c}{back_c}{right_c}{left_c}")

    return all_unique_colors_schemes


def make_all_colors_schemes_svg(colors_schemes, svg_template_fn, output_svg_fn_prefix, out_mode):
    """ Generate images with the cube color schemes
        The output directory is automatically generated

    Arguments:
        colors_schemes {list(k,string,string)} -- color schemes
        svg_template_fn {string} -- svg template filename
        output_svg_fn_prefix {string} -- prefix of the output svg file names
        out_mode (string or None) -- the mode of image generation (None for default or "summary")
    """

    os.makedirs(os.path.dirname(output_svg_fn_prefix), exist_ok=True)
    svg_template_text = open(svg_template_fn, "r").read()

    if out_mode == "summary":
        colors_schemes = colors_schemes[::2]

    for k, current_scheme, scheme_description in colors_schemes:
        svg_tree = etree.fromstring(svg_template_text)
        col_scheme = [STICKERLESS_COLORS[m] for m in current_scheme]

        (col_up, col_down, col_front, col_back, col_left, col_right) = col_scheme
        (c_up, c_down, c_front, c_back, c_left, c_right) = current_scheme

        # replace the stylesheet with the generated one
        style_css = f"""
        .col_up {{ fill:{col_up} }}
        .col_down {{ fill:{col_down} }}
        .col_front {{ fill:{col_front} }}
        .col_back {{ fill:{col_back} }}
        .col_left {{ fill:{col_left} }}
        .col_right {{ fill: {col_right} }}
        """

        svg_style_element = svg_tree.find(".//style")
        if svg_style_element is None:
            raise ValueError(
                f"no <style> is present into the svg template '{svg_template_fn}'")

        svg_style_element.text = style_css

        # add the label
        svg_label_element = svg_tree.find(".//text[@id = 'label']")
        if svg_label_element is not None:
            scheme_label = f"{c_up}{c_down}{c_front}{c_back}{c_left}{c_right}"
            if scheme_description:
                scheme_description = f" ({scheme_description})"
            svg_label_element.text = f"({k:02}) {scheme_label}{scheme_description}"

        # save the result
        svg = etree.tostring(svg_tree, pretty_print=True, encoding="unicode")

        out_svg_filename = f"{output_svg_fn_prefix}_{k:02}_{current_scheme}.svg"
        with open(out_svg_filename, "w") as f:
            f.write(svg)


if __name__ == "__main__":
    TEMPLATES_WITH_OUTPUT = [
        # The templates as tuples of (input svg_template, output_directory_name, output_prefix, mode)
        ("template_simplified.svg", "color_scheme_simplified", "simplified", None),
        ("template_detailed.svg", "color_scheme_detailed", "detailed", None),
        ("template_checkerboard.svg",
         "color_scheme_checkerboard", "checkerboard", None),
        ("template_flat.svg", "color_scheme_flat", "flat", None),
        ("template_checkerboard_summary.svg",
         "color_scheme_checkerboard_summary", "checkerboard_summary", "summary"),
    ]
    # Make the images
    for input_svg_template, out_dir_name, out_prefix, out_mode in TEMPLATES_WITH_OUTPUT:
        print(
            f'Generating {len(UNIQUE_COLOR_SCHEME)} images for "{out_dir_name}".')
        svg_template_fn = os.path.join(os.path.dirname(
            __file__), "templates", input_svg_template)
        make_all_colors_schemes_svg(
            UNIQUE_COLOR_SCHEME, svg_template_fn, os.path.join("output", out_dir_name, out_prefix), out_mode)

    # The output can be assemblend into a single image with the command:
    #  montage *.svg -geometry +30+30 -background black -tile 6x all_schemes.png
