---
draft: true
sidebar_position: 101
slug: /instruments/videomancer/encore
title: "Encore"
image: /img/instruments/videomancer/encore/encore_hero_s1.png
description: "Broadcast television invented picture-in-picture to show two things at once — a sports score ticker floating over live action, a news anchor inset against a remote feed."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import encore_control_panel from '/img/instruments/videomancer/encore/encore_control_panel.png';
import encore_source1_ballerina from '/img/instruments/videomancer/encore/encore_source1_ballerina.png';
import encore_source2_boat from '/img/instruments/videomancer/encore/encore_source2_boat.png';
import encore_source3_turtle from '/img/instruments/videomancer/encore/encore_source3_turtle.png';
import encore_source4_pattern from '/img/instruments/videomancer/encore/encore_source4_pattern.png';
import encore_source5_girl from '/img/instruments/videomancer/encore/encore_source5_girl.png';
import encore_source6_wood from '/img/instruments/videomancer/encore/encore_source6_wood.png';
import encore_hero_s1 from '/img/instruments/videomancer/encore/encore_hero_s1.png';
import encore_hero_s2 from '/img/instruments/videomancer/encore/encore_hero_s2.png';
import encore_hero_s3 from '/img/instruments/videomancer/encore/encore_hero_s3.png';
import encore_hero_s4 from '/img/instruments/videomancer/encore/encore_hero_s4.png';
import encore_hero_s5 from '/img/instruments/videomancer/encore/encore_hero_s5.png';
import encore_hero_s6 from '/img/instruments/videomancer/encore/encore_hero_s6.png';
import encore_ex1_s1 from '/img/instruments/videomancer/encore/encore_ex1_s1.png';
import encore_ex1_s2 from '/img/instruments/videomancer/encore/encore_ex1_s2.png';
import encore_ex1_s3 from '/img/instruments/videomancer/encore/encore_ex1_s3.png';
import encore_ex1_s4 from '/img/instruments/videomancer/encore/encore_ex1_s4.png';
import encore_ex1_s5 from '/img/instruments/videomancer/encore/encore_ex1_s5.png';
import encore_ex1_s6 from '/img/instruments/videomancer/encore/encore_ex1_s6.png';
import encore_ex2_s1 from '/img/instruments/videomancer/encore/encore_ex2_s1.png';
import encore_ex2_s2 from '/img/instruments/videomancer/encore/encore_ex2_s2.png';
import encore_ex2_s3 from '/img/instruments/videomancer/encore/encore_ex2_s3.png';
import encore_ex2_s4 from '/img/instruments/videomancer/encore/encore_ex2_s4.png';
import encore_ex2_s5 from '/img/instruments/videomancer/encore/encore_ex2_s5.png';
import encore_ex2_s6 from '/img/instruments/videomancer/encore/encore_ex2_s6.png';
import encore_ex3_s1 from '/img/instruments/videomancer/encore/encore_ex3_s1.png';
import encore_ex3_s2 from '/img/instruments/videomancer/encore/encore_ex3_s2.png';
import encore_ex3_s3 from '/img/instruments/videomancer/encore/encore_ex3_s3.png';
import encore_ex3_s4 from '/img/instruments/videomancer/encore/encore_ex3_s4.png';
import encore_ex3_s5 from '/img/instruments/videomancer/encore/encore_ex3_s5.png';
import encore_ex3_s6 from '/img/instruments/videomancer/encore/encore_ex3_s6.png';

# Encore

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Ballerina", before: encore_source1_ballerina, after: encore_hero_s1 },
    { label: "Boat", before: encore_source2_boat, after: encore_hero_s2 },
    { label: "Turtle", before: encore_source3_turtle, after: encore_hero_s3 },
    { label: "Pattern", before: encore_source4_pattern, after: encore_hero_s4 },
    { label: "Girl", before: encore_source5_girl, after: encore_hero_s5 },
    { label: "Wood", before: encore_source6_wood, after: encore_hero_s6 },
  ]}
/>
*Encore compositing a bordered picture-in-picture window with drop shadow over a darkened background.*

---

## Overview

Broadcast television invented picture-in-picture to show two things at once — a sports score ticker floating over live action, a news anchor inset against a remote feed. Encore brings that compositing language to Videomancer. It defines a rectangular window on screen and treats it as a stage: the input video plays inside the window, the area outside is darkened to half brightness, and the window itself can be framed with a bright white border and a drop shadow offset four pixels down and to the right.

The program operates entirely in the spatial domain. There are no BRAMs, no delay lines, no frequency accumulators — just a pixel position counter, a rectangle test, and a set of conditional assignments that decide what each pixel becomes. The name *Encore* references both the theatrical sense (bringing the performance back for another appearance, framed and spotlit) and the echo of early Quantel digital video effects hardware that made picture-in-picture compositing a defining visual of broadcast television.

At default settings, Encore presents a centered inset window at roughly 40% frame size with a visible border. The six knobs position and size the window, control border thickness, and set a shadow intensity parameter. The fader provides a wet/dry mix that crossfades between the windowed composite and the unprocessed input.

---

## Quick Start

1. **Minimum window is 64×64**: Even with Width and Height at zero, the window is never smaller than 64 pixels in each dimension, ensuring it is always visible.
2. **Border eats into the window**: The border is drawn inward from the window edges. A very thick border on a small window can consume most of the video area inside.
3. **Border width is coarse**: Only the top 4 bits of the pot register are used, giving 16 discrete steps (0–15 pixels). Fine pot movements near the bottom of the range may not produce visible changes.

---

## Background

### Picture-in-Picture in Broadcast History

Picture-in-picture (PIP) compositing was one of the first real-time digital video effects. Devices like the Quantel DPE 5000 and Ampex ADO introduced the ability to shrink, position, and layer live video feeds during the 1970s and 1980s. The technique rapidly became a staple of news broadcasts, sports coverage, and music video production. Encore distills the core mechanic — a movable rectangular inset — into a single FPGA program with dedicated knob-per-function control.

### The Quantel Legacy

Quantel (an abbreviation of *Quantified Television*) was a British company that pioneered digital video effects hardware from 1973 onward. Their systems — Paintbox, Harry, Henry, and the DPE series — defined the visual language of broadcast compositing. The picture-in-picture window with a clean border, positioned freely over a background, was a signature Quantel capability. Encore belongs to the Quantel category because it recreates this fundamental operation: windowed compositing with border decoration.

### Drop Shadow Rendering

A drop shadow is a darkened duplicate of a foreground element, offset slightly in position, that creates the illusion of the element floating above the background. In print design and GUI rendering, drop shadows use alpha blending and Gaussian blur for soft edges. Encore's implementation is deliberately simple — a hard-edged rectangle offset four pixels to the right and four pixels down, filled with the input video at half brightness. This matches the integer-arithmetic approach of early broadcast hardware, where shadows were rectangular and shadow softness was a luxury.

### Border Effects in Video Compositing

Borders serve two purposes in windowed compositing: they visually separate the inset from the background, and they establish a graphic frame that signals to the viewer that the window is an intentional overlay rather than a transmission artifact. Encore renders borders by testing whether the pixel falls within a configurable number of pixels from the window edge. When it does, the pixel is replaced with peak white (Y=1023) at neutral chroma (U=V=512). The border width is derived from the top four bits of the Border pot register, giving 0–15 pixels of border thickness.

### Window Transform and the Mirror Toggle

The Mirror toggle applies a bitwise NOT to the luminance channel inside the window. This is not a spatial mirror (horizontal or vertical flip) — it is a tonal inversion where every Y sample is complemented. Bright areas become dark and dark areas become bright, while chrominance passes through unchanged. The name "Mirror" reflects the reflective quality of the inverted image, reminiscent of a photographic negative viewed against light.


---

## Signal Flow

Timing Detection → Window Region Test → Shadow Region Test → ... → Mix Stage → Bypass Mux

```
Input Video (YUV 4:4:4)
│
├── Timing Detection ───────────────────────────────────────────
│   ├─ hsync_n / vsync_n fall-edge detection
│   ├─ x_counter (pixel position, 12-bit)
│   └─ y_counter (line position, 12-bit)
│
├── Window Region Test ─────────────────────────────────────────
│   ├─ x1 = Window X,  y1 = Window Y
│   ├─ x2 = x1 + Width + 64,  y2 = y1 + Height + 64
│   ├─ in_window = (x ∈ [x1, x2]) AND (y ∈ [y1, y2])
│   └─ in_border = in_window AND within border_width of any edge
│
├── Shadow Region Test (when shadow enabled, outside window) ───
│   └─ shadow = (x ∈ [x1+4, x2+4]) AND (y ∈ [y1+4, y2+4])
│
├── Pixel Assignment ───────────────────────────────────────────
│   ├─ Border:    Y = 1023 (white), U = 512, V = 512
│   ├─ Window:    Y = input Y (or NOT Y if Mirror), U/V = input
│   └─ Outside:   Y = input Y >> 1 (half brightness), U/V = input
│
├── Sync & Data Delay (8 clocks) ───────────────────────────────
│   └─ Shift registers for hsync, vsync, field, Y, U, V
│
├── Mix Stage (3× interpolator_u, 4 clocks) ────────────────────
│   └─ result = lerp(dry, wet, mix_amount)
│
└── Bypass Mux ─────────────────────────────────────────────────
    └─ bypass=1 → delayed dry;  bypass=0 → mixed output
```

The pipeline has two parallel paths: the processing path computes per-pixel window/border/shadow assignments based on position counters, while the delay path shifts the dry input through an 8-clock shift register to time-align it with the processed result. The three interpolator instances then crossfade between the delayed dry signal and the processed wet signal on all three YUV channels simultaneously. The border width is derived from only the top four bits of the Border pot register (`border_w(9 downto 6)`), giving a 0–15 pixel range for the white outline.

---

## Parameter Reference

<img src={encore_control_panel} alt="Videomancer front panel with Encore loaded"/>
*Videomancer's front panel with Encore active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Window X
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 63% |
| Suffix | % |

At 0% the window's left edge is at the left margin of the frame. At 100% the window's left edge is at pixel 1023, which may push the right edge off-screen depending on the Width setting. This register value maps directly to the x_counter comparison, so each increment moves the window one pixel to the right. Internally, sets the horizontal starting position of the picture-in-picture window.

---

#### Knob 2 — Window Y
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 63% |
| Suffix | % |

At 0% the top edge of the window sits at the top of the frame. Increasing this value moves the window downward. Combined with Window X, the two position knobs give full control over where the inset appears on screen. The default value of 640 places the window roughly in the lower third of a standard-definition frame. Internally, sets the vertical starting position of the window.

---

#### Knob 3 — Width
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Controls the horizontal extent of the window. The window's right edge is calculated as the left edge plus this register value plus a fixed offset of 64 pixels. At 0% the window is 64 pixels wide (the minimum). At 100% the window expands to 1087 pixels wide. The default value of 384 produces a medium-sized window suitable for inset compositing.

---

#### Knob 4 — Height
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Controls the vertical extent of the window. Like Width, the bottom edge is the top edge plus this register value plus 64 pixels. The minimum window height is 64 pixels, expanding to 1087 at maximum. Adjusting Width and Height independently allows rectangular windows of any aspect ratio — wide cinematic letterbox frames, tall portrait-style columns, or matched square insets.

---

#### Knob 5 — Border
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Controls the thickness of the white border drawn around the window edge. Only the top four bits of the 10-bit register are used, giving a range of 0–15 pixels. At low pot settings (below ~64), the border is invisible (0 pixels). Each subsequent 64-count increment adds one pixel of border width. The border is drawn inward from the window edges — it occupies space inside the window rectangle, so a thick border reduces the visible video area within the inset.

---

#### Knob 6 — Shadow
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 13% |
| Suffix | % |

The Shadow pot register is mapped but does not modulate the shadow effect in the current VHDL implementation. The shadow feature is controlled solely by the Shadow toggle (Toggle 8), which enables or disables a fixed half-brightness rectangle offset four pixels to the right and down from the window. The pot is reserved for future use as a shadow opacity or offset control.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Border** | Off | On |
| **8 — Shadow** | Off | On |
| **9 — Zoom** | Off | On |
| **10 — Mirror** | Off | On |
| **11 — Bypass** | Off | On |

Toggles 7–11 control five independent binary features. Border (7) and Shadow (8) add decorative elements to the window composite. Zoom (9) is declared in the register mapping but not connected to any processing logic. Mirror (10) applies luminance inversion inside the window. Bypass (11) routes the delayed dry signal directly to the output, skipping the mix stage.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |


#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Wet/dry crossfade between the original (dry) signal and the Encore-processed (wet) signal. At 0%, the output is the unprocessed input. At 100%, the output is the fully processed signal. Intermediate positions blend the two via a multi-clock interpolator operating on all channels simultaneously, producing a smooth crossfade with no color artifacts.



> See [Common Controls & Glossary Reference](../common_reference.md) for details.

---

## Guided Exercises

These exercises progress from basic window positioning to layered compositing with border decoration and tonal effects.

### Exercise 1: Centered Inset

<BeforeAfterSlider
  sources={[
    { label: "Ballerina", before: encore_source1_ballerina, after: encore_ex1_s1 },
    { label: "Boat", before: encore_source2_boat, after: encore_ex1_s2 },
    { label: "Turtle", before: encore_source3_turtle, after: encore_ex1_s3 },
    { label: "Pattern", before: encore_source4_pattern, after: encore_ex1_s4 },
    { label: "Girl", before: encore_source5_girl, after: encore_ex1_s5 },
    { label: "Wood", before: encore_source6_wood, after: encore_ex1_s6 },
  ]}
/>
*Centered Inset — simulated result across source images.*
**Source**: A live camera feed or recorded footage with a clearly recognizable subject.

**What You'll Create**: Learn the four spatial controls and position a clean picture-in-picture window.

1. **Default view**: Load Encore with default settings. Observe the window with its white border floating over the darkened background.
2. **Move horizontally**: Sweep Window X from 0% to 100%. Watch the window slide across the frame.
3. **Move vertically**: Sweep Window Y. The window moves up and down.
4. **Resize**: Adjust Width and Height to create a small centered inset — try Width ~25%, Height ~25% with Window X ~50%, Window Y ~30%.
5. **Aspect ratio**: Set Width to maximum and Height to minimum. The window becomes a wide horizontal strip. Reverse for a tall vertical column.

**Key concepts**: Window position is set in absolute pixel coordinates, window size adds to position plus a 64-pixel minimum, the four spatial controls are fully independent

---

### Exercise 2: Framed Window with Shadow

<BeforeAfterSlider
  sources={[
    { label: "Ballerina", before: encore_source1_ballerina, after: encore_ex2_s1 },
    { label: "Boat", before: encore_source2_boat, after: encore_ex2_s2 },
    { label: "Turtle", before: encore_source3_turtle, after: encore_ex2_s3 },
    { label: "Pattern", before: encore_source4_pattern, after: encore_ex2_s4 },
    { label: "Girl", before: encore_source5_girl, after: encore_ex2_s5 },
    { label: "Wood", before: encore_source6_wood, after: encore_ex2_s6 },
  ]}
/>
*Framed Window with Shadow — simulated result across source images.*
**Source**: Any video footage with moderate brightness and color variation.

**What You'll Create**: Explore border thickness and shadow placement to create a broadcast-style floating window.

1. **Position the window**: Set Window X ~40%, Window Y ~30%, Width ~35%, Height ~35% for a centered medium inset.
2. **Thick border**: Increase Border to ~75%. The white outline becomes prominently visible (approximately 12 pixels wide).
3. **Enable shadow**: Toggle Shadow On. A half-brightness copy of the window region appears offset 4 pixels down and right, giving the window a floating appearance.
4. **Thin border**: Reduce Border to ~10%. The outline shrinks to 1–2 pixels — a subtle hairline frame.
5. **Remove border**: Toggle Border Off. The window has no outline; only the brightness difference and shadow separate it from the background.
6. **Mix fade**: Sweep the Mix fader from 100% to 0%. Watch the window composite dissolve into the full-frame input.

**Key concepts**: Border width uses only the top 4 register bits giving 0–15 pixel steps, shadow is a fixed 4-pixel offset at half brightness, mix crossfades between composite and dry signal

---

### Exercise 3: Inverted Inset Composite

<BeforeAfterSlider
  sources={[
    { label: "Ballerina", before: encore_source1_ballerina, after: encore_ex3_s1 },
    { label: "Boat", before: encore_source2_boat, after: encore_ex3_s2 },
    { label: "Turtle", before: encore_source3_turtle, after: encore_ex3_s3 },
    { label: "Pattern", before: encore_source4_pattern, after: encore_ex3_s4 },
    { label: "Girl", before: encore_source5_girl, after: encore_ex3_s5 },
    { label: "Wood", before: encore_source6_wood, after: encore_ex3_s6 },
  ]}
/>
*Inverted Inset Composite — simulated result across source images.*
**Source**: High-contrast footage — strong lighting, distinct bright and dark regions.

**What You'll Create**: Combine window compositing with the Mirror luma inversion to create a negative-within-positive frame.

1. **Set up window**: Position a medium window — Window X ~30%, Window Y ~25%, Width ~40%, Height ~40%.
2. **Enable border**: Turn Border On with Border pot at ~50% for a visible white frame.
3. **Enable Mirror**: Toggle Mirror On. The video inside the window becomes tonally inverted — a photographic negative framed within the positive image.
4. **Compare**: Toggle Mirror On/Off to see the inversion effect. Notice that chrominance shifts but is not fully inverted.
5. **Mix interaction**: Reduce Mix to ~50%. The inverted window blends with the original, creating a partially transparent negative overlay.
6. **Full composite**: Enable Shadow and increase Border for a complete broadcast-style composite with an inverted inset.

**Key concepts**: Mirror applies bitwise NOT to Y only (not a spatial flip), chrominance is unaffected by mirror, mix blends the inverted composite with the original input

---


## Tips

- **Mirror is tonal, not spatial**: The Mirror toggle inverts luminance values (bitwise NOT), not the spatial arrangement of pixels. It creates a photographic-negative effect, not a horizontal or vertical flip.
- **Shadow pot is reserved**: The Shadow knob (Pot 6) is mapped in the register file but does not modulate the shadow effect. Shadow is controlled solely by the Shadow toggle (Toggle 8).
- **Feedback routing**: Connect the Encore output back to its input for recursive window-in-window effects. Each feedback pass creates a smaller, darker copy of the window nested inside itself.
- **Mix for dissolves**: The Mix fader smoothly crossfades between the composite and the dry input. Use it for gradual reveal or dissolve transitions during live performance.

---

## Glossary

| Term | Definition |
|------|------------|
| **BT.601** | ITU-R Recommendation for standard-definition television color encoding, defining the YUV color matrix used throughout the Videomancer pipeline. |
| **Bypass** | A signal routing mode that sends the input directly to the output, skipping all processing stages. |
| **Compositing** | Combining multiple visual elements into a single output frame, typically by layering one image over another. |
| **Drop Shadow** | A darkened duplicate of a foreground element offset in position to create the illusion of depth or floating. |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **PIP** | Picture-in-Picture; a compositing technique that displays one video source inside a window overlaid on another. |
| **Quantel** | A pioneering British digital video effects company whose hardware defined broadcast compositing from the 1970s onward. |

For common terms (YUV, FPGA, BRAM, Pipeline, etc.) see the [Common Glossary](../common_reference.md#common-glossary).

---
