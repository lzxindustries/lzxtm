---
draft: true
sidebar_position: 236
slug: /instruments/videomancer/prism
title: "Prism"
image: /img/instruments/videomancer/prism/prism_hero_s1.png
description: "Prism takes the three channels of a YUV video signal and shifts each one independently along the horizontal axis."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import prism_control_panel from '/img/instruments/videomancer/prism/prism_control_panel.png';
import prism_source1_fruit from '/img/instruments/videomancer/prism/prism_source1_fruit.png';
import prism_source2_boat from '/img/instruments/videomancer/prism/prism_source2_boat.png';
import prism_source3_elephant from '/img/instruments/videomancer/prism/prism_source3_elephant.png';
import prism_source4_pattern from '/img/instruments/videomancer/prism/prism_source4_pattern.png';
import prism_source5_man from '/img/instruments/videomancer/prism/prism_source5_man.png';
import prism_source6_wood from '/img/instruments/videomancer/prism/prism_source6_wood.png';
import prism_hero_s1 from '/img/instruments/videomancer/prism/prism_hero_s1.png';
import prism_hero_s2 from '/img/instruments/videomancer/prism/prism_hero_s2.png';
import prism_hero_s3 from '/img/instruments/videomancer/prism/prism_hero_s3.png';
import prism_hero_s4 from '/img/instruments/videomancer/prism/prism_hero_s4.png';
import prism_hero_s5 from '/img/instruments/videomancer/prism/prism_hero_s5.png';
import prism_hero_s6 from '/img/instruments/videomancer/prism/prism_hero_s6.png';
import prism_ex1_s1 from '/img/instruments/videomancer/prism/prism_ex1_s1.png';
import prism_ex1_s2 from '/img/instruments/videomancer/prism/prism_ex1_s2.png';
import prism_ex1_s3 from '/img/instruments/videomancer/prism/prism_ex1_s3.png';
import prism_ex1_s4 from '/img/instruments/videomancer/prism/prism_ex1_s4.png';
import prism_ex1_s5 from '/img/instruments/videomancer/prism/prism_ex1_s5.png';
import prism_ex1_s6 from '/img/instruments/videomancer/prism/prism_ex1_s6.png';
import prism_ex2_s1 from '/img/instruments/videomancer/prism/prism_ex2_s1.png';
import prism_ex2_s2 from '/img/instruments/videomancer/prism/prism_ex2_s2.png';
import prism_ex2_s3 from '/img/instruments/videomancer/prism/prism_ex2_s3.png';
import prism_ex2_s4 from '/img/instruments/videomancer/prism/prism_ex2_s4.png';
import prism_ex2_s5 from '/img/instruments/videomancer/prism/prism_ex2_s5.png';
import prism_ex2_s6 from '/img/instruments/videomancer/prism/prism_ex2_s6.png';
import prism_ex3_s1 from '/img/instruments/videomancer/prism/prism_ex3_s1.png';
import prism_ex3_s2 from '/img/instruments/videomancer/prism/prism_ex3_s2.png';
import prism_ex3_s3 from '/img/instruments/videomancer/prism/prism_ex3_s3.png';
import prism_ex3_s4 from '/img/instruments/videomancer/prism/prism_ex3_s4.png';
import prism_ex3_s5 from '/img/instruments/videomancer/prism/prism_ex3_s5.png';
import prism_ex3_s6 from '/img/instruments/videomancer/prism/prism_ex3_s6.png';

# Prism

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: prism_source1_fruit, after: prism_hero_s1 },
    { label: "Boat", before: prism_source2_boat, after: prism_hero_s2 },
    { label: "Elephant", before: prism_source3_elephant, after: prism_hero_s3 },
    { label: "Pattern", before: prism_source4_pattern, after: prism_hero_s4 },
    { label: "Man", before: prism_source5_man, after: prism_hero_s5 },
    { label: "Wood", before: prism_source6_wood, after: prism_hero_s6 },
  ]}
/>
*Prism applying per-channel horizontal displacement and channel swapping to decompose video into separated colour planes.*

---

## Overview

Prism takes the three channels of a YUV video signal and shifts each one independently along the horizontal axis. The result is chromatic aberration — the colour planes separate, creating prismatic rainbow fringes around edges and a distinctive split-colour aesthetic. Because each channel has its own delay line backed by BRAM, the displacement is true pixel-level re-sampling, not a colour-space trick.

The program offers three individual delay controls (Y, U, V) plus a Spread parameter that pushes U and V symmetrically apart while leaving Y centred. A luma modulation path allows the input brightness to dynamically vary the displacement amount, causing the separation to follow the content of the image — bright areas warp more than dark areas. Channel swap toggles reroute the Y/U/V paths after delay for creative colour remapping, and a Mirror toggle reverses the delay direction for bilateral symmetry.

One parameter — Mod Bias — is declared in the register map but has no effect on the output in the current implementation. The supplement notes this explicitly.

---

## Quick Start

1. **Spread is the quick-start knob**: For instant chromatic aberration, leave the individual delay knobs at zero and just turn Spread. It pushes U and V apart symmetrically while keeping Y centred.
2. **Luma Mod creates organic warping**: Without modulation, displacement is uniform across the image. With modulation, the displacement follows the scene content, creating effects that feel more like refraction than mechanical offset.
3. **Mirror for bilateral fringes**: Real optical chromatic aberration produces fringes on both sides of edges. Enable Mirror to approximate this symmetric look.

---

## Background

### Chromatic Aberration

Optical systems focus different wavelengths of light at slightly different points, causing colour channels to misalign at the edges of an image. This is **chromatic aberration** — an optical defect in photography that has become a deliberate creative effect in video art at digital processing. Prism reproduces this digitally by independently delaying each colour channel along the horizontal axis.

### BRAM Delay Lines

Each channel passes through a `variable_delay_u` module: a write pointer stores incoming pixels into a BRAM array, and a read pointer reads back from an earlier address. The difference between write and read pointers is the delay in pixels. With an 11-bit depth (2048 entries), each channel can be offset by up to 2047 pixels horizontally — far more than most practical uses require. The BRAM provides single-cycle read access, adding only 2 clocks of latency to the pipeline.

### Luma-Driven Modulation

The Luma Mod knob scales the input brightness value and adds it to all three delay values. This makes the displacement content-dependent: bright regions of the source image receive more horizontal shift than dark regions. The result is an organic, image-adaptive warping where chromatic fringes grow and shrink with the scene content. Combined with Luma Invert, the modulation polarity can be flipped so that dark regions receive the maximum displacement.

### Channel Swapping

After the delay lines, three combinational swap paths reroute the channels. U-V Swap exchanges the two chrominance channels (blue-difference and red-difference), rotating hues by approximately 90°. Y-U Swap places the delayed U signal into the luminance path and the delayed Y into the U path, creating dramatic false-colour effects where chrominance becomes brightness and vice versa. Combined swaps produce six distinct channel permutations from three toggle states.

### Mirror Mode

The Mirror toggle subtracts each computed delay from the maximum value (2047), effectively reversing the direction of displacement. A channel that was shifted right becomes shifted left by the same amount. When combined with Spread, this creates bilateral chromatic fringes that appear symmetrically on both sides of edges.


---

## Signal Flow

Input Registration → BRAM Delay Lines → Channel Swap → Interpolator → Sync Delay Pipeline → Output Mux

```
Input Video (YUV 4:4:4)
│
├── Input Registration (1 clock) ──────────────────────
│   ├─ Optional luma inversion (Luma Invert toggle)
│   ├─ Luma modulation: mod_offset = Y × Luma_Mod
│   ├─ Spread: spread_half = Spread >> 1
│   ├─ Y delay = Y_Delay + mod_offset
│   ├─ U delay = U_Delay + spread_half + mod_offset
│   ├─ V delay = V_Delay + spread_half + mod_offset
│   └─ Mirror toggle: delay = 2047 − delay
│
├── BRAM Delay Lines (2 clocks) ───────────────────────
│   ├─ variable_delay_u (Y channel, 2048-deep)
│   ├─ variable_delay_u (U channel, 2048-deep)
│   └─ variable_delay_u (V channel, 2048-deep)
│
├── Channel Swap (1 clock) ────────────────────────────
│   ├─ U-V Swap: exchange U ↔ V
│   ├─ Y-U Swap: exchange Y ↔ U
│   └─ Combined: 6 permutations from 2-bit toggle
│
├── Interpolator (4 clocks) ───────────────────────────
│   └─ Wet/dry crossfade (Mix fader)
│
├── Sync Delay Pipeline (7 clocks) ────────────────────
│   └─ Align sync + dry data to processed path
│
└── Output Mux ────────────────────────────────────────
    └─ Bypass toggle selects processed or dry signal
```

The delay computation stage packs significant logic into a single clock: luma modulation (10×10-bit multiply), spread halving, per-channel addition, and optional mirror inversion. The mod_offset is computed from the current pixel's brightness and added to all three channel delays, so a bright pixel shifts Y, U, and V by similar amounts. Spread adds a fixed offset only to U and V, creating differential displacement between luma and chroma. The Mirror toggle applies after all additions, reversing the entire delay vector. Mod Bias is registered but never read by any logic — it has no effect.

---

## Parameter Reference

<img src={prism_control_panel} alt="Videomancer front panel with Prism loaded"/>
*Videomancer's front panel with Prism active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Y Delay
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Y Delay sets the horizontal pixel offset for the luminance channel. At 0, the Y channel is not displaced. Increasing the value shifts Y horizontally, causing the brightness component to separate from the colour channels. Combined with luma modulation, the actual delay per pixel equals `Y_Delay + luma_mod_offset`, creating a brightness-dependent displacement. The delay range extends to the full BRAM depth when summed with spread and modulation.

---

#### Knob 2 — U Delay
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

U Delay sets the horizontal pixel offset for the blue-difference chrominance channel. When set differently from Y Delay and V Delay, blue-cyan fringes appear on horizontal edges — the classic chromatic aberration look. The Spread parameter further adds a symmetric offset on top of this base value, so even with U Delay at zero, the Spread knob can push U away from Y.

---

#### Knob 3 — V Delay
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

V Delay sets the horizontal pixel offset for the red-difference chrominance channel. Displacing V independently from U creates red-magenta fringes on horizontal transitions. For prismatic rainbow edges, set Y Delay to zero, U Delay to a moderate value, and V Delay to a higher value — this staggers the three channels like light through a glass prism.

---

#### Knob 4 — Spread
| Property | Value |
|----------|-------|
| Range | -100.0% – 100.0% |
| Default | 0.1% |
| Suffix | % |

Spread adds a symmetric offset to both U and V delay values (Spread divided by 2). At the midpoint (512), the spread offset is 256, pushing both chroma channels away from Y by the same amount. At zero, no additional spread is applied. Spread acts on top of the individual U/V Delay values, so it provides a single-knob way to increase or decrease the overall chromatic separation without adjusting two knobs independently.

---

#### Knob 5 — Luma Mod
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Luma Mod controls how strongly the input pixel brightness modulates the delay amount. The modulation is an unsigned multiply: `mod_offset = input_Y × Luma_Mod / 1023`. This offset is added to all three channel delays (Y, U, and V). At zero, delay is purely manual. At maximum, bright pixels shift by hundreds of additional pixels, creating an organic warping effect that tracks the image content. With Luma Invert active, dark areas receive the maximum modulation instead.

---

#### Knob 6 — Mod Bias
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Mod Bias is declared in the register map but has no effect on the output in the current VHDL implementation. It is reserved for a future modulation centre-point offset that would shift the operating point of the luma-to-delay modulation curve. Adjusting this knob produces no visible change.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — U-V Swap** | Off | On |
| **8 — Y-U Swap** | Off | On |
| **9 — Luma Invert** | Off | On |
| **10 — Mirror** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles divide into four active controls and one standard bypass. U-V Swap and Y-U Swap reroute the channel paths after delay processing. Luma Invert flips the brightness before it enters both the delay line and the modulation path. Mirror reverses the direction of all displacements. These can be combined freely for six channel permutations × two modulation polarities × two displacement directions.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Mix crossfades between the dry (original) signal and the wet (displaced) signal via the interpolator stage. At 100% (default, register 1023), only the processed signal is output. At 0%, the original signal passes through unchanged. Intermediate values create a semi-transparent overlay of the displaced channels over the original, which can produce subtle ghosting or halo effects.


#### Switch 11 — Bypass
| Property | Value |
|----------|-------|
| Off | Processing active |
| On | Bypass engaged |

Routes the unprocessed input signal directly to the output, bypassing all Prism processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.

---



> See [Common Controls & Glossary Reference](../common_reference.md) for details.

---

## Guided Exercises

These exercises progress from simple chromatic separation to dynamic luma-modulated warping and creative channel remapping, building familiarity with Prism's displacement engine.

### Exercise 1: Classic Chromatic Aberration

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: prism_source1_fruit, after: prism_ex1_s1 },
    { label: "Boat", before: prism_source2_boat, after: prism_ex1_s2 },
    { label: "Elephant", before: prism_source3_elephant, after: prism_ex1_s3 },
    { label: "Pattern", before: prism_source4_pattern, after: prism_ex1_s4 },
    { label: "Man", before: prism_source5_man, after: prism_ex1_s5 },
    { label: "Wood", before: prism_source6_wood, after: prism_ex1_s6 },
  ]}
/>
*Classic Chromatic Aberration — simulated result across source images.*
**Source**: A high-contrast image with sharp edges — text overlays, geometric shapes, or architectural footage.

**What You'll Create**: Create prismatic colour fringes that mimic optical chromatic aberration.

1. Set Y Delay to 0% so the luminance channel stays centred.
2. Increase U Delay to ~20% to shift the blue-difference channel rightward.
3. Increase V Delay to ~40% to shift the red-difference channel further right.
4. Observe the staggered rainbow fringes appearing on horizontal edges.
5. Enable Mirror (Switch 10) to see bilateral fringes on both sides of edges.
6. Adjust Mix to ~70% to soften the effect for a more subtle aberration.

**Key concepts**: Per-channel delay creates chromatic separation, staggering Y/U/V delays mimics prismatic dispersion, mirror creates bilateral symmetry

---

### Exercise 2: Luma-Modulated Warping

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: prism_source1_fruit, after: prism_ex2_s1 },
    { label: "Boat", before: prism_source2_boat, after: prism_ex2_s2 },
    { label: "Elephant", before: prism_source3_elephant, after: prism_ex2_s3 },
    { label: "Pattern", before: prism_source4_pattern, after: prism_ex2_s4 },
    { label: "Man", before: prism_source5_man, after: prism_ex2_s5 },
    { label: "Wood", before: prism_source6_wood, after: prism_ex2_s6 },
  ]}
/>
*Luma-Modulated Warping — simulated result across source images.*
**Source**: Footage with a wide tonal range — faces, landscapes, or imagery with strong light/dark contrast.

**What You'll Create**: Use input brightness to dynamically control displacement for content-adaptive chromatic effects.

1. Set all three delay knobs (Y, U, V) to 0%.
2. Increase Spread to ~70% to create a base chromatic separation.
3. Slowly increase Luma Mod from 0% to ~60%. Watch the displacement become content-dependent: bright areas warp more than dark areas.
4. Toggle Luma Invert (Switch 9) to reverse the modulation — now dark regions receive maximum separation.
5. Feed the output back to the input (feedback loop) to amplify the warping.

**Key concepts**: Luma modulation multiplies brightness × mod amount and adds to all delays, Luma Invert flips which regions get maximum displacement, feedback amplifies the effect

---

### Exercise 3: False-Colour Channel Remix

<BeforeAfterSlider
  sources={[
    { label: "Fruit", before: prism_source1_fruit, after: prism_ex3_s1 },
    { label: "Boat", before: prism_source2_boat, after: prism_ex3_s2 },
    { label: "Elephant", before: prism_source3_elephant, after: prism_ex3_s3 },
    { label: "Pattern", before: prism_source4_pattern, after: prism_ex3_s4 },
    { label: "Man", before: prism_source5_man, after: prism_ex3_s5 },
    { label: "Wood", before: prism_source6_wood, after: prism_ex3_s6 },
  ]}
/>
*False-Colour Channel Remix — simulated result across source images.*
**Source**: Any video — the channel swaps create dramatic recolouring of any content.

**What You'll Create**: Explore the six channel permutations created by the two swap toggles.

1. Set moderate delays: Y Delay ~10%, U Delay ~30%, V Delay ~50%.
2. Enable U-V Swap (Switch 7). Observe the hue rotation — reds become blues.
3. Disable U-V Swap. Enable Y-U Swap (Switch 8). Observe false-colour: chrominance becomes brightness.
4. Enable both swaps simultaneously. A third, more extreme remapping appears.
5. With both swaps active, increase Luma Mod to ~50% for modulation-driven false-colour warping.
6. Try Luma Invert with both swaps — the inverted luma feeding into a chrominance output creates negative-image colour effects.

**Key concepts**: Channel swaps happen after delay, two toggle combinatorics yield six permutations, luma becoming chroma (and vice versa) creates false colour

---


## Tips

- **Channel swaps are post-delay**: Swapping happens after displacement, so you can set up a specific delay pattern and then remap it to different colour channels without changing the delay values.
- **Luma Invert affects two paths**: It inverts both the Y channel data going into the delay line and the modulation source. The dual effect is intentional — it reverses the entire displacement polarity.
- **Mod Bias has no effect**: The knob is reserved for future development. Don't spend time adjusting it.
- **Feedback amplifies fringing**: Routing the output back to the input stacks displacement on top of displacement, creating ever-widening colour separation that can fill the entire frame.

---

## Glossary

| Term | Definition |
|------|------------|
| **Channel Swap** | Rerouting the Y, U, and V signal paths to different output channels after processing. |
| **Chromatic Aberration** | Colour fringing caused by different colour channels being displaced relative to each other. |
| **Delay Line** | A FIFO buffer that stores incoming pixel values and reads them back after a configurable number of clock cycles, implementing horizontal displacement. |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **Luma Modulation** | Multiplying input brightness by a control parameter to dynamically vary a processing parameter (here, delay amount). |
| **Spread** | A symmetric offset added equally to U and V delay values to create uniform chromatic separation. |
| **Variable Delay** | A delay line whose read-back position can be changed per pixel, enabling dynamic horizontal displacement. |

For common terms (YUV, FPGA, BRAM, Pipeline, etc.) see the [Common Glossary](../common_reference.md#common-glossary).

---
