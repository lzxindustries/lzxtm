---
draft: true
sidebar_position: 282
slug: /instruments/videomancer/vortex
title: "Vortex"
image: /img/instruments/videomancer/vortex/vortex_hero.png
description: "Program guide for Vortex, a Videomancer demo program for the LZX video synthesizer."
---

import vortex_animation from '/img/instruments/videomancer/vortex/vortex_animation.gif';
import vortex_control_panel from '/img/instruments/videomancer/vortex/vortex_control_panel.png';
import vortex_exercise1_result from '/img/instruments/videomancer/vortex/vortex_exercise1_result.gif';
import vortex_exercise2_result from '/img/instruments/videomancer/vortex/vortex_exercise2_result.gif';
import vortex_exercise3_result from '/img/instruments/videomancer/vortex/vortex_exercise3_result.gif';
import vortex_hero from '/img/instruments/videomancer/vortex/vortex_hero.png';

# Vortex

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={vortex_hero} alt="Vortex hero image"/>
*Vortex generating a classic demoscene tunnel with checkerboard textures spiralling into infinite depth, animated by DDS-driven scrolling.*
<img src={vortex_animation} alt="Vortex animated output"/>
*Vortex output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

The tunnel effect is one of the defining visual tricks of the demoscene — a community of programmers who have been pushing the limits of real-time graphics on constrained hardware since the late 1980s. The technique maps each screen pixel to polar coordinates relative to a vanishing point, then scrolls a procedural texture through the resulting warped space to create the illusion of flying into an infinitely deep tunnel. Vortex implements this classic effect in FPGA hardware, running at full video rate with zero frame buffer.

The name *Vortex* captures the spinning, spiralling motion of the tunnel as both depth and rotation scroll simultaneously. The program computes a per-pixel polar coordinate transformation using a pair of 256-entry BRAM lookup tables — one for inverse distance (providing the perspective foreshortening) and one for arctan2 (providing the angular position). These two values become texture coordinates into a procedurally generated checkerboard or stripe pattern. Frame-synced DDS accumulators add scrolling offsets to produce continuous fly-through and rotation animations.

Vortex can operate as a pure synthesis engine generating its own imagery, or it can modulate its output based on the incoming video — either brightening the tunnel walls with the input luma or warping the tunnel geometry using the video signal as a displacement source. The movable vanishing point, configurable texture scale, and depth-gradient colorization provide extensive creative control over the tunnel's appearance.

---

## Background

### Demoscene Tunnel Effects

The tunnel (or "zoom rotator") became a staple of the demoscene in the early 1990s, appearing in productions for the Amiga, Atari ST, and early PC platforms. The key insight was that computing distance and angle for each pixel — operations normally requiring expensive sqrt and atan2 — could be replaced with precomputed lookup tables. A 256×256 distance table and a 256×256 angle table, indexed by (|dx|, |dy|), provided instant per-pixel polar coordinates. On early CPUs this was revolutionary; on an FPGA it maps naturally to BRAM-based constant-time lookups with single-clock access.

### Polar Coordinate Transformation

Every pixel on screen has a Cartesian position (x, y) relative to the tunnel's vanishing point. The polar transform computes two values: the distance from the center (r = sqrt(dx² + dy²)) and the angle (θ = atan2(dy, dx)). For the tunnel illusion, the depth coordinate is 1/r rather than r itself — this creates the perspective compression where distant objects (far from center) are spatially compressed and nearby objects (close to center) are expanded. Vortex uses an octagonal approximation for distance (dist ≈ max(|dx|,|dy|) + 0.41 × min(|dx|,|dy|)) and an octant-symmetric arctan LUT for the angle, avoiding all multiplication and division in the distance computation.

### Inverse Distance and Perspective

The 1/distance LUT is the heart of the tunnel illusion. Pixels near the vanishing point have large distance values and therefore small 1/distance values, meaning they sample texture coordinates that are close together — producing the effect of distant, compressed detail. Pixels at the screen periphery have small distance values and large 1/distance values, sampling widely-spaced texture coordinates that appear to rush toward the viewer. The constant entry at distance=0 (clamped to 255) prevents division by zero at the singularity at the vanishing point.

### DDS Scrolling Animation

Direct Digital Synthesis accumulators provide continuous, phase-coherent scrolling. Each frame, a fixed increment (proportional to the speed parameter) is added to a 20-bit accumulator. The upper 10 bits of this accumulator provide the scroll offset added to the texture coordinates. Because the accumulator naturally wraps at its bit width, the scrolling repeats seamlessly with no discontinuities. Depth speed creates the fly-through effect; rotation speed produces the tunnel spin.

### Depth Shading and Colorization

In a real tunnel, distant surfaces receive less light. Vortex simulates this by multiplying the pattern brightness by the inverse distance value — pixels far from the vanishing point appear dim, while pixels near the center (which represent close surfaces) appear bright. The Depth Color toggle switches between monochrome shading (depth fades to black) and a gradient mode that tints the depth values through the hue spectrum, producing a rainbow tunnel effect.


---

## Signal Flow

```
Vanishing Point (Center X, Y)
│
├── Polar Transform ────────────────────────────────────────────
│   ├─ 1. dx, dy from center        (coordinate subtraction)
│   ├─ 2. |dx|, |dy| + octagonal distance
│   │     └─ Shape: Circle (octagonal approx) / Diamond (Manhattan)
│   ├─ 3. 1/dist BRAM LUT           (256 entries → depth)
│   └─ 3. arctan BRAM LUT           (256 entries → angle)
│         └─ Octant reconstruction   (3-bit → full 10-bit angle)
│
├── Texture Mapping ────────────────────────────────────────────
│   ├─ 4. tex_u = inv_dist + depth_scroll (DDS accumulator)
│   ├─ 4. tex_v = angle + rot_scroll      (DDS accumulator)
│   └─ 4. Scale: tex_scale > 512 → shift left (double frequency)
│
├── Pattern + Shading ──────────────────────────────────────────
│   ├─ 5. Checkerboard: tex_u(5) XOR tex_v(5)
│   │     Stripes: tex_v(4)
│   ├─ 5. Depth shade: inv_dist << 2 (clamped to 1023)
│   └─ 5. Video mod: Bright → shade × video_y / 1024
│                     Warp  → (pass through, geometry warp)
│
├── Colorize ───────────────────────────────────────────────────
│   ├─ 6. Pattern × shade           (bright / dark pattern bands)
│   ├─ 6. Depth color: Mono (neutral UV) / Gradient (hue shift)
│   └─ 6. Wall hue tinting          (add UV components by range)
│
├── Mix ────────────────────────────────────────────────────────
│   └─ Interpolator × 3             (wet/dry crossfade per channel)
│
└── Sync Signals ───────────────────────────────────────────────
    └─ 8-clock delay pipeline        (hsync, vsync, field)
```

The polar coordinate transformation drives everything. The center point is offset by the Center X and Center Y pots, which map the 0–1023 register range to screen coordinates using additive offsets (X adds 448, Y subtracts 16). The octagonal distance approximation uses max + 0.41×min, implemented as max + (min × 105) >> 8, which avoids any true multiplication by exploiting the fact that 105/256 ≈ 0.41. The Diamond shape toggle replaces this with pure Manhattan distance (|dx| + |dy|), producing a more angular tunnel cross-section.

The animation accumulators update once per vsync, adding the speed parameters to 20-bit phase registers. This means the animation rate is locked to the video frame rate, providing perfectly stable scrolling. The upper 10 bits of each accumulator are added to the texture coordinates, so even small speed values eventually produce visible scrolling — the accumulator resolution ensures smooth sub-pixel motion. The Wall Hue parameter adds color tinting by injecting U/V components proportional to the depth shade, with four different hue ranges selected by the parameter's position within the 0–1023 range.

---

## Parameter Reference

<img src={vortex_control_panel} alt="Videomancer front panel with Vortex loaded"/>
*Videomancer's front panel with Vortex active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Depth Spd
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Depth Speed controls how fast the tunnel appears to rush toward the viewer. The DDS accumulator adds this value each frame, so low values produce a gentle drift while high values create a rapid fly-through. At zero the tunnel is static in the depth axis; at maximum the texture scrolls through approximately one full pattern repeat every few frames. The effect is most dramatic with the checkerboard texture, where the alternating dark and light bands create a strobing hypnotic pattern as they scroll.

---

#### Knob 2 — Rot Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |
| Suffix | % |

Rotation Speed controls the angular velocity of the tunnel spin. Like Depth Speed, this drives a DDS accumulator that offsets the angular texture coordinate. Low values produce a slow, graceful rotation; high values create a rapid vortex. Combining depth and rotation speeds produces a spiral motion — the viewer appears to fly through a spinning tunnel, creating complex moiré interactions between the radial texture and the rotational scroll.

---

#### Knob 3 — Center X
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Center X positions the tunnel's vanishing point horizontally. At 512 (center) the tunnel is centered on screen. Moving the pot left shifts the vanishing point left, causing the tunnel to appear to emerge from the left side of the frame; moving right shifts it correspondingly. The VHDL adds a 448-pixel offset, so the full pot range maps to approximately 448–1472 in screen coordinates, covering the central portion of a 1920-wide frame.

---

#### Knob 4 — Center Y
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Center Y positions the vanishing point vertically. Combined with Center X, this lets you place the tunnel anywhere on screen, creating off-axis perspectives that feel like peering into a pipe from an angle. The offset subtraction of 16 pixels compensates for the vertical blanking region, so the midpoint (512) places the center at approximately scan line 496, near the middle of a 1080-line frame.

---

#### Knob 5 — Tex Scale
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Texture Scale controls the spatial frequency of the procedural pattern. Below 512 the pattern uses its native frequency, producing wide checkerboard squares or broad stripes. Above 512 a left-shift doubles the frequency, creating finer detail with more repeats across the tunnel surface. This interacts dramatically with depth shading — finer patterns produce more intricate moiré interference when scrolling, while coarser patterns emphasize the bold geometric structure of the tunnel.

---

#### Knob 6 — Wall Hue
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Wall Hue tints the tunnel wall color. The full parameter range is divided into four zones: below 256 the walls are untinted (neutral); 256–512 adds a warm red-orange tint; 512–768 adds a cool blue-green tint; above 768 adds a mixed warm tone. The tinting is proportional to the depth shade value, so it becomes more saturated near the viewer (bright areas) and fades toward neutral at the vanishing point. This creates natural depth cuing through color temperature.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Texture** | Checker | Stripes |
| **8 — Shape** | Circle | Diamond |
| **9 — Video Mod** | Bright | Warp |
| **10 — Depth Col** | Mono | Gradient |
| **11 — Bypass** | Off | On |

The toggles divide into three functional pairs plus bypass. Texture and Shape configure the generated pattern and distance metric respectively. Video Mod and Depth Color control how the tunnel interacts with the input video and how depth is expressed through color. Bypass routes input directly to output. The four creative toggles interact multiplicatively — each combination produces a distinct visual character.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Mix crossfades between the dry input and the wet tunnel output. At 0% the output is pure input video with no tunnel visible. At 100% the output is the full tunnel synthesis. Intermediate values create a layered effect where the tunnel overlay sits on top of the video at partial opacity. The crossfade operates independently on Y, U, and V channels via three interpolator_u instances.

---

## Guided Exercises

These exercises explore Vortex's tunnel synthesis from basic configuration through complex animation and color effects.

### Exercise 1: Classic Tunnel Fly-Through

<img src={vortex_exercise1_result} alt="Classic Tunnel Fly-Through result"/>
*Classic Tunnel Fly-Through — simulated result across source images.*
**Objective**: Create a basic centered tunnel with moderate fly-through speed to experience the fundamental demoscene tunnel illusion.

1. Set Depth Speed to 40% for moderate fly-through
2. Set Rotation Speed to 0% for pure depth scrolling
3. Center the vanishing point (both Center X and Y at 50%)
4. Set Texture Scale to 50% for medium pattern detail
5. Observe the classic tunnel rushing toward you
6. Slowly increase Rotation Speed and watch the tunnel begin to spin

**Key concepts**: Polar coordinate transformation, inverse distance perspective, DDS-driven scrolling, and the relationship between depth and rotation animation.

---

### Exercise 2: Diamond Spiral with Color Gradient

<img src={vortex_exercise2_result} alt="Diamond Spiral with Color Gradient result"/>
*Diamond Spiral with Color Gradient — simulated result across source images.*
**Objective**: Combine the diamond distance metric with gradient colorization and simultaneous depth/rotation animation for a vivid spiral vortex.

1. Start from Exercise 1 settings
2. Switch Shape to Diamond
3. Switch Depth Color to Gradient
4. Set Depth Speed to 30% and Rotation Speed to 25%
5. Set Wall Hue to 60% for a blue-green tint
6. Observe the diamond-shaped tunnel with rainbow depth gradient
7. Increase Texture Scale above 50% and watch the pattern complexity double

**Key concepts**: Manhattan vs. octagonal distance, depth-through-color expression, interaction between texture frequency and distance metric.

---

### Exercise 3: Off-Axis Video-Modulated Tunnel

<img src={vortex_exercise3_result} alt="Off-Axis Video-Modulated Tunnel result"/>
*Off-Axis Video-Modulated Tunnel — simulated result across source images.*
**Objective**: Move the vanishing point off-center and use the input video to modulate the tunnel brightness, blending synthesis with live imagery.

1. Feed a video source with good contrast (a face, geometric pattern, or landscape)
2. Move Center X to 30% and Center Y to 35% for an off-axis perspective
3. Set Video Mod to Bright
4. Set Depth Speed to 15% for gentle scrolling
5. Set Rotation Speed to 10% for subtle spin
6. Switch Texture to Stripes for radial ring pattern
7. Observe how the input video brightness modulates the tunnel wall intensity
8. Set Mix to 60% and see the tunnel layered over the source

**Key concepts**: Off-axis vanishing point perspective, video-modulated synthesis, wet/dry overlay blending, and the creative interaction between structured synthesis and organic video.

---


## Tips

- **Start with depth only** — set Rotation Speed to zero first to understand the depth perspective, then gradually add rotation for spiral effects.
- **Diamond shape reveals structure** — the angular Diamond distance metric makes the underlying coordinate grid visible, useful for understanding how the polar transform works.
- **Texture Scale is a multiplier** — going above 50% doubles the pattern frequency in one step; use this as a discrete texture detail control rather than a smooth frequency sweep.
- **Wall Hue is zoned** — the parameter range has four distinct color zones rather than a smooth hue sweep, so significant jumps in color occur at the 25%, 50%, and 75% positions.
- **Video Bright mode for layering** — when using Mix at intermediate values, Bright video modulation creates a more natural blend between the tunnel and input video.
- **Off-center tunnels for perspective** — moving the vanishing point to one side creates dramatic asymmetric perspectives, ideal for paired or split-screen setups.
- **Slow speeds for meditation** — very low Depth and Rotation speeds produce a gentle, hypnotic drift suitable for ambient installation work.
- **Stripes emphasize depth** — the stripe pattern creates concentric rings that make the depth compression effect more visually obvious than the checkerboard.
