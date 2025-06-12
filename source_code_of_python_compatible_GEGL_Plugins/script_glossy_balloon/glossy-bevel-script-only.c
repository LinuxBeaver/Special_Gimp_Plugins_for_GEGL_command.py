/* This file is an image processing operation for GEGL
 *
 * GEGL is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 3 of the License, or (at your option) any later version.
 *
 * GEGL is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with GEGL; if not, see <https://www.gnu.org/licenses/>.
 *
 * Credit to Øyvind Kolås (pippin) for major GEGL contributions
 * 2022, 2023 Beaver GEGL Glossy Balloon (FOR GEGL-COMMAND.PY SCRIPTING ONLY)


THIS FILTER SHOULD NEVER BE RAN IN A GUI OUTSIDE OF PYTHON SCRIPTING. IT IS HIDDEN FROM GEGL OPERATIONS AND EVERY GIMP MENU IN DEFAULT
 */

#include "config.h"
#include <glib/gi18n-lib.h>

#ifdef GEGL_PROPERTIES



#define TUTORIAL \
" color-overlay value=#f587ff median-blur  percentile=90 alpha-percentile=100 "\


#define TUTORIAL2 \
" id=3 screen aux=[   ref=3 emboss  type=bumpmap azimuth=30  elevation=15 ] median-blur  percentile=90 alpha-percentile=100 gaussian-blur std-dev-x=1 std-dev-y=1 filter=fir id=3 screen aux=[ ref=3  emboss  type=bumpmap azimuth=90  elevation=15 ] screen aux=[ ref=3  emboss  type=bumpmap azimuth=90  elevation=15 ] median-blur  percentile=50 alpha-percentile=100 screen aux=[ ref=3  emboss  type=bumpmap azimuth=90  elevation=15 ] median-blur  percentile=50 alpha-percentile=100 screen aux=[ ref=3  emboss  type=bumpmap azimuth=90  elevation=15 ] reinhard05 brightness=-4 light=0 chromatic=0   "\



property_double (gaus, _("Balloonification of text"), 6.0)
   description  (_("The lower the less balloonification. The higher the more balloonification.'"))
  value_range (0.5, 20.0)
  ui_range (0.5, 14)
  ui_gamma (1.5)

property_double (hue, _("Color rotation"),  0.0)
   description  (_("Hue Rotation"))
   value_range  (-180.0, 180.0)

property_double (lightness, _("Lightness"), -7)
   description  (_("Lightness adjustment"))
   value_range  (-15.0, 15)

property_double (saturation, _("Desaturation for Image File Upload"), 1.2)
   description  (_("Saturation"))
  ui_range (0.0, 1.5)
   value_range  (0.0, 1.5)

property_file_path(src, _("Image file overlay (Desaturation and bright light recommended)"), "")
    description (_("Source image file path (png, jpg, raw, svg, bmp, tif, ...)"))

property_double (opacityall, _("Slide up to remove transparency puff around edges"), 3.0)
    description (_("Global opacity value that is always used on top of the optional auxiliary input buffer."))
    value_range (1.0, 5.0)
    ui_range    (1.0, 5.0)



#else

#define GEGL_OP_META
#define GEGL_OP_NAME     glossy_bevel_script_only
#define GEGL_OP_C_SOURCE glossy-bevel-script-only.c

#include "gegl-op.h"

static void attach (GeglOperation *operation)
{
  GeglNode *gegl = operation->node;
  GeglNode *input, *output, *blur, *graph, *fix, *graph2, *hue, *layer, *saturation, *opacityall, *multiply;

  input    = gegl_node_get_input_proxy (gegl, "input");
  output   = gegl_node_get_output_proxy (gegl, "output");

  blur    = gegl_node_new_child (gegl,
                                  "operation", "gegl:gaussian-blur",
   "filter", 1,
                                  NULL);

 graph   = gegl_node_new_child (gegl,
                                  "operation", "gegl:gegl", "string", TUTORIAL,
                                  NULL);

 graph2   = gegl_node_new_child (gegl,
                                  "operation", "gegl:gegl", "string", TUTORIAL2,
                                  NULL);



 hue   = gegl_node_new_child (gegl,
                                  "operation", "gegl:hue-chroma",
                                  NULL);

 layer   = gegl_node_new_child (gegl,
                                  "operation", "gegl:layer",
                                  NULL);


 opacityall   = gegl_node_new_child (gegl,
                                  "operation", "gegl:opacity",
                                  NULL);

 fix   = gegl_node_new_child (gegl,
                                  "operation", "gegl:median-blur", "radius", 0,
                                  NULL);

 saturation   = gegl_node_new_child (gegl,
                                  "operation", "gegl:saturation",
                                  NULL);

 multiply   = gegl_node_new_child (gegl,
                                  "operation", "gegl:multiply",
                                  NULL);

  gegl_node_link_many (input, graph, blur, graph2, hue, saturation, multiply, opacityall, fix, output, NULL);
  gegl_node_connect (multiply, "aux", layer, "output");

  gegl_operation_meta_redirect (operation, "gaus", blur, "std-dev-x");
  gegl_operation_meta_redirect (operation, "gaus", blur, "std-dev-y");
  gegl_operation_meta_redirect (operation, "hue", hue, "hue");
  gegl_operation_meta_redirect (operation, "lightness", hue, "lightness");
  gegl_operation_meta_redirect (operation, "src", layer, "src");
  gegl_operation_meta_redirect (operation, "saturation", saturation, "scale");
  gegl_operation_meta_redirect (operation, "opacityall",  opacityall, "value");

}

static void
gegl_op_class_init (GeglOpClass *klass)
{
  GeglOperationClass *operation_class;

  operation_class = GEGL_OPERATION_CLASS (klass);

  operation_class->attach = attach;

  gegl_operation_class_set_keys (operation_class,
    "name",        "lb:script-glossy-balloon",
    "title",       _("Glossy Balloon for scripting"),
    "categories",  "hidden",
    "reference-hash", "45a42mkf903ig3212c",
    "description", _("The normal glossy ballon filter does not work with gegl command.py scripting. This modded version will "
                     ""),
    NULL);
}

#endif
