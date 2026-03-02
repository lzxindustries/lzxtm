---
draft: true
sidebar_position: 53
slug: /instruments/videomancer/cloudgate
title: "Cloudgate"
image: /img/instruments/videomancer/cloudgate/cloudgate_hero.png
description: "In the early 1990s, the NewTek Video Toaster turned commodity hardware into a broadcast studio."
---

import cloudgate_hero from '/img/instruments/videomancer/cloudgate/cloudgate_hero.png';
import cloudgate_before_after from '/img/instruments/videomancer/cloudgate/cloudgate_before_after.png';
import cloudgate_control_panel from '/img/instruments/videomancer/cloudgate/cloudgate_control_panel.png';
import cloudgate_exercise1_result from '/img/instruments/videomancer/cloudgate/cloudgate_exercise1_result.png';
import cloudgate_exercise2_result from '/img/instruments/videomancer/cloudgate/cloudgate_exercise2_result.png';
import cloudgate_exercise3_result from '/img/instruments/videomancer/cloudgate/cloudgate_exercise3_result.png';

# Cloudgate

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={cloudgate_hero} alt="Cloudgate hero image"/>
*Cloudgate dissolving a video source through multi-octave procedural cloud noise with radial tunnel masking and warm tint.*
<img src={cloudgate_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Cloudgate applied.*

---

## Overview

In the early 1990s, the NewTek Video Toaster turned commodity hardware into a broadcast studio. Among its most iconic features were the cloud-based dissolve transitions — Cloud Tunnel In, Cloud Tunnel Out, and SmokeScreen — which rendered volumetric noise over live video to create the illusion of flying through fog or smoke. Cloudgate recreates these effects as a real-time FPGA program, generating dual-octave procedural noise, applying radial tunnel masking, and alpha-compositing tinted cloud layers over the input signal.

The name *Cloudgate* is a reference to Anish Kapoor's reflective sculpture in Chicago — a polished surface that distorts the sky into itself. Here, the metaphor is inverted: instead of reflecting the sky in metal, you dissolve the video into clouds. The program's four modes (Cloud Tunnel In, Cloud Tunnel Out, Smoke Up, Uniform Clouds) and four tint colors (Warm White Mist, Golden Glow, Cool Gray Mist, Dark Smoke) provide sixteen possible atmosphere combinations, all animated by a continuous drift accumulator that keeps the clouds moving even with static input.

At subtle settings — low density, gentle drift, minimal tunnel masking — Cloudgate adds a soft haze or vignette to the image. At extreme settings, the clouds consume the entire frame, leaving only wisps of the original signal visible through the noise field. The Mix fader controls the blend between the cloud-composited result and the dry input, while Bypass routes the input signal directly to the output for instant A/B comparison.

---

## Background

### Procedural Noise and Lattice Hashing

Cloudgate generates its cloud texture using **value noise** — a technique where pseudo-random values are assigned to points on a regular grid and the spaces between are filled by interpolation. The grid values come from a 16-entry permutation table, indexed by a hash function that combines the integer grid coordinates with a seed: `idx = (gx × 7 + gy × 13) XOR seed`. This flat-hash approach avoids the memory cost of large lookup tables while producing visually convincing randomness. The same permutation engine is shared with the Organica program.

### Fractional Brownian Motion (fBM)

A single octave of value noise produces smooth, blobby shapes. Real clouds have structure at multiple scales — large billows contain smaller puffs, which contain finer wisps. **Fractional Brownian motion** approximates this by summing multiple octaves of noise at increasing frequencies and decreasing amplitudes. Cloudgate uses two octaves: the base octave provides the large-scale cloud shape, and a second octave at double the spatial frequency adds fine detail. The Detail knob controls how much of the second octave is mixed in, ranging from pure smooth blobs (Detail = 0%) to richly textured cloud surfaces (Detail = 100%).

### The Video Toaster Cloud Dissolves

The NewTek Video Toaster (1990) popularized real-time video effects on the Amiga platform. Its transition effects included several cloud-based dissolves where procedural noise fields would sweep across the frame, revealing the next video source as the clouds cleared. Cloud Tunnel In pushed clouds inward from the edges, converging at the center. Cloud Tunnel Out expanded from the center outward. SmokeScreen rolled fog upward across the frame. These effects were revolutionary for their time — previously, such transitions required expensive dedicated hardware. Cloudgate's four modes directly reference these original Toaster transitions.

### Alpha Compositing

The cloud layer is blended with the input video using **alpha compositing**: `output = input × (1 − α) + cloud_color × α`. The alpha value is derived from the noise field after tunnel masking and density thresholding. Where the cloud noise is dense and above the density threshold, alpha approaches 1.0 and the cloud tint color dominates. Where the noise is sparse or below threshold, alpha approaches 0.0 and the input video shows through. This per-pixel blending creates soft, organic boundaries between cloud and video rather than hard edges.

### Radial Tunnel Masking

The tunnel modes use a radial distance calculation to restrict cloud coverage to specific regions of the frame. The distance from each pixel to the frame center is approximated using an **octagon distance** formula: `dist ≈ max(|dx|, |dy|) + min(|dx|, |dy|)/2 − min(|dx|, |dy|)/8`. This avoids the square root needed for true Euclidean distance while producing a reasonably circular mask. In Cloud Tunnel In mode, pixels inside the tunnel radius are clear; outside is clouded. Cloud Tunnel Out reverses this — the center is filled with clouds while the edges remain clear.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Cloud Generation Engine ────────────────────────────────────
│   │
│   ├─ 1. Grid Coordinates       (pixel pos + drift offset → grid int + frac)
│   │      + Hash Lookups         (perm_hash × 4 corners + octave 2)
│   │
│   ├─ 2. Bilinear H-Lerps       (h00↔h10, h01↔h11 via frac_x)
│   │      + Detail Scaling       (oct2 × Detail pot)
│   │
│   ├─ 3. Bilinear V-Lerp        (lerp_x0↔lerp_x1 via frac_y)
│   │      + fBM Combine          (base + detail × 0.5, clamped)
│   │      + Radial Distance      (octagon approx from center)
│   │
│   ├─ 4. Tunnel Mask            (mode-dependent radial gate)
│   │      + Density→Opacity      (threshold + ×4 ramp + brightness)
│   │
│   └─ 5. Tint + Alpha Comp      (cloud_color × α + input × (1 − α))
│
├── Interpolator ───────────────────────────────────────────────
│   └─ Wet/Dry Mix                (4 clocks per channel × 3 = YUV)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ 9-clock delay pipeline     (hsync, vsync, field)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or composited signal
```

The drift accumulator updates once per frame on the vsync falling edge, adding a mode-dependent offset to the pixel coordinates before grid quantization. This means the cloud pattern scrolls continuously even with static video input. The four modes affect both the drift direction (diagonal, radial outward, or strong vertical) and whether the tunnel mask is applied. In Smoke Up mode, the vertical drift component is the full speed value while horizontal drift is only one quarter — creating a rising smoke column. In Uniform Clouds mode, drift is diagonal and no tunnel mask is applied, so the entire frame is covered.

The density-to-opacity conversion applies a hard threshold followed by a ×4 gain ramp. This means clouds transition from fully transparent to fully opaque over approximately one quarter of the noise value range, creating relatively sharp cloud boundaries rather than gradual fades. The Brightness knob scales the final alpha, allowing you to soften even dense clouds into translucent haze.

---

## Parameter Reference

<img src={cloudgate_control_panel} alt="Videomancer front panel with Cloudgate loaded"/>
*Videomancer's front panel with Cloudgate active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Density
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the opacity threshold for the cloud layer. At 0%, even the faintest noise values produce visible clouds, resulting in near-total coverage. At 100%, only the very peak noise values break through, leaving just thin wisps of cloud. This is the primary control for how much of the frame is obscured — think of it as the atmospheric visibility dial. The threshold applies after the tunnel mask, so in tunnel modes only the masked region is affected.

---

#### Knob 2 — Scale
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Sets the spatial frequency of the noise field by selecting which bits of the pixel coordinate feed into the grid quantizer. Low values produce large, billowing cloud formations that span hundreds of pixels. High values create fine, granular cloud textures. The scale affects both octaves proportionally, so the relative detail structure is preserved across the range. At minimum scale, individual hash cells become visible as large rectangular patches.

---

#### Knob 3 — Detail
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the amplitude of the second noise octave in the fBM summation. At 0%, the cloud texture is a single smooth octave — soft, blobby shapes with gentle gradients. Increasing Detail mixes in the second octave at half amplitude, adding fine-grained structure on top of the base shapes. At 100%, the second octave contributes at full strength, producing clouds with clearly visible turbulent detail within each larger formation.

---

#### Knob 4 — Drift Spd
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Sets the speed of the drift accumulator that animates the cloud field. At 0%, the clouds are frozen in place. As you increase the speed, the noise coordinates shift each frame, creating the illusion of cloud movement. The drift direction depends on the mode: Cloud Tunnel modes drift radially outward, Smoke Up drifts strongly upward with slight horizontal turbulence, and Uniform Clouds drift diagonally. At maximum speed, the clouds rush across the frame rapidly.

---

#### Knob 5 — Tunnel
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the radius of the radial tunnel mask in Cloud Tunnel In and Cloud Tunnel Out modes. At 0%, the tunnel is fully closed — in Tunnel In mode, the entire frame is clouded; in Tunnel Out mode, the entire frame is clear. At 100%, the tunnel opens to approximately 640 pixels radius, covering most of the frame. In Smoke Up and Uniform Clouds modes, this control has no visible effect because those modes apply a full-frame mask regardless of the tunnel radius.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Scales the final cloud alpha value after density thresholding. At 0%, the cloud alpha is zero everywhere — no clouds are visible regardless of other settings. At 50%, even fully dense clouds are semi-transparent, allowing the input video to show through. At 100%, clouds above the density threshold are fully opaque. This control acts as a global opacity multiplier, softening the cloud effect without changing its spatial structure.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Mode A** | Off | On |
| **8 — Mode B** | Off | On |
| **9 — Tint A** | Off | On |
| **10 — Tint B** | Off | On |
| **11 — Bypass** | Off | On |

Toggles 7 and 8 (Mode A and Mode B) form a 2-bit mode selector that determines both the drift behavior and tunnel mask type. The four combinations are: Off/Off = Cloud Tunnel In (dense edges, clear center), On/Off = Cloud Tunnel Out (dense center, clear edges), Off/On = Smoke Up (vertical drift, full-frame coverage), On/On = Uniform Clouds (diagonal drift, full-frame coverage). Toggles 9 and 10 (Tint A and Tint B) form a second 2-bit selector choosing the cloud color: Off/Off = Warm White Mist, On/Off = Golden Glow, Off/On = Cool Gray Mist, On/On = Dark Smoke. Toggle 11 is an independent bypass switch.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry mix via three parallel interpolator instances (one per YUV channel). At 0%, the output is the original input signal — no clouds visible. At 100%, the output is the fully cloud-composited result. Intermediate positions blend the two linearly. This provides a smooth fade-in for the cloud effect without changing the cloud structure itself. The interpolator adds 4 clocks of latency per channel, contributing to the total 9-clock pipeline.

---

## Guided Exercises

These exercises progress from basic cloud overlay through tunnel dissolves to animated atmospheric effects. Each introduces additional controls while building on previous understanding.

### Exercise 1: Warm Fog Layer

<img src={cloudgate_exercise1_result} alt="Warm Fog Layer result"/>
*Warm Fog Layer — simulated result across source images.*
**Source**: A landscape or outdoor scene with visible depth — trees, buildings, and sky.

**Objective**: Create a gentle fog overlay that partially obscures distant elements while preserving foreground detail.

1. **Initialize**: Set all controls to defaults. Ensure Bypass is Off, Mode A and B are both Off (Cloud Tunnel In mode).
2. **Reveal clouds**: Slowly decrease Density from 50% toward 30%. Watch as cloud formations begin to appear over the image.
3. **Adjust scale**: Set Scale to approximately 40% for medium-sized cloud formations that suggest atmospheric fog.
4. **Add detail**: Increase Detail to approximately 60% to give the clouds internal texture — soft wisps within larger patches.
5. **Set brightness**: Lower Brightness to approximately 70% so the clouds are semi-transparent, letting the video show through.
6. **Open tunnel**: Increase Tunnel to 100% to expand the clear center area, keeping fog primarily at the frame edges.
7. **Final mix**: Adjust the Mix fader to taste — around 80% provides a natural fog layer.

**Key concepts**: Density controls the opacity threshold (lower = more visible clouds), Brightness scales the global cloud alpha, Tunnel opens a clear window in the center for tunnel modes

---

### Exercise 2: Golden Cloud Tunnel Dissolve

<img src={cloudgate_exercise2_result} alt="Golden Cloud Tunnel Dissolve result"/>
*Golden Cloud Tunnel Dissolve — simulated result across source images.*
**Source**: Two video sources if available, or a single source with strong visual content — a performer, dancer, or graphic animation.

**Objective**: Recreate the classic Video Toaster Cloud Tunnel Out dissolve where golden clouds expand from the center outward.

1. **Set mode**: Enable Mode A (Toggle 7 On) for Cloud Tunnel Out. Leave Mode B Off.
2. **Set tint**: Enable Tint A (Toggle 9 On) for Golden Glow.
3. **Dense clouds**: Set Density to approximately 20% for thick cloud coverage.
4. **Medium scale**: Set Scale to approximately 50% for balanced cloud formations.
5. **Rich detail**: Set Detail to approximately 80% for complex, turbulent cloud texture.
6. **Animate**: Increase Drift Spd to approximately 50%. Watch the clouds flow outward from the center.
7. **Tunnel size**: Start Tunnel at 0% (fully covered), then slowly increase to watch the golden clouds recede from the center, revealing the video source.
8. **Full brightness**: Set Brightness to 100% for opaque golden clouds.

**Key concepts**: Cloud Tunnel Out fills the center and clears the edges, the Tunnel knob becomes the dissolve controller, drift direction is radial outward in tunnel modes

---

### Exercise 3: Dark Smoke Rising

<img src={cloudgate_exercise3_result} alt="Dark Smoke Rising result"/>
*Dark Smoke Rising — simulated result across source images.*
**Source**: A dark, moody scene — nighttime footage, candlelit subjects, or dark abstract patterns.

**Objective**: Create a rising dark smoke effect that drifts upward across the frame, partially obscuring the source.

1. **Set mode**: Enable Mode B (Toggle 8 On), leave Mode A Off — this selects Smoke Up mode.
2. **Set tint**: Enable both Tint A and Tint B (Toggles 9+10 On) for Dark Smoke.
3. **Moderate density**: Set Density to approximately 35% so the smoke has defined tendrils rather than total coverage.
4. **Fine scale**: Set Scale to approximately 70% for smaller, more turbulent smoke wisps.
5. **High detail**: Set Detail to approximately 90% for maximum fBM complexity.
6. **Rising speed**: Set Drift Spd to approximately 60%. Watch the smoke rise vertically with slight horizontal turbulence.
7. **Dim brightness**: Set Brightness to approximately 50% to make the dark smoke semi-transparent, creating a layered effect.
8. **Full mix**: Set Mix to 100%.

**Key concepts**: Smoke Up mode drifts primarily upward with quarter-speed horizontal turbulence, Dark Smoke tint (Y=300) creates dim rather than bright clouds, combining low brightness with dark tint produces translucent shadow layers

---


## Tips

- **Density is subtractive**: Lower Density values produce *more* visible clouds because the threshold is lower. Think of it as "how much noise must accumulate before clouds appear" — less threshold means more clouds.
- **Tunnel only works in tunnel modes**: The Tunnel knob controls the radial aperture, but Smoke Up and Uniform Clouds ignore it entirely. If adjusting Tunnel has no effect, check which mode is active.
- **Scale and Detail interact**: At very large scales (low Scale value), the second octave adds visible high-frequency texture on top of smooth blobs. At very small scales (high Scale value), both octaves are already fine-grained and the Detail control has a subtler effect.
- **Drift accumulates forever**: The drift offset wraps at 16-bit boundaries, so the cloud pattern eventually repeats — but the period is long enough that repetition is not noticeable during normal use.
- **Tint colors affect compositing**: Dark Smoke (Y=300) creates dim overlay clouds, while Warm White Mist (Y=900) creates bright overlay clouds. The same Density and Brightness settings produce visually different opacity when combined with different tints because the tint luminance affects the perceived contrast against the source.
- **Mix for smooth transitions**: Use the Mix fader rather than Bypass for gradual fade-in/fade-out of the cloud effect during live performance.
- **Feedback loops**: Routing the output back to the input creates recursive cloud compositing — each pass adds another layer of cloud, gradually building up dense volumetric effects.
- **Combine with other programs**: Cloudgate works well as a transition layer in a signal chain. Place it after a color correction program to add atmosphere, or before a keyer to create cloud-shaped masks.

---

## Glossary

| Term | Definition |
|------|------------|
| **Alpha Compositing** | Blending two images using a per-pixel opacity (alpha) value: `output = A × α + B × (1 − α)`. |
| **Bilinear Interpolation** | Smoothly blending four grid corner values using horizontal then vertical linear interpolation. |
| **BT.601** | ITU-R standard defining the YUV color space used in standard-definition video; Videomancer uses 10-bit BT.601. |
| **Drift Accumulator** | A counter that increments each frame, shifting the noise coordinate space to animate the cloud pattern. |
| **fBM** | Fractional Brownian Motion; summing multiple octaves of noise at increasing frequency and decreasing amplitude to create natural-looking fractal textures. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Hash Function** | A deterministic function that maps grid coordinates to pseudo-random values via a permutation table. |
| **Octagon Distance** | An approximation of Euclidean distance using only additions and shifts: `max(|dx|,|dy|) + min(|dx|,|dy|)/2 − min(|dx|,|dy|)/8`. |
| **Octave** | In noise terminology, a single layer of the noise function at a specific spatial frequency; fBM sums multiple octaves. |
| **Permutation Table** | A fixed array of pseudo-random values indexed by hashed coordinates to generate repeatable noise patterns. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Value Noise** | A type of procedural noise where random values are assigned to lattice points and interpolated between them. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
