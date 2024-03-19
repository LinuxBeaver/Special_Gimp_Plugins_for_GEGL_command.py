#!/usr/bin/env python
# -*- coding: utf-8 -*-

# License: GPLv3
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY# without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# To view a copy of the GNU General Public License
# visit: http://www.gnu.org/licenses/gpl.html
#
#
# ------------
#| Change Log |
# ------------
# Rel 1: Initial release: dinasset_gegl.py by paynekj http://gimpchat.com/viewtopic.php?f=9&t=18040&p=254914#p254914
# This is a addition to  gegl-python-fu & gegl_graph.py that includes Beaver's third party GEGL plugins

from gimpfu import *
from sys import argv, platform
from ctypes import *
import random
import math
import sys, os

def load_library (library_name):
    if platform == "linux" or platform == "linux2":
        library_name = library_name + '.so.0'
    elif platform == "win32":
        from ctypes.util import find_library
        library_name = find_library (library_name + "-0")
    else:
        raise BaseException ("TODO")
    return CDLL (library_name)

gimp = load_library ('libgimp-2.0')

def gegl_graph(image, drawable, gegl_graph_string):
    class GeglBuffer(Structure):
        pass
    drawable_id = drawable.ID
    
    gegl = load_library ('libgegl-0.4')
    sucess = gegl.gegl_init (None, None)
    gimp.gimp_drawable_get_shadow_buffer.restype = POINTER (GeglBuffer)
    gimp.gimp_drawable_get_buffer.restype        = POINTER (GeglBuffer)

    x = c_int (); y = c_int (); w = c_int (); h = c_int ()
    non_empty,x,y,w,h = pdb.gimp_drawable_mask_intersect (drawable)
    args = [b"string", c_char_p (gegl_graph_string), c_void_p ()]
    
    if non_empty:
        source = gimp.gimp_drawable_get_buffer (drawable_id)
        target = gimp.gimp_drawable_get_shadow_buffer (drawable_id)
        sucess = gegl.gegl_render_op (source, target, "gegl:gegl", *args)
        gegl.gegl_buffer_flush (target)
        gimp.gimp_drawable_merge_shadow (drawable_id, PushUndo = True)
        gimp.gimp_drawable_update (drawable_id, x, y, w, h)
        gimp.gimp_displays_flush ()

register(
   "python_fu_gegl_graph",
   "Do GEGL graph example Tooltip",
   "Do GEGL graph example Additional",
   "paynekj",
   "GPL3",
   "2020.08.24",
   "Do GEGL graph", 
   "RGB*",
   [
     (PF_IMAGE,      "image",       "Input image", None),
     (PF_DRAWABLE,   "drawable", "Input drawable", None),
     (PF_STRING, "gegl_graph_string", "GEGL Graph String", "gegl:wind")
   ],
   [],
   gegl_graph,

   )

#---------------------------------------------------------------------------------------------
#| Change Log |
# ------------
# Web page: https://github.com/LinuxBeaver?tab=repositories
# Binaries_for_windows_and_linux (gegl_command.py_compatible_plugins) https://github.com/LinuxBeaver/Special_Gimp_Plugins_for_GEGL_command.py/releases/tag/gegl_command.py_compatible_plugins

# Change Log

# Rel 1.0: Initial release: 23/11/2023 LinuxBeaver [ aka contrast_]: 19 plugins (scheduled 24) Rel 1.0 includes these five: Glossy Balloon, Custom Bevel, Sharp Bevel, Metallic, Action Lines,
# Rel 1.1: adds the following: Align, Old Photo Effect, Bokeh, Clouds, Double Glow, Edge Extract, Electricity, Fog, Grains of Sand, Inner Glow, Long Shadow Extrusion, Neon Border, Pencil,
# Rel 1.2:

#-------------------------------------MrQ-----------------------------------------------------
def rgb_to_hex(rgb_color):
    r = rgb_color[0]
    g = rgb_color[1]
    b = rgb_color[2]
    return '#%02x%02x%02x' % (r,g,b)
	

#-------------------------------------Glossy_Balloon-----------------------------------------------------	

def gegl_glossy_balloon(image, layer, gaus,hue,lightness,opacityall):


    gegl_graph_string="lb:script-glossy-balloon gaus=%f hue=%f lightness=%f opacityall=%f" % (gaus, hue, lightness, opacityall)
    pdb.python_fu_gegl_graph(image, layer, gegl_graph_string)

register(
    "python_fu_gegl_glossy_balloon",
    "GEGL to Python. Works on the active layer",
    "Glossy Balloon GEGL Text Styling Plugin In Python (Special fork)",
    "Auto Author",
    "Auto Author",
    "Auto Generated Dated",
    "<Image>/GEGL as Python/Third_Party_GEGL_Plugins/gegl-glossy-balloon...",             #Menu path
    "*", 
    [
    (PF_FLOAT, "gaus","Balloonification (default:6.0, 0.5 20.0):", 6.0),	 
    (PF_FLOAT, "hue","Rotate Color (default:0, -180 180.0):", 0),
    (PF_FLOAT, "lightness","Lightness (default:-7, -15.0 15.0):", -7),
    (PF_FLOAT, "opacityall","Internal Opacity (default:0.0, 1.0 5.0):", 3.0),

    ],
    [],
    gegl_glossy_balloon)

#-------------------------------------Custom_Bevel-----------------------------------------------------	

def gegl_custom_bevel(image, layer, opacity, blendmode, azimuth, elevation, depth, size, alphapercentile, gaus, box, mcb):


    if blendmode==0:
        blend_mode= "Hardlight"
    if blendmode==1:
        blend_mode= "Multiply"
    if blendmode==2:
        blend_mode= "ColorDodge"
    if blendmode==3:
        blend_mode= "Plus"
    if blendmode==4:
        blend_mode= "Darken"
    if blendmode==5:
        blend_mode= "Lighten"



    gegl_graph_string="lb:script-custom-bevel opacity=%f blendmode=%s azimuth=%f elevation=%f depth=%f size=%f alphapercentile=%f gaus=%f box=%f mcb=%f" % (opacity, blend_mode, azimuth, elevation, depth, size, alphapercentile, gaus, box, mcb)
    pdb.python_fu_gegl_graph(image, layer, gegl_graph_string)

register(
    "python_fu_gegl_custom_bevel",
    "GEGL to Python. Works on the active layer",
    "Custom Bevel GEGL Text Styling Plugin In Python (Special fork)",
    "Auto Author",
    "Auto Author",
    "Auto Generated Dated",
    "<Image>/GEGL as Python/Third_Party_GEGL_Plugins/gegl-custom-bevel...",             #Menu path
    "*", 
    [
    (PF_FLOAT, "opacity","Internal opacity (default:1.0, 3.5 10.0):", 3.5),
    (PF_OPTION,  "blend_mode", "Blendmode:", 0, ["Hardlight","Multiply","ColorDodge","Plus","Darken","Lighten"]), 
    (PF_FLOAT, "azimuth","Azimuth (default:67, 30 90.0):", 67),
    (PF_FLOAT, "elevation","Elevation (default:25, 7 90):", 25),
    (PF_FLOAT, "depth","Depth (default:24, 1 100):", 24),
    (PF_FLOAT, "size","Internal Median Radius (default:1, 0 15):", 1),
    (PF_FLOAT, "alphapercentile","Internal Median AP (default:68, 0 100):", 68),
    (PF_FLOAT, "gaus","Internal Gaussian Blur (default:2, 0 9):", 2),
    (PF_FLOAT, "box","Internal Box Blur (default:0, 0 6):", 0),
    (PF_FLOAT, "mcb","Smooth (default:0, 0 6):", 1),

    ],
    [],
    gegl_custom_bevel)

#-------------------------------------Sharp_Bevel-----------------------------------------------------	

def gegl_sharp_bevel(image, layer, blendmode,  azimuth, elevation, depth,  size,  transvalue, bevelcontrol, smooth):

    if blendmode==0:
        blend_mode= "hardlight"
    if blendmode==1:
        blend_mode= "multiply"
    if blendmode==2:
        blend_mode= "colordodge"
    if blendmode==3:
        blend_mode= "plus"
    if blendmode==4: 
        blend_mode= "darken"
    if blendmode==5:
        blend_mode= "lighten"
    if blendmode==6:
        blend_mode= "overlay"


    gegl_graph_string="lb:script-sharpbevel blendmode=%s azimuth=%f elevation=%f depth=%f size=%f transvalue=%f bevelcontrol=%f smooth=%f" % (blend_mode, azimuth, elevation, depth, size, transvalue, bevelcontrol, smooth)
    pdb.python_fu_gegl_graph(image, layer, gegl_graph_string)

register(
    "python_fu_gegl_sharp_bevel",
    "GEGL to Python. Works on the active layer",
    "Sharp Bevel GEGL Text Styling Plugin In Python (Special fork)",
    "Auto Author",
    "Auto Author", 
    "Auto Generated Dated",
    "<Image>/GEGL as Python/Third_Party_GEGL_Plugins/gegl-sharp-bevel...",             #Menu path
    "*", 
    [
    (PF_OPTION,  "blend_mode", "Blendmode:", 0, ["Hardlight","Multiply","ColorDodge","Plus","Darken","Lighten","Overlay"]), 
    (PF_FLOAT, "azimuth","Azimuth (default:67, 20 90.0):", 67),
    (PF_FLOAT, "elevation","Elevation (default:25, 7 140):", 25),
    (PF_FLOAT, "depth","Depth (default:24, 8 100):", 24),
    (PF_FLOAT, "size","Size (default:3, 1 9):", 3),
    (PF_FLOAT, "transvalue","Remove Black Artifact (default:0.05, 0.00 0.03):", 0.05),
    (PF_FLOAT, "bevelcontrol","Make Surface Flat (default:1, 1 6):", 1),
    (PF_FLOAT, "smooth","Smooth (default:9, 1 20):", 9),


    ],
    [],
    gegl_sharp_bevel)
#-------------------------------------Metallic-----------------------------------------------------

def gegl_metallic(image, layer, solar1, solar2, solar3, light, smooth, value):


    gegl_graph_string="lb:script-metallic solar1=%f solar2=%f solar3=%f light=%f smooth=%f value=%f" % (solar1, solar2, solar3, light, smooth, value)
    pdb.python_fu_gegl_graph(image, layer, gegl_graph_string)

register(
    "python_fu_gegl_metallic",
    "GEGL to Python. Works on the active layer",
    "Metallic GEGL Plugin In Python (Special fork)",
    "Auto Author",
    "Auto Author",
    "Auto Generated Dated",
    "<Image>/GEGL as Python/Third_Party_GEGL_Plugins/gegl-metallic...",             #Menu path
    "*", 
    [
    (PF_FLOAT, "solar1","Solarization of Red Channel (default:2.7, 0.0 4.0):", 2.7),
    (PF_FLOAT, "solar2","Solarization of Green Channel (default:2.8, 2.2 4.0):", 2.8),
    (PF_FLOAT, "solar3","Solarization of Blue Channel (default:2.1, 0.0 4.0):", 2.1),
    (PF_FLOAT, "light","Lightness (default:0, -10.0 10.0):", 0),		 
    (PF_FLOAT, "smooth","Smooth (default:2, 0 8):", 2),
    (PF_FLOAT, "value","Invert Original Image (default:0.0, 0.0 1.0):", 0),

    ],
    [],
    gegl_metallic)

#-------------------------------------Action_Lines-----------------------------------------------------

def gegl_action_lines(image, layer, movex,movey,color_al,radius,lines, seed_al, opacity):

    color_to_gegl_al=rgb_to_hex(color_al)
    if seed_al==0:
        seed=0
    if seed_al==1:
        seed=random.randrange(0,4294967296)	   

    gegl_graph_string="lb:script-action-lines movex=%f movey=%f color=%s radius=%d lines=%d seed=%s opacity=%f" % (movex, movey, color_to_gegl_al, radius, lines, seed, opacity)
    pdb.python_fu_gegl_graph(image, layer, gegl_graph_string)

register(
    "python_fu_gegl_action_lines",
    "GEGL to Python. Works on the active layer",
    "Action Lines GEGL Plugin In Python",
    "Auto Author",
    "Auto Author",
    "Auto Generated Dated",
    "<Image>/GEGL as Python/Third_Party_GEGL_Plugins/gegl-action_lines...",             #Menu path
    "*", 
    [
    (PF_FLOAT, "movex","Move Horizontal (default:0.500, 0.0 0.80):", 0.500),
    (PF_FLOAT, "movey","Move Vertical (default:0.500, 0.0 0.80):", 0.500),
    (PF_COLOR, "color_al",         "Color:", (0, 0, 0)), 
    (PF_SPINNER, "radius","Radius of Lines (default:3200, 800..10000):", 3200, (800, 10000, 3200)),
    (PF_SPINNER, "lines","Amount of Lines (default:700, 380..1024):", 700, (380, 1024, 700)),
    (PF_OPTION,  "seed_al", "Seed:", 0, ["Seed=0","Random seed"]),
    (PF_FLOAT, "opacity","Opacity of Lines (default:2.0, 0.6 3.0):", 2.0),

    ],
    [],
    gegl_action_lines)

#-------------------------------------Align-----------------------------------------------------

def gegl_align (image, layer, scale_mode, scale, x, y):

    if scale_mode==0:
        scalemode= "nohalo"
    if scale_mode==1:
        scalemode= "lohalo"

    gegl_graph_string="lb:align algorithm=%s scale=%f x=%f y=%f" % (scalemode, scale, x, y)
    pdb.python_fu_gegl_graph(image, layer, gegl_graph_string)

register(
    "python_fu_gegl_align",
    "GEGL to Python. Works on the active layer",
    "Align GEGL Plugin In Python",
    "Auto Author",
    "Auto Author", 
    "Auto Generated Dated",
    "<Image>/GEGL as Python/Third_Party_GEGL_Plugins/gegl-align...",             #Menu path
    "*", 
    [
    (PF_OPTION,  "scale_mode", "Algorithm:", 0, ["nohalo","lohalo"]), 
    (PF_FLOAT, "scale","Scale Down Image (default:1.00, 0.05 1.00):", 1.00),
    (PF_FLOAT, "x","X Horizontal (default:0.5, 0.0 1.0):", 0.5),
    (PF_FLOAT, "y","Y Vertical (default:0.5, 0.0 1.0):", 0.5),

    ],
    [],
    gegl_align)

#-------------------------------------Old Photo Effect-----------------------------------------------------

def gegl_antique (image, layer, scale1, scale, lightness, noisergb, gaus, shadows, highlights):

    gegl_graph_string="lb:script-antique scale1=%f scale=%f lightness=%f noisergb=%f gaus=%f shadows=%f  highlights=%f" % (scale1, scale, lightness, noisergb, gaus, shadows, highlights)
    pdb.python_fu_gegl_graph(image, layer, gegl_graph_string)

register(
    "python_fu_gegl_antique",
    "GEGL to Python. Works on the active layer",
    "Align GEGL Plugin In Python",
    "Auto Author",
    "Auto Author", 
    "Auto Generated Dated",
    "<Image>/GEGL as Python/Third_Party_GEGL_Plugins/gegl-antique...",             #Menu path
    "*", 
    [
    (PF_FLOAT, "scale1","Saturation (default:-11, -100 20.00):", -11),
    (PF_FLOAT, "scale","Sepia (default:0.0, 0.0 1.0):", 0.3),
    (PF_FLOAT, "lightness","Lightness (default:0.88, 0.0 1.00):", 0.88),
    (PF_FLOAT, "noisergb","Noise (default:0.2, 0.0 0.3):", 0.2),
    (PF_FLOAT, "gaus","Mild Blur (default:1.5, 0.0 3.5):", 1.5),
    (PF_FLOAT, "shadows","Shadows (default:0.0, -100.0 100.0):", 0.0),
    (PF_FLOAT, "highlights","highlights (default:0.0, -70.0 50.0):", 0.0),

    ],
    [],
    gegl_antique)


#-------------------------------------Aura-----------------------------------------------------

def gegl_aura (image, layer, color, radius, gradius, opacity, tile_size, tile_saturation, maskradius):

    zegl=rgb_to_hex(color)

    gegl_graph_string="lb:script-aura color=%s radius=%f gradius=%f opacity=%f tile-size=%f tile-saturation=%f maskradius=%f" % (zegl, radius, gradius, opacity, tile_size, tile_saturation, maskradius)
    pdb.python_fu_gegl_graph(image, layer, gegl_graph_string)

register(
    "python_fu_gegl_aura",
    "GEGL to Python. Works on the active layer",
    "Aura GEGL Plugin In Python",
    "Auto Author",
    "Auto Author", 
    "Auto Generated Dated",
    "<Image>/GEGL as Python/Third_Party_GEGL_Plugins/gegl-aura...",             #Menu path
    "*", 
    [
    (PF_COLOR,   "color",         "Color:", (0, 255, 31)),
    (PF_FLOAT, "radius","Lens Blur Radius (default:11, 0.0 50.0):", 11),
    (PF_FLOAT, "gradius","Gaussian Radius (default:0.0, 0 50.0):", 0.0),
    (PF_FLOAT, "opacity","Opacity (default:1.0, 1 4.0):", 1.0),
    (PF_FLOAT, "tile_size","Internal Tile Size (default:6, 16.0):", 6),
    (PF_FLOAT, "tile_saturation","Internal Tile Saturation(default:3.0, 3.0 8.0):", 5.4),
    (PF_FLOAT, "mask_radius","Oilify (default:1.0, 1.0 4.0):", 4.0),

    ],
    [],
    gegl_aura)


#-------------------------------------Bokeh-----------------------------------------------------

def gegl_bokeh (image, layer, color, shape_2, amount, seed_al, size, opacity, blur):

    zegl=rgb_to_hex(color)
    if seed_al==0:
        seed=0
    if seed_al==1:
        seed=random.randrange(0,4294967296)	


    if shape_2==0:
        shape= "circle"
    if shape_2==1:
        shape= "square"
    if shape_2==2:
        shape= "diamond"

   
    gegl_graph_string="lb:script-bokeh color=%s neighborhood=%s amount=%f seed=%s size=%f opacity=%f blur=%f " % (zegl, shape, amount, seed, size, opacity, blur)
    pdb.python_fu_gegl_graph(image, layer, gegl_graph_string)





register(
    "python_fu_gegl_bokeh",
    "GEGL to Python. Works on the active layer",
    "Bokeh GEGL Plugin In Python",
    "Auto Author",
    "Auto Author", 
    "Auto Generated Dated",
    "<Image>/GEGL as Python/Third_Party_GEGL_Plugins/gegl-bokeh...",             #Menu path
    "*", 
    [
    (PF_COLOR,   "color",         "Color:", (255, 255, 255)),
    (PF_OPTION,  "shape", "Bokeh Shape:", 0, ["circle","square","diamond"]), 
    (PF_FLOAT, "amount","Increase Amount of Bokeh's (default:0.12, 0.05 0.35):", 0.12),
    (PF_OPTION,  "seed_al", "Seed:", 0, ["Seed=0","Random seed"]),
    (PF_FLOAT, "size","Size of Bokeh's (default:25, 1 80):", 25),
    (PF_FLOAT, "opacity","Opacity (default:0.6, 0.1 1.3):", 0.6),
    (PF_FLOAT, "blur","blur (default:2, 0 12):", 2),

    ],
    [],
    gegl_bokeh)

#-------------------------------------Clouds-----------------------------------------------------


def gegl_clouds (image, layer, cloudsize, saturation, hue, seed_al):

    if seed_al==0:
        seed=0
    if seed_al==1:
        seed=random.randrange(0,4294967296)	

    gegl_graph_string="lb:script-clouds cloudsize=%f saturation=%f hue=%f seed=%s " % (cloudsize, saturation, hue, seed)
    pdb.python_fu_gegl_graph(image, layer, gegl_graph_string)

register(
    "python_fu_gegl_clouds",
    "GEGL to Python. Works on the active layer",
    "Clouds GEGL Plugin In Python",
    "Auto Author",
    "Auto Author", 
    "Auto Generated Dated",
    "<Image>/GEGL as Python/Third_Party_GEGL_Plugins/gegl-clouds...",             #Menu path
    "*", 
    [
    (PF_FLOAT, "cloudsize","Cloud Size (default:4.0, 0.05 4.14):", 4.0),
    (PF_FLOAT, "saturation","Saturation (default:0.6, 0.6 1.0):", 0.6),
    (PF_FLOAT, "hue","Hue Rotation (default:0, -180 180):", 0),
    (PF_OPTION,  "seed_al", "Seed:", 0, ["Seed=0","Random seed"]),


    ],
    [],
    gegl_clouds)

#-------------------------------------Double Glow-----------------------------------------------------

def gegl_double_glow (image, layer, photocopy, photocopy2, photocopy3, photocopy4, color, gaussian1, glow1, color2, gaussian2, glow2, glow2radius, blurall):

    color_special=rgb_to_hex(color)
    color2_special=rgb_to_hex(color2)


    gegl_graph_string="lb:script-doubleglow photocopy=%f photocopy2=%f photocopy3=%f photocopy4=%f color=%s gaussian=%f opacity=%f color2=%s radius=%f opacity2=%f grow-radius=%f gaussian3=%f " % (photocopy, photocopy2, photocopy3, photocopy4, color_special, gaussian1, glow1, color2_special, gaussian2, glow2, glow2radius, blurall)
    pdb.python_fu_gegl_graph(image, layer, gegl_graph_string)

register(
    "python_fu_double_glow",
    "GEGL to Python. Works on the active layer",
    "Double Glow GEGL Plugin In Python",
    "Auto Author",
    "Auto Author", 
    "Auto Generated Dated",
    "<Image>/GEGL as Python/Third_Party_GEGL_Plugins/gegl-doubleglow...",             #Menu path
    "*", 
    [
    (PF_FLOAT, "photocopy","Internal Photocopy (default:5, 3 50):", 5),
    (PF_FLOAT, "photocopy2","Internal Photocopy 2 (default:1, 0.5 1):", 1),
    (PF_FLOAT, "photocopy3","Internal Photocopy 3 (default:1, 0.5 1):", 1),
    (PF_FLOAT, "photocopy4","Internal Photocopy 4 (default:0.99, 0.6 1):", 0.99),
    (PF_COLOR,   "color",         "Color:", (248, 0, 75)),
    (PF_FLOAT, "gaussian1","Blur Glow 1 (default:24, 0 50):", 24),
    (PF_FLOAT, "glow1","Hyper Opacity Glow 1 (default:2.5, 0 4):", 2.5),
    (PF_COLOR,   "color2",         "Color:", (252, 117, 47)),
    (PF_FLOAT, "gaussian2","Blur Glow 2 (default:1, 0 40):", 1),
    (PF_FLOAT, "glow2","Hyper Opacity Glow 2 (default:1.2, 0 2.0):", 1.2),
    (PF_FLOAT, "glow2radius","Radius of Glow 2 (default:1, -1 50):", 1),
    (PF_FLOAT, "blurall","Blur all (default:10, 0 60):", 10),

    ],
    [],
    gegl_double_glow)

#-------------------------------------Edge Extract-----------------------------------------------------

def gegl_edge_extract (image, layer, edgeamount, threshold, gaus, color):

    color_special=rgb_to_hex(color)

    gegl_graph_string="gegl:script-edge-extract edgeamount=%f threshold=%f gaus=%f value=%s  " % (edgeamount, threshold, gaus, color_special)
    pdb.python_fu_gegl_graph(image, layer, gegl_graph_string)

register(
    "python_fu_edge_extract",
    "GEGL to Python. Works on the active layer",
    "Edge Extract GEGL Plugin In Python",
    "Auto Author",
    "Auto Author", 
    "Auto Generated Dated",
    "<Image>/GEGL as Python/Third_Party_GEGL_Plugins/gegl-edge-extract...",             #Menu path
    "*", 
    [
    (PF_FLOAT, "edgeamount","Edge Amount (default:10, 3 16):", 10),
    (PF_FLOAT, "threshold","Threshold (default:0.76, -0.25 0.90):", 0.76),
    (PF_FLOAT, "gaus","Blur (default:1, 0.5 20.0):", 1),
    (PF_COLOR,   "color",         "Color:", (255, 255, 255)),

    ],
    [],
    gegl_edge_extract)

#-------------------------------------Electricity-----------------------------------------------------

def gegl_electricity (image, layer, tile_size, tile_saturation, seed_al, transparency_threshold, oil, iterations, opacity, blur, col):

    zegl=rgb_to_hex(col)
    if seed_al==0:
        seed=0
    if seed_al==1:
        seed=random.randrange(0,4294967296)	

    gegl_graph_string="lb:script-electricity tile-size=%f tile-saturation=%f seed=%s transparency-threshold=%f oil=%f iterations=%f opacity=%f blur=%f col=%s  " % (tile_size, tile_saturation, seed, transparency_threshold, oil, iterations, opacity, blur, zegl)
    pdb.python_fu_gegl_graph(image, layer, gegl_graph_string)


register(
    "python_fu_gegl_electricity",
    "GEGL to Python. Works on the active layer",
    "Electricity GEGL Plugin In Python",
    "Auto Author",
    "Auto Author", 
    "Auto Generated Dated",
    "<Image>/GEGL as Python/Third_Party_GEGL_Plugins/gegl-electricity...",             #Menu path
    "*", 
    [
    (PF_FLOAT, "tile_size","Internal Cubism Size (default:19, 6.0 35.0):", 19),
    (PF_FLOAT, "tile_saturation","Internal Cubism Spacing (default:4.0, 2 9.0):", 4.0),
    (PF_OPTION,  "seed_al", "Seed:", 0, ["Seed=0","Random seed"]),
    (PF_FLOAT, "transparency_threshold","Reduce electricity effect (default:0.064, 0.020 0.600):", 0.064),
    (PF_FLOAT, "oil","Internal Oilify to enhance electric effect (default:14, 8 30):", 14),
    (PF_FLOAT, "iterations","Internal Mean Curvature (default:20, 8 30):", 20),
    (PF_FLOAT, "opacity","Hyper Opacity (default:1.0, 1.0 2.0):", 1.0),
    (PF_FLOAT, "blur","Blur Rough Edges (default:1, 0 1):", 1),
    (PF_COLOR,   "col",         "Color:", (255, 255, 255)),

    ],
    [],
    gegl_electricity)

#-------------------------------------Fog-----------------------------------------------------


def gegl_fog (image, layer, turbulence, seed_al, transparency, gaus, value, opacity, width, height):


    zegl=rgb_to_hex(value)
    if seed_al==0:
        seed=0
    if seed_al==1:
        seed=random.randrange(0,4294967296)	

    gegl_graph_string="lb:script-fog turbulence=%f seed=%s transparency=%f gaus=%f value=%s opacity=%f width=%f height=%f " % (turbulence, seed, transparency, gaus, zegl, opacity, width, height)
    pdb.python_fu_gegl_graph(image, layer, gegl_graph_string)


register(
    "python_fu_gegl_fog",
    "GEGL to Python. Works on the active layer",
    "Fog GEGL Plugin In Python",
    "Auto Author",
    "Auto Author", 
    "Auto Generated Dated",
    "<Image>/GEGL as Python/Third_Party_GEGL_Plugins/gegl-fog...",             #Menu path
    "*", 
    [
    (PF_FLOAT, "turbulence","Turbulence of Fog (default:1.0, 0.0 26.0):", 1.0),
    (PF_OPTION,  "seed_al", "Seed:", 0, ["Seed=0","Random seed"]),
    (PF_FLOAT, "transparency","Isolate Fog patches (default:0.1, 0.0 0.5):", 0.1),
    (PF_FLOAT, "gaus","blur (default:0.0, 0.0 1.0):", 0.0),
    (PF_COLOR,   "col",         "Color:", (65535, 0, 0)),
    (PF_FLOAT, "opacity","opacity (default:1.0, 0.6 1.5):", 1.0),
    (PF_FLOAT, "width","width (default:1024, 0 4096):", 1024),
    (PF_FLOAT, "height","height (default:786, 0 4096):", 768),


    ],
    [],
    gegl_fog)

#-------------------------------------Grains of Sand-----------------------------------------------------



def gegl_grains_of_sand (image, layer, lightness, value, amountx, amounty, seed_al, tilesize,  amountx2, amounty2, seed_al2, tilesize2,  value2):


    zegl=rgb_to_hex(value)
    zegl2=rgb_to_hex(value2)
    if seed_al==0:
        seed=0
    if seed_al==1:
        seed=random.randrange(0,4294967296)	
    if seed_al2==0:
        seed2=0
    if seed_al2==1:
        seed2=random.randrange(0,4294967296)	

    gegl_graph_string="lb:script-sand-text lightness=%f value=%s amount-x=%f amount-y=%f seed=%s tilesize=%f amount-x2=%f amount-y2=%f seed2=%s tilesize2=%f  value2=%s   " % (lightness, zegl, amountx, amounty, seed, tilesize, amountx2, amounty2, seed2, tilesize2,  zegl2)
    pdb.python_fu_gegl_graph(image, layer, gegl_graph_string)


register(
    "python_fu_gegl_grains_of_sand",
    "GEGL to Python. Works on the active layer",
    "Grains of Sand GEGL Plugin In Python",
    "Auto Author",
    "Auto Author", 
    "Auto Generated Dated",
    "<Image>/GEGL as Python/Third_Party_GEGL_Plugins/gegl-grains_of_sand...",             #Menu path
    "*", 
    [
    (PF_FLOAT, "lightness","Lightness (default:0.0, 0.0 15.0):", 0.0),
    (PF_COLOR,   "value",         "Color:", (255, 255, 255)),
    (PF_FLOAT, "amountx","Amount X (default:20, 15 60):", 20),
    (PF_FLOAT, "amounty","Amount Y (default:20, 15 60):", 20),
    (PF_OPTION,  "seed_al", "Seed:", 0, ["Seed=0","Random seed"]),
    (PF_FLOAT, "tilesize","Tile Size (default:1.7, 1.5 2):", 1.7),
    (PF_FLOAT, "amountx2","Amount X2 (default:180, 100 512):", 180),
    (PF_FLOAT, "amounty2","Amount Y2 (default:150, 100 512):", 150),
    (PF_OPTION,  "seed_al2", "Seed2:", 0, ["Seed=0","Random seed"]),
    (PF_FLOAT, "tilesize2","Tile Size (default:1.7, 1.5 2.0):", 1.7),
    (PF_COLOR,   "value2",         "Color:", (255, 255, 255))


    ],
    [],
    gegl_grains_of_sand)

#-------------------------------------Inner Glow-----------------------------------------------------

def gegl_inner_glow(image, layer, mode,  x, y, radius, growradius, opacity, fixoutline, value2):


    if mode==0:
        modex= "default"
    if mode==1:
        modex= "invert"

    zegl=rgb_to_hex(value2)

    gegl_graph_string="lb:script-innerglow mode=%s  x=%f y=%f radius=%f grow-radius=%f opacity=%f fixoutline=%d value2=%s" % (modex, x, y, radius, growradius, opacity, fixoutline, zegl)
    pdb.python_fu_gegl_graph(image, layer, gegl_graph_string)





register(
    "python_fu_gegl_inner_glow",
    "GEGL to Python. Works on the active layer",
    "Inner Glow GEGL Text Styling and Outlining Effect Plugin In Python",
    "Auto Author",
    "Auto Author", 
    "Auto Generated Dated",
    "<Image>/GEGL as Python/Third_Party_GEGL_Plugins/gegl-inner_glow...",             #Menu path
    "*", 
    [
    (PF_OPTION,  "modex", "Mode of Inner Glow", 0, ["default","invert"]), 
    (PF_FLOAT, "x","Amount X (default:0, -20 20):", 0),
    (PF_FLOAT, "y","Amount Y (default:0, -20 20):", 0),
    (PF_FLOAT, "radius","Blur Radius (default:9.0, 0.0 60.0):", 9.0),
    (PF_FLOAT, "growradius","Grow Radius (default:4, 1 40):", 4),
    (PF_FLOAT, "opacity","opacity (default:1.2, 0.0 2.0):", 1.2),
    (PF_SPINNER, "fixoutline","Median to cover hard to reach pixels (default:60, 50 100):", 60, (50, 100, 60)),
    (PF_COLOR,   "value2",         "Color:", (255, 255, 255))

    ],
    [],
    gegl_inner_glow)

#-------------------------------------Long Shadow PD (Extrusion 2)-----------------------------------------------------


def gegl_long_shadow_pd(image, layer, angle, length, lengthblur, ls2, chroma, lightness, eob):


    if eob==0:
        eobx= "standalone"
    if eob==1:
        eobx= "behind"

    gegl_graph_string="gegl:script-long-shadow-pd angle=%f length=%f lengthblur=%f ls2=%s chroma=%f lightness=%f extract-or-behind=%s " % (angle, length, lengthblur, ls2, chroma, lightness, eobx)
    pdb.python_fu_gegl_graph(image, layer, gegl_graph_string)


register(
    "python_fu_gegl_long_shadow_pd",
    "GEGL to Python. Works on the active layer",
    "Long Shadow PD Extrusion Text Styling Plugin In Python",
    "Auto Author",
    "Auto Author", 
    "Auto Generated Dated",
    "<Image>/GEGL as Python/Third_Party_GEGL_Plugins/gegl-long-shadow-pd-extrusion...",             #Menu path
    "*", 
    [
    (PF_FLOAT, "angle","Angle (default:0, -180 180):", 0),
    (PF_FLOAT, "length","Length (default:40, 0 55):", 40),
    (PF_FLOAT, "lengthblur","Length Blur (LS2 only) (default:100, 95 200):", 100),
    (PF_TOGGLE,  "ls2",     "Enable Fading Long Shadow",   False),
    (PF_FLOAT, "chroma","Chroma (default:0, 0 30):", 0),
    (PF_FLOAT, "lightness","Lightness (default:0, -30 30):", 0),
    (PF_OPTION,  "eob", "Isolate extrusion or behind blend it", 1, ["Extract","Behind"]), 

    ],
    [],
    gegl_long_shadow_pd)

#-------------------------------------Neon_Border-----------------------------------------------------

def gegl_neon_border(image, layer, blurstroke, blurstroke2, stroke, stroke2, opacity, opacity2,  gaus, gaus2, opacityglow, colorneon, colorneontwo, colorblur):

    zegl=rgb_to_hex(colorneon)
    zegl2=rgb_to_hex(colorneontwo)
    zegl3=rgb_to_hex(colorblur)


    gegl_graph_string="lb:script-neon-border  blurstroke=%f blurstroke2=%f stroke=%f stroke2=%f opacity=%f opacity2=%f gaus=%f gaus2=%f opacityglow=%f colorneon=%s colorneon2=%s colorblur=%s " % (blurstroke, blurstroke2, stroke, stroke2, opacity, opacity2, gaus, gaus2, opacityglow, zegl, zegl2, zegl3)

    pdb.python_fu_gegl_graph(image, layer, gegl_graph_string)

register(
    "python_fu_gegl_neon_border",
    "GEGL to Python. Works on the active layer",
    "Neon Border Text Styling Plugin In Python",
    "Auto Author",
    "Auto Author", 
    "Auto Generated Dated",
    "<Image>/GEGL as Python/Third_Party_GEGL_Plugins/gegl-neon-border...",             #Menu path
    "*", 
    [
    (PF_FLOAT, "blurstroke","Blur Radius 1 (default:2.2, 0.0 14.0):", 2.2),
    (PF_FLOAT, "blurstroke2","Blur Radius 2 (default:2.2, 0.0 14.0):", 4.3),
    (PF_FLOAT, "stroke","Grow Radius 1 (default:9.0, 0 50.0):", 9.0),
    (PF_FLOAT, "stroke2","Grow Radius 2 (default:2.1, 0.0 12.0):", 2.1),
    (PF_FLOAT, "opacity","Outline Opacity 1 (default:1.2, 0.0 1.3):", 1.2),
    (PF_FLOAT, "opacity2","Outline Opacity 2 (default:1.2, 0.0 1.3):", 1.2),
    (PF_FLOAT, "gaus","Behind Glow Horizontal Range (default:10, 0 100):", 10),
    (PF_FLOAT, "gaus2","Behind Glow Vertical Range  (default:10, 0 100):", 65),
    (PF_FLOAT, "opacityglow","Opacity of behind glow (default:0.40, 0.0 1.0):", 0.40),
    (PF_COLOR,   "colorneon",         "Color:", (255, 255, 255)),
    (PF_COLOR,   "colorneontwo",         "Color 2:", (0, 255, 5)),
    (PF_COLOR,   "colorblur",         "Color of Behind Glow:", (78, 239, 161)),

    ],
    [],
    gegl_neon_border)

#-------------------------------------Pencil-----------------------------------------------------

def gegl_pencil(image, layer, gaus, dt, dg1, dg2, low, high):

    gegl_graph_string="lb:script-pencil gaus=%f dt=%f dg1=%f dg2=%f low=%f high=%f " % (gaus, dt, dg1, dg2, low, high)
    pdb.python_fu_gegl_graph(image, layer, gegl_graph_string)


register(
    "python_fu_gegl_pencil",
    "GEGL to Python. Works on the active layer",
    "Pencil Plugin In Python",
    "Auto Author",
    "Auto Author", 
    "Auto Generated Dated",
    "<Image>/GEGL as Python/Third_Party_GEGL_Plugins/gegl-pencil...",             #Menu path
    "*", 
    [
    (PF_FLOAT, "gaus","Blur (default:2.0, 0.0 2.5):", 2.0),
    (PF_FLOAT, "dt","Smoothness (default:1, 1 5):", 1),
    (PF_FLOAT, "dg1","Internal Difference of Gaussian 1 (default:0.4, 0.4 1.0):", 1.0),
    (PF_FLOAT, "dg2","Internal Difference of Gaussian 2 (default:0.4, 0.0 1.0):", 0.3),
    (PF_FLOAT, "low","Output Low Levels (default:0.004, 0.000 0.008):", 0.004),
    (PF_FLOAT, "high","Input High Levels (default:0.004, 0.004 0.010):", 0.009),

    ],
    [],
    gegl_pencil)

#-------------------------------------Polygons, Starbackground, Starburst, Starfield, and Video Degradation Mod (5 plugins) remain -----------------------------------------------------



#---------------------------------------------------------------------------------------------


main()

