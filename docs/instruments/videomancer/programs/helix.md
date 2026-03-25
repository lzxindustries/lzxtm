---
draft: true
sidebar_position: 135
slug: /instruments/videomancer/helix
title: "Helix"
image: /img/instruments/videomancer/helix/helix_hero.png
description: "Before digital displays, oscilloscopes were the only way to visualize electronic signals as images."
---

![Helix hero image](/img/instruments/videomancer/helix/helix_hero_s1.png)
*Helix tracing luminous Lissajous figures with phosphor-decay afterglow, painting spirograph geometry onto a black canvas.*

---

## Overview

Helix is a parametric curve synthesizer that draws animated ***Lissajous figures*** and ***spirograph*** patterns directly onto the video signal. It works like a virtual oscilloscope: two sinusoidal functions: one for horizontal position, one for vertical position: sweep a bright point across the screen. The path of that point becomes the image. Adjusting the frequency ratio between the two axes produces the full family of Lissajous curves, from simple circles and figure-eights to elaborate knotwork and flowers.

What makes Helix special is its phosphor afterglow system. Each frame, the previous brightness is decayed and blended with the new beam position, producing luminous trails that linger on the screen like the phosphor glow of a long-persistence CRT monitor. At high afterglow settings, the entire curve is simultaneously visible as a glowing sculpture of light. At low settings, only the current beam position is bright, and the curve appears to be drawn in real time.

:::tip
***Helix is a synthesis program.*** It generates imagery from scratch: no input video is required. The curve, the glow, and the color are all created internally. The **Mix** fader can blend the generated pattern with an input signal if one is present.
:::

### What's In a Name?

A ***helix*** is a three-dimensional spiral: a curve that winds around a central axis while advancing along it. The name evokes the twisting, coiling geometry that this program produces. In Lissajous mode, the interlocking sine waves create flat figures that resemble projections of a helix viewed from different angles. In Spiral mode, the expanding radius literally traces a coil that unfurls from the center of the screen.

---

## Quick Start

1. With default settings, you will see a bright vertical line slowly drifting across the screen. Turn **Freq Y** (Knob 2) clockwise until the display reads about 3. A classic Lissajous bow-tie pattern appears, animated by the phase accumulator.
2. Increase **Afterglow** (Knob 5) to about 60%. The curve now leaves glowing phosphor trails behind it, revealing the full shape of the figure at once.
3. Raise **Beam Width** (Knob 4) to about 40%. The thin line thickens into a soft, luminous ribbon.
4. Switch **Color** (Switch 9) to **Rainbow**. The monochrome phosphor glow transforms into a spectrum of hues that shift across the width of the figure.

---

## Parameters

![Videomancer front panel with Helix loaded](/img/instruments/videomancer/helix/helix_control_panel.png)
*Videomancer's front panel with Helix active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Freq X

| Property | Value |
|----------|-------|
| Range | 1 – 16 |
| Default | 3 |

**Freq X** sets the horizontal frequency of the parametric curve. It selects one of sixteen integer frequency multipliers (1 through 16) that determine how many horizontal oscillation cycles the curve completes per frame. At the minimum setting, the beam sweeps back and forth once. At the maximum, sixteen complete cosine cycles are packed into a single frame, creating dense, tightly wound figures.

The ***frequency ratio*** between Freq X and **Freq Y** (Knob 2) is what determines the shape of the Lissajous figure. A ratio of 1 to 1 traces a circle or ellipse. A ratio of 1 to 2 creates a figure-eight. Ratios like 3 to 4 or 5 to 7 produce increasingly complex, interleaved patterns. Irrational-seeming ratios (where 16 frequency steps don't quite align) create figures that never perfectly close on themselves, drifting endlessly.

:::note
Both Freq X and Freq Y are quantized to integer steps. The knob's 10-bit range is divided into 16 equal zones, so you may notice the curve snapping between distinct shapes as you turn the knob.
:::

---

### Knob 2 — Freq Y

| Property | Value |
|----------|-------|
| Range | 1 – 16 |
| Default | 5 |

**Freq Y** sets the vertical frequency of the parametric curve. It works identically to **Freq X** (Knob 1) but controls the vertical sine component. Together, Freq X and Freq Y define the frequency ratio that determines the Lissajous figure's geometry. Low values of Freq Y produce simple figures with few lobes; high values create intricate, multi-lobed patterns.

When the **Curve** toggle (Switch 7) is set to **Spiral**, Freq Y controls the winding density of the spiral (higher values produce more tightly coiled spirals.)

---

### Knob 3 — Speed

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 20% |

**Speed** controls the animation rate of the curve. Each frame, an internal ***phase accumulator*** advances by the Speed value, continuously shifting the starting angle of the parametric equations. At 0%, the curve is frozen in place as a static figure. As Speed increases, the figure rotates, evolves, and flows like a living thing. At maximum, the figure whips through its cycle rapidly.

:::tip
At very low Speed values, the curve appears to breathe slowly: its lobes gradually shifting and morphing. This is because the phase accumulator's lower bits are being used, creating extremely fine angular steps between frames.
:::

---

### Knob 4 — Beam Width

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 29% |

**Beam Width** controls the thickness of the drawn curve. At 0%, the beam is a single pixel wide: a razor-thin line. As the value increases, the line thickens into a soft, glowing ribbon. The beam falloff is computed using a ***reciprocal lookup table*** that approximates a linear brightness gradient from the center of the beam to its edge, giving the curve a smooth, rounded cross-section when the **Beam** toggle (Switch 8) is set to **Soft**.

At high Beam Width values, the curve becomes a broad luminous band that can fill large portions of the screen, especially when combined with high **Afterglow** settings.

---

### Knob 5 — Afterglow

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 59% |

**Afterglow** controls the phosphor decay rate: how quickly previous frames fade out. At 0%, there is no persistence; only the current frame's beam positions are visible, and the curve appears as a set of scattered dots or short arcs. As Afterglow increases, previous frames linger longer, and the full Lissajous or spiral figure becomes visible as a continuous, glowing shape. At 100%, the decay is so slow that the entire history of the curve remains visible, eventually filling the screen with accumulated brightness.

The afterglow is implemented as an ***IIR filter*** (infinite impulse response): each pixel's brightness is the maximum of the new beam and the previous frame's brightness multiplied by the Afterglow coefficient. This produces the exponential decay characteristic of real CRT phosphor.

:::warning
Very high Afterglow values can cause brightness to accumulate over many frames, eventually saturating the image to full white. Reduce Afterglow or increase Speed to keep the figure balanced.
:::

---

### Knob 6 — Hue Shift

| Property | Value |
|----------|-------|
| Range | 0d – 360d |
| Default | 0d |

**Hue Shift** rotates the color palette when the **Color** toggle (Switch 9) is set to **Rainbow**. The full 360-degree range shifts the rainbow mapping along the horizontal axis, cycling through different starting colors. At 0 degrees, the default rainbow mapping is used. Rotating through 360 degrees cycles through the full spectrum and returns to the starting point.

When the **Phase Link** toggle (Switch 10) is set to **Linked**, Hue Shift additionally offsets the X-axis phase of the parametric curve, causing the figure's shape to rotate in tandem with the color change.

:::note
In **Mono** color mode, Hue Shift has no visible effect on brightness, but it still affects the phase offset when Phase Link is enabled.
:::

---

### Switch 7 — Curve

| Property | Value |
|----------|-------|
| Off | Lissajous |
| On | Spiral |
| Default | Lissajous |

**Curve** selects between two curve generation modes. In **Lissajous** mode, the vertical position is computed as `sin(b×t)` scaled by a fixed amplitude, producing classical Lissajous figures where every point on the curve sits within a fixed rectangular boundary. In **Spiral** mode, the vertical amplitude scales with the sample index, so the curve expands outward from the center as it traces, producing spirograph-like patterns that radiate from a central point.

Spiral mode creates denser, more complex geometric structures because the expanding radius causes successive loops to overlap at different distances from the center.

---

### Switch 8 — Beam

| Property | Value |
|----------|-------|
| Off | Soft |
| On | Hard |
| Default | Soft |

**Beam** selects the brightness profile of the drawn curve. In **Soft** mode, pixels near the center of the beam are brightest, and brightness falls off linearly toward the edge, producing a smooth, antialiased appearance. In **Hard** mode, every pixel inside the beam width is drawn at full brightness, creating a flat, uniform stroke with sharp edges.

:::tip
**Hard** beam mode combined with low **Beam Width** and low **Afterglow** produces a crisp, oscilloscope-like display. **Soft** beam mode with high width and high afterglow produces dreamy, ethereal phosphor paintings.
:::

---

### Switch 9 — Color

| Property | Value |
|----------|-------|
| Off | Mono |
| On | Rainbow |
| Default | Mono |

**Color** selects between two color mapping modes. In **Mono** mode, the curve is drawn with a ***green phosphor*** tint: the luminance drives a slight green-cyan bias in the chrominance channels, mimicking the characteristic glow of a P1 phosphor CRT oscilloscope. In **Rainbow** mode, the chrominance is derived from the horizontal screen position, producing a spectrum of colors that shifts across the width of the image. The **Hue Shift** knob (Knob 6) rotates this rainbow palette.

---

### Switch 10 — Phase Link

| Property | Value |
|----------|-------|
| Off | Free |
| On | Linked |
| Default | Free |

**Phase Link** couples the **Hue Shift** knob (Knob 6) to the X-axis phase of the parametric curve. In **Free** mode, Hue Shift only affects color (in Rainbow mode). In **Linked** mode, Hue Shift also offsets the phase accumulator for the X cosine, causing the Lissajous figure to rotate spatially when you turn Knob 6. This creates a direct connection between the curve's orientation and its color mapping.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Helix synthesis. The sync delay pipeline still aligns timing, so there is no glitch on transition. Because Helix is a synthesis program, enabling Bypass effectively mutes the generated pattern and passes through whatever input signal is present (or black, if no input is connected).

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**Mix** controls the dry/wet crossfade between the input video signal and the generated Helix pattern. At 0%, only the dry input signal is visible. At 100%, only the generated curve is visible. Intermediate values blend the two together, allowing the Lissajous figures to be superimposed on top of live video at any desired opacity.

:::tip
Mix is especially useful for layering Helix patterns over other Videomancer programs in a signal chain. Feed a processed signal into Helix and use Mix to blend the geometric curves with the incoming video.
:::

---

## Background

### Lissajous figures

***Lissajous figures*** are the patterns produced when two sinusoidal signals are used to drive the horizontal and vertical deflection of a point simultaneously. If you feed two sine waves into the X and Y inputs of an oscilloscope in XY mode, the resulting pattern on the screen is a Lissajous figure. The shape of the figure depends entirely on the ***frequency ratio*** and ***phase relationship*** between the two signals.

When the frequencies are equal (1:1), the figure is a circle or ellipse depending on the phase offset. A 2:1 ratio produces a figure-eight. A 3:2 ratio creates a trefoil-like shape with three lobes. As the ratio becomes more complex: 5:4, 7:6, 13:8: the figure gains more lobes and interlocking petals, eventually resembling intricate lace or Celtic knotwork. When the ratio is irrational, the figure never closes on itself and continuously traces out new paths.

Jules Antoine Lissajous first studied these curves in the 1850s using tuning forks and mirrors. They became a staple of oscilloscope art in the 20th century, and remain a fundamental tool for visualizing frequency relationships in electronics.

### Phosphor persistence

Early cathode-ray tube (CRT) displays used ***phosphor*** coatings that continued to glow after the electron beam had passed. The duration of this afterglow varied by phosphor type: P1 (green, medium persistence), P7 (blue-white to yellow, long persistence), and P31 (green, short persistence) were common in oscilloscope CRTs. Long-persistence phosphors allowed the entire trace to remain visible simultaneously, which was essential for viewing slow-moving waveforms.

Helix simulates this behavior digitally. Each pixel remembers its brightness from the previous frame and decays it by a configurable amount before comparing it with the new frame. The maximum of the decayed value and the new beam brightness is kept, producing the characteristic ghosting trails of a phosphor display. This is mathematically equivalent to a first-order ***IIR low-pass filter*** with a configurable time constant.

### Spirograph geometry

When Helix is set to **Spiral** mode, the vertical amplitude grows with the sample index, producing curves that expand outward from the center. This is related to the geometry of a ***spirograph***: the classic drawing toy where a small gear rolls inside a larger ring, tracing out ***hypotrochoid*** and ***epitrochoid*** curves. While Helix does not model the exact gear mechanics, its parametric equations produce visually similar results: rosette patterns, multi-petaled flowers, and expanding coils.


---

## Signal Flow

### Signal Flow Notes

Two systems work in alternation. During the ***vertical blanking interval***, Helix evaluates 256 points along the parametric curve and writes the Y position of the nearest curve point into a column-indexed BRAM. During ***active video***, each pixel reads that BRAM to find how far it is from the nearest curve point, then computes beam brightness accordingly.

The afterglow system operates per-pixel in a second BRAM bank. Each pixel's previous glow value is read, decayed by multiplication with the Afterglow coefficient, then max-blended with the current beam brightness. This IIR feedback loop produces the exponential phosphor decay: bright areas fade gradually over many frames, while the newest beam position always appears at full brightness.

:::tip
**The curve is recomputed every frame.** Because the phase accumulator advances each vsync, the curve's orientation shifts continuously. The afterglow BRAM preserves the trail of previous positions, so the visible figure is actually the rolling maximum of many slightly different curve positions.
:::


---

## Exercises

These exercises explore Helix's controls from simple Lissajous figures through phosphor painting to complex animated spirograph geometry.
### Exercise 1: Classic Lissajous Figures

![Classic Lissajous Figures result](/img/instruments/videomancer/helix/helix_ex1_s1.png)
*Classic Lissajous Figures — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Explore the fundamental Lissajous shapes by adjusting the X and Y frequency ratio, then reveal the complete figures with afterglow persistence.

#### Key Concepts

- Frequency ratio determines curve shape
- Phase accumulator creates continuous animation
- Afterglow reveals the full figure

#### Steps

1. **Simple oscillation**: With defaults, a single line drifts across the screen. Set **Freq X** (Knob 1) to 1 and **Freq Y** (Knob 2) to 2. A figure-eight appears.
2. **Reveal the figure**: Increase **Afterglow** (Knob 5) to about 80%. The persistence trails reveal the complete bow-tie shape of the 1:2 Lissajous.
3. **More complex shapes**: Set Freq Y to 3. The figure becomes a three-lobed trefoil. Try 5, 7, and other values to see how the lobe count changes.
4. **Equal frequencies**: Set both Freq X and Freq Y to 3. The figure collapses into a circle or ellipse, depending on the current phase.
5. **Dense knotwork**: Set Freq X to 7 and Freq Y to 9. A complex, interlocking pattern emerges.
6. **Freeze the figure**: Set **Speed** (Knob 3) to 0%. The animation halts, and you can study the frozen figure.

#### Settings

| Control | Value |
|---------|-------|
| Freq X | 1 |
| Freq Y | 2 |
| Speed | ~20% |
| Beam Width | ~30% |
| Afterglow | 80% |
| Hue Shift | 0d |
| Curve | Lissajous |
| Beam | Soft |
| Color | Mono |
| Phase Link | Free |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Phosphor Painting

![Phosphor Painting result](/img/instruments/videomancer/helix/helix_ex2_s1.png)
*Phosphor Painting — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Use Helix as a luminous painting tool, creating thick, soft phosphor trails that build up into glowing abstractions.

#### Key Concepts

- Beam Width controls the thickness and softness of the drawn line
- Soft vs. Hard beam modes produce different visual characters
- Afterglow creates long-exposure-like accumulation

#### Steps

1. **Thick beam**: Set **Beam Width** (Knob 4) to about 70%. The curve becomes a wide, luminous ribbon.
2. **Maximum afterglow**: Set **Afterglow** (Knob 5) to about 90%. The ribbon's trail fills the screen slowly, creating a glowing painting.
3. **Hard edges**: Toggle **Beam** (Switch 8) to **Hard**. The soft glow snaps to flat, uniform brightness with crisp edges (like neon tubing.)
4. **Add color**: Switch **Color** (Switch 9) to **Rainbow**. The monochrome glow transforms into a spectrum. Rotate **Hue Shift** (Knob 6) to shift the palette.
5. **Speed dynamics**: Slowly increase **Speed** (Knob 3). The painting evolves faster, the trails becoming denser and eventually merging into solid regions of accumulated brightness.
6. **Reduce afterglow**: Lower Afterglow back to about 30%. Now the trails are short, creating a comet-like tail behind the beam.

#### Settings

| Control | Value |
|---------|-------|
| Freq X | 3 |
| Freq Y | 4 |
| Speed | ~30% |
| Beam Width | 70% |
| Afterglow | 90% |
| Hue Shift | 0d |
| Curve | Lissajous |
| Beam | Soft |
| Color | Rainbow |
| Phase Link | Free |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Spirograph Geometry

![Spirograph Geometry result](/img/instruments/videomancer/helix/helix_ex3_s1.png)
*Spirograph Geometry — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Switch to Spiral mode and combine high frequencies, phase linking, and afterglow to create intricate, animated spirograph patterns.

#### Key Concepts

- Spiral mode creates expanding-radius curves
- Phase Link couples color rotation with curve orientation
- High frequency ratios produce dense rosette patterns

#### Steps

1. **Enter Spiral mode**: Toggle **Curve** (Switch 7) to **Spiral**. The Lissajous figure transforms into an expanding coil radiating from the center.
2. **Higher frequencies**: Set **Freq X** (Knob 1) to 5 and **Freq Y** (Knob 2) to 8. The spiral gains multiple petals, resembling a spirograph drawing.
3. **Full afterglow**: Set **Afterglow** (Knob 5) to about 85%. The spirograph rosette reveals itself as a complete, symmetric flower.
4. **Link phase and color**: Switch **Phase Link** (Switch 10) to **Linked** and **Color** (Switch 9) to **Rainbow**. Now rotate **Hue Shift** (Knob 6) slowly. The color palette and the curve's orientation rotate together, creating a kaleidoscopic effect.
5. **Fine beam**: Set **Beam Width** (Knob 4) to about 15% and **Beam** (Switch 8) to **Hard**. The pattern becomes a precise, fine-lined geometric drawing.
6. **Animate**: Set **Speed** (Knob 3) to about 50%. The spirograph rotates continuously, its petals cycling through the rainbow.

#### Settings

| Control | Value |
|---------|-------|
| Freq X | 5 |
| Freq Y | 8 |
| Speed | ~50% |
| Beam Width | ~15% |
| Afterglow | 85% |
| Hue Shift | 180d |
| Curve | Spiral |
| Beam | Hard |
| Color | Rainbow |
| Phase Link | Linked |
| Bypass | Off |
| Mix | 100% |

---
## Glossary

- **Afterglow**: The lingering brightness left on screen after the beam has moved on, simulating the phosphor persistence of a CRT display.

- **Beam Width**: The thickness of the drawn curve, measured in pixels from the center of the line to its edge; controls how much screen area each curve point illuminates.

- **Frequency Ratio**: The relationship between the X and Y oscillation frequencies; determines the shape and number of lobes in a Lissajous figure.

- **IIR Filter**: Infinite Impulse Response filter; a feedback-based filter where each output depends on previous outputs, producing exponential decay.

- **Lissajous Figure**: A parametric curve created by plotting two sinusoidal signals against each other on perpendicular axes; the shape depends on their frequency ratio and phase.

- **Phase Accumulator**: A counter that advances by a fixed increment each frame, producing a continuously changing angle that animates the parametric curve.

- **Phosphor**: A luminescent coating on a CRT screen that glows when struck by an electron beam and continues to emit light briefly afterward.

- **Reciprocal LUT**: A lookup table storing precomputed 1/x values, used to replace hardware division with a single table read and multiply.

- **Spirograph**: A geometric drawing toy that produces hypotrochoid and epitrochoid curves; Helix's Spiral mode creates visually similar expanding rosette patterns.

---
