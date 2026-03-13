---
draft: true
sidebar_position: 329
slug: /instruments/videomancer/voido
title: "Voido"
image: /img/instruments/videomancer/voido/voido_hero_s1.png
description: "Early television chromakey — known at the BBC as Colour Separation Overlay (CSO) — was a crude but effective technique."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import voido_control_panel from '/img/instruments/videomancer/voido/voido_control_panel.png';
import voido_source1_parrot from '/img/instruments/videomancer/voido/voido_source1_parrot.png';
import voido_source2_sunset from '/img/instruments/videomancer/voido/voido_source2_sunset.png';
import voido_source3_collage from '/img/instruments/videomancer/voido/voido_source3_collage.png';
import voido_source4_pattern from '/img/instruments/videomancer/voido/voido_source4_pattern.png';
import voido_source5_woman from '/img/instruments/videomancer/voido/voido_source5_woman.png';
import voido_source6_knit from '/img/instruments/videomancer/voido/voido_source6_knit.png';
import voido_hero_s1 from '/img/instruments/videomancer/voido/voido_hero_s1.png';
import voido_hero_s2 from '/img/instruments/videomancer/voido/voido_hero_s2.png';
import voido_hero_s3 from '/img/instruments/videomancer/voido/voido_hero_s3.png';
import voido_hero_s4 from '/img/instruments/videomancer/voido/voido_hero_s4.png';
import voido_hero_s5 from '/img/instruments/videomancer/voido/voido_hero_s5.png';
import voido_hero_s6 from '/img/instruments/videomancer/voido/voido_hero_s6.png';
import voido_ex1_s1 from '/img/instruments/videomancer/voido/voido_ex1_s1.png';
import voido_ex1_s2 from '/img/instruments/videomancer/voido/voido_ex1_s2.png';
import voido_ex1_s3 from '/img/instruments/videomancer/voido/voido_ex1_s3.png';
import voido_ex1_s4 from '/img/instruments/videomancer/voido/voido_ex1_s4.png';
import voido_ex1_s5 from '/img/instruments/videomancer/voido/voido_ex1_s5.png';
import voido_ex1_s6 from '/img/instruments/videomancer/voido/voido_ex1_s6.png';
import voido_ex2_s1 from '/img/instruments/videomancer/voido/voido_ex2_s1.png';
import voido_ex2_s2 from '/img/instruments/videomancer/voido/voido_ex2_s2.png';
import voido_ex2_s3 from '/img/instruments/videomancer/voido/voido_ex2_s3.png';
import voido_ex2_s4 from '/img/instruments/videomancer/voido/voido_ex2_s4.png';
import voido_ex2_s5 from '/img/instruments/videomancer/voido/voido_ex2_s5.png';
import voido_ex2_s6 from '/img/instruments/videomancer/voido/voido_ex2_s6.png';
import voido_ex3_s1 from '/img/instruments/videomancer/voido/voido_ex3_s1.png';
import voido_ex3_s2 from '/img/instruments/videomancer/voido/voido_ex3_s2.png';
import voido_ex3_s3 from '/img/instruments/videomancer/voido/voido_ex3_s3.png';
import voido_ex3_s4 from '/img/instruments/videomancer/voido/voido_ex3_s4.png';
import voido_ex3_s5 from '/img/instruments/videomancer/voido/voido_ex3_s5.png';
import voido_ex3_s6 from '/img/instruments/videomancer/voido/voido_ex3_s6.png';

# Voido

<span class="head2_nolink">Videomancer Program Guide</span>

:::warning
This document is still in progress, may contain errors, and is for preview only.
:::

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: voido_source1_parrot, after: voido_hero_s1 },
    { label: "Sunset", before: voido_source2_sunset, after: voido_hero_s2 },
    { label: "Collage", before: voido_source3_collage, after: voido_hero_s3 },
    { label: "Pattern", before: voido_source4_pattern, after: voido_hero_s4 },
    { label: "Woman", before: voido_source5_woman, after: voido_hero_s5 },
    { label: "Knit", before: voido_source6_knit, after: voido_hero_s6 },
  ]}
/>
*Voido performing BBC-style chromakey separation with deliberate edge artifacts, spill suppression, and patterned fill behind keyed regions.*

---

## Overview

Early television chromakey — known at the BBC as Colour Separation Overlay (CSO) — was a crude but effective technique. A camera pointed at a performer standing in front of a uniformly colored backdrop; an analog circuit compared each pixel's hue to a reference, and wherever the hue matched, the pixel was replaced with a second video source. The system was imprecise. Edges tore and flickered, the key color bled into foreground skin tones, and the threshold between "in" and "out" wobbled with lighting changes. Voido recreates this experience faithfully.

The name *Voido* is a play on *video* and *void* — the empty space left behind when the key removes the background. The program operates entirely in the hue domain: it extracts an approximate hue angle from the U/V chroma channels using an octant-plus-ratio atan2 approximation, computes the circular distance to a user-selected key hue, and generates a soft or hard key signal. Foreground pixels are despilled to remove contamination from the key color, while keyed regions are filled with one of four selectable patterns — a flat matte, horizontal bars, a color ramp, or a grid. An artifact generator adds LFSR-driven noise and slew-rate limiting to the key signal, replicating the edge tearing and hysteresis of vintage CSO hardware.

At clean settings Voido is a functional chromakey — usable for real compositing work. At high Artifact settings it becomes a creative tool, generating the characteristic edge fringing, color spill, and unstable boundaries that defined the look of early science fiction television.

---

## Quick Start

1. **Start with Spill Show**: Toggle it On to visualize the key before worrying about fill colors or artifacts. Tune Key Hue, Tolerance, and Sat Floor until the key map is clean, then switch back to normal compositing.
2. **Sat Floor prevents gray-area flicker**: Desaturated pixels have unreliable hue angles. Set Sat Floor to 10–20% to prevent them from sporadically entering the key.
3. **Despill overshoots are creative**: At extreme Despill settings, foreground colors shift toward the complement of the key hue. Red key with high despill creates a cyan-tinted foreground — useful for deliberate color effects.

---

## Background

### BBC Colour Separation Overlay

Colour Separation Overlay (CSO) was the BBC's name for their chromakey system, first used in production in the late 1960s. Unlike American systems that typically keyed on blue, the BBC's CSO could key on any saturated color, though yellow and green were most common for Doctor Who-era effects. The circuit compared the amplitude and phase of the chrominance signal to a reference, producing a switching signal that selected between two video inputs on a pixel-by-pixel basis. Early CSO was notoriously temperamental — uneven lighting, wrinkled backdrops, and reflective costumes all caused the key to break down, producing the characteristic "halo" and "tearing" artifacts visible in 1970s BBC productions.

### Hue-Domain Keying

Rather than keying on raw U/V chroma component values (as some simpler keyers do), Voido extracts the hue angle of each pixel using an octant-based atan2 approximation. This approach is angle-invariant: it responds to the *direction* of the chroma vector, not its magnitude. A pixel with deeply saturated green and a pixel with pale, desaturated green can both match the same key hue, provided their hue angle is similar. The Tolerance control sets the angular width of the acceptance zone. The Saturation Floor control provides a safety gate: pixels below a minimum chroma magnitude are never keyed, preventing the system from keying on gray or white regions that have no meaningful hue.

### Spill Suppression

When a performer stands in front of a colored backdrop, reflected light from the backdrop contaminates the foreground — green light bounces off the green screen and tints the performer's hair, skin, and costume. This contamination is called *spill*. Professional keyers include a despill stage that identifies and removes the key-color component from foreground pixels. Voido's despill computes the U/V component vector of the key hue and subtracts a scaled version of it from the foreground chroma, effectively pulling contaminated colors back toward neutral. The Despill control sets the strength of this correction.

### Edge Artifacts and Slew Limiting

Real analog keyers suffer from bandwidth and timing limitations that produce artifacts at the boundary between foreground and background. The key signal — which is derived from the chroma — has limited slew rate: it cannot switch instantaneously from "foreground" to "background" at a sharp edge. This produces a visible transition zone where neither source is cleanly selected, resulting in edge tearing, color fringing, and semi-transparent blending. Voido simulates these artifacts with two mechanisms: an LFSR noise source that modulates the key signal at boundaries, and a slew-rate limiter that restricts how fast the key can change from pixel to pixel. Higher Artifact settings increase the noise amplitude and decrease the slew rate, producing increasingly unstable edges.

### Fill Patterns

In a real compositing scenario, the fill behind keyed regions comes from a second video source. Voido provides four built-in fill options for standalone use: a flat matte colored by the Fill Color pot, horizontal stripe bars, a position-dependent color ramp, and a checkerboard grid. These patterns serve both practical and creative purposes — the flat matte is useful for clean compositing, while the geometric patterns create graphic effects when combined with high Artifact settings.


---

## Signal Flow

Hue Extraction → Key Generation → Foreground Path → ... → Mix → Sync Signals

```
Input Video (YUV 4:4:4)
│
├── Hue Extraction ─────────────────────────────────────────────
│   └─ 1. Octant + Ratio atan2    (U,V → 10-bit hue angle)
│      └─ Chroma magnitude         (Manhattan |U| + |V|)
│
├── Key Generation ─────────────────────────────────────────────
│   ├─ 2. Circular hue distance    (|pixel_hue − key_hue| mod 1024)
│   ├─ 3. Tolerance ramp           (linear ramp within window)
│   ├─ 4. Saturation gate          (suppress key below Sat Floor)
│   ├─ 5. Artifact generator       (LFSR noise + slew limiter)
│   ├─ 6. Hard/Soft key mode       (binarize or keep soft ramp)
│   └─ 7. Key inversion            (optional complement)
│
├── Foreground Path ────────────────────────────────────────────
│   └─ 8. Despill                  (subtract key-color UV component)
│
├── Fill Path ──────────────────────────────────────────────────
│   └─ 9. Fill generator           (matte / bars / ramp / grid)
│
├── Compositor ─────────────────────────────────────────────────
│   ├─ 10. Alpha blend             (FG × (1−key) + Fill × key)
│   └─ 11. Spill Show mode         (key as false-color overlay)
│
├── Mix ────────────────────────────────────────────────────────
│   └─ Interpolator × 3            (wet/dry crossfade per channel)
│
└── Sync Signals ───────────────────────────────────────────────
    └─ 7-clock delay pipeline      (hsync, vsync, field)
```

The key signal flows through three distinct stages before reaching the compositor. First, the raw hue comparison outputs a linear ramp within the tolerance window (1023 at exact match, 0 outside). Second, the saturation gate zeros the key for low-chroma pixels. Third, the artifact generator adds noise and slew limiting. The order is critical: noise is added *after* the saturation gate, so desaturated regions remain cleanly unkeyed even with high artifact settings. The hard/soft key mode and key inversion operate on the final post-artifact key signal.

The foreground despill and fill generation run in parallel (Stage 4 in the VHDL pipeline), both using the delayed input data from the alignment pipe. This means the despill computation does not depend on the fill — each path operates independently, and the compositor simply blends the two based on the key value. The spill-show diagnostic mode bypasses the compositor entirely, displaying the raw key signal as monochrome luma with neutral chroma.

---

## Parameter Reference

<img src={voido_control_panel} alt="Videomancer front panel with Voido loaded"/>
*Videomancer's front panel with Voido active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Key Hue
| Property | Value |
|----------|-------|
| Range | 0° – 359° |
| Default | 120° |
| Suffix | ° |

Sets the target hue angle for chromakey extraction. The control spans the full 360° hue circle: 0° corresponds to pure red, 120° to green, 240° to blue, with all intermediate hues available. For traditional green-screen keying, set this to approximately 120° (the default). For blue-screen keying, use approximately 240°. The hue extraction uses an octant-based atan2 approximation internally — 10-bit hue resolution with 8 octants of 128 steps each — so the exact correlation between degree markings and internal hue values is approximate, not exact.

---

#### Knob 2 — Tolerance
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

At 0% only pixels with an exact hue match are keyed — in practice this produces a very noisy, unstable key because even minor color variations fall outside the window. As Tolerance increases, the acceptance angle widens, keying a broader range of hues around the target. At high settings, even moderately off-hue pixels are captured, which can cause foreground elements with similar hues to be incorrectly keyed. A good starting point is 25–35% for typical green-screen footage. Internally, controls the angular width of the keying acceptance window.

---

#### Knob 3 — Despill
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the strength of spill suppression on foreground pixels. The despill circuit computes the U/V component vector of the key hue and subtracts a scaled version from the foreground chroma. At 0% no despill is applied — foreground colors near the key hue retain their original chroma. At moderate settings, the key-color contamination is removed without disturbing other colors. At extreme settings, the despill overshoots and pushes foreground chroma in the opposite direction from the key hue, creating a complementary color cast. Start with 30–40% for natural-looking results.

---

#### Knob 4 — Artifact
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

At 0% the key is clean — edges are smooth (soft mode) or sharp (hard mode) with no noise or tearing. As the control increases, two artifact mechanisms engage: LFSR noise modulates the key value at a pixel level, and a slew-rate limiter restricts how fast the key can transition between foreground and background. The result is edge fringing, tearing, and semi-transparent blending zones that replicate the look of vintage BBC CSO. At maximum, the key becomes highly unstable with visible color bleeding at all boundaries. Internally, controls the intensity of deliberate edge artifacts on the key signal.

---

#### Knob 5 — Fill Color
| Property | Value |
|----------|-------|
| Range | 0° – 359° |
| Default | 0° |
| Suffix | ° |

Sets the hue angle of the fill color used in solid matte mode (Fill Mode 00). The control spans 360° and determines the hue of the flat color that replaces keyed-out regions. This control also affects the base color of the Bars and Grid fill modes, which alternate between the fill color and a dark value. The Color Ramp mode ignores this control, deriving its colors from pixel position instead.

---

#### Knob 6 — Sat Floor
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 6.3% |
| Suffix | % |

Sets the minimum chroma magnitude below which pixels are never keyed, regardless of their hue. This prevents the keyer from acting on desaturated regions — grays, whites, and blacks — that happen to have a hue angle near the key color. At 0% (the default), all pixels with measurable chroma are eligible for keying. Increasing Sat Floor progressively excludes low-saturation pixels, which is useful when the scene contains gray objects that would otherwise flicker in and out of the key.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Fill B0** | 0 | 1 |
| **8 — Fill B1** | 0 | 1 |
| **9 — Key Invert** | Off | On |
| **10 — Spill Show** | Off | On |
| **11 — Hard Key** | Soft | Hard |

Toggles 7 and 8 form a two-bit fill mode selector (4 patterns). Toggle 9 inverts the key signal, swapping foreground and background. Toggle 10 enables a diagnostic display showing the key signal as a false-color overlay. Toggle 11 switches between soft key (smooth alpha transitions at edges) and hard key (binary threshold). Note that Voido has no bypass toggle — use the Mix fader at 0% to pass the original signal through.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade between the composited output and the original unprocessed input. At 100% (default, fully clockwise) the full chromakey effect is visible. At 0% the original signal passes through unchanged. Intermediate positions blend between the two. Since Voido has no bypass toggle, use this fader at 0% to pass the unprocessed signal. The crossfade operates per-channel through three interpolator instances.





---

## Guided Exercises

These exercises progress from basic chromakeying through creative artifact generation. Each demonstrates a different aspect of the CSO simulation, from clean compositing to deliberate vintage degradation.

### Exercise 1: Clean Green Screen Key

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: voido_source1_parrot, after: voido_ex1_s1 },
    { label: "Sunset", before: voido_source2_sunset, after: voido_ex1_s2 },
    { label: "Collage", before: voido_source3_collage, after: voido_ex1_s3 },
    { label: "Pattern", before: voido_source4_pattern, after: voido_ex1_s4 },
    { label: "Woman", before: voido_source5_woman, after: voido_ex1_s5 },
    { label: "Knit", before: voido_source6_knit, after: voido_ex1_s6 },
  ]}
/>
*Clean Green Screen Key — simulated result across source images.*
**Source**: Video of a subject in front of a green backdrop, or any footage with a large area of saturated green.

**What You'll Create**: Set up a clean chromakey with proper despill and tolerance, using solid matte fill.

1. **Set key hue**: Turn Key Hue to approximately 120° (green). With Tolerance at about 25%, the green background should begin to disappear.
2. **Widen tolerance**: Increase Tolerance until the entire green area is cleanly keyed with no residual green patches. Around 30-40% is typical.
3. **Apply despill**: Increase Despill to about 35%. Watch green contamination on the foreground edges disappear. The subject's hair and skin tones should become neutral.
4. **Set fill color**: Turn Fill Color to approximately 210° for a blue matte. The keyed regions fill with solid blue.
5. **Check with Spill Show**: Toggle Spill Show On to see the key signal in monochrome. White areas are keyed, black areas are foreground. Adjust Tolerance and Sat Floor until the separation is clean. Toggle Spill Show Off to return to normal compositing.

**Key concepts**: Hue-domain keying extracts hue angle from UV chroma, tolerance sets angular acceptance width, despill removes key-color contamination from foreground, Spill Show is a diagnostic tool

---

### Exercise 2: Vintage BBC CSO Artifacts

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: voido_source1_parrot, after: voido_ex2_s1 },
    { label: "Sunset", before: voido_source2_sunset, after: voido_ex2_s2 },
    { label: "Collage", before: voido_source3_collage, after: voido_ex2_s3 },
    { label: "Pattern", before: voido_source4_pattern, after: voido_ex2_s4 },
    { label: "Woman", before: voido_source5_woman, after: voido_ex2_s5 },
    { label: "Knit", before: voido_source6_knit, after: voido_ex2_s6 },
  ]}
/>
*Vintage BBC CSO Artifacts — simulated result across source images.*
**Source**: Same green-screen footage as Exercise 1, or any keyed material.

**What You'll Create**: Introduce deliberate edge artifacts to replicate the look of 1970s BBC Colour Separation Overlay.

1. **Start clean**: Begin with the clean key from Exercise 1.
2. **Add artifacts**: Slowly increase Artifact from 0% to about 50%. Watch the key edges begin to tear and flicker with noise.
3. **Switch to Hard Key**: Toggle Hard Key to Hard. The soft transitions snap to binary — either foreground or background, with noisy edges producing visible tearing.
4. **Increase artifacts further**: Push Artifact to about 70%. The edges become heavily fringe-colored with visible slew-rate-limited tearing — pixels along the boundary switch unpredictably between foreground and fill.
5. **Try fill patterns**: Switch Fill B0 to 1 (Horizontal Bars). The bars become visible through the torn key edges, creating a retro broadcast-error aesthetic.
6. **Key Invert**: Toggle Key Invert On. Now the foreground disappears and the green screen remains, with all artifacts inverted.

**Key concepts**: Artifact generator adds LFSR noise and slew-rate limiting, hard key binarizes the key signal, higher artifact = more vintage degradation, key invert swaps foreground and background

---

### Exercise 3: Creative Color Extraction

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: voido_source1_parrot, after: voido_ex3_s1 },
    { label: "Sunset", before: voido_source2_sunset, after: voido_ex3_s2 },
    { label: "Collage", before: voido_source3_collage, after: voido_ex3_s3 },
    { label: "Pattern", before: voido_source4_pattern, after: voido_ex3_s4 },
    { label: "Woman", before: voido_source5_woman, after: voido_ex3_s5 },
    { label: "Knit", before: voido_source6_knit, after: voido_ex3_s6 },
  ]}
/>
*Creative Color Extraction — simulated result across source images.*
**Source**: Any colorful footage — street scenes, nature, abstract patterns — without a dedicated green screen.

**What You'll Create**: Use Voido as a creative color extraction tool to isolate and replace arbitrary hue ranges within the image.

1. **Pick a hue**: Sweep Key Hue through 360° while watching the image. Find a hue that isolates an interesting region — a blue sky, red clothing, warm skin tones.
2. **Set tolerance**: Adjust Tolerance to capture the desired area. Use Spill Show to visualize exactly which pixels are selected.
3. **Grid fill**: Set Fill B0=1, Fill B1=1 for checkerboard grid. The keyed regions become a repeating pattern while the non-keyed colors remain.
4. **Sat Floor gating**: Increase Sat Floor to exclude gray areas from the key. This cleans up noise in shadows and highlights.
5. **Soft artifact halo**: Set Artifact to about 30% in Soft mode. The key edges develop a subtle halo that blends the foreground into the pattern fill.
6. **Reduce mix**: Bring Mix to about 60% to let the original image show through the effect partially.

**Key concepts**: Voido keys on any hue not just green, Sat Floor prevents keying desaturated pixels, fill patterns create graphic effects when used creatively, mix controls effect intensity

---


## Tips

- **Artifact intensity maps to era**: Low artifact = modern digital keyer. Medium artifact = 1980s analog keyer. High artifact = 1970s BBC CSO. Maximum artifact = broken equipment.
- **Hard Key + High Artifact = maximum vintage**: This combination produces the most dramatic edge tearing and binary switching artifacts.
- **Fill patterns behind real content**: The grid and ramp fills create strong graphic effects. Use them with a moderate key and soft edges for pattern textures that follow the scene's color structure.
- **No bypass — use Mix**: Since there's no bypass toggle, set Mix to 0% for a clean pass-through, or use it as an opacity control for the keyed composite.
- **Key Invert for color isolation**: Instead of removing a color, invert the key to *keep only* that color. Everything that isn't the key hue becomes fill — an instant color isolation tool.

---

## Glossary

| Term | Definition |
|------|------------|
| **Alpha** | A per-pixel transparency value; key=1023 means fully keyed (transparent to fill), key=0 means fully opaque (foreground passes through). |
| **Artifact** | Deliberate imperfections added to the key signal to replicate the edge behavior of vintage chromakey hardware. |
| **Chroma Magnitude** | The length of the UV vector; larger values indicate more saturated color. Used by the saturation gate to exclude desaturated pixels. |
| **Chromakey** | The technique of replacing pixels matching a specific key color with an alternate video source or fill pattern. |
| **CSO** | Colour Separation Overlay; the BBC's term for their chromakey system, used from the late 1960s through the 1980s. |
| **Despill** | Removing contamination of the key color from foreground pixels by subtracting the key-hue UV component. |
| **Fill** | The video content displayed in keyed-out regions; Voido provides four built-in patterns. |
| **Hard Key** | A binary key mode where pixels are either fully keyed or fully unkeyed, with no intermediate values. |
| **Hue Angle** | The angular direction of the UV chroma vector, representing the pure color (red, green, blue, etc.) independent of saturation. |
| **LFSR** | Linear Feedback Shift Register; a hardware pseudo-random number generator used to produce noise for the artifact stage. |
| **Octant** | One of eight 45° sectors used in the atan2 approximation to extract hue angle from U/V coordinates. |
| **Slew Rate** | The maximum speed at which the key signal can change between adjacent pixels; limiting slew rate produces gradual transitions and tearing. |
| **Soft Key** | A key mode with linear ramp transitions at edges, producing smooth, anti-aliased boundaries between foreground and fill. |
| **Spill** | Reflected light from the backdrop that contaminates the foreground subject's colors with the key hue. |
| **Tolerance** | The angular width of the hue acceptance window; larger tolerance captures a wider range of hues around the key target. |

---
