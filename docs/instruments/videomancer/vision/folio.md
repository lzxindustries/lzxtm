---
draft: true
sidebar_position: 119
slug: /instruments/videomancer/folio
title: "Folio"
image: /img/instruments/videomancer/folio/folio_hero_s1.png
description: "Folio simulates the page turn transition familiar from presentation software and e-book readers, implemented entirely in scanline-rate FPGA logic."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import folio_source1_sunset from '/img/instruments/videomancer/folio/folio_source1_sunset.png';
import folio_source2_house from '/img/instruments/videomancer/folio/folio_source2_house.png';
import folio_source3_elephant from '/img/instruments/videomancer/folio/folio_source3_elephant.png';
import folio_source4_pattern from '/img/instruments/videomancer/folio/folio_source4_pattern.png';
import folio_source5_man from '/img/instruments/videomancer/folio/folio_source5_man.png';
import folio_source6_paint from '/img/instruments/videomancer/folio/folio_source6_paint.png';
import folio_hero_s1 from '/img/instruments/videomancer/folio/folio_hero_s1.png';
import folio_hero_s2 from '/img/instruments/videomancer/folio/folio_hero_s2.png';
import folio_hero_s3 from '/img/instruments/videomancer/folio/folio_hero_s3.png';
import folio_hero_s4 from '/img/instruments/videomancer/folio/folio_hero_s4.png';
import folio_hero_s5 from '/img/instruments/videomancer/folio/folio_hero_s5.png';
import folio_hero_s6 from '/img/instruments/videomancer/folio/folio_hero_s6.png';
import folio_ex1_s1 from '/img/instruments/videomancer/folio/folio_ex1_s1.png';
import folio_ex1_s2 from '/img/instruments/videomancer/folio/folio_ex1_s2.png';
import folio_ex1_s3 from '/img/instruments/videomancer/folio/folio_ex1_s3.png';
import folio_ex1_s4 from '/img/instruments/videomancer/folio/folio_ex1_s4.png';
import folio_ex1_s5 from '/img/instruments/videomancer/folio/folio_ex1_s5.png';
import folio_ex1_s6 from '/img/instruments/videomancer/folio/folio_ex1_s6.png';
import folio_ex2_s1 from '/img/instruments/videomancer/folio/folio_ex2_s1.png';
import folio_ex2_s2 from '/img/instruments/videomancer/folio/folio_ex2_s2.png';
import folio_ex2_s3 from '/img/instruments/videomancer/folio/folio_ex2_s3.png';
import folio_ex2_s4 from '/img/instruments/videomancer/folio/folio_ex2_s4.png';
import folio_ex2_s5 from '/img/instruments/videomancer/folio/folio_ex2_s5.png';
import folio_ex2_s6 from '/img/instruments/videomancer/folio/folio_ex2_s6.png';
import folio_ex3_s1 from '/img/instruments/videomancer/folio/folio_ex3_s1.png';
import folio_ex3_s2 from '/img/instruments/videomancer/folio/folio_ex3_s2.png';
import folio_ex3_s3 from '/img/instruments/videomancer/folio/folio_ex3_s3.png';
import folio_ex3_s4 from '/img/instruments/videomancer/folio/folio_ex3_s4.png';
import folio_ex3_s5 from '/img/instruments/videomancer/folio/folio_ex3_s5.png';
import folio_ex3_s6 from '/img/instruments/videomancer/folio/folio_ex3_s6.png';

# Folio

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: folio_source1_sunset, after: folio_hero_s1 },
    { label: "House", before: folio_source2_house, after: folio_hero_s2 },
    { label: "Elephant", before: folio_source3_elephant, after: folio_hero_s3 },
    { label: "Pattern", before: folio_source4_pattern, after: folio_hero_s4 },
    { label: "Man", before: folio_source5_man, after: folio_hero_s5 },
    { label: "Paint", before: folio_source6_paint, after: folio_hero_s6 },
  ]}
/>
*A photographic image caught mid-page-turn, its right half compressed into a narrow vertical strip against a saturated teal background — the fold edge darkened, the revealed colour field filling the vacated screen space.*

---

## Overview

Folio simulates the page turn transition familiar from presentation software and e-book readers, implemented entirely in scanline-rate FPGA logic. The incoming video frame is treated as a flat page anchored at one edge — the hinge — that rotates away from the viewer to reveal a coloured background. As the turn angle increases, the visible width of the page shrinks according to a cosine function: at zero degrees the page is fully open and fills the screen; at ninety degrees it collapses to a vertical line and vanishes. A Digital Differential Analyzer compresses the full source scanline into the narrowing visible region, maintaining horizontal detail as the page folds.

The effect operates on every scanline independently, reading from a line buffer and writing compressed pixels into the visible region while filling the remaining screen with a configurable background colour. Fold shading attenuates the luminance of the turning page proportional to the cosine of the turn angle, simulating the way a physical page catches less light as it turns edge-on. An optional sharp shadow near the fold edge adds depth cues. The background is a solid colour field whose hue and luminance are controlled independently, allowing the revealed surface to range from deep black through vivid chromatic fields to bright white.

The name *Folio* refers to a single leaf of a book or manuscript — a page that can be turned to reveal the next surface beneath. In bookbinding, a folio is also the largest standard page format, formed by folding a full press sheet once. Both meanings resonate: the program treats the entire video frame as one large page, folding it away to expose a new field.

---

## Background

### Page Turn Transitions in Presentation Software

The page turn is one of the oldest and most recognisable slide transitions, appearing in early Macintosh presentation tools and later becoming a standard effect in PowerPoint, Keynote, and PDF viewers. The visual metaphor is immediately legible: the current content lifts from one edge and curls away, revealing the next slide beneath. Early implementations used simple horizontal wipes or accordion folds; modern versions add perspective distortion, specular highlights, and shadow mapping. Folio distills the effect to its geometric essence — cosine-based width compression and luminance attenuation — producing a convincing page turn without the computational overhead of 3D texture mapping or mesh deformation.

### Cosine-Based Horizontal Compression

When a flat surface rotates around a vertical axis, its projected width on a frontal plane follows a cosine curve: $W = W_0 \cos(\theta)$. At $\theta = 0°$ (face-on), the full width is visible; at $90°$ (edge-on), the projected width reaches zero. This relationship is exact for orthographic projection and a close approximation for moderate perspective. Folio stores a 128-entry quarter-cosine lookup table covering $0°$ to approximately $180°$ (oscillating), with 10-bit output precision. The table maps the turn angle to a scaling factor that determines how many screen pixels the compressed page occupies. Because the cosine function is smooth and monotonic in the first quadrant, the compression accelerates as the page approaches edge-on — a visually natural behaviour that matches real paper.

### DDA Line Drawing and Scanline Resampling

The Digital Differential Analyzer is a classic algorithm for rasterising lines and resampling signals at non-integer rates. In Folio, the DDA compresses a full 1280-pixel source scanline into the visible width determined by the cosine lookup. The DDA step size is computed as $\text{step} = \text{source\_width} / \text{visible\_width}$ in 11.10 fixed-point arithmetic. As the output pixel counter traverses the visible region, the DDA accumulator increments by this step, and the integer part of the accumulator selects the source pixel from the line buffer. When the visible width is smaller than the source width, the step exceeds 1.0 and source pixels are skipped — an effective nearest-neighbour decimation that preserves edges and high-contrast features better than linear interpolation at this resolution.

### Fold Shading in 3D Graphics

In 3D rendering, surfaces that face away from the light source receive less illumination — the classic Lambertian shading model scales brightness by the cosine of the angle between the surface normal and the light direction. Folio applies a simplified version: the shade factor is derived from the same cosine value used for width compression, attenuating the page's luminance as it turns away. An additional shadow depth parameter sets a floor — the minimum brightness the page reaches at $90°$. Near the fold edge (within 8 pixels of the hinge-opposite boundary), an optional extra darkening halves the luminance, simulating the crease shadow where a physical page bends. This two-level shading produces a convincing depth illusion at minimal hardware cost.

### Background Chromakey and Hue Selection

The area behind the turning page is filled with a solid colour determined by two parameters: a hue angle and a luminance value. The hue is resolved through 64-entry sinusoidal U and V lookup tables that map the 10-bit register to a full $360°$ colour wheel at the chroma midpoint. The luminance control sets the Y channel directly. This separation allows the background to take any visible colour — from deep saturated primaries at moderate luminance to pastel tints at high luminance to solid black at zero. The background acts as a chromakey surface: downstream keying programs can isolate the revealed region by colour, making Folio useful as a shaped mask generator in multi-program video chains.


---

## Signal Flow

```
[Per-Frame (vsync_start)]
├─ Auto Animate?
│   ├─ Yes: turn_phase += anim_speed   (16-bit DDS accumulator)
│   └─ No:  turn_phase = turn_pot << 9 (manual, 7-bit index)
└─ Cosine LUT: cos_value = COS_LUT[turn_phase[15:9]]

[Per-Pixel Pipeline]
│
├─ Stage 0: Input Register + Counter Update
│   ├─ Write input Y/U/V to line buffer at wr_addr
│   ├─ h_count++ during AVID
│   ├─ v_count++ at hsync, lb_ab toggle
│   └─ ◄── data_in
│
├─ Stage 1: Visible Region Geometry
│   ├─ visible_width = active_width × cos_value / 1024
│   ├─ Hinge Left:  visible_left=0, visible_right=visible_width
│   ├─ Hinge Right: visible_left=active_width−visible_width, visible_right=active_width
│   ├─ DDA step = active_width × 1024 / visible_width  (11.10 fixed-point)
│   └─ shade_factor = shadow_depth + (1023 − shadow_depth) × cos_value / 1024
│       ◄── Turn Pos (pot 1), Shadow (pot 5), Hinge (tog 7)
│
├─ Stage 2: Region Classification + DDA Address
│   ├─ in_visible = (h_count ≥ visible_left) ∧ (h_count < visible_right) ∧ (visible_width > 2)
│   ├─ DDA accumulator: accum += dda_step (reset at visible_left)
│   ├─ read_addr = accum[20:10]  (integer part)
│   ├─ Fold zone: 8 pixels from fold edge
│   │   ├─ Hinge Left:  fold = (visible_right − h_count ≤ 8)
│   │   └─ Hinge Right: fold = (h_count − visible_left < 8)
│   └─ Pipeline: in_visible_d1/d2, in_fold_d1/d2
│
├─ Stages 3–4: Line Buffer Read (2-clock latency)
│   ├─ lb_y_out = Y_buffer[read_addr]
│   ├─ lb_u_out = U_buffer[read_addr]
│   └─ lb_v_out = V_buffer[read_addr]
│
├─ Stage 5: Compositor (fold shading + background)
│   ├─ Visible pixel:
│   │   ├─ comp_y = lb_y × shade_factor / 1024
│   │   ├─ Fold zone + Fold Shadow enabled: comp_y >>= 1
│   │   ├─ comp_u = lb_u,  comp_v = lb_v
│   ├─ Background pixel:
│   │   ├─ comp_y = bkg_lum
│   │   ├─ comp_u = HUE_U_LUT[bkg_hue[9:4]]
│   │   └─ comp_v = HUE_V_LUT[bkg_hue[9:4]]
│   └─ ◄── BKG Hue (pot 2), BKG Lum (pot 6), Fold Shd (tog 9)
│
├─ Stages 6–9: Interpolator Mix (×3 channels, 4 clocks)
│   └─ mix = lerp(delayed_input, composite, mix_amount)
│       ◄── Mix (fader 12)
│
├─ Sync Delay Pipeline (10-clock shift register)
│
└─ Output Mux
    ├─ Bypass Off → mixed Y/U/V + aligned sync
    └─ Bypass On  → delayed input Y/U/V + aligned sync
        ◄── Bypass (tog 11)
```

The cosine lookup and visible width computation are updated once per frame during vertical blanking. The 7-bit LUT index derived from the turn phase maps onto 128 entries that cover a full oscillation cycle — the first 82 entries span $0°$ to approximately $90°$ (full open to edge-on), and the remaining entries mirror the descent back. In manual mode the pot maps directly to the first quadrant ($0°$–$90°$), while auto-animate mode free-runs through the full oscillation. The DDA step calculation uses a fixed-point division that produces exact nearest-neighbour resampling: each screen pixel in the visible region maps to one or more source pixels, with no interpolation or blending between samples.

The fold zone detection identifies the 8 pixels nearest the fold edge — the boundary where the page meets the background. When fold shadow is enabled, these pixels receive an additional 50% luminance reduction on top of the global shade factor, producing a visible dark crease line at the fold. The zone is measured from the hinge-opposite edge: for a left hinge, the fold is at the right boundary of the visible region; for a right hinge, the fold is at the left boundary. This 8-pixel shadow is narrow enough to read as a crease rather than a gradient, adding depth without obscuring content.

---

## Parameter Reference


### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Turn Pos
| Property | Value |
|----------|-------|
| Range | 0° – 90° |
| Default | 0° |
| Suffix | ° |

Sets the page turn angle in manual mode. At minimum the page is fully open and fills the entire screen width — no compression or shading is applied. As the knob advances, the visible width narrows according to the cosine curve, reaching approximately half width at $60°$ and collapsing to a thin strip near $90°$. The luminance also dims progressively as the shade factor tracks the same cosine value. This control has no effect when Animate is set to Auto, since the DDS phase accumulator overrides the manual position. The relationship between knob position and visual width is non-linear — the first $45°$ of rotation removes relatively little width, while the final $45°$ compresses the page dramatically. This matches the geometric reality of a cosine curve and produces a natural-feeling turn.

---

#### Knob 2 — BKG Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 180° |
| Suffix | ° |

Selects the hue of the background colour revealed behind the turning page. The 10-bit register indexes into 64-entry sinusoidal U and V lookup tables that sweep through the full $360°$ colour wheel. At $0°$ the background has maximum U (blue-shifted) with neutral V. Sweeping clockwise traverses cyan, green, yellow, red, magenta, and back to blue. The hue control affects only the chrominance of the background — luminance is set independently by BKG Lum. At any hue, the background saturation is fixed at the LUT's peak amplitude; to desaturate, reduce BKG Lum toward zero (which produces dark, near-black tones) or increase it toward maximum (which pushes toward pastel territory as Y rises above the chroma signal).

---

#### Knob 3 — Anim Spd
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Controls the speed of automatic page turn animation. In Auto mode, this value is added to a 16-bit phase accumulator once per frame during vertical blanking. At minimum (0), the accumulator does not advance and the page holds its current position. At moderate values the page turns slowly — completing a full open-close-open oscillation cycle over several seconds. At maximum the page flips rapidly, producing a fast, rhythmic folding and unfolding motion. Because the cosine LUT covers a symmetric oscillation (open → closed → open), the animation appears as a continuous back-and-forth page flip rather than a one-way turn. This parameter has no effect when Animate is set to Manual.

---

#### Knob 4 — Curvatur
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Reserved for fold curvature control. In the current VHDL implementation, this register is read but not connected to any processing logic — the page turn is always a flat fold with no cylindrical curvature. The parameter is exposed for future firmware revisions that may add perspective warping or curved fold geometry. Adjusting this knob has no visible effect on the output.

---

#### Knob 5 — Shadow
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the shadow depth — the minimum luminance the page retains at its most edge-on orientation. At minimum ($0$%), the shade factor allows the page to dim all the way to black at $90°$, creating dramatic contrast between the fully open and fully closed states. At the default midpoint ($50$%), the page retains moderate brightness even when nearly edge-on. At maximum ($100$%), no luminance attenuation occurs regardless of turn angle — the page stays at full brightness throughout the turn. The shade factor is computed as $\text{shadow\_depth} + (1023 - \text{shadow\_depth}) \times \cos(\theta) / 1024$, so higher values raise the floor without affecting the fully-open brightness. This control interacts with Fold Shadow: when both are active, the fold zone receives the shade factor's attenuation plus an additional $50$% cut, which can produce very dark crease lines at low shadow depth settings.

---

#### Knob 6 — BKG Lum
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the luminance of the background colour field. This value is applied directly as the Y channel for all background pixels — those outside the visible page region. At zero, the background is black regardless of the hue setting. At maximum, the background is a bright pastel or near-white depending on the hue. At the default midpoint, the background sits at a moderate luminance that allows most hue selections to read as saturated colours. This control is independent of the page's own luminance — the page brightness is governed by the shade factor, while the background brightness is set here. The combination of BKG Hue and BKG Lum provides full control over the revealed surface colour.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Hinge** | Left | Right |
| **8 — Axis** | Horiz | Vert |
| **9 — Fold Shd** | Off | On |
| **10 — Animate** | Manual | Auto |
| **11 — Bypass** | Off | On |

The five toggles divide into three functional groups. Hinge (7) and Axis (8) define the geometric configuration of the page turn — which edge is anchored and which axis the fold operates along. In the current implementation only Hinge is active; Axis is reserved for future use. Fold Shadow (9) and Animate (10) control the rendering and animation behaviour — whether the fold crease is visible and whether the turn angle auto-advances. Bypass (11) overrides all processing. The most common workflow is to set Hinge and Fold Shadow first to define the visual character, then choose Manual or Auto animation, and finally use Bypass for A/B comparison.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Crossfades between the delayed dry input and the processed page turn composite. At $0$% (fader down), the output is the unprocessed input — no page turn is visible. At $100$% (fader up), the output is the full composite with the page turn effect, fold shading, and background colour. Intermediate positions blend the two, allowing the page turn to appear as a semi-transparent overlay. This is useful for softening the transition or for creating ghostly page-fold effects where the background shows through a dimmed, partially visible page. The interpolator operates independently on Y, U, and V channels.

---

## Guided Exercises

These exercises progress from a static half-turn through animated oscillation to creative use of the background colour as a shaped mask. Feed a recognisable source image — text, graphics, or camera footage — so the compression and shading effects are clearly visible.

### Exercise 1: Static Half Turn

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: folio_source1_sunset, after: folio_ex1_s1 },
    { label: "House", before: folio_source2_house, after: folio_ex1_s2 },
    { label: "Elephant", before: folio_source3_elephant, after: folio_ex1_s3 },
    { label: "Pattern", before: folio_source4_pattern, after: folio_ex1_s4 },
    { label: "Man", before: folio_source5_man, after: folio_ex1_s5 },
    { label: "Paint", before: folio_source6_paint, after: folio_ex1_s6 },
  ]}
/>
*Static Half Turn — simulated result across source images.*
**Source**: A high-contrast image with readable text or geometric patterns — something where horizontal compression is immediately obvious.

**Objective**: Observe the cosine-based width compression and fold shading at a fixed turn angle to understand the geometric relationship between angle and visible width.

1. **Set manual mode**: Ensure Animate is set to Manual.
2. **Half turn**: Set Turn Pos to approximately 60° (~66%). The page should compress to roughly half its original width.
3. **Left hinge**: Set Hinge to Left. The visible region occupies the left portion of the screen, with background filling the right.
4. **Enable fold shadow**: Set Fold Shd to On. A dark crease should be visible at the right edge of the visible page.
5. **Adjust shadow depth**: Sweep Shadow from 0% to 100%. At 0%, the page is dramatically darkened; at 100%, the page retains full brightness despite the turn angle.
6. **Switch hinge**: Flip Hinge to Right. The visible region mirrors to the right side of the screen. The fold shadow moves to the left edge of the visible region.
7. **Full turn**: Advance Turn Pos to 90°. The page collapses to a thin strip and nearly disappears.

**Key concepts**: Cosine curve produces non-linear width compression — the page narrows slowly at first and rapidly near 90°. Fold shadow adds a visible crease at the fold boundary. Shadow depth sets the minimum brightness floor. Hinge selection mirrors the geometry.

---

### Exercise 2: Animated Page Flip

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: folio_source1_sunset, after: folio_ex2_s1 },
    { label: "House", before: folio_source2_house, after: folio_ex2_s2 },
    { label: "Elephant", before: folio_source3_elephant, after: folio_ex2_s3 },
    { label: "Pattern", before: folio_source4_pattern, after: folio_ex2_s4 },
    { label: "Man", before: folio_source5_man, after: folio_ex2_s5 },
    { label: "Paint", before: folio_source6_paint, after: folio_ex2_s6 },
  ]}
/>
*Animated Page Flip — simulated result across source images.*
**Source**: A video source with moderate motion — camera footage or a slowly changing pattern. The motion helps distinguish the compressed page content from the static background.

**Objective**: Explore automatic page turn animation, observing the oscillating open-close cycle and the interaction between animation speed and shade factor.

1. **Enable auto animation**: Set Animate to Auto.
2. **Slow speed**: Set Anim Spd to approximately 20%. The page turns slowly, taking several seconds for a full cycle.
3. **Watch the cycle**: Observe the page open fully, compress to a thin strip, then open again. The cosine LUT produces a smooth oscillation.
4. **Increase speed**: Raise Anim Spd to 60%. The page flips rapidly — note how the shading pulses in sync with the width compression.
5. **Reduce shadow**: Set Shadow to 0%. The page now darkens dramatically at the closed position, creating a strong strobe-like pulse.
6. **Disable fold shadow**: Set Fold Shd to Off. The crease line disappears, leaving only the global shade attenuation.
7. **Right hinge**: Switch Hinge to Right. The animation mirrors — the page now folds away from the left.

**Key concepts**: DDS phase accumulator produces continuous oscillation through the cosine LUT. The open-close-open cycle is inherent to the symmetric LUT. Shadow depth modulates the contrast of the animation cycle. Animation speed is additive — higher values complete cycles faster.

---

### Exercise 3: Coloured Mask Generation

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: folio_source1_sunset, after: folio_ex3_s1 },
    { label: "House", before: folio_source2_house, after: folio_ex3_s2 },
    { label: "Elephant", before: folio_source3_elephant, after: folio_ex3_s3 },
    { label: "Pattern", before: folio_source4_pattern, after: folio_ex3_s4 },
    { label: "Man", before: folio_source5_man, after: folio_ex3_s5 },
    { label: "Paint", before: folio_source6_paint, after: folio_ex3_s6 },
  ]}
/>
*Coloured Mask Generation — simulated result across source images.*
**Source**: Any video source — the source content is secondary to the background colour field in this exercise.

**Objective**: Use the page turn as a shaped vertical wipe to create a coloured mask region, exploring the background hue and luminance controls for downstream keying applications.

1. **Set a vivid background**: Set BKG Hue to approximately 120° (green region) and BKG Lum to approximately 70%.
2. **Half turn**: Set Turn Pos to approximately 45° in Manual mode. The background fills roughly 30% of the screen.
3. **Full shadow suppression**: Set Shadow to 0%. The page content at the fold edge is very dark, creating a clear boundary between page and background.
4. **Sweep hue**: Slowly rotate BKG Hue through the full range. The background cycles through the colour wheel — blue, cyan, green, yellow, red, magenta.
5. **Luminance extremes**: Set BKG Lum to 0% (black background — the mask disappears into darkness). Then set BKG Lum to 100% (bright, pastel background).
6. **Increase turn angle**: Advance Turn Pos to 75°. The background now dominates the frame — most of the screen is the solid colour field with a narrow strip of compressed page at the hinge.
7. **Mix reduction**: Pull Mix to 50%. The page turn composite blends with the dry input, creating a partially transparent colour overlay.

**Key concepts**: The background colour field acts as a solid mask region. Hue and luminance are independently controllable. At high turn angles, the background dominates the frame. The sharp boundary between page and background can serve as a vertical key edge for downstream processing.

---


## Tips

- **Start in Manual mode**: Set Animate to Manual and explore different turn angles with the Turn Pos knob before enabling auto-animation. This builds intuition for the cosine compression curve.
- **Shadow depth sets the mood**: Low Shadow values create dramatic contrast between open and closed states — the page darkens significantly as it turns. High values keep the page bright throughout, producing a flatter, more graphic look.
- **Fold shadow adds depth**: The 8-pixel crease shadow is subtle but effective. Enable it for realistic page turn simulations; disable it for a cleaner, more abstract wipe effect.
- **Background as chromakey**: Use a vivid, saturated background colour (BKG Hue at a primary, BKG Lum at 50–70%) to create a colour field that downstream keying programs can isolate. The sharp edge between page and background makes an effective key boundary.
- **Mix fader for overlays**: At 50% Mix, the page turn composite blends with the dry input, creating a ghost-fold effect where both the original and the compressed page are visible simultaneously.
- **Hinge for directionality**: Left hinge creates a right-to-left reveal (page folds away rightward); right hinge creates a left-to-right reveal. Choose based on the visual flow of your composition.
- **Auto speed sweet spot**: Moderate Anim Spd values (20–40%) produce graceful, readable page turns. Very high values create a rapid flicker that can serve as a rhythmic strobe effect.
- **DDA is nearest-neighbour**: The horizontal compression skips source pixels rather than averaging them. Fine horizontal detail may alias at high compression ratios — feed content with bold, high-contrast features for the best visual results.

---

## Glossary

| Term | Definition |
|------|------------|
| **AVID (Active Video ID)** | A timing signal that is high during the active picture area of each scanline, indicating valid pixel data. |
| **Cosine LUT** | A lookup table storing pre-computed cosine values for 128 angle positions, used to determine the projected width of the turning page. |
| **DDA (Digital Differential Analyzer)** | An incremental algorithm that maps source pixel positions to output positions at non-integer step sizes, used here to compress a scanline into a narrower visible region. |
| **DDS (Direct Digital Synthesis)** | A technique for generating cyclical motion using a fixed-width phase accumulator incremented by a tuning word, producing smooth oscillation with automatic wraparound. |
| **Fixed-point** | A number representation where a fixed number of bits represent the fractional part; the DDA uses 11.10 format (11 integer bits, 10 fractional bits). |
| **Fold shadow** | A narrow band of extra luminance reduction near the fold edge, simulating the crease shadow where a physical page bends away from the viewer. |
| **Hinge** | The fixed edge around which the page rotates; determines whether the page folds away from the left or right side of the screen. |
| **Line buffer** | A dual-port BRAM that stores one scanline of video data, allowing the previous line to be read while the current line is being written. |
| **Shade factor** | A per-frame luminance multiplier derived from the cosine of the turn angle and the shadow depth parameter, attenuating the page brightness as it rotates away. |
| **YUV** | A colour model separating luminance (Y) from two chrominance components (U and V), used throughout Videomancer's video pipeline. |

---
