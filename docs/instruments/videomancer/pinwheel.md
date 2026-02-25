---
draft: false
sidebar_position: 4
slug: /instruments/videomancer/pinwheel
title: "Pinwheel"
---

import pinwheel_hero from '/img/instruments/videomancer/pinwheel/pinwheel_hero.png';
import pinwheel_before_after from '/img/instruments/videomancer/pinwheel/pinwheel_before_after.png';
import pinwheel_control_panel from '/img/instruments/videomancer/pinwheel/pinwheel_control_panel.png';
import pinwheel_exercise1_result from '/img/instruments/videomancer/pinwheel/pinwheel_exercise1_result.png';
import pinwheel_exercise2_result from '/img/instruments/videomancer/pinwheel/pinwheel_exercise2_result.png';
import pinwheel_exercise3_result from '/img/instruments/videomancer/pinwheel/pinwheel_exercise3_result.png';

# Pinwheel

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={pinwheel_hero} alt="Pinwheel mapping brightness gradients into a full rainbow spectrum using luminance-to-hue modulation"/>

<img src={pinwheel_before_after} alt="Left: unprocessed source. Right: Pinwheel applied"/>

*Left: unprocessed source. Right: Pinwheel applied.*

**Source images used in this guide:**
- **1**. kodim04.png — Portrait of girl in red — wide brightness range
- **2**. peppers_512.png — Peppers — saturated primary colors
- **3**. kodim23.png — Parrots — bold colors and high contrast

<details>
<summary>Hero image settings</summary>

| Control | Value |
|---------|-------|
| Colorize | On |
| Luma to Hue | ~75% |
| Hue | ~80% |
| Saturation | ~65% |
| Brightness | center |
| Luma Gain | ~55% |
| Posterize | 100% (no crushing) |
| Crush Mode | Clean (AND) |
| All inversions | Off |

</details>

---

## Overview

Color in digital video is encoded as numbers. In YUV color space, brightness (Y) travels separately from color (U and V). Most video processors treat these channels as independent — adjust brightness here, adjust color there. Pinwheel deliberately crosses the boundary. It uses the luminance channel to drive hue rotation, mapping brightness gradients into sweeping rainbow spectra.

The program chains five processing concepts together — hue rotation via sine/cosine lookup tables, luminance-to-hue modulation, brightness and gain adjustment, chroma colorization, and bitwise crushing. The name evokes a spinning color wheel: as you sweep the Hue control, colors rotate through the full spectrum. When the Luma to Hue control is engaged, the rotation becomes *adaptive* — different brightness levels map to different hue angles, and a simple grayscale gradient becomes a rainbow.

At moderate settings, Pinwheel acts as a precise hue rotator and color corrector. At extreme settings with bit-crushing engaged, it produces psychedelic glitch textures where color and brightness are shattered into hard-edged digital fragments.

---

## Background

### What Is Hue Rotation?

In video color space, hue is the *angle* of the color vector in the UV plane. Red, yellow, green, cyan, blue, and magenta are arranged around a circle at 0°, 60°, 120°, 180°, 240°, and 300° respectively. **Hue rotation** spins all colors around this circle by a fixed angle — at 180°, every color maps to its complement. Pinwheel implements hue rotation using a full 10-bit sine/cosine lookup table, applying the standard 2D rotation matrix to the U and V components:

$U' = U \cos\theta - V \sin\theta$

$V' = U \sin\theta + V \cos\theta$

### What Is Luminance-to-Hue Modulation?

The Luma to Hue control makes the rotation angle *dependent on brightness*. Instead of rotating all pixels by the same angle, each pixel gets a rotation proportional to its Y value: $\theta = Y \times k + \theta_0$, where $k$ is the modulation depth and $\theta_0$ is the base Hue setting. The result: brightness gradients become color gradients. A smooth grayscale ramp becomes a smooth rainbow. Edges between bright and dark areas become edges between different hues. This is Pinwheel's signature effect — turning tonal structure into chromatic structure.

### What Is Colorization?

The Colorize toggle replaces the input's chrominance with neutral (U = V = midpoint), effectively converting the input to grayscale *before* hue rotation. This means the output color comes entirely from the Hue and Luma to Hue controls rather than from the original source color. Without Colorize, the original colors are *rotated*; with Colorize, they are *replaced*.

### What Is Bit-Crushing?

Bit-crushing applies a binary mask to the output values using AND or XOR operations. The **Posterize** control (Knob 5) masks the Y channel, and the **Chroma Crush** fader (Fader 12) masks the U and V channels. **Crush Mode** (Switch 10): AND cleanly zeros bits (smooth staircase quantization), XOR flips bits (chaotic, glitch-like value scrambling). AND crushing is predictable; XOR crushing is deterministic but visually wild.

---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y Channel ──────────────────────────────────────────────────
│   ├─ 1. Proc Amp               (Luma Gain × Y + Brightness offset)
│   └─ 2. Output Logic            Y AND/XOR Posterize mask, optional invert
│
├── U/V Channels ───────────────────────────────────────────────
│   ├─ 1. Colorize               (optional: replace UV with midpoint)
│   ├─ 2. Hue Rotation           (sin/cos LUT, angle = Y × LumaToHue + Hue)
│   ├─ 3. Saturation Scaling     (proc amp: UV around midpoint)
│   └─ 4. Output Logic           UV AND/XOR ChromaCrush mask, optional invert
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Pass-through
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

Two key interactions: (1) **Luminance drives chrominance**: The hue rotation angle is computed from the *processed* Y channel (after Luma Gain and Brightness). This means the Y-channel proc amp controls also change the hue rotation mapping, creating a coupled luminance-chrominance creative space. (2) **AND vs. XOR crushing**: AND is structured and predictable — it produces smooth staircase quantization. XOR is glitchy and surprising — it flips bits in a deterministic but visually chaotic pattern.

---

## Parameter Reference

<img src={pinwheel_control_panel} alt="Videomancer front panel with Pinwheel loaded, controls annotated"/>

*Videomancer's front panel with Pinwheel active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Hue
| Property | Value |
|----------|-------|
| Range | 0.0% – 200.0% |
| Default | 100.1% |
| Suffix | % |

Base hue rotation angle. Sweeping this control rotates all colors through the spectrum — a full turn takes every color through red, yellow, green, cyan, blue, magenta, and back to red. This sets $\theta_0$ in the rotation equation. When Luma to Hue is at zero, all pixels rotate by the same angle. When Luma to Hue is active, this control shifts the *starting point* of the brightness-to-color mapping.

---

#### Knob 2 — Saturation
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Color saturation *after* hue rotation. This scales the rotated U and V values around the neutral midpoint. Important: Saturation operates on the post-rotation chrominance, not the original colors. At 0%, the output is monochrome regardless of hue rotation or Luma to Hue settings. At higher values, the rotated colors become increasingly vivid.

---

#### Knob 3 — Brightness
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Brightness offset via the Y-channel proc amp. Because the Y value drives hue rotation (when Luma to Hue is active), changing Brightness also shifts the hue mapping — it acts as a *chromatic offset*. Increasing brightness shifts the entire rainbow palette toward one end; decreasing shifts it toward the other.

---

#### Knob 4 — Luma to Hue
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Pinwheel's signature parameter. Controls how strongly input luminance modulates the hue rotation angle. At 0%, all pixels rotate by the same angle (set by Hue). As you increase this control, different brightness levels get different rotation angles, and a grayscale gradient becomes a full rainbow spectrum. With Colorize enabled, this control determines the *entire* chromatic output — the color palette is built entirely from brightness structure.

---

#### Knob 5 — Posterize
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Y channel bit-crushing depth. The crushing mode (AND or XOR) is set by Switch 10. In **Clean** (AND) mode: higher values progressively zero the least significant bits, creating a smooth staircase quantization. In **Glitch** (XOR) mode: higher values flip bits, producing chaotic, nonlinear value scrambling. The effect on the Y channel is visible as brightness quantization or brightness scrambling.

---

#### Knob 6 — Luma Gain
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Luminance gain via the Y-channel proc amp. Because Y drives hue rotation, increasing Luma Gain also stretches the brightness range that feeds the rotation angle — the rainbow maps across more of the color spectrum. Reducing gain compresses the Y range, narrowing the rainbow. This is a second-order chromatic control that couples brightness to color.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Colorize** | Off | On |
| **8 — Luma Invert** | Off | On |
| **9 — Chroma Invert** | Off | On |
| **10 — Crush Mode** | Clean | Glitch |
| **11 — Bypass** | Off | On |

The five toggle switches control independent binary processing options. Colorize (Switch 7) dramatically changes the program's character by removing original chrominance. Luma Invert (Switch 8) and Chroma Invert (Switch 9) are independent inversions that interact with the hue rotation pipeline. Crush Mode (Switch 10) fundamentally changes the character of bit-crushing. Bypass (Switch 11) provides instant A/B comparison.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Chroma Crush
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

UV channel bit-crushing depth. Independent of Posterize (Knob 5), which crushes the Y channel. The crushing mode (AND or XOR) follows Switch 10. At 100%, no crushing — full color resolution. As you lower the fader, color values are progressively masked. In AND mode, this produces smooth color quantization. In XOR mode, this produces psychedelic color scrambling. You can crush color while leaving brightness intact (high Posterize, low Chroma Crush) or vice versa.

---

## Guided Exercises

These exercises progress from subtle color correction to extreme psychedelic processing. Pinwheel's range is enormous — the same controls produce gentle hue shifts at one end and total chromatic chaos at the other.

### Exercise 1: Luminance Rainbow

<img src={pinwheel_exercise1_result} alt="Luminance Rainbow — simulated result across source images"/>

*Luminance Rainbow — simulated result across source images.*

**Source**: Footage with a wide range of brightness — landscapes, portraits, or gradient test patterns.

**Objective**: Learn luminance-to-color mapping and understand how brightness becomes color.

1. **Colorize**: Enable the Colorize toggle (Switch 7). The input chrominance is replaced with neutral — the image is now effectively grayscale.
2. **Activate modulation**: Slowly increase Luma to Hue (Knob 4) from center toward maximum. Watch the monochrome image develop into a rainbow as different brightness levels map to different hue angles.
3. **Rotate the palette**: Sweep the Hue knob (Knob 1). The entire rainbow palette rotates — the same brightness gradient maps to a different set of colors.
4. **Saturation**: Adjust Saturation (Knob 2) to control color intensity. At 0%, the image returns to monochrome regardless of hue rotation.
5. **Brightness interaction**: Change Brightness (Knob 3). Notice that the rainbow palette shifts — brightness acts as a chromatic offset when Luma to Hue is active.

:::tip
Colorize removes original color allowing pure luminance-to-hue mapping, Luma to Hue controls modulation depth, Hue rotates the palette, Brightness acts as a chromatic offset.
:::

---

### Exercise 2: Color Corrector to Glitch Machine

<img src={pinwheel_exercise2_result} alt="Color Corrector to Glitch Machine — simulated result across source images"/>

*Color Corrector to Glitch Machine — simulated result across source images.*

**Source**: Colorful footage — flowers, fruit, painted surfaces, or video art.

**Objective**: Experience the full range from subtle color correction to extreme glitch texture.

1. **Subtle correction**: Start with a small hue rotation (Knob 1 near center). Observe gentle shifts in the color palette — this is Pinwheel as a color corrector.
2. **Add gain**: Increase Luma Gain (Knob 6). The brightness range stretches, and if Luma to Hue is active, the rainbow palette expands.
3. **Clean crushing**: Begin increasing Posterize (Knob 5) in Clean mode (Switch 10 Off/AND). Watch brightness quantize into smooth staircase levels.
4. **Glitch mode**: Switch Crush Mode (Switch 10) to Glitch (XOR). The same Posterize setting now produces chaotic, scrambled brightness.
5. **Color crushing**: Lower the Chroma Crush fader (Fader 12). In XOR mode, colors explode into psychedelic fragments.
6. **Compare**: Toggle Crush Mode back and forth. AND is structured and predictable. XOR is chaotic and surprising. Same controls, fundamentally different character.

:::tip
AND crushing is structured staircase quantization, XOR crushing is chaotic bit scrambling, Posterize crushes Y (brightness) and Chroma Crush crushes UV (color) independently.
:::

---

### Exercise 3: Psychedelic Colorizer

<img src={pinwheel_exercise3_result} alt="Psychedelic Colorizer — simulated result across source images"/>

*Psychedelic Colorizer — simulated result across source images.*

**Source**: Any footage — the more varied, the more interesting.

**Objective**: Combine all capabilities into a maximally expressive color processor.

1. **Foundation**: Enable Colorize. Set Luma to Hue to ~80%, Hue to ~60%.
2. **Intensity**: Boost Saturation to ~70–80%. Increase Luma Gain.
3. **Complement**: Toggle Chroma Invert (Switch 9) for a complementary color palette.
4. **Total negative**: Toggle Luma Invert (Switch 8) for reversed brightness mapping (which also reverses the hue mapping).
5. **Crush both channels**: Set Crush Mode to Glitch (XOR). Increase Posterize to ~40%, lower Chroma Crush to ~50%.
6. **Animate**: Slowly sweep the Hue knob. The entire psychedelic palette rotates through the spectrum — a hallucinatory, ever-shifting chromatic landscape.

:::tip
Colorize + Luma to Hue creates pure brightness-to-color mapping, inversion and crushing compound the effect, sweeping Hue animates the entire palette.
:::

---

## Tips

- **Colorize is the key to rainbow mapping**: Without Colorize, Pinwheel rotates existing colors and the output depends on the source chrominance. With Colorize, it maps brightness to color from scratch — the output is entirely determined by the luminance structure and the Hue/Luma to Hue controls.
- **Brightness and Gain affect color, not just luminance**: Because the Y value drives hue rotation (when Luma to Hue is active), the Y-channel proc amp controls shift and stretch the color mapping. Use this coupling intentionally.
- **AND vs. XOR is the biggest toggle**: fundamentally changes the character of all bit-crushing. AND is structured. XOR is chaotic. It's the difference between posterization and glitch art.
- **Independent Y and UV crushing**: Posterize crushes Y only. Chroma Crush crushes UV only. High Posterize with no Chroma Crush = quantized brightness with smooth color. No Posterize with low Chroma Crush = smooth brightness with quantized color. Both have distinct visual characters.
- **Chroma Invert complements the palette**: Instantly flip every color to its complement without changing luminance or modulation depth. Useful for quickly exploring palette variations.
- **Feedback loops with hue rotation**: Each feedback pass rotates hue further, creating cycling chromatic cascades that evolve over time.
- **Bypass for A/B comparison**: Switch 11 shows the unprocessed signal instantly.
