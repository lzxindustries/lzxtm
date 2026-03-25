---
draft: true
sidebar_position: 196
slug: /instruments/videomancer/mobius
title: "Mobius"
image: /img/instruments/videomancer/mobius/mobius_hero_s1.png
description: "Mobius maps video onto the surface of a Möbius strip — a one-sided topological surface created by taking a rectangular band, giving it a half-twist, and joining the ends."
---

![Mobius hero image](/img/instruments/videomancer/mobius/mobius_hero_s1.png)
*Mobius applying topological twist mapping to fold video through progressive mirror, luma inversion, and quadrant-based chroma rotation.*

---

## Overview

**Mobius** reimagines your video as a surface with only one side. The familiar rectangle of the screen becomes a twisted band: as your eye moves from top to bottom, the image progressively mirrors, its brightness inverts toward a photographic negative, and its colors rotate through a complete hue cycle. At the twist midpoint the transformation is at full strength: then it unwinds, returning to normal by the bottom of the frame. The result is a seamless topological loop where the beginning and the end are the same.

A luminous seam line traces across the frame, marking the single boundary where the virtual strip's surface folds back on itself. Mobius requires no frame buffer: every transformation is a per-pixel coordinate computation, giving the effect a crisp, immediate character with zero latency beyond the pipeline.

Mobius operates in the ***Warp*** category. At subtle settings it adds an uncanny symmetry to ordinary footage. At extreme settings it fractures the image into kaleidoscopic color fields that bear little resemblance to the source, especially when the animation engine is engaged and the twist scrolls continuously through the frame.

:::tip
Mobius is a ***processing*** program: it transforms an incoming video signal. Feed it a camera, a pattern generator, or the output of another Videomancer program for best results.
:::

### What's In a Name?

A ***Möbius strip*** is the famous mathematical surface with only one side and one boundary. You can make one by taking a strip of paper, giving it a single half-twist, and gluing the ends together. An ant walking along the surface would traverse both "sides" before returning to its starting point, never crossing an edge. **Mobius** maps this topology onto video: as scanlines advance down the frame, the image undergoes a continuous twist: mirroring, inverting, and rotating: then unwinds back to normal, forming a closed loop with no seam between the beginning and the end.

---

## Quick Start

1. Turn **Twist Rate** (Knob 1) clockwise to about 40%. You'll see the image begin to mirror vertically from the center of the frame: the top half gradually flips while the bottom half remains normal.
2. Increase **Inversion Depth** (Knob 3) past 50%. The twisted region now darkens and inverts, resembling a photographic negative at the midpoint of the twist.
3. Turn **Hue Rotation** (Knob 4) clockwise. Colors in the twisted region begin shifting: reds become blues, greens become magentas: as chroma rotates through quadrant-based hue shifts.
4. Set **Seam Width** (Knob 5) to around 25% and observe a bright line tracing across the frame, marking the boundary of the virtual Möbius surface.

---

## Parameters

![Videomancer front panel with Mobius loaded](/img/instruments/videomancer/mobius/mobius_control_panel.png)
*Videomancer's front panel with Mobius active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — TwstRate

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |

**Twist Rate** controls how many ***half-twists*** the virtual Möbius band makes across the height of the frame. At minimum, a single gentle half-twist stretches from top to bottom: the image barely folds before unwinding. As you increase Twist Rate, the band winds more tightly: two half-twists, then four, then eight. Each additional half-twist adds another cycle of mirroring, inversion, and hue rotation within the frame height.

At low values, the effect is a broad, sweeping warp. At high values, the frame fills with rapid oscillations of mirrored and inverted bands, creating a striped, almost kaleidoscopic texture.

:::note
The twist phase follows a ***triangle wave***, ramping from 0 to full effect and back again smoothly. This is what creates the seamless topological loop: the image at the bottom of the frame matches the image at the top.
:::

---

### Knob 2 — TwstCntr

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Twist Center** sets the vertical origin line around which the twist is computed. At 50%, the twist is centered in the middle of the frame. Turning the knob counterclockwise shifts the twist origin toward the top of the frame; turning it clockwise shifts it toward the bottom.

Moving the center repositions the entire twist pattern vertically, which changes where the maximum-effect zone falls within the visible image.

---

### Knob 3 — InvDepth

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Inversion Depth** controls the strength of the ***luma inversion*** component of the twist. At 0% the twist only mirrors: brightness is unaffected. As Inversion Depth increases, pixels in the twisted region progressively invert: midtones stay stable while highlights become shadows and shadows become highlights. At 100%, the midpoint of the twist is a full photographic negative.

When **Mode** (Switch 8) is set to Mirror, Inversion Depth has no visible effect (the inversion pathway is disabled entirely.)

---

### Knob 4 — Hue Rot

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Hue Rotation** controls the strength of the ***chroma rotation*** applied in the twisted region. At 0%, colors pass through unchanged regardless of the twist phase. As Hue Rotation increases, the U and V chroma channels rotate through four quadrants as the twist progresses: original → 90° → 180° → 270° → original. At 100%, the full quadrant rotation is applied.

The rotation uses ***quadrant interpolation***: instead of a smooth continuous rotation, the chroma snaps between four cardinal directions and interpolates within each quadrant. This produces bold, graphic color shifts rather than subtle tinting.

:::tip
Setting Hue Rotation to maximum while keeping Inversion Depth at zero isolates the color effect: you get a rainbow-banded image without any brightness changes.
:::

---

### Knob 5 — SeamWdth

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 13% |

**Seam Width** sets the thickness of the bright boundary line that traces the single edge of the Möbius surface across the frame. At 0%, no seam is visible. As Seam Width increases, a white line appears and grows wider, marking the fold point of the twist. The seam's horizontal position follows the twist phase, sweeping across the frame as the twist oscillates.

The seam replaces the processed video with a bright achromatic line (white with neutral chroma). When **Seam** (Switch 9) is set to Soft, the seam fades at its edges rather than cutting sharply.

---

### Knob 6 — AnimSpd

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |

**Animation Speed** controls how quickly the twist phase scrolls when animation is enabled. At 0% the twist is stationary. Increasing the value causes the twist pattern to drift continuously downward through the frame, driven by a ***phase accumulator*** that advances once per video field. Higher values produce faster scrolling.

Animation Speed has no effect unless **Animate** (Switch 7) is set to On.

---

### Switch 7 — Animate

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Animate** enables or disables the automatic animation engine. When set to Off, the twist pattern is fixed in position: it responds only to the static **Twist Rate** and **Twist Center** parameters. When set to On, the twist scrolls continuously through the frame at a rate determined by **Animation Speed** (Knob 6). The animation accumulates phase over time, so the twist pattern cycles endlessly.

---

### Switch 8 — Mode

| Property | Value |
|----------|-------|
| Off | Full |
| On | Mirror |
| Default | Full |

**Mode** selects between two twist behaviors. In Full mode, the twist applies all three transformations: mirroring, luma inversion, and chroma rotation: creating the complete Möbius topology. In Mirror mode, only the mirror component is active: brightness and color pass through unchanged, and only the spatial mirroring of horizontal position follows the twist phase.

:::note
Mirror mode is useful when you want the geometric folding without the tonal or color changes. It's a gentler, more purely spatial effect.
:::

---

### Switch 9 — Seam

| Property | Value |
|----------|-------|
| Off | Hard |
| On | Soft |
| Default | Hard |

**Seam** controls the rendering style of the boundary line. In Hard mode, pixels within the seam width are replaced with solid white (maximum luminance, neutral chroma), creating a crisp geometric line. In Soft mode, the seam brightness falls off with distance from the center of the line, producing a glowing, anti-aliased appearance.

---

### Switch 10 — Channels

| Property | Value |
|----------|-------|
| Off | YUV |
| On | Y Only |
| Default | YUV |

**Channels** selects which color channels receive the twist transformation. In YUV mode, all three channels (Y, U, and V) are processed: luma inversion affects brightness and chroma rotation affects color. In Y Only mode, the chroma rotation is disabled: only the luminance channel is twisted, while U and V pass through unchanged. This produces a monochromatic twist where brightness shifts but colors stay anchored to the original image.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, skipping all Mobius processing stages. The sync delay pipeline still aligns timing, so there is no glitch when toggling. Use Bypass for instant A/B comparison between the raw input and the twisted result.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (unprocessed) input and the wet (twisted) output. At 0%, only the original signal appears. At 100%, only the Mobius-processed signal appears. Intermediate values blend the two, which can produce ghostly overlays of the twisted and original images.

---

## Background

### The Möbius Strip in Mathematics

The ***Möbius strip*** (or Möbius band) is a surface with the remarkable property of being ***non-orientable***: it has only one side and one boundary curve. Discovered independently by August Ferdinand Möbius and Johann Benedict Listing in 1858, it became one of the most recognized objects in topology, the branch of mathematics concerned with properties preserved under continuous deformation.

The key property that Mobius borrows is the twist. On a physical Möbius strip, traveling along the surface reverses your orientation: left becomes right, up becomes down. The program maps this to video: as you move down the frame, the image progressively flips horizontally (mirroring), inverts tonally (negative), and rotates chromatically (hue shift). At the twist midpoint the transformation is at full strength. By the bottom of the frame, it has unwound completely: the video matches the top again, forming a closed topological loop.

### Quadrant Chroma Rotation

The chroma rotation in Mobius is not a smooth angular sweep: it uses ***quadrant interpolation*** to approximate a full 360° rotation using only addition, subtraction, and fixed-point multiplication. The U and V chroma channels are treated as coordinates on a plane centered at neutral gray (512, 512). The twist phase divides this plane into four quadrants:

| Quadrant | U transform | V transform |
|----------|-------------|-------------|
| 0 (0°–90°) | U → −V | V → U |
| 1 (90°–180°) | U → −U | V → −V |
| 2 (180°–270°) | U → V | V → −U |
| 3 (270°–360°) | U → U | V → V |

Within each quadrant, the program interpolates linearly between the start and end positions. This produces color shifts that move through the primaries in bold steps rather than continuous sweeps: an aesthetic choice that gives the effect a graphic, almost posterized quality.

### Phase Accumulator Animation

When animation is enabled, a 16-bit ***phase accumulator*** advances by the animation speed value on every vertical sync pulse. This is a ***direct digital synthesis*** (DDS) technique: a fixed increment is added to a running counter each frame, and the counter's value determines the current phase offset of the twist. Because the accumulator wraps at 16 bits, the animation loops seamlessly: the twist pattern scrolls endlessly through the frame without discontinuities.


---

## Signal Flow

### Signal Flow Notes

The critical interaction is between the ***twist phase*** and the three transformation channels (mirror, inversion, chroma rotation). All three are modulated by the same triangle-wave phase signal derived from the vertical position counter, twist scale, and animation offset. This means mirroring, inversion, and color rotation always move in lockstep (they cannot be independently animated.)

The ***triangle wave folding*** is essential to the Möbius topology. The raw phase (distance × scale + animation) is a sawtooth that could jump discontinuously. Bit 10 of the raw phase determines the fold direction: when it's 0, the phase ramps up; when it's 1, the phase ramps down (1023 minus the lower bits). This creates a smooth back-and-forth sweep that gives the twist its seamless, looping character.

:::tip
Because all three transformations share a single phase signal, adjusting **Twist Rate** changes the spatial frequency of mirroring, inversion, *and* hue rotation simultaneously. To isolate just one transformation, use **Mode** (Mirror only) or **Channels** (Y Only) to disable the others.
:::


---

## Exercises

These exercises progress from simple mirroring to full topological color mapping. Each exercise introduces additional transformation layers.
### Exercise 1: The Basic Twist

![The Basic Twist result](/img/instruments/videomancer/mobius/mobius_ex1_s1.png)
*The Basic Twist — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A symmetric mirror effect that folds the image like a paper strip, demonstrating the core Möbius geometry.

#### Key Concepts

- The twist phase creates a triangle-wave mirror pattern
- Twist Rate controls the spatial frequency of the fold
- Twist Center repositions the origin

#### Video Source

A live camera feed or recorded footage with clear left-right asymmetry (text, faces, or objects placed off-center).

#### Steps

1. Set **Mode** (Switch 8) to Mirror to isolate the spatial component.
2. Turn **Twist Rate** (Knob 1) slowly clockwise from minimum. At low values, a single broad fold appears (the bottom of the frame mirrors the top.)
3. Continue increasing Twist Rate. The frame fills with alternating normal and mirrored bands, like a hall of mirrors laid horizontally.
4. Sweep **Twist Center** (Knob 2) from left to right. The fold pattern slides up and down the frame as the origin moves.
5. Enable **Animate** (Switch 7) and set **Animation Speed** (Knob 6) to around 25%. The mirror bands scroll continuously through the frame.

#### Settings

| Control | Value |
|---------|-------|
| Twist Rate | ~40% |
| Twist Center | 50% |
| Inversion Depth | 0% |
| Hue Rotation | 0% |
| Seam Width | 0% |
| Animation Speed | ~25% |
| Animate | Off |
| Mode | Mirror |
| Seam | Hard |
| Channels | YUV |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Negative Twist with Seam

![Negative Twist with Seam result](/img/instruments/videomancer/mobius/mobius_ex2_s1.png)
*Negative Twist with Seam — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A dramatic inversion effect where the image alternates between positive and negative, with a visible boundary line tracing the twist.

#### Key Concepts

- Luma inversion creates photographic negative zones
- The seam line traces the Möbius boundary
- Hard vs. soft seam rendering

#### Video Source

High-contrast footage: strong blacks and whites show the inversion most clearly. Architectural subjects or bold graphics work well.

#### Steps

1. Set **Mode** (Switch 8) to Full and **Twist Rate** (Knob 1) to about 40%.
2. Increase **Inversion Depth** (Knob 3) to 100%. The twisted regions now fully invert: bright areas become dark and vice versa, meeting normal regions at the fold boundary.
3. Set **Seam Width** (Knob 5) to about 25%. A bright white line appears, tracing the fold point across the frame.
4. Toggle **Seam** (Switch 9) between Hard and Soft. Hard produces a crisp geometric line; Soft produces a glowing falloff.
5. Enable **Animate** (Switch 7) and set **Animation Speed** (Knob 6) to about 50%. The seam sweeps across the frame as the twist scrolls.

#### Settings

| Control | Value |
|---------|-------|
| Twist Rate | ~40% |
| Twist Center | 50% |
| Inversion Depth | 100% |
| Hue Rotation | 0% |
| Seam Width | ~25% |
| Animation Speed | ~50% |
| Animate | On |
| Mode | Full |
| Seam | Soft |
| Channels | YUV |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Full Topological Color Map

![Full Topological Color Map result](/img/instruments/videomancer/mobius/mobius_ex3_s1.png)
*Full Topological Color Map — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

The complete Möbius experience: mirroring, inversion, and rainbow chroma rotation scrolling through an animated twist.

#### Key Concepts

- Quadrant chroma rotation produces bold hue shifts
- All three transformations lock to a single phase
- Mix crossfade creates ghostly overlay effects

#### Video Source

Colorful footage with a variety of hues: nature scenes, abstract patterns, or a color bar test signal.

#### Steps

1. Set **Mode** (Switch 8) to Full and **Channels** (Switch 10) to YUV.
2. Set **Twist Rate** (Knob 1) to about 50% and **Inversion Depth** (Knob 3) to about 70%.
3. Turn **Hue Rotation** (Knob 4) to 100%. The twisted regions now cycle through bold color shifts: reds become blues, greens become magentas: locked to the same phase as the mirror and inversion.
4. Set **Seam Width** (Knob 5) to about 15% with **Seam** set to Soft for a glowing boundary line.
5. Enable **Animate** (Switch 7) and set **Animation Speed** (Knob 6) to about 35%. Watch the complete topological transformation scroll endlessly through the frame.
6. Lower **Mix** (Fader 12) to about 60%. The processed and original images overlap, creating a ghostly double-exposure where twisted and untwisted versions of the image coexist.

#### Settings

| Control | Value |
|---------|-------|
| Twist Rate | ~50% |
| Twist Center | 50% |
| Inversion Depth | ~70% |
| Hue Rotation | 100% |
| Seam Width | ~15% |
| Animation Speed | ~35% |
| Animate | On |
| Mode | Full |
| Seam | Soft |
| Channels | YUV |
| Bypass | Off |
| Mix | ~60% |

---
## Glossary

- **Chroma**: The color information in a video signal, encoded as U and V components in YUV color space.

- **Direct Digital Synthesis (DDS)**: A technique for generating periodic waveforms by incrementing a phase accumulator at a fixed rate. Used here to animate the twist.

- **Half-Twist**: A 180° rotation of a strip before joining its ends; the defining operation of a Möbius strip. Mobius maps this to one full cycle of mirror + invert + hue rotate.

- **Luma**: The brightness component (Y) of a YUV video signal, representing perceived lightness.

- **Luma Inversion**: Subtracting the luminance value from the maximum (1023 − Y), producing a photographic negative.

- **Non-Orientable**: A surface that has no consistent "inside" and "outside." The Möbius strip is the simplest example.

- **Phase Accumulator**: A counter that adds a fixed increment each frame, wrapping at overflow. Its current value sets the animation position.

- **Quadrant Interpolation**: Approximating a full 360° rotation by dividing the angle into four 90° segments and interpolating linearly within each.

- **Topology**: The branch of mathematics concerned with properties that are preserved under continuous deformation: stretching, twisting, and bending, but not tearing or gluing.

- **Triangle Wave**: A periodic waveform that ramps linearly up and then linearly down, creating a symmetric back-and-forth oscillation.

---
