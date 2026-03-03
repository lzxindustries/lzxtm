---
draft: true
sidebar_position: 120
slug: /instruments/videomancer/fresnel
title: "Fresnel"
image: /img/instruments/videomancer/fresnel/fresnel_hero.png
description: "A Fresnel zone plate is one of the oldest optical test patterns — concentric rings whose spacing decreases with distance from the center, following a square-root law."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import fresnel_hero from '/img/instruments/videomancer/fresnel/fresnel_hero.png';
import fresnel_control_panel from '/img/instruments/videomancer/fresnel/fresnel_control_panel.png';
import fresnel_exercise1_result from '/img/instruments/videomancer/fresnel/fresnel_exercise1_result.png';
import fresnel_exercise2_result from '/img/instruments/videomancer/fresnel/fresnel_exercise2_result.png';
import fresnel_exercise3_result from '/img/instruments/videomancer/fresnel/fresnel_exercise3_result.png';
import fresnel_source1_kodim15 from '/img/instruments/videomancer/fresnel/fresnel_source1_kodim15.png';
import fresnel_source2_kodim01 from '/img/instruments/videomancer/fresnel/fresnel_source2_kodim01.png';
import fresnel_source3_kodim01_bw from '/img/instruments/videomancer/fresnel/fresnel_source3_kodim01_bw.png';

# Fresnel

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: fresnel_source1_kodim15, after: fresnel_hero },
    { label: "Kodim01", before: fresnel_source2_kodim01, after: fresnel_hero },
    { label: "Kodim01 B&W", before: fresnel_source3_kodim01_bw, after: fresnel_hero },
  ]}
/>
*Fresnel zone plate interference rings radiating from a displaced center, with dual-source moire and video-tinted coloring.*

---

## Overview

A Fresnel zone plate is one of the oldest optical test patterns — concentric rings whose spacing decreases with distance from the center, following a square-root law. Fresnel generates this pattern digitally by computing the squared radial distance r² = dx² + dy² for every pixel on every frame, then extracting a single bit from that value to determine whether the pixel belongs to a bright ring or a dark ring. Because the bit positions of r² cycle at rates proportional to the square root of the distance, the rings naturally bunch together as they move outward, producing the distinctive zone plate look without any trigonometric functions or lookup tables.

The program adds several layers of control on top of the raw zone plate. The center can be repositioned anywhere on screen. A second zone plate, mirrored about the screen center, can be XORed with the first to produce moire interference fringes. The rings can be animated — an accumulating phase offset added to r² before bit selection makes the rings expand outward continuously. And the ring pattern can be colorized by passing the source video's chrominance through the bright zones while desaturating the dark zones, turning the geometric pattern into a video-driven color mask.

The name references Augustin-Jean Fresnel, the French physicist whose work on wave optics and diffraction gave us the zone plate construction. In Videomancer's signal chain, Fresnel serves as both a standalone pattern generator and a structured keying mask — its rings carve the input video into concentric regions with independently adjustable brightness and contrast.

---

## Background

### Fresnel Zone Plates in Optics

A Fresnel zone plate is a flat optical element consisting of concentric rings that alternate between transparent and opaque. Each ring boundary falls at a radius where the optical path length from a point source changes by half a wavelength. This means the transparent zones all contribute constructively at the focal point, and the plate acts as a lens — focusing light by diffraction rather than refraction. Zone plates were first described by Fresnel in the early 19th century and are used today in X-ray microscopy, radio telescopes, and lithography masks where conventional glass lenses are impractical.

### The r² Principle

The key mathematical property is that the zone boundaries fall at radii proportional to the square root of successive integers: r_n = √(n · λ · f), where λ is the wavelength and f is the focal length. Equivalently, the zone number at radius r is proportional to r². This is exactly what the VHDL computes: r² = dx² + dy², a simple sum of squared pixel distances. The zone assignment comes from examining a single bit of this sum — if the bit is 1 the pixel is in a bright zone, if 0 it is in a dark zone. Different bit positions select different spatial frequencies: higher bits give wider rings (low frequency), lower bits give tighter rings (high frequency). The entire zone plate pattern emerges from one addition, two multiplications, and a bit extraction — no sine waves, no square roots, no lookup tables.

### Moire from Dual Sources

When two periodic patterns are overlaid with a slight offset, their interaction produces a third pattern at a much lower spatial frequency — a moire. In Fresnel, enabling the Dual Source toggle creates a second zone plate centered at the mirror image of the primary center (reflected about the screen midpoint). The XOR of the two binary ring patterns produces interference fringes that move dynamically as you reposition the primary center. Because the zone plate spacing is non-uniform, the moire fringes are not simple straight lines — they form hyperbolic curves that sweep and rotate as the two centers shift relative to each other.

### Zone Plate Photography and Holography

Zone plates have a long history as photographic tools. Photographers have used pinhole zone plate filters to create soft-focus effects with characteristic ring-shaped bokeh. In holography, zone plates are the simplest possible hologram — a recording of the interference between a point source and a plane reference wave. Fresnel's digital zone plate is functionally identical: it encodes the wavefront from a virtual point source as a binary amplitude pattern. The Dual Source mode extends this to two-point interference, producing the same fringe patterns that appear in two-beam holographic recordings.

### Binary vs Sinusoidal Gratings

The VHDL implementation produces a strictly binary zone plate — each pixel is either bright or dark, with a hard edge between zones. A true optical zone plate modulated as a sinusoidal grating would produce smoother, anti-aliased transitions and suppress higher-order diffraction. The TOML exposes Mode labels (Binary, Sine, Chirp, Gabor) suggesting future extensions, but the current implementation uses only the binary form. The hard-edged binary pattern has its own aesthetic: it emphasizes the geometric structure and creates sharp contrast boundaries that interact strongly with downstream video processing.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Parameter Pre-Registration ─────────────────────────────────
│   ├─ Center X/Y → 12-bit pixel coordinates (cx, cy)
│   ├─ Dual Center → mirrored coordinates (cx2, cy2)
│   ├─ Ring Scale → bit index (9–22) via threshold table
│   ├─ Brightness + Video Mod → ring bright/dark levels
│   └─ Anim Speed → phase accumulator (when Anim = On)
│
├── Stage 1: Input Register ────────────────────────────────────
│   └─ Latch Y, U, V + pixel position counters (h_count, v_count)
│
├── Stage 2: Distance Computation ──────────────────────────────
│   ├─ dx = h_count − cx,  dy = v_count − cy   (primary)
│   └─ dx2 = h_count − cx2, dy2 = v_count − cy2 (secondary)
│
├── Stage 3: Squared Distance (13×13 multiply) ─────────────────
│   ├─ r²  = dx²  + dy²   (24-bit, primary)
│   └─ r²b = dx2² + dy2²  (24-bit, secondary)
│
├── Stage 4: Bit Selection + Animation ─────────────────────────
│   ├─ r² += anim_offset (expanding rings)
│   ├─ ring_a = r²(bit_sel),  ring_b = r²b(bit_sel)
│   ├─ Dual Source: ring = ring_a XOR ring_b
│   └─ Mode (Invert): ring = NOT ring
│
├── Stage 5: Pattern Compose ───────────────────────────────────
│   ├─ Y: ring=1 → ring_bright, ring=0 → ring_dark
│   ├─ Fill (Color):  ring=1 → pass source U/V
│   │                 ring=0 → desaturate toward mid-chroma
│   └─ Fill (Mono):   U = V = 512
│
├── Stage 6–10: Interpolator Mix (4 clocks) ────────────────────
│   └─ Y/U/V = lerp(dry, wet, Mix)
│
├── Sync Delay Pipeline (10 clocks) ────────────────────────────
│   └─ hsync_n, vsync_n, field_n, Y/U/V delayed to match
│
└── Output Assignment ──────────────────────────────────────────
    └─ Bypass: select processed or delayed original
```

The core computation is remarkably compact: two 13-bit multiplications and one addition produce the entire zone plate pattern. The bit-selection stage is the spatial frequency control — moving one bit position up or down doubles or halves the ring count across the screen. Animation works by adding an ever-increasing offset to r² before bit extraction, which shifts all zone boundaries outward at a rate set by the Anim Speed pot. The dual-center XOR creates interference because the two zone plates share the same bit index but have different centers, so their ring boundaries only occasionally coincide — everywhere they disagree, the XOR flips polarity, carving moire fringes into the combined pattern.

---

## Parameter Reference

<img src={fresnel_control_panel} alt="Videomancer front panel with Fresnel loaded"/>
*Videomancer's front panel with Fresnel active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Ring Scale
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Selects which bit of the squared radial distance determines ring polarity. Low values choose high-order bits, producing wide rings with few concentric bands visible on screen. High values select lower-order bits, packing more rings into the same area and creating dense, tightly-spaced patterns. The transition between ring counts is discrete — there are 14 distinct steps corresponding to bits 9 through 22 of the 24-bit r² value. Each step roughly doubles the ring count, so small adjustments produce dramatic changes in pattern density.

---

#### Knob 2 — Center X
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the horizontal position of the zone plate center. At midpoint the pattern is centered horizontally on screen. Sweeping left or right moves the concentric rings off-center, revealing the asymmetric ring spacing that is characteristic of off-axis zone plates. When Dual Source is active, this also moves the mirrored secondary center in the opposite direction, causing the moire fringe pattern to shift and rotate.

---

#### Knob 3 — Center Y
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the vertical position of the zone plate center. Combined with Center X, this places the origin of the r² computation anywhere on screen. Moving both center controls simultaneously drags the entire zone plate pattern diagonally. Extreme positions push the center off-screen entirely, leaving only the outermost rings visible — these appear as nearly parallel curved lines rather than closed circles.

---

#### Knob 4 — Anim Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the rate of ring expansion when Anim is enabled. At zero, rings are static even with Anim on. Higher values increase the accumulation rate of the phase offset added to r², making rings expand outward more quickly. At maximum, the rings scroll outward so fast they create a strobing, pulsating texture. This control has no effect when Anim is off.

---

#### Knob 5 — Video Mod
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the contrast range between bright ring zones and dark ring zones. At zero, the bright and dark levels converge to the Brightness value and the rings vanish. Increasing this control spreads the bright level upward and the dark level downward, creating progressively higher contrast rings. At maximum, bright zones reach full white (or clip at 1023) while dark zones drop near black, producing a stark binary pattern. This interacts with Brightness — the contrast range is symmetric around the Brightness level.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the overall brightness of the zone plate pattern. The bright ring level equals Brightness plus half the Video Mod value (clamped to 1023), and the dark ring level equals Brightness minus half the Video Mod value (clamped to 0). At the midpoint with moderate Video Mod, rings appear as mid-gray and dark bands. Turning Brightness fully up pushes both ring levels toward white; fully down pushes both toward black.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Mode** | Binary | Sine |
| **8 — Fill** | Invert | Tint |
| **9 — Anim** | Off | On |
| **10 — Dual Source** | Off | On |
| **11 — Bypass** | Off | On |

Toggles 7–11 control five independent binary options. Toggle 7 (Mode) inverts ring polarity — swapping which zones are bright and which are dark. Toggle 8 (Fill) switches between monochrome rings and video-colored rings. Toggle 9 (Anim) enables the expanding ring animation. Toggle 10 (Dual Source) activates the second zone plate for moire interference. Toggle 11 (Bypass) routes the input directly to the output. Note that the TOML labels for Toggles 7 and 8 suggest multi-position selectors (Binary/Sine/Chirp/Gabor and Invert/Tint/Key/Add), but the current VHDL implementation reads only one bit from each, providing two-state on/off behavior.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade between the original input video and the processed zone plate output. At 0% the output is the unmodified source. At 100% the output is the full zone plate effect. Intermediate positions blend the two, which is especially useful with color rings enabled — partial mix overlays transparent zone plate bands on the source video.

---

## Guided Exercises

These exercises build from a basic zone plate through dual-source moire to video-integrated color masking. Each exercise uses a different combination of controls to explore the program's range.

### Exercise 1: Basic Zone Plate

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: fresnel_source1_kodim15, after: fresnel_exercise1_result },
    { label: "Kodim01", before: fresnel_source2_kodim01, after: fresnel_exercise1_result },
    { label: "Kodim01 B&W", before: fresnel_source3_kodim01_bw, after: fresnel_exercise1_result },
  ]}
/>
*Basic Zone Plate — simulated result across source images.*
**Source**: A static test pattern or color bars — any clean signal that lets you see the ring structure clearly.

**Objective**: Understand how Ring Scale, Center X/Y, and Brightness/Video Mod interact to create and control a Fresnel zone plate pattern.

1. **Default rings**: With all controls at default, observe the concentric ring pattern centered on screen. Note how rings bunch together toward the edges.
2. **Scale sweep**: Slowly turn Ring Scale from minimum to maximum. Watch the ring count multiply at each step — there are 14 discrete density levels.
3. **Reposition**: Move Center X and Center Y to place the zone plate off-center. Notice how the ring curvature changes as the origin moves toward a screen edge.
4. **Contrast**: Sweep Video Mod from 0 to maximum. At zero the rings vanish; at maximum they are stark black-and-white.
5. **Brightness**: Raise and lower Brightness to shift the overall tonal range of the rings.
6. **Invert**: Toggle Mode to swap bright and dark zones.

**Key concepts**: Zone plate spacing follows sqrt(r), bit selection controls spatial frequency, brightness and contrast set the ring tonal levels

---

### Exercise 2: Dual-Source Moire

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: fresnel_source1_kodim15, after: fresnel_exercise2_result },
    { label: "Kodim01", before: fresnel_source2_kodim01, after: fresnel_exercise2_result },
    { label: "Kodim01 B&W", before: fresnel_source3_kodim01_bw, after: fresnel_exercise2_result },
  ]}
/>
*Dual-Source Moire — simulated result across source images.*
**Source**: A solid color field or gentle gradient — minimal source detail lets the moire structure stand out.

**Objective**: Explore the interference patterns created by XORing two zone plates with different centers.

1. **Enable dual**: Turn on Dual Source (Toggle 10). A second set of rings appears, XORed with the first.
2. **Offset center**: Move Center X slightly off-center. Watch large-scale moire fringes sweep across the screen.
3. **Vertical offset**: Now adjust Center Y. The fringe orientation rotates as the axis between the two centers changes.
4. **Scale interaction**: Change Ring Scale while dual is active. Tighter rings produce finer moire structure; wider rings produce broader fringes.
5. **Animate the moire**: Enable Anim (Toggle 9) and set Anim Speed to about 40%. The expanding rings create a dynamic, pulsating moire.
6. **Invert**: Toggle Mode to swap the moire fringe polarity. Notice how the bright and dark fringes swap everywhere simultaneously.

**Key concepts**: Moire fringes arise from XOR of two non-aligned periodic patterns, fringe spacing and orientation depend on center separation, animation adds temporal dynamics

---

### Exercise 3: Color Zone Mask

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: fresnel_source1_kodim15, after: fresnel_exercise3_result },
    { label: "Kodim01", before: fresnel_source2_kodim01, after: fresnel_exercise3_result },
    { label: "Kodim01 B&W", before: fresnel_source3_kodim01_bw, after: fresnel_exercise3_result },
  ]}
/>
*Color Zone Mask — simulated result across source images.*
**Source**: Live camera feed or richly colored footage — scenes with varied hues make the color masking most visible.

**Objective**: Use the zone plate as a selective color mask that reveals and hides the source video's chrominance in concentric bands.

1. **Enable color**: Turn on Fill (Toggle 8). Bright ring zones now carry the source video's color; dark zones are desaturated.
2. **Partial mix**: Lower Mix to about 60%. The zone plate overlays transparently on the source, creating colored ring bands over the original image.
3. **Reposition**: Move Center X and Center Y to place the zone plate origin over a specific subject. The rings radiate outward from that subject.
4. **Fine scale**: Set Ring Scale high (~80%) for tightly-spaced rings. The video alternates between full color and desaturated narrow bands.
5. **Add dual**: Enable Dual Source to create moire-patterned color masking — the XOR fringes selectively reveal color in complex curved bands.
6. **Animate**: Enable Anim with moderate speed. The color mask bands expand outward continuously, creating a pulsing color-reveal effect.

**Key concepts**: Zone plate as a structured chroma key, partial mix blends mask with source, dual moire creates complex shape masking

---


## Tips

- **Ring Scale is logarithmic in effect**: Each step doubles the ring count. Mid-range settings (bits 14–16) give the most recognizable zone plate patterns.
- **Dual Source is center-sensitive**: Even tiny offsets from center produce large moire fringes. Use Dual Source with Center X/Y near 50% for the most dramatic fringe effects.
- **Color mask technique**: Enable Fill with partial Mix to overlay colored zone rings on source video — the rings act as a structured chroma key.
- **Animation speed matters**: Very high Anim Speed creates a strobing effect. For smooth expansion, keep Anim Speed below 30%.
- **Combine with feedback**: Routing the output back to the input creates recursive zone plate rings that interact with themselves, forming fractal-like nested interference patterns.
- **Zero contrast for flat fields**: Set Video Mod to 0% but leave Mix at 100% to generate a flat field at the Brightness level — useful as a reference or setup tool.
- **Off-screen centers**: Pushing the center off-screen reveals only the outermost ring arcs, which appear as gently curved parallel lines — useful for subtle, non-circular patterns.
- **Bypass for A/B comparison**: Toggle Bypass to instantly compare the raw source with the processed output without changing any settings.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bit Selection** | Extracting a single bit from a binary value to determine a binary outcome; in Fresnel, the bit position within r² determines ring polarity. |
| **BRAM** | Block RAM; dedicated FPGA memory. Fresnel uses 0 BRAMs — the pattern is computed combinatorially. |
| **Chroma** | The color information in a video signal, encoded as U and V components in YUV color space. |
| **Desaturation** | Reducing the color intensity of a pixel by blending its chroma values toward the neutral midpoint (512 in 10-bit YUV). |
| **Fresnel Zone Plate** | An optical element with concentric rings whose spacing follows a square-root law, focusing light by diffraction. |
| **Interpolator** | A pipelined linear-interpolation module that crossfades between two values based on a fractional parameter. |
| **Luma** | The brightness component (Y) of a YUV video signal. |
| **Moire** | A large-scale interference pattern produced when two periodic patterns are overlaid with a slight offset. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **r²** | The squared radial distance from the zone plate center; computed as dx² + dy² without taking the square root. |
| **XOR** | Exclusive OR; a binary operation that returns 1 when its two inputs differ. Used here to combine two zone plate patterns. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |
| **Zone Plate** | Synonym for Fresnel zone plate; a pattern of concentric rings used in optics, photography, and video test signals. |

---
