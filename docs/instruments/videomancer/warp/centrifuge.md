---
draft: true
sidebar_position: 42
slug: /instruments/videomancer/centrifuge
title: "Centrifuge"
image: /img/instruments/videomancer/centrifuge/centrifuge_hero_s1.png
description: "Every image has a hidden angular geometry."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import centrifuge_control_panel from '/img/instruments/videomancer/centrifuge/centrifuge_control_panel.png';
import centrifuge_source1_parrot from '/img/instruments/videomancer/centrifuge/centrifuge_source1_parrot.png';
import centrifuge_source2_fruit from '/img/instruments/videomancer/centrifuge/centrifuge_source2_fruit.png';
import centrifuge_source3_turtle from '/img/instruments/videomancer/centrifuge/centrifuge_source3_turtle.png';
import centrifuge_source4_pattern from '/img/instruments/videomancer/centrifuge/centrifuge_source4_pattern.png';
import centrifuge_source5_man from '/img/instruments/videomancer/centrifuge/centrifuge_source5_man.png';
import centrifuge_source6_paint from '/img/instruments/videomancer/centrifuge/centrifuge_source6_paint.png';
import centrifuge_hero_s1 from '/img/instruments/videomancer/centrifuge/centrifuge_hero_s1.png';
import centrifuge_hero_s2 from '/img/instruments/videomancer/centrifuge/centrifuge_hero_s2.png';
import centrifuge_hero_s3 from '/img/instruments/videomancer/centrifuge/centrifuge_hero_s3.png';
import centrifuge_hero_s4 from '/img/instruments/videomancer/centrifuge/centrifuge_hero_s4.png';
import centrifuge_hero_s5 from '/img/instruments/videomancer/centrifuge/centrifuge_hero_s5.png';
import centrifuge_hero_s6 from '/img/instruments/videomancer/centrifuge/centrifuge_hero_s6.png';
import centrifuge_ex1_s1 from '/img/instruments/videomancer/centrifuge/centrifuge_ex1_s1.png';
import centrifuge_ex1_s2 from '/img/instruments/videomancer/centrifuge/centrifuge_ex1_s2.png';
import centrifuge_ex1_s3 from '/img/instruments/videomancer/centrifuge/centrifuge_ex1_s3.png';
import centrifuge_ex1_s4 from '/img/instruments/videomancer/centrifuge/centrifuge_ex1_s4.png';
import centrifuge_ex1_s5 from '/img/instruments/videomancer/centrifuge/centrifuge_ex1_s5.png';
import centrifuge_ex1_s6 from '/img/instruments/videomancer/centrifuge/centrifuge_ex1_s6.png';
import centrifuge_ex2_s1 from '/img/instruments/videomancer/centrifuge/centrifuge_ex2_s1.png';
import centrifuge_ex2_s2 from '/img/instruments/videomancer/centrifuge/centrifuge_ex2_s2.png';
import centrifuge_ex2_s3 from '/img/instruments/videomancer/centrifuge/centrifuge_ex2_s3.png';
import centrifuge_ex2_s4 from '/img/instruments/videomancer/centrifuge/centrifuge_ex2_s4.png';
import centrifuge_ex2_s5 from '/img/instruments/videomancer/centrifuge/centrifuge_ex2_s5.png';
import centrifuge_ex2_s6 from '/img/instruments/videomancer/centrifuge/centrifuge_ex2_s6.png';
import centrifuge_ex3_s1 from '/img/instruments/videomancer/centrifuge/centrifuge_ex3_s1.png';
import centrifuge_ex3_s2 from '/img/instruments/videomancer/centrifuge/centrifuge_ex3_s2.png';
import centrifuge_ex3_s3 from '/img/instruments/videomancer/centrifuge/centrifuge_ex3_s3.png';
import centrifuge_ex3_s4 from '/img/instruments/videomancer/centrifuge/centrifuge_ex3_s4.png';
import centrifuge_ex3_s5 from '/img/instruments/videomancer/centrifuge/centrifuge_ex3_s5.png';
import centrifuge_ex3_s6 from '/img/instruments/videomancer/centrifuge/centrifuge_ex3_s6.png';

# Centrifuge

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: centrifuge_source1_parrot, after: centrifuge_hero_s1 },
    { label: "Fruit", before: centrifuge_source2_fruit, after: centrifuge_hero_s2 },
    { label: "Turtle", before: centrifuge_source3_turtle, after: centrifuge_hero_s3 },
    { label: "Pattern", before: centrifuge_source4_pattern, after: centrifuge_hero_s4 },
    { label: "Man", before: centrifuge_source5_man, after: centrifuge_hero_s5 },
    { label: "Paint", before: centrifuge_source6_paint, after: centrifuge_hero_s6 },
  ]}
/>
*Centrifuge splitting a sunlit porch into eight spinning colour wedges, each sector carrying a different luma and chroma offset as the angular wheel rotates through the frame.*

---

## Overview

Every image has a hidden angular geometry. Draw a line from any pixel to a chosen centre point, measure the angle, and you have partitioned the frame into radiating wedges — a colour wheel laid over the scene itself. Centrifuge makes that geometry visible by dividing the screen into angular sectors emanating from a configurable origin, applying a distinct luma offset and chroma tint to each sector, and then rotating the entire sector assignment over time. The result is a spinning kaleidoscope of colour-shifted wedges that turns the input video into a stained-glass rosette.

The angular classification is performed without trigonometric functions. The pipeline computes the signed horizontal and vertical distance from each pixel to the centre point, uses the signs to determine the quadrant, and compares the absolute magnitudes to subdivide each quadrant into two octants — yielding eight angular sectors from pure integer arithmetic. A frame counter, incremented by the Spin Spd parameter on each vertical sync, shifts the octant assignment over time so the colour pattern appears to rotate. In quad mode the eight octants collapse to four broader quadrants, producing wider, more dramatic colour bands. The name *Centrifuge* evokes the spinning separation this process creates — like a laboratory centrifuge that flings substances outward into distinct bands, the program flings tonal and chromatic identity outward along angular slices.

At gentle settings the effect is a subtle tonal rosette overlaid on the source — a soft warm-cool alternation that gives the image a hand-tinted, directional quality. At full contrast and colour intensity, the spinning sectors turn the frame into an aggressive colour wheel where each wedge carries its own vivid hue, the image content visible beneath the tint like stained glass held up to the sun. Mixed at partial wet, the sector colouring blends into the original palette, adding rotational colour energy without obliterating the source.

---

## Background

### Angular Partitioning Without Trigonometry

Computing the angle from a point to a centre normally requires an `atan2` function — expensive in silicon and ill-suited to a streaming pixel pipeline at 74.25 MHz. Centrifuge avoids trigonometry entirely by exploiting octant classification: the signs of dx and dy determine the quadrant (4 sectors), and comparing |dx| against |dy| subdivides each quadrant at the 45-degree diagonal (8 sectors). This is the same technique used in Bresenham-family algorithms and fast sprite rotation on early game consoles. The result is a piecewise-constant angular partition — each octant spans exactly 45 degrees — computed with only subtraction, sign extraction, and magnitude comparison, all completing in a single pipeline clock.

### Colour Wheel Tinting

Each of the eight sectors applies a different combination of luma offset and UV chroma offset to the input pixel. The offsets follow a complementary pattern: sector 0 brightens and shifts toward warm hues, sector 4 (the opposing wedge) darkens and shifts toward cool hues. Intermediate sectors apply proportionally scaled offsets, creating a gradual tonal rotation around the angular wheel. The overall effect is analogous to placing a multicoloured gel filter over a spotlight and rotating it — the hues sweep through the scene as the sector assignment cycles. Two palette modes (warm and cool) swap the U/V roles, flipping the colour circle orientation so that the same rotation can produce either amber-to-teal or magenta-to-green sweeps.

### Frame-Counter Rotation

The spinning animation is driven by a 16-bit frame counter that increments by the spin speed parameter on each vertical sync pulse. Only the upper three bits of the counter feed the rotation offset, so the angular wheel advances in discrete 45-degree steps. At low spin speeds, the sectors shift slowly — dwelling on each angular position for many frames before clicking to the next. At high speeds, the rotation becomes rapid, producing a strobing colour wheel that cycles through all eight sector assignments in rapid succession. The discrete stepping is a feature, not a limitation: it preserves the hard geometric sector boundaries that define the program's visual character.

### Octant vs Quadrant Modes

The Mode toggle collapses the eight 45-degree octants into four 90-degree quadrants by clearing the lowest bit of the sector index. In quadrant mode, pairs of adjacent octants receive identical colour treatment, doubling the angular width of each coloured band. The visual difference is significant: octant mode creates a fine pinwheel with eight narrow spokes of colour, while quadrant mode produces four broad sweeping quadrants — a simpler, bolder geometry that reads clearly even at small display sizes or through heavy downstream processing.

### Centre-Point Displacement

The centre of the angular partition is not fixed at the screen centre. Pots 1 and 2 (mapped internally to Center X and Center Y) move the origin point across the frame. The X coordinate is scaled to span roughly 0–2046 pixels (covering 1920 active), while Y spans 0–1023 (covering 1080 active at a slightly compressed ratio). Displacing the centre off-screen produces asymmetric sector geometries where only a few wedges are visible — a partial colour fan that sweeps across the frame edge. This makes the centre position a powerful compositional control, placing the rotational axis wherever the eye should be drawn.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├─ 1. Parameter Pre-Registration        (on vsync: latch pots, map center coords)
│
├─ 2. Pixel Counters                    (h_count, v_count from timing generator)
│
├─ 3. Stage 1 — Delta + Abs             (1 clk)
│      ├─ dx = h_count − center_x
│      ├─ dy = v_count − center_y
│      ├─ sign(dx), sign(dy)
│      └─ |dx|, |dy|
│
├─ 4. Stage 2 — Octant + Rotation       (1 clk)
│      ├─ Quadrant from sign(dx), sign(dy)
│      ├─ Octant from |dx| vs |dy|
│      ├─ sector = octant + rotation_offset
│      └─ Quad mode: sector(0) ← 0
│
├─ 5. Stage 3 — Per-Sector Colour Mod   (1 clk)
│      ├─ Y ← Y + luma_offset(sector, contrast)
│      ├─ U ← U + u_offset(sector, color_int, color_mode)
│      └─ V ← V + v_offset(sector, color_int, color_mode)
│
├─ 6. Stage 4 — Clamp 0..1023           (1 clk)
│
├─ 7. Interpolator Mix (×3 channels)    (4 clks — dry/wet crossfade)
│      └─ t = Mix: 0 = dry (input), 1023 = wet (sector-tinted)
│
├─ Sync/Data Delay Pipeline              (8-clock shift register for alignment)
│
└─ Output Mux
    ├─ Bypass off → mixed Y/U/V + aligned sync
    └─ Bypass on  → delayed input Y/U/V + aligned sync
```

The angular classification in stages 1 and 2 is the heart of the program. Stage 1 produces signed deltas from the centre point and decomposes them into sign bits and absolute magnitudes — all in one clock. Stage 2 uses those four pieces of information (two signs, one magnitude comparison) to classify the pixel into one of eight octants, then adds the frame-derived rotation offset to spin the assignment over time. The entire angular computation is purely combinational within each registered stage, requiring no multipliers, no lookup tables, and no BRAM.

The per-sector colour modification in stage 3 follows a complementary pattern: opposing sectors (0 vs 4, 1 vs 5, etc.) receive opposite-sign luma and chroma offsets. This creates a natural push-pull contrast between adjacent halves of the colour wheel — one side brightens while the other darkens, one side shifts warm while the other shifts cool. The colour mode toggle swaps which chroma axis receives the primary offset (U or V), rotating the entire hue palette by 90 degrees in the UV plane.

---

## Parameter Reference

<img src={centrifuge_control_panel} alt="Videomancer front panel with Centrifuge loaded"/>
*Videomancer's front panel with Centrifuge active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Spin Spd
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the rate at which the angular sector assignment rotates over time. Internally this parameter sets the frame counter increment — the amount added to a 16-bit accumulator on each vertical sync. The upper three bits of that accumulator become the rotation offset, so higher values cause faster stepping through the eight sector positions. At 0% the sectors are frozen in place; at 100% the colour wheel spins at maximum speed, cycling through all eight angular positions in rapid succession. Moderate values produce a slow, deliberate rotation that lets each colour arrangement linger before advancing. The discrete 45-degree stepping gives the rotation a mechanical, indexing quality rather than a smooth sweep.

---

#### Knob 2 — Sectors
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the vertical centre position of the angular partition. All sector boundaries radiate outward from this point. At midpoint, the origin sits near the vertical centre of the screen, producing a symmetric colour rosette. Moving toward 0% shifts the origin to the top of the frame, causing the sector wedges to fan downward; moving toward 100% shifts it to the bottom. Combined with Spin Spd, this lets you place the axis of rotation at any vertical position — anchoring the spinning colour wheel to a subject's head, to the horizon line, or to the frame edge for asymmetric partial-sector effects.

---

#### Knob 3 — Sep Dist
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the strength of the luma offset applied to each sector. At 0% no brightness modification occurs — all sectors share the input luminance. As the value increases, opposing sectors receive progressively larger positive and negative luma offsets, brightening one half of the colour wheel while darkening the other. At full strength, the contrast between adjacent sectors is dramatic: some wedges are pushed toward white clipping while their opposites are driven toward black. The upper six bits of the 10-bit register value scale the offset magnitude, providing 64 discrete contrast levels. Intermediate sectors receive half the offset of their neighbours, creating a smooth brightness gradient around the angular wheel.

---

#### Knob 4 — Band W
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the magnitude of the chroma offset applied per sector. At 0% the sectors differ only in brightness — no colour tinting occurs. As the value increases, each sector acquires a progressively stronger UV shift, pushing it toward a distinct hue in the colour circle. The warm/cool palette mode (Toggle 9) determines which axis receives the primary offset. At full intensity the colour separation is vivid: opposing sectors carry complementary hues, and the spinning wheel becomes a rotating chromatic filter laid over the source image. Like the contrast control, the upper six bits are used, giving 64 steps of colour intensity.

---

#### Knob 5 — Feather
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the horizontal centre position of the angular partition. The 10-bit register value is scaled to approximately double resolution, spanning 0–2046 pixels to cover the full 1920-pixel active width. At midpoint, the origin falls near the horizontal centre of the screen. Moving left shifts all sector boundaries so that the wedges fan out from the left side of the frame; moving right does the opposite. Off-screen centre positions are valid and produce sector geometries where only a subset of wedges are visible — a partial colour fan that adds asymmetry and directional emphasis to the composition.

---

#### Knob 6 — Tilt
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

This parameter is reserved in the current firmware revision and has no effect on the processing pipeline. The register value is read but not mapped to any internal signal. Future firmware versions may assign it to additional processing features such as angular offset bias or sector width modulation. Leaving the knob at its default midpoint position is recommended.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Mode** | Radial | Spiral |
| **8 — Dir** | CW | CCW |
| **9 — Color** | Source | Tinted |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control independent aspects of the processing: Mode (7) sets the number of angular sectors, Dir (8) and Color (9) control the colour palette orientation, Animate (10) is reserved, and Bypass (11) overrides all processing. Mode and Color interact closely — Mode determines how many sectors are visible, while Color determines which of two complementary hue palettes is applied. Dir controls the spin direction via the frame counter: clockwise increments, counter-clockwise decrements. The toggles can be combined freely; the most visually significant combination is Mode + Color, which together define the geometric and chromatic character of the sector pattern.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfades between the dry input signal and the sector-tinted processed signal. At 0% (fader down), the output is the unmodified source — no sector colouring is visible. At 100% (fader up), the output is the fully tinted sector image. Intermediate positions blend the two, allowing you to dial in a subtle angular colour cast over the source without completely replacing its natural palette. This is the master intensity control for the effect: keeping it at 30–50% adds a gentle directional colour toning, while pushing toward 100% commits fully to the colour-wheel aesthetic.

---

## Guided Exercises

These exercises progress from a static sector overlay through animated colour-wheel spinning to fine compositional control via centre-point placement. Each exercise introduces new parameters while reinforcing the relationship between angular geometry, rotation speed, and colour palette.

### Exercise 1: Static Colour Rosette

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: centrifuge_source1_parrot, after: centrifuge_ex1_s1 },
    { label: "Fruit", before: centrifuge_source2_fruit, after: centrifuge_ex1_s2 },
    { label: "Turtle", before: centrifuge_source3_turtle, after: centrifuge_ex1_s3 },
    { label: "Pattern", before: centrifuge_source4_pattern, after: centrifuge_ex1_s4 },
    { label: "Man", before: centrifuge_source5_man, after: centrifuge_ex1_s5 },
    { label: "Paint", before: centrifuge_source6_paint, after: centrifuge_ex1_s6 },
  ]}
/>
*Static Colour Rosette — simulated result across source images.*
**Source**: A high-contrast photograph with clear geometry — architectural lines or a centred portrait work well.

**Objective**: Understand how the angular sector classification divides the frame into coloured wedges and how contrast and colour intensity create the tonal separation between sectors.

1. **Freeze the wheel**: Set Spin Spd to 0% so the sector assignment does not move.
2. **Centre the origin**: Set Sectors and Tilt both to ~50%, placing the angular origin near the frame centre.
3. **Add contrast**: Slowly increase Sep Dist from 0% to ~60%. Watch as opposing sectors brighten and darken relative to each other — the image acquires a directional tonal gradient.
4. **Add colour**: Increase Band W from 0% to ~50%. Each sector now carries a distinct hue — a chromatic rosette overlaid on the source.
5. **Switch to quad mode**: Toggle Mode (Toggle 7) to Spiral. The eight narrow wedges collapse to four broad quadrants — a simpler, bolder colour partition.
6. **Blend with mix**: Pull the Mix fader to ~40%. The sector tinting becomes a subtle colour overlay rather than a dominant effect.

**Key concepts**: Octant classification divides the screen into 8 angular sectors from a centre point, contrast and colour intensity control the magnitude of per-sector luma and chroma offsets, quad mode merges octant pairs into broader quadrants

---

### Exercise 2: Spinning Colour Wheel

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: centrifuge_source1_parrot, after: centrifuge_ex2_s1 },
    { label: "Fruit", before: centrifuge_source2_fruit, after: centrifuge_ex2_s2 },
    { label: "Turtle", before: centrifuge_source3_turtle, after: centrifuge_ex2_s3 },
    { label: "Pattern", before: centrifuge_source4_pattern, after: centrifuge_ex2_s4 },
    { label: "Man", before: centrifuge_source5_man, after: centrifuge_ex2_s5 },
    { label: "Paint", before: centrifuge_source6_paint, after: centrifuge_ex2_s6 },
  ]}
/>
*Spinning Colour Wheel — simulated result across source images.*
**Source**: A slowly moving video source — panning landscape footage or a gently moving subject against a neutral background.

**Objective**: Explore the rotation animation and the interplay between spin speed, direction, and colour palette.

1. **Set the full effect**: Sep Dist ~50%, Band W ~60%, Mix ~80%.
2. **Start slow rotation**: Set Spin Spd to ~20%. The colour wheel begins to advance in discrete 45-degree steps — slow enough to see each sector position individually.
3. **Increase speed**: Push Spin Spd to ~60%. The stepping accelerates into a rapid colour strobe. Notice how the discrete rotation creates a flickering pattern rather than a smooth sweep.
4. **Reverse direction**: Toggle Dir (Toggle 8) to CCW. The colour wheel now rotates in the opposite direction.
5. **Swap colour palette**: Toggle Color (Toggle 9) to Tinted. The hue progression shifts from warm-cool to blue-yellow, changing the character of the spinning pattern while keeping the geometry identical.
6. **Return to octant mode**: If still in quad mode, switch Mode (Toggle 7) back to Radial. The eight-sector pattern creates a finer, more intricate rotation.

**Key concepts**: Spin Spd controls the frame counter increment determining rotation rate, rotation advances in discrete 45-degree steps via the upper 3 bits of a 16-bit counter, Dir toggle reverses the increment direction, Color toggle swaps between warm and cool UV palettes

---

### Exercise 3: Off-Centre Composition

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: centrifuge_source1_parrot, after: centrifuge_ex3_s1 },
    { label: "Fruit", before: centrifuge_source2_fruit, after: centrifuge_ex3_s2 },
    { label: "Turtle", before: centrifuge_source3_turtle, after: centrifuge_ex3_s3 },
    { label: "Pattern", before: centrifuge_source4_pattern, after: centrifuge_ex3_s4 },
    { label: "Man", before: centrifuge_source5_man, after: centrifuge_ex3_s5 },
    { label: "Paint", before: centrifuge_source6_paint, after: centrifuge_ex3_s6 },
  ]}
/>
*Off-Centre Composition — simulated result across source images.*
**Source**: A portrait or any image with an identifiable focal point that is not centred in the frame.

**Objective**: Use the centre-point controls to anchor the angular partition to a compositional feature, creating asymmetric sector patterns.

1. **Prepare the base**: Sep Dist ~45%, Band W ~40%, Spin Spd ~15%, Mix ~70%.
2. **Default centre**: With Feather and Sectors both at ~50%, the origin is near the screen centre. Observe the symmetric colour rosette.
3. **Move the origin**: Shift Feather (horizontal centre) toward ~25%. The angular origin moves left — the sector wedges now fan out from the left side of the frame, creating an asymmetric colour field.
4. **Vertical offset**: Shift Sectors (vertical centre) toward ~75%. The origin drops to the lower quarter of the frame, and the wedges spread upward across the image.
5. **Extreme displacement**: Push Feather to ~5%. The origin is near the left edge — only three or four sectors are visible across the frame, creating a wide colour gradient rather than a complete rosette.
6. **Anchor to subject**: Adjust both centre controls to place the angular origin directly on the subject's face or a key compositional element. The colour wedges now radiate from the subject, drawing the eye toward it.

**Key concepts**: Centre X and Y move the angular origin across the frame, off-centre positions create asymmetric sector patterns where only a subset of wedges are visible, anchoring the origin to a subject creates a compositional focal point

---


## Tips

- **Start with zero spin**: Set Spin Spd to 0% when learning the controls. A static colour rosette is much easier to read than a spinning one. Add rotation once you understand the sector geometry.
- **Contrast before colour**: Increase Sep Dist (luma contrast) before Band W (colour intensity). The luma structure of the effect is more visible and easier to evaluate than the chroma shift alone.
- **Centre is composition**: The angular origin is the most powerful compositional control. Moving it off-centre or anchoring it to a subject transforms the effect from a decorative overlay to a directed focal element.
- **Quad mode for bold looks**: Use Spiral (quadrant) mode when you want large, graphic colour blocks. Use Radial (octant) mode for finer, more intricate colour pinwheels.
- **Mix for subtlety**: The Mix fader at 20–40% blends the sector colouring into the source as a gentle directional tint — far more usable in live performance than 100% wet.
- **Direction for variety**: Swap the Dir toggle during a performance to reverse the colour wheel's spin. The sudden reversal creates a visual accent that draws attention.
- **Palette swap is instant**: Toggling Color between Source and Tinted instantly changes the hue character of the wheel without affecting brightness or geometry. Use it as a mood switch.
- **Bypass for sanity**: When the spinning colour wheel becomes overwhelming, tap Bypass (Toggle 11) for an instant return to the source image. There is no glitch — the transition is seamless.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bresenham algorithm** | A family of efficient integer-only rasterisation algorithms used in computer graphics; Centrifuge's octant classification uses the same sign-and-magnitude technique. |
| **Chrominance** | The colour-difference components (U and V) of a YUV video signal, encoding hue and saturation independently of brightness. |
| **Complementary hues** | Colours positioned opposite each other on the colour wheel, such as warm amber and cool cyan, which create maximum contrast when juxtaposed. |
| **Frame counter** | A register that increments once per video frame (at vsync), used here to drive the rotation animation of the sector pattern. |
| **Luma offset** | A signed brightness adjustment added to or subtracted from the Y channel, brightening or darkening the affected region. |
| **Octant** | One of eight 45-degree angular sectors produced by sign-and-magnitude classification of pixel coordinates relative to a centre point. |
| **Quadrant** | One of four 90-degree angular sectors; in Centrifuge, quadrant mode merges adjacent octant pairs into broader colour bands. |
| **UV colour plane** | The two-dimensional space defined by the U and V chrominance axes, in which any hue and saturation can be represented as a point. |
| **Vsync (Vertical Sync)** | A timing pulse marking the start of each new video frame, used as the trigger for per-frame parameter updates and counter increments. |
| **YUV** | A colour model that separates luminance (Y) from two chrominance components (U and V), widely used in video signal processing. |

---
