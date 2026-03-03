---
draft: true
sidebar_position: 298
slug: /instruments/videomancer/tableau
title: "Tableau"
image: /img/instruments/videomancer/tableau/tableau_hero_s1.png
description: "In the golden age of Hollywood visual effects, matte painters would paint scenery — castles, skylines, alien landscapes — onto sheets of glass positioned between the camera and the set."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import tableau_control_panel from '/img/instruments/videomancer/tableau/tableau_control_panel.png';
import tableau_source1_dog from '/img/instruments/videomancer/tableau/tableau_source1_dog.png';
import tableau_source2_boat from '/img/instruments/videomancer/tableau/tableau_source2_boat.png';
import tableau_source3_turtle from '/img/instruments/videomancer/tableau/tableau_source3_turtle.png';
import tableau_source4_pattern from '/img/instruments/videomancer/tableau/tableau_source4_pattern.png';
import tableau_source5_woman from '/img/instruments/videomancer/tableau/tableau_source5_woman.png';
import tableau_source6_berries from '/img/instruments/videomancer/tableau/tableau_source6_berries.png';
import tableau_hero_s1 from '/img/instruments/videomancer/tableau/tableau_hero_s1.png';
import tableau_hero_s2 from '/img/instruments/videomancer/tableau/tableau_hero_s2.png';
import tableau_hero_s3 from '/img/instruments/videomancer/tableau/tableau_hero_s3.png';
import tableau_hero_s4 from '/img/instruments/videomancer/tableau/tableau_hero_s4.png';
import tableau_hero_s5 from '/img/instruments/videomancer/tableau/tableau_hero_s5.png';
import tableau_hero_s6 from '/img/instruments/videomancer/tableau/tableau_hero_s6.png';
import tableau_ex1_s1 from '/img/instruments/videomancer/tableau/tableau_ex1_s1.png';
import tableau_ex1_s2 from '/img/instruments/videomancer/tableau/tableau_ex1_s2.png';
import tableau_ex1_s3 from '/img/instruments/videomancer/tableau/tableau_ex1_s3.png';
import tableau_ex1_s4 from '/img/instruments/videomancer/tableau/tableau_ex1_s4.png';
import tableau_ex1_s5 from '/img/instruments/videomancer/tableau/tableau_ex1_s5.png';
import tableau_ex1_s6 from '/img/instruments/videomancer/tableau/tableau_ex1_s6.png';
import tableau_ex2_s1 from '/img/instruments/videomancer/tableau/tableau_ex2_s1.png';
import tableau_ex2_s2 from '/img/instruments/videomancer/tableau/tableau_ex2_s2.png';
import tableau_ex2_s3 from '/img/instruments/videomancer/tableau/tableau_ex2_s3.png';
import tableau_ex2_s4 from '/img/instruments/videomancer/tableau/tableau_ex2_s4.png';
import tableau_ex2_s5 from '/img/instruments/videomancer/tableau/tableau_ex2_s5.png';
import tableau_ex2_s6 from '/img/instruments/videomancer/tableau/tableau_ex2_s6.png';
import tableau_ex3_s1 from '/img/instruments/videomancer/tableau/tableau_ex3_s1.png';
import tableau_ex3_s2 from '/img/instruments/videomancer/tableau/tableau_ex3_s2.png';
import tableau_ex3_s3 from '/img/instruments/videomancer/tableau/tableau_ex3_s3.png';
import tableau_ex3_s4 from '/img/instruments/videomancer/tableau/tableau_ex3_s4.png';
import tableau_ex3_s5 from '/img/instruments/videomancer/tableau/tableau_ex3_s5.png';
import tableau_ex3_s6 from '/img/instruments/videomancer/tableau/tableau_ex3_s6.png';

# Tableau

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Dog", before: tableau_source1_dog, after: tableau_hero_s1 },
    { label: "Boat", before: tableau_source2_boat, after: tableau_hero_s2 },
    { label: "Turtle", before: tableau_source3_turtle, after: tableau_hero_s3 },
    { label: "Pattern", before: tableau_source4_pattern, after: tableau_hero_s4 },
    { label: "Woman", before: tableau_source5_woman, after: tableau_hero_s5 },
    { label: "Berries", before: tableau_source6_berries, after: tableau_hero_s6 },
  ]}
/>
*Tableau dividing the frame with a feathered matte boundary, desaturating and tinting one region to simulate classic glass painting composites.*

---

## Overview

In the golden age of Hollywood visual effects, matte painters would paint scenery — castles, skylines, alien landscapes — onto sheets of glass positioned between the camera and the set. The painted regions replaced parts of the live-action frame, creating impossible vistas from a few brushstrokes. The boundary between the painted region and the live action was called the *matte line*, and keeping it invisible was the matte artist's greatest challenge.

Tableau recreates this technique in the digital domain. A procedural matte boundary divides the frame into two regions: a "live plate" that passes the input video untouched, and a "matte plate" where the signal is desaturated, contrast-compressed, and tinted to simulate hand-painted glass artwork. The boundary can be horizontal or vertical, angled via a shift-based slope, and softened with a variable-width feather. A crawl artifact — a brightness pulse that travels along the matte line — and an optional LFSR grain overlay add the imperfections that make the composite feel authentically analog.

All processing is per-pixel with zero BRAM usage. The desaturation and contrast compression use shift-based arithmetic quantized to eight levels, keeping the FPGA resource footprint small. The result is a real-time glass painting compositor that can transform any video input into a split-screen diorama blending reality and artifice.

---

## Background

### Glass Painting in Cinema

The glass shot was invented in the early 1900s by Norman Dawn. A large sheet of glass was placed between the camera and the set, and parts of the glass were painted to extend or replace the scenery. Later practitioners — most famously Albert Whitlock at Universal Studios — refined the technique into an art form capable of creating photorealistic vistas. The key challenges were matching the lighting and color temperature of the painted region to the live action, and hiding the matte line where paint met reality.

### The Matte Line and Feathering

In a hard matte composite, the boundary between the two regions is a sharp edge. Any misalignment or color mismatch at this edge is immediately visible. Feathering — gradually blending the two regions over a transition zone — hides these artifacts. Tableau implements feathering as a linear alpha ramp: pixels near the boundary receive a mix of both the live and painted signals, with the blend ratio varying linearly across the feather width. The wider the feather, the softer and more invisible the transition.

### Desaturation and Contrast Compression

Glass paintings were typically created with oil paints, which have a narrower dynamic range and lower color saturation than photographic film. To simulate this, Tableau applies two processing stages to the matte region: desaturation (blending U and V chrominance channels toward their neutral value of 512) and contrast compression (pulling the Y luminance channel toward 512, reducing the dynamic range by approximately 25%). Together, these operations give the matte region the muted, painterly quality of actual glass artwork.

### Matte Crawl

In optical composites, slight mechanical vibration or film-gate instability caused the matte boundary to shift by one or two pixels between frames. On screen, this appeared as a faint bright or dark line that "crawled" along the matte edge — a telltale artifact of the compositing process. Tableau recreates this with a DDS (Direct Digital Synthesis) phase accumulator that modulates a brightness pulse at the boundary. The crawl phase advances once per frame, creating a slowly evolving boundary artifact whose intensity is controlled by the Crawl Int knob.

### LFSR Grain Overlay

Real glass paintings were photographed alongside the live action, so they acquired the same film grain as the rest of the frame. Tableau uses a 16-bit LFSR (Linear Feedback Shift Register) to generate pseudo-random noise that is added to the luminance channel in the matte region. This grain overlay makes the painted region feel like it was photographed rather than generated, improving the illusion of a real composite.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Position counters (h_count, v_count from video_timing_generator)
├── LFSR noise generator (lfsr16, seed 0xACE1)
│
├─ 1. Matte Distance ────────────────────────────────────────
│      axis = v_count (horiz split) or h_count (vert split)
│      slope = shift-based quantised angle (8 levels)
│      distance = primary − split_pos + slope_term
│
├─ 2. Feather Alpha ─────────────────────────────────────────
│      feather=0: hard step function
│      feather>0: linear ramp over feather width
│      invert_side: flip alpha (swap live/matte regions)
│
├─ 3a. Desaturation + Contrast ──────────────────────────────
│       U,V ← blend toward 512 (8-level shift-based)
│       Y ← compress toward 512 by 25%
│
├─ 3b. Tint + Clamp ────────────────────────────────────────
│       U,V ← desaturated + tint_u/tint_v offsets
│       Clamp to [0, 1023]
│
├─ 4. Alpha Composite ──────────────────────────────────────
│      4-bit alpha: result = input + (matte − input) * alpha >> 4
│      Clamp to [0, 1023]
│
├─ 5. Crawl + Grain ────────────────────────────────────────
│      Crawl: brightness bump near boundary (±3 pixels)
│      Grain: LFSR noise added to matte region (alpha > 25%)
│      Clamp to [0, 1023]
│
├─ 6. Mix (interpolator_u × 3) ─────────────────────────────
│      result = lerp(dry, wet, Mix)
│
├── Sync Signals ────────────────────────────────────────────
│   └─ Pass-through (delayed 11 clocks)
│
└── Bypass (via Mix fader at 0%) ────────────────────────────
```

The matte distance computation uses shift-based slope quantization to avoid a full multiply. The angle pot is divided into eight zones via its top 3 bits, producing slopes of 0, ±1/8, ±1/4, and ±1/2. This means the boundary angle snaps between discrete values rather than rotating continuously — an intentional constraint that keeps the design within the FPGA's LUT budget.

The alpha composite uses only the top 4 bits of the 10-bit alpha value, giving 16 effective blend levels. This is sufficient for a smooth-looking feather at typical feather widths but may show slight banding at very narrow feather settings. The crawl and grain are applied after the composite, so they affect only the blended result, not the raw matte or live regions independently.

---

## Parameter Reference

<img src={tableau_control_panel} alt="Videomancer front panel with Tableau loaded"/>
*Videomancer's front panel with Tableau active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Split Pos
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the position of the matte boundary along the primary axis. At 0%, the boundary sits at one edge of the frame and the entire image is the matte region. At 100%, the boundary moves to the opposite edge and the entire image is the live plate. At 50%, the frame is split roughly in half. The exact pixel position depends on the frame dimensions and the current angle setting.

---

#### Knob 2 — Angle
| Property | Value |
|----------|-------|
| Range | -45 – 45 |
| Default | 0 |

Controls the angle or tilt of the matte boundary. The pot is mapped to eight discrete slope levels via shift-based quantization: slopes of −1/2, −1/4, −1/8, 0, 0, +1/8, +1/4, and +1/2 relative to the secondary axis. The center range (roughly 37–63%) produces a straight horizontal or vertical boundary; the edges produce a diagonal boundary. The angle does not rotate continuously — it snaps between slope levels.

---

#### Knob 3 — Feather
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the width of the feather zone at the matte boundary. At 0%, the transition is a hard step — pixels are either fully live or fully matte. As the control increases, the alpha ramp widens, creating a gradual blend zone between the two regions. Wide feather settings make the matte line nearly invisible; narrow settings produce a visible hard edge suitable for split-screen effects.

---

#### Knob 4 — Desaturate
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Controls the amount of desaturation applied to the matte region. At 0%, the matte region retains its original color saturation. As the control increases, U and V channels are blended toward neutral (512) using shift-based arithmetic quantized to eight levels. At maximum the matte region is nearly monochrome, simulating the muted palette of oil paint on glass.

---

#### Knob 5 — Tint Color
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |
| Suffix | % |

Selects the tint hue applied to the desaturated matte region. The 10-bit register is divided into four quadrants mapping around a simplified hue wheel: sepia/warm (0–25%), green (25–50%), blue (50–75%), and amber (75–100%), wrapping back to sepia. The tint is added as fixed UV offsets on top of the desaturated signal, simulating the color cast of aged paint or tinted lacquer.

---

#### Knob 6 — Crawl Int
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the intensity of the matte crawl artifact. At 0%, no crawl is visible. As the control increases, a brightness pulse appears along the matte boundary that shifts phase once per frame. Higher values produce a more prominent crawl — a bright flash where the matte line sits. The crawl is only visible near the boundary (within ±3 pixels of the matte distance zero-crossing) and only during half of the DDS cycle, creating an intermittent flicker.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Split Axis** | Horiz | Vert |
| **8 — Invert Side** | Normal | Invert |
| **9 — Grain** | Off | On |
| **10 — Crawl Anim** | Static | Animate |
| **11 — Bypass** | Off | On |

The five toggles configure the composite's geometry, region assignment, texture, animation, and bypass. Split Axis selects horizontal or vertical division. Invert Side swaps which region gets the matte processing. Grain adds LFSR film noise to the painted region. Crawl Anim enables or freezes the per-frame phase advance of the crawl artifact. Bypass routes the input directly to the output.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade between the original signal and the composited result. At 100%, the output is fully processed. At 0%, the output is the unmodified input. This provides a final control over the composite opacity — useful for blending subtle matte effects into the live signal.

---

## Guided Exercises

These exercises progress from a basic split-screen composite to a full cinematic glass painting effect, introducing each processing stage incrementally.

### Exercise 1: Simple Split Screen

<BeforeAfterSlider
  sources={[
    { label: "Dog", before: tableau_source1_dog, after: tableau_ex1_s1 },
    { label: "Boat", before: tableau_source2_boat, after: tableau_ex1_s2 },
    { label: "Turtle", before: tableau_source3_turtle, after: tableau_ex1_s3 },
    { label: "Pattern", before: tableau_source4_pattern, after: tableau_ex1_s4 },
    { label: "Woman", before: tableau_source5_woman, after: tableau_ex1_s5 },
    { label: "Berries", before: tableau_source6_berries, after: tableau_ex1_s6 },
  ]}
/>
*Simple Split Screen — simulated result across source images.*
**Source**: A live camera feed or recorded footage with clear horizontal features (horizon line, architectural divisions).

**Objective**: Learn how the split position, axis, and feather controls define the matte boundary geometry.

1. **Horizontal split**: Confirm Split Axis is set to Horiz. Set Split Pos to 50%. The frame divides into upper and lower halves.
2. **Move the boundary**: Sweep Split Pos from 0% to 100%. Watch the matte line travel vertically across the frame.
3. **Angle the boundary**: Turn the Angle knob away from center. The boundary tilts, creating a diagonal split.
4. **Feather**: Increase Feather from 0%. The hard edge softens into a gradual blend zone.
5. **Vertical split**: Switch Split Axis to Vert. The split now divides left and right.
6. **Invert**: Toggle Invert Side to swap which region is the matte plate.

**Key concepts**: Split Pos controls boundary position, Angle tilts the boundary using shift-based discrete slopes, Feather controls the width of the alpha blend zone, Split Axis selects horizontal or vertical division

---

### Exercise 2: Painted Region Processing

<BeforeAfterSlider
  sources={[
    { label: "Dog", before: tableau_source1_dog, after: tableau_ex2_s1 },
    { label: "Boat", before: tableau_source2_boat, after: tableau_ex2_s2 },
    { label: "Turtle", before: tableau_source3_turtle, after: tableau_ex2_s3 },
    { label: "Pattern", before: tableau_source4_pattern, after: tableau_ex2_s4 },
    { label: "Woman", before: tableau_source5_woman, after: tableau_ex2_s5 },
    { label: "Berries", before: tableau_source6_berries, after: tableau_ex2_s6 },
  ]}
/>
*Painted Region Processing — simulated result across source images.*
**Source**: Footage with a visible sky or background area suitable for matte painting simulation.

**Objective**: Explore desaturation, contrast compression, and tinting to create a painterly matte region.

1. **Set the split**: Position the matte boundary so the sky or background area falls in the matte region (adjust Split Pos and Invert Side as needed).
2. **Desaturate**: Increase Desaturate from 0% to ~75%. Watch the matte region lose color, shifting toward monochrome.
3. **Tint**: Sweep Tint Color slowly. At ~10%, the matte region takes on a warm sepia cast. At ~50%, it shifts to blue. At ~75%, amber. Find a tint that complements the live plate.
4. **Widen feather**: Increase Feather to ~50% to create an invisible transition between the vivid live plate and the muted matte plate.
5. **Compare**: Toggle Bypass to see the original versus the composite.

**Key concepts**: Desaturation blends chroma toward neutral using shift-based arithmetic, tint adds UV offsets from a four-quadrant hue wheel, contrast compression reduces the matte region's dynamic range by ~25%

---

### Exercise 3: Full Cinematic Composite

<BeforeAfterSlider
  sources={[
    { label: "Dog", before: tableau_source1_dog, after: tableau_ex3_s1 },
    { label: "Boat", before: tableau_source2_boat, after: tableau_ex3_s2 },
    { label: "Turtle", before: tableau_source3_turtle, after: tableau_ex3_s3 },
    { label: "Pattern", before: tableau_source4_pattern, after: tableau_ex3_s4 },
    { label: "Woman", before: tableau_source5_woman, after: tableau_ex3_s5 },
    { label: "Berries", before: tableau_source6_berries, after: tableau_ex3_s6 },
  ]}
/>
*Full Cinematic Composite — simulated result across source images.*
**Source**: Any footage — especially material with an interesting horizon, skyline, or background/foreground division.

**Objective**: Combine all Tableau features for a complete glass painting composite with crawl and grain artifacts.

1. **Set geometry**: Position the split and angle to place the boundary along a natural feature in the frame.
2. **Process the matte**: Set Desaturate ~60%, Tint Color ~10% (sepia), Feather ~35%.
3. **Add crawl**: Increase Crawl Int to ~40%. Enable Crawl Anim (Animate). Watch the faint bright pulse travel along the matte line.
4. **Add grain**: Enable Grain (Switch 9). The matte region now has subtle film-grain noise.
5. **Fine-tune**: Adjust Split Pos and Angle to align the composite with the scene. Lower Mix to ~80% to let a hint of the original through.
6. **Explore inversion**: Toggle Invert Side to swap which region is painted. Try the complementary composition.

**Key concepts**: Crawl artifact is a DDS-driven brightness pulse near the boundary, grain adds LFSR noise to the matte region for photographic authenticity, all features combine for a complete vintage composite effect

---


## Tips

- **Start with geometry before processing**: Set Split Pos, Axis, and Angle first to position the matte boundary where you want it. Then engage desaturation and tint to process the matte region.
- **Wide feather hides the boundary**: A feather width of 30–50% makes the matte line nearly invisible. This is the key to a convincing composite — the viewer shouldn't see where the split is.
- **Sepia tint for vintage look**: A Tint Color of ~10% produces a warm sepia cast that closely resembles aged oil paint and early Technicolor matte paintings.
- **Crawl adds authenticity**: A subtle crawl (Crawl Int ~20–30%) adds the telltale artifact that signals "optical composite" to the viewer. Too much crawl breaks the illusion; too little looks too clean.
- **Grain matches textures**: Enabling grain in the matte region prevents it from looking "too digital" compared to a noisy input. The grain amplitude is small and adds photographic texture without overwhelming the image.
- **Combine with other programs**: Tableau is most powerful when the painted region is replaced with output from another program in a feedback chain, rather than just desaturation of the same input.
- **Invert Side for foreground mattes**: Use Invert Side to paint the foreground instead of the background — useful for simulating a glass painting placed close to the lens.
- **Angle snaps, not rotates**: The angle control quantizes to eight discrete slopes. If you need a specific tilt, work in the zone that gives the closest slope. Continuous rotation is not supported.

---

## Glossary

| Term | Definition |
|------|------------|
| **Alpha** | A per-pixel blend weight (0 = fully transparent, 1023 = fully opaque) controlling how two regions are composited. |
| **BT.601** | The ITU television standard defining the YUV color encoding used throughout the Videomancer video pipeline. |
| **Contrast Compression** | Reducing the dynamic range of a signal by pulling values toward mid-gray (512), making the image look flatter and more muted. |
| **DDS** | Direct Digital Synthesis; a technique for generating periodic waveforms using a phase accumulator that increments each clock cycle. |
| **Desaturation** | Reducing color saturation by blending chrominance channels toward their neutral value (512), shifting the image toward monochrome. |
| **Feather** | A gradual blend zone at the boundary between two composited regions, softening the transition to hide the matte line. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Glass Painting** | A traditional visual effects technique where scenery is painted onto glass placed between the camera and the live-action set. |
| **LFSR** | Linear Feedback Shift Register; a digital circuit that generates pseudo-random bit sequences, used here for film grain simulation. |
| **Matte** | A mask that defines which regions of a frame are replaced during compositing; the term also refers to the replacement region itself. |
| **Matte Crawl** | A flickering brightness artifact along the matte boundary, caused by mechanical instability in optical compositing systems. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Tint** | A uniform color cast applied to a region by adding fixed UV offsets, simulating colored paint or lacquer. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
