---
draft: true
sidebar_position: 208
slug: /instruments/videomancer/peephole
title: "Peephole"
image: /img/instruments/videomancer/peephole/peephole_hero.png
description: "Every video synthesizer needs a way to isolate part of the frame — to say \"this region is visible, everything else is black.\" Peephole is a position-based video keyer that generates a soft mask from horizontal and vertical position ramps."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import peephole_hero from '/img/instruments/videomancer/peephole/peephole_hero.png';
import peephole_control_panel from '/img/instruments/videomancer/peephole/peephole_control_panel.png';
import peephole_exercise1_result from '/img/instruments/videomancer/peephole/peephole_exercise1_result.png';
import peephole_exercise2_result from '/img/instruments/videomancer/peephole/peephole_exercise2_result.png';
import peephole_exercise3_result from '/img/instruments/videomancer/peephole/peephole_exercise3_result.png';
import peephole_source1_kodim02 from '/img/instruments/videomancer/peephole/peephole_source1_kodim02.png';
import peephole_source2_kodim07 from '/img/instruments/videomancer/peephole/peephole_source2_kodim07.png';
import peephole_source3_kodim01_bw from '/img/instruments/videomancer/peephole/peephole_source3_kodim01_bw.png';

# Peephole

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Kodim02", before: peephole_source1_kodim02, after: peephole_hero },
    { label: "Kodim07", before: peephole_source2_kodim07, after: peephole_hero },
    { label: "Kodim01 B&W", before: peephole_source3_kodim01_bw, after: peephole_hero },
  ]}
/>
*Peephole carving a diamond key window through a live camera feed, luma modulation pulling the boundary inward around dark regions.*

---

## Overview

Every video synthesizer needs a way to isolate part of the frame — to say "this region is visible, everything else is black." Peephole is a position-based video keyer that generates a soft mask from horizontal and vertical position ramps. Four edge thresholds define the boundaries of a rectangular window, and the signal inside that window passes through while everything outside fades to black.

The name comes from the idea of looking through a small opening in a door — a narrow aperture that reveals a limited view of the world beyond. Here, the aperture is a rectangular or diamond-shaped key window whose size, position, gain, and edge softness are all under continuous control. Input video brightness can modulate the key boundary, making the aperture breathe with the image content. A border extraction mode reduces the key to its edges, producing luminous outlines that trace the window boundary.

At wide-open settings, Peephole passes the full frame. As you narrow the thresholds, the visible region shrinks. Push the edge thresholds past each other and the key collapses entirely. The interaction between the four threshold controls, gain amplification, and luma modulation creates a rich space of masking, framing, and content-responsive vignette effects.

---

## Background

### Position-Based Keying

Traditional video keyers separate foreground from background based on signal content — chroma keyers use color, luma keyers use brightness. Peephole takes a fundamentally different approach: it generates a key signal from the *position* of each pixel in the frame. Horizontal and vertical ramps sweep from 0 at one edge to approximately 1023 at the opposite edge, and the key value at each pixel is determined solely by where that pixel sits relative to the four edge thresholds.

This makes the key shape independent of image content (before luma modulation is applied). The mask is a geometric construct — a rectangle carved into the frame by four boundary lines.

### Frequency Accumulator Ramps

The position ramps are not simple counters. Peephole uses phase accumulators — 16-bit registers that add a fixed frequency value every clock cycle. The upper 10 bits of each accumulator produce the ramp output. The horizontal accumulator resets at the start of each active video line and increments every pixel clock. The vertical accumulator resets at the start of each field and increments once per line. The result is a pair of sawtooth ramps that sweep across the visible area, providing a continuous coordinate system for the key geometry.

### Edge Distance and Shape Modes

The key window is defined by four thresholds: left, right, top, and bottom. For each pixel, the distance to each boundary is computed and clamped to zero (pixels outside the boundary contribute nothing). The horizontal key is the minimum of the left and right distances; the vertical key is the minimum of the top and bottom distances.

Two shape modes combine these values differently. Rectangle mode takes the minimum of horizontal and vertical keys, producing axis-aligned rectangular masks with soft edges proportional to distance from the nearest boundary. Diamond mode sums the horizontal and vertical keys, producing a rhombus inscribed within the rectangle — the boundary follows Manhattan distance from the window edges, cutting the corners. Both shapes have naturally soft edges whose softness depends on the key gain.

### Luma Modulation and Border Extraction

After the geometric key is computed and amplified by the gain stage, Peephole can modulate it with the input video's brightness. The modulation is bipolar and centered: at zero modulation depth, the contribution is zero. Positive modulation causes bright pixels to expand the key boundary outward; negative modulation causes bright pixels to shrink it. This makes the geometric mask respond to image content — the aperture boundary deforms around objects in the scene.

Border extraction is a separate feature that computes the horizontal gradient of the final key — the absolute difference between adjacent pixels, scaled up by four for visibility. This converts the filled key region into a pair of luminous lines tracing the vertical edges of the window boundary.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Position Ramps ─────────────────────────────────────────────
│   ├─ Video Timing Generator (~2 clk sync detection)
│   ├─ H Accumulator (~2 clk, freq=76, resets at avid_start)
│   └─ V Accumulator (~2 clk, freq=248, resets at vsync_start)
│
├── Key Generation ─────────────────────────────────────────────
│   ├─ 1. Edge Distances (1 clk)
│   │     Left: clamp(h_ramp - left_thresh, 0)
│   │     Right: clamp(right_thresh - h_ramp, 0)
│   │     Top: clamp(v_ramp - top_thresh, 0)
│   │     Bottom: clamp(bot_thresh - v_ramp, 0)
│   ├─ 2. Shape Selection (1 clk)
│   │     Rectangle: min(min(L,R), min(T,B))
│   │     Diamond: clamp(min(L,R) + min(T,B), 0, 1023)
│   ├─ 3. Key Gain (1 clk)
│   │     gained = (soft_key × key_gain) / 512
│   ├─ 4. Luma Modulation (2 clk)
│   │     contribution = (luma - 512) × (luma_mod - 512) / 1024
│   │     modulated = clamp(gained + contribution, 0, 1023)
│   ├─ 5. Global Threshold + Invert + Border (1 clk)
│   │     effective = 1023 - global_thresh
│   │     thresholded = max(0, modulated - effective)
│   │     inverted = key_invert ? 1023 - thresholded : thresholded
│   │     border = |inverted[x] - inverted[x-1]| × 4
│   └─ Final key signal
│
├── Video Delay Pipeline (11 stages) ───────────────────────────
│   └─ Aligns input YUV with key output
│
├── Output Mix (2 clk) ────────────────────────────────────────
│   ├─ Y = (delayed_Y × key) / 1024
│   ├─ U = 512 + ((delayed_U - 512) × key) / 1024
│   └─ V = 512 + ((delayed_V - 512) × key) / 1024
│
├── Bypass ─────────────────────────────────────────────────────
│   └─ Select original or processed signal
│
└── Sync ───────────────────────────────────────────────────────
    └─ Pass-through (hsync, vsync, field, avid)
```

The key computation is purely geometric — it depends only on pixel position and the four edge thresholds — until the luma modulation stage adds content dependency. The gain stage amplifies the naturally soft distance-based key before modulation, controlling how quickly the key transitions from zero to full. At gain = 512 (unity), the key ramps linearly from the boundary. At gain = 1023, the key reaches full value in half the distance, creating harder edges.

The output mix scales luma directly (zero key = black) but applies chroma relative to neutral (zero key = neutral gray, not green/purple). This ensures that keyed-out areas are true black rather than having residual color artifacts.

---

## Parameter Reference

<img src={peephole_control_panel} alt="Videomancer front panel with Peephole loaded"/>
*Videomancer's front panel with Peephole active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Top Thresh
| Property | Value |
|----------|-------|
| Range | 0.0% – 200.0% |
| Default | 100.1% |
| Suffix | % |

Sets the vertical position of the top key boundary. At 0%, the top edge cuts into the frame from above. At 200%, the boundary moves below the visible area, opening the top fully. As you increase this control, the visible region expands downward from the top edge. The interaction with Bot Thresh defines the vertical span of the key window — when top exceeds bottom, the vertical key collapses to zero.

---

#### Knob 2 — Left Thresh
| Property | Value |
|----------|-------|
| Range | 0.0% – 200.0% |
| Default | 100.1% |
| Suffix | % |

Sets the horizontal position of the left key boundary. At 0%, the left edge sits at the frame boundary. As you increase the value, the boundary moves rightward into the frame, cutting off the left side. Combined with Right Thresh, this defines the horizontal span of the key window. The edge softness is inherent — pixels near the boundary have small key values that ramp up with distance.

---

#### Knob 3 — Key Gain
| Property | Value |
|----------|-------|
| Range | 0.0% – 200.0% |
| Default | 100.1% |
| Suffix | % |

Controls key amplitude. At 512 (midpoint), the gain is unity — the distance-based soft key passes through unchanged. Below 512, the key is attenuated, making even the center of the window dimmer. Above 512, the gain amplifies the key, making the transition from edge to full brightness steeper. At maximum gain (~2×), the key clips to full white after only half the normal distance from the boundary, producing harder-edged masks.

---

#### Knob 4 — Bot Thresh
| Property | Value |
|----------|-------|
| Range | -100.0% – 100.0% |
| Default | 0.1% |
| Suffix | % |

Sets the vertical position of the bottom key boundary. Works inversely to Top Thresh — as you increase this control, the bottom boundary moves higher, restricting the visible region. When Bot Thresh is set lower than Top Thresh, no vertical range satisfies both conditions and the key collapses.

---

#### Knob 5 — Right Thresh
| Property | Value |
|----------|-------|
| Range | -100.0% – 100.0% |
| Default | 0.1% |
| Suffix | % |

Sets the horizontal position of the right key boundary. As you decrease this control, the right boundary moves leftward. The key exists only where the horizontal ramp is simultaneously above Left Thresh and below Right Thresh. The distance from the nearer boundary determines the horizontal key contribution at each pixel.

---

#### Knob 6 — Luma Mod
| Property | Value |
|----------|-------|
| Range | -100.0% – 100.0% |
| Default | 0.1% |
| Suffix | % |

Bipolar luma modulation depth. At 512 (0%), no modulation — the key is purely geometric. Turning clockwise (toward +100%) causes bright areas of the input to expand the key boundary outward. Turning counter-clockwise (toward -100%) causes bright areas to shrink the boundary. The modulation is computed as a signed product of centered luma and centered modulation depth, then added to the gained key signal.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Luma Invert** | Off | On |
| **8 — Key Shape** | Rectangle | Diamond |
| **9 — Key Invert** | Off | On |
| **10 — Key Border** | Off | On |
| **11 — Bypass** | Off | On |

The five toggle switches control independent binary processing options. Luma Invert and Key Invert are separate inversions at different points in the processing chain — Luma Invert flips the brightness input to the modulation stage, while Key Invert flips the final key output. Key Shape selects between two fundamentally different geometries. Key Border extracts edge information rather than area information. Bypass is a simple pass-through.

Note: This program uses an unpacked toggle ABI — each toggle switch occupies its own SPI register (registers 6 through 10) rather than being bit-packed into register 6. The VHDL reads bit 0 of each register independently.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Global Thresh
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Master key level controlling the overall strength of the key effect. At 100% (initial value), the full computed key passes through. As you lower the fader, progressively more of the key is subtracted via an inverted threshold: the effective threshold is 1023 minus the fader value. At 0%, the effective threshold equals 1023 and virtually nothing survives. This provides a smooth global fade of the keying effect without affecting the geometric shape.

---

## Guided Exercises

These exercises progress from simple rectangular masking to content-responsive key effects and edge extraction. Each builds on the previous, gradually engaging more of the processing chain.

### Exercise 1: Rectangular Window Framing

<BeforeAfterSlider
  sources={[
    { label: "Kodim02", before: peephole_source1_kodim02, after: peephole_exercise1_result },
    { label: "Kodim07", before: peephole_source2_kodim07, after: peephole_exercise1_result },
    { label: "Kodim01 B&W", before: peephole_source3_kodim01_bw, after: peephole_exercise1_result },
  ]}
/>
*Rectangular Window Framing — simulated result across source images.*
**Source**: A live camera feed or recorded footage with recognizable subjects.

**Objective**: Learn how the four edge thresholds define the key window and how gain controls edge softness.

1. **Open window**: Start with all thresholds at default (Top and Left at 100%, Bot and Right at 0%). The key window should span the full frame.
2. **Narrow horizontally**: Increase Left Thresh and decrease Right Thresh. Watch the visible region shrink from both sides.
3. **Narrow vertically**: Increase Top Thresh and decrease Bot Thresh. The window becomes a small rectangle in the center.
4. **Soften edges**: Lower Key Gain below 100%. The transition from visible to black becomes gradual — a soft vignette.
5. **Harden edges**: Raise Key Gain above 100%. The transition sharpens. At maximum, the edge becomes nearly binary.
6. **Asymmetric framing**: Set different values for Left vs. Right and Top vs. Bottom to position the window off-center.

**Key concepts**: Four independent edge boundaries define the window, key value is the minimum distance to the nearest boundary, gain amplifies the soft distance-based key to control edge hardness

---

### Exercise 2: Diamond Keys and Luma Modulation

<BeforeAfterSlider
  sources={[
    { label: "Kodim02", before: peephole_source1_kodim02, after: peephole_exercise2_result },
    { label: "Kodim07", before: peephole_source2_kodim07, after: peephole_exercise2_result },
    { label: "Kodim01 B&W", before: peephole_source3_kodim01_bw, after: peephole_exercise2_result },
  ]}
/>
*Diamond Keys and Luma Modulation — simulated result across source images.*
**Source**: Footage with strong brightness contrast — spotlit subjects against dark backgrounds.

**Objective**: Explore diamond shape mode and how luma modulation deforms the key boundary.

1. **Set up window**: Create a centered rectangular window (Top ~60%, Left ~60%, Bot ~40%, Right ~40%).
2. **Switch to Diamond**: Toggle Key Shape to Diamond. The rectangle's corners cut away, forming a rhombus.
3. **Add luma modulation**: Slowly increase Luma Mod from 0% toward +100%. Watch the key boundary respond to image brightness — bright areas push the boundary outward.
4. **Invert luma**: Toggle Luma Invert. Now dark areas push outward instead.
5. **Negative modulation**: Set Luma Mod toward -100% with Luma Invert off. Bright areas now shrink the boundary.
6. **Combine with gain**: Increase Key Gain to sharpen the modulated edge. The boundary deformation becomes more defined.

**Key concepts**: Diamond mode sums horizontal and vertical keys (Manhattan distance), luma modulation is bipolar and centered around zero at 512, Luma Invert reverses the brightness signal before the modulation multiply

---

### Exercise 3: Border Extraction and Key Sculpting

<BeforeAfterSlider
  sources={[
    { label: "Kodim02", before: peephole_source1_kodim02, after: peephole_exercise3_result },
    { label: "Kodim07", before: peephole_source2_kodim07, after: peephole_exercise3_result },
    { label: "Kodim01 B&W", before: peephole_source3_kodim01_bw, after: peephole_exercise3_result },
  ]}
/>
*Border Extraction and Key Sculpting — simulated result across source images.*
**Source**: Any footage — high-contrast material works well for visible borders.

**Objective**: Combine border extraction, key inversion, and global threshold for abstract edge effects.

1. **Set up a key window**: Create a moderately sized centered window with medium gain.
2. **Enable Key Border**: Toggle Key Border on. The filled rectangle becomes two luminous vertical lines at the left and right boundaries.
3. **Add luma modulation**: Increase Luma Mod. The border lines deform with brightness, creating wavy edge traces.
4. **Key Invert**: Toggle Key Invert. The sense reverses — the lines now appear as dark cuts in a bright field.
5. **Global threshold sculpt**: Lower Global Thresh gradually. Watch the border lines thin and eventually vanish as the threshold eats into the key amplitude.
6. **Diamond borders**: Switch to Diamond mode. The border lines now trace the diagonal edges of the rhombus.
7. **Extreme gain**: Push Key Gain to maximum. The border lines become very thin and bright — nearly single-pixel edges.

**Key concepts**: Border extraction computes the horizontal gradient of the key signal, global threshold subtracts a floor from the key before display, border mode and key inversion interact to produce different edge representations

---


## Tips

- **Four-corner framing**: The four thresholds are independent — each edge can be placed anywhere. This allows off-center windows, narrow slits, and L-shaped masks (when combined with key inversion).
- **Gain controls edge hardness**: Low gain produces soft vignettes; high gain produces sharp-edged masks. Unity gain (100%) gives a linear ramp from boundary to center.
- **Diamond for organic shapes**: Diamond mode adds the horizontal and vertical keys, producing rounded corners that feel more organic than the axis-aligned rectangle. Combined with luma modulation, diamond keys produce flowing, content-responsive boundaries.
- **Luma mod is bipolar**: The modulation is centered at 512. Clockwise modulates one way, counter-clockwise the other. Luma Invert flips which brightness values drive the modulation, not the depth.
- **Border extraction is horizontal only**: The border mode computes horizontal differences, so it traces vertical edges of the key window. Horizontal edges (top/bottom boundaries) are not extracted — use this asymmetry creatively.
- **Global Thresh as fade control**: Use the fader to smoothly bring the key effect in and out during performance without changing the window geometry.
- **Feedback loops**: Route the output back to the input. The key boundary deforms recursively because the keyed output has different brightness than the original, changing the luma modulation contribution.

---

## Glossary

| Term | Definition |
|------|------------|
| **Accumulator** | A register that adds a fixed increment every clock cycle, producing a sawtooth ramp; used here to generate position coordinates across the frame. |
| **Bipolar** | A control centered at its midpoint, with positive and negative effects on either side of center. |
| **Border Extraction** | Computing the horizontal gradient (difference between adjacent pixels) of a signal to isolate edge transitions. |
| **Chroma** | The color information in a video signal, encoded as U and V components in YUV color space. |
| **Clamp** | Constraining a value to remain within a fixed range, preventing overflow or underflow. |
| **Diamond Key** | A key shape formed by summing horizontal and vertical edge distances, producing a rhombus boundary following Manhattan distance. |
| **Edge Threshold** | A position value defining one side of the key window boundary; pixels beyond the threshold contribute zero key. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Key** | A control signal (0–1023) that determines the opacity of each pixel; 0 = fully transparent (black), 1023 = fully opaque. |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **Manhattan Distance** | The sum of horizontal and vertical distances, producing diamond-shaped iso-distance contours. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Position Ramp** | A linearly increasing signal that sweeps from 0 to 1023 across the horizontal or vertical extent of the frame. |
| **Proc Amp** | Processing Amplifier; a gain-and-offset stage that applies brightness and contrast adjustment to a signal. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
