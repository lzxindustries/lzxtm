---
draft: true
sidebar_position: 272
slug: /instruments/videomancer/stoa
title: "Stoa"
image: /img/instruments/videomancer/stoa/stoa_hero.png
description: "The stoa was the defining architectural form of ancient Greece — a long covered walkway fronted by a row of columns."
---

import stoa_hero from '/img/instruments/videomancer/stoa/stoa_hero.png';
import stoa_before_after from '/img/instruments/videomancer/stoa/stoa_before_after.png';
import stoa_control_panel from '/img/instruments/videomancer/stoa/stoa_control_panel.png';
import stoa_exercise1_result from '/img/instruments/videomancer/stoa/stoa_exercise1_result.png';
import stoa_exercise2_result from '/img/instruments/videomancer/stoa/stoa_exercise2_result.png';
import stoa_exercise3_result from '/img/instruments/videomancer/stoa/stoa_exercise3_result.png';

# Stoa

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={stoa_hero} alt="Stoa hero image"/>
*Stoa transforming live video into a Doric colonnade with cosine-shaded fluting, arris ridges, and entablature patterning.*
<img src={stoa_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Stoa applied.*

---

## Overview

The *stoa* was the defining architectural form of ancient Greece — a long covered walkway fronted by a row of columns. The Stoa of Attalos in Athens (c. 150 BC) and the Parthenon's Doric colonnade (c. 432 BC) remain among the most reproduced architectural images in Western culture. Their visual power comes not from color but from light — sunlight raking across the vertical concavities carved into each column shaft, called *flutes*, creating a repeating pattern of highlight and shadow that gives cylindrical stone the appearance of depth and mass.

Stoa divides the video frame into vertical strips representing column shafts and applies a cosine-based brightness curve across each strip, simulating the way directional light falls across fluted stone. A controllable light angle shifts the cosine phase, rotating the apparent illumination direction. Dark arris lines mark the sharp ridges between adjacent flutes. An entablature — the horizontal beam structure that sits atop the columns — can be rendered as an alternating triglyph-and-metope pattern in the upper portion of the frame. Capitals (the transitional elements between shaft and entablature) appear as a lighter band when enabled. Depth fade darkens columns toward the frame edges, suggesting a receding colonnade viewed in perspective.

The effect ranges from a subtle sculptural overlay that gives video the appearance of being projected onto carved stone, to a complete architectural abstraction where the original image is visible only as luminance modulation within the column structure. The stone surface color can be warmed or cooled to simulate different marble and limestone types.

---

## Background

### Classical Column Orders

Greek architecture recognized three major column orders — Doric, Ionic, and Corinthian — distinguished by their proportions, capitals, and fluting. Doric columns (the oldest and simplest) have 20 shallow flutes meeting at sharp edges called *arrises*. Ionic columns typically have 24 deeper flutes separated by flat bands called *fillets*. Stoa implements both flute counts (20 and 24) via the Flute Count toggle. The distinction is subtle but historically significant: Doric conveys strength and austerity; Ionic conveys grace and refinement.

### Fluting and the Cosine Curve

A column flute is a concave channel carved vertically into the shaft. In cross-section, each flute approximates a half-circle or ellipse. When parallel light strikes the column at an angle, the illumination across each flute follows a cosine distribution — brightest where the surface faces the light, darkest where it faces away. Stoa stores a 32-entry cosine lookup table and maps each pixel's horizontal position within a flute to a table index, producing a smooth brightness modulation. The Light Angle control shifts the cosine phase, rotating the apparent direction of illumination across all flutes simultaneously.

### Entablature and Architectural Elements

Above the columns, the entablature consists of the architrave (main beam), frieze, and cornice. The Doric frieze alternates between *triglyphs* (vertically grooved rectangular blocks) and *metopes* (smooth or sculpted panels between them). Stoa renders this as an alternating dark/light pattern in the top region of the frame, with the pattern width matched to the column width. Capitals — the transitional elements between shaft and entablature — appear as a lighter horizontal band of carved stone.

### Depth and Perspective

A colonnade viewed from one end recedes in perspective — each successive column appears smaller and darker. Stoa's Depth Fade toggle simulates this by linearly attenuating brightness from the center of the frame toward the edges. Columns near the center remain at full brightness; columns at the periphery darken as though farther from the viewer. This creates a spatial depth cue even in a flat 2D video signal.

### Stone and Light in Video Art

Architectural projection mapping — projecting video onto buildings — has become a major art form. Stoa inverts this concept: instead of projecting *onto* architecture, it projects architecture *into* the video signal. The stone color control tints the column surface warm (sandstone, terra cotta) or cool (marble, limestone), while the fluting pattern shapes the video content into something that reads as carved and illuminated stone.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Strip Coordinates ──────────────────────────────────
│   │   h_count / col_width → column index
│   │   h_count mod col_width → position within column
│   │
├── Stage 2: Flute Shading + Arris Detection ────────────────────
│   │   position within flute → cosine LUT index
│   │   + light angle offset (+ animation DDS)
│   │   cosine value × flute depth → shade
│   │   arris: pixels within arris_width of flute boundaries
│   │
├── Stage 3: Compositing + Entablature + Capitals ───────────────
│   │   input Y − (1023 − shade) + stone_base_Y/2
│   │   arris override → dark stone color
│   │   entablature: triglyph/metope pattern (top region)
│   │   capitals: light stone band (below entablature)
│   │
├── Stage 4: Depth Fade + Stone Color ───────────────────────────
│   │   depth fade: linear attenuation from center
│   │   stone hue offset → U ± offset/4, V ∓ offset/4
│   │
├── Interpolator Mix (4 clk each × 3 channels) ─────────────────
│   │   crossfade dry/wet
│   │
├── Sync Delay (8 clocks) ──────────────────────────────────────
│   │
└── Bypass Mux ─────────────────────────────────────────────────
    └─ Select original or processed signal
```

Input video luminance is the primary carrier: the fluting curve is *subtracted* from the input Y, so bright source regions show the fluting pattern most prominently while dark regions are pushed toward black. The stone base brightness (720/1023 ≈ 70%) is added back to lift the overall level. Chrominance is replaced entirely by stone surface colors — the input's hue and saturation are discarded in favor of the warm stone tint controlled by Stone Color. The entablature and capital regions override both luminance and chrominance with flat architectural colors, creating hard horizontal zones that break the columnar pattern.

---

## Parameter Reference

<img src={stoa_control_panel} alt="Videomancer front panel with Stoa loaded"/>
*Videomancer's front panel with Stoa active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Column W
| Property | Value |
|----------|-------|
| Range | 0 – 7 |
| Default | 3 |

Selects one of eight column widths ranging from 40 to 240 pixels. Narrow columns create a dense colonnade with many thin shafts; wide columns create a monumental, Parthenon-like appearance with fewer massive pillars. The number of flutes per column remains constant (20 or 24), so wider columns have proportionally wider individual flutes with more gradual cosine shading.

---

#### Knob 2 — Flute Depth
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the depth of the fluting concavity — the amplitude of the cosine-based brightness modulation. At zero, the columns appear smooth and unfluted (like pilasters). As depth increases, the brightness contrast between flute peaks (ridges) and troughs (valleys) grows, creating more dramatic light-and-shadow interplay. At maximum, the troughs are nearly black and the ridges are bright highlights.

---

#### Knob 3 — Light Angle
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Sets the directional light angle by offsetting the cosine lookup phase. At 0°, light appears to come from directly in front of the column (symmetric highlighting). Rotating the angle shifts the highlight toward one side of each flute, simulating raking sunlight from the left or right. The full 360° range cycles through all lighting directions. Combined with Light Anim, this becomes the starting phase of the animated rotation.

---

#### Knob 4 — Arris W
| Property | Value |
|----------|-------|
| Range | 0 – 3 |
| Default | 1 |

Selects the arris line width from 1 to 4 pixels. Arrises are the sharp ridges between adjacent flutes — the narrow edges where two concave surfaces meet. In real Doric columns, arrises catch the light as thin bright lines. In Stoa, they are rendered as dark shadow lines using the arris stone color (Y=200, near-black). Wider arris settings create bolder grid lines separating the flutes; narrower settings produce delicate ridge accents.

---

#### Knob 5 — Entablatur
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Controls the height of the entablature region at the top of the frame. At zero, no entablature is drawn. As the height increases, a horizontal zone of alternating triglyph (dark grooved) and metope (light smooth) blocks appears, sized to match the column width. This transforms the top of the video into an architectural frieze structure. The entablature height is specified directly in scanlines.

---

#### Knob 6 — Stone Color
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Tints the stone surface by applying a signed hue offset to the U and V channels. At 0°/360°, the stone retains its neutral warm tone (slight yellow-warm bias from the base UV constants). Rotating the control shifts the tint through blue-cool marbles, green-gray limestones, and red-warm terra cottas. The offset is applied as U + offset/4 and V − offset/4, creating complementary hue shifts.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Flute Count** | 20 Doric | Fit Frame |
| **8 — Light Anim** | Static | Animated |
| **9 — Capitals** | Off | On |
| **10 — Depth Fade** | Off | On |
| **11 — Bypass** | Off | On |

Switches 7–11 control five independent options affecting the column geometry, animation, and architectural elements. Flute Count changes the number of flutes per column (20 vs 24). Light Anim enables continuous rotation of the light angle. Capitals and Depth Fade add spatial detail. Bypass is the standard signal passthrough.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Crossfades between the dry (unprocessed) and wet (column-processed) signal via the interpolator. At 0%, the output is the original input. At 100%, the output is fully processed. Intermediate values blend the columnar shading with the original video, producing a translucent stone overlay effect where the columns appear to float on top of the source material.

---

## Guided Exercises

These exercises progress from basic column shading through architectural composition to animated light effects. Each builds on the previous, gradually engaging more of the processing chain.

### Exercise 1: Columnar Light Study

<img src={stoa_exercise1_result} alt="Columnar Light Study result"/>
*Columnar Light Study — simulated result across source images.*
**Source**: A live camera feed or recorded footage with recognizable subjects and moderate contrast.

**Objective**: Explore how column width and flute depth shape the image, and how the light angle creates the illusion of three-dimensional stone.

1. **Basic columns**: Set Column W to position 4 (~100 px wide). You should see the image divided into vertical strips with cosine-based brightness modulation.
2. **Flute depth**: Sweep Flute Depth from 0% to 100%. Watch the columns transform from smooth pillars to deeply carved flutes with dramatic highlight/shadow contrast.
3. **Light direction**: Slowly rotate Light Angle through 360°. The highlight slides across each flute, simulating rake lighting sweeping from one direction to another.
4. **Column width**: Sweep Column W through all 8 positions. Narrow columns (40 px) create a dense colonnade; wide columns (240 px) create monumental pillars.
5. **Arris lines**: Set Arris W to position 4. Bold dark lines now divide the flutes. Reduce to position 1 for delicate accents.

**Key concepts**: The cosine curve creates naturalistic flute shading, light angle shifts the cosine phase across all flutes simultaneously, arris lines mark the ridges between adjacent flutes

---

### Exercise 2: Architectural Composition

<img src={stoa_exercise2_result} alt="Architectural Composition result"/>
*Architectural Composition — simulated result across source images.*
**Source**: Wide-angle footage of interiors or urban scenes with strong vertical lines.

**Objective**: Build a complete classical architectural scene using entablature, capitals, and depth fade.

1. **Set columns**: Column W at position 3 (~80 px), Flute Depth ~60%.
2. **Add entablature**: Slowly increase Entablatur from 0%. A triglyph/metope pattern appears at the top of the frame, alternating dark and light blocks.
3. **Enable capitals**: Toggle Capitals on. A bright horizontal band appears between the entablature and the column shafts.
4. **Add depth**: Toggle Depth Fade on. Edge columns darken, creating a receding-colonnade perspective.
5. **Stone warmth**: Rotate Stone Color to warm the stone to a sandstone/terra cotta tone, then cool it to a marble blue-gray.
6. **Flute count**: Toggle Flute Count to see the difference between 20 and 24 flutes per column.

**Key concepts**: Entablature height controls the frieze zone, capitals add a transitional bright band, depth fade creates perspective by darkening edges, stone color tints the surface

---

### Exercise 3: Animated Light Sweep

<img src={stoa_exercise3_result} alt="Animated Light Sweep result"/>
*Animated Light Sweep — simulated result across source images.*
**Source**: Any footage — abstract or representational. Static footage works well to isolate the light animation.

**Objective**: Experience the animated light rotation and explore how mix blending creates a sculptural overlay.

1. **Set up columns**: Column W at position 5 (~120 px), Flute Depth ~70%, Arris W at 1 (fine ridges).
2. **Enable animation**: Toggle Light Anim to Animated. The highlight begins slowly sweeping across each flute in a continuous rotation.
3. **Set starting angle**: Rotate Light Angle to set the initial illumination direction.
4. **Full architecture**: Enable Entablatur (~15%), Capitals on, Depth Fade on. The entire scene becomes a slowly shifting colonnade.
5. **Mix for overlay**: Lower Mix to ~60%. The original video becomes visible through the stone texture, creating a projection-mapped effect.
6. **Mix near zero**: Lower Mix to ~10% for a very subtle architectural ghosting over the original footage.

**Key concepts**: Light animation creates a continuous phase shift on the cosine LUT index, mix blending determines how strongly the stone effect overlays the source, static vs animated light creates fundamentally different visual experiences

---


## Tips

- **Start with column width**: The column width defines the spatial rhythm of the entire effect. Choose it first based on how many columns you want visible in frame.
- **Moderate flute depth for realism**: Real stone fluting is subtle — keep Flute Depth around 30–50% for a naturalistic carved-stone look. Higher values produce dramatic but abstracted results.
- **Light Angle at 45° for drama**: Direct front-lighting (0°) is flat and symmetrical. Raking light at 30–60° creates the strongest sense of depth across the flutes.
- **Entablature needs headroom**: The entablature renders in absolute scanlines from the top of frame. Leave enough column shaft below it for the fluting to be visible.
- **Depth Fade with wide view**: Depth fade works best when the frame shows many columns — at least 4–6 — so the edge-to-center gradient is visible as a perspective cue.
- **Mix at 40–60% for overlay**: Blend the architectural structure with the source video for a projection-mapping effect where the original content appears through the stone texture.
- **Feedback for infinite colonnades**: Routing the output back to the input creates recursive column patterns — columns within columns, like looking down an infinite hall of pillars.
- **Arris W at 1 for film, 3–4 for graphic**: Fine arris lines (1 px) look photographic. Bold arris lines (3–4 px) look like architectural drawings or engravings.

---

## Glossary

| Term | Definition |
|------|------------|
| **Arris** | The sharp edge or ridge formed where two flute concavities meet on a column shaft; rendered as a dark line in Stoa. |
| **BT.601** | ITU-R Recommendation BT.601; the color matrix standard for standard-definition YUV encoding used throughout the Videomancer pipeline. |
| **Capital** | The uppermost element of a column, transitioning between the shaft and the entablature; rendered as a bright horizontal band. |
| **Colonnade** | A row of evenly spaced columns supporting a horizontal entablature; the defining element of a stoa. |
| **Cosine LUT** | A 32-entry lookup table storing cosine values mapped to [0–1023]; used to compute the flute shading curve. |
| **DDS** | Direct Digital Synthesis; a phase-accumulator technique used here to generate the animated light rotation at a constant rate per frame. |
| **Doric** | The oldest and simplest of the three Greek column orders, characterized by 20 flutes with sharp arrises and no base. |
| **Entablature** | The horizontal structure above the columns, consisting of architrave, frieze (with triglyphs and metopes), and cornice. |
| **Flute** | A concave vertical channel carved into a column shaft; Stoa simulates flutes using a cosine brightness curve. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Ionic** | The second Greek column order, characterized by 24 flutes with flat fillets and scroll-shaped volute capitals. |
| **Metope** | The smooth or sculpted panel between triglyphs in a Doric frieze. |
| **Stoa** | A covered walkway or portico with a row of columns along its front, common in ancient Greek public architecture. |
| **Triglyph** | A vertically grooved rectangular block in a Doric frieze, alternating with metopes. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
