---
draft: true
sidebar_position: 187
slug: /instruments/videomancer/marquee
title: "Marquee"
image: /img/instruments/videomancer/marquee/marquee_hero_s1.png
description: "Before desktop publishing and digital titling systems, television stations used dedicated character generators — standalone hardware boxes that composited text and graphics over live programme video."
---

![Marquee hero image](/img/instruments/videomancer/marquee/marquee_hero_s1.png)
*Marquee compositing a bold outlined title key with drop shadow over live video, recreating broadcast character generator aesthetics.*

---

## Overview

Marquee is a broadcast-style character generator effect that turns luminance contrast into a multi-layered titling composite. Feed it video containing bright shapes on a dark background: text, graphics, or any high-contrast source: and Marquee extracts a binary key, wraps it in a bold colored outline, stamps a drop shadow behind it, and composites the whole stack over the original picture. The result is the unmistakable look of 1970s and 1980s television titles: solid fills, hard outlines, crisp shadows, and a semi-transparent background box, all rendered in real time from nothing but the incoming video signal.

At gentle settings, Marquee adds a clean luminance key with a thin colored border: useful as a practical downstream keyer for titling and overlays. At extreme settings, it transforms any high-contrast footage into psychedelic stained glass, where every bright edge sprouts a halo of saturated color and displaced shadow copies chase each other across the screen.

:::tip
Marquee is a ***processing*** program. It needs a video input with strong luminance contrast to produce visible results. Text generators, graphic cards, high-contrast camera shots, and the output of other Videomancer programs all make excellent sources.
:::

### What's In a Name?

A ***marquee*** is the illuminated sign above a theater entrance: bold lettering outlined in bright lights, announcing the show to passersby. In broadcast television, the term was adopted for electronic ***character generators*** (CGs) that superimposed titles and credits over programme video. Marquee recreates that process entirely inside the FPGA, extracting titles from the video itself and dressing them up with the full CG treatment: colored fills, bold outlines, drop shadows, and background boxes.

---

## Quick Start

1. Feed a source with bright shapes on a dark background. Adjust **Key Level** (Knob 1) until the bright areas cleanly separate from the dark areas: you should see solid colored shapes appear where the bright content was.
2. Turn **Outline Width** (Knob 2) clockwise. A bold colored border grows around the edges of each keyed shape. The outline color is set by **Outline Hue** (Knob 4).
3. With **Shadow** (Switch 8) set to **On**, increase **Shadow Offset** (Knob 5). A dark displaced copy of each shape slides to the right, appearing behind the fill (just like a drop shadow in a graphics program.)
4. Toggle **Box** (Switch 9) to **On**. A semi-transparent darkened region appears behind the title area, improving legibility over busy video backgrounds.

---

## Parameters

![Videomancer front panel with Marquee loaded](/img/instruments/videomancer/marquee/marquee_control_panel.png)
*Videomancer's front panel with Marquee active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Key Level

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Key Level** sets the luminance threshold that separates "title" from "background." Every pixel whose gained brightness exceeds this threshold becomes part of the key; everything below it is treated as background video. At 0%, fully counterclockwise, even very dim pixels pass the threshold, and almost the entire image is keyed. As the value increases toward 100%, the threshold rises, and only the brightest areas of the image survive as key regions. Finding the right Key Level for your source is the first step in setting up a clean composite.

:::note
Key Level works together with **Key Gain** (Knob 6). If your source doesn't have enough contrast to produce a clean key, increase Key Gain to boost the luminance before it reaches the threshold. The two controls together give you precise control over key extraction.
:::

---

### Knob 2 — Outline Width

| Property | Value |
|----------|-------|
| Range | 0 – 7 |
| Default | 3 |

**Outline Width** controls the thickness of the colored border drawn around the edges of keyed shapes. The control is quantized into eight discrete steps, from 0 (no outline) to 7 (maximum thickness). At step 0, no outline is drawn and only the fill and shadow layers are visible. Each step adds approximately one pixel of ***dilation*** to the detected edges, making the border progressively bolder. Edge detection operates in both horizontal and vertical directions, so the outline surrounds the entire perimeter of each keyed shape.

---

### Knob 3 — Fill Hue

| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 60° |

**Fill Hue** selects the color used to fill the interior of keyed shapes when **Fill Mode** (Switch 7) is set to **Color**. The knob sweeps through six saturated hue sectors: red, yellow, green, cyan, blue, and magenta: plus a neutral white at the far end of the range. The fill is rendered at a bright, constant luminance level, giving titles a solid, opaque appearance.

:::tip
When **Fill Mode** is set to **Video**, this control has no visible effect: the original video passes through inside the keyed region instead.
:::

---

### Knob 4 — Outline Hue

| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |

**Outline Hue** selects the color of the outline border, independently of the fill color. It sweeps through the same six hue sectors as **Fill Hue**: red, yellow, green, cyan, blue, and magenta: plus neutral white. The outline is rendered at a slightly lower luminance than the fill, creating a subtle tonal distinction between the border and the interior even when both are set to similar hues.

---

### Knob 5 — Shadow Offset

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |

**Shadow Offset** controls how far the drop shadow is displaced from the keyed shape. At 0%, fully counterclockwise, the shadow sits directly behind the title and is invisible. As the value increases, the shadow slides to the right by up to 15 pixels. The shadow also has a one-line vertical displacement, giving a slight diagonal drop. The shadow is rendered as a very dark, desaturated copy of the key shape: it appears only where the shadow falls outside the fill region, so the title itself is never obscured.

---

### Knob 6 — Key Gain

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Key Gain** applies a contrast boost to the luminance signal before it reaches the **Key Level** threshold. At 50%, the gain is unity: the luminance passes through unchanged. Below 50%, the gain is reduced, making it harder for pixels to exceed the threshold. Above 50%, the gain is amplified, pushing more of the image above the threshold and creating a broader, more aggressive key. Key Gain is especially useful for sources with low contrast, where the natural luminance difference between title and background isn't sufficient for a clean key extraction.

---

### Switch 7 — Fill Mode

| Property | Value |
|----------|-------|
| Off | Color |
| On | Video |
| Default | Color |

**Fill Mode** selects what appears inside the keyed region. When set to **Color**, the keyed area is filled with a solid color chosen by **Fill Hue** (Knob 3): this is the classic character generator look. When set to **Video**, the original input video passes through unchanged inside the keyed region, and only the outline and shadow layers are added around it. Video mode is useful for creating outlined, shadowed versions of the source content without replacing its interior.

---

### Switch 8 — Shadow

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Shadow** enables or disables the drop shadow layer. When set to **On**, a dark displaced copy of the key appears behind the fill, offset to the right by the amount set with **Shadow Offset** (Knob 5). When set to **Off**, no shadow is drawn, and the compositor skips directly from the fill layer to the box or background video.

---

### Switch 9 — Box

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Box** enables or disables the background box layer. When set to **On**, any scan line that contains at least one keyed pixel is dimmed to 50% brightness, creating a semi-transparent darkened strip behind the title area. The box improves legibility when compositing titles over busy or bright video backgrounds. When set to **Off**, background video passes through at full brightness.

:::note
The box region is detected per scan line: it activates on any line where key pixels are present. This means the box hugs the vertical extent of the title content automatically.
:::

---

### Switch 10 — Invert Key

| Property | Value |
|----------|-------|
| Off | Norm |
| On | Inv |
| Default | Norm |

**Invert Key** reverses the polarity of the binary key signal. When set to **Norm**, bright areas of the source become the fill and dark areas become the background: the standard character generator behavior. When set to **Inv**, the relationship flips: dark areas become the fill, and bright areas become the background. Inversion happens immediately after threshold comparison and before all downstream layers (outline, shadow, box), so the entire composite inverts.

---

### Switch 11 — Outline Only

| Property | Value |
|----------|-------|
| Off | Full |
| On | Outl |
| Default | Full |

**Outline Only** removes the fill layer from the composite, leaving only the outline border visible over the background video. When set to **Full**, both the outline and the fill are drawn (the normal CG look). When set to **Outl**, the fill is suppressed, and only the edge outline and shadow remain. This creates a wireframe or neon-sign aesthetic where shapes are defined solely by their contours.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (unprocessed) input and the wet (composited) output. At 0%, fully down, the output is the original video with no Marquee processing. At 100%, fully up, the output is the full composite. Intermediate values blend between the two, allowing you to dial in the intensity of the effect or create transparent overlay composites.

---

## Background

### Character generators and downstream keying

In broadcast television, a ***character generator*** (or CG) is a device that superimposes text and graphics over live video. Early CGs were dedicated hardware boxes: often costing more than the cameras: that generated title cards electronically and keyed them over the programme signal using a ***downstream keyer***. The downstream keyer sits at the very end of the video chain, after all switching and effects, so titles appear on top of everything.

Marquee recreates this process inside the FPGA. Instead of generating its own text, it extracts title-like shapes from the incoming video signal using ***luminance keying***: a technique where brightness is used to separate foreground from background. Any bright shape on a dark field becomes a "title" that Marquee can dress up with the full CG treatment.

### Luminance keying

***Luminance keying*** (also called ***luma keying***) is the simplest form of video keying. A threshold divides the luminance range into two zones: pixels above the threshold are "foreground" and pixels below are "background." The result is a binary mask: a 1-bit image where each pixel is either fully keyed or fully transparent.

Marquee adds a ***gain*** stage before the threshold. The gain multiplies the luminance, spreading the contrast range so that even low-contrast sources can produce a clean, hard-edged key. The combination of gain and threshold gives you a two-parameter key extraction system: gain controls *how much* contrast you have to work with, and threshold controls *where* the cut falls.

### Edge detection and dilation

Once the binary key is extracted, Marquee detects its edges by comparing each pixel to its neighbors. ***Horizontal edges*** are found by XOR-ing the current key value with a delayed copy of itself: wherever the key changes from 0 to 1 or 1 to 0, the XOR produces a 1. ***Vertical edges*** are found the same way, but comparing the current line to the previous line stored in block RAM.

The raw edge signal is then ***dilated***: thickened: by OR-ing it with its neighboring samples across a shift register. The **Outline Width** control sets how many neighboring samples are included, producing outlines from one pixel thin to several pixels bold. This is the same morphological dilation operation used in image processing, implemented here in a single clock cycle using combinational logic.

### Drop shadows

The drop shadow is a displaced copy of the binary key, shifted to the right by a variable number of pixels. The displacement is achieved by reading from a horizontal shift register at a tap selected by the **Shadow Offset** control. The shadow also includes a one-line vertical offset from block RAM, giving a slight diagonal displacement.

Crucially, the shadow is rendered only where it falls *outside* the fill region. The compositor masks the shadow with the inverse of the current key, so the title itself is never darkened: the shadow appears exclusively in the space behind and beside the title, just as it would in a real graphics program.


---

## Signal Flow

### Signal Flow Notes

The compositor is a strict priority stack. Each pixel is assigned to exactly one layer based on the first condition that matches, evaluated top to bottom: outline, fill, shadow, box, video. This means the outline always wins: it paints over everything, including the fill. The fill paints over the shadow. And the shadow paints over the box and the background video, but never over the fill or outline.

The shadow masking logic (`shadow AND NOT fill_key`) is what makes the compositor look correct. Without it, the shadow would darken the interior of the title wherever it overlaps: destroying the clean, bright fill. With the mask, the shadow only appears in the gap between the title edge and its displaced copy, exactly as expected.

:::tip
**Box region detection is line-based.** The box activates on any scan line where at least one key pixel was detected on the *previous* line. This one-line delay means the box extends slightly beyond the bottom of the title content.
:::


---

## Exercises

These exercises progress from basic key extraction to full broadcast-style compositing, building up the layer stack one feature at a time.
### Exercise 1: Clean Title Key

![Clean Title Key result](/img/instruments/videomancer/marquee/marquee_ex1_s1.png)
*Clean Title Key — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A clean, outlined title composite over live video (the fundamental character generator look.)

#### Key Concepts

- Luminance keying separates bright foreground from dark background
- Key Gain and Key Level work together to control key extraction
- The outline adds a colored border around keyed shapes

#### Video Source

A graphic card, text generator, or camera shot of white text or shapes on a black background.

#### Steps

1. **Extract the key**: Feed your source and adjust **Key Level** (Knob 1) until the bright shapes cleanly separate. You should see the shapes filled with a solid color (the default Fill Hue).
2. **Refine the key**: If the edges are rough or the key is incomplete, increase **Key Gain** (Knob 6) to boost contrast before the threshold.
3. **Add an outline**: Turn **Outline Width** (Knob 2) clockwise to step 3 or 4. A colored border appears around each shape.
4. **Color the outline**: Sweep **Outline Hue** (Knob 4) to find a contrasting color for the border. Try a complementary hue to the fill.
5. **Color the fill**: Sweep **Fill Hue** (Knob 3) to choose the interior color of the title shapes.

#### Settings

| Control | Value |
|---------|-------|
| Key Level | ~50% |
| Outline Width | 3 |
| Fill Hue | 180° |
| Outline Hue | 0° |
| Shadow Offset | 0% |
| Key Gain | ~50% |
| Fill Mode | Color |
| Shadow | Off |
| Box | Off |
| Invert Key | Norm |
| Outline Only | Full |
| Mix | 100% |

---

### Exercise 2: Broadcast Composite

![Broadcast Composite result](/img/instruments/videomancer/marquee/marquee_ex2_s1.png)
*Broadcast Composite — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A full broadcast-style title composite with shadow, box, and colored layers (the complete 1970s CG look.)

#### Key Concepts

- Drop shadows improve legibility by creating depth
- The background box dims video behind the title area
- Layer priority ensures each element composites correctly

#### Video Source

Live camera footage or recorded video with recognizable content, plus a title source (text generator, graphic card, or high-contrast overlay).

#### Steps

1. **Start with a clean key**: Set up **Key Level** and **Key Gain** for a solid key, as in Exercise 1.
2. **Enable the shadow**: Set **Shadow** (Switch 8) to **On**. Increase **Shadow Offset** (Knob 5) to about 40%. A dark copy of each shape appears displaced to the right.
3. **Enable the box**: Set **Box** (Switch 9) to **On**. A semi-transparent darkened strip appears behind the title area, improving legibility.
4. **Add a bold outline**: Set **Outline Width** (Knob 2) to step 5 or 6 for a thick border.
5. **Choose broadcast colors**: Set **Fill Hue** (Knob 3) to a warm yellow or white. Set **Outline Hue** (Knob 4) to a dark blue or black. This classic combination is instantly recognizable as a broadcast title.
6. **Dial the mix**: Lower **Mix** (Fader 12) to about 80% to let a hint of the background video show through the composite layers.

#### Settings

| Control | Value |
|---------|-------|
| Key Level | ~50% |
| Outline Width | 5 |
| Fill Hue | 60° |
| Outline Hue | 240° |
| Shadow Offset | ~40% |
| Key Gain | ~50% |
| Fill Mode | Color |
| Shadow | On |
| Box | On |
| Invert Key | Norm |
| Outline Only | Full |
| Mix | ~80% |

---

### Exercise 3: Neon Wireframe

![Neon Wireframe result](/img/instruments/videomancer/marquee/marquee_ex3_s1.png)
*Neon Wireframe — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A glowing wireframe contour effect where shapes are defined only by their colored outlines: no fill, no shadow, just luminous edges floating over the video.

#### Key Concepts

- Outline Only mode removes the fill, leaving just edge contours
- Invert Key reverses which areas are treated as foreground
- Combining inversion with outline-only creates a neon-sign aesthetic

#### Video Source

A camera shot or recorded footage with strong edges and varied shapes: architecture, plant silhouettes, or a face with dramatic lighting.

#### Steps

1. **Set up the key**: Adjust **Key Level** (Knob 1) and **Key Gain** (Knob 6) to extract the major shapes from your source. Don't worry about a perfect key (rough edges create more interesting contours.)
2. **Remove the fill**: Set **Outline Only** (Switch 11) to **Outl**. The solid fill disappears, leaving only the outline border.
3. **Maximize the outline**: Set **Outline Width** (Knob 2) to step 6 or 7 for the thickest possible contour lines.
4. **Disable the shadow**: Set **Shadow** (Switch 8) to **Off** for a cleaner wireframe look.
5. **Choose a neon color**: Set **Outline Hue** (Knob 4) to a vivid hue (magenta, cyan, or green work well for a neon aesthetic.)
6. **Invert the key**: Toggle **Invert Key** (Switch 10) to **Inv**. The contour lines now trace the dark areas instead of the bright areas, often revealing an entirely different set of edges.
7. **Experiment**: Slowly sweep **Key Level** to shift which contours are visible. The wireframe traces different depth layers of the image as the threshold moves.

#### Settings

| Control | Value |
|---------|-------|
| Key Level | ~30% |
| Outline Width | 7 |
| Fill Hue | 0° |
| Outline Hue | 180° |
| Shadow Offset | 0% |
| Key Gain | ~60% |
| Fill Mode | Color |
| Shadow | Off |
| Box | Off |
| Invert Key | Inv |
| Outline Only | Outl |
| Mix | 100% |

---
## Glossary

- **Character Generator (CG)**: A device that creates text and graphic overlays for television, superimposed over the programme video signal.

- **Dilation**: A morphological operation that thickens edges by OR-ing each pixel with its neighbors across a shift register.

- **Downstream Keyer**: A keying stage positioned after all other video switching and effects, used for titles and lower-third graphics.

- **Drop Shadow**: A dark, displaced copy of a shape rendered behind it to simulate depth and improve legibility against busy backgrounds.

- **Edge Detection**: Identifying boundaries between keyed and un-keyed regions by comparing adjacent pixels (horizontal) or adjacent lines (vertical) via XOR.

- **Luminance Key**: A keying technique that uses brightness to separate foreground from background, producing a binary mask from a threshold comparison.

- **Pipeline**: A sequence of processing stages where each stage completes in one clock cycle, allowing data to flow through continuously.

- **Priority Compositor**: A layering system where each pixel is assigned to the first matching layer in a fixed priority order.

- **Shift Register**: A chain of flip-flops where data advances one position per clock cycle, used here for edge detection, dilation, and shadow displacement.

---
