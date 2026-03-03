---
draft: true
sidebar_position: 186
slug: /instruments/videomancer/marquee
title: "Marquee"
image: /img/instruments/videomancer/marquee/marquee_hero_s1.png
description: "Before desktop publishing and digital titling systems, television stations used dedicated character generators — standalone hardware boxes that composited text and graphics over live programme video."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import marquee_source1_fruit from '/img/instruments/videomancer/marquee/marquee_source1_fruit.png';
import marquee_source2_ballerina from '/img/instruments/videomancer/marquee/marquee_source2_ballerina.png';
import marquee_source3_turtle from '/img/instruments/videomancer/marquee/marquee_source3_turtle.png';
import marquee_source4_pattern from '/img/instruments/videomancer/marquee/marquee_source4_pattern.png';
import marquee_source5_boy from '/img/instruments/videomancer/marquee/marquee_source5_boy.png';
import marquee_source6_wood from '/img/instruments/videomancer/marquee/marquee_source6_wood.png';
import marquee_hero_s1 from '/img/instruments/videomancer/marquee/marquee_hero_s1.png';
import marquee_hero_s2 from '/img/instruments/videomancer/marquee/marquee_hero_s2.png';
import marquee_hero_s3 from '/img/instruments/videomancer/marquee/marquee_hero_s3.png';
import marquee_hero_s4 from '/img/instruments/videomancer/marquee/marquee_hero_s4.png';
import marquee_hero_s5 from '/img/instruments/videomancer/marquee/marquee_hero_s5.png';
import marquee_hero_s6 from '/img/instruments/videomancer/marquee/marquee_hero_s6.png';
import marquee_ex1_s1 from '/img/instruments/videomancer/marquee/marquee_ex1_s1.png';
import marquee_ex1_s2 from '/img/instruments/videomancer/marquee/marquee_ex1_s2.png';
import marquee_ex1_s3 from '/img/instruments/videomancer/marquee/marquee_ex1_s3.png';
import marquee_ex1_s4 from '/img/instruments/videomancer/marquee/marquee_ex1_s4.png';
import marquee_ex1_s5 from '/img/instruments/videomancer/marquee/marquee_ex1_s5.png';
import marquee_ex1_s6 from '/img/instruments/videomancer/marquee/marquee_ex1_s6.png';
import marquee_ex2_s1 from '/img/instruments/videomancer/marquee/marquee_ex2_s1.png';
import marquee_ex2_s2 from '/img/instruments/videomancer/marquee/marquee_ex2_s2.png';
import marquee_ex2_s3 from '/img/instruments/videomancer/marquee/marquee_ex2_s3.png';
import marquee_ex2_s4 from '/img/instruments/videomancer/marquee/marquee_ex2_s4.png';
import marquee_ex2_s5 from '/img/instruments/videomancer/marquee/marquee_ex2_s5.png';
import marquee_ex2_s6 from '/img/instruments/videomancer/marquee/marquee_ex2_s6.png';
import marquee_ex3_s1 from '/img/instruments/videomancer/marquee/marquee_ex3_s1.png';
import marquee_ex3_s2 from '/img/instruments/videomancer/marquee/marquee_ex3_s2.png';
import marquee_ex3_s3 from '/img/instruments/videomancer/marquee/marquee_ex3_s3.png';
import marquee_ex3_s4 from '/img/instruments/videomancer/marquee/marquee_ex3_s4.png';
import marquee_ex3_s5 from '/img/instruments/videomancer/marquee/marquee_ex3_s5.png';
import marquee_ex3_s6 from '/img/instruments/videomancer/marquee/marquee_ex3_s6.png';

# Marquee

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: marquee_source1_fruit, after: marquee_hero_s1 },
    { label: "Ballerina", before: marquee_source2_ballerina, after: marquee_hero_s2 },
    { label: "Turtle", before: marquee_source3_turtle, after: marquee_hero_s3 },
    { label: "Pattern", before: marquee_source4_pattern, after: marquee_hero_s4 },
    { label: "Boy", before: marquee_source5_boy, after: marquee_hero_s5 },
    { label: "Wood", before: marquee_source6_wood, after: marquee_hero_s6 },
  ]}
/>
*Marquee compositing bold colored titles with outlines and drop shadows over programme video, recreating the broadcast character generator aesthetic of 1970s television.*

---

## Overview

Before desktop publishing and digital titling systems, television stations used dedicated **character generators** — standalone hardware boxes that composited text and graphics over live programme video. The operator typed a title, chose a fill color and outline style, and the character generator keyed it over whatever the camera was showing. The result was bold, graphic, and immediately recognizable: solid colored text, a hard contrasting outline, a dark drop shadow offset a few pixels to the right, and sometimes a translucent background box to improve readability over busy video.

Marquee recreates this entire compositing chain in a single FPGA program. It extracts a binary key signal from input luminance, detects edges to create a multi-pixel outline, generates a displaced drop shadow, and composites five layers in strict priority order: outline, fill, shadow, box, and passthrough video. Feed it any high-contrast source — text overlays, graphic mattes, or even camera footage of physical lettering — and it will treat the bright regions as "foreground" and build a complete broadcast titling treatment around them.

The name references the marquee signs of theaters and cinemas — illuminated letter displays with bold outlines and dramatic shadows. At conservative settings, Marquee produces clean, professional lower-thirds. At extreme settings — wide outlines, strong shadows, inverted keys — it becomes an aggressive graphic design tool that fragments the source into pop-art layers of color and shadow.

---

## Background

### Luminance Keying

All compositing begins with a **key signal** — a binary mask that separates foreground from background. Marquee extracts its key from luminance: every pixel brighter than the Key Level threshold becomes foreground (key=1), everything else becomes background (key=0). This is the same principle used in chroma keyers, but operating on brightness rather than color. Key Gain applies a pre-threshold contrast multiplication so that even low-contrast sources can produce a clean binary key.

### Edge Detection and Dilation

To create an outline, Marquee detects the boundaries of the key signal using XOR-based edge detection — comparing each pixel to its horizontal neighbor (via a shift register) and to the corresponding pixel from the previous scan line (via BRAM). Wherever the key transitions between 0 and 1, an edge is flagged. The Outline Width control then **dilates** this edge by OR-ing adjacent edge samples from a shift register, thickening the outline from a single pixel to up to 7 pixels wide.

### Drop Shadows in Hardware

A drop shadow is nothing more than a displaced copy of the key signal. Marquee creates horizontal shadow displacement by reading from a shift register at an offset determined by the Shadow Offset control. Vertical displacement uses a second BRAM that stores one scan line of key data, providing a one-line vertical offset. The shadow layer is visible only where the shadow key is active but the fill key is *not* — the shadow appears behind the title, never inside it.

### Priority Compositing

Television compositing hardware uses **priority layers** — a strict top-to-bottom ordering where the first active layer wins. Marquee implements five priority layers: (1) the bold colored outline, (2) the fill region (solid color or video passthrough), (3) the drop shadow (dark and neutral), (4) the background box (50% dimmed video), and (5) the original passthrough video. At each pixel, the compositor checks layers in order and outputs the first one whose key condition is met.

### Hue Sector Mapping

Rather than a continuous color space, Marquee maps hue controls to six saturated primary and secondary colors plus white, using the top three bits of the 10-bit register. The six sectors are red, yellow, green, cyan, blue, and magenta — the same six colors used in broadcast color bar test patterns. This quantized approach gives instant access to bold, recognizable broadcast colors without the complexity of continuous hue rotation.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Key Gain Multiply ─────────────────────────────────
│   └─ y_gained = clamp(Y × key_gain >> 9)  [gain=512 = unity]
│
├── Stage 2: Threshold + BRAM ──────────────────────────────────
│   ├─ key_raw = (y_gained > key_threshold) XOR invert_key
│   ├─ Write key_raw → key_line BRAM[h_count]
│   ├─ Write key_raw → shadow_line BRAM[h_count]
│   ├─ Read key_prev_line ← key_line BRAM[h_count]
│   ├─ Read shadow_key_v ← shadow_line BRAM[h_count]
│   ├─ Shift key_raw → key_h_history[7:0]
│   └─ Shift key_raw → shadow_h_hist[15:0]
│
├── Stage 3: Edge Detection + Dilation ─────────────────────────
│   ├─ h_edge = key XOR key_h_history[outline_width-1]
│   ├─ v_edge = key XOR key_prev_line
│   ├─ outline_raw = h_edge OR v_edge
│   ├─ Dilate: OR adjacent outline samples (0..outline_width)
│   └─ shadow_key_h = shadow_h_hist[shadow_h_idx-1]
│
├── Stage 4: Layer Priority Compositor ─────────────────────────
│   ├─ Layer 1 (top): Outline → outline_color (Y=640 + hue UV)
│   ├─ Layer 2: Fill key → fill_color (Y=768 + hue UV) or video
│   ├─ Layer 3: Shadow → dark (Y=64, neutral UV)
│   ├─ Layer 4: Box → 50% dimmed video
│   └─ Layer 5 (bottom): Original video passthrough
│
├── Interpolator (4 clk) ──────────────────────────────────────
│   └─ Mix: lerp(dry_input, wet_composite, mix_amount)
│
└── Output ─────────────────────────────────────────────────────
    └─ data_out.y / u / v + delayed sync
```

The critical interaction is between the key extraction and the multi-layer compositor. The key gain multiply runs *before* thresholding, so adjusting Key Gain changes which pixels cross the threshold without moving the threshold itself — this is how you clean up marginal keys from low-contrast sources. The outline and shadow layers are both derived from the same binary key signal but displaced differently: outlines use XOR edge detection followed by OR dilation, while shadows use pure shift-register displacement. The shadow is masked by the fill key so it only appears *behind* the foreground, never overlapping it.

---

## Parameter Reference


### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Key Level
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Sets the luminance threshold for binary key extraction. Every pixel whose gained luminance exceeds this level becomes foreground. At low values, nearly the entire image becomes keyed — useful when the source is a dark graphic on a black background. At high values, only the brightest highlights survive. For clean title keying, set this just below the luminance of your text while above the luminance of the background.

---

#### Knob 2 — Outline Width
| Property | Value |
|----------|-------|
| Range | 0 – 7 |
| Default | 3 |

Controls the outline width in pixels. The top 3 bits of the register select 8 discrete widths from 0 (no outline) to 7 pixels. The outline is created by XOR edge detection of the key boundary followed by OR dilation across adjacent samples. At width 0, no outline appears. At width 7, the outline is bold enough to serve as the primary visual element — set Outline Only mode and the title becomes a wireframe rendering of its edges.

---

#### Knob 3 — Fill Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 60° |
| Suffix | ° |

Selects the fill color hue from six broadcast primary/secondary colors plus white. The top 3 bits address a piecewise lookup: red (0°), yellow (60°), green (120°), cyan (180°), blue (240°), magenta (300°), and white (above 300°). The fill appears at full brightness (Y=768) inside the keyed region when Fill Mode is set to Color. When Fill Mode is Video, this control has no effect — the original video shows through instead.

---

#### Knob 4 — Outline Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Selects the outline color hue using the same six-sector mapping as Fill Hue. The outline renders at slightly lower brightness (Y=640) than the fill (Y=768), creating a subtle depth distinction between the two layers. Choose a contrasting hue for maximum readability — yellow fill with blue outline, or white fill with red outline, for example.

---

#### Knob 5 — Shadow Offset
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Controls the horizontal displacement of the drop shadow in pixels. The top 4 bits of the register select offsets from 0 to 15 pixels. Vertical shadow displacement is fixed at one scan line, derived from the shadow BRAM. At zero offset, the shadow sits directly behind the text and is invisible. At moderate offsets (4–8 pixels), the shadow creates a classic broadcast lower-third depth effect. At maximum offset, the shadow detaches noticeably from the text.

---

#### Knob 6 — Key Gain
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Pre-threshold contrast boost applied to the luminance channel before key extraction. At 512 (center), the gain is unity — the raw input luminance is compared against the threshold unchanged. Below 512, the gain attenuates and fewer pixels cross the threshold. Above 512, the gain amplifies and more pixels are keyed. Use this to compensate for low-contrast input sources without adjusting the threshold itself.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Fill Mode** | Color | Video |
| **8 — Shadow** | Off | On |
| **9 — Box** | Off | On |
| **10 — Invert Key** | Norm | Inv |
| **11 — Outline Only** | Full | Outl |

The five toggles each control a distinct compositing behavior. Fill Mode and Shadow are the primary creative toggles — switching between solid color fills and video passthrough, and enabling or disabling the drop shadow layer. Box adds a translucent background for readability. Invert Key reverses which parts of the image are treated as foreground. Outline Only strips away the fill and shadow, leaving just the edge contour. Note that there is no bypass toggle — set Mix to 0% to pass the original signal through unchanged.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfades between the original dry input and the wet composited output. At 0%, the output is 100% dry — effectively bypassing all processing. At 100%, the output is fully wet — the complete five-layer composite. Intermediate values blend the two, creating a semi-transparent overlay effect where the title compositing fades over the original video. Since there is no dedicated bypass toggle, this fader is the primary bypass control.

---

## Guided Exercises

These exercises progress from basic key extraction to full broadcast-style title compositing, using increasingly complex layer combinations.

### Exercise 1: Clean Title Key

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: marquee_source1_fruit, after: marquee_ex1_s1 },
    { label: "Ballerina", before: marquee_source2_ballerina, after: marquee_ex1_s2 },
    { label: "Turtle", before: marquee_source3_turtle, after: marquee_ex1_s3 },
    { label: "Pattern", before: marquee_source4_pattern, after: marquee_ex1_s4 },
    { label: "Boy", before: marquee_source5_boy, after: marquee_ex1_s5 },
    { label: "Wood", before: marquee_source6_wood, after: marquee_ex1_s6 },
  ]}
/>
*Clean Title Key — simulated result across source images.*
**Source**: High-contrast text or graphics on a dark background — a title card, text overlay, or white lettering on black.

**Objective**: Learn to extract a clean binary key and apply a solid colored fill with an outline.

1. **Set key threshold**: With the source displayed, slowly increase Key Level until the text is cleanly keyed — foreground white, background removed.
2. **Adjust gain**: If the key is noisy, increase Key Gain slightly above center to boost the contrast before thresholding.
3. **Choose fill color**: Set Fill Hue to select a broadcast color — try yellow (60°) for classic title card feel.
4. **Add outline**: Increase Outline Width to 3–4 pixels. Set Outline Hue to a contrasting color — blue (240°) works well against yellow.
5. **Compare**: Sweep Mix from 0% to 100% to see the composited title build up over the source.

**Key concepts**: Luminance keying extracts foreground from brightness, key gain compensates for low-contrast sources, outline is created by edge detection and dilation

---

### Exercise 2: Broadcast Lower-Third

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: marquee_source1_fruit, after: marquee_ex2_s1 },
    { label: "Ballerina", before: marquee_source2_ballerina, after: marquee_ex2_s2 },
    { label: "Turtle", before: marquee_source3_turtle, after: marquee_ex2_s3 },
    { label: "Pattern", before: marquee_source4_pattern, after: marquee_ex2_s4 },
    { label: "Boy", before: marquee_source5_boy, after: marquee_ex2_s5 },
    { label: "Wood", before: marquee_source6_wood, after: marquee_ex2_s6 },
  ]}
/>
*Broadcast Lower-Third — simulated result across source images.*
**Source**: A title card or graphic overlaid on live camera footage — any high-contrast text over a scene.

**Objective**: Build a complete broadcast lower-third with fill, outline, shadow, and background box.

1. **Start from Exercise 1**: Use the clean key settings from Exercise 1 as a starting point.
2. **Enable shadow**: Toggle Shadow to On. Set Shadow Offset to about 5 pixels (30%). Watch the dark shadow appear offset from the title.
3. **Enable box**: Toggle Box to On. A translucent dimmed background appears behind text lines, improving readability over busy video.
4. **Refine colors**: Experiment with Fill Hue and Outline Hue combinations — white fill with red outline is another classic broadcast look.
5. **Adjust outline width**: Try width 2 for a subtle professional look, or width 6 for bold impact graphics.

**Key concepts**: Drop shadows create depth by displacement of the key, background boxes improve readability, priority compositing stacks layers in a fixed order

---

### Exercise 3: Wireframe Edge Graphics

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: marquee_source1_fruit, after: marquee_ex3_s1 },
    { label: "Ballerina", before: marquee_source2_ballerina, after: marquee_ex3_s2 },
    { label: "Turtle", before: marquee_source3_turtle, after: marquee_ex3_s3 },
    { label: "Pattern", before: marquee_source4_pattern, after: marquee_ex3_s4 },
    { label: "Boy", before: marquee_source5_boy, after: marquee_ex3_s5 },
    { label: "Wood", before: marquee_source6_wood, after: marquee_ex3_s6 },
  ]}
/>
*Wireframe Edge Graphics — simulated result across source images.*
**Source**: Camera footage of physical objects or people — anything with strong brightness contrast and recognizable contours.

**Objective**: Use Outline Only mode and inverted keying to create abstract edge-contour graphics from camera footage.

1. **Enable outline only**: Toggle Outline Only to Outl. The fill, shadow, and box layers disappear — only the outline contour remains.
2. **Set wide outline**: Increase Outline Width to 6–7 for bold contour lines.
3. **Lower key threshold**: Reduce Key Level until contour edges appear tracing the major brightness transitions in the source.
4. **Boost key gain**: Increase Key Gain to amplify subtle edges, bringing more contour detail into the outline.
5. **Invert the key**: Toggle Invert Key to Inv. The edge contours wrap around the dark regions instead of the bright ones, revealing a different structural reading of the image.
6. **Choose outline color**: Set Outline Hue to green (120°) for a scope-like wireframe appearance, or cyan (180°) for a blueprint aesthetic.

**Key concepts**: Outline Only mode isolates edge detection from fill compositing, inverted keying reverses which structures generate contours, wider dilation creates bolder contour graphics

---


## Tips

- **No bypass toggle**: Unlike most programs, Marquee uses Toggle 11 for Outline Only instead of bypass. Set the Mix fader to 0% for instant A/B comparison with the unprocessed source.
- **Key Gain before threshold**: If your source is low-contrast, boost Key Gain rather than lowering Key Level. Gain amplifies before thresholding, producing a cleaner binary key with less noise.
- **Contrasting colors**: Choose Fill Hue and Outline Hue from opposite sides of the color wheel for maximum readability — yellow fill with blue outline, or white fill with red outline.
- **Shadow direction**: The shadow always displaces to the right (positive horizontal offset) and one line down. For a different shadow position, pre-process the input with a flip or rotation program upstream.
- **Outline Only as a key source**: Use Outline Only mode to generate clean edge contour graphics, then feed the output to a downstream keyer or compositor as a matte source.
- **Box for readability**: The background box is invaluable when compositing titles over busy or unpredictable live footage — it creates a consistent dark band behind the text regardless of the background content.
- **Invert Key for negatives**: When working with inverted or negative source material, toggle Invert Key to swap the foreground/background assignment without adjusting threshold or gain.
- **Feedback compositing**: Route the output back to the input for layered shadow accumulation — each pass adds another offset shadow, creating a cascading depth effect.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; dedicated memory within the FPGA used to store one scan line of key data for vertical edge detection and shadow displacement. |
| **Character Generator** | Dedicated broadcast hardware for compositing text and graphics over live video, widely used in television from the 1970s onward. |
| **Compositor** | A priority-based layer system that combines multiple visual elements (fill, outline, shadow, box, video) into a single output frame. |
| **Dilation** | Expanding a binary mask by OR-ing adjacent samples, used here to thicken the outline edge from a single pixel to multiple pixels. |
| **Drop Shadow** | A displaced dark copy of a foreground element, creating the illusion of depth by simulating a shadow cast onto the background. |
| **Edge Detection** | Identifying boundaries in a binary signal by comparing adjacent samples (XOR); transitions between 0 and 1 produce an edge flag. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Key Signal** | A binary mask (0 or 1 per pixel) that separates foreground from background for compositing. |
| **Lower-Third** | A title or graphic overlay positioned in the lower portion of the screen, commonly used for name identifications in broadcast television. |
| **Luminance** | The brightness component (Y) of a YUV video signal. |
| **Pipeline** | Sequential processing stages where each stage's output feeds the next on every clock cycle. |
| **Priority Compositing** | A compositing method where layers are evaluated top-to-bottom and the first active layer determines the output pixel color. |
| **Shift Register** | A chain of flip-flops that delays a signal by a programmable number of clock cycles, used for horizontal displacement and edge detection. |
| **YUV** | A color encoding separating luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
