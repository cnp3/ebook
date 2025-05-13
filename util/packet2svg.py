#!/usr/bin/python3

"""
This module converts packet descriptions in SVG format by outputing a simplified SVG file that can be processed by inkscape
"""

from xml.etree.ElementTree import Element, SubElement, ElementTree
import sys
import os

def ascii_to_svg(input_file, output_file, font_size=14, font_family="DejaVu Sans Mono", line_spacing=1.2):
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        ascii_lines = [line.rstrip('\n') for line in f]

    # Create SVG root
    svg = Element('svg', {
        'xmlns': 'http://www.w3.org/2000/svg',
        'version': '1.1',
    })

    line_height = int(font_size * line_spacing)
    y = font_size  # Initial vertical position

    for line in ascii_lines:
        text = SubElement(svg, 'text', {
            'x': '0',
            'y': str(y),
            'font-family': font_family,
            'font-size': f'{font_size}px',
            'xml:space': 'preserve'
        })
        text.text = line
        y += line_height

    max_width = max(len(line) for line in ascii_lines) * (font_size * 0.6)  # estimate width
    height = len(ascii_lines) * line_height

    svg.set('width', str(int(max_width)))
    svg.set('height', str(height))

    ElementTree(svg).write(output_file, encoding='utf-8', xml_declaration=True)
    print(f"✅ SVG saved as: {output_file}")


if __name__ == "__main__":
    # Set default file paths

    for fileName in (sys.argv[1:]) :
        input_file = fileName
        output_file = fileName.replace('.pkt','.svg')
        ascii_to_svg(input_file, output_file)


