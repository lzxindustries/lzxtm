---
draft: true
sidebar_position: 28
slug: /instruments/videomancer/borealis
title: "Borealis"
image: /img/instruments/videomancer/borealis/borealis_hero.png
description: "In 1860, the explorer Isaac Israel Hayes sailed north of Greenland into the Kane Basin and sketched the arctic aurora from the deck of his schooner."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import borealis_hero from '/img/instruments/videomancer/borealis/borealis_hero.png';
import borealis_control_panel from '/img/instruments/videomancer/borealis/borealis_control_panel.png';
import borealis_exercise1_result from '/img/instruments/videomancer/borealis/borealis_exercise1_result.png';
import borealis_exercise2_result from '/img/instruments/videomancer/borealis/borealis_exercise2_result.png';
import borealis_exercise3_result from '/img/instruments/videomancer/borealis/borealis_exercise3_result.png';
import borealis_source1_kodim01 from '/img/instruments/videomancer/borealis/borealis_source1_kodim01.png';
import borealis_source2_kodim02 from '/img/instruments/videomancer/borealis/borealis_source2_kodim02.png';
import borealis_source3_stream_bridge_512 from '/img/instruments/videomancer/borealis/borealis_source3_stream_bridge_512.png';

# Borealis

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Kodim01", before: borealis_source1_kodim01, after: borealis_hero },
    { label: "Kodim02", before: borealis_source2_kodim02, after: borealis_hero },
    { label: "Stream Bridge", before: borealis_source3_stream_bridge_512, after: borealis_hero },
  ]}
/>
*Borealis generating procedural aurora curtains with dual oxygen emission colors composited additively over a mountain landscape.*

---

## Overview

In 1860, the explorer Isaac Israel Hayes sailed north of Greenland into the Kane Basin and sketched the arctic aurora from the deck of his schooner. Five years later, Frederic Edwin Church — the foremost painter of the Hudson River School — transformed those field sketches into the largest and most scientifically accurate aurora painting in Western art. *Aurora Borealis* (1865, Smithsonian American Art Museum) depicts what Church understood as the aurora's fundamental visual property: it appears as vertical curtains of colored light, brightest at their lower edges, their hems scalloped and rippling like fabric draped from the magnetic field lines above.

Borealis recreates this phenomenon in hardware. It generates 1 to 8 procedural vertical curtain bands that drift horizontally via independent DDS oscillators, each with a bottom-heavy vertical brightness profile, scalloped lower edges via sine function modulation, and dual-color emission mapping — green at the base (corresponding to the 557.7 nm oxygen line) transitioning to magenta at the top (the 630.0 nm oxygen line). The curtains are composited additively over the input video, matching the physics of emission phenomena where light is added to the scene rather than reflected.

The program operates with zero BRAM tiles — all computation is per-pixel procedural. Curtain intensity is the product of horizontal proximity (linear falloff from center), vertical brightness ramp (inverted — brightest at bottom), and scallop mask (sine function at the lower edge). The sum of all curtain contributions is then mapped to emission colors and composited over the source. Optional substorm pulsation via LFSR-based brightness modulation creates the rapid brightening and dimming characteristic of geomagnetic disturbances.

---

## Background

### Auroral Curtain Physics

The aurora borealis occurs when charged particles from the solar wind spiral along Earth's magnetic field lines and collide with atmospheric gases. The collisions excite oxygen and nitrogen atoms, which emit light at specific wavelengths as they return to their ground states. The dominant green emission at 557.7 nm comes from oxygen atoms at approximately 100 km altitude, where atmospheric density is highest. The red/magenta emission at 630.0 nm comes from oxygen at higher altitudes (200-300 km) where lower density allows the longer-lived excited state to radiate before collisional de-excitation. The result is a vertical color gradient: green at the base, transitioning to red/magenta above — exactly the palette Church captured and exactly what Borealis generates.

### Curtain Geometry and DDS Oscillators

Real auroral curtains are elongated structures aligned with magnetic field lines, typically oriented roughly north-south. They drift east-west under the influence of convection patterns in the magnetosphere. Borealis models each curtain as a vertical band at a specific horizontal position that drifts via a Direct Digital Synthesis (DDS) oscillator — a phase accumulator whose rate is proportional to the Drift Speed parameter multiplied by a per-curtain prime-like rate constant. Using different rate multipliers (3, 5, 7, 4, 6, 9, 2, 8) for each curtain ensures they move independently, creating the layered, depth-ambiguous visual field of a real aurora where curtains sometimes overlap and reinforce, sometimes separate.

### Bottom-Heavy Brightness

Unlike most radial or gradient effects, aurora curtains are brightest at their *lower* edge and fade upward. This inverted brightness profile reflects the physics: the densest atmospheric layer produces the most collisional excitation and therefore the brightest emission. Borealis implements this as a linear ramp from the curtain's scalloped lower edge (maximum brightness) upward to its top boundary (zero brightness). The characteristic look — luminous lower hems with ghostly transparent upper reaches — is what gives the aurora its fabric-like, curtain quality.

### Scalloped Lower Edges

The lower edge of an auroral curtain is not smooth. It undulates in a wave pattern caused by instabilities in the boundary between the precipitating particle streams and the surrounding atmosphere. Church depicted these as ragged, rippling hems. Borealis models them with a sine function applied per-column to modulate the curtain's base position, creating a rhythmic scalloped edge whose frequency is controlled by the Scallop parameter. Each curtain has an independent scallop phase offset, preventing the scallops from aligning uniformly.

### Substorm Dynamics

Auroral substorms are periods of rapid intensification caused by sudden releases of energy stored in the magnetotail. During a substorm, aurora brightness can increase dramatically within minutes, with pulsating patterns and breakup arcs. Borealis simulates substorm dynamics with an LFSR-based brightness modulation that creates rapid, semi-random pulsation when enabled — the aurora's intensity fluctuates between half and full brightness each frame, producing the nervous, agitated quality characteristic of disturbed geomagnetic conditions.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Frame Update (per vsync) ───────────────────────────────────
│   │
│   ├─ 1. DDS Phase Advance       (8 curtain oscillators × rate multiplier)
│   ├─ 2. Curtain X Positions     (sine(phase) → horizontal position)
│   ├─ 3. LFSR Substorm           (brightness modulation if enabled)
│   └─ 4. Color Cycle Phase       (optional emission color cycling)
│
├── Pipeline Stage 0-1: Horizontal Distance ────────────────────
│   │
│   └─ 5. Per-Curtain Distance    (|h_count - curtain_x| for all 8)
│
├── Pipeline Stage 2: Vertical Ramp + Scallop ──────────────────
│   │
│   ├─ 6. Ceiling Mode Flip       (optional vertical inversion)
│   ├─ 7. Scallop Lower Edge      (sine of h_count × freq → base offset)
│   └─ 8. Vertical Brightness     (linear ramp: base=max, top=0)
│
├── Pipeline Stage 3: Sum Contributions ────────────────────────
│   │
│   ├─ 9. h_falloff × v_ramp      (per-curtain intensity product)
│   └─ 10. Sum Active Curtains    (saturating add × brightness × substorm)
│
├── Pipeline Stage 4: Emission Color ───────────────────────────
│   │
│   ├─ 11. v_position → green/red (lower=green base, upper=magenta top)
│   └─ 12. YUV Emission Map       (intensity × color → aurora Y, U, V)
│
├── Pipeline Stage 5: Additive Composite ───────────────────────
│   │
│   ├─ 13. Y += aurora_y           (saturating add for luma)
│   └─ 14. UV blend                (blend toward aurora UV where bright)
│
├── Mix ────────────────────────────────────────────────────────
│   └─ 15. Interpolator × 3        (dry/wet crossfade Y, U, V)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

Two critical design decisions define the aurora's appearance. First, the luma compositing is **additive**: aurora brightness is saturating-added to the input Y channel, reflecting the physical behavior of emission phenomena (the aurora is a light source, not a filter). Second, the chroma compositing is **intensity-weighted blending**: the U and V channels blend from the input's chrominance toward the aurora's emission color in proportion to the aurora's local intensity. This means the aurora colors dominate where the curtains are bright, but the input video's colors persist where the aurora contribution is weak — matching how real aurora interacts with the illuminated landscape below it.

---

## Parameter Reference

<img src={borealis_control_panel} alt="Videomancer front panel with Borealis loaded"/>
*Videomancer's front panel with Borealis active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Drift Spd
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 29.3% |
| Suffix | % |

Controls the drift speed of all curtain horizontal positions. At 0%, curtains are nearly stationary. At higher values, curtains sweep visibly across the frame. Each curtain uses a different rate multiplier (prime-like values from 2 to 9), so increasing drift speed amplifies the relative motion differences between curtains. The curtain positions are derived from sine functions of the DDS phases, producing smooth oscillatory drift rather than linear translation.

---

#### Knob 2 — Curtains
| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 4 |

Selects how many curtains are active, from 1 to 8 in discrete steps. A single curtain produces a focused, monumental aurora display. Two to four curtains create a classic multi-band aurora. Six to eight curtains fill the sky with overlapping bands that merge and separate dynamically. The curtains are spread across the frame at evenly distributed initial positions (80, 240, 400, 560, 720, 880, 1040, 1200 pixels), so adding more curtains progressively fills the horizontal space.

---

#### Knob 3 — Width
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the horizontal width of each curtain band. At narrow settings, curtains appear as thin vertical streaks. At wide settings, each curtain spans a significant portion of the frame and adjacent curtains overlap extensively. The width parameter defines a linear falloff zone: within the inner half-width, brightness is maximum; between half-width and full-width, brightness falls linearly to zero. This creates soft-edged bands rather than hard-cut columns.

---

#### Knob 4 — Scallop
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 39.1% |
| Suffix | % |

Controls the frequency of the scalloped lower edge undulation. At low values, the scallop is a gentle, long-wavelength ripple producing smoothly flowing hemlines. At high values, the scallop becomes a rapid oscillation creating a finely serrated lower edge. Each curtain has an independent scallop phase offset, so even at high frequency the scallops do not synchronize across curtains — each curtain ripples independently. The scallop amplitude is fixed at approximately 60 pixels, so the frequency parameter controls fineness rather than depth of the undulation.

---

#### Knob 5 — Grn/Red
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 68.4% |
| Suffix | % |

Controls the balance between green and red/magenta emission colors. At values biased toward green, the aurora appears in the classic green oxygen emission palette — warm, vivid green dominating the lower curtain regions. At values biased toward red, the magenta upper emission becomes prominent, pushing the overall palette toward purple-red tones. This control interacts with the vertical position: the lower half of the aurora always has a stronger green component, and the upper half always has a stronger red component, but this knob shifts the overall balance between the two.

---

#### Knob 6 — Bright
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 58.7% |
| Suffix | % |

Controls the overall brightness (intensity) of the aurora composite. This parameter scales the summed curtain contributions before compositing. At low values, the aurora is a faint atmospheric glow barely visible over the source. At high values, the aurora's additive brightness can wash out the underlying video, creating an intensely illuminated scene. Brightness also interacts with the substorm modulation — during substorm pulses, the effective brightness fluctuates between half and full of this setting.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Ceiling** | Upper | Lower |
| **8 — ClrCycle** | Static | Cycle |
| **9 — Substorm** | Off | On |
| **10 — Full Sky** | Normal | Full |
| **11 — Bypass** | Off | On |

The five toggles shape the aurora's atmospheric behavior and spatial arrangement. Ceiling selects whether the aurora appears in the upper or lower portion of the frame. ClrCycle enables slow cycling of the emission color balance. Substorm activates rapid LFSR-based brightness pulsation. Full Sky expands the aurora to cover the entire frame height rather than the upper quarter. Bypass passes the signal through unprocessed.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the dry/wet mix between the original input video and the aurora-composited output. At 0% (fully dry), the output is the unprocessed input. At 100% (fully wet), the output is the full aurora composite. Intermediate values crossfade between the two, allowing the aurora to be subtly blended over the source content.

---

## Guided Exercises

These exercises progress from a simple single-curtain aurora to a full-sky substorm display, exploring curtain width, emission colors, scallop dynamics, and substorm pulsation effects.

### Exercise 1: Single Curtain Aurora

<BeforeAfterSlider
  sources={[
    { label: "Kodim01", before: borealis_source1_kodim01, after: borealis_exercise1_result },
    { label: "Kodim02", before: borealis_source2_kodim02, after: borealis_exercise1_result },
    { label: "Stream Bridge", before: borealis_source3_stream_bridge_512, after: borealis_exercise1_result },
  ]}
/>
*Single Curtain Aurora — simulated result across source images.*
**Source**: Feed a landscape with a visible sky region (Kodak #13 — the mountain/water scene has a natural horizon that contextualizes the aurora above).

**Objective**: Create a classic single aurora curtain with green/magenta emission and visible scalloped lower edge.

1. Set Drift Speed to 20% for gentle horizontal drift.
2. Set Curtains to 1 (step 1) for a single focused band.
3. Set Width to 60% for a moderately wide curtain.
4. Set Scallop to 40% for visible but gentle lower edge undulation.
5. Set Green/Red to 70% for green-dominant emission with some visible magenta.
6. Set Brightness to 60% for a naturally visible aurora.
7. Set Ceiling to Upper — aurora appears in the upper portion of the frame.
8. Set ClrCycle to Static for fixed color.
9. Set Substorm to Off for steady brightness.
10. Set Full Sky to Normal for upper-frame aurora.
11. Set Mix to 100%.
12. Observe the single curtain drifting gently with its scalloped lower hem glowing green, fading to magenta at the top.

**Key concepts**: A single curtain clearly shows the three defining properties of the aurora simulation: horizontal falloff (the curtain has soft edges), bottom-heavy vertical brightness (brightest at the scalloped lower edge), and dual-color emission (green base, magenta top). The scallop is visible as a rippling lower hem that varies the base position per-column.

---

### Exercise 2: Multi-Band Northern Lights

<BeforeAfterSlider
  sources={[
    { label: "Kodim01", before: borealis_source1_kodim01, after: borealis_exercise2_result },
    { label: "Kodim02", before: borealis_source2_kodim02, after: borealis_exercise2_result },
    { label: "Stream Bridge", before: borealis_source3_stream_bridge_512, after: borealis_exercise2_result },
  ]}
/>
*Multi-Band Northern Lights — simulated result across source images.*
**Source**: Feed a scene with a prominent vertical element (Kodak #21 — the lighthouse provides a vertical anchor against which the horizontal curtain drift is clearly visible).

**Objective**: Create a classic multi-band aurora display with 5 curtains, color cycling, and moderate scallop frequency.

1. Set Drift Speed to 40% for visible curtain motion.
2. Set Curtains to 5 (step 5) for a multi-band display.
3. Set Width to 45% for moderately wide bands that partially overlap.
4. Set Scallop to 60% for more pronounced lower edge serration.
5. Set Green/Red to 50% for balanced green/magenta emission.
6. Set Brightness to 70% for prominent aurora.
7. Set Ceiling to Upper.
8. Enable ClrCycle — watch the emission colors slowly shift.
9. Set Substorm to Off for steady, contemplative aurora.
10. Set Full Sky to Normal.
11. Set Mix to 100%.
12. Observe multiple curtains drifting at different speeds, their scalloped hems independently rippling, with slowly cycling green-to-magenta color balance.

**Key concepts**: With 5 curtains, the independent DDS rate multipliers become apparent — curtains drift and separate at different speeds (rates 3, 5, 7, 4, 6), creating a layered, depth-ambiguous visual field. Color cycling adds temporal variation to the emission palette, and the per-curtain scallop phase offsets prevent the lower edges from synchronizing.

---

### Exercise 3: Full-Sky Substorm

<BeforeAfterSlider
  sources={[
    { label: "Kodim01", before: borealis_source1_kodim01, after: borealis_exercise3_result },
    { label: "Kodim02", before: borealis_source2_kodim02, after: borealis_exercise3_result },
    { label: "Stream Bridge", before: borealis_source3_stream_bridge_512, after: borealis_exercise3_result },
  ]}
/>
*Full-Sky Substorm — simulated result across source images.*
**Source**: Feed a vibrant, colorful image (Kodak #16 — the warm tropical tones create a dramatic contrast with the cool green/magenta aurora filling the sky).

**Objective**: Create an intense, full-sky aurora substorm with maximum curtains, brightness pulsation, and dramatic color contrast.

1. Set Drift Speed to 65% for fast curtain motion.
2. Set Curtains to 8 (step 8) for maximum curtain density.
3. Set Width to 55% for overlapping bands filling the frame.
4. Set Scallop to 75% for rapid, sharply serrated edges.
5. Set Green/Red to 30% for stronger magenta/red emission.
6. Set Brightness to 85% for intense, near-saturating aurora.
7. Set Ceiling to Upper.
8. Enable ClrCycle for shifting color.
9. Enable Substorm — observe rapid brightness pulsation.
10. Enable Full Sky — curtains now extend to fill the entire frame.
11. Set Mix to 100%.
12. Watch the full-sky substorm: 8 curtains pulsating and drifting rapidly over the tropical source, green and magenta light washing across the entire frame.

**Key concepts**: Full Sky mode extends the aurora's vertical range to nearly the entire frame height, creating an immersive display. Substorm pulsation adds LFSR-driven brightness fluctuation that creates a nervous, agitated quality. With 8 curtains at 55% width, significant overlap produces areas of reinforced brightness where curtains merge — these hot spots shift as curtains drift, creating a dynamic, living light display.

---


## Tips

- **Start with one curtain**: A single curtain clearly shows the bottom-heavy brightness, scallop edge, and dual emission colors. Add more curtains once you understand the individual curtain's visual properties.
- **Dark sources favor aurora**: The additive composite means aurora colors read most clearly over dark source regions. A night sky or dark landscape will show the green/magenta emission vividly.
- **Scallop frequency for mood**: Low scallop (20-30%) creates gentle, flowing curtain hems; high scallop (70%+) creates energetic, sharply serrated edges. Match scallop frequency to the emotional energy of the composition.
- **Substorm for drama**: Reserve substorm pulsation for high-energy moments. The rapid brightness fluctuation is visually intense and works best at high brightness settings where the contrast is dramatic.
- **Full Sky for immersion**: In Normal mode, the aurora is a distant atmospheric phenomenon. In Full Sky mode, it fills the scene, creating the feeling of standing directly beneath the curtains.
- **Color balance tells time**: In real aurora viewing, green-dominant displays are common; magenta-dominant displays indicate higher-altitude activity typically seen during intense storms. Set Green/Red accordingly to suggest different conditions.
- **Width affects overlap**: With many curtains and wide width settings, curtains overlap extensively, creating smooth brightness contours. With narrow width, individual curtain bands are distinct and separate.
- **Mix for ambient glow**: At 20-40% mix, the aurora becomes a subtle ambient glow — useful for adding atmospheric color to source material without dominating the composition.

---

## Glossary

| Term | Definition |
|------|------------|
| **Additive composite** | A blending mode where pixel brightness values are summed rather than replaced, simulating light emission where new light adds to existing illumination. |
| **Chrominance** | The color-difference components (U and V) of a YUV signal, encoding hue and saturation independently of brightness. |
| **DDS (Direct Digital Synthesis)** | A technique for generating waveforms using a phase accumulator that increments at a programmable rate, used here to drive curtain drift oscillators. |
| **Emission spectrum** | The set of specific wavelengths of light radiated by excited atoms or molecules; auroral green (557.7 nm) and red (630.0 nm) are both oxygen emission lines. |
| **LFSR (Linear Feedback Shift Register)** | A shift register producing a deterministic pseudo-random bit sequence, used here for substorm brightness pulsation. |
| **Luma** | The luminance (Y) component of a YUV video signal, representing perceived brightness. |
| **Magnetotail** | The elongated region of Earth's magnetosphere on the side opposite the Sun, where energy accumulates before being released in auroral substorms. |
| **Phase accumulator** | A digital counter that advances by a fixed increment each clock cycle, wrapping at overflow to produce a repeating ramp; the core element of a DDS oscillator. |
| **Saturating add** | An addition operation that clamps the result at the maximum representable value instead of wrapping around on overflow. |
| **Scallop** | A repeating wave-shaped undulation modulating the lower edge of each aurora curtain, simulating plasma instabilities at the precipitation boundary. |
| **Substorm** | A sudden intensification of auroral activity caused by rapid energy release from the magnetotail, characterised by pulsating brightness and arc breakup. |
| **YUV** | A color encoding scheme that separates luminance (Y) from chrominance (U, V), widely used in video signal processing. |

---
