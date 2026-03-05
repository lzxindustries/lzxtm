---
draft: true
sidebar_position: 28
slug: /instruments/videomancer/borderline
title: "Borderline"
image: /img/instruments/videomancer/borderline/borderline_hero.png
description: "Borderline generates animated colour stripes across the video frame, inspired by the ZX Spectrum demo technique of rapidly changing the BORDER colour register to draw patterns in the overscan area."
---

import borderline_hero from '/img/instruments/videomancer/borderline/borderline_hero.png';
import borderline_animation from '/img/instruments/videomancer/borderline/borderline_animation.gif';
import borderline_control_panel from '/img/instruments/videomancer/borderline/borderline_control_panel.png';
import borderline_exercise1_result from '/img/instruments/videomancer/borderline/borderline_exercise1_result.gif';
import borderline_exercise2_result from '/img/instruments/videomancer/borderline/borderline_exercise2_result.gif';
import borderline_exercise3_result from '/img/instruments/videomancer/borderline/borderline_exercise3_result.gif';

# Borderline

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={borderline_hero} alt="Borderline hero image"/>
*Scrolling colour stripes in ZX Spectrum palette tones frame the video in a lively border of cycling retro hues, just as demo coders once painted the overscan.*
<img src={borderline_animation} alt="Borderline animated output"/>
*Borderline output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Borderline generates animated colour stripes across the video frame, inspired by the ZX Spectrum demo technique of rapidly changing the BORDER colour register to draw patterns in the overscan area. On the original hardware, the ULA border colour could be reprogrammed mid-scanline, allowing skilled programmers to create elaborate patterns and artwork in the normally uniform border region. This program extends that concept to the full HD frame with configurable border zones, stripe widths, and palette cycling.

The name is a play on "border" and "line" — the fundamental elements of the effect. Four complete 8-colour palettes are available: the canonical ZX Spectrum palette, C64, Amstrad CPC, and a modern neon set. Stripes scroll through these palettes at controllable speeds, and a configurable border width parameter determines how far the coloured frame extends inward from the edges.

Within the border zone, stripes always appear. Inside the border (the "window" area), the input video can either pass through unmodified or receive an additive overlay of the stripe pattern. Mirror mode reflects the stripe pattern from the screen centre, creating symmetric designs.

---

## Quick Start

1. **Small border width with Replace** creates a subtle colour accent frame that enhances the video without overwhelming it.
2. **Maximum border width** turns the entire screen into scrolling stripes, useful as a standalone colour generator or backdrop.
3. **Two-speed animation** — use Stripe Speed for spatial scrolling and Colour Speed for palette rotation to create complex evolving patterns.

---

## Background

### Border Effects on the ZX Spectrum

The Spectrum's ULA generated a 256×192 pixel display surrounded by a wide border tinted by a single 3-bit colour register. During each frame, software could change this register on exact scanlines — or even within a scanline — to produce multicoloured borders. Classic demos like "Shock Megademo" and "1991" featured elaborate border artwork that turned the normally dead area into a canvas. The key constraint was per-scanline timing: each register write had to occur at precisely the right T-state.

### Cross-Platform Palette Archaeology

The four palettes represent distinct home computer colour identities. The ZX Spectrum's 8-colour palette (black, blue, red, magenta, green, cyan, yellow, white) was defined by 3-bit indexing with a brightness modifier. The C64's palette of 16 colours had a distinctive desaturated warmth. The Amstrad CPC offered 27 colours from an RGB space. Each palette brings a different emotional character to the scrolling stripes.

### Stripe Animation Principles

The stripe coordinate is computed by offsetting the scanline number by a frame-accumulated phase. Dividing by the stripe width (via bit shifts) and taking the low 3 bits creates repeating colour bands. Adding a separate colour cycle phase rotates which palette entries appear in which positions, producing the cascading rainbow effect visible in many demo loading screens and intros.

### Border as Performance Frame

In live video synthesis, the border zone acts as a performance frame — a colourful surround that contains and visually anchors the video content. The separate border and interior treatment allows the operator to create a "picture in picture" effect where processed borders and clean video coexist.


---

## Signal Flow

```
registers_in ──→ [Register Map] ──→ stripe speed, stripe width, colour speed,
                                    border width, symmetry, brightness
                                    toggles: palette, direction, mirror, overlay, bypass

                ┌─────────────────────────────────────────┐
                │           VBLANK ANIMATION              │
                │  stripe_phase += speed − 512            │
                │  colour_phase += colour_speed           │
                └─────────────────────────────────────────┘

data_in ──→ [Stage 1: Border Zone + Stripe Coord]
              border detect: h/v within border_width of edges?
              stripe coord = v_count or h_count (direction)
              mirror fold from center
              + stripe_phase animation
                        │
                        ▼
            [Stage 2: Stripe Index]
              coord >> shift (stripe width)
              + colour_phase → palette index (3 bits)
                        │
                        ▼
            [Stage 3: Palette Lookup]
              Spectrum / C64 / CPC / Neon palette[index]
                        │
                        ▼
            [Stage 4: Brightness + Zone Select]
              border zone → stripe colour × brightness
              interior → input video or additive overlay
                        │
                        ▼
            [Stage 5: Output / Overlay]
                        │
                        ▼
            [interpolator_u × 3]
              wet/dry crossfade
                        │
                        ▼
                   data_out
```

Border zone detection in stage 1 compares the pixel coordinates against the border width threshold from all four edges. The stripe coordinate is selected from either the vertical or horizontal counter depending on the Direction toggle, then optionally folded around the screen centre for the mirror effect. The animation phase accumulated each vblank is added to create the scrolling motion. In stage 2, the coordinate is divided by the stripe width via progressive bit shifts, and the colour cycle phase is added to rotate palette assignments. The zone selector in stage 4 is the key architectural decision: border pixels always show stripes, while interior pixels either pass the input through or receive an additive overlay.

---

## Parameter Reference

<img src={borderline_control_panel} alt="Videomancer front panel with Borderline loaded"/>
*Videomancer's front panel with Borderline active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Stripe Speed
| Property | Value |
|----------|-------|
| Range | -90deg – 90deg |
| Default | 12deg |
| Suffix | deg |

Stripe Speed controls the scrolling velocity of the stripe pattern. At centre (512) the stripes are stationary. Clockwise speeds scroll the stripes in one direction; counter-clockwise reverses the scroll. The bipolar implementation allows precise speed control from frozen to rapid cascading.

---

#### Knob 2 — Stripe Width
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Stripe Width controls the thickness of each colour band in four steps. At minimum the stripes are thin (divider 4), creating dense colour packing. At maximum the stripes are wide (divider 32), producing broad bands. Thin stripes create more colour variation per screen area; wide stripes produce a bolder, more graphic appearance.

---

#### Knob 3 — Colour Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Colour Speed controls how fast the palette colours cycle through the stripes. At zero the colour assignment is static. Increasing colour speed creates a rainbow chase effect where each stripe's colour shifts over time, independent of the spatial scrolling. Combined with Stripe Speed, two independent animation rates interact.

---

#### Knob 4 — Border Width
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Border Width sets how far the border zone extends inward from the screen edges. At zero the entire screen is "interior" and stripes only appear if overlay is enabled. At maximum the border extends ~240 pixels from each edge, leaving a small window for the interior. The border zone is defined identically on all four sides, creating a symmetric frame.

---

#### Knob 5 — Symmetry
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Symmetry adjusts the symmetry of the stripe pattern. This control interacts with the animation phase to produce asymmetric or symmetric visual weighting of the colour bands across the frame.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Brightness scales the luminance of the stripe colours from black to full intensity. At zero the stripes are invisible even in the border zone. At maximum, the brightest palette colours reach near-peak white. This control directly multiplies the palette Y value before compositing.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Palette** | Spectrum | Neon |
| **8 — Direction** | Horizontal | Vertical |
| **9 — Mirror** | Off | On |
| **10 — Overlay** | Replace | Add |
| **11 — Bypass** | Off | On |

The five toggles configure palette selection, stripe orientation, mirror symmetry, interior compositing, and bypass. Palette chooses between four retro colour sets. Direction switches stripes between horizontal and vertical. Mirror creates symmetric patterns. Overlay determines whether stripes appear only in the border or also additively in the interior.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Mix crossfades between the dry (unprocessed) input and the wet (border-striped) output. At 0% the output matches the input. At 100% the full border effect is visible.



> See [Common Controls & Glossary Reference](../common_reference.md) for details.

---

## Guided Exercises

These exercises demonstrate border stripe effects from classic framing to full-screen colour overlay.

### Exercise 1: Classic Border Frame

<img src={borderline_exercise1_result} alt="Classic Border Frame result"/>
*Classic Border Frame — simulated result across source images.*
**What You'll Create**: Create a colourful Spectrum-palette border frame around the video.

1. Set Palette to Spectrum, Direction to Horizontal.
2. Border Width to 60% for a visible border frame.
3. Stripe Speed to a gentle scroll (~570).
4. Stripe Width to step 2, Colour Speed to 30%.
5. Brightness to 80%, Mirror off, Overlay to Replace.
6. The video should appear framed by scrolling multicoloured stripes.
7. Try C64 palette for a warmer feel.

**Key concepts**: - Border width defines the frame thickness
- Replace overlay keeps the interior video clean
- Palette selection dramatically changes the colour vocabulary

---

### Exercise 2: Neon Candy Overlay

<img src={borderline_exercise2_result} alt="Neon Candy Overlay result"/>
*Neon Candy Overlay — simulated result across source images.*
**What You'll Create**: Layer scrolling neon stripes across the entire frame.

1. Set Palette to Neon, Direction to Vertical.
2. Border Width to maximum so the entire frame is the border zone.
3. Stripe Speed to 600, Colour Speed to 50%.
4. Stripe Width to step 3 for medium bands.
5. Brightness to 50% so stripes are translucent.
6. Enable Overlay=Add for full-frame blending.
7. The source should appear behind scrolling neon candy stripes.

**Key concepts**: - Maximum border width makes the entire frame a border zone
- Low brightness creates translucent stripes that reveal the source
- Neon palette provides vivid contemporary colours

---

### Exercise 3: Symmetric Mirror Frame

<img src={borderline_exercise3_result} alt="Symmetric Mirror Frame result"/>
*Symmetric Mirror Frame — simulated result across source images.*
**What You'll Create**: Create a symmetric, kaleidoscopic border frame using mirror mode.

1. Set Palette to CPC, Direction to Horizontal.
2. Enable Mirror for symmetric stripes.
3. Border Width to 50%, Stripe Speed to 560.
4. Stripe Width to step 1 (thin stripes) for dense pattern.
5. Colour Speed to 70%, Brightness to 85%.
6. Observe how the stripes reflect from the screen centre.
7. Switch to vertical direction to see vertical mirroring.

**Key concepts**: - Mirror mode creates symmetric designs from the centre outward
- Thin stripes produce the densest colour patterns
- Direction change rotates the symmetry axis

---


## Tips

- **C64 palette at low brightness** produces a warm, nostalgic colour wash that complements vintage footage.
- **Neon palette with Add overlay** on dark video creates a vivid light-show effect perfect for music visualisation.
- **Mirror + thin stripes** creates dense symmetric patterns reminiscent of tapestry or weaving designs.

---
