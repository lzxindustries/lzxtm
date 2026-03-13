---
draft: true
sidebar_position: 6
slug: /instruments/videomancer/anaglyph
title: "Anaglyph"
image: /img/instruments/videomancer/anaglyph/anaglyph_hero_s1.png
description: "Anaglyph creates stereoscopic 3D anaglyphic images from 2D video by using source luminance as a depth map."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import anaglyph_control_panel from '/img/instruments/videomancer/anaglyph/anaglyph_control_panel.png';
import anaglyph_source1_runner from '/img/instruments/videomancer/anaglyph/anaglyph_source1_runner.png';
import anaglyph_source2_field from '/img/instruments/videomancer/anaglyph/anaglyph_source2_field.png';
import anaglyph_source3_clouds from '/img/instruments/videomancer/anaglyph/anaglyph_source3_clouds.png';
import anaglyph_source4_pattern from '/img/instruments/videomancer/anaglyph/anaglyph_source4_pattern.png';
import anaglyph_source5_man from '/img/instruments/videomancer/anaglyph/anaglyph_source5_man.png';
import anaglyph_source6_wood from '/img/instruments/videomancer/anaglyph/anaglyph_source6_wood.png';
import anaglyph_hero_s1 from '/img/instruments/videomancer/anaglyph/anaglyph_hero_s1.png';
import anaglyph_hero_s2 from '/img/instruments/videomancer/anaglyph/anaglyph_hero_s2.png';
import anaglyph_hero_s3 from '/img/instruments/videomancer/anaglyph/anaglyph_hero_s3.png';
import anaglyph_hero_s4 from '/img/instruments/videomancer/anaglyph/anaglyph_hero_s4.png';
import anaglyph_hero_s5 from '/img/instruments/videomancer/anaglyph/anaglyph_hero_s5.png';
import anaglyph_hero_s6 from '/img/instruments/videomancer/anaglyph/anaglyph_hero_s6.png';
import anaglyph_ex1_s1 from '/img/instruments/videomancer/anaglyph/anaglyph_ex1_s1.png';
import anaglyph_ex1_s2 from '/img/instruments/videomancer/anaglyph/anaglyph_ex1_s2.png';
import anaglyph_ex1_s3 from '/img/instruments/videomancer/anaglyph/anaglyph_ex1_s3.png';
import anaglyph_ex1_s4 from '/img/instruments/videomancer/anaglyph/anaglyph_ex1_s4.png';
import anaglyph_ex1_s5 from '/img/instruments/videomancer/anaglyph/anaglyph_ex1_s5.png';
import anaglyph_ex1_s6 from '/img/instruments/videomancer/anaglyph/anaglyph_ex1_s6.png';
import anaglyph_ex2_s1 from '/img/instruments/videomancer/anaglyph/anaglyph_ex2_s1.png';
import anaglyph_ex2_s2 from '/img/instruments/videomancer/anaglyph/anaglyph_ex2_s2.png';
import anaglyph_ex2_s3 from '/img/instruments/videomancer/anaglyph/anaglyph_ex2_s3.png';
import anaglyph_ex2_s4 from '/img/instruments/videomancer/anaglyph/anaglyph_ex2_s4.png';
import anaglyph_ex2_s5 from '/img/instruments/videomancer/anaglyph/anaglyph_ex2_s5.png';
import anaglyph_ex2_s6 from '/img/instruments/videomancer/anaglyph/anaglyph_ex2_s6.png';
import anaglyph_ex3_s1 from '/img/instruments/videomancer/anaglyph/anaglyph_ex3_s1.png';
import anaglyph_ex3_s2 from '/img/instruments/videomancer/anaglyph/anaglyph_ex3_s2.png';
import anaglyph_ex3_s3 from '/img/instruments/videomancer/anaglyph/anaglyph_ex3_s3.png';
import anaglyph_ex3_s4 from '/img/instruments/videomancer/anaglyph/anaglyph_ex3_s4.png';
import anaglyph_ex3_s5 from '/img/instruments/videomancer/anaglyph/anaglyph_ex3_s5.png';
import anaglyph_ex3_s6 from '/img/instruments/videomancer/anaglyph/anaglyph_ex3_s6.png';

# Anaglyph

<span class="head2_nolink">Videomancer Program Guide</span>

:::warning
This document is still in progress, may contain errors, and is for preview only.
:::

<BeforeAfterSlider
  sources={[
    { label: "Runner", before: anaglyph_source1_runner, after: anaglyph_hero_s1 },
    { label: "Field", before: anaglyph_source2_field, after: anaglyph_hero_s2 },
    { label: "Clouds", before: anaglyph_source3_clouds, after: anaglyph_hero_s3 },
    { label: "Pattern", before: anaglyph_source4_pattern, after: anaglyph_hero_s4 },
    { label: "Man", before: anaglyph_source5_man, after: anaglyph_hero_s5 },
    { label: "Wood", before: anaglyph_source6_wood, after: anaglyph_hero_s6 },
  ]}
/>
*Anaglyph rendering a landscape as a red/cyan stereoscopic image — bright regions push forward and dark regions recede, creating a convincing 3D depth illusion viewable with classic red/cyan glasses.*

---

## Overview

Anaglyph creates stereoscopic 3D anaglyphic images from 2D video by using source luminance as a depth map. Bright pixels are treated as near objects and dark pixels as far objects (or vice versa), with each pixel horizontally displaced according to its brightness. Two virtual "eyes" read the displaced image at different horizontal offsets — the left eye reads from one direction and the right eye from the opposite direction — then each eye's view is encoded with complementary colour tints. When viewed through red/cyan (or green/magenta) filter glasses, the brain fuses the two colour-separated views into a perception of three-dimensional depth.

The effect operates on a per-scanline basis using ping-pong line buffers. Six line buffers (Y, U, V for each eye) store the current scanline; the left eye reads at `h_count − displacement` and the right eye at `h_count + displacement`. A convergence offset shifts both eyes equally, controlling where in the image the zero-parallax plane sits — objects at that depth appear to sit on the screen surface, objects in front of it appear to pop out, and objects behind it appear to recede.

At moderate settings, the program produces a subtle but convincing stereoscopic effect from any video source. At extreme settings — very high depth amount with wide separation — the image splits dramatically into separated red and cyan ghost images with obvious depth layering.

---

## Quick Start

1. **With glasses, start conservative**: Begin with Depth Amt ~35% and Separation ~30% for comfortable viewing. Increase gradually.
2. **Convergence matters for comfort**: Set convergence so the most important subject has minimal colour fringe — that puts it on the screen plane. Objects behind and in front will pop.
3. **Red/Cyan is more available, Green/Magenta is more accurate**: Red/Cyan glasses are cheap and ubiquitous but desaturate reds. Green/Magenta preserves more colour but the glasses are less common.

---

## Background

### What Is Anaglyphic 3D?

**Anaglyphic 3D** is one of the oldest stereoscopic display techniques, dating to the 1850s. It works by encoding the left-eye and right-eye views of a scene in complementary colours — typically red for one eye and cyan (blue-green) for the other. When viewed through glasses with matching colour filters, each filter blocks one view and passes the other, so each eye sees only its intended perspective. The brain's binocular disparity processing interprets the two slightly different views as depth.

The most common colour pair is **red/cyan**, where the left eye sees through a red filter (blocking cyan) and the right eye through a cyan filter (blocking red). The **green/magenta** pair is an alternative that distributes the colour spectrum differently, often producing better colour fidelity at the expense of slightly less effective depth separation.

### What Is Luminance-as-Depth?

Traditional stereoscopic imaging requires two cameras at different positions. **Luminance-as-depth** is a synthesis technique that creates a depth map from a single image by assuming that brightness correlates with distance — bright areas are "closer" and dark areas are "further" (or the reverse). While this is a crude approximation of real depth, it produces surprisingly effective pseudo-3D from many natural images, especially landscapes, portraits with bright foreground subjects, and any scene with strong brightness gradients.

### What Is Convergence?

In stereoscopic imaging, the **convergence point** is the distance at which the left and right eye views overlap perfectly. Objects at this distance have zero parallax — they appear to sit on the screen plane. Objects in front of the convergence point have positive parallax (they appear to pop out of the screen), while objects behind it have negative parallax (they recede into the screen). The Converge pot in Anaglyph shifts this zero-parallax plane, allowing you to control which brightness range appears to sit "on" the screen.


---

## Signal Flow

Y Channel → Sync Signals → 6× Line Buffers → Interpolator → Output

```
Input Video (YUV 4:4:4 30-bit)
│
├── Y Channel ──────────────────────────────────────────────────────
│   │
│   ├─ 1.  Input register + depth multiply   (depth_amt × luma → disp_raw)
│   ├─ 2.  Separation multiply               (separation × disp_raw → displacement)
│   ├─ 3.  Address computation               (h_count − disp + conv → left_addr
│   │                                          h_count + disp + conv → right_addr)
│   ├─ 4-5. Line buffer read latency         (2 clocks registered I/O)
│   ├─ 6.  Stereo compositor                 (tinting: left=red/green offset,
│   │                                          right=cyan/mag offset + avg Y)
│   └─ 7.  Saturation clamp + brightness     (clamp UV 0-1023, Y × brightness)
│
├── Sync Signals ───────────────────────────────────────────────────
│   └─ 12-clock delay pipeline                (align with processing depth)
│
├── 6× Line Buffers (ping-pong Y/U/V) ─────────────────────────────
│   └─ Left eye reads at h−disp, Right eye reads at h+disp
│
├── Interpolator (4 clocks per channel) ────────────────────────────
│   └─ Mix = lerp(input_delayed, processed, mix_amount)
│
└── Output ─────────────────────────────────────────────────────────
    └─ Y/U/V from interpolator mix
```

The depth computation uses an 8×8 reduced multiply: the top 8 bits of `depth_amt` are multiplied by the top 8 bits of input luma, producing a displacement value that controls how far each pixel shifts horizontally. A second multiply stage applies the separation control as a secondary scaling of the raw displacement, allowing independent control of the per-pixel depth amount vs the overall inter-eye spacing.

The convergence offset is a signed quantity centred at 512: values below 512 shift both eyes left (moving the convergence plane), values above 512 shift both eyes right. This does not change the magnitude of the stereo separation — it only shifts where zero parallax occurs.

The colour tints are computed per-pixel in YUV space. In Red/Cyan mode, the left-eye luma drives V up and U down (red shift), while the right-eye luma drives U up and V down (cyan shift). In Green/Magenta mode, the channels are swapped. The tint strength pot controls the magnitude of these offset: at zero, only the luma channel carries the stereo separation; at maximum, the colour separation is dramatic.

---

## Parameter Reference

<img src={anaglyph_control_panel} alt="Videomancer front panel with Anaglyph loaded"/>
*Videomancer's front panel with Anaglyph active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Depth Amt
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

At 0%, there is no displacement and both eyes see the same image (flat, no 3D). At 50%, moderate depth mapping creates a subtle stereoscopic effect. At 100%, extreme displacement produces very strong parallax shifts — bright pixels are displaced far from their original position, potentially creating visible ghosting and tearing artefacts. Internally, controls the overall depth effect strength by scaling how much each pixel's luminance contributes to its horizontal displacement.

---

#### Knob 2 — Converge
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the convergence (zero-parallax) point. At 50% (centre), the convergence plane sits at mid-brightness. Below 50%, the convergence plane shifts toward darker values — bright objects appear more in front of the screen and dark objects stay on-screen. Above 50%, the convergence plane shifts toward brighter values. This control is subtle but important for comfortable viewing — incorrect convergence can cause eyestrain.

---

#### Knob 3 — Separation
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Controls the inter-eye separation as a secondary multiplier on the displacement. This works with Depth Amt to control the final pixel shift. When Depth Amt sets the per-pixel depth scaling, Separation controls an overall magnification of the resulting displacement. At 0%, both eyes read from the same position regardless of Depth Amt. At moderate values, the separation is comfortable for glasses viewing. At maximum, the separation is exaggerated.

---

#### Knob 4 — Tint Str
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

At 0%, the output luma carries the stereo information but no colour separation — the effect is primarily a brightness shift between left and right. At moderate values, a clear red/cyan (or green/magenta) colour separation is visible. At 100%, the tint dominates the output colour, producing vivid red and cyan hues. Internally, controls the strength of the colour tint applied to each eye's view.

---

#### Knob 5 — Edge Boost
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls edge enhancement of the depth map before displacement. Higher values sharpen the luminance transitions, leading to more pronounced depth boundaries. At 0%, the depth map is the raw source luminance. At higher values, edges in the source image create sharper depth steps, which can enhance the perception of object boundaries in the 3D rendering.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls output brightness gain. At 50% (value 512), the brightness is unity (unchanged). Below 50%, the output is dimmer. Above 50%, the output is brighter. This compensates for brightness loss when viewing through the colour filter glasses, which typically attenuate overall brightness significantly.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Mode** | Red/Cyan | Mono |
| **8 — Depth Dir** | Bright Near | Bright Far |
| **9 — Edge Key** | Off | On |
| **10 — Crosseye** | Off | On |
| **11 — Bypass** | Off | On |

Toggle 7 is a **mode selector** controlling the colour pair used for stereoscopic encoding. The VHD implements a single-bit mode (0=Red/Cyan, 1=Green/Magenta). Toggle 8 swaps left and right eye assignments, reversing the depth direction. Toggle 9 forces a mono depth source. Toggle 10 enables an animation counter.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade between the original input video (delayed to match the 12-clock processing pipeline plus 4-clock interpolator) and the anaglyphic stereoscopic output. At 0%, pure unprocessed input. At 100%, fully processed anaglyph rendering.





---

## Guided Exercises

These exercises progress from basic depth mapping through stereo configuration to colour mode exploration, demonstrating how to create effective stereoscopic imagery from 2D sources.

### Exercise 1: Basic Depth Mapping

<BeforeAfterSlider
  sources={[
    { label: "Runner", before: anaglyph_source1_runner, after: anaglyph_ex1_s1 },
    { label: "Field", before: anaglyph_source2_field, after: anaglyph_ex1_s2 },
    { label: "Clouds", before: anaglyph_source3_clouds, after: anaglyph_ex1_s3 },
    { label: "Pattern", before: anaglyph_source4_pattern, after: anaglyph_ex1_s4 },
    { label: "Man", before: anaglyph_source5_man, after: anaglyph_ex1_s5 },
    { label: "Wood", before: anaglyph_source6_wood, after: anaglyph_ex1_s6 },
  ]}
/>
*Basic Depth Mapping — simulated result across source images.*
**Source**: Landscape or scene with clear brightness gradients (bright foreground, dark background or vice versa).

**What You'll Create**: Understand how luminance-as-depth creates horizontal displacement and how the basic stereo parameters interact.

1. **Start moderate**: Set Depth Amt to ~50%, Separation to ~40%, Converge to ~50%. Tint Str at ~75%.
2. **Observe displacement**: Look at the image — you should see a slight red/cyan fringe around bright objects. This fringe IS the stereo separation.
3. **Increase depth**: Push Depth Amt to ~80%. The red/cyan fringing becomes more pronounced — bright areas shift more.
4. **Adjust convergence**: Move Converge below 50%. Notice how the fringe pattern shifts — objects at mid-brightness now have less fringe.
5. **Try red/cyan glasses**: If available, put on red/cyan glasses. The bright foreground pops forward, dark background recedes.
6. **Full mix**: Set Mix to 100%.

**Key concepts**: Luminance-as-depth mapping, horizontal displacement, convergence plane, inter-eye separation

---

### Exercise 2: Depth Direction and Separation

<BeforeAfterSlider
  sources={[
    { label: "Runner", before: anaglyph_source1_runner, after: anaglyph_ex2_s1 },
    { label: "Field", before: anaglyph_source2_field, after: anaglyph_ex2_s2 },
    { label: "Clouds", before: anaglyph_source3_clouds, after: anaglyph_ex2_s3 },
    { label: "Pattern", before: anaglyph_source4_pattern, after: anaglyph_ex2_s4 },
    { label: "Man", before: anaglyph_source5_man, after: anaglyph_ex2_s5 },
    { label: "Wood", before: anaglyph_source6_wood, after: anaglyph_ex2_s6 },
  ]}
/>
*Depth Direction and Separation — simulated result across source images.*
**Source**: High-contrast image with both bright and dark areas.

**What You'll Create**: Explore how swapping the depth direction changes the 3D perception and how separation controls the stereo intensity.

1. **Set moderate depth**: Depth Amt ~60%, Separation ~50%, Converge ~50%.
2. **Bright Near mode**: Depth Dir set to Bright Near. Bright areas separate outward (closer).
3. **Swap to Bright Far**: Toggle Depth Dir. Now dark areas appear closer — completely different depth reading of same image.
4. **Reduce separation**: Drop Separation to ~20%. The stereo effect becomes very subtle.
5. **Maximum separation**: Push Separation to ~90%. Dramatic split — left and right eye views are clearly visible as separate ghost images.
6. **Find comfortable range**: Bring Separation back to ~35-45% for comfortable viewing with glasses.

**Key concepts**: Depth direction inversion, separation as stereo magnifier, comfortable viewing range

---

### Exercise 3: Green/Magenta Mode and Brightness Compensation

<BeforeAfterSlider
  sources={[
    { label: "Runner", before: anaglyph_source1_runner, after: anaglyph_ex3_s1 },
    { label: "Field", before: anaglyph_source2_field, after: anaglyph_ex3_s2 },
    { label: "Clouds", before: anaglyph_source3_clouds, after: anaglyph_ex3_s3 },
    { label: "Pattern", before: anaglyph_source4_pattern, after: anaglyph_ex3_s4 },
    { label: "Man", before: anaglyph_source5_man, after: anaglyph_ex3_s5 },
    { label: "Wood", before: anaglyph_source6_wood, after: anaglyph_ex3_s6 },
  ]}
/>
*Green/Magenta Mode and Brightness Compensation — simulated result across source images.*
**Source**: Colourful subject with varied hues — flowers, artwork, or coloured fabrics.

**What You'll Create**: Compare Red/Cyan vs Green/Magenta colour separation and understand brightness compensation for glasses viewing.

1. **Red/Cyan baseline**: Mode set to Red/Cyan. Moderate all depth parameters.
2. **Observe colour loss**: Note how the red/cyan tint desaturates some original colours. Red objects look especially affected.
3. **Switch to Green/Magenta**: Toggle Mode. The colour palette shifts — greens and magentas now carry the separation instead.
4. **Compare colour fidelity**: Toggle back and forth between modes. Green/Magenta often preserves more of the original colour range.
5. **Adjust brightness**: With glasses on, the image appears dimmer. Increase Brightness above 50% to compensate.
6. **High tint strength**: Push Tint Str to ~90%. The colour separation is vivid — very strong effect.
7. **Low tint strength**: Pull Tint Str to ~30%. Subtle separation — the effect is primarily a brightness shift, less colour.

**Key concepts**: Red/Cyan vs Green/Magenta encoding, colour fidelity trade-offs, brightness compensation for coloured filter glasses

---


## Tips

- **Dark subjects need Bright Far**: If your subject is dark against a bright background, toggle Depth Dir to Bright Far for a more natural depth relationship.
- **Brightness compensation**: Colour filter glasses typically reduce brightness by 40-60%. Increase the Brightness pot above 50% to compensate.
- **Tint strength is creative**: At moderate tint (50-75%), the effect is functional for 3D. At extreme tint, the red/cyan colour separation becomes an artistic aesthetic even without glasses.
- **Works best with high-contrast sources**: The depth mapping is most effective when the source has strong brightness gradients between foreground and background.
- **Edge Boost sharpens depth boundaries**: A small amount of Edge Boost (10-20%) clarifies where depth transitions occur, creating crisper separation between near and far planes.

---

## Glossary

| Term | Definition |
|------|------------|
| **Anaglyphic 3D** | A stereoscopic display technique encoding left-eye and right-eye views in complementary colours (e.g. red and cyan) so that colour-filter glasses separate them for depth perception. |
| **Binocular Disparity** | The slight difference between the images seen by the left and right eyes; the brain interprets this difference as depth information. |
| **Convergence** | The point in a stereoscopic image where left-eye and right-eye views overlap perfectly (zero parallax); objects at this distance appear on the screen plane. |
| **Depth Map** | A representation where each pixel's brightness encodes its relative distance from the viewer; Anaglyph derives this from the source luminance. |
| **Line Buffer** | FPGA block RAM storing one scanline of pixel data; Anaglyph uses six ping-pong line buffers (Y, U, V for each virtual eye). |
| **Luminance (Luma)** | The Y channel of a YUV signal, representing brightness independent of colour. |
| **Parallax** | The apparent horizontal shift of an object when viewed from two different positions; positive parallax places objects behind the screen, negative parallax places them in front. |
| **Ping-Pong Buffer** | A double-buffering scheme where one buffer is written while the other is read, then the roles swap each line, preventing read/write conflicts. |
| **Stereoscopic** | A technique that creates the illusion of three-dimensional depth by presenting slightly different images to each eye. |
| **Wet/Dry** | A mixing convention where "wet" is the fully processed signal and "dry" is the unprocessed original; the fader crossfades between them. |
| **Zero-Parallax Plane** | The virtual depth at which left and right eye views align exactly; objects here appear to sit on the screen surface, while nearer objects pop forward and farther objects recede. |

---
