---
draft: true
sidebar_position: 99
slug: /instruments/videomancer/flaregun
title: "Flaregun"
image: /img/instruments/videomancer/flaregun/flaregun_hero.png
description: "Bright light entering a camera lens scatters off internal glass surfaces, creating glowing halos, horizontal streaks, and star-shaped diffraction patterns."
---

import flaregun_hero from '/img/instruments/videomancer/flaregun/flaregun_hero.png';
import flaregun_before_after from '/img/instruments/videomancer/flaregun/flaregun_before_after.png';
import flaregun_control_panel from '/img/instruments/videomancer/flaregun/flaregun_control_panel.png';
import flaregun_exercise1_result from '/img/instruments/videomancer/flaregun/flaregun_exercise1_result.png';
import flaregun_exercise2_result from '/img/instruments/videomancer/flaregun/flaregun_exercise2_result.png';
import flaregun_exercise3_result from '/img/instruments/videomancer/flaregun/flaregun_exercise3_result.png';

# Flaregun

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={flaregun_hero} alt="Flaregun hero image"/>
*Flaregun compositing radial Gaussian bloom, anamorphic streak, and starburst rays over video in the style of the NewTek Video Toaster's Flare Center effect.*
<img src={flaregun_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Flaregun applied.*

---

## Overview

Bright light entering a camera lens scatters off internal glass surfaces, creating glowing halos, horizontal streaks, and star-shaped diffraction patterns. These artifacts — collectively called *lens flare* — are technically undesirable, but decades of cinema have made them a visual shorthand for brilliance, warmth, and dramatic intensity. Flaregun synthesizes these optical artifacts digitally, compositing them over live video as a controllable light burst overlay.

The program generates three distinct optical components — a radial core bloom with Gaussian falloff, an anamorphic streak (horizontal or vertical), and a starburst ray pattern (4-ray cross or 8-ray asterisk) — sums them with saturating arithmetic, applies a color temperature tint, and adds the result to the input video. The name references both the pyrotechnic signal device that produces a brilliant, expanding light burst and the act of "firing" a lens flare into the video frame at a chosen origin point.

At low intensity, Flaregun adds a subtle luminous glow to a specific region of the frame — a highlight catch on a reflective surface or a soft halo around a light source. At high intensity, the bloom expands to fill the frame with saturating white, reproducing the dramatic "whiteout" transition that made the NewTek Video Toaster's Flare Center and Flare Corners effects iconic in 1990s broadcast television.

---

## Background

### Lens Flare in Cinema

Real lens flare occurs when non-image-forming light enters a compound lens system and bounces between glass element surfaces before reaching the sensor or film. Each internal reflection creates a ghost image of the aperture — typically a bright disc, hexagon, or polygon — at a position determined by the geometry of the lens elements. The sum of all these reflections produces the characteristic multi-element flare pattern: a bright core bloom, secondary ghost reflections, veiling glare that reduces contrast across the frame, and — in lenses with straight aperture blades — starburst rays caused by diffraction. Cinematographers once considered flare a defect to be minimized with lens coatings and matte boxes. J.J. Abrams, Jan de Bont, and other filmmakers turned it into a deliberate stylistic choice, using uncoated or detuned lenses to create flares that suggest the presence of a powerful, almost overwhelming light source just outside or at the edge of the frame.

### The NewTek Video Toaster's Light Effects

The NewTek Video Toaster (1990) included a bank of transition effects that simulated optical phenomena digitally — among them **Flare Center** (a single expanding light burst from the center of the frame) and **Flare Corners** (four simultaneous bursts converging from each corner). These effects were revolutionary because they brought cinematic lens flare to desktop video editing at a time when such effects required expensive optical printers or dedicated hardware. The Toaster's flare effects were typically used as *transitions* — the flare would build to a peak whiteout, revealing the next scene as it faded — but they were equally effective as decorative overlays. Their warm, slightly golden visual quality became a ubiquitous signature of wedding videos, worship broadcasts, and corporate presentations throughout the 1990s. Flaregun recreates this aesthetic as a continuously controllable real-time overlay rather than a canned transition sequence.

### Anamorphic Streaks and CinemaScope

The horizontal streak that characterizes cinematic lens flare comes from **anamorphic lenses** — cylindrical optics that compress a wide field of view onto a narrower film frame. Because anamorphic elements have different curvature in the horizontal and vertical axes, internal reflections are stretched along the horizontal, producing the characteristic blue-white horizontal line passing through bright light sources. This artifact became so associated with the widescreen cinema experience that it is now deliberately simulated in post-production even when spherical lenses were used for shooting. Flaregun's Streak control implements this as a narrow perpendicular Gaussian envelope multiplied by a wide linear falloff along the primary axis.

### Gaussian Bloom and Radial Falloff

The core bloom component uses a **Gaussian radial falloff** — intensity decreases as $e^{-(r/\sigma)^2}$ where $r$ is the distance from the flare origin and $\sigma$ is the bloom radius. This produces a smooth, bell-curve-shaped brightness profile that looks naturally optical. The FPGA implements this via a 64-entry lookup table, with distance normalized to the table range so that the bloom footprint scales with the Intensity control. Radial distance itself is approximated using the **octagon metric**: $d \approx \max(|dx|, |dy|) + \frac{3}{8} \min(|dx|, |dy|)$, which avoids the square root needed for true Euclidean distance and produces a slightly faceted but visually convincing circular profile.

### Starburst Ray Generation

In a real camera, starburst rays are **diffraction spikes** caused by the straight edges of the aperture blades. A lens with $n$ straight blades produces $n$ or $2n$ rays depending on whether $n$ is even or odd. Flaregun approximates this by testing whether each pixel falls within a narrow angular sector aligned with the ray directions. For 4-ray mode, rays follow the horizontal and vertical axes (a cross pattern). For 8-ray mode, four additional diagonal rays are added by testing the condition $|dx| \approx |dy|$, which identifies pixels along the 45° and 135° diagonals. Each ray's brightness decreases linearly with distance from the origin, creating the tapered spike shape characteristic of diffraction artifacts.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Position Counters ──────────────────────────────────────────
│   ├─ h_count: pixel position within line
│   └─ v_count: line position within frame
│
├── Animation Counter ──────────────────────────────────────────
│   └─ frame_count: 8-bit counter (vsync-driven triangle wave)
│
├── Coordinate Transform (Stage 1) ─────────────────────────────
│   ├─ origin_h = Origin X × 1280 >> 10
│   ├─ origin_v = Origin Y × 720 >> 10
│   ├─ dx = h_count − origin_h
│   ├─ dy = v_count − origin_v
│   └─ abs_dx, abs_dy
│
├── Radial Distance (Stage 2) ──────────────────────────────────
│   └─ dist ≈ max(|dx|,|dy|) + ½×min − ⅛×min  (octagon approx)
│
├── Component Calculation (Stage 3) ────────────────────────────
│   ├─ Core Bloom:     Gaussian LUT[dist × 63 / bloom_radius]
│   ├─ Anamorphic Streak:  Gaussian(perpendicular) × linear(primary)
│   └─ Starburst Rays: 4-ray cross + optional 8-ray diagonals
│
├── Composite (Stage 4) ────────────────────────────────────────
│   ├─ flare_total = saturate(core + streak + rays)
│   ├─ flare_scaled = flare_total × anim_intensity >> 10
│   ├─ Color tint: warmth → 4-band YUV tint (cool → neutral → gold → amber)
│   ├─ Y_out = clamp(Y_in + flare_scaled × flare_Y >> 10)
│   ├─ U_out = clamp(U_in + flare_scaled × (flare_U − 512) >> 10)
│   └─ V_out = clamp(V_in + flare_scaled × (flare_V − 512) >> 10)
│
├── Wet/Dry Mix (Stages 5–8) ───────────────────────────────────
│   └─ 3× interpolator_u: lerp(original, composited, Mix)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ 8-clock delay pipeline (hsync, vsync, field)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The three flare components — core bloom, anamorphic streak, and starburst rays — are computed independently in Stage 3 and then summed with saturating arithmetic in Stage 4 before a single color tint is applied. This means the streak and rays inherit the same warmth color as the core bloom. The critical interaction is between the Intensity control and the animation system: when animation is enabled, a triangle-wave frame counter modulates the effective intensity, causing the bloom radius and overall brightness to pulse. The pulsation does not affect the Streak or Ray Count controls independently — it modulates only the final scaling of the combined flare signal.

---

## Parameter Reference

<img src={flaregun_control_panel} alt="Videomancer front panel with Flaregun loaded"/>
*Videomancer's front panel with Flaregun active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Intensity
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 39.1% |
| Suffix | % |

Controls both the bloom radius and the overall brightness of the flare. At minimum, the bloom collapses to a tiny bright point at the origin. As intensity increases, the Gaussian core bloom expands outward and the additive composite grows brighter, washing out progressively more of the underlying video. At maximum, the bloom radius reaches across a substantial portion of the frame, producing a dramatic white-hot flare that can blow out the image to near-total white. When animation is enabled, this parameter sets the peak intensity of the pulsation cycle.

---

#### Knob 2 — Streak
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Sets the length of the anamorphic streak. At zero, no streak is generated and only the core bloom and rays are visible. As the control increases, a line of light extends outward from the origin along the primary axis — horizontal by default, vertical when the Streak Dir toggle is engaged. The streak uses a tight Gaussian envelope in the perpendicular direction (approximately 8 pixels wide) and a linear falloff along the primary direction, producing the characteristic flat, elongated highlight associated with anamorphic cinema lenses.

---

#### Knob 3 — Ray Count
| Property | Value |
|----------|-------|
| Range | 0 – 3 |
| Default | 1 |

Selects the starburst ray configuration. The four steps of this control determine how many angular ray spikes appear: at lower settings only the 4-ray cross pattern (horizontal and vertical axes) is active, while higher settings add four diagonal rays for an 8-ray asterisk pattern. Diagonal rays are detected by testing $|dx| \approx |dy|$, which identifies pixels along the 45° lines. The Ray Count control only takes effect when the Rays toggle is enabled — with Rays off, no starburst is generated regardless of this setting.

---

#### Knob 4 — Origin X
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Positions the flare origin horizontally within the frame. At 0%, the origin sits at the left edge; at 100%, at the right edge. The pot value is mapped to pixel coordinates by scaling to the active picture width (1280 pixels for HD). All three flare components — bloom, streak, and rays — emanate from this horizontal position, so sweeping this control slides the entire flare assembly across the frame.

---

#### Knob 5 — Origin Y
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Positions the flare origin vertically within the frame. At 0%, the origin sits at the top edge; at 100%, at the bottom edge. Combined with Origin X, this gives full two-dimensional control over the flare source position. Moving the origin toward the edge of the frame shifts the visible bloom off-center, producing the asymmetric flare patterns typical of light sources entering at oblique angles.

---

#### Knob 6 — Warmth
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 58.7% |
| Suffix | % |

Controls the color temperature of the flare. The VHDL uses four discrete tint bands in YUV space: cool blue-white below 25%, neutral warm white from 25–50%, warm gold from 50–75%, and deep amber above 75%. At the cool end, the flare has a slightly blue-tinted quality reminiscent of optically coated modern lenses. At the warm end, it acquires the amber-gold character of uncoated vintage glass — the signature look of the Video Toaster's original flare effects.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Animate** | Off | On |
| **8 — Corners** | Center | Corners |
| **9 — Rays** | Off | On |
| **10 — Streak Dir** | Horiz | Vert |
| **11 — Bypass** | Off | On |

Switches 7–11 control five independent aspects of the flare generation. Animate enables automatic pulsation. Corners is defined in the TOML but not active in the current VHDL implementation. Rays enables or disables the starburst component. Streak Dir swaps the anamorphic streak between horizontal and vertical orientation. Bypass routes the input signal directly to the output for A/B comparison.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Controls the wet/dry mix ratio between the original input video and the flare-composited output. At 0%, the output is the unprocessed input regardless of other settings. At 100%, the full additive composite is output. Intermediate positions blend between the two via the interpolator_u pipeline, which provides a smooth crossfade. This allows dialing in a subtle flare overlay without full-intensity additive blow-out.

---

## Guided Exercises

These exercises progress from a simple centered bloom to complex multi-component flare compositions, exploring each optical element and their interactions.

### Exercise 1: Classic Toaster Bloom

<img src={flaregun_exercise1_result} alt="Classic Toaster Bloom result"/>
*Classic Toaster Bloom — simulated result across source images.*
**Source**: A mid-brightness camera feed or recorded footage with visible content and moderate contrast.

**Objective**: Recreate the warm, centered lens flare of the NewTek Video Toaster's Flare Center effect using only the core bloom and anamorphic streak.

1. **Center the origin**: Set Origin X and Origin Y both to ~50%. The flare origin sits at the center of the frame.
2. **Moderate bloom**: Set Intensity to ~40%. A soft Gaussian glow appears around the center, brightening the underlying video.
3. **Add the streak**: Increase Streak to ~60%. A horizontal line of light appears through the bloom center — the anamorphic signature.
4. **Warm it up**: Increase Warmth to ~70%. The flare shifts from neutral white to warm gold, matching the Toaster's characteristic amber tone.
5. **Adjust mix**: Set Mix to ~75%. The composite is strong but the source video is still visible beneath the flare. Toggle Bypass to compare.
6. **Try animation**: Enable Animate (Switch 7). The bloom begins to pulse — the intensity cycles through a triangle wave, creating a breathing, living light source.

**Key concepts**: Gaussian radial falloff creates a naturally optical bloom, the anamorphic streak adds cinematic character, warmth tinting controls the emotional quality of the light

---

### Exercise 2: Starburst Highlight

<img src={flaregun_exercise2_result} alt="Starburst Highlight result"/>
*Starburst Highlight — simulated result across source images.*
**Source**: Dark footage with isolated bright elements — stage lighting, candles, or specular reflections.

**Objective**: Create dramatic starburst diffraction spikes with 8-ray configuration over dark source material.

1. **Off-center origin**: Set Origin X to ~30% and Origin Y to ~25% to position the flare away from center, as if a light source were entering from the upper left.
2. **Low bloom**: Set Intensity to ~25% for a compact core that does not overwhelm the dark source.
3. **Enable rays**: Turn Rays on (Switch 9). A 4-ray cross pattern appears emanating from the origin.
4. **Switch to 8-ray**: Turn Ray Count to maximum. Diagonal rays appear, producing an 8-pointed asterisk.
5. **No streak**: Set Streak to 0%. The flare is pure bloom and rays, without the horizontal line.
6. **Cool tint**: Set Warmth to ~15%. The rays take on a cool blue-white quality, suggesting a modern multi-coated lens.
7. **Full mix**: Set Mix to ~100%. The additive composite is at full strength — the rays are bright spikes against the dark background.

**Key concepts**: Starburst rays simulate aperture-blade diffraction, 8-ray mode adds diagonals via the |dx−dy| test, cool color tinting conveys a modern optical quality

---

### Exercise 3: Cinematic Anamorphic Sweep

<img src={flaregun_exercise3_result} alt="Cinematic Anamorphic Sweep result"/>
*Cinematic Anamorphic Sweep — simulated result across source images.*
**Source**: Any footage — the flare will dominate the composition at these settings.

**Objective**: Use the anamorphic streak at high intensity with origin movement to simulate a cinematic lens flare sweep across the frame.

1. **Strong streak**: Set Streak to ~90%. The anamorphic line extends nearly across the full frame width.
2. **Moderate bloom**: Set Intensity to ~50%. The core bloom is prominent but does not completely white-out the frame.
3. **Horizontal orientation**: Ensure Streak Dir is set to Horiz.
4. **Edge origin**: Set Origin X to ~10% and Origin Y to ~50%. The flare source is near the left edge of the frame and the long horizontal streak cuts across toward the right.
5. **Warm gold**: Set Warmth to ~80%. Deep amber-gold tinting for maximum cinematic drama.
6. **Rays and mix**: Enable Rays (Switch 9), set Ray Count to ~1 for 4-ray cross only. Set Mix to ~85%.
7. **Sweep**: Slowly turn Origin X from ~10% toward ~90%. Watch the entire flare assembly — bloom, streak, and rays — slide across the frame. The streak always passes through the current origin.
8. **Try vertical**: Toggle Streak Dir to Vert and repeat the sweep with Origin Y.

**Key concepts**: The anamorphic streak always passes through the origin point, sweeping the origin creates a cinematic flare wipe, vertical streak orientation produces a different visual axis

---


## Tips

- **Warmth sets the mood**: Cool blue-white flares suggest modern coated optics (sci-fi, thriller). Warm gold flares invoke vintage lenses and 1990s broadcast nostalgia. Deep amber pushes into sunset-dramatic territory.
- **Streak without bloom**: Set Intensity very low and Streak very high for a pure horizontal (or vertical) line of light through the frame — useful as a compositional element independent of the bloom.
- **Animate for transitions**: Enable animation and sweep Intensity from low to high to simulate a lens flare burst transition. The triangle wave creates a natural build-and-fade cycle.
- **Origin at the edge**: Positioning the origin at the frame edge creates an asymmetric flare with half the bloom clipped — the look of a light source just entering the lens's field of view.
- **Rays need distance**: The starburst pattern only activates beyond 8 pixels from the origin, creating a dark core zone where only the bloom is visible. This matches real diffraction behavior where rays emerge from the aperture edge, not the center.
- **Feedback routing**: Sending Flaregun's output back to its input creates recursive bloom — each pass adds another layer of glow, rapidly building to white. Use low Mix and Intensity settings to control the feedback intensity.
- **Combine with keyers**: Use a downstream key to composite the flare over a different source than the input. Flaregun generates the glow; the keyer controls where it appears.
- **Vertical streak for rain/waterfall**: The vertical Streak Dir creates a columnar light effect that can simulate sunlight through vertically falling water or rain streaks catching light.

---

## Glossary

| Term | Definition |
|------|------------|
| **Additive Composite** | A blending method where the flare and input pixel values are summed, naturally producing blown-out highlights. Brighter areas saturate toward white. |
| **Anamorphic** | Relating to cylindrical lens optics that compress the image horizontally, producing characteristic horizontal streaks through bright light sources. |
| **BRAM** | Block RAM; dedicated memory blocks within the FPGA fabric used for line delays, framebuffers, and lookup tables. |
| **BT.601** | The ITU-R standard defining the color matrix used to convert between RGB and YUV in video systems. |
| **Diffraction Spike** | A streak of light extending radially from a bright point, caused by diffraction around straight-edged aperture blades in a camera lens. |
| **FPGA** | Field-Programmable Gate Array; the reconfigurable hardware chip that implements Videomancer's real-time video processing. |
| **Gaussian Falloff** | An intensity profile that follows the bell curve $e^{-(r/\sigma)^2}$, producing a smooth, optically natural radial brightness gradient. |
| **Lens Flare** | Optical artifacts caused by non-image-forming light scattering within a compound lens system, manifesting as blooms, streaks, and ghost reflections. |
| **Octagon Approximation** | A computationally efficient distance estimate: $d \approx \max(|dx|,|dy|) + \frac{3}{8}\min(|dx|,|dy|)$, avoiding square root operations. |
| **Pipeline** | A chain of processing stages where each stage performs one operation per clock cycle on streaming pixel data. |
| **Saturating Arithmetic** | Addition that clamps at the maximum representable value (1023 for 10-bit) instead of wrapping around, preventing overflow glitches. |
| **Starburst** | A radial pattern of light rays emanating from a bright point source, simulating aperture-blade diffraction. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V); the native format of Videomancer's 30-bit video pipeline. |

---
