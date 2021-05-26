#!/usr/bin/python
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT

import math
import argparse
import subprocess

from pysvg.filter import *
from pysvg.gradient import *
from pysvg.linking import *
from pysvg.script import *
from pysvg.shape import *
from pysvg.structure import *
from pysvg.style import *
from pysvg.text import *
from pysvg.builders import *
from pysvg.parser import parse

pt = 25.4/72.
oh = ShapeBuilder()

params = {
    'PAGE_HEIGHT' : 210.,
    'PAGE_WIDTH' : 297.,

    'STROKEWIDTH' : 0.15,
    'MAJOR_TICK_STROKE_LENGTH' : 2,
    'MINOR_TICK_STROKE_LENGTH' : 1,

    'LAT_SCALE' : 1.4, # in mm per minutes
    'FONT_SIZE' : 6 # in pt

}



text_style_middle_anchor = StyleBuilder()
text_style_middle_anchor.setFontFamily(fontfamily="Arial")
text_style_middle_anchor.setFontSize(6*pt)
text_style_middle_anchor.style_dict["alignment-baseline"] = "middle"
text_style_middle_anchor.style_dict["dominant-baseline"]="middle"
text_style_middle_anchor.setTextAnchor("middle")
text_style_middle_anchor.setFilling("black")

text_style_start_anchor = StyleBuilder()
text_style_start_anchor.setFontFamily(fontfamily="Arial")
text_style_start_anchor.setFontSize(6*pt)
text_style_start_anchor.style_dict["alignment-baseline"] = "middle"
text_style_start_anchor.style_dict["dominant-baseline"]="middle"
text_style_start_anchor.setTextAnchor("start")
text_style_start_anchor.setFilling("black")



def draw_polar_ticks(svg, radius, spacing_degree = 10, strokelength=2, strokewidth=0.15):

    for theta in range(0, 360, spacing_degree):
        line = oh.createLine(0, radius, 0, radius-strokelength, strokewidth=strokewidth, stroke='black')

        t = TransformBuilder()
        t.setRotation("%d" % theta)
        line.set_transform(t.getTransform())
        svg.addElement(line)

def draw_polar_degree_labels(svg, radius, spacing_degree = 10, intake=3):

    #for theta in np.deg2rad(range(0, 360, spacing_degree)):
    for theta in range(270, 270+181, spacing_degree):
        theta %= 360
        if theta in [270, 0, 90]:
            continue
        text = Text("%d" % (theta), 0, -(radius-intake))
        text.set_style(text_style_middle_anchor.getStyle())

        t = TransformBuilder()
        t.setRotation("%d" % theta)
        text.set_transform(t.getTransform())
        svg.addElement(text)

    for theta in range(100, 269, spacing_degree):
        if theta in [180]:
            continue
        text = Text("%d" % (theta), 0, (radius-intake))
        text.set_style(text_style_middle_anchor.getStyle())

        t = TransformBuilder()
        t.setRotation("%d" % (theta-180))
        text.set_transform(t.getTransform())
        svg.addElement(text)

    for theta in range(0, 80, spacing_degree):
        if theta in [0]:
            continue

        text = Text("%d" % (theta), (radius+intake-2), 0)
        text.set_style(text_style_middle_anchor.getStyle())

        t = TransformBuilder()
        t.setRotation("%d" % (theta))
        text.set_transform(t.getTransform())
        svg.addElement(text)

        text = Text("%d" % (theta), (radius+intake-2), 0)
        text.set_style(text_style_middle_anchor.getStyle())
        t = TransformBuilder()
        t.setRotation("%d" % (-theta))
        text.set_transform(t.getTransform())
        svg.addElement(text)


def draw_meridian(svg, major_tick_length, minor_tick_length):
    PAGE_HEIGHT = params['PAGE_HEIGHT']
    LAT_SCALE = params['LAT_SCALE']
    STROKEWIDTH = params['STROKEWIDTH']

    svg.addElement(oh.createLine(0, PAGE_HEIGHT, 0, -PAGE_HEIGHT, strokewidth=STROKEWIDTH, stroke='black'))

    for tick in range(-int(PAGE_HEIGHT/2), int(PAGE_HEIGHT/2)):
        if tick % 5 == 0:
            svg.addElement(oh.createLine(0,tick*LAT_SCALE, major_tick_length, tick*LAT_SCALE, strokewidth=STROKEWIDTH, stroke='black'))
        else:
            svg.addElement(oh.createLine(0,tick*LAT_SCALE, minor_tick_length, tick*LAT_SCALE, strokewidth=STROKEWIDTH, stroke='black'))

        if tick % 10 == 0 and (-tick % 60) != 0:
            t = Text("%d'" % (-tick % 60), major_tick_length , tick*LAT_SCALE)
            t.set_style(text_style_start_anchor.getStyle())
            svg.addElement(t)

def draw_parallels(svg):
    PAGE_WIDTH = params['PAGE_WIDTH']
    LAT_SCALE = params['LAT_SCALE']
    STROKEWIDTH = params['STROKEWIDTH']

    svg.addElement(oh.createLine(-int(PAGE_WIDTH), 0, int(PAGE_WIDTH), 0, strokewidth=STROKEWIDTH, stroke='black'))
    for i in [1,2]:
        svg.addElement(oh.createLine(-int(PAGE_WIDTH), i*LAT_SCALE*60, int(PAGE_WIDTH), i*LAT_SCALE*60, strokewidth=STROKEWIDTH, stroke='black'))
        svg.addElement(oh.createLine(-int(PAGE_WIDTH), i*-LAT_SCALE*60, int(PAGE_WIDTH), i*-LAT_SCALE*60, strokewidth=STROKEWIDTH, stroke='black'))


def draw_conversion_chart(svg, yscaling=0.8):
    LAT_SCALE = params['LAT_SCALE']
    STROKEWIDTH = params['STROKEWIDTH']

    g = G()
    svg.addElement(g)

    lons = [0,2,4,6,8] + list(range(10, 70, 10))
    for lon in lons:
        points = []
        for lat in range(0, 71, 1):
            f = lat/360. * 2 * math.pi
            f =  math.cos(f)
            x = -LAT_SCALE * lon*f
            y = -LAT_SCALE*lat*yscaling

            if lat % 10 == 0 and lon == max(lons):
                g.addElement(oh.createLine(0+2, y, x, y, strokewidth=STROKEWIDTH, stroke='black'))

            if lat % 10 == 0 and lon == min(lons) and lat > 0:
                t = Text("%d°" % (lat), x+3 , y)
                t.set_style(text_style_start_anchor.getStyle())
                g.addElement(t)

            if lat % 5 == 0 and (lon == min(lons) or lon == max(lons)):
                g.addElement(oh.createLine(x+2, y, x, y, strokewidth=STROKEWIDTH, stroke='black'))
            elif lat % 1 == 0 and (lon == min(lons) or lon == max(lons)):
                g.addElement(oh.createLine(x+1, y, x, y, strokewidth=STROKEWIDTH, stroke='black'))

            points.append((x,y))

        pg=oh.createPolyline(points=oh.convertTupleArrayToPoints(points),strokewidth=0.1, stroke='black')
        g.addElement(pg)
    return g

def draw_compass(svg):
    MAJOR_TICK_STROKE_LENGTH = params['MAJOR_TICK_STROKE_LENGTH']
    MINOR_TICK_STROKE_LENGTH = params['MINOR_TICK_STROKE_LENGTH']
    LAT_SCALE = params['LAT_SCALE']
    STROKEWIDTH = params['STROKEWIDTH']

    compass = G()
    svg.addElement(compass)

    radius = LAT_SCALE * 60

    compass.addElement(oh.createCircle(0, 0, radius, strokewidth=STROKEWIDTH, stroke='black', fill='none'))

    draw_polar_ticks(compass, radius, spacing_degree=5, strokelength=MAJOR_TICK_STROKE_LENGTH)
    draw_polar_ticks(compass, radius, spacing_degree=1, strokelength=MINOR_TICK_STROKE_LENGTH)
    draw_polar_degree_labels(compass, radius, spacing_degree=10, intake = MAJOR_TICK_STROKE_LENGTH+2)
    draw_meridian(compass, MAJOR_TICK_STROKE_LENGTH, MINOR_TICK_STROKE_LENGTH)
    draw_parallels(compass)
    return compass

def ups(filename = "ups.svg", portrait = False):
    PAGE_HEIGHT = params['PAGE_HEIGHT']
    PAGE_WIDTH = params['PAGE_WIDTH']
    LAT_SCALE = params['LAT_SCALE']

    svg = Svg(width = "%fmm" % params['PAGE_WIDTH'], height= "%fmm" % params['PAGE_HEIGHT'])
    svg.set_viewBox("0 0 %f %f" % (params['PAGE_WIDTH'],  params['PAGE_HEIGHT']))

    t_compass = TransformBuilder()
    t_conv = TransformBuilder()

    yscaling=0.8

    if portrait:
        t_compass.setTranslation("%d %d" % (PAGE_WIDTH*0.5, PAGE_HEIGHT*2/5))
        t_conv.setTranslation("%d %d" % (PAGE_WIDTH-10, PAGE_HEIGHT*2/5 + 2* LAT_SCALE * 60))

    else:
        t_compass.setTranslation("%d %d" % (PAGE_WIDTH*0.4, PAGE_HEIGHT/2))
        t_conv.setTranslation("%d %d" % (PAGE_WIDTH-10, PAGE_HEIGHT/2 + LAT_SCALE * 60))

    compass = draw_compass(svg)
    compass.set_transform(t_compass.getTransform())

    c = draw_conversion_chart(svg, yscaling=yscaling)
    c.set_transform(t_conv.getTransform())

    svg.save(filename, encoding='utf-8')
    inkscape_pdf(filename)

def inkscape_pdf(svg_filename):
    return_code = subprocess.run(['C:\\Program Files\\Inkscape\\bin\\inkscape.exe', '--export-type=pdf', svg_filename])
    #print(return_code)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-pg", "--page", type=str, choices=["a4", "letter"],
                    help="Set page format", default='a4')
    parser.add_argument("-p", "--portrait", action="store_true",
                    help="Set format to portrait instead of landscape")
    parser.add_argument("-s", "--scale", type=float,
                    help="Set latitude scaling in mm per minutes", default=1.4)
    args = parser.parse_args()

    if args.page == 'A4':
        params['PAGE_HEIGHT'] = 210.
        params['PAGE_WIDTH'] = 297.
    elif args.page == 'letter':
        params['PAGE_HEIGHT'] =  8.5*2.54*10
        params['PAGE_WIDTH'] =  11*2.54*10

    if args.portrait:
        t = params['PAGE_WIDTH']
        params['PAGE_WIDTH'] = params['PAGE_HEIGHT']
        params['PAGE_HEIGHT'] = t


    ups(portrait=args.portrait)
