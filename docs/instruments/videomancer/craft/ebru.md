---
draft: true
sidebar_position: 91
slug: /instruments/videomancer/ebru
title: "Ebru"
image: /img/instruments/videomancer/ebru/ebru_hero.png
description: "In the art of Turkish marbling, pigment drops fall onto the surface of a water bath treated with gum solution."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import ebru_hero from '/img/instruments/videomancer/ebru/ebru_hero.png';
import ebru_control_panel from '/img/instruments/videomancer/ebru/ebru_control_panel.png';
import ebru_exercise1_result from '/img/instruments/videomancer/ebru/ebru_exercise1_result.png';
import ebru_exercise2_result from '/img/instruments/videomancer/ebru/ebru_exercise2_result.png';
import ebru_exercise3_result from '/img/instruments/videomancer/ebru/ebru_exercise3_result.png';
import ebru_source1_kodim13 from '/img/instruments/videomancer/ebru/ebru_source1_kodim13.png';
import ebru_source2_kodim13_bw from '/img/instruments/videomancer/ebru/ebru_source2_kodim13_bw.png';
import ebru_source3_kodim03 from '/img/instruments/videomancer/ebru/ebru_source3_kodim03.png';

# Ebru

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Kodim13", before: ebru_source1_kodim13, after: ebru_hero },
    { label: "Kodim13 B&W", before: ebru_source2_kodim13_bw, after: ebru_hero },
    { label: "Kodim03", before: ebru_source3_kodim03, after: ebru_hero },
  ]}
/>
*Ebru applying concentric ring distortion and sinusoidal comb rake displacement to create Turkish water marbling textures from live video.*

---

## Overview

In the art of Turkish marbling, pigment drops fall onto the surface of a water bath treated with gum solution. Each drop expands into concentric rings as surface tension pushes the pigment outward. The artist then drags a comb or stylus through the floating ink, stretching and interleaving the rings into the flowing, organic patterns found on the endpapers of centuries-old books.

Ebru translates this physical process into a real-time video effect. A DDS (direct digital synthesis) sine oscillator generates concentric ring patterns radiating from a movable centre point. A second sinusoidal oscillator sweeps perpendicular to the rings, displacing them along horizontal or vertical scan axes — the digital equivalent of dragging a comb through wet ink. When multi-drop mode is engaged, a second virtual ink drop creates overlapping ring fields that interfere and blend, producing the complex interlocking patterns characteristic of traditional Ebru.

The concentric rings modulate the source video's luminance — bright rings lift it, dark troughs suppress it — creating an impression of ink floating on water. An optional color-band mode pushes U and V chroma in opposite directions, producing rainbow-hued rings that shift the video's palette through warm and cool tones simultaneously.

---

## Background

### Turkish Marbling (Ebru)

The word *ebru* derives from the Persian *ab-rū* ("water surface") and refers to the art of paper marbling practiced in the Ottoman Empire since at least the fifteenth century. The marbler prepares a shallow tray of water thickened with carrageenan or gum tragacanth, then drops pigment mixed with ox gall (a surfactant) onto the surface. Each drop pushes aside the previous colours, forming concentric rings. The artist manipulates these with combs, needles, and rakes to create *battal* (free-form), *gel-git* (back-and-forth), and *tarakli* (combed) patterns before laying a sheet of paper on top to capture the image. Ebru was inscribed in UNESCO's Representative List of the Intangible Cultural Heritage of Humanity in 2014.

### Suminagashi

A parallel tradition, *suminagashi* ("floating ink"), developed independently in Japan during the Heian period (794–1185). Suminagashi uses *sumi* ink and pine resin surfactant on plain water. The artist touches alternating brushes of ink and surfactant to the water's surface, creating concentric rings that are then blown or fanned into flowing patterns before transferring to absorbent *washi* paper. While the underlying physics are similar — concentric expansion driven by surface tension gradients — the aesthetic is characteristically different: Suminagashi favours monochromatic, vein-like organic flows, whereas Ebru embraces vivid polychromatic geometric patterns.

### Concentric Ring Patterns

When a drop of ink lands on the prepared water surface, the surfactant in the pigment reduces surface tension locally, causing the liquid to pull away from the impact point in all directions. This radial expansion creates concentric rings whose spacing depends on the relative concentrations of surfactant and thickener. In the VHDL implementation, the ring spacing is controlled by a frequency parameter that multiplies radial distance — higher frequency values produce tighter, more closely spaced rings. The distance field itself uses a Manhattan approximation (|dx| + |dy| scaled by ¾) rather than true Euclidean distance, which gives the rings a slightly diamond-shaped character reminiscent of the subtle faceting seen in actual ink drops on high-viscosity surfaces.

### Comb Rake Techniques

The comb or rake is the marbler's primary tool for transforming concentric drops into flowing patterns. A traditional Turkish comb is a row of evenly spaced pins mounted on a straight bar. Dragged horizontally through the floating ink, it creates sinusoidal displacement — each pin pushes the ink in its path, stretching the concentric rings into S-curves. The pitch (pin spacing) and the depth of the drag determine the resulting pattern geometry. In Ebru, the *tarakli* (combed) pattern uses alternating horizontal and vertical passes with combs of different pitches to create the intricate nested structure seen on Ottoman bookbindings. The effect's comb simulation applies a sinusoidal displacement at a variable frequency and depth, mimicking the periodic disturbance of pin-by-pin dragging.

### Water Surface Tension and Ink Dynamics

The physics of Ebru depend on a delicate balance of forces. The thickened water surface creates a quasi-two-dimensional medium where ink pigment floats rather than sinking. The surfactant in the pigment locally reduces surface tension, causing the surrounding liquid to retract and the pigment to spread until the surface tension gradient reaches equilibrium. Multiple drops interact through these tension fields — a new drop pushes existing pigment aside, creating the nested ring structure that is Ebru's visual signature. The multi-drop mode in this program models this interaction by computing ring patterns from two virtual centre points and averaging their sine outputs, producing the constructive and destructive interference patterns that arise when multiple ink drops overlap on real water.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Input Register + Position Counters
│   └── Pixel (H,V) tracking; animation phase accumulates (+4/frame)
│
├── Stage 2: Distance Computation
│   ├── Centre 1: (center_x × 2, center_y × 2) from Pot 3 & 4
│   ├── Manhattan dist₁ = (|dx₁| + |dy₁|) × ¾
│   ├── Centre 2: Centre 1 offset by (+256, +192) pixels
│   ├── Manhattan dist₂ = (|dx₂| + |dy₂|) × ¾
│   └── Comb coordinate = V (horiz comb) or H (vert comb)
│
├── Stage 3: Sine Phase Index
│   ├── ring_phase₁ = (dist₁ × freq[9:2]) >> 6  +  anim_offset
│   ├── ring_phase₂ = (dist₂ × freq[9:2]) >> 6  +  anim_offset
│   ├── comb_phase  = (comb_coord × comb_freq[9:2]) >> 6
│   └── Extract 7-bit phase indices for quarter-wave LUT
│
├── Stage 4: Sine LUT + Ring Combine + Comb Multiply
│   ├── 32-entry quarter-wave LUT → full-wave via quadrant mirror/negate
│   ├── Multi-drop OFF: ring_val = sin(ring_phase₁)
│   │   Multi-drop ON:  ring_val = (sin₁ + sin₂) / 2
│   ├── comb_val = sin(comb_phase) × comb_depth[9:4] >> 5
│   └── combined = ring_val + comb_val
│
├── Stage 5: Amplitude Multiply
│   └── mod_value = combined × ring_amplitude  [bits 19:10]
│
├── Stage 6: Composite
│   ├── Y_out = clamp(Y_in + mod_value, 0, 1023)
│   ├── Color bands ON:
│   │   ├── U_out = clamp(U_in + mod_value/2, 0, 1023)
│   │   └── V_out = clamp(V_in − mod_value/2, 0, 1023)
│   └── Color bands OFF: U/V pass through unchanged
│
├── Stages 7–10: Interpolator wet/dry mix (4 clocks)
│   └── output = lerp(delayed_dry, wet, mix_amount)
│
└── Output: Bypass mux → processed or original signal
```

The pipeline's central interaction is between the ring generator and the comb rake. The ring pattern creates concentric brightness modulation radiating from the centre point, but the comb displaces the ring phase along the perpendicular scan axis, stretching the rings into the sinusoidal S-curves that define marbled patterns. The comb displacement is additive — it shifts the ring's effective phase rather than blending a separate pattern — so the result is a single coherent distortion field rather than two superimposed textures.

When multi-drop mode is active, the pipeline computes two complete distance-to-sine chains in parallel and averages their outputs before comb displacement. This creates constructive interference (brighter peaks) where both ring patterns align and destructive interference (cancellation toward neutral) where they oppose. The second centre is offset by a fixed 256 × 192 pixel displacement from the first, ensuring the two drop patterns are always visually distinct.

---

## Parameter Reference

<img src={ebru_control_panel} alt="Videomancer front panel with Ebru loaded"/>
*Videomancer's front panel with Ebru active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Ring Space
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Ring Space controls the spatial frequency of the concentric rings. At low values, the rings are widely spaced — broad, gentle bands of brightening and darkening radiate outward from the centre point. As the control increases, the rings tighten, producing fine concentric striations. The VHDL multiplies radial distance by the upper 8 bits of this register, so the frequency response is linear with respect to the control position. At very high settings, the rings may alias against the pixel grid, producing Moire-like shimmer that can be an interesting textural effect in its own right.

---

#### Knob 2 — Rake Pitch
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Rake Pitch scales the amplitude of the combined ring-plus-comb modulation before it is applied to the source video. At zero, no modulation reaches the output and the image passes through unchanged (assuming full wet mix). As the control increases, the ring and comb pattern bites deeper into the luminance signal — highlights push toward white, troughs push toward black. At maximum, the modulation can swing the full 10-bit range, producing high-contrast marbled textures that overpower the source content.

---

#### Knob 3 — Rake Depth
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Rake Depth sets the horizontal position of the primary ink drop centre. The 10-bit register value is doubled internally to span the full HD horizontal range (0–2047 pixels). When multi-drop mode is active, the second centre is offset 256 pixels to the right of this position. Sweeping this control moves the entire ring pattern across the screen, which also changes how the comb rake interacts with the rings — because the comb's phase is position-dependent, sliding the centre alters the rake's apparent angle of attack.

---

#### Knob 4 — Anim Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Anim Speed sets the vertical position of the primary ink drop centre. Like Rake Depth, the register value is doubled for full vertical coverage. Together with Rake Depth, this control positions the virtual point where the ink "drops" onto the video surface. Moving the centre into a corner concentrates the ring pattern in one quadrant; centring it produces a symmetrical bulls-eye that radiates to all edges of the frame.

---

#### Knob 5 — Color Spread
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Color Spread controls the spatial frequency of the comb rake oscillation. Lower values produce wide, sweeping S-curves; higher values create tighter, more closely spaced teeth. This corresponds to the pin spacing on a physical marbling comb — a fine-toothed comb (high frequency) creates dense, closely packed undulations, while a coarse comb (low frequency) produces broad, gentle curves. The comb oscillates along either the horizontal or vertical axis depending on the Rake Dir toggle.

---

#### Knob 6 — Ink Density
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Ink Density controls the depth (strength) of the comb rake displacement. At zero, the comb has no effect and the ring pattern radiates as pure concentric circles (or diamonds, due to the Manhattan distance approximation). As Ink Density increases, the comb sinusoid adds progressively larger phase offsets to the ring pattern, stretching the rings into the flowing, organic S-curves characteristic of combed Ebru. At maximum, the comb displacement can exceed the ring spacing, folding the pattern back on itself and creating complex interference textures.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Rake Dir** | Horiz | Vert |
| **8 — Seeds** | 2 | 4 |
| **9 — Color Mode** | Video | Palette |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control binary processing options that partition the effect into distinct modes. Rake Dir selects the axis of comb displacement. Seeds engages the second virtual ink drop for overlapping ring interference. Color Mode enables ring-outward animation. Animate activates chromatic colour banding that shifts U and V in opposite directions. Bypass routes the input directly to the output for instant A/B comparison.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade between the processed marbled signal and the original source video. At 100% (maximum, default), the output is fully processed. At 0%, the output is the unmodified source. Intermediate positions blend the two signals linearly via the interpolator, allowing subtle marbling textures to be layered gently over the source. This is particularly useful when the ring amplitude is set high — reducing the mix tames the intensity without changing the pattern geometry.

---

## Guided Exercises

These three exercises build from basic ring patterning through comb rake shaping to full multi-drop chromatic marbling, progressively revealing how each stage of the Ebru pipeline contributes to the final texture.

### Exercise 1: Concentric Rings

<BeforeAfterSlider
  sources={[
    { label: "Kodim13", before: ebru_source1_kodim13, after: ebru_exercise1_result },
    { label: "Kodim13 B&W", before: ebru_source2_kodim13_bw, after: ebru_exercise1_result },
    { label: "Kodim03", before: ebru_source3_kodim03, after: ebru_exercise1_result },
  ]}
/>
*Concentric Rings — simulated result across source images.*
**Source**: A live camera feed or recorded footage with mid-range brightness and visible detail — faces, landscapes, or architectural subjects work well.

**Objective**: Understand how the concentric ring generator interacts with the source video and how centre position and ring spacing shape the pattern.

1. **Centre the drop**: Set Rake Depth and Anim Speed to 50% each, placing the ring centre in the middle of the frame.
2. **Open the rings**: Set Ring Space to about 25% for wide, gentle ring bands. Observe how brightness modulation radiates outward from the centre.
3. **Tighten the rings**: Slowly increase Ring Space to 75%. The concentric bands become finer and more numerous.
4. **Increase amplitude**: Raise Rake Pitch from zero to about 60%. The ring pattern bites deeper into the luminance — highlights brighten, troughs darken.
5. **Move the centre**: Sweep Rake Depth left to right. Watch the entire ring pattern slide across the frame, changing which parts of the source video fall on peaks versus troughs.

**Key concepts**: Manhattan distance approximation, concentric ring frequency and amplitude, centre position as creative control

---

### Exercise 2: Comb Rake Shaping

<BeforeAfterSlider
  sources={[
    { label: "Kodim13", before: ebru_source1_kodim13, after: ebru_exercise2_result },
    { label: "Kodim13 B&W", before: ebru_source2_kodim13_bw, after: ebru_exercise2_result },
    { label: "Kodim03", before: ebru_source3_kodim03, after: ebru_exercise2_result },
  ]}
/>
*Comb Rake Shaping — simulated result across source images.*
**Source**: A high-contrast source — black and white patterns, bold graphics, or a colour-bar test signal.

**Objective**: Learn how the comb rake displaces ring patterns into flowing marbled S-curves.

1. **Establish rings**: Set Ring Space ~40%, Rake Pitch ~50%, centre at 50%/50%.
2. **Introduce the comb**: With a horizontal comb (Rake Dir = Horiz), slowly increase Ink Density from zero. Watch the concentric rings begin to wobble and stretch into sinusoidal curves.
3. **Vary the pitch**: Sweep Color Spread from low to high. Low values create broad, languid S-curves; high values create tight, densely packed teeth.
4. **Rotate the comb**: Switch Rake Dir to Vert. The flow direction rotates 90° — the same rings now undulate horizontally instead of vertically.
5. **Maximum displacement**: Push Ink Density to 100%. The comb displacement exceeds the ring spacing, folding the pattern and creating complex interference textures.

**Key concepts**: Comb direction selects displacement axis, comb frequency controls tooth spacing, comb depth controls displacement amplitude, ring-comb interaction creates marbled flow

---

### Exercise 3: Multi-Drop Chromatic Marbling

<BeforeAfterSlider
  sources={[
    { label: "Kodim13", before: ebru_source1_kodim13, after: ebru_exercise3_result },
    { label: "Kodim13 B&W", before: ebru_source2_kodim13_bw, after: ebru_exercise3_result },
    { label: "Kodim03", before: ebru_source3_kodim03, after: ebru_exercise3_result },
  ]}
/>
*Multi-Drop Chromatic Marbling — simulated result across source images.*
**Source**: Footage with rich colour content — botanical close-ups, textiles, or painted surfaces.

**Objective**: Combine multi-drop interference and chromatic colour bands to create polychromatic Ebru textures.

1. **Base pattern**: Set Ring Space ~35%, Rake Pitch ~50%, Ink Density ~40%, Color Spread ~50%.
2. **Enable multi-drop**: Toggle Seeds to engage the second ring centre. Observe how overlapping ring patterns create interference — bright where both peaks align, neutral where they cancel.
3. **Enable colour bands**: Toggle Animate to On. The ring modulation now pushes U and V chroma in opposite directions, producing rainbow-hued concentric bands.
4. **Animate**: Toggle Color Mode to Palette. The rings begin to expand outward slowly, creating a hypnotic, pulsing marbled texture.
5. **Subtle blend**: Lower the Mix fader to about 60%. The marbled texture overlays the source more gently, allowing the original colour content to show through the chromatic rings.

**Key concepts**: Multi-drop creates ring interference patterns, chromatic banding produces rainbow rings via opposing U/V modulation, animation drives continuous ring expansion, mix blending controls effect intensity

---


## Tips

- **Start with rings alone**: Set Ink Density to zero and explore Ring Space and Rake Pitch before engaging the comb. Understanding the concentric ring pattern in isolation makes it easier to predict how the comb will reshape it.
- **Centre position is compositional**: Rake Depth and Anim Speed position the virtual ink drop. Placing it on a face, a highlight, or an edge creates different compositional effects — the rings radiate from whatever the centre touches.
- **Comb direction dictates flow**: Horizontal combing creates vertical flow; vertical combing creates horizontal flow. Think of it as dragging a physical comb through the image — the pattern stretches in the direction of the drag.
- **Multi-drop adds complexity quickly**: Enabling the second ring centre doubles the pattern density and creates interference. Use lower Ring Space and Rake Pitch values when multi-drop is active to keep the texture legible.
- **Colour bands transform the palette**: The opposing U/V shifts create warm-cool gradients that follow the ring contours. This works especially well with desaturated source material, where the chromatic rings become the dominant colour information.
- **Use Mix for subtlety**: The wet/dry fader is the easiest way to tame an intense marbling effect. Blending at 30–40% creates a gentle watercolour overlay without losing source detail.
- **Animation is meditative**: The ring expansion is slow and constant (+4 phase per frame). It works best as a background texture evolution rather than a rhythmic animation. Pair with video feedback for slowly morphing, self-referencing patterns.
- **Feedback loops with Ebru**: Routing the output back to the input through an external feedback path causes the rings to marble themselves, creating recursive, ever-deepening concentric structures that evolve over time.

---

## Glossary

| Term | Definition |
|------|------------|
| **BT.601** | ITU-R Recommendation BT.601; the standard defining YUV colour encoding used throughout the Videomancer video pipeline. |
| **Comb Rake** | A row of evenly spaced pins dragged through floating ink to create sinusoidal displacement patterns in water marbling. |
| **DDS** | Direct Digital Synthesis; a technique for generating periodic waveforms using a phase accumulator and waveform lookup table. |
| **Ebru** | Turkish art of paper marbling, from Persian *ab-rū* ("water surface"); inscribed in UNESCO's Intangible Cultural Heritage list in 2014. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline in real time. |
| **Interpolator** | A linear crossfade unit used for wet/dry mixing, blending two inputs based on a 10-bit mix parameter. |
| **LUT** | Look-Up Table; a pre-computed array used to evaluate functions (here, the quarter-wave sine) efficiently in hardware. |
| **Manhattan Distance** | The sum of absolute coordinate differences (|dx| + |dy|), approximating Euclidean distance without square root computation. |
| **Multi-drop** | A mode that computes ring patterns from two virtual centre points and averages their outputs, simulating overlapping ink drops. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Quarter-Wave Sine** | A 32-entry table storing one quarter of a sine cycle; full-wave values are reconstructed via quadrant mirroring and sign inversion. |
| **Suminagashi** | Japanese floating-ink marbling technique, a parallel tradition to Ebru using *sumi* ink on plain water. |
| **YUV** | A colour encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
