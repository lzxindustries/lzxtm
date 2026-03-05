---
draft: true
sidebar_position: 267
slug: /instruments/videomancer/shadebob
title: "Shadebob"
image: /img/instruments/videomancer/shadebob/shadebob_hero.png
description: "Shadebob recreates the classic Amiga demoscene \"shade blob\" (shadebob) effect, in which a soft circular or diamond-shaped sprite is additively blended onto a persistent framebuffer."
---

import shadebob_hero from '/img/instruments/videomancer/shadebob/shadebob_hero.png';
import shadebob_animation from '/img/instruments/videomancer/shadebob/shadebob_animation.gif';
import shadebob_control_panel from '/img/instruments/videomancer/shadebob/shadebob_control_panel.png';
import shadebob_exercise1_result from '/img/instruments/videomancer/shadebob/shadebob_exercise1_result.gif';
import shadebob_exercise2_result from '/img/instruments/videomancer/shadebob/shadebob_exercise2_result.gif';
import shadebob_exercise3_result from '/img/instruments/videomancer/shadebob/shadebob_exercise3_result.gif';

# Shadebob

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={shadebob_hero} alt="Shadebob hero image"/>
*A luminous blob traces spiralling paths across a dark framebuffer, leaving colour trails that fade through the spectrum — an Amiga demoscene shadebob effect realised in FPGA hardware.*
<img src={shadebob_animation} alt="Shadebob animated output"/>
*Shadebob output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Shadebob recreates the classic Amiga demoscene "shade blob" (shadebob) effect, in which a soft circular or diamond-shaped sprite is additively blended onto a persistent framebuffer. As the blob moves along a Lissajous trajectory, each pixel it passes gains brightness; the framebuffer then globally decays, creating luminous trails of colour that fade through a palette from hot white through spectral hues to black.

The name derives from the demoscene terminology: a "shade bob" is a bob (blitter object) that adds to rather than replaces the framebuffer contents, producing additive shading. The technique was popularised on the Amiga in the late 1980s and became a staple effect in demos competing at parties such as The Party, Assembly, and Revision. The additive blending creates something closer to photographic light exposure than conventional sprite drawing.

Videomancer's implementation uses a 64×64 framebuffer with 4-bit-per-pixel indexed colour, a configurable circular or diamond stamp shape with variable size, optional dual-bob mode for two simultaneous emitters, and Lissajous motion with adjustable speed and frequency ratio. The Hue Speed knob cycles the palette assignment over time, so trails gradually shift colour as they age.

---

## Quick Start

1. **Balance Decay and Speed**: The trail length is the ratio of blob speed to decay rate. Fast speed with slow decay creates long sweeping trails; slow speed with fast decay creates short, crisp stamps.
2. **Dual Bob for symmetry**: Enable Dual Bob to double the visual complexity without changing the trajectory — the mirrored second blob creates symmetric patterns automatically.
3. **Diamond for geometry**: Diamond stamps create sharper, more angular trail patterns than circles. Use them for crystalline or pixelated aesthetics.

---

## Background

### Amiga Demoscene Shade Blobs

The shadebob effect emerged from the Amiga demoscene circa 1988–1990. The Amiga's blitter could perform per-pixel addition in hardware, allowing coders to efficiently add a soft sprite's brightness to a persistently stored framebuffer. The effect was computationally elegant: a small lookup table defined the blob's shape, and the blitter did the rest. Shadebobs appeared in landmark demos including RSI's "Megademo" (1989) and Sanity's "Arte" (1993), where plasma-like colour trails mesmerised audiences.

### Additive Blending and Persistence

Each frame, the blob shape's brightness values are added to the framebuffer cells it covers, clamped to the maximum palette index (15). Simultaneously, all framebuffer cells are decremented by the Decay amount. This creates a dynamic equilibrium: cells under the current blob position are pushed toward maximum brightness, while cells left behind gradually fade. The rate of decay versus the blob's speed and size determines whether trails are long and diffuse or short and concentrated.

### Lissajous Motion and Frequency Ratio

The blob follows a Lissajous trajectory defined by two orthogonal sine oscillators. The Ratio knob sets the frequency ratio between x and y oscillators — a 1:1 ratio produces circles or ellipses, 1:2 produces figure-eights, and irrational ratios produce dense space-filling curves. The Speed knob scales both frequencies uniformly. Over time these trajectories trace complex spirograph-like patterns across the framebuffer.

### Dual-Bob Mode

When Dual Bob is enabled, a second blob is rendered symmetrically opposite the first on the framebuffer. The two blobs trace mirrored Lissajous curves simultaneously, doubling the trail density and creating symmetric patterns. Their additive contributions can overlap at the centre, producing brighter hotspots where both blobs converge.


---

## Signal Flow

```
 registers_in(0) ── Speed ─────────────────────────────────────────────────┐
 registers_in(1) ── Decay ─────────────────────────────────────────────────┤
 registers_in(2) ── Bob Size ──────────────────────────────────────────────┤
 registers_in(3) ── Hue Speed ─────────────────────────────────────────────┤
 registers_in(4) ── Bright ────────────────────────────────────────────────┤
 registers_in(5) ── Ratio ─────────────────────────────────────────────────┤
 registers_in(6) ── Toggles [Dual Bob|Shape Circ/Diam|Reset|ModVid|Bypass]─┤
 registers_in(7) ── Mix Fader ─────────────────────────────────────────────┤
                                                                            │
 ┌─────────────────────────────────────────────────────────────────────────┘
 │
 │    ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
 ├───►│  LISSAJOUS GEN   │────►│  BLOB STAMP      │────►│  FRAMEBUFFER     │
 │    │  speed × ratio   │     │  circle/diamond  │     │  64×64 × 4bpp   │
 │    │  → (x, y) pos    │     │  additive blend  │     │  global decay    │
 │    │  + mirror for    │     │  size control    │     │  per frame       │
 │    │  dual bob        │     └──────────────────┘     └───────┬──────────┘
 │    └──────────────────┘                                      │
 │                                                              │ 4-bit index
 │    ┌──────────────────┐     ┌──────────────────┐             │
 │    │  PALETTE LOOKUP  │◄────│  HUE ROTATION    │◄────────────┘
 │    │  16-colour table │     │  palette offset   │
 │    │  → YUV 10-bit   │     │  cycles by Hue   │
 │    └───────┬──────────┘     │  Speed per frame │
 │            │                └──────────────────┘
 │    ┌───────┴──────────┐
 │    │  BRIGHTNESS      │
 │    │  × Bright knob   │
 │    └───────┬──────────┘
 │            │
 │    ┌───────┴──────────┐
 └───►│  INTERPOLATOR    │
      │  dry/wet mix     │
      └──────────────────┘
               │
               ▼
          data_out (YUV)
```

The Lissajous oscillator produces an (x, y) position each frame. In Dual Bob mode, a second position is generated as the framebuffer-centre mirror of the first. The blob stamp (either a circular or diamond-shaped soft profile) is additively blended into the framebuffer at each position — cells are incremented by the stamp's radial brightness profile, clamped at 15.

After all blobs are drawn, the entire framebuffer undergoes a global decay pass: every cell is decremented by the Decay amount (clamped at 0). The resulting 4-bit values are looked up in a 16-entry colour palette. The Hue Speed control adds a frame-counter-scaled offset to the palette index, causing the trail colours to cycle through the spectrum over time.

---

## Parameter Reference

<img src={shadebob_control_panel} alt="Videomancer front panel with Shadebob loaded"/>
*Videomancer's front panel with Shadebob active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Speed sets the Lissajous oscillator rate — how quickly the blob traverses its trajectory. At zero the blob is frozen. At moderate values it traces smooth loops. At maximum the blob moves so rapidly that its trail fills the framebuffer before decay can clear old stamps, creating dense plasma-like colour fields.

---

#### Knob 2 — Decay
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 13% |
| Suffix | % |

Decay controls the per-frame brightness decrement applied to all framebuffer cells. At zero there is no decay and the framebuffer accumulates indefinitely toward full white. At moderate values a balanced trail length is maintained. At maximum, stamps vanish almost immediately, leaving only a brief flash at the blob's current position.

---

#### Knob 3 — Bob Size
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Bob Size sets the radius of the blob stamp in framebuffer cells. A small blob produces fine, precise trails like a paintbrush tip. A large blob creates broad, diffuse washes of colour. Very large blobs at high speed can saturate the entire framebuffer, creating a pulsing glow effect rather than distinct trails.

---

#### Knob 4 — Hue Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Hue Speed controls how quickly the palette index offset advances over time. At zero the colour assignment is static — trails fade through a fixed colour gradient. At moderate values the palette rotates slowly, causing the trail colour to drift through the spectrum. At maximum the colours cycle rapidly, creating a rainbow shimmer across the trails.

---

#### Knob 5 — Bright
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Bright is a global luminance multiplier applied to the palette output. At zero the output is black. At full value the palette colours reach their maximum defined brightness. This interacts with the blob's additive blending — even at moderate brightness, cells near the blob centre can appear intense due to additive accumulation.

---

#### Knob 6 — Ratio
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Ratio sets the frequency ratio between the x and y Lissajous oscillators. At minimum the ratio is 1:1, producing circles or ellipses. As the knob increases, the y frequency increases relative to x, producing figure-eights (1:2), trefoils (1:3), and increasingly complex interlocking curves. Higher ratios create denser, more space-filling trajectories.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Dual Bob** | Off | On |
| **8 — Shape** | Circle | Diamond |
| **9 — Reset** | Off | Reset |
| **10 — Mod Vid** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles configure blob rendering and trajectory. Dual Bob adds a second symmetric emitter. Shape switches between circular and diamond stamp profiles. Reset clears the framebuffer. Mod Video and Bypass control video compositing.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Mix crossfades between the dry input and the synthesised shadebob output. At minimum the output is entirely dry. At maximum the output is entirely wet. Intermediate values blend the blob trails over the source material.



> See [Common Controls & Glossary Reference](../common_reference.md) for details.

---

## Guided Exercises

These exercises explore the interaction between blob size, decay rate, and trajectory complexity, progressing from a single simple trail to a dual-bob plasma composition.

### Exercise 1: Single Slow Trail

<img src={shadebob_exercise1_result} alt="Single Slow Trail result"/>
*Single Slow Trail — simulated result across source images.*
**What You'll Create**: Study the core additive blending and decay mechanics with a single slow-moving blob.

1. Disable Dual Bob.
2. Set Shape to Circle.
3. Set Bob Size to approximately 40%.
4. Set Speed to approximately 20%.
5. Set Decay to approximately 30%.
6. Set Ratio to approximately 25% (near-circular trajectory).
7. Set Hue Speed to approximately 20%.
8. Set Bright to approximately 80%.
9. Set Mix to 100%.
10. Observe the blob tracing a circular path with a fading colour trail behind it.

**Key concepts**: Additive blending, decay rate, Lissajous circular trajectory, palette colour cycling.

---

### Exercise 2: Dual Diamond Spirograph

<img src={shadebob_exercise2_result} alt="Dual Diamond Spirograph result"/>
*Dual Diamond Spirograph — simulated result across source images.*
**What You'll Create**: Create a complex dual-bob spirograph pattern using diamond stamps and a higher frequency ratio.

1. Enable Dual Bob.
2. Set Shape to Diamond.
3. Set Bob Size to approximately 30%.
4. Set Speed to approximately 40%.
5. Set Ratio to approximately 60% (complex figure-eight trajectory).
6. Set Decay to approximately 25%.
7. Set Hue Speed to approximately 40%.
8. Set Bright to full.
9. Set Mix to 100%.
10. Observe two diamond blobs tracing mirror-symmetric complex curves with overlapping colour trails.

**Key concepts**: Dual blob symmetry, diamond stamp profile, complex Lissajous ratio, trail overlap.

---

### Exercise 3: Video-Modulated Plasma

<img src={shadebob_exercise3_result} alt="Video-Modulated Plasma result"/>
*Video-Modulated Plasma — simulated result across source images.*
**What You'll Create**: Layer the dual-blob effect over live video as a performance-ready composite.

1. Continue from Exercise 2 with Dual Bob and Diamond.
2. Enable Mod Video.
3. Set Mix to approximately 70%.
4. Feed a high-contrast video source.
5. Adjust Speed and Ratio to find a visually pleasing trajectory.
6. Increase Bob Size to approximately 50% for broader colour washes.
7. Experiment with Hue Speed for static vs cycling trail colours.
8. Use Reset to clear accumulated trails and start fresh.

**Key concepts**: Video modulation masking, overlay blending, performance composition, framebuffer management.

---


## Tips

- **Hue Speed as colour animation**: Animate Hue Speed for trails that shift colour over time, independent of the spatial pattern. Slow cycling produces gradual palette shifts; fast cycling creates rainbow strobe effects.
- **Large Bob Size for plasma**: A very large blob with moderate speed and low decay creates a plasma-like glow that fills the screen with soft colour fields.
- **Reset for composition**: Use Reset liberally during performance to clear accumulated clutter and start fresh compositions on demand.
- **Ratio for trajectory complexity**: Low ratio values (near 1:1) produce simple circles. Higher ratios create figure-eights and complex interlocking curves that fill more of the framebuffer.

---
