---
draft: true
sidebar_position: 38
slug: /instruments/videomancer/cartouche
title: "Cartouche"
image: /img/instruments/videomancer/cartouche/cartouche_hero_s1.png
description: "Ancient Egyptian artists did not paint pictures the way we understand them."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import cartouche_source1_skull from '/img/instruments/videomancer/cartouche/cartouche_source1_skull.png';
import cartouche_source2_castle from '/img/instruments/videomancer/cartouche/cartouche_source2_castle.png';
import cartouche_source3_collage from '/img/instruments/videomancer/cartouche/cartouche_source3_collage.png';
import cartouche_source4_pattern from '/img/instruments/videomancer/cartouche/cartouche_source4_pattern.png';
import cartouche_source5_girl from '/img/instruments/videomancer/cartouche/cartouche_source5_girl.png';
import cartouche_source6_wood from '/img/instruments/videomancer/cartouche/cartouche_source6_wood.png';
import cartouche_hero_s1 from '/img/instruments/videomancer/cartouche/cartouche_hero_s1.png';
import cartouche_hero_s2 from '/img/instruments/videomancer/cartouche/cartouche_hero_s2.png';
import cartouche_hero_s3 from '/img/instruments/videomancer/cartouche/cartouche_hero_s3.png';
import cartouche_hero_s4 from '/img/instruments/videomancer/cartouche/cartouche_hero_s4.png';
import cartouche_hero_s5 from '/img/instruments/videomancer/cartouche/cartouche_hero_s5.png';
import cartouche_hero_s6 from '/img/instruments/videomancer/cartouche/cartouche_hero_s6.png';
import cartouche_ex1_s1 from '/img/instruments/videomancer/cartouche/cartouche_ex1_s1.png';
import cartouche_ex1_s2 from '/img/instruments/videomancer/cartouche/cartouche_ex1_s2.png';
import cartouche_ex1_s3 from '/img/instruments/videomancer/cartouche/cartouche_ex1_s3.png';
import cartouche_ex1_s4 from '/img/instruments/videomancer/cartouche/cartouche_ex1_s4.png';
import cartouche_ex1_s5 from '/img/instruments/videomancer/cartouche/cartouche_ex1_s5.png';
import cartouche_ex1_s6 from '/img/instruments/videomancer/cartouche/cartouche_ex1_s6.png';
import cartouche_ex2_s1 from '/img/instruments/videomancer/cartouche/cartouche_ex2_s1.png';
import cartouche_ex2_s2 from '/img/instruments/videomancer/cartouche/cartouche_ex2_s2.png';
import cartouche_ex2_s3 from '/img/instruments/videomancer/cartouche/cartouche_ex2_s3.png';
import cartouche_ex2_s4 from '/img/instruments/videomancer/cartouche/cartouche_ex2_s4.png';
import cartouche_ex2_s5 from '/img/instruments/videomancer/cartouche/cartouche_ex2_s5.png';
import cartouche_ex2_s6 from '/img/instruments/videomancer/cartouche/cartouche_ex2_s6.png';
import cartouche_ex3_s1 from '/img/instruments/videomancer/cartouche/cartouche_ex3_s1.png';
import cartouche_ex3_s2 from '/img/instruments/videomancer/cartouche/cartouche_ex3_s2.png';
import cartouche_ex3_s3 from '/img/instruments/videomancer/cartouche/cartouche_ex3_s3.png';
import cartouche_ex3_s4 from '/img/instruments/videomancer/cartouche/cartouche_ex3_s4.png';
import cartouche_ex3_s5 from '/img/instruments/videomancer/cartouche/cartouche_ex3_s5.png';
import cartouche_ex3_s6 from '/img/instruments/videomancer/cartouche/cartouche_ex3_s6.png';

# Cartouche

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: cartouche_source1_skull, after: cartouche_hero_s1 },
    { label: "Castle", before: cartouche_source2_castle, after: cartouche_hero_s2 },
    { label: "Collage", before: cartouche_source3_collage, after: cartouche_hero_s3 },
    { label: "Pattern", before: cartouche_source4_pattern, after: cartouche_hero_s4 },
    { label: "Girl", before: cartouche_source5_girl, after: cartouche_hero_s5 },
    { label: "Wood", before: cartouche_source6_wood, after: cartouche_hero_s6 },
  ]}
/>
*Cartouche dividing a landscape into four horizontal registers with Egyptian mineral pigment palette quantization and painted ground line separators.*

---

## Overview

Ancient Egyptian artists did not paint pictures the way we understand them. There was no vanishing point, no atmospheric perspective, no single unified scene. Instead, they divided the wall into horizontal bands — called *registers* — separated by painted ground lines. Each register contained its own independent scene, its own figures, its own narrative. The wall was read like a page: band by band, top to bottom.

Cartouche recreates this compositional system as a real-time video effect. It divides the frame into two to five horizontal registers, quantizes the color of each register to a six-pigment mineral palette modeled on actual tomb painting materials, and draws ground line separators between the bands. The name comes from the *cartouche* — the oval frame surrounding a pharaoh's name in hieroglyphic inscriptions — a fitting symbol for a program that frames and partitions the image.

At subtle settings, Cartouche applies a warm mineral wash over live video with faint dividing lines. At extreme settings, it reduces the image to stark horizontal bands of flat Egyptian color separated by thick dark ground lines — a living tomb wall painting scrolling in real time.

---

## Background

### What Is the Egyptian Register System?

The register system was the most distinctive and enduring compositional convention in ancient Egyptian art, maintained with remarkable consistency for over three thousand years. A painted or carved wall surface was divided into horizontal bands — typically three to five — each separated by a straight ground line. Each register functioned as an independent pictorial zone. Figures stood on their ground line, and their size indicated social importance rather than spatial distance: a pharaoh towered over servants regardless of position in the scene. This convention appears in the Tomb of Nebamun (c. 1350 BC), the Tomb of Nefertari, the Book of the Dead papyri, and thousands of other surviving works.

### What Are Mineral Pigments?

Egyptian painters worked with a remarkably limited palette derived entirely from minerals. Six pigments dominated: *carbon black* (soot or charcoal), *Egyptian blue* (calcium copper silicate — the first synthetic pigment in human history), *red ochre* (iron oxide), *yellow ochre* (hydrated iron oxide), *malachite green* (copper carbonate), and *calcium white* (gypsum or chalk). These pigments were ground, mixed with a binder of plant gum or egg white, and applied to dry plaster. Cartouche models these six colors as fixed YUV coordinate points and maps input video to the nearest pigment.

### What Is Palette Quantization?

Palette quantization is the process of reducing a continuous-tone image to a small set of predetermined colors. For each pixel, the algorithm finds the closest color in the target palette — typically by measuring distance in a color space — and replaces the original value with that palette entry. Cartouche uses squared luminance distance as its matching metric: it compares the input Y value to each of the six palette Y values and selects the closest. The Palette Depth control blends between the original color and the quantized result, allowing a smooth transition from full-color video to flat mineral pigment.

### What Is Boustrophedon Scrolling?

*Boustrophedon* — from the Greek for "as the ox turns" — describes a pattern in which alternating lines run in opposite directions, like the path of an ox plowing a field. In ancient writing, boustrophedon text alternated left-to-right and right-to-left on successive lines. Cartouche's Scroll Direction toggle offers a boustrophedon mode in which adjacent registers accumulate scroll phase in opposite directions. Although the current VHDL computes these opposing DDS phase offsets, the scroll displacement is not yet applied to the pixel read address — the phase accumulators run but do not shift the image horizontally. This infrastructure exists for a future update that will create the visual effect of registers sliding past each other in alternating directions.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Stage 1 — Register Zone Classification ─────────────────────
│   │
│   ├─ reg_height = 1080 / num_registers
│   ├─ reg_idx = v_count / reg_height (clamped)
│   ├─ Ground line test: v_count mod reg_height < ground_width?
│   └─ DDS scroll phase accumulators (5 independent)
│
├── Stage 2 — Palette Blend Preparation ────────────────────────
│   │
│   └─ blend_amt = palette_depth_pot
│
├── Stage 3 — Nearest Palette Match ────────────────────────────
│   │
│   ├─ Squared luminance distance to 6 pigment entries
│   ├─ Select minimum distance → nearest palette Y/U/V
│   ├─ Color mode remap (Full / Mono / Warm / Cool)
│   └─ Blend: out = (palette × blend + orig × (1023 − blend)) >> 10
│
├── Stage 4 — Ground Line + Accent Hue ────────────────────────
│   │
│   ├─ If ground region → insert ground color (Y=120, U=490, V=540)
│   └─ Else → U += accent_offset/4, V −= accent_offset/4
│
├── Interpolator — Wet/Dry Mix ─────────────────────────────────
│   │
│   └─ output = processed × mix + original × (1 − mix)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Pass-through (hsync, vsync, field, avid)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The pipeline divides cleanly into spatial classification (Stage 1) and color processing (Stages 3–4). Stage 1 determines *where* each pixel falls — which register, whether it sits on a ground line — and Stage 3 determines *what color* it becomes based on the nearest mineral pigment. The ground line test is a simple modular comparison: if the pixel's vertical position within its register falls within the ground width, the entire palette matching is overridden with a fixed dark brown color.

Note that Mode Vary (Toggle 8) and Scale Rank (Toggle 10) are declared as VHDL signals but are not connected to the processing pipeline in the current implementation — they are reserved for future features. Similarly, the DDS scroll phase accumulators in Stage 1 compute per-register offsets but do not yet shift the horizontal read address, so scrolling behavior is not visible in the current hardware.

---

## Parameter Reference


### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Registers
| Property | Value |
|----------|-------|
| Range | 0 – 3 |
| Default | 2 |

Selects the number of horizontal registers dividing the frame. The frame height is divided equally among the selected number of bands. At two registers the frame splits into upper and lower halves. At five registers the bands become narrow strips, creating a denser layered composition reminiscent of the most elaborate tomb wall paintings. The ground lines (if enabled) appear at the top edge of each register boundary.

---

#### Knob 2 — Scroll Spd
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Controls the scroll speed — the rate at which the DDS phase accumulators advance per frame. Note that in the current VHDL implementation, the computed scroll phase is not applied to the pixel read address, so this control does not produce a visible horizontal shift. The phase infrastructure is in place for a planned update. Turning this control currently has no visual effect on the output.

---

#### Knob 3 — Palette Dep
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the depth of palette quantization — how strongly pixel colors are pulled toward the nearest Egyptian mineral pigment. At minimum, the original video passes through with no color change. At maximum, every pixel snaps fully to one of the six palette entries, producing flat expanses of carbon black, Egyptian blue, red ochre, yellow ochre, malachite green, or calcium white. Intermediate values blend between the original color and the nearest pigment, creating a watercolor wash effect.

---

#### Knob 4 — Color Mode
| Property | Value |
|----------|-------|
| Range | 0 – 3 |
| Default | 0 |

Selects one of four color sub-palettes. Full mode uses all six pigments. Mono mode restricts the palette to carbon black and calcium white, producing a stark two-tone rendering like a charcoal sketch. Warm mode remaps blue and green entries to yellow ochre, concentrating the palette in earth tones. Cool mode remaps red to blue and yellow to green, shifting the palette toward cooler mineral hues. The remap occurs after the nearest-match stage, so the luminance structure is preserved while the chromatic character changes.

---

#### Knob 5 — Ground Line
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Controls the thickness of the painted ground line separators between registers. At minimum the lines are invisible — zero pixels wide. As the control increases, the ground lines thicken from hairline dividers to broad dark bands that consume a significant fraction of each register. The ground lines are only drawn when the Separator toggle is enabled. The ground line color is a fixed dark brown (Y=120, U=490, V=540), matching the earth-toned outlines used in Egyptian tomb painting.

---

#### Knob 6 — Accent Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Applies a hue rotation to the processed output by shifting the U and V channels in opposite directions. At the center position, no shift occurs. Rotating the control adds a warm or cool tint over the entire mineral palette — as if viewing the tomb painting under colored lighting. The shift is applied as U plus offset divided by four, V minus offset divided by four, keeping the modification subtle. This control does not affect ground line regions.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Scroll Dir** | Alternate | Same |
| **8 — Mode Vary** | Uniform | Alternate |
| **9 — Separator** | Plain | Zigzag |
| **10 — Scale Rank** | Equal | Graduated |
| **11 — Bypass** | Off | On |

Toggles 7–11 configure scrolling direction, palette variation, ground line display, scale ranking, and bypass. In the current VHDL implementation, only three of the five toggles produce a visible effect: Scroll Dir (Toggle 7) affects the DDS phase computation (though scrolling is not yet visible), Separator (Toggle 9) enables or disables ground lines, and Bypass (Toggle 11) routes input directly to output. Mode Vary (Toggle 8) and Scale Rank (Toggle 10) are declared as signals but are not connected to the processing pipeline — they are reserved for future features and have no current effect on the output.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Wet/dry mix at the end of the processing chain. At maximum, the full Egyptian register effect is applied. Lowering the fader blends the processed signal with the original, fading the palette quantization and ground lines back toward the unprocessed video. At minimum, the output matches the input regardless of all other control settings.

---

## Guided Exercises

These exercises explore the register system, mineral palette, and ground line separators. Each builds from simple frame division to full tomb wall composition.

### Exercise 1: Register Division and Ground Lines

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: cartouche_source1_skull, after: cartouche_ex1_s1 },
    { label: "Castle", before: cartouche_source2_castle, after: cartouche_ex1_s2 },
    { label: "Collage", before: cartouche_source3_collage, after: cartouche_ex1_s3 },
    { label: "Pattern", before: cartouche_source4_pattern, after: cartouche_ex1_s4 },
    { label: "Girl", before: cartouche_source5_girl, after: cartouche_ex1_s5 },
    { label: "Wood", before: cartouche_source6_wood, after: cartouche_ex1_s6 },
  ]}
/>
*Register Division and Ground Lines — simulated result across source images.*
**Source**: A live camera feed or recorded footage with horizontally distributed content — landscapes, cityscapes, or scenes with distinct upper and lower regions.

**Objective**: Learn how the register count and ground lines divide the frame into independent horizontal bands.

1. **Two registers**: Set Registers to its minimum. The frame splits into two equal halves with a single boundary.
2. **Add ground lines**: Enable the Separator toggle and increase Ground Line to about 40%. A dark brown line appears at the register boundary.
3. **More registers**: Sweep Registers through 3, 4, and 5 bands. Watch the frame subdivide into increasingly narrow horizontal strips, each separated by ground lines.
4. **Thick separators**: Push Ground Line toward maximum. The dark brown lines thicken into broad bands that dominate the composition.
5. **Remove lines**: Disable the Separator toggle to see the registers without visible division.

**Key concepts**: The register system divides the frame equally by height, ground lines mark boundaries between registers, separator thickness is continuously variable

---

### Exercise 2: Mineral Pigment Palette

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: cartouche_source1_skull, after: cartouche_ex2_s1 },
    { label: "Castle", before: cartouche_source2_castle, after: cartouche_ex2_s2 },
    { label: "Collage", before: cartouche_source3_collage, after: cartouche_ex2_s3 },
    { label: "Pattern", before: cartouche_source4_pattern, after: cartouche_ex2_s4 },
    { label: "Girl", before: cartouche_source5_girl, after: cartouche_ex2_s5 },
    { label: "Wood", before: cartouche_source6_wood, after: cartouche_ex2_s6 },
  ]}
/>
*Mineral Pigment Palette — simulated result across source images.*
**Source**: Footage with a wide range of colors — the macaw image or colorful market scenes.

**Objective**: Explore palette quantization across the four color modes.

1. **Prepare**: Set 3 registers, disable ground lines (Separator off), and push Palette Depth to about 80%.
2. **Full palette**: Leave Color Mode at Full (step 0). The image snaps to six mineral pigment colors — observe how saturated colors map to Egyptian blue, red ochre, malachite green, and yellow ochre.
3. **Mono mode**: Switch Color Mode to step 1. The image reduces to carbon black and calcium white — a stark two-tone rendering.
4. **Warm mode**: Switch to step 2. Blue and green entries remap to yellow ochre, concentrating the palette in warm earth tones.
5. **Cool mode**: Switch to step 3. Red remaps to blue, yellow to green — a cooler mineral palette.
6. **Partial blend**: Lower Palette Depth to about 40%. The mineral pigments blend with the original color, creating a watercolor wash.

**Key concepts**: Palette quantization maps each pixel to the nearest of six mineral pigments by luminance distance, color modes restrict or remap the available palette entries, blend depth controls the strength of quantization

---

### Exercise 3: Complete Tomb Wall Composition

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: cartouche_source1_skull, after: cartouche_ex3_s1 },
    { label: "Castle", before: cartouche_source2_castle, after: cartouche_ex3_s2 },
    { label: "Collage", before: cartouche_source3_collage, after: cartouche_ex3_s3 },
    { label: "Pattern", before: cartouche_source4_pattern, after: cartouche_ex3_s4 },
    { label: "Girl", before: cartouche_source5_girl, after: cartouche_ex3_s5 },
    { label: "Wood", before: cartouche_source6_wood, after: cartouche_ex3_s6 },
  ]}
/>
*Complete Tomb Wall Composition — simulated result across source images.*
**Source**: Any footage, especially scenes with figures, animals, or objects that evoke narrative content.

**Objective**: Combine all active controls to create a full Egyptian register composition with palette, ground lines, and accent hue.

1. **Frame structure**: Set 4 registers with thick ground lines (Ground Line ~50%, Separator enabled).
2. **Full palette**: Push Palette Depth to ~90% with Full color mode for the classic six-pigment look.
3. **Accent shift**: Slowly rotate the Accent Hue knob. Watch the mineral palette shift subtly in hue — warm tones become cooler and vice versa.
4. **Warm palette**: Switch Color Mode to Warm. The composition concentrates in earth tones with dark ground lines — the closest approximation to an actual tomb wall painting.
5. **Mix blend**: Lower the Mix fader to about 60%. The original video shows through the mineral pigment wash, creating a ghostly overlay of ancient and modern imagery.
6. **A/B compare**: Toggle Bypass to compare the full composition against the unprocessed source.

**Key concepts**: Register division and palette quantization are independent but complementary, ground lines provide structural framing, accent hue applies a global color shift to the mineral palette

---


## Tips

- **Start with registers alone**: Set Palette Depth to 0% and enable ground lines first. Understand the spatial structure before adding color.
- **Full palette at 100% is the signature look**: Pushing Palette Depth to maximum with all six pigments creates the most dramatic tomb wall effect — flat mineral colors with no trace of the original video's continuous tones.
- **Mono mode for charcoal sketches**: Color Mode step 1 reduces the palette to black and white only, producing a stark high-contrast rendering that works beautifully with thick ground lines.
- **Warm mode is the most historically accurate**: Warm mode concentrates the palette in earth tones (ochres, black, white) — the dominant colors in most surviving Egyptian tomb paintings.
- **Ground lines frame the composition**: Even thin ground lines (5–10%) dramatically change the perception of the image by imposing the register structure. Thick lines make the registers feel like separate panels.
- **Accent Hue is subtle**: The hue shift divides the offset by four, so changes are gentle. Use it to simulate different lighting conditions on the painted wall surface.
- **Unused controls are intentional**: Mode Vary, Scale Rank, and Scroll Speed are declared but not yet active. They are infrastructure for planned features — do not expect visible results from adjusting them.
- **Feedback routing**: Sending the output back to the input re-quantizes the already-quantized palette, progressively flattening the image to fewer and fewer pigment entries until it converges on a single dominant color per register.

---

## Glossary

| Term | Definition |
|------|------------|
| **Boustrophedon** | A bidirectional pattern, from the Greek for "as the ox turns," in which adjacent rows run in alternating directions like an ox plowing a field. |
| **Chrominance** | The colour-difference components of a video signal (U and V channels), encoding hue and saturation independently of brightness. |
| **DDS (Direct Digital Synthesis)** | A technique using a phase accumulator and fixed increment value to generate a periodic waveform or scrolling offset digitally. |
| **Ground line** | In Egyptian art, a painted horizontal line separating registers on which figures stand; in Cartouche, the dark brown separator drawn between horizontal bands. |
| **Luminance** | The brightness component of a video signal, represented by the Y channel in YUV colour space. |
| **Palette quantization** | The process of reducing a continuous-tone image to a small set of predetermined colours by mapping each pixel to the nearest palette entry. |
| **Register (compositional)** | A horizontal band in ancient Egyptian wall painting, functioning as an independent pictorial zone separated by ground lines. |
| **Squared luminance distance** | A colour-matching metric that compares pixel brightness to palette entries by squaring the difference, avoiding the computational cost of a square-root operation. |
| **VHDL** | VHSIC Hardware Description Language, used to define digital logic circuits for FPGA implementation. |
| **YUV** | A colour model that separates luminance (Y) from two chrominance components (U and V), widely used in video signal processing. |

---
