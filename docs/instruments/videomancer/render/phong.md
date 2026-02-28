---
draft: true
sidebar_position: 198
slug: /instruments/videomancer/phong
title: "Phong"
image: /img/instruments/videomancer/phong/phong_hero.png
---

import phong_animation from '/img/instruments/videomancer/phong/phong_animation.gif';
import phong_control_panel from '/img/instruments/videomancer/phong/phong_control_panel.png';
import phong_exercise1_result from '/img/instruments/videomancer/phong/phong_exercise1_result.gif';
import phong_exercise2_result from '/img/instruments/videomancer/phong/phong_exercise2_result.gif';
import phong_exercise3_result from '/img/instruments/videomancer/phong/phong_exercise3_result.gif';
import phong_hero from '/img/instruments/videomancer/phong/phong_hero.png';

# Phong

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={phong_hero} alt="Phong hero image"/>
*Phong rendering animated spheres with Blinn-Phong specular highlights, rim lighting, and user-defined chrominance orbiting against a dark background.*
<img src={phong_animation} alt="Phong animated output"/>
*Phong output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Phong brings classical 3D illumination to the Videomancer pipeline. The program generates up to four implicit spheres with real-time Phong shading — ambient, diffuse, and specular components computed per pixel on every frame. No geometry is stored in memory; sphere surfaces are defined by a distance test against analytically computed centers, and surface normals are derived directly from pixel position.

The name honours Bui Tuong Phong, whose 1973 PhD dissertation at the University of Utah introduced the specular reflection model that bears his name. Every real-time 3D renderer since — from arcade cabinets to modern GPUs — descends from Phong's insight that specular highlights can be approximated by raising the cosine of the reflection angle to a power.

Phong synthesises its own imagery: sphere centers drift in Lissajous orbits driven by DDS phase accumulators, the light source rotates via its own DDS, and the specular power spans seven octaves of shininess. At low Orbit Speed the spheres hover serenely; at high speed they trace complex figures of eight. The Video Sphere toggle replaces the synthetic surface colour with the incoming video signal modulated by illumination, turning any camera feed into a spherical projection.

---

## Background

### The Phong Reflection Model

Phong's model decomposes the light arriving at the viewer into three independent terms. **Ambient** is a constant floor representing light that has bounced so many times it reaches everywhere equally. **Diffuse** reflection obeys Lambert's cosine law: the brightness of a matte surface is proportional to the dot product of the surface normal with the light direction, $I_d = k_d \max(0, \mathbf{N} \cdot \mathbf{L})$. **Specular** reflection models the concentrated highlight of a glossy surface: $I_s = k_s (\mathbf{R} \cdot \mathbf{V})^n$, where $\mathbf{R}$ is the reflected light direction and $n$ controls the sharpness of the highlight.

### Implicit Surfaces and Distance Fields

A sphere centred at $(c_x, c_y)$ with radius $r$ is the set of pixels satisfying $(x - c_x)^2 + (y - c_y)^2 \leq r^2$. Phong tests this at every pixel, every frame, with no stored geometry — the sphere exists as a mathematical condition, not as a mesh. The surface normal at any on-sphere pixel is simply the normalised displacement vector from the centre: $\mathbf{N} = (x - c_x, y - c_y) / r$.

### DDS Oscillators and Lissajous Figures

Each sphere centre is animated by two independent 16-bit phase accumulators — one per axis — with different increment rates. This makes each sphere trace a Lissajous figure. The increments include prime-number offsets (7919 and 6131 per sphere index) so that the four spheres follow distinct, non-repeating orbits. A triangle-wave function approximates sine from the phase accumulator without any BRAM lookup table.

### Blinn-Phong Variant

The toggle between Phong and Blinn shading selects how the specular highlight is computed. Classic Phong uses the reflected light vector $\mathbf{R}$; Blinn's simplification uses the half-vector $\mathbf{H} = (\mathbf{L} + \mathbf{V}) / 2$ and evaluates $(\mathbf{N} \cdot \mathbf{H})^n$. In Phong's VHDL implementation, the Blinn toggle shares bit 1 with the sphere-count selector, so enabling Blinn simultaneously forces the sphere count to 2 or 4 (the high bit of the two-bit count field is always set). This coupling is a hardware artifact of the register packing.

### Rim Lighting

Rim lighting simulates the bright halo visible on the edges of backlit objects. It is the inverse of the diffuse term: the surface normal at the sphere's rim points nearly perpendicular to the view direction, so $\text{rim} \approx 1 - |\mathbf{N} \cdot \mathbf{V}|$. In the VHDL, this is approximated by the ratio of distance-squared to radius — pixels near the sphere edge have the highest rim contribution.


---

## Signal Flow

```
DDS Phase Accumulators (updated per frame at vsync)
│
├── 4× Sphere X/Y Phase → triangle_wave() → Center Positions
│       └── Prime offsets per sphere index (7919×i, 6131×i)
├── Light Phase → triangle_wave() → Light Direction (lx, ly)
│
└── Per-Pixel Pipeline ──────────────────────────────────────
    │
    ├─ Stage 1: Sphere Distance Test
    │   ├── dx = hcount - center_x[i], dy = vcount - center_y[i]
    │   ├── dist_sq = dx² + dy²
    │   ├── on_sphere = (dist_sq < radius²) for nearest of [1..4]
    │   └── Store nearest dx, dy, dist_sq
    │
    ├─ Stage 2: Surface Normal
    │   ├── nx ≈ dx >> log2(radius)   (barrel shift approximation)
    │   └── ny ≈ dy >> log2(radius)
    │
    ├─ Stage 3: Phong Lighting
    │   ├── Diffuse: N·L = nx×lx + ny×ly >> 10, clamped ≥ 0
    │   ├── Specular: (N·L)^(2^shin) via iterated squaring (0–6 rounds)
    │   ├── Rim: dist_sq(19:12) if rim enabled, else 0
    │   └── Total = ambient + diffuse/2 + specular + rim/2, clamped to 1023
    │
    ├─ Stage 4: Colour Output
    │   ├── Video Sphere off: Y = illumination, U/V = hue from quadrant map
    │   ├── Video Sphere on:  Y = input_Y × illumination >> 10, U/V = input
    │   └── Background: Y = 0, U = 512, V = 512
    │
    └─ Interpolator Mix (4 clk) → Bypass Mux → Output
```

The specular exponent is not a smooth ramp — it is $2^k$ where $k$ is the 3-bit quantised Shininess value. This means jumps between exponents 1, 2, 4, 8, 16, 32, 64, 128. The iterated-squaring loop runs up to 7 rounds, multiplying the base dot product by itself at each step. At high shininess the highlight becomes a single bright pixel. The Blinn/sphere-count coupling on register bit 1 means that switching from Phong to Blinn always changes the number of visible spheres — an intentional limitation of the packed toggle register.

---

## Parameter Reference

<img src={phong_control_panel} alt="Videomancer front panel with Phong loaded"/>
*Videomancer's front panel with Phong active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Orbit Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Orbit Speed controls how fast the sphere centres drift. At 0% the spheres are stationary (phase accumulators frozen). As you increase the speed, the Lissajous orbits become visible — each sphere traces a distinct figure of eight because of the prime-number increments per index. At 100% the spheres race across the screen. Because the DDS updates once per frame at vsync, higher speeds do not cause flicker — just faster movement.

---

#### Knob 2 — Sphere Size
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Sphere Size maps linearly to the sphere radius: 0% gives a tiny 32-pixel sphere, 100% gives a nearly screen-filling 480-pixel sphere. The radius maps as $r = \text{pot}/2 + 32$. Radius squared is precomputed once per frame and used in every per-pixel distance test. Large spheres reveal the limitations of the barrel-shift normal approximation — the surface shading can show stepped bands near the equator.

---

#### Knob 3 — Shininess
| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 4 |

Shininess uses the Steps-8 control mode. The 3 most significant bits of the register select the specular exponent: values 0–7 correspond to $2^0$ through $2^7$ squarings. Low values create a broad, matte highlight spread across much of the sphere. High values compress the specular into a tiny, bright point — the classic "billiard ball" look of high-gloss materials.

---

#### Knob 4 — Ambient
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |
| Suffix | % |

Ambient sets the constant illumination floor. At 0% the far side of each sphere is pure black. At 100% the entire sphere is uniformly lit — no diffuse or specular shading is visible because the ambient dominates. The ambient value is added directly to the total illumination before saturation clamping.

---

#### Knob 5 — Light Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Light Speed controls the DDS increment for the light-direction phase accumulator. At 0% the light is static; at 100% it rotates rapidly around the scene. The light direction vector is computed from a triangle-wave sine approximation at 90° phase offset between X and Y, producing a circular orbit. At high speed the specular highlight sweeps across each sphere like a searchlight.

---

#### Knob 6 — Sphere Hue
| Property | Value |
|----------|-------|
| Range | 0deg – 360deg |
| Default | 0deg |
| Suffix | deg |

Sphere Hue uses a 360° polar mode to set the chrominance of the sphere surface. The VHDL maps the 10-bit register to four quadrants of the YUV colour space: 0–255 shifts U and V above midpoint, 256–511 drops V while U falls, 512–767 drops both, 768–1023 raises V while U rises. The result cycles through warm reds, greens, cyans, and magentas. When Video Sphere is enabled, this control is ignored — the input video's chrominance replaces the synthetic colour.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Spheres** | 1 | 2 |
| **8 — Lighting** | Phong | Blinn |
| **9 — Rim Light** | Off | On |
| **10 — Video Sphere** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles share a packed register. Toggle 7 uses bits 1:0 as a two-bit sphere-count selector (1/2/3/4). Toggle 8 uses bit 1 for the Phong/Blinn switch — because bit 1 overlaps with the high bit of the sphere-count field, enabling Blinn forces that bit high. Toggles 9 (Rim Light), 10 (Video Sphere), and 11 (Bypass) are independent single-bit controls.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade between the delayed input signal and the rendered sphere output. At 0% the output is pure input (dry). At 100% the output is the full sphere rendering (wet). Intermediate values blend the two via the 4-clock interpolator, allowing the spheres to float as a translucent overlay on top of upstream video.

---

## Guided Exercises

These exercises progress from a single static sphere through multi-sphere animation to video-textured surfaces, exploring each control's contribution to the Phong illumination model.

### Exercise 1: Single Lit Sphere

<img src={phong_exercise1_result} alt="Single Lit Sphere result"/>
*Single Lit Sphere — simulated result across source images.*
**Objective**: Understand the three components of the Phong illumination model: ambient, diffuse, and specular.

1. **Isolate ambient**: Set Ambient to ~50%, Shininess to 1, Orbit Speed and Light Speed to 0%. The sphere appears as a uniform grey disc — no shading variation because the light is static and diffuse is minimal at low exponent.
2. **Add diffuse**: Observe the sphere. One side is brighter than the other because the static light direction creates a nonzero N·L gradient. Increasing Ambient washes this out; decreasing it makes the gradient more dramatic.
3. **Sharpen specular**: Increase Shininess to 6 or 7. A tiny, bright highlight appears where N·L is maximum. Move the light by increasing Light Speed slightly — the highlight glides across the surface.
4. **Rim glow**: Enable Rim Light (Toggle 9). A bright edge appears around the sphere silhouette. Set Ambient low (~10%) and observe the backlit halo effect.
5. **Sweep light speed**: Increase Light Speed to ~50%. The highlight now orbits the sphere. Note how the diffuse shading follows the light direction while the specular point is much more localised.

**Key concepts**: Ambient provides a global floor, diffuse follows Lambert's cosine law $\max(0, \mathbf{N} \cdot \mathbf{L})$, specular concentrates via the exponent, rim approximates edge glow

---

### Exercise 2: Multi-Sphere Lissajous Ballet

<img src={phong_exercise2_result} alt="Multi-Sphere Lissajous Ballet result"/>
*Multi-Sphere Lissajous Ballet — simulated result across source images.*
**Objective**: Explore sphere count, orbit speed, and the interaction between overlapping spheres.

1. **Two spheres**: Set Spheres to 2 and Orbit Speed to ~25%. Two spheres drift across the screen in distinct Lissajous paths. Notice they never share the same orbit — the prime offsets guarantee different frequencies.
2. **Four spheres**: Set Spheres to 4. The screen becomes busier. When spheres overlap, only the nearest one is shaded — no transparency or blending. Observe how highlights wink in and out as spheres occlude each other.
3. **Speed up**: Increase Orbit Speed to ~80%. The complex orbital patterns become visible as the spheres trace loops. At very high speed, the trails may become hard to track — this is where feedback routing would create persistence.
4. **Change size**: Reduce Sphere Size to ~20%. The small spheres dart quickly across the screen, each carrying its own specular highlight. Increase to ~80% and watch the large overlapping discs create a disco-ball-like effect.
5. **Add colour**: Sweep Sphere Hue from 0° through 360°. All spheres share the same chrominance — the colour changes uniformly.

**Key concepts**: DDS phase accumulator animation, prime-number frequency offsets, nearest-sphere occlusion, Lissajous figure formation

---

### Exercise 3: Video-Textured Spheres

<img src={phong_exercise3_result} alt="Video-Textured Spheres result"/>
*Video-Textured Spheres — simulated result across source images.*
**Objective**: Use Video Sphere mode to project live camera or upstream video onto the sphere surface using Phong lighting as a modulator.

1. **Enable Video Sphere**: Toggle Video Sphere on. The sphere surface now shows the input video, with brightness modulated by the Phong illumination. Dark areas of the sphere show dark video; the specular highlight creates a bright window.
2. **Adjust lighting**: Set Light Speed to ~30% so the highlight sweeps across the video texture. Observe how the video appears to rotate under a fixed light — this is the illusion of a 3D surface.
3. **Ambient sets black level**: Reduce Ambient to ~5%. The far side of the sphere shows very dark video. Increase to ~40% and the video becomes visible across the entire sphere but with less contrast.
4. **Shininess for texture**: Set Shininess to 2 for a broad, matte-looking highlight. Set to 7 for a hard specular point — the video texture is revealed mainly around that point.
5. **Multiple video spheres**: Set Spheres to 3 and Orbit Speed to ~15%. Now three spheres float across the screen, each showing the same video feed modulated by its own local illumination. Sphere Hue has no effect in this mode.

**Key concepts**: Y output is $Y_{\text{in}} \times \text{illumination} / 1024$, chrominance passes through, illumination acts as a brightness mask, ambient controls minimum visibility

---


## Tips

- **Ambient is your fill light**: Keep it between 5–20% for dramatic shading. Above 50% the sphere becomes a flat disc.
- **Shininess jumps in powers of two**: Steps 1–3 look matte; steps 5–7 look mirror-glossy. There is no smooth continuum — plan your look around the specific exponent values.
- **Blinn changes sphere count**: Because of the bit-1 overlap, toggling Lighting always changes the number of visible spheres. Use this as a creative surprise rather than fighting it.
- **Video Sphere needs input**: In a standalone configuration with no upstream video, Video Sphere mode shows a black sphere. Route a camera or pattern generator upstream for the effect to work.
- **Feedback loops**: Routing Phong's output back to its input creates recursive illumination — the specular highlight feeds back on itself, creating cascading bright rings.
- **Rim Light for silhouettes**: Combine Rim Light with low Ambient and zero Shininess for a clean silhouette outline — the sphere appears as a backlit disc.
- **Colour cycling**: Automate Sphere Hue via MIDI CC for smooth colour transitions. The quadrant mapping produces four distinct tonal zones per revolution.

---

## Glossary

| Term | Definition |
|------|------------|
| **Ambient** | Constant illumination floor; models indirect light reaching all surfaces equally regardless of orientation. |
| **Blinn-Phong** | Variant specular model using the half-vector instead of the reflection vector; slightly broader highlight than classic Phong. |
| **DDS** | Direct Digital Synthesis; a phase-accumulator technique that generates waveforms by incrementing a counter and reading a function at each step. |
| **Diffuse** | Lambertian reflection proportional to the cosine of the angle between the surface normal and the light direction. |
| **Implicit Surface** | A surface defined by a mathematical condition (e.g., distance from centre ≤ radius) rather than by stored geometry. |
| **Lissajous Figure** | A parametric curve produced by two harmonic oscillators at different frequencies, creating figure-eight or looping patterns. |
| **Phong Shading** | An illumination model combining ambient, diffuse, and specular components to simulate surface lighting. |
| **Rim Light** | A bright halo at the silhouette edge of a surface, approximating backlighting. |
| **Specular Exponent** | The power $n$ in $(\mathbf{R} \cdot \mathbf{V})^n$ that controls the sharpness of the specular highlight. |
| **Triangle Wave** | A piecewise-linear approximation of a sine wave, rising and falling in straight ramps; used as a zero-BRAM sine substitute. |
| **YUV** | A colour encoding separating luminance (Y) from chrominance (U, V), used throughout the Videomancer pipeline. |
