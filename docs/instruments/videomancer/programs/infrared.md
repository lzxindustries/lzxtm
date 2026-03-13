---
draft: true
sidebar_position: 145
slug: /instruments/videomancer/infrared
title: "Infrared"
image: /img/instruments/videomancer/infrared/infrared_hero_s1.png
description: "Thermal imaging cameras do not capture color."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import infrared_control_panel from '/img/instruments/videomancer/infrared/infrared_control_panel.png';
import infrared_source1_cat from '/img/instruments/videomancer/infrared/infrared_source1_cat.png';
import infrared_source2_parrot from '/img/instruments/videomancer/infrared/infrared_source2_parrot.png';
import infrared_source3_elephant from '/img/instruments/videomancer/infrared/infrared_source3_elephant.png';
import infrared_source4_pattern from '/img/instruments/videomancer/infrared/infrared_source4_pattern.png';
import infrared_source5_girl from '/img/instruments/videomancer/infrared/infrared_source5_girl.png';
import infrared_source6_paint from '/img/instruments/videomancer/infrared/infrared_source6_paint.png';
import infrared_hero_s1 from '/img/instruments/videomancer/infrared/infrared_hero_s1.png';
import infrared_hero_s2 from '/img/instruments/videomancer/infrared/infrared_hero_s2.png';
import infrared_hero_s3 from '/img/instruments/videomancer/infrared/infrared_hero_s3.png';
import infrared_hero_s4 from '/img/instruments/videomancer/infrared/infrared_hero_s4.png';
import infrared_hero_s5 from '/img/instruments/videomancer/infrared/infrared_hero_s5.png';
import infrared_hero_s6 from '/img/instruments/videomancer/infrared/infrared_hero_s6.png';
import infrared_ex1_s1 from '/img/instruments/videomancer/infrared/infrared_ex1_s1.png';
import infrared_ex1_s2 from '/img/instruments/videomancer/infrared/infrared_ex1_s2.png';
import infrared_ex1_s3 from '/img/instruments/videomancer/infrared/infrared_ex1_s3.png';
import infrared_ex1_s4 from '/img/instruments/videomancer/infrared/infrared_ex1_s4.png';
import infrared_ex1_s5 from '/img/instruments/videomancer/infrared/infrared_ex1_s5.png';
import infrared_ex1_s6 from '/img/instruments/videomancer/infrared/infrared_ex1_s6.png';
import infrared_ex2_s1 from '/img/instruments/videomancer/infrared/infrared_ex2_s1.png';
import infrared_ex2_s2 from '/img/instruments/videomancer/infrared/infrared_ex2_s2.png';
import infrared_ex2_s3 from '/img/instruments/videomancer/infrared/infrared_ex2_s3.png';
import infrared_ex2_s4 from '/img/instruments/videomancer/infrared/infrared_ex2_s4.png';
import infrared_ex2_s5 from '/img/instruments/videomancer/infrared/infrared_ex2_s5.png';
import infrared_ex2_s6 from '/img/instruments/videomancer/infrared/infrared_ex2_s6.png';
import infrared_ex3_s1 from '/img/instruments/videomancer/infrared/infrared_ex3_s1.png';
import infrared_ex3_s2 from '/img/instruments/videomancer/infrared/infrared_ex3_s2.png';
import infrared_ex3_s3 from '/img/instruments/videomancer/infrared/infrared_ex3_s3.png';
import infrared_ex3_s4 from '/img/instruments/videomancer/infrared/infrared_ex3_s4.png';
import infrared_ex3_s5 from '/img/instruments/videomancer/infrared/infrared_ex3_s5.png';
import infrared_ex3_s6 from '/img/instruments/videomancer/infrared/infrared_ex3_s6.png';

# Infrared

<span class="head2_nolink">Videomancer Program Guide</span>

:::warning
This document is still in progress, may contain errors, and is for preview only.
:::

<BeforeAfterSlider
  sources={[
    { label: "Cat", before: infrared_source1_cat, after: infrared_hero_s1 },
    { label: "Parrot", before: infrared_source2_parrot, after: infrared_hero_s2 },
    { label: "Elephant", before: infrared_source3_elephant, after: infrared_hero_s3 },
    { label: "Pattern", before: infrared_source4_pattern, after: infrared_hero_s4 },
    { label: "Girl", before: infrared_source5_girl, after: infrared_hero_s5 },
    { label: "Paint", before: infrared_source6_paint, after: infrared_hero_s6 },
  ]}
/>
*Infrared applying false-color thermal palette mapping to transform source luminance into ironbow and arctic color schemes with isotherm contour overlays.*

---

## Overview

Thermal imaging cameras do not capture color. They measure infrared radiation — heat — and assign artificial colors to make the temperature map readable. Hot objects glow white or yellow; cold objects sink into deep blues or purples. Infrared brings this technique to video synthesis, treating the luminance channel of any video signal as a temperature map and painting it with a piecewise-linear false-color palette.

The program divides the luminance range into four zones — cool, warm, hot, and white-hot — each with its own color assignment. Zone boundaries are determined by the top two bits of the mapped luminance value, and within each zone the lower eight bits drive smooth ramps between the base colors. Two palette modes are available: an ironbow scheme that moves from blue through red to orange and white, and an arctic scheme that substitutes cyan and green tones for the cooler zones. A palette selection knob adjusts chroma saturation of the thermal colors, while temperature range, hot threshold, cold floor, and gradient controls reshape the mapping curve before palette lookup.

Isotherm lines — bright white contours drawn at zone boundaries — can be enabled with a toggle, adding topographic-style banding that emphasizes temperature transitions. An invert toggle flips the luminance before mapping, turning hot regions cold and cold regions hot. The result is a purely register-based processor (zero BRAM) with an eight-clock pipeline that can transform any video source into a thermal camera aesthetic.

---

## Quick Start

1. **Start with ironbow:** The ironbow palette provides the most intuitive thermal camera aesthetic. Switch to arctic once you have a feel for the zone structure.
2. **Window your range:** Narrowing the temperature range (low Pot 2) dramatically increases contrast within the visible zones — useful for revealing subtle brightness differences in flat-lit scenes.
3. **Use cold floor to hide noise:** Raising the cold floor suppresses the coolest zone, which often contains dark noise or letterbox bars.

---

## Background

### False-Color Palette Mapping

False-color mapping is a visualization technique that assigns arbitrary colors to a measured quantity. In thermal imaging, the quantity is temperature (or more precisely, radiant flux in the infrared band). The color assignment is chosen for perceptual clarity: humans can distinguish far more color hues than greyscale levels, so a rainbow or ironbow palette reveals details that a monochrome image hides. Infrared applies this same idea to video luminance — each brightness level maps to a specific Y/U/V triplet drawn from a four-zone piecewise-linear color table.

### Piecewise-Linear Interpolation

Rather than storing a full 1024-entry lookup table, Infrared uses four zones with linear ramps between anchor colors. The zone is selected by the two most significant bits of the mapped luminance (bits 9:8), and the remaining eight bits drive a linear interpolation within that zone. This approach uses zero BRAM and only a few hundred logic cells, trading color table flexibility for resource efficiency.

### Isotherm Contours

In meteorology and thermal analysis, an isotherm is a line connecting points of equal temperature. Infrared draws isotherm lines at zone boundaries — where the fractional part of the luminance is near zero or 255. These thin bright lines create a contour-map effect that emphasizes the temperature gradient structure of the image, similar to the elevation contours on a topographic map.

### Temperature Range and Windowing

Real thermal cameras let the operator adjust the temperature range to match the scene. A narrow range increases contrast within a small temperature band; a wide range compresses the entire temperature span onto the available palette. Infrared emulates this with a combination of range scaling (which compresses or expands the luminance before zone detection) and cold floor (which raises the minimum luminance, effectively clipping out the coldest portion of the scene).

### Ironbow and Spectral Palettes

The ironbow palette — dark blue → red → orange → yellow → white — is the most common thermal imaging color scheme and was designed to mimic the colors of heated iron. The arctic palette substitutes cyan and green for the blue and red midtones, producing a cooler-toned aesthetic reminiscent of FLIR maritime or environmental monitoring displays. Both palettes share the same zone structure; only the U/V chrominance values differ.


---

## Signal Flow

Y/U/V Channels → Sync Signals → Bypass

```
Input Video (YUV 4:4:4)
│
├── Y/U/V Channels ─────────────────────────────────────────────
│   │
│   ├─ 1. Input Register + Invert     (optional Y inversion)
│   ├─ 2. Zone Detect                 (temp range scale + cold floor offset
│   │                                   → mapped Y → zone[1:0] + frac[7:0])
│   ├─ 3. Piecewise Color Mapping     (4-zone palette lookup
│   │      ├─ Zone 00: Cool           (dark Y, blue/cyan chroma)
│   │      ├─ Zone 01: Warm           (mid Y, neutral-to-red/green chroma)
│   │      ├─ Zone 10: Hot            (bright Y + hot threshold boost, orange)
│   │      └─ Zone 11: White-hot      (max Y, neutral chroma)
│   │      └─ Palette Sel saturation bias applied to U/V)
│   ├─ 4. Isotherm Lines + Compose    (bright white lines at zone boundaries)
│   │
│   └─ 5. Interpolator Mix            (4-clock wet/dry crossfade per channel)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Delay pipeline (8 clocks)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The critical path runs through two luminance transformations before the palette lookup. First, the temperature range parameter rescales the input luminance — low range values expand the mapping (shift left by 2), compressing the full brightness range into fewer zones and pushing more of the image into white-hot. High range values leave the mapping at unity. Second, the cold floor adds a DC offset that raises the minimum luminance, effectively hiding the coolest zone. Both transformations happen in Stage 2, feeding the zone detector that drives Stage 3's color assignment. The palette selection knob operates after the zone color is chosen, scaling the chroma distance from midpoint to boost or reduce saturation of the thermal colors.

---

## Parameter Reference

<img src={infrared_control_panel} alt="Videomancer front panel with Infrared loaded"/>
*Videomancer's front panel with Infrared active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Range
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the saturation intensity of the thermal palette colors. Above 50%, the chroma components of each zone are boosted — blues become more vivid, oranges richer. Below 50%, chroma is pulled toward neutral grey, creating a more subdued pastel thermal map. At zero the output is effectively a luminance-only remapping with desaturated hints of the palette. This knob does not change which palette is active (that is determined by toggle 7); it adjusts how strongly the color is applied within whichever palette is selected.

---

#### Knob 2 — Hot Thr
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

At maximum (100%), the mapping operates near unity — the full 0–1023 luminance range maps linearly across all four zones. At minimum (0%), the luminance is expanded by shifting left two bits, which compresses the entire image into fewer zones and pushes mid-brightness content into the hot and white-hot regions. This control works like the temperature span adjustment on a FLIR camera: narrowing the range increases thermal contrast but clips the extremes. Internally, sets the temperature range scaling applied to the input luminance before zone detection.

---

#### Knob 3 — Cold Flr
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the hot threshold boost applied in Zone 2 (the hot zone). Higher values add a luminance offset to the hot-zone output, making the orange/yellow region brighter and pushing it closer to white-hot. At zero the hot zone follows the standard ramp; at maximum the hot zone is nearly as bright as white-hot, compressing the visual distinction between the two upper zones. This is useful for emphasizing hot spots in the source or creating a more dramatic thermal flare.

---

#### Knob 4 — Gradient
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Raises the minimum luminance level by adding a DC offset after range scaling. At zero the cold floor has no effect and the darkest input pixels map to the cool zone as expected. Increasing the cold floor lifts the entire mapped luminance, effectively removing the lowest zone from the output. At maximum, even moderate-brightness content maps into the warm or hot zones, producing a thermal image that appears to have a higher baseline temperature.

---

#### Knob 5 — Iso Therm
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the gradient steepness of within-zone ramp transitions. The VHDL implements this as a shift-based modifier on the fractional ramp signal. At maximum steepness (100%), zone transitions are sharp with rapid color changes. At minimum steepness (0%), the ramp is smoothed via right-shifting, producing softer gradients between zone anchor colors. This does not affect where zone boundaries fall — only how quickly the color transitions within each zone.

---

#### Knob 6 — Bright
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Mapped to internal signal `s_mix_knob` but currently unused in the VHDL processing pipeline. The register is read and assigned but does not affect any stage of the thermal mapping or output composition. This parameter is reserved for a future firmware revision. Adjusting this knob has no visible effect on the output.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Palette** | Iron | Lava |
| **8 — Scale** | Linear | Step |
| **9 — Overlay** | Full | Blend |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles span palette selection, isotherm overlay, mapping inversion, a reserved function, and bypass. Toggle 7 selects between two distinct palette color schemes — ironbow and arctic — by changing the U/V values assigned in each zone. Toggle 8 enables isotherm contour lines at zone boundaries. Toggle 9 inverts the input luminance before zone detection, flipping the hot/cold mapping. Toggle 10 is reserved (unused in the current VHDL). Toggle 11 bypasses the entire processor. Note that the TOML configuration lists additional value labels for toggles 7 and 8 (four options each), but the VHDL implementation uses only a single bit — so only the first two labels map to actual hardware behavior.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry mix between the original video signal and the thermal-mapped output. At 0% the output is entirely the dry (original) signal; at 100% the output is entirely the wet (thermal-mapped) signal. Intermediate positions create a crossfade that blends the false-color palette over the original image. This is implemented via three parallel `interpolator_u` instances (one per Y/U/V channel) using the fader register value as the interpolation parameter `t`.





---

## Guided Exercises

The following exercises demonstrate how Infrared's controls interact to produce different thermal visualization styles, from subtle heat-map overlays to dramatic sci-fi scanner aesthetics.

### Exercise 1: Classic Thermal Camera

<BeforeAfterSlider
  sources={[
    { label: "Cat", before: infrared_source1_cat, after: infrared_ex1_s1 },
    { label: "Parrot", before: infrared_source2_parrot, after: infrared_ex1_s2 },
    { label: "Elephant", before: infrared_source3_elephant, after: infrared_ex1_s3 },
    { label: "Pattern", before: infrared_source4_pattern, after: infrared_ex1_s4 },
    { label: "Girl", before: infrared_source5_girl, after: infrared_ex1_s5 },
    { label: "Paint", before: infrared_source6_paint, after: infrared_ex1_s6 },
  ]}
/>
*Classic Thermal Camera — simulated result across source images.*
**Source**: A portrait or figure against a mid-tone background. Face and hands provide natural "hot spots" against a cooler backdrop.

**What You'll Create**: Reproduce the look of a standard FLIR thermal camera with ironbow palette, emphasizing skin-tone heat signatures against a cool background.

1. Set the palette to ironbow (Toggle 7 = Iron).
2. Set Range (Pot 1) to 50% for moderate palette saturation.
3. Adjust Hot Thr (Pot 2) to 65% to brighten the hot zone and make skin tones stand out.
4. Set Cold Flr (Pot 3) to 25% to slightly lift the cold floor, hiding the darkest blue zone.
5. Set Gradient (Pot 4) to 60% for moderate transition sharpness.
6. Enable isotherm lines (Toggle 8 = on) to add contour overlay.
7. Set Mix (Fader) to 100% for full thermal effect.

**Key concepts**: Temperature windowing (range + cold floor), hot threshold boost, isotherm contouring.

---

### Exercise 2: Inverted Arctic Scan

<BeforeAfterSlider
  sources={[
    { label: "Cat", before: infrared_source1_cat, after: infrared_ex2_s1 },
    { label: "Parrot", before: infrared_source2_parrot, after: infrared_ex2_s2 },
    { label: "Elephant", before: infrared_source3_elephant, after: infrared_ex2_s3 },
    { label: "Pattern", before: infrared_source4_pattern, after: infrared_ex2_s4 },
    { label: "Girl", before: infrared_source5_girl, after: infrared_ex2_s5 },
    { label: "Paint", before: infrared_source6_paint, after: infrared_ex2_s6 },
  ]}
/>
*Inverted Arctic Scan — simulated result across source images.*
**Source**: High-contrast geometric shapes — a checkerboard, barcode, or architectural scene with strong shadows and bright highlights.

**What You'll Create**: Create a cold-toned inverted thermal scan where bright areas appear cool and dark areas appear hot, using the arctic palette.

1. Switch to arctic palette (Toggle 7 = Rainbow/arctic position).
2. Enable invert (Toggle 9 = Blend/invert position) to flip hot and cold.
3. Set Range (Pot 2) to 30% for narrow temperature window — maximum contrast.
4. Set Cold Flr (Pot 3) to 0% — no floor lift, allow full cool-zone depth.
5. Set Hot Thr (Pot 2) to 40% for moderate hot-zone boost.
6. Turn off isotherm lines (Toggle 8 = off) for clean color bands.
7. Set Gradient (Pot 4) to 80% for sharp zone transitions.

**Key concepts**: Palette inversion, narrow-range windowing, arctic palette chrominance, sharp gradients.

---

### Exercise 3: Pastel Thermal Overlay

<BeforeAfterSlider
  sources={[
    { label: "Cat", before: infrared_source1_cat, after: infrared_ex3_s1 },
    { label: "Parrot", before: infrared_source2_parrot, after: infrared_ex3_s2 },
    { label: "Elephant", before: infrared_source3_elephant, after: infrared_ex3_s3 },
    { label: "Pattern", before: infrared_source4_pattern, after: infrared_ex3_s4 },
    { label: "Girl", before: infrared_source5_girl, after: infrared_ex3_s5 },
    { label: "Paint", before: infrared_source6_paint, after: infrared_ex3_s6 },
  ]}
/>
*Pastel Thermal Overlay — simulated result across source images.*
**Source**: A slowly moving organic texture — clouds, water, or foliage with gentle brightness gradients.

**What You'll Create**: Blend a desaturated, soft thermal palette over the original video to create a subtle heat-map overlay effect rather than a full false-color replacement.

1. Set palette to ironbow (Toggle 7 = Iron).
2. Reduce Range (Pot 1) to 20% — pull chroma toward neutral for pastel tones.
3. Set Gradient (Pot 4) to 15% for very smooth zone transitions.
4. Set Cold Flr (Pot 3) to 40% to lift the baseline and spread the image across warm/hot zones.
5. Set Mix (Fader) to 50% for a half-blend with the original signal.
6. Disable isotherm (Toggle 8 = off) and invert (Toggle 9 = off).

**Key concepts**: Wet/dry mixing, desaturated palette, smooth gradients, overlay compositing.

---


## Tips

- **Isotherm lines as composition guides:** Enable isotherm lines temporarily to visualize where zone boundaries fall, then disable them for a cleaner final output.
- **Combine with upstream keyers:** Feed Infrared a pre-keyed signal (e.g., luminance key isolating a performer) to apply thermal coloring only to the keyed region.
- **Mix for subtlety:** A 30–50% wet/dry mix blends the thermal palette as a color overlay on top of the original image, creating a heads-up-display thermal scanner effect.
- **Pot 6 is inert:** The Bright knob has no effect in the current firmware. Do not expect brightness adjustment from this control.
- **Toggle label caveat:** Toggles 7 and 8 show four value labels in the UI, but only two hardware states exist. The third and fourth positions duplicate the second.

---
