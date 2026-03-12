---
draft: true
sidebar_position: 91
slug: /instruments/videomancer/dottunnel
title: "Dottunnel"
image: /img/instruments/videomancer/dottunnel/dottunnel_hero.png
description: "Dot Tunnel recreates one of the most recognisable effects from the ZX Spectrum, Amstrad CPC, and Amiga demoscene: a three-dimensional tunnel rendered entirely from discrete dots."
---

import dottunnel_hero from '/img/instruments/videomancer/dottunnel/dottunnel_hero.png';
import dottunnel_animation from '/img/instruments/videomancer/dottunnel/dottunnel_animation.gif';
import dottunnel_control_panel from '/img/instruments/videomancer/dottunnel/dottunnel_control_panel.png';
import dottunnel_exercise1_result from '/img/instruments/videomancer/dottunnel/dottunnel_exercise1_result.gif';
import dottunnel_exercise2_result from '/img/instruments/videomancer/dottunnel/dottunnel_exercise2_result.gif';
import dottunnel_exercise3_result from '/img/instruments/videomancer/dottunnel/dottunnel_exercise3_result.gif';

# Dottunnel

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={dottunnel_hero} alt="Dottunnel hero image"/>
*Concentric rings of bright dots spiral toward a central vanishing point, creating the classic demoscene point-cloud tunnel over live video.*
<img src={dottunnel_animation} alt="Dottunnel animated output"/>
*Dottunnel output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Dot Tunnel recreates one of the most recognisable effects from the ZX Spectrum, Amstrad CPC, and Amiga demoscene: a three-dimensional tunnel rendered entirely from discrete dots. Unlike the textured polygonal tunnels of later hardware, early 8-bit demos built the illusion of depth from nothing more than carefully placed individual pixels arranged in concentric circles.

The name is literal. Each ring of dots represents a cross-section of an imaginary cylindrical tunnel. Rings near the viewer are large and bright; rings farther away shrink toward a vanishing point and dim through depth fog. Because every dot position is computed from trigonometric functions each frame, the entire formation can rotate, drift, and pulse while remaining geometrically perfect.

In Videomancer's implementation, the tunnel overlays live video using either additive blending — where dots burn bright hotspots into the picture — or replacement compositing, where each dot punches its colour directly over the source.

---

## Quick Start

1. **Start sparse**: Begin with 8 dots per ring and Low ring count to understand the geometry before adding density.
2. **Use Replace first**: Replace compositing makes dots easier to see against any source material while dialling in tunnel parameters.
3. **Modulate Center X/Y**: Connecting CV to Center X and Center Y produces a compelling orbital wobble that makes the tunnel feel alive.

---

## Background

### The Demoscene Dot Tunnel

Dot tunnels emerged in the late 1980s as a showpiece effect on platforms with no 3D hardware whatsoever. A ZX Spectrum demo might render sixteen rings of eight dots each, updating every frame by scrolling Z depths and recomputing screen positions via integer sine and cosine tables. Despite the simplicity of the algorithm, the visual result — a swirling vortex of luminous particles — was mesmerising, and the effect became a staple of demo competitions on every platform from the Commodore 64 to the Atari ST.

### Perspective Projection in One Division

The key mathematical trick is that a ring of radius R at depth Z projects to screen radius R/Z (after appropriate scaling). This single division — or in fixed-point hardware, a shift-based approximation — converts a flat circle into a foreshortened ellipse that the viewer perceives as receding into the screen. By scrolling Z values forward and wrapping the nearest ring to the far end, the rings appear to fly toward the viewer endlessly.

### Manhattan Distance Particle Rendering

On hardware without floating-point or multiplication-heavy Euclidean distance, dot hits are tested using Manhattan distance: the sum of absolute horizontal and vertical offsets. This produces diamond-shaped rather than circular dots, a characteristic look of 8-bit demo effects. The VHDL implementation tests every visible dot in parallel each clock cycle, tracking the nearest hit and its owning ring index for colour assignment.

### Depth Fog and Rainbow Hue

Two colouring strategies are provided. In Depth mode every dot is white, and its brightness is inversely proportional to its ring's Z depth — near dots blaze while far dots fade, producing natural atmospheric perspective. In Rainbow mode each ring is assigned a hue derived from its index via the same sine LUT used for position calculations, so the tunnel becomes a spinning colour wheel. Both modes multiply by the global Brightness control for overall intensity scaling.


---

## Signal Flow

```
 registers_in(0) ── Depth Speed ─────────────────────────────────────────────┐
 registers_in(1) ── Rotation ────────────────────────────────────────────────┤
 registers_in(2) ── Center X ────────────────────────────────────────────────┤
 registers_in(3) ── Center Y ────────────────────────────────────────────────┤
 registers_in(4) ── Dot Size ────────────────────────────────────────────────┤
 registers_in(5) ── Brightness ──────────────────────────────────────────────┤
 registers_in(6) ── Toggles [Dots/Ring|Rings|Colour|Comp|Bypass] ────────────┤
 registers_in(7) ── Mix Fader ───────────────────────────────────────────────┤
                                                                             │
 ┌────────────────────────────────────────────────────────────────────────────┘
 │
 │    ┌──────────────────┐     ┌────────────────┐     ┌─────────────────────┐
 ├───►│  VBLANK UPDATE   │────►│  DOT POSITION  │────►│  PER-PIXEL DOT     │
 │    │  Z scroll + wrap │     │  sin/cos per   │     │  DISTANCE TEST      │
 │    │  advance rot     │     │  ring × dot    │     │  (Manhattan, all    │
 │    └──────────────────┘     └────────────────┘     │  visible dots)      │
 │                                                    └────────┬────────────┘
 │                                                             │
 │    ┌────────────────────────────────────────────────────┐    │ nearest dot +
 │    │   COLOUR                                          │◄───┘ ring index
 │    │   depth fog = 1023 - ring_z                       │
 │    │   bright = fog × brightness_knob                  │
 │    │   mode: Depth (white) / Rainbow (sine hue)        │
 │    │   composite: Add (Y + dot) / Replace (dot only)   │
 │    └──────────────────────────┬─────────────────────────┘
 │                               │
 │    ┌──────────────────┐       │ processed YUV
 └───►│  INTERPOLATOR    │◄──────┘
      │  dry/wet mix     │
      └──────────────────┘
               │
               ▼
          data_out (YUV)
```

All dot positions are pre-computed during the vertical blanking interval. For each of the 8 or 16 rings, and for each of the 8/12/16/24 dots in a ring, the XY screen position is derived from the ring's Z depth, the global rotation angle, and a per-ring twist offset of seven units per ring index. During active video every pixel is tested against all visible dots simultaneously using Manhattan distance, and the nearest hit determines the output colour. This massively parallel comparison is the most resource-intensive part of the design.

The depth fog calculation produces a natural sense of recession: a ring at Z = 64 glows almost at full brightness, while one at Z = 960 is barely visible. When rainbow colouring is enabled, each ring's hue is derived by multiplying its index by 64 and feeding the result into the sine/cosine LUT, producing a uniformly spaced colour wheel that rotates with the tunnel.

---

## Parameter Reference

<img src={dottunnel_control_panel} alt="Videomancer front panel with Dottunnel loaded"/>
*Videomancer's front panel with Dottunnel active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Depth Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 58.7% |
| Suffix | % |

Depth Speed controls how quickly rings advance toward the viewer. At low values the tunnel creeps forward slowly, giving a floating or meditative quality. At high values rings rush past rapidly, creating a warp-speed effect. The scroll wraps: when a ring's Z exceeds the maximum depth it reappears at the near end, so the tunnel is always infinitely deep.

---

#### Knob 2 — Rotation
| Property | Value |
|----------|-------|
| Range | -180deg – 180deg |
| Default | 17deg |
| Suffix | deg |

Rotation sets the per-frame rotational increment applied to all rings. At the midpoint the tunnel is stationary; turning clockwise adds positive angular velocity (counter-clockwise spin visually), turning counter-clockwise subtracts it. Each ring also receives a small per-ring twist offset proportional to its index, so the overall formation develops a corkscrew shape when rotating.

---

#### Knob 3 — Center X
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Center X positions the tunnel's vanishing point horizontally across the screen. At the midpoint the tunnel is centred; sweeping left or right slides the convergence point, causing the dot formation to tilt like looking at the tunnel from an angle. Combined with Center Y this lets you place the focus anywhere in the frame.

---

#### Knob 4 — Center Y
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Center Y positions the tunnel's vanishing point vertically. At the midpoint it sits at screen centre. Pulling it upward makes the tunnel appear to recede into the sky; pushing downward makes it plunge toward the ground. Rapid CV modulation of both X and Y creates an orbital wobble.

---

#### Knob 5 — Dot Size
| Property | Value |
|----------|-------|
| Range | 1px – 4px |
| Default | 2px |
| Suffix | px |

Dot Size sets the Manhattan distance threshold for a pixel to be considered "inside" a dot. At the minimum step the dots are single pixels — crisp and star-like. At the maximum step each dot becomes a large diamond shape covering many pixels, filling the screen more densely and merging adjacent dots in nearby rings.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Brightness is a global intensity multiplier applied after the depth fog calculation. At zero the dots vanish entirely. At full the nearest rings blaze at maximum white, and even distant rings remain clearly visible. This control works multiplicatively with the depth fog, so it cannot override the natural dimming of far rings — it scales the entire brightness curve.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Dots/Ring** | 8 | 24 |
| **8 — Ring Count** | Low | High |
| **9 — Colour** | Depth | Rainbow |
| **10 — Composite** | Add | Replace |
| **11 — Bypass** | Off | On |

The five toggles control the tunnel's fundamental geometry and presentation. Dots/Ring sets the angular density — more dots per ring fill the circles more completely but cost more computational work. Ring Count doubles the depth resolution from 8 to 16 rings, filling the tunnel interior more densely. Colour switches between monochrome depth-faded dots and a per-ring rainbow. Composite chooses whether dots add brightness to the input image or replace it entirely, and Bypass disables processing for A/B comparison.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Mix crossfades between the dry input signal and the processed dot tunnel output. At minimum the output is entirely dry (input only); at maximum the output is entirely wet (full tunnel effect). Intermediate positions blend the two, letting you fade the tunnel in and out smoothly.





---

## Guided Exercises

These three exercises explore the dot tunnel's geometry, colour, and compositing modes from a minimal starting configuration to a full multi-layered performance setup.

### Exercise 1: Classic Demo Tunnel

<img src={dottunnel_exercise1_result} alt="Classic Demo Tunnel result"/>
*Classic Demo Tunnel — simulated result across source images.*
**What You'll Create**: Recreate the iconic 8-bit demo look: sparse white dots spiralling toward the centre of the screen over a dark background.

1. Start with all pots centred and Bypass off.
2. Set Dots/Ring to 8 and Ring Count to High.
3. Set Colour to Depth for white dots.
4. Set Composite to Replace to see dots on black.
5. Advance Depth Speed slowly — watch rings scroll forward and wrap.
6. Add moderate Rotation to start the corkscrew spin.
7. Reduce Dot Size to minimum for single-pixel dots.
8. Raise Brightness until distant rings are just visible.

**Key concepts**: Perspective projection, depth fog, ring wrapping.

---

### Exercise 2: Rainbow Particle Overlay

<img src={dottunnel_exercise2_result} alt="Rainbow Particle Overlay result"/>
*Rainbow Particle Overlay — simulated result across source images.*
**What You'll Create**: Layer a dense rainbow dot tunnel additively over live video, so the dots glow on top of the source material.

1. Switch Colour to Rainbow.
2. Set Composite to Add.
3. Increase Dots/Ring to 24.
4. Set Ring Count to High.
5. Increase Dot Size to the second step.
6. Raise Depth Speed for a fast-scrolling tunnel.
7. Moderate Rotation for gentle spin.
8. Adjust Mix to taste — around 75% blends well.

**Key concepts**: Additive compositing, rainbow hue assignment, dot size scaling.

---

### Exercise 3: Off-Centre Wormhole

<img src={dottunnel_exercise3_result} alt="Off-Centre Wormhole result"/>
*Off-Centre Wormhole — simulated result across source images.*
**What You'll Create**: Push the vanishing point to one corner and use large dots to create a wormhole-like vortex effect blended with the input.

1. Set Center X to approximately 256 (left quarter).
2. Set Center Y to approximately 768 (lower quarter).
3. Set Dot Size to maximum for large diamond particles.
4. Set Dots/Ring to 16.
5. Set Ring Count to Low for wider ring spacing.
6. Set Composite to Add.
7. Set Colour to Depth for monochrome intensity variation.
8. Increase Rotation fully for violent spin.
9. Set Depth Speed moderate.
10. Blend Mix to around 60%.

**Key concepts**: Off-centre projection, large-dot coverage, angular velocity.

---


## Tips

- **Depth fog is free**: The natural brightness falloff from depth fog means you rarely need to adjust Brightness beyond 75% — let the fog do the work.
- **Combine with feedback**: Patching the output back into the input with a slight delay creates a recursive tunnel-within-tunnel effect.
- **Match Dot Size to content**: Larger dots work well over busy video to ensure visibility; smaller dots suit clean or dark backgrounds.
- **Rainbow at slow rotation**: The colour wheel effect is most readable at slow rotation speeds where individual ring hues are distinguishable.

---
