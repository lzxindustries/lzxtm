---
draft: true
sidebar_position: 4
slug: /instruments/videomancer/pinwheel
title: "Pinwheel"
---

import pinwheel_hero from '/img/instruments/videomancer/pinwheel/pinwheel_hero.png';
import pinwheel_control_panel from '/img/instruments/videomancer/pinwheel/pinwheel_control_panel.png';
import pinwheel_hue_rotation from '/img/instruments/videomancer/pinwheel/pinwheel_hue_rotation.png';
import pinwheel_exercise2_result from '/img/instruments/videomancer/pinwheel/pinwheel_exercise2_result.png';
import pinwheel_exercise3_result from '/img/instruments/videomancer/pinwheel/pinwheel_exercise3_result.png';

# Pinwheel

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={pinwheel_hero} alt="Pinwheel processed video output showing rainbow hue rotation, colorization, and bit-crushing on a natural source"/>

*Pinwheel rotates hue through the color spectrum using luminance as a compass — brightness becomes color, and video becomes a rotating palette of chromatic texture.*

---

## Overview

Color in digital video is encoded as numbers. In YUV color space, brightness (Y) travels separately from color (U and V). Most video processors treat these channels as independent — adjust brightness here, adjust color there. Pinwheel deliberately crosses the boundary. It uses the luminance channel to drive hue rotation, mapping brightness gradients into sweeping rainbow spectra.

The program chains five processing concepts together — hue rotation via sine/cosine lookup tables, luminance-to-hue modulation, brightness and gain adjustment, chroma colorization, and bitwise crushing. The name evokes a spinning color wheel: as you sweep the Hue control, colors rotate through the full spectrum. When the Luma to Hue control is engaged, the rotation becomes *adaptive* — different brightness levels map to different hue angles, and a simple grayscale gradient becomes a rainbow.

At moderate settings, Pinwheel acts as a precise hue rotator and color corrector. At extreme settings with bit-crushing engaged, it produces psychedelic glitch textures where color and brightness are shattered into hard-edged digital fragments.

---

## Background

### What Is Hue Rotation?

In video color space, hue is the *angle* of the color vector in the UV plane. Red, yellow, green, cyan, blue, and magenta are arranged around a circle at 0°, 60°, 120°, 180°, 240°, and 300° respectively. **Hue rotation** spins all colors around this circle by a fixed angle — at 180°, every color maps to its complement (red becomes cyan, blue becomes yellow). Pinwheel implements hue rotation using a full 10-bit sine/cosine lookup table, applying the standard 2D rotation matrix to the U and V components:

$$U' = U \cos\theta - V \sin\theta$$
$$V' = U \sin\theta + V \cos\theta$$

Because Pinwheel uses a 10-bit LUT with 1024 entries, the rotation is continuous and smooth through any angle.

### What Is Luminance-to-Hue Modulation?

The Luma to Hue control makes the rotation angle *dependent on brightness*. Instead of rotating all pixels by the same angle, each pixel gets a rotation proportional to its Y value: $\theta = Y \times k + \theta_0$, where $k$ is the modulation depth and $\theta_0$ is the base Hue setting. The result: brightness gradients become color gradients. A smooth grayscale ramp becomes a smooth rainbow. Edges between bright and dark areas become edges between different hues. This is Pinwheel's signature effect — turning tonal structure into chromatic structure.

### What Is Colorization?

The Colorize toggle replaces the input's chrominance with neutral (U = V = midpoint), effectively converting the input to grayscale *before* hue rotation. This means the output color comes entirely from the Hue and Luma to Hue controls rather than from the original source color. The source provides only the luminance "skeleton" — the brightness pattern — and Pinwheel paints it with a new palette. Without Colorize, the original colors are *rotated*; with Colorize, they are *replaced*.

### What Is Bit-Crushing?

Bit-crushing applies a binary mask to the output values using AND or XOR operations. The **Posterize** control (Knob 5) masks the Y channel, and the **Chroma Crush** fader (Fader 12) masks the U and V channels. The mask zeros out the lower bits of each value, quantizing the signal into discrete levels — similar to reducing bit depth. The **Crush Mode** toggle (Switch 10) selects between AND (which cleanly zeros bits, producing smooth staircase quantization) and XOR (which flips bits, producing chaotic, glitch-like value scrambling). AND crushing is predictable; XOR crushing is deterministic but visually wild.

---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y Channel ──────────────────────────────────────────────────
│   │
│   ├─ 1. Proc Amp               (Luma Gain × Y + Brightness offset)
│   └─ 2. Output Logic            Y AND/XOR Posterize mask, optional invert
│
├── U/V Channels ───────────────────────────────────────────────
│   │
│   ├─ 1. Colorize               (optional: replace UV with midpoint)
│   ├─ 2. Hue Rotation           (sin/cos LUT, angle = Y × LumaToHue + Hue)
│   ├─ 3. Saturation Scaling     (proc amp: UV around midpoint)
│   └─ 4. Output Logic           UV AND/XOR ChromaCrush mask, optional invert
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Pass-through (hsync, vsync, field, avid)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

Two key interactions to notice:

1. **Luminance drives chrominance**: The hue rotation angle is computed from the *processed* Y channel (after gain and brightness adjustment). This means Luma Gain and Brightness controls don't just affect brightness — they also change the hue rotation mapping, creating a coupled luminance-chrominance creative space.

2. **AND vs. XOR crushing**: The output logic uses either AND-masking (clean quantization, like reducing bit depth) or XOR-masking (chaotic value scrambling). The choice profoundly affects the visual character: AND is structured and predictable; XOR is glitchy and surprising.

---

## Parameter Reference

<img src={pinwheel_control_panel} alt="Videomancer front panel with Pinwheel loaded, controls annotated"/>

*Videomancer's front panel with Pinwheel active. Knobs 1–6, Switches 7–11, and Fader 12 are labeled with their Pinwheel functions.*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Hue
| Property | Value |
|----------|-------|
| Range | 0.0% – 200.0% |
| Default | 100.0% (center) |
| Suffix | % |

Controls the **base hue rotation angle**. At center (100%), the rotation angle is at a midpoint. Sweeping from 0% to 200% rotates through the full color spectrum and beyond. This parameter sets the $\theta_0$ offset — the starting point for all hue rotation. If Luma to Hue is at zero modulation, this control alone determines the uniform hue shift applied to the entire image.

Sweep this control slowly to watch every color in the image rotate through the spectrum: reds become yellows become greens become cyans become blues become magentas and back to reds.

---

#### Knob 2 — Saturation
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% (center) |
| Suffix | % |

Controls the **color saturation** after hue rotation. This is a proc amp gain applied to U and V around their midpoint (512). At center, saturation is at a moderate level. Fully CCW, the color is reduced toward monochrome. Fully CW, color is boosted.

Because saturation is applied *after* hue rotation, it scales the rotated colors rather than the originals. This means you can rotate to a new hue angle and then control how vivid the result is.

---

#### Knob 3 — Brightness
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% (center) |
| Suffix | % |

Controls the **brightness offset** applied to the Y channel via the proc amp stage. At center, the brightness is unmodified. Below center, the image darkens. Above center, the image brightens.

Because the Y channel drives the hue rotation angle (via Luma to Hue), changing Brightness also shifts the hue mapping — brightening the image rotates the Luma-to-Hue mapping forward, darkening it rotates the mapping backward. This is an important interaction: Brightness is not purely a luminance control in Pinwheel — it's also a chromatic offset when Luma to Hue is active.

---

#### Knob 4 — Luma to Hue
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% (center) |
| Suffix | % |

Controls how strongly **input luminance modulates the hue rotation angle**. This is Pinwheel's signature parameter. At center (50%), there is a moderate correlation between brightness and hue — bright areas rotate further than dark areas. Below center, less modulation. Above center, strong modulation — a grayscale ramp becomes a full rainbow spectrum.

<img src={pinwheel_hue_rotation} alt="Hue rotation diagram showing how luminance maps to rotation angle across the color spectrum"/>

*Luminance-to-hue modulation: as the modulation depth increases, brightness gradients map to wider arcs of the color wheel, turning tonal structure into chromatic structure.*

With Colorize enabled, Luma to Hue controls the *entire* chromatic output — the source provides the brightness structure, and this control determines how that structure maps to color. Without Colorize, the original colors are rotated by a luminance-dependent amount — existing colors shift and blend in luminance-adaptive patterns.

---

#### Knob 5 — Posterize
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% (fully CW) |
| Suffix | % |

Controls the **Y channel bit-crushing depth**. At 100% (default), the mask is all 1s — full resolution, no crushing. As you decrease toward 0%, progressively more low-order bits are masked out, quantizing the Y output into fewer discrete levels.

The visual effect depends on **Crush Mode** (Switch 10):
- **Clean (AND)**: Smooth staircase quantization — brightness levels snap to discrete steps, similar to posterization.
- **Glitch (XOR)**: Chaotic value scrambling — the XOR of the value with the mask creates unpredictable brightness inversions and digital glitch textures.

---

#### Knob 6 — Luma Gain
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% (center) |
| Suffix | % |

Controls the **luminance gain** (multiplication factor) applied to the Y channel in the proc amp stage. At center, gain is at a moderate level. Below center, the Y channel is attenuated (lower contrast). Above center, the Y channel is amplified (higher contrast, with clipping at extremes).

Like Brightness, Luma Gain also affects the hue rotation mapping because a gained-up Y channel produces a wider range of rotation angles. Increasing gain stretches the luminance range, which stretches the Luma-to-Hue rainbow across more of the color spectrum.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Colorize** | Original UV preserved | UV replaced with midpoint (grayscale input) |
| **8 — Luma Invert** | Normal luminance | Luminance inverted (negative) |
| **9 — Chroma Invert** | Normal chrominance | Chroma inverted (complementary colors) |
| **10 — Crush Mode** | Clean (AND masking) | Glitch (XOR masking) |
| **11 — Bypass** | Processing active | Bypass (signal passes unmodified) |

**Colorize** replaces the input chrominance (U and V) with the neutral midpoint *before* hue rotation. The input effectively becomes grayscale, and all output color comes from the Hue, Luma to Hue, and Saturation controls. This is essential for creating pure luminance-to-color mappings — the source provides only structure, Pinwheel provides the palette. Without Colorize, the hue rotation operates on the original colors, producing shifted and blended hues.

**Luma Invert** flips the Y channel (bitwise complement). Since Y drives the hue rotation angle, inverting luminance also inverts the color mapping — dark areas get the hue angles that bright areas previously had. The visual effect is a negative image where the color palette is also reversed.

**Chroma Invert** inverts the U and V channels after all processing, mapping every color to its complement. Red becomes cyan, blue becomes yellow, green becomes magenta. This is independent of Luma Invert — you can invert luminance, chroma, both, or neither.

**Crush Mode** switches the output masking operation:
- **Clean (AND)**: `output = value AND mask`. Zeros out bits, producing clean quantization steps. Predictable, structured reduction.
- **Glitch (XOR)**: `output = value XOR mask`. Flips bits, producing chaotic value remapping. The same mask value produces completely different visual results in XOR vs. AND mode.

**Bypass** routes the input signal directly to the output, skipping all processing.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Chroma Crush
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% (fully up) |
| Suffix | % |

Controls the **UV channel bit-crushing depth**, operating identically to the Posterize control (Knob 5) but on the chrominance channels. At 100% (default), full chroma resolution. As you lower the fader, more low-order bits of U and V are masked out.

The Crush Mode toggle (Switch 10) applies to both Y (Posterize) and UV (Chroma Crush) masking simultaneously — you cannot use AND for luma and XOR for chroma or vice versa.

Chroma Crush and Posterize (Knob 5) are independent: you can crush the color while leaving brightness intact, or crush brightness while leaving color intact, or crush both. Crushing chroma with Clean mode creates banded, posterized color transitions. Crushing chroma with Glitch mode creates psychedelic color scrambling.

---

## Guided Exercises

### Exercise 1: Luminance Rainbow

**Source**: A live camera feed or recorded footage with a wide range of brightness — faces with highlights and shadows, landscapes with sky and ground, or any high-contrast subject.

**Objective**: Learn how Pinwheel maps brightness to color using hue rotation and luminance modulation.

1. **Initialize**: Load Pinwheel with all defaults. The image should appear with moderate color processing.

2. **Enable Colorize**: Flip **Colorize** (Switch 7) to On. The image loses its original color and becomes a tinted monochrome — Pinwheel is now the sole source of color.

3. **Engage Luma to Hue**: Slowly sweep **Luma to Hue** (Knob 4) from center toward fully CW. Watch the monochrome image develop into a rainbow — bright areas take on one hue, mid-tones another, and dark areas a third. At maximum modulation, the full brightness range maps to a wide arc of the color spectrum.

4. **Rotate the palette**: While Luma to Hue is at a high value, slowly sweep **Hue** (Knob 1) from 0% to 200%. The entire rainbow palette rotates — the hues shift uniformly, sliding the color mapping around the color wheel. Regions that were red become green, regions that were green become blue, and so on.

5. **Adjust saturation**: With a compelling rainbow established, sweep **Saturation** (Knob 2). Watch the rainbow intensify (CW) or fade toward monochrome (CCW). Find the sweet spot where the colors are vivid without clipping.

6. **Brightness interaction**: Sweep **Brightness** (Knob 3). Notice that changing brightness also shifts the rainbow mapping — as you brighten the image, the Luma-to-Hue correlation shifts because the Y values feeding the rotation angle have changed.

:::tip
Colorize removes original color. Luma to Hue maps brightness to hue angle. Hue rotates the mapping. Brightness offsets the mapping. Saturation controls vividness.
:::

---

### Exercise 2: Color Corrector to Glitch Machine

<img src={pinwheel_exercise2_result} alt="Pinwheel transitioning from subtle hue rotation to wild XOR glitch textures"/>

*Pinwheel with moderate hue rotation and XOR crushing — the color spectrum is rotated and then shattered into digital fragments.*

**Source**: Colorful footage — nature, graphics, or anything with a variety of hues.

**Objective**: Experience the range from subtle color correction to extreme glitch, controlled by Crush Mode and the crushing depth.

1. **Start subtle**: Load Pinwheel defaults. Disable Colorize. Sweep **Hue** slowly — you are performing basic hue rotation, a standard color correction operation. Find a hue angle that creates a color palette you like.

2. **Add gain**: Set **Luma Gain** (Knob 6) slightly above center. The contrast increases, and because gain affects the Luma-to-Hue mapping, the color palette shifts slightly with gain.

3. **Begin crushing**: With the image at a pleasing hue rotation, slowly lower **Posterize** (Knob 5) from 100% toward 0%. In Clean mode (default), the brightness quantizes smoothly into steps. The image develops a posterized look — flat tonal regions with hard edges.

4. **Switch to Glitch**: Flip **Crush Mode** (Switch 10) to Glitch. The same Posterize position now produces a completely different result — the XOR masking scrambles brightness values instead of quantizing them. The image becomes chaotic and digital.

5. **Add Chroma Crush**: Lower **Chroma Crush** (Fader 12) from 100% toward 50%. The color channels are now also XOR-crushed — colors fracture into unexpected hues. The combination of hue rotation and XOR crushing creates psychedelic, glitch-art palettes.

6. **Compare modes**: Toggle Crush Mode back and forth between Clean and Glitch while watching the output. Same controls, completely different aesthetic: one is structured and graphic, the other is chaotic and digital.

:::tip
Hue rotation is the foundation. Posterize and Chroma Crush are independent bit-crushers. Crush Mode (AND vs. XOR) is the most transformative single toggle — it fundamentally changes the character of all crushing.
:::

---

### Exercise 3: Psychedelic Colorizer

<img src={pinwheel_exercise3_result} alt="Extreme Pinwheel processing — full rainbow mapping with chroma inversion and bit-crushing creating a hallucinatory color field"/>

*Pinwheel at full rainbow modulation with Chroma Invert and Glitch crushing — the source image is transformed into a psychedelic color field.*

**Source**: Any footage — faces, landscapes, abstract patterns, or live camera.

**Objective**: Combine all of Pinwheel's capabilities into a maximally expressive color processor.

1. **Colorize and modulate**: Enable **Colorize** (Switch 7). Set **Luma to Hue** to about 80%. Set **Hue** to about 60%. A strong rainbow mapping is established.

2. **Boost saturation and gain**: Set **Saturation** to about 70%. Set **Luma Gain** to about 65%. Colors are vivid and the luminance range is stretched.

3. **Invert chroma**: Flip **Chroma Invert** (Switch 9) to On. The rainbow palette shifts to its complement — every color in the mapping is replaced by the color opposite it on the color wheel. Toggle Chroma Invert on and off to see the two complementary versions of the same rainbow.

4. **Invert luma**: Flip **Luma Invert** (Switch 8) to On. The brightness is negated, which also reverses the Luma-to-Hue mapping — the color assignments for bright and dark regions swap. With both inversions active, the image is a doubly-transformed version of itself.

5. **Add Glitch crushing**: Flip **Crush Mode** (Switch 10) to Glitch. Lower **Posterize** (Knob 5) to about 40% and **Chroma Crush** (Fader 12) to about 50%. The hue-rotated, inverted image is now shattered by XOR masking — colors fragment into hard-edged digital shards.

6. **Animate**: Slowly sweep **Hue** (Knob 1) while everything else is engaged. The entire color field rotates — patches of color cycle through the spectrum, creating a hallucinatory, ever-shifting chromatic landscape. Because Luma to Hue ties the rotation to brightness, moving subjects create trails of shifting color as they cross different brightness zones.

:::tip
Pinwheel's full expressive range spans from precise hue rotation (one control) to psychedelic glitch texture (all controls). Colorize + Luma to Hue creates the rainbow mapping. Inversions flip the mapping. Crush Mode (XOR) shatters it. Hue rotation animates it.
:::

---

## Tips

- **Colorize is the key to rainbow mapping**: Without Colorize, Pinwheel rotates the existing colors. With Colorize, it maps brightness to color from scratch. For the classic luminance-rainbow effect, start with Colorize On.

- **Brightness and Gain affect color, not just luminance**: Because Y drives the hue rotation angle, Brightness (offset) and Luma Gain (scale) shift and stretch the color mapping. Think of them as chromatic controls when Luma to Hue is active.

- **AND vs. XOR is the biggest toggle**: Crush Mode changes the fundamental character of all bit-crushing. AND produces clean, structured quantization. XOR produces chaotic, glitch-art scrambling. Try both with the same Posterize and Chroma Crush settings — the results are dramatically different.

- **Independent Y and UV crushing**: Posterize (Knob 5) crushes only Y. Chroma Crush (Fader 12) crushes only U and V. You can have smooth brightness with crushed color (low Chroma Crush, full Posterize) or crushed brightness with smooth color (low Posterize, full Chroma Crush). Both combinations have distinct visual characters.

- **Chroma Invert complements the palette**: Toggle Switch 9 to instantly flip every color to its complement without changing the luminance structure or the modulation depth. This is a fast way to explore alternative color palettes from the same Luma-to-Hue mapping.

- **Feedback loops with hue rotation**: If Videomancer's output feeds back to its input, each pass through Pinwheel rotates the hue further. With a fixed Hue angle of, say, 30°, each feedback iteration advances the colors by 30°, creating a cycling chromatic cascade that evolves in real time.

- **Bypass for A/B comparison**: Switch 11 (Bypass) instantly shows the unprocessed signal. Use it to compare Pinwheel's output against the original. Toggle rapidly for before/after evaluation.
