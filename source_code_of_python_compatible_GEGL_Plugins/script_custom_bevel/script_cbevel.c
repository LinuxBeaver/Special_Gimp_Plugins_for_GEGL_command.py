/*This file is an image processing operation for GEGL
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
 * 2022,2023 Beaver (GEGL custom bevel FOR SCRIPTING ONLY) 
 */

#include "config.h"
#include <glib/gi18n-lib.h>

#ifdef GEGL_PROPERTIES



#define GEGLGRAPHSTRING \
" id=graph src-in aux=[ ref=graph ] id=graph src-in aux=[ ref=graph ]  "\


#define GEGLGRAPHSTRING2 \
"  id=0 dst-out aux=[ ref=0  component-extract component=alpha   levels in-low=0.15  color-to-alpha opacity-threshold=0.6 ] median-blur radius=0    "\


enum_start (scriptgegl_blend_mode_typecbevel)
  enum_value (GEGL_BLEND_MODE_TYPE_HARDLIGHT, "Hardlight",
              N_("HardLight"))
  enum_value (GEGL_BLEND_MODE_TYPE_MULTIPLY,      "Multiply",
              N_("Multiply"))
  enum_value (GEGL_BLEND_MODE_TYPE_COLORDODGE,      "ColorDodge",
              N_("ColorDodge"))
  enum_value (GEGL_BLEND_MODE_TYPE_PLUS,      "Plus",
              N_("Plus"))
  enum_value (GEGL_BLEND_MODE_TYPE_DARKEN,      "Darken",
              N_("Darken"))
  enum_value (GEGL_BLEND_MODE_TYPE_LIGHTEN,      "Lighten",
              N_("Lighten"))
  enum_value (GEGL_BLEND_MODE_TYPE_EMBOSSBLEND,      "EmbossBlend",
              N_("Grayscale Multiply for Image uploads"))
enum_end (scriptGeglBlendModeTypecbevel)

property_enum (blendmode, _("Blend Mode of Internal Emboss"),
    scriptGeglBlendModeTypecbevel, scriptgegl_blend_mode_typecbevel,
    GEGL_BLEND_MODE_TYPE_HARDLIGHT)

enum_start (scriptgegl_median_blur_neighborhoodcb)
  enum_value (GEGL_MEDIAN_BLUR_NEIGHBORHOOD_SQUAREcb,  "squarecb",  N_("Square"))
  enum_value (GEGL_MEDIAN_BLUR_NEIGHBORHOOD_CIRCLEcb,  "circlecb",  N_("Circle"))
  enum_value (GEGL_MEDIAN_BLUR_NEIGHBORHOOD_DIAMONDcb, "diamondcb", N_("Diamond"))
enum_end (scriptGeglMedianBlurNeighborhoodcb)


property_enum (type, _("Choose Internal Median Shape"),
               scriptGeglMedianBlurNeighborhoodcb, scriptgegl_median_blur_neighborhoodcb,
               GEGL_MEDIAN_BLUR_NEIGHBORHOOD_CIRCLEcb)
  description (_("Neighborhood type"))


property_double (opacity, _("Make bevel wider"), 3.5)
    description (_("Makes Bevel more opaque with gegl opacity. This on high settings can create a problem where the outlines of the bevel are irregular with rough edges. Certain blend modes benefit from lower settings or higher settings."))
    value_range (1.0, 10.0)
    ui_range    (1.0, 10.0)


property_int (azimuth, _("Azimuth"), 67)
    description (_("Light angle (degrees)"))
    value_range (30, 90)
    ui_meta ("unit", "degree")


property_int (elevation, _("Elevation"), 25)
    description (_("Elevation angle (degrees)"))
    value_range (7, 90)
    ui_meta ("unit", "degree")

property_int (depth, _("Depth and or detail"), 24)
    description (_("Brings out depth and or detail of the bevel depending on the blend mode"))
    value_range (1, 100)

property_int  (size, _("Internal Median Blur Radius"), 1)
  value_range (0, 15)
  ui_range    (0, 15)
  ui_meta     ("unit", "pixel-distance")
  description (_("Neighborhood radius, a negative value will calculate with inverted percentiles"))

property_int  (percentile, _("Internal Median Blur Percentile"), 53)
  value_range (20, 80)
  description (_("Neighborhood color percentile"))


property_int  (alphapercentile, _("Internal Median Blur Alpha percentile"), 68)
  value_range (0, 100)
  description (_("Neighborhood alpha percentile"))

property_double (gaus, _("Internal Gaussian Blur for a normal bevel"), 2)
   description (_("Makes a normal bevel by calling an internal gaussian blur"))
   value_range (0.0, 9.0)

property_int (box, _("Internal Box Blur for a box bevel"), 3)
   description(_("Makes a box bevel by calling an internal box blur"))
   value_range (0, 10)
   ui_range    (0, 10)

property_int  (mcb, _("Smooth bevel"), 1)
    description(_("Applies a mean curvature blur on the bevel"))
  value_range (0, 6)
  ui_range    (0, 6)


property_double (sharpen, _("Sharpen"), 0.2)
    description(_("Applies a sharpen filter on the bevel"))
    value_range (0.0, 4.5)
    ui_range    (0.0, 4.5)

property_file_path(src, _("Image file Overlay - Desaturate and lighten for best results"), "")
    description (_("Source image file path (png, jpg, raw, svg, bmp, tif, ...) You can remove an image file overlay by going back to the image file select window, removing all text from --location-- then click open. Image file overlay will then go back to its default (None)"))


property_double (slideupblack, _("Dark Text mode"), 0.000)
   description  (_("For dark bevels and bevels with images under them. Use 1. Slide up if text color is dark or black and this will allow the bevel to significantly better on dark and black text. Dark bevels seem to work best on the multiply blend mode."))
   value_range  (0.000, 0.050)

property_double (desat, _("Desaturate for image file and color overlay"), 1.0)
    description(_("Desaturates the bevel to prepare it for a image file overlay"))
    value_range (0.0, 1.3)
    ui_range (0.0, 1.3)



property_double (lightness, _("Lightness that can help image file and color overlay"), 0.0)
   description  (_("Lightness adjustment, lightness adjustment can add imagefile overlay"))
   value_range  (-12.0, 26.0)


property_double (hue, _("Hue Rotation -0 resets"),  0.0)
   description  (_("Hue adjustment -  0 resets. This will hue rotate everything in the bevel and is useful if you want to maintain a shine associated with a certain color. Rotating the hue on a shiny inducing color (like pink on color dodge) is a good idea."))
   value_range  (-180.0, 180.0)


property_enum (switchbevel, _("Custom Bevel mode/version select"),
    scriptcustombevelmodes, scriptcustom_bevel_modes,
    CLASSIC)
    description (_("The new version of Custom Bevel that is not default has an easier recolor and does not conform to image file overlays via dark bevel mode. "))


property_color (coloroverlay, _("Color Overlay (requires white text/shape on non recolor modes"), "#ffffff")
    description (_("The color to paint over a white bevel. If the text is white the bevel will become any color. If it is not white it could distort things as it will behave as if you are applying a multiply blend mode color overlay on the bevel. White makes transparent. This is literally a multiply blend mode color overlay. This does not apply to Modern Recolor mode where it will force the color to be anything."))


enum_start (scriptcustom_bevel_modes)
  enum_value (CLASSIC, "classic",
              N_("Classic Custom Bevel"))
  enum_value (NO_COLOR_MODERN, "modernnocolor",
              N_("Modern Custom Bevel"))
  enum_value (COLOR_MODERN,      "moderncolor",
              N_("Modern Custom Bevel (recolor mode)"))
enum_end (scriptcustombevelmodes)



#else

#define GEGL_OP_META
#define GEGL_OP_NAME     script_cbevel
#define GEGL_OP_C_SOURCE script_cbevel.c

#include "gegl-op.h"

typedef struct
{
  GeglNode *input;
  GeglNode *median;
  GeglNode *box;
  GeglNode *gaussian;
  GeglNode *hardlight;
  GeglNode *multiply;
  GeglNode *colordodge;
  GeglNode *emboss;
  GeglNode *plus;
  GeglNode *darken;
  GeglNode *lighten;
  GeglNode *opacity;
  GeglNode *mcb;
  GeglNode *sharpen;
  GeglNode *desat;
  GeglNode *multiply2;
  GeglNode *nop;
  GeglNode *nop2;
  GeglNode *mcol;
  GeglNode *col;
  GeglNode *imagefileoverlay;
  GeglNode *lightness;
  GeglNode *embossblend;
  GeglNode *killpuff;
  GeglNode *killpuff2;
  GeglNode *repairgeglgraph;
  GeglNode *medianbookmark;
  GeglNode *bookmark;
  GeglNode *multiplybookmark;
  GeglNode *darkbevel;
  GeglNode *white;
  GeglNode *output;
}State;

static void
update_graph (GeglOperation *operation)
{
  GeglProperties *o = GEGL_PROPERTIES (operation);
  State *state = o->user_data;
  if (!state) return;


  GeglNode *usethis = state->hardlight; /* the default */
  switch (o->blendmode) {
    case GEGL_BLEND_MODE_TYPE_MULTIPLY: usethis = state->multiply; break;
    case GEGL_BLEND_MODE_TYPE_COLORDODGE: usethis = state->colordodge; break;
    case GEGL_BLEND_MODE_TYPE_PLUS: usethis = state->plus; break;
    case GEGL_BLEND_MODE_TYPE_DARKEN: usethis = state->darken; break;
    case GEGL_BLEND_MODE_TYPE_LIGHTEN: usethis = state->lighten; break;
    case GEGL_BLEND_MODE_TYPE_EMBOSSBLEND: usethis = state->embossblend; break;
default: usethis = state->hardlight;

}


switch (o->switchbevel) {
        break;
    case CLASSIC:
  gegl_node_link_many (state->input,  state->darkbevel, state->nop, state->mcol, state->median, state->box, state->gaussian, usethis, state->opacity, state->mcb, state->sharpen, state->desat, state->multiply2,  state->lightness, state->killpuff, state->repairgeglgraph, state->output,  NULL);
/* Blend emboss with one of many blend modes*/
  gegl_node_connect (usethis, "aux", state->emboss, "output");
  gegl_node_link_many (state->gaussian, state->emboss,  NULL);
/* Blend color overlay with multiply*/
  gegl_node_connect (state->mcol, "aux", state->col, "output");
  gegl_node_link_many (state->nop, state->col,  NULL);
/* Blend multiply with image file overlay*/
  gegl_node_connect (state->multiply2, "aux", state->imagefileoverlay, "output");
        break;
    case NO_COLOR_MODERN:
  gegl_node_link_many (state->input, state->bookmark,  state->white, state->multiplybookmark, state->darkbevel, state->median, state->box, state->gaussian, usethis, state->opacity, state->mcb, state->sharpen, state->desat, state->multiply2,  state->lightness,  state->repairgeglgraph, state->killpuff2, state->output,  NULL);
/* Blend emboss with one of many blend modes*/
  gegl_node_connect (usethis, "aux", state->emboss, "output");
  gegl_node_link_many (state->gaussian, state->emboss,  NULL);
/* Blend multiply with image file overlay*/
  gegl_node_connect (state->multiply2, "aux", state->imagefileoverlay, "output");
/* Blend multiply with original image color*/
  gegl_node_connect (state->multiplybookmark, "aux", state->medianbookmark, "output");
  gegl_node_link_many (state->bookmark, state->medianbookmark,  NULL);
        break;
    case COLOR_MODERN:
  gegl_node_link_many (state->input, state->col,  state->darkbevel, state->median, state->box, state->gaussian, usethis, state->opacity, state->mcb, state->sharpen, state->desat, state->multiply2,  state->lightness, state->repairgeglgraph, state->killpuff2,  state->output,  NULL);
/* Blend emboss with one of many blend modes*/
  gegl_node_connect (usethis, "aux", state->emboss, "output");
  gegl_node_link_many (state->gaussian, state->emboss,  NULL);
/* Blend multiply with image file overlay*/
  gegl_node_connect (state->multiply2, "aux", state->imagefileoverlay, "output");
}
 }

static void attach (GeglOperation *operation)
{
  GeglNode *gegl = operation->node;
GeglProperties *o = GEGL_PROPERTIES (operation);
  GeglNode *input, *output, *median, *multiply, *hardlight, *white, *killpuff, *killpuff2,  *embossblend, *colordodge,  *nop2, *darken, *darkbevel, *desat, *multiply2, *lighten, *mcol, *col, *nop, *plus, *opacity, *gaussian, *emboss, *box, *lightness, *imagefileoverlay, *mcb, *sharpen, *bookmark, *medianbookmark, *multiplybookmark, *repairgeglgraph;

  input    = gegl_node_get_input_proxy (gegl, "input");
  output   = gegl_node_get_output_proxy (gegl, "output");


  darkbevel    = gegl_node_new_child (gegl,
                                  "operation", "gegl:levels",
                                  NULL);

  white    = gegl_node_new_child (gegl,
                                  "operation", "gegl:levels", "out-low", 1.0,
                                  NULL);

 bookmark    = gegl_node_new_child (gegl,
                                  "operation", "gegl:nop",
                                  NULL);

  multiplybookmark    = gegl_node_new_child (gegl,
                                  "operation", "gegl:multiply",
                                  NULL);


  medianbookmark    = gegl_node_new_child (gegl,
                                  "operation", "gegl:median-blur", "radius", 30, "alpha-percentile", 100.0,
                                  NULL);


  median    = gegl_node_new_child (gegl,
                                  "operation", "gegl:median-blur",
                                  NULL);


  killpuff    = gegl_node_new_child (gegl,
                                  "operation", "gegl:gegl", "string", GEGLGRAPHSTRING,
                                  NULL);

  killpuff2    = gegl_node_new_child (gegl,
                                  "operation", "gegl:gegl", "string", GEGLGRAPHSTRING2,
                                  NULL);


  nop    = gegl_node_new_child (gegl,
                                  "operation", "gegl:nop",
                                  NULL);

  nop2    = gegl_node_new_child (gegl,
                                  "operation", "gegl:nop",
                                  NULL);


  col   = gegl_node_new_child (gegl,
                                  "operation", "gegl:color-overlay",
                                  NULL);



  gaussian    = gegl_node_new_child (gegl,
                                  "operation", "gegl:gaussian-blur",
                                  NULL);


  emboss    = gegl_node_new_child (gegl,
                                  "operation", "gegl:emboss",
                                  NULL);

  box    = gegl_node_new_child (gegl,
                                  "operation", "gegl:box-blur",
                                  NULL);


  imagefileoverlay    = gegl_node_new_child (gegl,
                                  "operation", "gegl:layer",
                                  NULL);

  lightness    = gegl_node_new_child (gegl,
                                  "operation", "gegl:hue-chroma",
                                  NULL);


  mcb    = gegl_node_new_child (gegl,
                                  "operation", "gegl:mean-curvature-blur",
                                  NULL);

  sharpen    = gegl_node_new_child (gegl,
                                  "operation", "gegl:unsharp-mask",
                                  NULL);

  desat   = gegl_node_new_child (gegl,
                                  "operation", "gegl:saturation",
                                  NULL);


  opacity   = gegl_node_new_child (gegl,
                                  "operation", "gegl:opacity",
                                  NULL);


  multiply    = gegl_node_new_child (gegl,
                                  "operation", "gegl:multiply",
                                  NULL);

  multiply2    = gegl_node_new_child (gegl,
                                  "operation", "gegl:multiply",
                                  NULL);

  hardlight    = gegl_node_new_child (gegl,
                                  "operation", "gegl:hard-light",
                                  NULL);

  colordodge    = gegl_node_new_child (gegl,
                                  "operation", "gegl:color-dodge",
                                  NULL);

  darken    = gegl_node_new_child (gegl,
                                  "operation", "gegl:darken",
                                  NULL);

  lighten    = gegl_node_new_child (gegl,
                                  "operation", "gegl:lighten",
                                  NULL);

  plus    = gegl_node_new_child (gegl,
                                  "operation", "gegl:plus",
                                  NULL);

  mcol   = gegl_node_new_child (gegl,
                                  "operation", "gegl:multiply",
                                  NULL);


  embossblend   = gegl_node_new_child (gegl,
                                  "operation", "gegl:src", 
                                  NULL);


   repairgeglgraph      = gegl_node_new_child (gegl, "operation", "gegl:median-blur",
                                         "radius",       0,
                                         NULL);

  gegl_operation_meta_redirect (operation, "size", median, "radius");
  gegl_operation_meta_redirect (operation, "gaus", gaussian, "std-dev-x");
  gegl_operation_meta_redirect (operation, "gaus", gaussian, "std-dev-y");
  gegl_operation_meta_redirect (operation, "azimuth", emboss, "azimuth");
  gegl_operation_meta_redirect (operation, "elevation", emboss, "elevation");
  gegl_operation_meta_redirect (operation, "depth", emboss, "depth");
  gegl_operation_meta_redirect (operation, "percentile", median, "percentile");
  gegl_operation_meta_redirect (operation, "alphapercentile", median, "alpha-percentile");
  gegl_operation_meta_redirect (operation, "src", imagefileoverlay, "src");
  gegl_operation_meta_redirect (operation, "lightness", lightness, "lightness");
  gegl_operation_meta_redirect (operation, "hue", lightness, "hue");
  gegl_operation_meta_redirect (operation, "opacity", opacity, "value");
  gegl_operation_meta_redirect (operation, "mcb", mcb, "iterations");
  gegl_operation_meta_redirect (operation, "sharpen", sharpen, "scale");
  gegl_operation_meta_redirect (operation, "box", box, "radius");
  gegl_operation_meta_redirect (operation, "type", median, "neighborhood");
  gegl_operation_meta_redirect (operation, "desat", desat, "scale");
  gegl_operation_meta_redirect (operation, "coloroverlay", col, "value");
  gegl_operation_meta_redirect (operation, "slideupblack", darkbevel, "out-low");



  State *state = g_malloc0 (sizeof (State));
  state->input = input;
  state->white = white;
  state->median = median;
  state->box = box;
  state->gaussian = gaussian;
  state->hardlight = hardlight;
  state->multiply = multiply;
  state->colordodge = colordodge;
  state->emboss = emboss;
  state->embossblend = embossblend;
  state->plus = plus;
  state->darken = darken;
  state->lighten = lighten;
  state->opacity = opacity;
  state->mcb = mcb;
  state->sharpen = sharpen;
  state->desat = desat;
  state->multiply2 = multiply2;
  state->nop = nop;
  state->nop2 = nop2;
  state->killpuff = killpuff;
  state->killpuff2 = killpuff2;
  state->mcol = mcol;
  state->col = col;
  state->imagefileoverlay = imagefileoverlay;
  state->lightness = lightness;
  state->repairgeglgraph = repairgeglgraph;
  state->medianbookmark = medianbookmark;
  state->multiplybookmark = multiplybookmark;
  state->bookmark = bookmark;
  state->darkbevel = darkbevel;
  state->output = output;

  o->user_data = state;
}

static void
gegl_op_class_init (GeglOpClass *klass)
{
  GeglOperationClass *operation_class;
GeglOperationMetaClass *operation_meta_class = GEGL_OPERATION_META_CLASS (klass);
  operation_class = GEGL_OPERATION_CLASS (klass);

  operation_class->attach = attach;
  operation_meta_class->update = update_graph;

  gegl_operation_class_set_keys (operation_class,
    "name",        "lb:script-custom-bevel",
    "title",       _("Custom Bevel SCRIPT ONLY"),
    "categories",  "hidden",
    "reference-hash", "scriptonlyefjf25sb2ac",
    "description", _("This is a version of custom bevel that is only meant for scripting with gegl command.py.  A bevel with high customization allowing choice of bevel size, internal blend modes and internal blur types. Different blend modes do different things regarding detail, depth or presence of a shine effect. Options exist to make the bevel box type, thick, or tubular."
                     ""),
    NULL);
}

#endif
