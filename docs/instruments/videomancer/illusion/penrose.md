---
draft: true
sidebar_position: 194
slug: /instruments/videomancer/penrose
title: "Penrose"
image: /img/instruments/videomancer/penrose/penrose_hero.png
description: "The Penrose triangle is perhaps the most famous impossible object — a three-bar figure that appears to represent a solid three-dimensional triangle, yet..."
---

import penrose_before_after from '/img/instruments/videomancer/penrose/penrose_before_after.png';
import penrose_control_panel from '/img/instruments/videomancer/penrose/penrose_control_panel.png';
import penrose_exercise1_result from '/img/instruments/videomancer/penrose/penrose_exercise1_result.png';
import penrose_exercise2_result from '/img/instruments/videomancer/penrose/penrose_exercise2_result.png';
import penrose_exercise3_result from '/img/instruments/videomancer/penrose/penrose_exercise3_result.png';
import penrose_hero from '/img/instruments/videomancer/penrose/penrose_hero.png';
import penrose_source1_kodim01 from '/img/instruments/videomancer/penrose/penrose_source1_kodim01.png';
import penrose_source2_kodim02 from '/img/instruments/videomancer/penrose/penrose_source2_kodim02.png';
import penrose_source3_kodim01_bw from '/img/instruments/videomancer/penrose/penrose_source3_kodim01_bw.png';

# Penrose

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={penrose_hero} alt="Penrose hero image"/>
*Penrose overlaying impossible triangle wireframes on live video, depth-cue shading creating spatial contradiction at every junction.*
<img src={penrose_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Penrose applied.*

---

## Overview

The Penrose triangle is perhaps the most famous impossible object — a three-bar figure that appears to represent a solid three-dimensional triangle, yet cannot exist in Euclidean space. Each junction connects two bars at a right angle in a way that is locally plausible but globally contradictory. Roger Penrose popularized the figure in 1958 and M.C. Escher used it repeatedly in his lithographs. Penrose brings this optical illusion into the domain of real-time video processing.

The program draws wireframe outlines by computing the perpendicular distance from each pixel to three axis-aligned bar centrelines. For the Penrose triangle shape, the three axes approximate 0°, 60°, and 120° using shift-based slope calculations — no hardware multipliers are needed. When the absolute distance from any centreline falls below a thickness threshold, that pixel is on the wireframe and receives a brightness boost, a solid replacement, a shadow subtraction, or a warm glow depending on the selected style. At bar junctions where two distance tests overlap, depth-cue shading darkens the intersection to create the illusion of one bar passing behind another.

Four shape modes are available: the classic Penrose triangle, a staircase (horizontal + vertical + diagonal bars), a Necker cube (three orthogonal edges), and a Blivet/trident (three parallel vertical bars with a connecting top). A repetition control tiles the shape across the screen using power-of-two bitmask modular coordinates, and a spin toggle adds per-frame phase offset for continuous rotation.

---

## Background

### Impossible Objects and Visual Paradox

An impossible object is a two-dimensional drawing that the visual system initially interprets as a projection of a three-dimensional structure, but which cannot actually exist in three dimensions because it contains contradictory depth cues. The Penrose triangle (also called the tribar) is the archetype: three mutually perpendicular bars connected in a closed loop. At each corner, the bars appear to join at a right angle — but following the loop around, you return to the starting bar from the wrong side. The illusion works because human vision processes local depth cues (T-junctions, occlusion, shading) independently before attempting global consistency.

### Wireframe Rendering via Distance Fields

Traditional wireframe rendering on a GPU draws line segments between vertices. On an FPGA without a line-drawing engine, Penrose uses a different approach borrowed from signed distance field (SDF) rendering. For each pixel, the program computes the perpendicular distance to each bar centreline. If the distance is less than a threshold (the line thickness), the pixel is "on" the wireframe. This approach is massively parallel — every pixel can be tested independently — and requires only subtraction, absolute value, and comparison operations. The 60° and 120° slopes for the triangle are approximated as `cx + cy>>1` and `-cx + cy>>1`, avoiding multiplies entirely.

### Depth Cue and the Impossibility Illusion

The depth-cue shading at junctions is the key to the impossible-object illusion. Where two bars overlap, the wireframe brightness is attenuated by a configurable shift amount. This simulates the visual cue that one bar passes behind the other. Because the shading is uniform at all junctions (rather than alternating front/back), the contradictory depth relationships are preserved — each bar simultaneously appears to be both in front of and behind its neighbor, exactly as in the original Penrose drawing.

### Tiling and Repetition

The Count control tiles the shape across the screen by applying a power-of-two bitmask to the centred pixel coordinates. With a 512-pixel repeat, coordinates wrap modulo 512, placing two copies across the screen. At 256-pixel repeat, four copies appear; at 128, eight. The bitmask approach avoids division — it simply masks off high-order bits, equivalent to modular arithmetic with a power-of-two modulus. Each tile is re-centred by subtracting half the repeat distance.

### Style Modes and Compositing

Four compositing styles determine how the wireframe interacts with the source video. **Wire** adds brightness to the source — the wireframe is transparent with a white glow. **Solid** replaces the source entirely with the wireframe color at neutral chroma. **Shadow** subtracts brightness — the wireframe appears as a dark etching. **Glow** adds brightness and shifts chroma toward warm tones (reducing U, increasing V), creating a golden luminous effect.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Parameter Derivation ───────────────────────────────────────
│   ├─ Size → half_size (64..576 px half-extent)
│   ├─ Line Thk → thickness (1..32 px)
│   ├─ Bright → wire_bright (0..1023 luma)
│   ├─ Depth Cue → depth_scale (0..4 shift levels)
│   ├─ Count → rep_shift (0=single, 1=2x, 2=4x, 3=8x)
│   └─ Rotation → offset / Spin → frame-count animation
│
├── Stage 1: Coordinate Offset (1 clk) ─────────────────────────
│   ├─ Centre at screen midpoint (960, 540)
│   ├─ Add rotation pot offset + spin animation phase
│   └─ Tile repetition via power-of-2 bitmask
│
├── Stage 2: Line Distance (1 clk) ─────────────────────────────
│   ├─ Axis A: horizontal bar |cy − half_size|
│   ├─ Axis B: 60° approx |cx + cy>>1 − half_size|
│   ├─ Axis C: 120° approx |−cx + cy>>1 − half_size|
│   └─ (Shape-dependent: staircase, cube, trident variants)
│
├── Stage 3: Threshold + Depth Cue (1 clk) ─────────────────────
│   ├─ Each |dist| < thickness → on_wire
│   ├─ Bounds check: all distances < 2× half_size
│   ├─ Junction detect: 2+ bars overlap → near_junc
│   └─ Shade: depth_scale shifts brightness at junctions
│
├── Stage 4: Wireframe Compose (1 clk) ─────────────────────────
│   ├─ Wire: source + wire_shade (add)
│   ├─ Solid: replace with wire_shade, neutral UV
│   ├─ Shadow: source − wire_shade (subtract)
│   └─ Glow: source + wire_shade, warm UV shift
│
├── Mix: Interpolator (4 clk) ──────────────────────────────────
│   └─ Y/U/V wet/dry crossfade via Mix fader
│
├── Sync Delay ─────────────────────────────────────────────────
│   └─ 8-clock shift register for hsync/vsync/field/data
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The core of the algorithm is the distance-to-line test in Stage 2. For the Penrose triangle, the three bar centrelines approximate 0°, 60°, and 120° using shift-based slope calculations: `cy`, `cx + cy>>1`, and `-cx + cy>>1`. These avoid multiplies while providing reasonable visual approximations of the equilateral triangle geometry. The bounds check in Stage 3 ensures wireframe pixels only appear within the shape's extent (2× half_size from centre), preventing stray lines from extending to the screen edges.

The depth-cue junction shading is a critical visual element — it darkens pixels where two or more bars overlap, simulating occlusion. Because the darkening is applied uniformly (not alternating front/back), the impossible-object illusion is preserved. The style selection in Stage 4 determines whether the wireframe adds to, replaces, subtracts from, or glows over the source video.

---

## Parameter Reference

<img src={penrose_control_panel} alt="Videomancer front panel with Penrose loaded"/>
*Videomancer's front panel with Penrose active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Size
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the spatial extent of the shape by setting the half-size parameter, which determines how far each bar centreline sits from the screen centre. At minimum, the shape is a tiny figure in the centre of the screen. At maximum, the bars extend nearly to the screen edges. The half-size is computed as `(pot >> 1) + 64`, giving a range of 64 to 576 pixels. This control interacts strongly with Count — larger shapes may overlap when tiled.

---

#### Knob 2 — Line Thk
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the wireframe stroke width in pixels. The thickness is derived as `(pot >> 5) + 1`, giving a range of 1 to 33 pixels. Thin lines produce a delicate wireframe drawing; thick lines create bold, architectural bars. At maximum thickness, the bars become wide enough to overlap at junctions even without the depth-cue shading, creating solid filled regions.

---

#### Knob 3 — Rotation
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Adds a horizontal offset to the centred coordinates, effectively panning the shape left or right across the screen. The offset is `pot − 512`, centred at zero. When the Spin toggle is active, this control is overridden by the animation phase. When Spin is off, Rotation provides manual positioning of the shape along the horizontal axis.

---

#### Knob 4 — Count
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls shape repetition via power-of-two tiling. Below 25%, a single shape appears at the screen centre. From 25–50%, the shape repeats every 512 pixels (approximately 2 copies across HD width). From 50–75%, the repeat period is 256 pixels (4 copies). Above 75%, the period is 128 pixels (8 copies). Each tile is re-centred so the shape appears symmetrically within its cell.

---

#### Knob 5 — Bright
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the brightness of the wireframe lines. This value is used directly as a 10-bit luma level in all four style modes. In Wire mode, it is added to the source luma. In Solid mode, it replaces the source. In Shadow mode, it is subtracted. In Glow mode, it is added to luma and also drives a warm chroma shift. At zero, the wireframe is invisible regardless of style.

---

#### Knob 6 — Depth Cue
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the strength of depth-cue shading at bar junctions. The pot value is quantised to five levels (0–4), each representing a right-shift applied to the wireframe brightness at junction pixels. At level 0, junctions are drawn at full brightness (no depth cue). At level 4, junction brightness is reduced to 1/16 of the line brightness, creating strong occlusion shading. This is the control that makes the impossible-object illusion convincing — moderate depth cue (levels 1–2) produces the most natural-looking spatial contradiction.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Shape** | Triangle | Stairs |
| **8 — Style** | Wire | Solid |
| **9 — Spin** | Off | On |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control shape selection (2-bit), rendering style (2-bit with bit overlap), spin animation, frame-based animation, and bypass. Note that the Style toggle (Switch 8) shares bit 1 with Shape (Switch 7) and bit 3 with Animate (Switch 10) due to the VHDL register packing — `s_style_bits <= registers_in(6)(3) & registers_in(6)(1)`. This means changing Shape or Animate may also alter the rendering style. This is a known hardware quirk that can be used creatively.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade between the source video (dry) and the wireframe-composited output (wet). At 0%, only the original source is visible. At 100%, the full wireframe effect is applied. Intermediate values blend the two, creating a translucent wireframe overlay. The crossfade uses three interpolator instances (one per Y/U/V channel) with 4-clock latency.

---

## Guided Exercises

These exercises explore the four shape modes, depth-cue shading, tiling, and compositing styles. Each builds progressively from basic wireframe overlay to complex tiled compositions.

### Exercise 1: Classic Penrose Triangle

<img src={penrose_exercise1_result} alt="Classic Penrose Triangle result"/>
*Classic Penrose Triangle — simulated result across source images.*
**Source**: A static or slowly moving camera feed with a medium-brightness, low-contrast background (e.g., a plain wall or sky gradient).

**Objective**: Draw a centered Penrose triangle wireframe and explore depth-cue shading to create the impossible-object illusion.

1. **Basic triangle**: Confirm Shape is set to Triangle and Style to Wire. A wireframe triangle should appear centred on the screen.
2. **Adjust size**: Sweep Size from minimum to maximum. Watch the triangle grow from a small figure to a screen-filling shape.
3. **Line thickness**: Increase Line Thk to about 40%. The thin lines become thick architectural bars.
4. **Depth cue**: Slowly increase Depth Cue from 0% to maximum. At the bar junctions, the brightness darkens progressively, simulating one bar passing behind another.
5. **Brightness**: Sweep Bright to control the wireframe intensity. At low values, the wireframe is a subtle ghost over the video.

**Key concepts**: Distance-field wireframe rendering, depth-cue shading at junctions creates the impossible-object illusion, the triangle uses 0°/60°/120° shift-approximated slopes

---

### Exercise 2: Tiled Impossible Staircase

<img src={penrose_exercise2_result} alt="Tiled Impossible Staircase result"/>
*Tiled Impossible Staircase — simulated result across source images.*
**Source**: A brightly lit scene with varied content — a cityscape, bookshelf, or garden.

**Objective**: Explore the staircase shape mode and repetition tiling.

1. **Switch to staircase**: Set Shape to Stairs. The wireframe changes to horizontal, vertical, and diagonal bars.
2. **Enable tiling**: Increase Count to about 60%. Four copies of the staircase appear across the screen.
3. **Adjust size**: Reduce Size to about 30% so each tiled copy fits within its cell without overlapping.
4. **Shadow style**: Switch Style to Shadow. The wireframe subtracts from the source, creating dark etchings over the bright video.
5. **Animate**: Enable Spin to see the tiled staircase pattern translate continuously.
6. **Depth cue**: Set Depth Cue to about 40% to add junction shading within each tiled copy.

**Key concepts**: Staircase uses horizontal/vertical/diagonal centrelines, tiling via bitmask modular coordinates, Shadow style subtracts brightness

---

### Exercise 3: Glowing Trident Composition

<img src={penrose_exercise3_result} alt="Glowing Trident Composition result"/>
*Glowing Trident Composition — simulated result across source images.*
**Source**: Dark or low-key footage — night scenes, dimly lit interiors, or abstract dark textures.

**Objective**: Use the Glow compositing style with the Trident shape to create luminous impossible objects over dark video.

1. **Trident shape**: Set Shape to Trident. Three parallel vertical bars with a connecting structure appear.
2. **Glow style**: Switch Style to Glow. The wireframe adds brightness and pushes chroma warm.
3. **High brightness**: Set Bright to about 80%. The wireframe glows intensely against the dark source.
4. **Depth cue**: Set Depth Cue to about 50%. Junction shading adds three-dimensionality.
5. **Mix blend**: Reduce Mix to about 70%. The glow becomes translucent, blending with the dark source.
6. **Size and count**: Try different Size and Count combinations to fill the screen with a repeating pattern of glowing tridents.
7. **Spin**: Enable Spin and Animate for continuous motion of the glowing pattern.

**Key concepts**: Glow style adds luma and shifts UV warm, Trident shape uses three parallel vertical bars, depth cue adds dimensional illusion to flat wireframe

---


## Tips

- **Depth Cue is the key to the illusion**: Without junction shading, the wireframe is just a geometric overlay. With moderate Depth Cue (40–60%), the darkened junctions create the perception of bars passing behind each other — the essence of the impossible object.
- **Thick lines make strong shapes**: Line Thk above 30% creates bold architectural bars rather than thin wireframe lines. Combined with Solid style, this produces clean geometric graphics.
- **Tiling fills the screen**: Count at 75%+ creates a dense repeating pattern of impossible objects. Reduce Size proportionally so each copy fits within its tile cell.
- **Style bit overlap is a feature**: The shared bits between Shape, Style, and Animate create unexpected style changes when toggling other controls. Explore these interactions for happy accidents.
- **Glow for dark backgrounds**: The Glow style shines brightest against dark or black video sources. Pair with the Trident shape for science-fiction-style luminous wireframes.
- **Spin + Rotation for compound motion**: Spin provides continuous translation while Rotation offsets the starting position. Together they create orbiting or scanning wireframe patterns.
- **Mix for subtle overlay**: Reducing Mix to 30–50% creates a ghostly, transparent wireframe that sits within the video rather than dominating it.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bitmask** | A binary mask applied to coordinates via AND operation, producing modular wrapping at power-of-two boundaries for tiling. |
| **Blivet** | An impossible object consisting of three cylindrical prongs that appear to merge into two rectangular bars; also known as the Devil's Fork or impossible trident. |
| **Depth Cue** | A visual signal (shading, occlusion, size) that suggests relative distance. In Penrose, junction shading simulates bar overlap. |
| **Distance Field** | A function that returns the perpendicular distance from each pixel to a geometric primitive. Used for wireframe rendering without explicit line drawing. |
| **FPGA** | Field-Programmable Gate Array; the reconfigurable hardware chip that implements Videomancer's real-time video processing. |
| **Impossible Object** | A two-dimensional drawing that appears to depict a three-dimensional structure but contains contradictory depth cues, making it physically unrealizable. |
| **Necker Cube** | An ambiguous wireframe cube drawing that can be perceived from two different orientations, named after crystallographer Louis Albert Necker. |
| **Penrose Triangle** | An impossible object consisting of three bars joined at right angles in a closed triangular loop; also known as the tribar. |
| **Pipeline** | A chain of processing stages where each stage performs one operation per clock cycle on streaming pixel data. |
| **SDF** | Signed Distance Field; a rendering technique where each pixel stores its signed perpendicular distance to the nearest surface boundary. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V); the native format of Videomancer's 30-bit video pipeline. |
