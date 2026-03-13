---
draft: true
sidebar_position: 312
slug: /instruments/videomancer/tripatron
title: "Tripatron"
image: /img/instruments/videomancer/tripatron/tripatron_hero.png
description: "Tripatron is a three-layer generative light synthesiser that composites independent ring, burst, and spiral patterns into a unified organic visual."
---

import tripatron_hero from '/img/instruments/videomancer/tripatron/tripatron_hero.png';
import tripatron_animation from '/img/instruments/videomancer/tripatron/tripatron_animation.gif';
import tripatron_control_panel from '/img/instruments/videomancer/tripatron/tripatron_control_panel.png';
import tripatron_exercise1_result from '/img/instruments/videomancer/tripatron/tripatron_exercise1_result.gif';
import tripatron_exercise2_result from '/img/instruments/videomancer/tripatron/tripatron_exercise2_result.gif';
import tripatron_exercise3_result from '/img/instruments/videomancer/tripatron/tripatron_exercise3_result.gif';

# Tripatron

<span class="head2_nolink">Videomancer Program Guide</span>

:::warning
This document is still in progress, may contain errors, and is for preview only.
:::

<img src={tripatron_hero} alt="Tripatron hero image"/>
*Concentric rings, radial bursts, and spiralling arms overlap in three independent layers, creating an infinitely evolving organic light sculpture reminiscent of deep-sea bioluminescence.*
<img src={tripatron_animation} alt="Tripatron animated output"/>
*Tripatron output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Tripatron is a three-layer generative light synthesiser that composites independent ring, burst, and spiral patterns into a unified organic visual. Each layer operates as its own radial oscillator rendered onto the framebuffer, and the three layers are summed additively before palette lookup. The result is a complex, continuously evolving pattern that appears to breathe and pulse with an organic, almost biological quality.

The name is a portmanteau of "trip" and "-tron" (a common suffix in electronic art machinery), evoking the psychedelic visual experience the program produces. It also recalls Jeff Minter's Trip-a-Tron (1987), the third program in Llamasoft's light synthesiser lineage. Videomancer's Tripatron takes the multi-layer compositing concept further, with three geometrically distinct pattern generators that interact through additive blending.

Each layer can be individually enabled or disabled: Rings produces concentric circle patterns from the screen centre, Bursts creates radial line patterns emanating outward, and Spirals generates logarithmic spiral arms. The Ring Freq, Burst Freq, and Spiral Arms knobs control the spatial frequency of each respective layer. The Layer Speed knob drives all three simultaneously, and Hue Shift rotates the colour palette.

---

## Quick Start

1. **Start with one layer**: Isolate each layer to understand its individual character before combining. Rings → Bursts → Spirals builds complexity incrementally.
2. **Odd spiral counts**: 3 or 5 spiral arms create asymmetric visual interest. Even counts (2, 4, 6, 8) produce more symmetric patterns.
3. **Frequency ratio matters**: When Ring Freq and Burst Freq are near-integer ratios, stable moiré patterns emerge. Non-integer ratios create more organic, drifting interference.

---

## Background

### Multi-Layer Light Synthesis

The light synthesiser tradition established by Jeff Minter's Llamasoft series was built on a principle of layered simplicity: individually simple patterns, when composited together, produce emergent complexity. Tripatron follows this principle with three geometrically distinct layers — each is a simple radial function, but their additive interaction creates interference patterns that no single layer could produce alone. This approach parallels analogue video synthesis, where multiple simple oscillators are combined to create complex imagery.

### Concentric Ring Patterns

The Rings layer computes the radial distance from screen centre and applies a periodic function to create alternating bright and dark bands. The Ring Freq knob controls the band spacing. At low frequencies, a few wide bands dominate the screen. At high frequencies, tightly spaced rings create a target or bullseye pattern. The rings pulsate in and out as the animation advances, creating the effect of waves emanating from the centre.

### Radial Burst Patterns

The Bursts layer computes the angular position of each pixel relative to screen centre and applies a periodic function. This creates a starburst pattern of lines radiating outward, like sunbeams or spokes. The Burst Freq knob sets the number of rays. The pattern rotates as the animation advances, creating a spinning wheel of light.

### Logarithmic Spiral Arms

The Spirals layer combines radial distance and angular position to create logarithmic spirals emanating from the centre. The Spiral Arms knob quantises the number of spiral arms (1–8). The spirals rotate and expand as the animation advances, creating a galaxy-like pinwheel effect. The interaction of spirals with the ring and burst layers creates moiré-like interference patterns at their intersections.


---

## Signal Flow

```
 registers_in(0) ── Layer Speed ───────────────────────────────────────────┐
 registers_in(1) ── Ring Freq ─────────────────────────────────────────────┤
 registers_in(2) ── Burst Freq ────────────────────────────────────────────┤
 registers_in(3) ── Spiral Arms (8 steps) ─────────────────────────────────┤
 registers_in(4) ── Brightness ────────────────────────────────────────────┤
 registers_in(5) ── Hue Shift ─────────────────────────────────────────────┤
 registers_in(6) ── Toggles [Rings|Bursts|Spirals|ModVid|Bypass] ──────────┤
 registers_in(7) ── Mix Fader ─────────────────────────────────────────────┤
                                                                            │
 ┌─────────────────────────────────────────────────────────────────────────┘
 │
 │    ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
 ├───►│  COORDINATE GEN  │────►│  RINGS LAYER     │     │  BURSTS LAYER    │
 │    │  dx, dy from     │     │  radial distance │     │  angular theta   │
 │    │  screen centre   │     │  periodic bands  │     │  periodic rays   │
 │    │  compute r, θ    │     └───────┬──────────┘     └───────┬──────────┘
 │    └──────────────────┘             │                        │
 │                                     │ ring value             │ burst value
 │    ┌──────────────────┐             │                        │
 │    │  SPIRALS LAYER   │─────────────┼────────────────────────┤
 │    │  r + θ periodic  │             │                        │
 │    │  arm count       │             │                        │
 │    └───────┬──────────┘             │                        │
 │            │ spiral value           │                        │
 │    ┌───────┴────────────────────────┴────────────────────────┘
 │    │  ADDITIVE SUM
 │    │  ring + burst + spiral (per enabled layers)
 │    └───────┬──────────┐
 │            │          │
 │    ┌───────┴──────────┤
 │    │  PALETTE LOOKUP  │
 │    │  summed index    │
 │    │  + hue shift     │
 │    │  → YUV 10-bit   │
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

For each pixel, the pipeline computes the relative position (dx, dy) from screen centre and derives the radial distance r and angle θ. Each enabled layer evaluates its own function of these coordinates: Rings uses r with a periodic modulation, Bursts uses θ, and Spirals uses r + θ combined. The three layer outputs are summed additively, and the result indexes into the colour palette after applying the Hue Shift offset.

The Layer Speed knob drives a global animation counter that shifts the phase of all three periodic functions simultaneously. This creates the effect of rings expanding outward, bursts rotating, and spirals unwinding — all moving in coordinated rhythm. The Brightness knob scales the final output luminance.

---

## Parameter Reference

<img src={tripatron_control_panel} alt="Videomancer front panel with Tripatron loaded"/>
*Videomancer's front panel with Tripatron active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Layer Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 34% |
| Suffix | % |

Layer Speed controls the animation rate of all three pattern layers simultaneously. At zero all patterns are frozen. At moderate values the rings pulsate outward, the bursts rotate, and the spirals unwind in a coordinated rhythm. At maximum the patterns animate so rapidly that individual features blur into a shimmering field.

---

#### Knob 2 — Ring Freq
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 39% |
| Suffix | % |

Ring Freq sets the spatial frequency of the concentric ring pattern. At minimum a single broad band dominates. At maximum many tightly spaced rings create a fine bullseye. The ring spacing is the reciprocal of this value — higher frequency means narrower bands.

---

#### Knob 3 — Burst Freq
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 29% |
| Suffix | % |

Burst Freq sets the angular frequency of the radial burst pattern — effectively the number of rays emanating from the centre. Low values produce a few broad beams of light. High values create a densely spoked starburst. The rays rotate at the Layer Speed rate.

---

#### Knob 4 — Spiral Arms
| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 3 |

Spiral Arms selects the number of logarithmic spiral arms from 1 to 8. A single arm creates an asymmetric pinwheel. Two arms produce a classic galaxy spiral. At 8 arms the pattern approaches rotational symmetry, with very narrow gaps between arms. More arms increase the interaction density with the other layers.

---

#### Knob 5 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 78% |
| Suffix | % |

Brightness is a global luminance multiplier applied after palette lookup. At zero the output is black. At full value the palette colours reach their maximum intensity. This control uniformly scales all three layers' combined output.

---

#### Knob 6 — Hue Shift
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Hue Shift rotates the colour palette index applied to the combined layer sum. Sweeping this knob cycles the colour assignment of all pattern elements simultaneously. At moderate values the pattern shifts from warm to cool tones. A full sweep cycles through the entire spectral palette.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Rings** | Off | On |
| **8 — Bursts** | Off | On |
| **9 — Spirals** | Off | On |
| **10 — Mod Video** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles enable or disable each pattern layer and control video compositing. Rings, Bursts, and Spirals can be individually toggled to isolate or combine layers. Mod Video and Bypass control the video processing chain.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Mix crossfades between the dry input and the synthesised tripatron output. At minimum the output is entirely dry. At maximum the output is entirely wet. Intermediate values blend the organic patterns over the source material.





---

## Guided Exercises

These exercises build from a single-layer pattern to the full three-layer composite, demonstrating how additive layer interaction creates emergent complexity.

### Exercise 1: Isolated Ring Pulse

<img src={tripatron_exercise1_result} alt="Isolated Ring Pulse result"/>
*Isolated Ring Pulse — simulated result across source images.*
**What You'll Create**: Study the concentric ring pattern in isolation to understand radial frequency and animation.

1. Enable Rings only (disable Bursts and Spirals).
2. Set Ring Freq to approximately 30%.
3. Set Layer Speed to approximately 25%.
4. Set Brightness to approximately 80%.
5. Set Hue Shift to 0.
6. Set Mix to 100%.
7. Observe concentric rings expanding outward from the centre.
8. Increase Ring Freq and note how bands become narrower.
9. Adjust Layer Speed and observe how pulsation rate changes.

**Key concepts**: Radial distance periodic function, spatial frequency, animation phase.

---

### Exercise 2: Two-Layer Interference

<img src={tripatron_exercise2_result} alt="Two-Layer Interference result"/>
*Two-Layer Interference — simulated result across source images.*
**What You'll Create**: Combine rings and bursts to observe the moiré-like interference at their intersection.

1. Enable both Rings and Bursts (keep Spirals off).
2. Set Ring Freq to approximately 40%.
3. Set Burst Freq to approximately 50%.
4. Set Layer Speed to approximately 30%.
5. Set Brightness to full.
6. Set Mix to 100%.
7. Observe the interference pattern where rings and bursts overlap.
8. Slowly adjust Ring Freq — note how the interference moves as frequencies change.
9. Enable Spirals to see the full three-layer composite.

**Key concepts**: Additive layer compositing, moiré interference, spatial frequency interaction.

---

### Exercise 3: Full Composite with Video Overlay

<img src={tripatron_exercise3_result} alt="Full Composite with Video Overlay result"/>
*Full Composite with Video Overlay — simulated result across source images.*
**What You'll Create**: Create the full three-layer organic synthesis and blend it over live video.

1. Enable all three layers: Rings, Bursts, and Spirals.
2. Set Ring Freq to approximately 35%.
3. Set Burst Freq to approximately 45%.
4. Set Spiral Arms to 3.
5. Set Layer Speed to approximately 25%.
6. Set Hue Shift to approximately 40%.
7. Enable Mod Video.
8. Set Mix to approximately 65%.
9. Feed a video source with organic shapes (flowers, water, etc.).
10. Adjust Spiral Arms from 1 to 8 and observe how the composite changes.
11. Sweep Hue Shift to cycle through colour palettes.

**Key concepts**: Three-layer compositing, spiral arm count, hue rotation, video modulation masking.

---


## Tips

- **Low speed for ambient**: Very slow layer speeds create meditative, slowly breathing patterns suitable for installations — the eye perceives smooth evolution rather than motion.
- **All layers off = black**: Use the three layer toggles as performance instruments — toggling layers on and off creates dramatic compositional shifts.
- **Hue Shift for colour composition**: Automate Hue Shift to cycle through warm/cool palettes during performance. This changes the emotional quality without affecting the geometric pattern.
- **Video modulation with organic sources**: Mod Video works especially well with organic video sources like water, smoke, or foliage, enhancing the biological quality of the synthesis.

---
