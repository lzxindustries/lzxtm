---
draft: true
sidebar_position: 8
slug: /instruments/videomancer/anodize
title: "Anodize"
image: /img/instruments/videomancer/anodize/anodize_hero.png
---

import anodize_hero from '/img/instruments/videomancer/anodize/anodize_hero.png';
import anodize_before_after from '/img/instruments/videomancer/anodize/anodize_before_after.png';
import anodize_control_panel from '/img/instruments/videomancer/anodize/anodize_control_panel.png';
import anodize_exercise1_result from '/img/instruments/videomancer/anodize/anodize_exercise1_result.png';
import anodize_exercise2_result from '/img/instruments/videomancer/anodize/anodize_exercise2_result.png';
import anodize_exercise3_result from '/img/instruments/videomancer/anodize/anodize_exercise3_result.png';

# Anodize

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={anodize_hero} alt="Anodize hero image"/>
*Anodize rendering a landscape in vivid red-orange anodized aluminum — the image is uniformly tinted with preserved specular highlights returning to white, metallic sheen coupling luma detail to chroma, and subtle grain texture on the surface.*
<img src={anodize_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Anodize applied.*

---

## Overview

Anodize simulates the appearance of anodized aluminum — the electrochemical surface treatment that gives metal products their vivid, uniform colours while maintaining a distinctive metallic reflective quality. The program applies a saturated colour tint across the entire image while preserving bright specular highlights, which remain white just as they do on real anodized metal surfaces. A metallic sheen effect couples brightness variations to chroma intensity, creating the characteristic luminance-dependent colour shift seen on anodized surfaces. Optional grain adds subtle surface texture.

The hue is selected from four colour quadrants in UV space — Red-Orange, Blue-Purple, Green-Teal, and Gold-Yellow — matching the most common anodized aluminum colours found in consumer electronics, architectural fixtures, and sporting equipment. A smooth mode interpolates between quadrants for continuous hue selection. The highlight threshold controls at what brightness level the tint begins to desaturate toward white, simulating specular reflections on the metal surface. Glossy mode pushes highlights further toward full desaturation, simulating a mirror-finish anodize.

At moderate settings, the program produces a convincing metallic tinted surface with natural highlight handling. At extreme settings — maximum saturation with low highlight threshold and full sheen — the image becomes a vivid metallic colour study.

---

## Background

### What Is Anodizing?

**Anodizing** is an electrochemical process that converts the surface of aluminum into a durable, corrosion-resistant aluminum oxide layer. This oxide layer is porous and can absorb dyes, allowing the metal to be coloured in a wide range of hues. Unlike paint, the colour is integrated into the surface itself — it cannot peel or chip because it IS the surface.

The most recognizable anodized products include Apple's MacBook Pro and iPhone housings (space grey, midnight, starlight), Leica camera bodies (black chrome), high-end bicycle frames, and architectural window frames. The distinctive quality of anodized colour is its uniformity combined with the metallic surface underneath — the colour is everywhere the same, but surface curvature and lighting create subtle brightness variations that the eye reads as "metal."

### What Are Specular Highlights on Anodized Metal?

The oxide layer on anodized aluminum is partially transparent. Light that penetrates the layer is absorbed and re-emitted at the dye colour, creating the uniform tint. However, some light reflects directly off the outer surface without penetrating — these direct reflections are **specular highlights**, and they retain the colour of the light source (typically white) rather than the dye colour.

This is why anodized metal looks coloured in general illumination but shows white highlights where light sources reflect directly. The program simulates this by detecting bright areas above a threshold and selectively reducing their colour saturation toward neutral (512, 512 in UV = grey/white).

### What Is Metallic Sheen?

Real metal surfaces have a unique optical property: their reflected colour varies with angle and curvature. This is because the reflected light is a mix of specular reflection (white) and diffuse reflection (coloured). As the surface curves, the ratio changes, creating subtle colour shifts that track the surface geometry. In video terms, this manifests as brightness-dependent colour saturation — brighter areas are slightly more coloured (or less coloured, depending on the finish). The Sheen control simulates this by coupling luma deviations from midpoint to chroma offsets.


---

## Signal Flow

```
Input Video (YUV 4:4:4 30-bit)
│
├── Y Channel ──────────────────────────────────────────────────────
│   │
│   ├─ 1.  Input register + parameter latch
│   ├─ 2.  Hue tint target              (quadrant select or smooth from
│   │       + saturation scale            Hue pot)
│   │       + invert option              (1023 − target if enabled)
│   ├─ 3.  Highlight detection           (Y > threshold → desaturate
│   │       + desaturation                toward 512; glossy mode:
│   │                                     far above → full neutral)
│   ├─ 4.  Metallic sheen              (4 tiers: luma−512 coupled
│   │       + compose                    to chroma at >>2/>>3/>>4/off)
│   └─ 5.  Grain apply                 (h_count XOR v_count
│                                        × grain pot >> 3 → additive Y)
│
├── Sync Signals ───────────────────────────────────────────────────
│   └─ 10-clock delay pipeline           (align with processing depth)
│
├── Interpolator (4 clocks per channel) ────────────────────────────
│   └─ Mix = lerp(input_delayed, processed, mix_amount)
│
└── Output ─────────────────────────────────────────────────────────
    └─ Y/U/V from interpolator mix
```

The hue tint target is computed from the Hue pot. In quadrant mode, the top 2 bits select one of four colour regions in UV space. In smooth mode, bits 7 and 6 of the hue fraction independently control the U and V polarity, creating a continuous four-zone sweep through the colour space. The Saturate pot controls the offset magnitude from the chroma midpoint (512).

The metallic sheen uses 4 tiers based on the Sheen pot value: above 768 → shift 2 (strongest coupling), above 512 → shift 3, above 256 → shift 4, below 256 → no coupling. The coupling adds a signed offset proportional to `(luma - 512) >> shift` to both U and V channels.

---

## Parameter Reference

<img src={anodize_control_panel} alt="Videomancer front panel with Anodize loaded"/>
*Videomancer's front panel with Anodize active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Hue
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Selects the anodize colour hue. In quadrant mode (Color toggle), the pot selects between four distinct hue zones: Red-Orange (0-25%), Blue-Purple (25-50%), Green-Teal (50-75%), and Gold-Yellow (75-100%). In smooth mode, the pot sweeps continuously through the colour space, with four distinct colour regions blending at the boundaries. The hue determines the base colour of the anodized surface.

---

#### Knob 2 — Saturate
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the saturation (colour intensity) of the anodized tint. At 0%, the U and V channels stay at the neutral midpoint (512) — no colour tint is applied. As saturation increases, the U and V values push further from midpoint toward the target hue. At maximum, the colour is fully saturated — vivid and intense. Moderate values (40-60%) are most realistic for actual anodized aluminum.

---

#### Knob 3 — Hi Thrsh
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the luminance threshold above which specular highlight desaturation begins. Pixels brighter than this threshold have their colour pulled toward neutral (grey/white). At low threshold, even moderate brightness triggers highlight whitening — the surface appears to have very bright, reflective highlights. At high threshold, only the very brightest pixels lose colour — the anodize tint persists through most of the brightness range.

---

#### Knob 4 — Sheen
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the metallic sheen intensity — the degree to which luma variations modulate chroma. At low values (below 25%), there is no luma-to-chroma coupling and the colour is perfectly uniform. At moderate values, the colour subtly shifts with brightness, creating a realistic metallic appearance. At maximum, the coupling is very strong — dark areas push the chroma in one direction and bright areas in the other, creating an exaggerated metallic shimmer.

---

#### Knob 5 — Grain
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the amplitude of the surface grain texture. At 0%, the surface is perfectly smooth. At higher values, a spatial noise pattern (derived from XOR of horizontal and vertical pixel coordinates) adds brightness variation, simulating the fine crystalline texture visible on real anodized surfaces under close inspection. The pattern is deterministic and repeating but appears random at normal viewing distances.

---

#### Knob 6 — Uniformty
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the uniformity of the anodize application. This parameter modifies how evenly the tint is distributed across the surface. Higher values produce more uniform colouring, while lower values allow the underlying luminance to show through the tint more strongly.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Color** | Red | Blue |
| **8 — Finish** | Matte | Satin |
| **9 — Hi Light** | Soft | Sharp |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

Toggle 7 maps to the VHD's hue_mode bit — the TOML labels "Red/Blue/Green/Gold" correspond to the four quadrant mode colours, while the VHD actually uses bit 0 for quadrant vs smooth mode selection. This means the TOML labels guide the user to different Hue pot ranges rather than directly switching modes. Toggle 8 maps to glossy mode. Toggle 9 enables grain. Toggle 10 enables tint inversion.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade between the original input video (delayed to match the 10-clock processing pipeline plus 4-clock interpolator) and the anodized output. At 0%, pure unprocessed input. At 100%, fully processed anodize rendering.

---

## Guided Exercises

These exercises progress from basic colour tinting through highlight preservation to metallic surface simulation, demonstrating how to create convincing anodized aluminum appearances.

### Exercise 1: Basic Anodized Surface

<img src={anodize_exercise1_result} alt="Basic Anodized Surface result"/>
*Basic Anodized Surface — simulated result across source images.*
**Source**: Image with even brightness distribution and clear subject — portrait or product photography.

**Objective**: Understand how the hue quadrant and saturation controls create the basic anodized colour tint.

1. **Select Red**: Set Hue to ~12% (Red-Orange quadrant). Saturate at ~50%.
2. **High threshold**: Hi Thrsh at ~80% so highlights are only on the very brightest areas.
3. **No sheen or grain**: Sheen at ~0%, Grain at ~0%. Color toggle to Red.
4. **Observe tint**: The entire image is uniformly tinted red-orange, with only the brightest highlights returning to white.
5. **Change hue**: Move Hue to ~37% (Blue-Purple quadrant). The tint shifts to blue.
6. **Try Green**: Hue at ~62%. Green-Teal anodize.
7. **Try Gold**: Hue at ~87%. Gold-Yellow anodize.
8. **Adjust saturation**: Sweep Saturate from 0% to 100%. At low values, the tint is subtle. At high values, it's vivid.

**Key concepts**: Hue quadrant selection, saturation control, uniform colour tinting in UV space

---

### Exercise 2: Highlight Preservation and Finish

<img src={anodize_exercise2_result} alt="Highlight Preservation and Finish result"/>
*Highlight Preservation and Finish — simulated result across source images.*
**Source**: Image with bright specular reflections — chrome objects, wet surfaces, or strong directional lighting.

**Objective**: Explore how the highlight threshold and finish settings control specular highlight behaviour on the anodized surface.

1. **Blue anodize**: Hue at ~37%, Saturate at ~60%.
2. **Low threshold**: Set Hi Thrsh to ~40%. Many areas lose their tint and return to white — like a very reflective surface.
3. **Raise threshold**: Push Hi Thrsh to ~70%. Only the brightest spots remain white.
4. **Glossy finish**: Toggle Finish to Gloss. The highlights snap harder to white — sharper specular reflections.
5. **Compare Matte**: Toggle back to Matte. The highlights are softer, more gradual.
6. **Sharp highlight**: Toggle Hi Light to Sharp. The highlight boundary becomes more defined.
7. **Find the sweet spot**: Set Hi Thrsh to ~60%, Matte, Soft — natural looking anodized metal with gentle highlights.

**Key concepts**: Highlight threshold, specular desaturation, glossy vs matte finish, hard vs soft highlight boundaries

---

### Exercise 3: Metallic Sheen and Grain

<img src={anodize_exercise3_result} alt="Metallic Sheen and Grain result"/>
*Metallic Sheen and Grain — simulated result across source images.*
**Source**: Image with gradual brightness variations — curved surfaces, light gradients, or natural textures.

**Objective**: Create the full metallic surface effect by adding luma-to-chroma coupling (sheen) and surface grain texture.

1. **Gold anodize**: Hue at ~87%, Saturate at ~55%.
2. **Moderate highlight**: Hi Thrsh at ~65%.
3. **Add sheen**: Set Sheen to ~60%. Notice how the colour subtly shifts with brightness — darker areas lean one way, brighter areas another.
4. **Maximum sheen**: Push Sheen to ~90%. The metallic colour variation is very pronounced.
5. **Add grain**: Toggle Hi Light to Sharp (enables grain via VHD mapping). Set Grain to ~30%.
6. **Observe texture**: A fine crystalline texture appears on the surface — especially visible on flat-colour areas.
7. **Full metallic**: Combine moderate sheen (~50%) with subtle grain (~20%) for the most realistic anodized aluminum look.

**Key concepts**: Metallic sheen (luma-to-chroma coupling), surface grain texture, combining effects for realism

---


## Tips

- **Moderate saturation is most realistic**: Real anodized aluminum has vivid but not neon-level colour. Saturate at 40-60% looks most authentic.
- **Highlight threshold matches the lighting**: Bright studio lighting needs a higher threshold; dim scenes need a lower threshold. Match the threshold to where specular reflections actually are in your source.
- **Sheen at ~50% is the sweet spot**: Enough metallic variation to read as metal, not so much that it overwhelms the colour.
- **Grain should be subtle**: Real anodized surfaces have very fine grain visible only at close range. Keep Grain below 25% for realism.
- **Red and Gold are the most common**: These are the colours most people associate with anodized aluminum from consumer products.
- **Blue anodize for sci-fi**: Blue-purple anodized aluminum is a staple of science-fiction production design.
- **Glossy finish for dark subjects**: The highlight desaturation is most visible on bright areas — on dark subjects, Matte and Gloss look similar.
- **Combine with other programs**: Anodize works well sequentially with programs that add structural texture — the tint unifies the visual while the texture adds surface detail.

---

## Glossary

| Term | Definition |
|------|------------|
| **Anodizing** | An electrochemical process that converts aluminum's surface into a durable, porous oxide layer capable of absorbing dye colour; the program simulates this uniform tinted-metal appearance. |
| **Chroma** | The colour-difference components (U and V) of a YUV signal, encoding hue and saturation independently of brightness. |
| **Desaturation** | Reducing a pixel's colour intensity by pulling its U and V values toward the neutral midpoint (512), making it appear more grey or white. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes Anodize's processing pipeline in hardware at pixel-clock speed. |
| **Luminance (Luma)** | The brightness component (Y channel) of a YUV video signal. |
| **Metallic Sheen** | A brightness-dependent colour shift that emulates how real metal surfaces vary in colour with viewing angle; implemented by coupling luma deviations to chroma offsets. |
| **Quadrant Mode** | A hue-selection scheme where the 10-bit pot range is divided into four zones, each producing a distinct colour family (Red-Orange, Blue-Purple, Green-Teal, Gold-Yellow). |
| **Specular Highlight** | A direct surface reflection of a light source that retains the light's colour (white) rather than the surface tint, because the light reflects before penetrating the dyed oxide layer. |
| **UV Space** | The two-dimensional chrominance plane of the YUV colour model, where angle from centre encodes hue and distance from centre encodes saturation. |
| **XOR Pattern** | A deterministic spatial noise texture generated by applying a bitwise exclusive-or operation to the horizontal and vertical pixel coordinates, used for surface grain. |
| **YUV** | A colour encoding separating brightness (Y) from colour (U, V); Videomancer's native 30-bit processing colour space. |

---
