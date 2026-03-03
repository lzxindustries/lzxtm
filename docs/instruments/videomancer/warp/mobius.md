---
draft: true
sidebar_position: 195
slug: /instruments/videomancer/mobius
title: "Mobius"
image: /img/instruments/videomancer/mobius/mobius_hero_s1.png
description: "Mobius maps video onto the surface of a Möbius strip — a one-sided topological surface created by taking a rectangular band, giving it a half-twist, and joining the ends."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import mobius_source1_fruit from '/img/instruments/videomancer/mobius/mobius_source1_fruit.png';
import mobius_source2_ballerina from '/img/instruments/videomancer/mobius/mobius_source2_ballerina.png';
import mobius_source3_clouds from '/img/instruments/videomancer/mobius/mobius_source3_clouds.png';
import mobius_source4_pattern from '/img/instruments/videomancer/mobius/mobius_source4_pattern.png';
import mobius_source5_boy from '/img/instruments/videomancer/mobius/mobius_source5_boy.png';
import mobius_source6_knit from '/img/instruments/videomancer/mobius/mobius_source6_knit.png';
import mobius_hero_s1 from '/img/instruments/videomancer/mobius/mobius_hero_s1.png';
import mobius_hero_s2 from '/img/instruments/videomancer/mobius/mobius_hero_s2.png';
import mobius_hero_s3 from '/img/instruments/videomancer/mobius/mobius_hero_s3.png';
import mobius_hero_s4 from '/img/instruments/videomancer/mobius/mobius_hero_s4.png';
import mobius_hero_s5 from '/img/instruments/videomancer/mobius/mobius_hero_s5.png';
import mobius_hero_s6 from '/img/instruments/videomancer/mobius/mobius_hero_s6.png';
import mobius_ex1_s1 from '/img/instruments/videomancer/mobius/mobius_ex1_s1.png';
import mobius_ex1_s2 from '/img/instruments/videomancer/mobius/mobius_ex1_s2.png';
import mobius_ex1_s3 from '/img/instruments/videomancer/mobius/mobius_ex1_s3.png';
import mobius_ex1_s4 from '/img/instruments/videomancer/mobius/mobius_ex1_s4.png';
import mobius_ex1_s5 from '/img/instruments/videomancer/mobius/mobius_ex1_s5.png';
import mobius_ex1_s6 from '/img/instruments/videomancer/mobius/mobius_ex1_s6.png';
import mobius_ex2_s1 from '/img/instruments/videomancer/mobius/mobius_ex2_s1.png';
import mobius_ex2_s2 from '/img/instruments/videomancer/mobius/mobius_ex2_s2.png';
import mobius_ex2_s3 from '/img/instruments/videomancer/mobius/mobius_ex2_s3.png';
import mobius_ex2_s4 from '/img/instruments/videomancer/mobius/mobius_ex2_s4.png';
import mobius_ex2_s5 from '/img/instruments/videomancer/mobius/mobius_ex2_s5.png';
import mobius_ex2_s6 from '/img/instruments/videomancer/mobius/mobius_ex2_s6.png';
import mobius_ex3_s1 from '/img/instruments/videomancer/mobius/mobius_ex3_s1.png';
import mobius_ex3_s2 from '/img/instruments/videomancer/mobius/mobius_ex3_s2.png';
import mobius_ex3_s3 from '/img/instruments/videomancer/mobius/mobius_ex3_s3.png';
import mobius_ex3_s4 from '/img/instruments/videomancer/mobius/mobius_ex3_s4.png';
import mobius_ex3_s5 from '/img/instruments/videomancer/mobius/mobius_ex3_s5.png';
import mobius_ex3_s6 from '/img/instruments/videomancer/mobius/mobius_ex3_s6.png';

# Mobius

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: mobius_source1_fruit, after: mobius_hero_s1 },
    { label: "Ballerina", before: mobius_source2_ballerina, after: mobius_hero_s2 },
    { label: "Clouds", before: mobius_source3_clouds, after: mobius_hero_s3 },
    { label: "Pattern", before: mobius_source4_pattern, after: mobius_hero_s4 },
    { label: "Boy", before: mobius_source5_boy, after: mobius_hero_s5 },
    { label: "Knit", before: mobius_source6_knit, after: mobius_hero_s6 },
  ]}
/>
*Mobius applying a progressive half-twist warp to a landscape source — the image folds over itself with luma inversion and chroma rotation revealing a seamless topological surface.*

---

## Overview

Mobius maps video onto the surface of a Möbius strip — a one-sided topological surface created by taking a rectangular band, giving it a half-twist, and joining the ends. In the FPGA, this is realized as a per-scanline coordinate transform: each row of pixels is displaced horizontally by an amount that varies smoothly from zero at the twist center to a full mirror-flip at the frame edges. Combined with progressive luma inversion and chroma hue rotation that track the twist phase, the result is a continuous surface where top and bottom blend seamlessly into each other through a twist that inverts brightness and rotates color.

The name references the Möbius strip discovered by August Ferdinand Möbius in 1858 — a surface with only one side and one edge. If you trace a finger along a Möbius strip, you return to the starting point having traversed both "sides" without ever crossing an edge. The program recreates this disorienting continuity: the image appears to fold over itself, with what was dark becoming light and what was blue becoming orange as you follow the twist around the frame.

At conservative settings — low twist rate, no animation — the effect is a subtle horizontal displacement that makes the image appear gently warped, like a reflection in a slightly curved mirror. At extreme settings — high twist rate, full inversion depth, active hue rotation, animation enabled — the frame becomes a writhing, color-shifting topological illusion where the boundary between original and transformed imagery dissolves.

---

## Background

### What Is a Möbius Strip?

A **Möbius strip** is the simplest non-orientable surface. Take a strip of paper, give one end a 180° twist (a half-twist), and tape the ends together. The result is a loop with the remarkable property that it has only one continuous side. In three dimensions, a Möbius strip is a two-dimensional surface embedded in three-dimensional space; it cannot exist without the twist.

This program simulates the visual effect of mapping a flat 2D image onto this twisted surface. Imagine printing a photograph on a long strip of transparent film, giving it a half-twist, and joining the ends into a loop. Looking at the loop from the front, the image gradually transitions from its normal orientation at one point to a mirror-reversed, brightness-inverted version at the opposite point — and then back again. The twist rate parameter controls how many half-twists fit across the frame.

### What Is a DDS Phase Accumulator?

The animation system uses a **Direct Digital Synthesis** (DDS) phase accumulator — a counter that increments by a fixed step value every frame. When the counter overflows its register width, it wraps around, producing a continuously advancing phase angle. This phase is used to scroll the twist pattern across the frame, creating the illusion of the Möbius surface rotating. The AnimSpd register controls the step size: larger steps produce faster scrolling, and zero disables animation entirely.

### What Is a Triangle Wave?

The twist displacement follows a **triangle wave** profile across the vertical axis — linearly increasing from zero at the twist center to a maximum at the edges, then linearly decreasing back. This produces a smooth, continuous displacement that is zero at the center of the twist and maximal at the extremes. Unlike a sine wave, the triangle wave has constant slope, creating a uniform shear effect rather than the accelerating/decelerating displacement of sinusoidal warping.

### What Is Quadrant-Based Hue Rotation?

The chroma rotation in Mobius uses a **quadrant-based** approach to transform the U and V color components. The twist phase at each scanline determines a rotation angle, and the U/V pair is rotated in the color plane by that angle. This is implemented approximately using sign flips and interpolation rather than trigonometric functions — the colour plane is divided into quadrants, and within each quadrant a linear interpolation approximates the sine/cosine relationship. The result is a smooth but computationally efficient hue shift that tracks the twist progression.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── DDS Phase Accumulator ──────────────────────────────────────
│   │
│   └─ 1. Per-frame phase increment (auto-scroll)
│            ◄── AnimSpd (reg 5), Animate (toggle bit 0)
│
├── Per-Scanline Twist Computation ─────────────────────────────
│   │
│   ├─ 2. Compute twist phase = (scanline - TwstCntr) × TwstRate + DDS
│   │        ◄── TwstRate (reg 0), TwstCntr (reg 1)
│   ├─ 3. Triangle wave fold → displacement magnitude
│   └─ 4. Mirror/non-mirror from twist phase sign
│            ◄── Mode (toggle bit 1)
│
├── Y Channel ──────────────────────────────────────────────────
│   │
│   ├─ 5. Horizontal pixel displacement (coordinate warp)
│   ├─ 6. Luma inversion blend: Y' = Y × (1 − inv) + (1 − Y) × inv
│   │        ◄── InvDepth (reg 2)
│   └─ 7. Seam line overlay (at twist boundary)
│            ◄── SeamWdth (reg 4), Seam (toggle bit 2)
│
├── U/V Channels ───────────────────────────────────────────────
│   │
│   ├─ 5. Same horizontal displacement as Y
│   ├─ 6. Quadrant-based hue rotation per scanline
│   │        ◄── Hue Rot (reg 3), Channels (toggle bit 3)
│   └─ 7. Seam chroma (neutral at seam lines)
│
├── Output Mixing ──────────────────────────────────────────────
│   └─ 8. Interpolator wet/dry mix
│            ◄── Mix (reg 7)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Pass-through (hsync, vsync, field, avid)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
         ◄── Bypass (toggle bit 4)
```

The key interaction is between the twist displacement and the luma inversion / chroma rotation. The displacement alone produces a warp effect — pixels slide horizontally. But the inversion and hue rotation track the same twist phase, so as the image warps it also inverts and shifts in color. This coupling is what creates the Möbius illusion: a surface that continuously transitions through itself. The seam line marks the boundary where the twist phase wraps, providing a visible reference for the topological discontinuity.

---

## Parameter Reference


### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — TwstRate
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Controls the number of half-twists mapped across the vertical extent of the frame. At minimum, the twist is subtle — a gentle shear that barely displaces pixels. At maximum, multiple full twists compress into the frame height, creating a tight zigzag displacement pattern where the image folds over itself many times. Each half-twist introduces one inversion boundary, so higher twist rates produce more alternating bands of normal and inverted imagery.

---

#### Knob 2 — TwstCntr
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the vertical center point of the twist. At 50%, the twist is centered in the frame — equal displacement above and below the midpoint. Moving the center toward the top or bottom shifts the entire twist pattern vertically, creating asymmetric warping where one half of the frame is more displaced than the other. This is equivalent to translating the Möbius strip vertically relative to the viewing window.

---

#### Knob 3 — InvDepth
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the depth of the luminance inversion that tracks the twist phase. At minimum, no inversion occurs — the twist warps pixel positions but leaves brightness unchanged. As InvDepth increases, scanlines at the peak of the twist progressively invert their luminance: midtones stay constant, highlights darken, shadows brighten. At maximum, scanlines at the twist apex are fully inverted. The inversion blends linearly with the twist displacement, creating a smooth transition from normal to inverted.

---

#### Knob 4 — Hue Rot
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls how strongly the chroma (U/V) rotates with the twist phase. At minimum, color is unaffected by the twist. As the value increases, scanlines at peak twist undergo progressive hue rotation — blues shift toward red, reds shift toward green, following the quadrant-based rotation. At maximum, a full 180° hue rotation occurs at the twist apex, complementing the luma inversion to create a complete color negative at the most twisted points.

---

#### Knob 5 — SeamWdth
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 13% |
| Suffix | % |

Controls the width of the visible seam line drawn at the twist boundary — the point where the twist phase wraps from one cycle to the next. At minimum, the seam is a single pixel or invisible. At maximum, a wide bright band marks the boundary. The seam serves as a visual reference for the topological discontinuity and can be used as a design element — a bright horizon line dividing the twisted zones.

---

#### Knob 6 — AnimSpd
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Controls the DDS phase increment for auto-scrolling animation. At minimum, the twist pattern is either static (Animate off) or scrolls imperceptibly slowly. At maximum, the twist pattern races vertically through the frame, creating a rapid rolling-shutter-like effect as different scanlines cycle through their twist phases. Moderate values produce a gentle, mesmerizing drift of the twist pattern.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Animate** | Off | On |
| **8 — Mode** | Full | Mirror |
| **9 — Seam** | Hard | Soft |
| **10 — Channels** | YUV | Y Only |
| **11 — Bypass** | Off | On |

Toggle 7 enables animation, Toggle 8 selects between full Möbius warp and mirror-only mode, Toggle 9 controls seam hardness, Toggle 10 limits processing to luma-only or full YUV, and Toggle 11 is the standard bypass. The Mode toggle has the most dramatic visual effect — mirror-only removes the horizontal displacement and color transform, leaving only the vertical reflection.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry mix between the processed Möbius output and the original input. At 100%, the full twist effect is visible. At 0%, the original input passes through unmodified. Intermediate values blend the warped and unwarped imagery, creating a ghostly double-exposure where the twisted version overlays the original at reduced opacity.

---

## Guided Exercises

These exercises progressively build the Möbius effect from simple displacement through full topological illusion, each adding one dimension of the transform.

### Exercise 1: The Basic Twist

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: mobius_source1_fruit, after: mobius_ex1_s1 },
    { label: "Ballerina", before: mobius_source2_ballerina, after: mobius_ex1_s2 },
    { label: "Clouds", before: mobius_source3_clouds, after: mobius_ex1_s3 },
    { label: "Pattern", before: mobius_source4_pattern, after: mobius_ex1_s4 },
    { label: "Boy", before: mobius_source5_boy, after: mobius_ex1_s5 },
    { label: "Knit", before: mobius_source6_knit, after: mobius_ex1_s6 },
  ]}
/>
*The Basic Twist — simulated result across source images.*
**Source**: A static image or camera feed with strong horizontal and vertical features — architecture, grid patterns, or text.

**Objective**: Understand how TwstRate and TwstCntr produce horizontal displacement that varies across the frame.

1. **Minimal twist**: Set TwstRate to ~10%, TwstCntr to ~50% (centered). The image has a subtle horizontal shear — straight vertical lines bend gently.
2. **Increase twist**: Sweep TwstRate to ~40%. Vertical lines develop a visible S-curve as the displacement increases.
3. **Multiple twists**: Push TwstRate to ~80%. The image folds over itself — multiple bands of image appear, each shifted horizontally by a different amount.
4. **Move the center**: Sweep TwstCntr from 0% to 100%. The twist pattern slides vertically. At the extremes, the maximum displacement is near one edge of the frame.
5. **Observe boundaries**: Note where the displacement wraps — this is where the seam line will appear once enabled.

**Key concepts**: TwstRate controls the number of half-twists, TwstCntr shifts the twist vertically, displacement follows a triangle wave profile, vertical lines reveal the warp most clearly

---

### Exercise 2: Adding Inversion and Color

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: mobius_source1_fruit, after: mobius_ex2_s1 },
    { label: "Ballerina", before: mobius_source2_ballerina, after: mobius_ex2_s2 },
    { label: "Clouds", before: mobius_source3_clouds, after: mobius_ex2_s3 },
    { label: "Pattern", before: mobius_source4_pattern, after: mobius_ex2_s4 },
    { label: "Boy", before: mobius_source5_boy, after: mobius_ex2_s5 },
    { label: "Knit", before: mobius_source6_knit, after: mobius_ex2_s6 },
  ]}
/>
*Adding Inversion and Color — simulated result across source images.*
**Source**: Footage with distinct bright and dark regions and saturated colors — sunset skies, neon signage, or color bars.

**Objective**: See how luma inversion and chroma rotation coupled to the twist phase create the continuity illusion of a Möbius surface.

1. **Start with twist**: Set TwstRate to ~35%, TwstCntr to ~50%, Mode off (full Möbius).
2. **Add inversion**: Slowly increase InvDepth from 0 to ~70%. Watch as scanlines at the twist peak progressively invert — bright areas darken, dark areas brighten, creating a smooth negative-positive transition across the frame.
3. **Add hue rotation**: Increase Hue Rot to ~60%. Colors shift at the twist peak — reds become blue-green, blues become orange. The combined inversion and hue shift creates a complete color negative at maximum twist.
4. **Enable seam**: Increase SeamWdth to ~30%. A bright line appears at the twist boundary, marking where the surface "joins."
5. **Soft seam**: Toggle Seam (Toggle 9) to soft mode. The seam line blends into the image.
6. **Y-only mode**: Toggle Channels (Toggle 10) on. Hue rotation disables — only the luma inversion remains. The structural twist is preserved but original colors survive.

**Key concepts**: Luma inversion tracks twist phase creating continuous surface illusion, chroma rotation complements inversion, seam marks the topological join, Y-only preserves original color

---

### Exercise 3: Animated Rotation

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: mobius_source1_fruit, after: mobius_ex3_s1 },
    { label: "Ballerina", before: mobius_source2_ballerina, after: mobius_ex3_s2 },
    { label: "Clouds", before: mobius_source3_clouds, after: mobius_ex3_s3 },
    { label: "Pattern", before: mobius_source4_pattern, after: mobius_ex3_s4 },
    { label: "Boy", before: mobius_source5_boy, after: mobius_ex3_s5 },
    { label: "Knit", before: mobius_source6_knit, after: mobius_ex3_s6 },
  ]}
/>
*Animated Rotation — simulated result across source images.*
**Source**: Moving footage — dancers, traffic, flowing water — material where the twist animation interacts with the source motion.

**Objective**: Combine animation with the full twist to create a continuously evolving topological warp.

1. **Full Möbius**: Set TwstRate ~25%, InvDepth ~50%, Hue Rot ~40%, SeamWdth ~20%.
2. **Enable animation**: Toggle Animate on (Toggle 7). Set AnimSpd to ~15%.
3. **Observe drift**: The twist pattern scrolls vertically — the inverted/rotated bands move smoothly through the frame like a barber pole stripe.
4. **Increase speed**: Push AnimSpd to ~50%. The twist cycles rapidly. The source video appears to roll through the twisted surface.
5. **Mirror mode**: Toggle Mode (Toggle 8) to mirror-only. The horizontal displacement and color transforms disappear — only a vertically scrolling mirror remains. This is a simpler, kaleidoscopic variant.
6. **Return to full Möbius**: Toggle Mode back off. Compare the full topological effect with the simpler mirror.
7. **Mix down**: Sweep Mix to ~50%. The twisted version ghosts over the original, creating a double-exposure composite.

**Key concepts**: DDS animation scrolls the twist pattern vertically, AnimSpd controls scroll rate, Mode toggle adds/removes the displacement and color transforms, Mix blends twisted with original

---


## Tips

- **TwstRate is the primary shape control**: Low rates create subtle warps; high rates create dense, folded structures. Start low and increase gradually to find the sweet spot.
- **InvDepth reveals the topology**: Without inversion, the twist is just a spatial warp. With inversion, the continuous surface nature of the Möbius strip becomes visible — you can "see" the twist through the brightness transition.
- **Animation makes it hypnotic**: Enable Animate and set AnimSpd to a slow value (~10–20%). The twist scrolls through the frame like a rotating surface, creating a mesmerizing barber-pole motion.
- **Mirror mode simplifies**: Toggle Mode to mirror-only when you want vertical kaleidoscope symmetry without the displacement and color transforms.
- **Seam as design element**: The seam line marks the topological join. Make it wide and bright for a structural dividing line, or thin/invisible for seamless flow.
- **Y-only preserves source color**: Toggle Channels on to keep original chrominance while still getting the structural twist and luma inversion — useful for sources where color is critical.
- **Feedback creates infinite corridors**: Route the output back to the input. The twist feeding on itself creates recursive displacements that converge into complex interference patterns.
- **Combine with other programs**: The Möbius warp is a geometric transform that chains well with colorizers and texture generators. Route through a posterizer or ditherer before Mobius for unique interactions.

---

## Glossary

| Term | Definition |
|------|------------|
| **BT.601** | ITU-R BT.601 color space standard defining the YUV encoding matrix used in standard-definition video and throughout the Videomancer pipeline. |
| **Chroma** | The color components (U and V) of a YUV video signal, encoding hue and saturation independently of brightness. |
| **DDS** | Direct Digital Synthesis; a technique using an incrementing phase accumulator to generate periodic waveforms or scrolling animations. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit executing the video pipeline in hardware. |
| **Half-Twist** | A 180° rotation of a strip before joining the ends, creating the non-orientable Möbius surface. |
| **Hue Rotation** | Rotating the (U, V) color vector in the chroma plane, shifting all colors toward different parts of the spectrum. |
| **Interpolator** | A DSP module that linearly blends between two signals based on a mix parameter. |
| **Luma** | The brightness component (Y) of a YUV video signal. |
| **Möbius Strip** | A non-orientable surface with only one side and one edge, formed by giving a rectangular strip a half-twist and joining the ends. |
| **Pipeline** | A chain of processing stages each completing one operation per clock cycle. |
| **Triangle Wave** | A periodic waveform with constant-slope linear ramps, used here for the twist displacement profile. |
| **YUV** | A color encoding separating luminance (Y) from chrominance (U, V); Videomancer processes all video in YUV 4:4:4 at 30-bit depth. |

---
