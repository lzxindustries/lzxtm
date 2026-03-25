---
draft: true
sidebar_position: 292
slug: /instruments/videomancer/subphase
title: "Sub Phase"
image: /img/instruments/videomancer/subphase/subphase_hero_s1.png
description: "Subphase simulates the subcarrier phase errors that plague analog color television reception."
---

![Sub Phase hero image](/img/instruments/videomancer/subphase/subphase_hero_s1.png)
*Sub Phase applying NTSC-style dot crawl and hue rotation to a color image, simulating the characteristic chroma artifacts of analog composite video.*

---

## Overview

Sub Phase simulates the color imperfections of analog composite television. It recreates the look of NTSC and PAL video by rotating the chroma plane, wobbling the phase angle line by line, injecting dot crawl interference, and scaling the color burst amplitude. The result ranges from a subtle warm tint: the kind of gentle hue shift you'd see on a slightly mistuned television: to aggressive chromatic destruction reminiscent of a VCR chewing through a tape.

At its heart, Sub Phase performs a ***rotation matrix*** on the U and V color channels, spinning hues around the color wheel while leaving brightness untouched. Layered on top of that rotation are three additional chroma distortion effects: phase wobble (randomized per-line jitter), dot crawl (a periodic chroma modulation at the subcarrier frequency), and chroma noise (random UV perturbation from a pseudo-random generator). A brightness offset and a wet/dry mix round out the controls.

:::tip
Sub Phase is a processing program. It transforms an incoming video signal: it does not generate imagery on its own. Feed it something colorful for the best results.
:::

### What's In a Name?

The name ***Sub Phase*** refers to the ***subcarrier phase*** of analog composite video. In NTSC and PAL television systems, color information is encoded as a high-frequency signal (the ***subcarrier***) that rides on top of the luminance waveform. The ***phase angle*** of this subcarrier determines the hue, and the ***amplitude*** determines the saturation. When the phase drifts or the reference burst is corrupted, colors shift and crawl (the very artifacts Sub Phase recreates digitally.)

---

## Quick Start

1. Turn **Phase Shift** (Knob 1) slowly clockwise. Watch the colors in your image rotate through the spectrum: reds become greens, blues become oranges, and everything shifts around the color wheel.
2. Increase **Phase Wobble** (Knob 2) to about 40%. Each scan line now has a slightly different hue, creating a shimmering, unstable look (like a TV with a weak antenna signal.)
3. Raise **Dot Crawl** (Knob 3) to about 50%. A fine, crawling interference pattern appears on vertical color edges, mimicking the classic composite video artifact.
4. Sweep **Color Burst** (Knob 4) from its default midpoint down toward zero. Colors fade toward monochrome as the chroma amplitude drops (a weak color burst.)

---

## Parameters

![Videomancer front panel with Sub Phase loaded](/img/instruments/videomancer/subphase/subphase_control_panel.png)
*Videomancer's front panel with Sub Phase active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Phase Shift

| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |

**Phase Shift** controls the base hue rotation angle applied to the U and V chroma channels. At 0°, fully counterclockwise, no rotation is applied and colors pass through unchanged. As the knob sweeps clockwise, colors rotate around the ***color wheel***: a 90° shift turns reds into purples and greens into yellows; at 180° the image is fully complementary: every color becomes its opposite; at 360° the rotation completes a full loop and returns to the original hues. The rotation is performed by a 32-entry sine/cosine lookup table driving a 2×2 matrix multiply on the centered U and V values.

:::note
Because the lookup table has 32 entries, the hue angle is quantized into 32 discrete steps of approximately 11.25° each. Fine hue adjustments between steps are not possible.
:::

---

### Knob 2 — Phase Wobble

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |

**Phase Wobble** adds per-line phase instability to the rotation angle, simulating a ***mis-locked color burst*** reference. At 0%, every scan line uses the same base phase from **Phase Shift**. As the value increases, a pseudo-random offset from the internal LFSR is mixed into the phase index, causing each line to land on a slightly different hue. At high values, the image becomes a horizontal rainbow of shifting tints: each line tells a different color story. The wobble intensity is masked by the knob setting, so lower values produce gentle shimmer while higher values create dramatic line-by-line hue variation.

---

### Knob 3 — Dot Crawl

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |

**Dot Crawl** injects a periodic chroma modulation pattern that mimics the ***cross-color*** interference artifacts seen on analog composite video. At 0%, no dot crawl is applied. As the value increases, a fine alternating pattern modulates the U channel at the simulated subcarrier frequency. In NTSC mode, the pattern repeats every 4 pixels; in PAL mode, it repeats every 8 pixels with per-line sign alternation. The effect appears as a crawling checkerboard of color fringing along edges, most visible on saturated vertical boundaries.

:::tip
Enable **Crawl Anim** (Switch 8) to see the dots "crawl" across the screen frame by frame. Set it to **Static** to freeze the pattern in place for a fixed texture overlay.
:::

---

### Knob 4 — Color Burst

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Color Burst** controls the amplitude of the chroma signal after rotation: effectively a saturation control. At the default midpoint (50%), colors pass through at their original saturation. Turning counterclockwise toward 0% fades chroma to nothing, producing a desaturated, near-monochrome image. Turning clockwise toward 100% boosts chroma amplitude to roughly double, creating oversaturated, bleeding colors. The control models the strength of the ***color burst*** reference signal that an analog TV uses to decode color.

---

### Knob 5 — Chroma Noise

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |

**Chroma Noise** adds pseudo-random perturbation to the U and V channels, simulating tape head instability or a noisy RF reception path. At 0%, no noise is added. As the value increases, random offsets from the internal 16-bit LFSR are scaled and summed into both chroma channels independently. At high values, the image develops a flickering, grainy color texture: the kind of chromatic instability you see on a worn VHS tape where the azimuth tracking is slightly off.

---

### Knob 6 — Brightness

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Brightness** applies a DC offset to the luminance channel. At the default midpoint (50%), no offset is applied. Turning counterclockwise darkens the image; turning clockwise brightens it. Unlike a multiplicative gain, this is a simple additive shift: black becomes gray when brightened, and white clips when pushed too far. Values are clamped to the valid 10-bit range, so extreme settings crush shadows or blow out highlights.

---

### Switch 7 — Standard

| Property | Value |
|----------|-------|
| Off | NTSC |
| On | PAL |
| Default | NTSC |

**Standard** selects between NTSC and PAL dot crawl patterns. With the switch set to **NTSC**, dot crawl uses a period-4 pixel pattern, matching the relationship between the 3.58 MHz NTSC subcarrier and the pixel clock. With the switch set to **PAL**, dot crawl uses a period-8 pattern with per-line sign alternation, reflecting the ***Phase Alternating Line*** encoding where the subcarrier phase flips on alternate scan lines. This toggle only affects the **Dot Crawl** parameter (it has no effect when Dot Crawl is at 0%.)

---

### Switch 8 — Crawl Anim

| Property | Value |
|----------|-------|
| Off | Static |
| On | Animate |
| Default | Animate |

**Crawl Anim** controls whether the dot crawl pattern animates or remains static. With the switch set to **Animate** (default), the dot pattern shifts by a pixel offset every frame, producing the characteristic "crawling" motion of composite video artifacts. With the switch set to **Static**, the pattern is frozen in place, creating a fixed spatial texture. Like **Standard**, this toggle only affects the **Dot Crawl** parameter.

---

### Switch 9 — Tint Lock

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Tint Lock** is a reserved toggle. In the current firmware version, this switch has no audible effect on the output signal. It is wired into the parameter register but is not referenced by the processing pipeline. Future firmware updates may assign it a function.

---

### Switch 10 — Chroma Kill

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Chroma Kill** forces both U and V channels to their neutral midpoint, stripping all color from the processed signal and leaving only the luminance channel active. With the switch set to **Off** (default), chroma passes through the rotation, burst, dot crawl, and noise stages normally. With the switch set to **On**, the processed U and V values are zeroed regardless of all other chroma controls. The brightness offset and luma channel are unaffected. Use Chroma Kill for instant monochrome comparison, or combine it with the **Mix** fader to blend between full color and monochrome.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the delay-aligned input signal directly to the output, skipping all Sub Phase processing stages. The sync delay pipeline still aligns timing, so there is no glitch when toggling. Use Bypass for instant A/B comparison between the raw input and the processed result.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**Mix** blends between the dry (unprocessed) and wet (processed) signals using three parallel interpolators: one each for Y, U, and V. At 0%, fully down, the output is the unprocessed input. At 100%, fully up (the default), the output is the fully processed signal. Intermediate positions create a crossfade. The mix is applied after all processing stages but before the bypass mux, so **Bypass** overrides the mix entirely.

---

## Background

### Composite video and the subcarrier

In the early days of color television, engineers faced a seemingly impossible constraint: color information had to be squeezed into the same bandwidth as the existing black-and-white signal, without breaking compatibility with millions of monochrome TVs already in living rooms. The solution was ***frequency-division multiplexing***: encoding color as a high-frequency sinusoidal signal, the ***subcarrier***, layered on top of the luminance waveform. Monochrome sets would simply ignore the high-frequency chroma signal as noise, while color sets could decode it.

In the NTSC system (used in North America and Japan), the subcarrier runs at precisely 3.579545 MHz. The hue of each pixel is encoded as the ***phase angle*** of this sinusoid relative to a reference burst at the start of each scan line. The saturation is encoded as the sinusoid's ***amplitude***. PAL (used in Europe and elsewhere) adds a twist: the subcarrier phase alternates sign on every other line, averaging out phase errors to improve color stability (hence the name ***Phase Alternating Line***.)

### Phase errors and their artifacts

When the phase reference drifts, every color in the image shifts by the same angle. A small drift gives the picture a warm or cool tint; a large drift maps colors to entirely wrong hues. This is exactly what Sub Phase's **Phase Shift** knob does: it rotates the U/V plane by a fixed angle, simulating a miscalibrated burst reference.

Real analog circuits don't drift the same way on every line. Temperature changes, component tolerances, and tape head instability cause the phase to jitter unpredictably. **Phase Wobble** models this jitter by adding a random offset per line, producing the shimmering, unstable tint characteristic of cheap consumer electronics from the 1980s.

### Dot crawl explained

***Dot crawl*** is a cross-color artifact unique to composite video. Because the luminance and chrominance signals share the same wire, sharp transitions in one domain leak into the other. On a composite monitor, you see this as a crawling pattern of colored dots along high-contrast edges: especially black-to-white boundaries. Sub Phase recreates this by modulating the U channel with a periodic alternating pattern at the simulated subcarrier frequency. In NTSC mode the period is 4 pixels; in PAL mode it's 8 pixels with per-line alternation.


---

## Signal Flow

### Signal Flow Notes

The most important interaction in the signal flow is the separation of Y and UV processing paths. The Y channel receives only a brightness offset: it is never rotated or affected by dot crawl or chroma noise. All chromatic distortion happens exclusively in the UV plane. This means Sub Phase can dramatically alter hue and saturation without touching the luminance structure of the image.

The chroma processing chain is sequential: rotation happens first, then burst amplitude scaling, then dot crawl injection, then noise. This order matters because the burst scaling multiplies the already-rotated values, and dot crawl adds to the already-scaled values. Reducing **Color Burst** also reduces the visible intensity of both dot crawl and noise, since their contributions are summed into the amplitude-scaled chroma.

:::note
The dot crawl pattern modulates only the U channel, not V. This is a simplification of real composite artifacts (which affect both luma and chroma) but produces a visually convincing approximation of cross-color interference.
:::


---

## Exercises

These exercises progress from basic hue rotation through analog simulation artifacts to full composite signal degradation. Each exercise builds on the previous one, layering more artifacts into the signal.
### Exercise 1: Hue Rotation and Tinting

![Hue Rotation and Tinting result](/img/instruments/videomancer/subphase/subphase_ex1_s1.png)
*Hue Rotation and Tinting — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Explore the color wheel by rotating hues and adjusting saturation, creating tinted and color-shifted versions of your source video.

#### Key Concepts

- UV rotation shifts all colors simultaneously around the color wheel
- Phase Shift quantizes to 32 discrete angles
- Color Burst controls post-rotation saturation

#### Video Source

A colorful image or video with recognizable, saturated subjects (a face, a bouquet of flowers, or a color bar pattern.)

#### Steps

1. **First rotation**: Slowly turn **Phase Shift** (Knob 1) clockwise. Watch every color in the image shift simultaneously: skin tones turn green, blue skies become orange, and red objects shift to purple.
2. **Complementary colors**: Set Phase Shift to approximately 180°. The image is now displayed in complementary colors (every hue is replaced by its opposite on the color wheel.)
3. **Desaturation**: Slowly turn **Color Burst** (Knob 4) counterclockwise from its default midpoint. Colors fade as if the TV's color control is being turned down. At zero, the image is monochrome.
4. **Oversaturation**: Turn Color Burst clockwise past the midpoint. Colors become vivid and oversaturated, bleeding beyond their natural boundaries.
5. **Combine**: Set Phase Shift to about 90° and Color Burst to about 75%. The shifted, saturated palette produces an otherworldly color scheme.

#### Settings

| Control | Value |
|---------|-------|
| Phase Shift | ~90° |
| Phase Wobble | 0% |
| Dot Crawl | 0% |
| Color Burst | ~75% |
| Chroma Noise | 0% |
| Brightness | 50% |
| Standard | NTSC |
| Crawl Anim | Animate |
| Tint Lock | Off |
| Chroma Kill | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Vintage Television Simulation

![Vintage Television Simulation result](/img/instruments/videomancer/subphase/subphase_ex2_s1.png)
*Vintage Television Simulation — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Simulate the look of a slightly mistuned analog television, complete with wobbly tints and crawling dot patterns along edges.

#### Key Concepts

- Phase wobble simulates per-line color instability
- Dot crawl recreates subcarrier interference patterns
- NTSC and PAL have different dot crawl periods

#### Video Source

Recorded footage of a scene with strong vertical edges and areas of high contrast: text on a dark background, window frames, or architectural details work well.

#### Steps

1. **Subtle tint**: Set **Phase Shift** (Knob 1) to about 15°–30° for a gentle warm or cool color bias, as if the TV's tint control is slightly off.
2. **Line wobble**: Raise **Phase Wobble** (Knob 2) to about 30%. Each scan line now wobbles independently, creating a shimmering color instability.
3. **Dot crawl**: Increase **Dot Crawl** (Knob 3) to about 50% with **Standard** (Switch 7) set to **NTSC**. A fine crawling pattern appears on high-contrast edges.
4. **Animate**: Confirm **Crawl Anim** (Switch 8) is set to **Animate**. Watch the dots march across edges frame by frame.
5. **PAL comparison**: Flip **Standard** to **PAL**. The dot pattern becomes wider (period-8) and alternates per line, creating a different texture. Flip back to NTSC to compare.
6. **Brightness adjustment**: Slightly reduce **Brightness** (Knob 6) to simulate a dim picture tube.

#### Settings

| Control | Value |
|---------|-------|
| Phase Shift | ~20° |
| Phase Wobble | ~30% |
| Dot Crawl | ~50% |
| Color Burst | 50% |
| Chroma Noise | 0% |
| Brightness | ~40% |
| Standard | NTSC |
| Crawl Anim | Animate |
| Tint Lock | Off |
| Chroma Kill | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Degraded Signal — Worn Tape

![Degraded Signal — Worn Tape result](/img/instruments/videomancer/subphase/subphase_ex3_s1.png)
*Degraded Signal — Worn Tape — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Combine all artifacts to simulate a heavily degraded composite signal: a worn VHS tape played back on a consumer VCR with a bad RF connection.

#### Key Concepts

- Chroma noise simulates tape head instability
- Layering multiple artifacts creates convincing analog degradation
- Mix fader allows blending between clean and degraded signals

#### Video Source

Any footage with a mix of saturated color, skin tones, and motion (a home movie aesthetic suits this exercise perfectly.)

#### Steps

1. **Base tint**: Set **Phase Shift** (Knob 1) to about 10° for a slight color drift.
2. **Heavy wobble**: Increase **Phase Wobble** (Knob 2) to about 60%. Lines shimmer dramatically.
3. **Moderate dot crawl**: Set **Dot Crawl** (Knob 3) to about 40%.
4. **Weak color**: Reduce **Color Burst** (Knob 4) to about 35%, simulating a fading color burst reference.
5. **Tape noise**: Raise **Chroma Noise** (Knob 5) to about 50%. The image develops a flickering chromatic grain.
6. **Dim picture**: Lower **Brightness** (Knob 6) to about 35%.
7. **Partial mix**: Pull the **Mix** fader (Fader 12) to about 70%. The degradation blends with the clean signal, as if the tape is partially tracking.
8. **Compare**: Toggle **Bypass** (Switch 11) to see the clean original beside the degraded version.

#### Settings

| Control | Value |
|---------|-------|
| Phase Shift | ~10° |
| Phase Wobble | ~60% |
| Dot Crawl | ~40% |
| Color Burst | ~35% |
| Chroma Noise | ~50% |
| Brightness | ~35% |
| Standard | NTSC |
| Crawl Anim | Animate |
| Tint Lock | Off |
| Chroma Kill | Off |
| Bypass | Off |
| Mix | ~70% |

---
## Glossary

- **Chroma**: The color component of a video signal, encoded as U and V values in YUV color space, representing hue and saturation independently of brightness.

- **Color Burst**: A short reference sinusoid transmitted at the start of each scan line in composite video, used by the receiver to lock onto the subcarrier phase for accurate color decoding.

- **Composite Video**: An analog video format that combines luminance, chrominance, and sync information into a single signal, used by NTSC, PAL, and SECAM television standards.

- **Dot Crawl**: A visible artifact in composite video where the subcarrier frequency creates a crawling pattern of colored dots along high-contrast edges, caused by incomplete separation of luma and chroma.

- **LFSR**: Linear Feedback Shift Register; a digital circuit that produces a pseudo-random sequence of bits by feeding back a combination of its internal state bits.

- **Luma**: The brightness component (Y) of a YUV video signal, representing perceived lightness independently of color.

- **NTSC**: National Television System Committee; the analog color television standard used in North America and Japan, with a 3.58 MHz subcarrier.

- **PAL**: Phase Alternating Line; the analog color television standard used in Europe and much of the world, which alternates the subcarrier phase on every other scan line to reduce hue errors.

- **Rotation Matrix**: A 2×2 matrix that rotates a two-dimensional vector (here, U and V) by an angle, using sine and cosine coefficients.

- **Subcarrier**: A secondary carrier signal modulated onto the main video signal to encode color information; its phase determines hue and its amplitude determines saturation.

---
