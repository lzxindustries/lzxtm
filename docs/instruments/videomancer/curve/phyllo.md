---
draft: true
sidebar_position: 200
slug: /instruments/videomancer/phyllo
title: "Phyllo"
image: /img/instruments/videomancer/phyllo/phyllo_hero.png
description: "Program guide for Phyllo, a Videomancer curve program for the LZX video synthesizer."
---

import phyllo_animation from '/img/instruments/videomancer/phyllo/phyllo_animation.gif';
import phyllo_control_panel from '/img/instruments/videomancer/phyllo/phyllo_control_panel.png';
import phyllo_exercise1_result from '/img/instruments/videomancer/phyllo/phyllo_exercise1_result.gif';
import phyllo_exercise2_result from '/img/instruments/videomancer/phyllo/phyllo_exercise2_result.gif';
import phyllo_exercise3_result from '/img/instruments/videomancer/phyllo/phyllo_exercise3_result.gif';
import phyllo_hero from '/img/instruments/videomancer/phyllo/phyllo_hero.png';

# Phyllo

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={phyllo_hero} alt="Phyllo hero image"/>
*Phyllo generating a golden-angle phyllotactic spiral pattern with color-cycling dots overlaid on a live video source.*
<img src={phyllo_animation} alt="Phyllo animated output"/>
*Phyllo output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Nature encodes efficient packing solutions in the arrangement of sunflower seeds, pinecone scales, and cactus spines. These structures all share a mathematical secret: each successive element is placed at the golden angle — approximately 137.508° — relative to the previous one. The result is a spiral that fills space without overlap and without gaps. Phyllo brings this arrangement to the screen, computing a phyllotactic spiral pattern in real-time FPGA hardware.

The program works by converting each pixel's screen coordinates to polar form relative to a configurable center, then testing whether the pixel lies on a spiral arm. The arm test compares the pixel's angular position against a function of its radial distance, scaled by the golden angle. Pixels that pass the test are brightened and optionally tinted using an 8-entry hue lookup table. Pixels that fail pass through unchanged, allowing the underlying video source to show between the spiral arms.

At conservative settings, Phyllo produces a sparse arrangement of dots radiating from the center — a digital sunflower head. As you increase the arm count and dot size, the pattern thickens into continuous spirals that wrap the screen. The animation toggle adds a frame-by-frame phase rotation that causes the entire pattern to slowly turn, creating hypnotic organic motion. The video-reactive toggle suppresses dots in dark regions of the source, making the spiral pattern follow the brightness contours of the input image.

---

## Background

### Phyllotaxis and the Golden Angle

Phyllotaxis — from the Greek *phyllon* (leaf) and *taxis* (arrangement) — describes how lateral organs are arranged around a plant stem. In 1837, the Bravais brothers demonstrated that the most common arrangement places each successive primordium at an angular displacement equal to 360° / φ² ≈ 137.508°, where φ is the golden ratio (1 + √5)/2. This angle is called the **golden angle**. It is the most irrational number in a precise sense: its continued fraction representation is [1; 1, 1, 1, ...], making it the slowest to converge of all continued fractions. This extreme irrationality is exactly what makes it optimal for packing — because no rational approximation is close, no two seeds ever align into radial rows, and the entire disc fills uniformly.

### Polar Coordinate Transformation

To generate the phyllotactic pattern without storing individual seed positions, Phyllo converts each pixel from Cartesian coordinates (h_count, v_count) to polar form (radius, angle). The radius uses Manhattan distance (|Δx| + |Δy|) rather than true Euclidean distance — this is cheaper on the iCE40 and produces a diamond-shaped radial field. The angle is approximated using an octant-based method: sign bits and magnitude comparison identify the octant, then a linear interpolation within the octant yields an 8-bit angle value covering the full 360° circle. This angular approximation avoids the need for a CORDIC or lookup table.

### Arm Test and the Modular Condition

The core of the pattern generator is a modular arithmetic test. For each pixel, the VHDL computes `arm_test = angle - (radius >> scale_shift)`. If the low bits of this value (masked by the arm count) fall below a width threshold, the pixel is "on arm." This is equivalent to testing whether the pixel's angular position, unwound by its radial distance at the golden angle rate, falls within a narrow band. The arm count mask controls how many distinct spiral arms are visible — from a single arm to eight interleaved arms. The scale shift controls how tightly the spiral winds.

### Dot vs. Spiral Rendering

Phyllo offers two rendering modes controlled by the Mode toggle. In **dot mode**, both an angular arm test *and* a radial threshold must pass — producing discrete dots at the intersections of spiral arms and concentric rings, mimicking individual sunflower seeds. In **spiral mode**, only the angular test is applied — producing continuous curved arcs that sweep outward from the center. Dot mode is closer to biological phyllotaxis; spiral mode is more decorative.

### 8-Entry Hue Lookup Table

When color mode is active, each dot or arm segment is tinted using an 8-entry table of pre-computed UV offset pairs. The hue index combines the Tint Hue pot's upper bits with the lower bits of the arm test value, creating a position-dependent color that cycles through the palette as you move along a spiral arm. The eight hue entries trace a full circle in UV space, giving red, orange, yellow-green, green, cyan, blue, magenta, and rose.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Timing Generator
│   └── h_count, v_count from video sync
│
├── Animation Phase (per vsync)
│   └── anim_phase += 1 when Animate enabled
│
├── Stage 1: Delta from Center
│   ├── dx = h_count - 960
│   └── dy = v_count - 540
│
├── Stage 2: Polar Conversion
│   ├── radius = |dx| + |dy|  (Manhattan)
│   ├── angle_approx (8-bit octant-based)
│   └── angle += anim_phase + rotation_offset
│
├── Stage 3: Spiral Arm Test
│   ├── arm_test = angle - (radius >> scale_shift)
│   ├── Dot mode: (arm_test AND arm_mask) < width_thresh
│   │             AND (radius AND 0x1F) < width_thresh
│   ├── Spiral mode: (arm_test AND arm_mask) < width_thresh
│   └── Video-reactive: suppress if source Y < 256
│
├── Stage 4: Composite
│   ├── On arm: Y += 512 >> bright_shift (saturating)
│   │   ├── Color mode: UV from HUE_LUT[tint_hue + arm_test]
│   │   └── Mono mode: U = V = 512
│   └── Off arm: pass through source YUV
│
├── Interpolator Mix (4 clocks)
│   └── lerp(source, composite, mix_amount)
│
├── Bypass Mux
│   └── Bypass toggle → pass input unchanged
│
└── Output (YUV 4:4:4)
```

The critical interaction is between the polar conversion and the arm test. The angle approximation and the radius use Manhattan geometry — which gives a diamond-shaped falloff rather than circular — so spiral arms appear slightly angular rather than perfectly curved. This is a deliberate trade-off for iCE40 timing closure without CORDIC hardware. The video-reactive path is a simple luma threshold (Y < 256 suppresses dots), not a proportional modulation — dots are either fully on or fully suppressed based on source brightness.

---

## Parameter Reference

<img src={phyllo_control_panel} alt="Videomancer front panel with Phyllo loaded"/>
*Videomancer's front panel with Phyllo active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Scale
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls spiral arm spacing via a shift-based scale selector. At the lowest settings (register < 128), the spiral is very tightly wound with arms close together — dense concentric wrapping. As you increase the control, the spacing grows geometrically because each step doubles the shift value: 128→384 is shift 3 (medium), 384→640 is shift 4 (wide), 640→896 is shift 5 (very sparse). This logarithmic response means the useful range of spiral tightness is spread across the full knob travel.

---

#### Knob 2 — Petal Size
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the width of each spiral arm or dot. The register's upper 5 bits directly set the width threshold used in the arm test. At minimum, the arms are razor-thin single-pixel lines. As you increase the value, the arms widen until at maximum they fill nearly the entire angular band. In dot mode, this control also sets the radial thickness of each dot — large values produce fat filled circles while small values produce thin rings.

---

#### Knob 3 — Rotation
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the arm count multiplier. The upper 3 bits of the register produce a mask from 0 to 7, which determines how many distinct spiral arms are visible. At 0, the mask passes everything — a single dominant arm. At 7, the mask creates eight interleaved arms that uniformly fill the angular space. Intermediate values produce 2, 3, 4, 5, 6, or 7 arms. More arms create a denser, more intricate pattern with finer angular subdivision.

---

#### Knob 4 — Anim Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Applies an angular offset to the entire spiral pattern. The upper 8 bits of the register are added to the computed angle, effectively rotating the pattern around the center point. Sweeping this control smoothly rotates all spiral arms in real time. Combined with the Animate toggle, the static rotation offset adds to the per-frame animation phase, allowing you to set a starting orientation for the animated rotation.

---

#### Knob 5 — Center X
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Selects the overlay hue when Color mode is active. The upper 3 bits index into the 8-entry hue lookup table, combined with the arm test's low bits to produce position-varying color. Sweeping this control rotates the entire color palette — the rainbow shifts along the spiral arms. At the boundary between two LUT entries, the color transitions abruptly (no interpolation between hue table entries).

---

#### Knob 6 — Center Y
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls dot brightness — how much the Y channel is boosted for pixels on a spiral arm. The implementation uses a shift-based attenuator: at low register values, the brightness addition is heavily shifted down (subtle glow), while at high values the shift is minimal (maximum brightness boost of 512 + source Y, saturating at 1023). The response is logarithmic — most of the visible brightness change happens in the upper quarter of knob travel.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Pattern** | Sunflwr | Pinecon |
| **8 — Fill** | Video | Tint |
| **9 — Animate** | Off | On |
| **10 — Invert** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control independent binary options. Mode selects between dot rendering (discrete seed-like points) and continuous spiral arcs. Color/Mono determines whether dots are tinted from the hue table or rendered as pure white (neutral UV). Animate adds a slowly incrementing phase rotation per field. Video Reactive suppresses dots where the source video is dark (Y < 256). Bypass routes the input signal directly to the output.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade via the interpolator. At 0 the output is 100% dry (source only). At 1023 the output is 100% wet (fully processed spiral overlay). Intermediate values produce a transparent blend where the spiral pattern is partially visible over the source. The interpolator uses 10-bit fractional multiplication, providing 1024 blend steps.

---

## Guided Exercises

These exercises explore the phyllotactic spiral from simple dot patterns to animated video-reactive overlays. Each builds on the previous, gradually engaging more processing features.

### Exercise 1: Sunflower Seed Pattern

<img src={phyllo_exercise1_result} alt="Sunflower Seed Pattern result"/>
*Sunflower Seed Pattern — simulated result across source images.*
**Objective**: Learn how the arm count and dot size controls shape the basic phyllotactic arrangement.

1. **Single arm**: Set Arm Count to minimum. Observe a single spiral arm sweeping outward from the center.
2. **Add arms**: Slowly increase Arm Count. Watch as 2, 3, 4, then 8 arms appear, each interleaved at the golden angle.
3. **Thicken dots**: Increase Dot Size from minimum. In dot mode, thin points expand into filled circles.
4. **Dense packing**: With Arm Count at maximum and Dot Size moderate, the screen fills with a uniform phyllotactic grid — a digital sunflower head.
5. **Spiral mode**: Toggle Mode to Spiral. The discrete dots merge into continuous curved arcs.

**Key concepts**: Golden angle spacing prevents radial alignment, arm count mask controls angular subdivision, dot mode requires both angular and radial test to pass

---

### Exercise 2: Rainbow Spiral Animation

<img src={phyllo_exercise2_result} alt="Rainbow Spiral Animation result"/>
*Rainbow Spiral Animation — simulated result across source images.*
**Objective**: Combine colour cycling with rotation animation to create evolving psychedelic spirals.

1. **Enable animation**: Toggle Animate on. Watch the pattern slowly rotate.
2. **Enable colour**: Toggle Color on. Dots acquire rainbow tint from the hue LUT.
3. **Sweep Tint Hue**: Rotate the Tint Hue knob — the colour palette shifts along the arms.
4. **Switch to spiral mode**: Toggle Mode to Spiral. The continuous arcs create more vivid colour gradients.
5. **Adjust scale**: Sweep Scale from tight to sparse — the spiral winds and unwinds in real time.
6. **Brighten**: Increase Brightness to maximum for saturated neon colours.

**Key concepts**: Hue LUT index combines pot position and arm test bits for position-dependent colour, animation phase increments once per field, colour cycles independently of animation speed

---

### Exercise 3: Video-Reactive Overlay

<img src={phyllo_exercise3_result} alt="Video-Reactive Overlay result"/>
*Video-Reactive Overlay — simulated result across source images.*
**Objective**: Use the video-reactive mode to map the spiral pattern onto bright regions of a source image.

1. **Prepare source**: Feed a high-contrast source with distinct bright and dark regions.
2. **Enable video reactive**: Toggle Video React on. Dots disappear from dark areas.
3. **Adjust brightness**: Increase Brightness so dots are clearly visible in bright regions.
4. **Enable colour**: Toggle Color on. The spiral pattern decorates only the bright content.
5. **Animate**: Toggle Animate on. The pattern rotates across the bright regions.
6. **Mix down**: Reduce Mix to ~60% to blend the effect subtly with the source.

**Key concepts**: Video-reactive mode is a hard gate at Y < 256 (not proportional), spiral pattern maps onto source brightness contours, mix crossfade blends effect with unprocessed source

---


## Tips

- **Manhattan distance matters**: The polar conversion uses Manhattan distance (|Δx| + |Δy|) rather than Euclidean, so the spiral pattern has a slightly diamond-shaped geometry rather than perfectly circular. This is most visible at large Scale values where the concentric rings are widely spaced.
- **Arm count controls density**: The arm mask is the single most powerful control for overall pattern density. At 1 arm, the pattern is sparse. At 8 arms, the pattern fills the angular space nearly uniformly.
- **Scale shift is logarithmic**: The four-step shift-based spacing produces a logarithmic tightness curve — most of the useful range for tight spirals is in the lowest quarter of knob travel.
- **Video reactive is a hard gate**: The Y < 256 threshold is not proportional — it is all-or-nothing. For softer interaction with the source, use the Mix fader to blend instead.
- **Animate speed is fixed**: The rotation rate is always 1 step per field (~6 RPM at 60 Hz). There is no speed control — use external modulation or animation of the Rotation pot for faster effects.
- **Hue cycling follows arm position**: The colour pattern repeats every 8 arm test values. With 8 arms visible, each arm gets a distinct hue. With fewer arms, a single arm cycles through all 8 colours along its length.
- **Feedback loops**: Routing the output back to the input creates recursive spiral overlays — dot patterns accumulate and interact with themselves, building increasingly dense textures.

---

## Glossary

| Term | Definition |
|------|------------|
| **DDS** | Direct Digital Synthesis; a technique using a phase accumulator to generate periodic waveforms from a fixed clock. |
| **Golden Angle** | Approximately 137.508°; the angle that divides a full circle in the ratio 1:φ, used in phyllotactic seed placement. |
| **Manhattan Distance** | The sum of absolute coordinate differences |Δx| + |Δy|; cheaper to compute than Euclidean distance but produces diamond-shaped contours. |
| **Octant** | One eighth of a full circle; the VHDL angle approximation divides the plane into 8 octants and interpolates linearly within each. |
| **Phase Accumulator** | A counter that wraps at a fixed modulus; its overflow rate sets the output frequency in DDS systems. |
| **Phyllotaxis** | The arrangement of leaves, seeds, or other lateral organs around a plant stem, typically governed by the golden angle. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Polar Coordinates** | A 2D coordinate system using radius and angle rather than x and y; the natural domain for spiral patterns. |
| **Proc Amp** | Processing Amplifier; a gain-and-offset stage that applies brightness and contrast adjustment to a signal. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |
