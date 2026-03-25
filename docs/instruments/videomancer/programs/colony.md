---
draft: true
sidebar_position: 56
slug: /instruments/videomancer/colony
title: "Colony"
image: /img/instruments/videomancer/colony/colony_hero.png
description: "Colony simulates the territorial expansion of bacterial cultures on a nutrient agar plate."
---

![Colony hero image](/img/instruments/videomancer/colony/colony_hero_s1.png)
*Four bacterial colonies expanding from quadrant centers, their colored territories meeting at bright boundary lines that map a living Voronoi diagram across the screen.*

---

## Overview

**Colony** is an organic synthesis program that simulates the territorial expansion of bacterial cultures across the video frame. Four colony seed points, fixed at the centers of each screen quadrant, grow outward over time. Each pixel is claimed by its nearest colony, and the boundaries where two territories meet are detected and highlighted as bright dividing lines. The result is a living ***Voronoi diagram***: a partition of space defined by proximity: that evolves frame by frame.

What makes Colony compelling is its combination of mathematical determinism and organic unpredictability. The colony boundaries follow strict nearest-neighbor geometry, but a linear feedback shift register injects noise at the growth fronts, producing ragged, irregular edges that look more like a petri dish than a geometry textbook. You can freeze the colonies in place for a static territorial map, let them expand endlessly, or set them pulsing in and out like breathing organisms.

Colony operates on a YUV 4:4:4 30-bit video stream and processes HD video at half clock rate. Its four-stage pipeline uses no block RAM: all territory computation is purely combinational, built from Manhattan distance calculations and a simple comparison tree.

:::note
Colony is a ***synthesis*** program. It generates its own imagery rather than transforming an incoming video signal, though it does blend the colony pattern with the input using the Mix fader.
:::

### What's In a Name?

The name ***Colony*** draws from microbiology, where a ***colony*** is a cluster of microorganisms growing on a nutrient medium. When multiple bacterial species are cultured on the same plate, they expand outward from their inoculation points until they encounter a neighbor. The boundary between two colonies is a ***zone of mutual exclusion***: neither species can cross into the other's territory. Colony recreates this biological turf war in real time, with each pixel on screen serving as a tiny parcel of contested ground.

---

## Quick Start

1. Flip **Video Mod** (Switch 9) to **On** to start animation. Four colored territories begin expanding from the corners of each quadrant.
2. Turn **Growth Sp** (Knob 1) clockwise to speed up the expansion. The colony edges creep outward faster, and the boundary lines between them shift as territories grow.
3. Adjust **Ring Sp** (Knob 3) to widen or narrow the bright boundary lines where colonies meet. At higher values, the exclusion zones become thick, luminous bands.
4. Flip **Reset** (Switch 10) to **On** and back to **Off** to clear all growth and watch the colonies expand from scratch.

---

## Parameters

![Videomancer front panel with Colony loaded](/img/instruments/videomancer/colony/colony_control_panel.png)
*Videomancer's front panel with Colony active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Growth Sp

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Growth Sp** controls how quickly the colony radii expand per video frame. When animation is active, each frame advances a ***DDS accumulator***: a digital phase counter: by an amount proportional to this knob. At the lowest setting, colonies barely creep outward between frames, producing slow, deliberate expansion. At the highest setting, the territories fill the screen rapidly, racing to claim every pixel. In monotonic mode, colonies grow until they saturate; in pulse mode, the speed determines how quickly the territories breathe in and out.

:::tip
Very low Growth Sp values paired with a live camera create a sense of geological time: the boundaries shift so slowly you almost don't notice until you look away and back.
:::

---

### Knob 2 — Colonies

| Property | Value |
|----------|-------|
| Range | 2 – 8 |
| Default | 5 |

**Colonies** sets how many of the four possible colony seed points are active. The VHDL quantizes this knob into four tiers: at the lowest setting, only one colony fills the screen; midway through the range, two or three colonies carve the frame into sections. At the highest setting, all four quadrant colonies compete for territory. Fewer colonies produce simpler compositions with longer boundary lines; more colonies create an intricate web of dividing walls.

---

### Knob 3 — Ring Sp

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Ring Sp** adjusts the width of the ***mutual exclusion zone***: the bright boundary band that appears where two colony territories come closest to each other. The boundary detector compares the distance to the nearest colony against the distance to the second-nearest colony; when the difference falls below a threshold set by this knob, the pixel is marked as a boundary. At the lowest setting, the boundaries are razor-thin bright lines. As you increase Ring Sp, the bright zones widen into thick luminous bands, and the colony interiors shrink. At extreme values, the boundaries dominate the image, and the colony interiors become small pools surrounded by broad walls of light.

---

### Knob 4 — Border W

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Border W** is a color intensity parameter that influences the saturation of colony tinting. At lower values, colony interiors appear more muted and neutral. As you increase this control, the color effect becomes more pronounced. The visual impact of this parameter is subtle and works best in combination with the **Border** toggle (Switch 8) set to **None**, which enables colored colony rendering.

---

### Knob 5 — Color Sp

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Color Sp** adjusts how much of the underlying source video shows through the colony pattern. At lower values, the colony color dominates the interior regions. At higher values, the input signal bleeds through the colony tinting, creating a translucent overlay effect. This parameter interacts with the **Mix** fader: Color Sp affects the colony composite while Mix controls the overall wet/dry balance.

---

### Knob 6 — Opacity

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Opacity** controls the amount of ***LFSR noise*** injected at colony growth fronts. The noise modulates the inside/outside test at each pixel, producing ragged, irregular colony edges instead of smooth geometric arcs. At the lowest setting, maximum noise is applied: edges become wildly jagged and unpredictable, resembling the irregular borders of real bacterial cultures. As you increase Opacity, the noise is progressively attenuated, and colony edges become smoother and more geometric. At the highest setting, only minimal noise remains, and the boundaries approach clean arcs defined purely by Manhattan distance.

:::note
The relationship is ***inverse***: turning Opacity up produces smoother edges, not rougher ones. Think of it as turning up the opacity of the clean geometric shape underneath the noise.
:::

---

### Switch 7 — Pattern

| Property | Value |
|----------|-------|
| Off | Colony |
| On | Moss |
| Default | Colony |

**Pattern** selects between two colony growth behaviors. In the default **Colony** position, radii grow monotonically: once a territory expands, it stays expanded, and growth stops only when the radius accumulator saturates. In the **Moss** position, the radii follow a ***triangle wave***: they grow outward, fold back to zero, and grow again, producing a pulsing, breathing effect where colony territories rhythmically expand and contract. The pulse rate depends on Growth Sp (Knob 1).

---

### Switch 8 — Border

| Property | Value |
|----------|-------|
| Off | Dark |
| On | None |
| Default | Dark |

**Border** selects between monochrome and colored colony rendering. In the default **Dark** position, colony interiors are rendered without chrominance: all colonies share the same neutral gray tone, differentiated only by the bright boundary lines between them. When set to **None**, each colony receives a distinct hue tint: red, green, blue, and magenta. The color is derived from fixed UV offsets applied to the colony interior pixels, with luminance darkened slightly to distinguish interior regions from boundaries.

:::tip
The name **Dark** / **None** may seem counterintuitive. Think of it as describing the boundary style: **Dark** colonies have dark monochrome interiors with bright borders, while **None** removes the monochrome restriction and lets color through.
:::

---

### Switch 9 — Video Mod

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Video Mod** enables or disables per-frame animation of colony growth. When set to **Off**, the colony radii freeze at their current values: whatever territory the colonies have claimed remains static. When set to **On**, the radii advance by the Growth Sp amount on each vertical sync, and the colony boundaries evolve continuously. This toggle is the master animation switch; without it, the colonies remain fixed.

---

### Switch 10 — Reset

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Reset** clears all colony radii back to zero on a rising edge: that is, when you flip it from **Off** to **On**. All four colonies collapse to zero-radius points at their quadrant centers. If Video Mod is active, they immediately begin regrowing. This provides a clean restart for the expansion animation.

:::warning
Reset triggers on the ***transition*** from Off to On, not on the sustained On position. To reset again, flip back to Off and then to On.
:::

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, skipping all colony computation. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use Bypass for instant A/B comparison between the colony pattern and the raw input.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** controls the wet/dry balance between the colony-processed output and the original input signal. Three interpolator instances: one per YUV channel: blend the delayed input with the composite output. At the minimum position, only the dry input passes through. At the maximum position, only the colony pattern is visible. The default position is fully wet, showing the full colony effect.

---

## Background

### Voronoi Tessellation

A ***Voronoi diagram*** is a partition of a plane into regions based on proximity to a set of seed points. Each region contains all points closer to its seed than to any other. The boundaries between regions: called ***Voronoi edges***: are equidistant from exactly two seeds. Voronoi diagrams appear throughout nature: the pattern of cracks in dried mud, the cellular structure of soap bubbles, the territorial boundaries of animal populations, and the segmentation of biological tissues.

Colony implements a discrete, animated version of a Voronoi diagram. Rather than computing the exact geometric boundaries, it evaluates ***Manhattan distance*** (the sum of horizontal and vertical displacements) from each pixel to each colony center and assigns the pixel to the nearest one. Manhattan distance produces diamond-shaped territories rather than the circular regions of Euclidean distance, giving Colony its distinctive angular aesthetic.

### Colony Growth and LFSR Noise

Each colony center maintains a 16-bit ***DDS phase accumulator*** that serves as its grow radius. On every vertical sync pulse (when animation is enabled), the accumulator advances by the Growth Sp amount. In monotonic mode, this radius grows until it saturates at the maximum value. In pulse mode, the top bit of the accumulator is used as a fold point: when it overflows past the halfway mark, the effective radius decreases, creating a triangle-wave oscillation.

A 16-bit ***linear feedback shift register*** (LFSR) generates pseudo-random noise that is added to the radius during the inside/outside test. This noise is attenuated by a shift amount controlled by the Opacity knob, producing growth fronts that range from wildly irregular to nearly geometric.

### Boundary Detection

The boundary between two colonies is detected by comparing the nearest and second-nearest distances. When the difference between these two values falls below a configurable threshold (set by Ring Sp), the pixel is classified as a boundary pixel and rendered as a bright highlight. This technique identifies the equidistant zone between two colony territories (exactly the region where a Voronoi edge would lie.)


---

## Signal Flow

### Signal Flow Notes

The pipeline's most important interaction is between the colony radius growth and the per-pixel distance computation. The radii update once per frame on the vertical sync edge, but the inside/outside test runs for every pixel at the full clock rate. This means the colony boundaries are perfectly consistent within a single frame but shift smoothly between frames as the radii advance.

The LFSR noise operates on a per-pixel basis: it advances with every active video pixel: so the noise pattern at the colony edges changes continuously across the frame. Combined with the per-frame radius growth, this creates the illusion of biological irregularity: each frame's growth front has a slightly different ragged shape, as though the colony is exploring its environment.

:::note
The boundary detection uses the ***difference*** between the two nearest distances, not an absolute threshold. This means boundary width scales naturally with the geometry: boundaries at colony meeting points are always the same visual thickness regardless of how far the colonies have grown.
:::


---

## Exercises

These exercises progress from static territory maps to animated colony growth, exploring how Colony's parameters interact to produce organic, evolving patterns.
### Exercise 1: Static Voronoi Map

![Static Voronoi Map result](/img/instruments/videomancer/colony/colony_ex1_s1.png)
*Static Voronoi Map — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A frozen territorial map showing all four colonies with bright boundary lines dividing the screen into diamond-shaped regions.

#### Key Concepts

- Colony territories form a Voronoi partition based on Manhattan distance
- Boundary width controls the mutual exclusion zone appearance
- Colony count changes the complexity of the territorial map

#### Steps

1. Ensure **Video Mod** (Switch 9) is set to **Off** so colonies don't animate.
2. Set **Growth Sp** (Knob 1) to about 60% (this determines the initial radius.)
3. Flip **Video Mod** to **On** briefly, wait two seconds for colonies to expand, then flip it back to **Off** to freeze the pattern.
4. Adjust **Ring Sp** (Knob 3) to widen the bright boundary lines. Notice how they trace the equidistant zones between colony centers.
5. Turn **Colonies** (Knob 2) through its range. With two colonies, the screen divides into two halves. With three, a triangular partition appears. With all four, you get the full quadrant map.
6. Set **Opacity** (Knob 6) low to see jagged, irregular colony edges, then increase it to see clean geometric boundaries.

#### Settings

| Control | Value |
|---------|-------|
| Growth Sp | ~60% |
| Colonies | 100% |
| Ring Sp | ~40% |
| Border W | 50% |
| Color Sp | 50% |
| Opacity | ~75% |
| Pattern | Colony |
| Border | None |
| Video Mod | Off |
| Reset | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Animated Colony Growth

![Animated Colony Growth result](/img/instruments/videomancer/colony/colony_ex2_s1.png)
*Animated Colony Growth — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Watch colonies expand from zero-radius seed points, racing outward until they collide and establish permanent boundary lines.

#### Key Concepts

- DDS accumulators drive per-frame colony expansion
- Pulse mode creates breathing, rhythmic territory changes
- Reset provides a clean restart for observing the growth sequence

#### Steps

1. Flip **Reset** (Switch 10) to **On** and back to **Off** to clear all colony radii.
2. Set **Growth Sp** (Knob 1) to about 25% for slow, observable growth.
3. Flip **Video Mod** (Switch 9) to **On**. Four colonies begin expanding from their quadrant centers.
4. Watch the boundary lines form as territories meet. The bright lines appear first where neighboring colonies are closest and gradually extend outward.
5. Now flip **Pattern** (Switch 7) to **Moss**. The colonies begin pulsing: expanding and contracting in a triangle wave. Increase **Growth Sp** to see faster breathing.
6. Set **Opacity** (Knob 6) low to add ragged noise at the growth fronts. Each expansion cycle produces a different irregular edge pattern.
7. Toggle **Border** (Switch 8) to **None** to see each colony rendered in a different color as it breathes.

#### Settings

| Control | Value |
|---------|-------|
| Growth Sp | ~25% |
| Colonies | 100% |
| Ring Sp | ~30% |
| Border W | 50% |
| Color Sp | 50% |
| Opacity | ~30% |
| Pattern | Moss |
| Border | None |
| Video Mod | On |
| Reset | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Organic Boundaries and Color

![Organic Boundaries and Color result](/img/instruments/videomancer/colony/colony_ex3_s1.png)
*Organic Boundaries and Color — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A richly colored, noisy colony map overlaid on the input signal, resembling a stained microscope slide of competing bacterial cultures.

#### Key Concepts

- LFSR noise creates biologically irregular edges
- Color mode assigns distinct hues to each colony territory
- Mix blends the colony pattern with the input signal for overlay effects

#### Steps

1. Flip **Border** (Switch 8) to **None** to enable colony colors.
2. Set **Colonies** (Knob 2) to maximum for all four competing territories.
3. Set **Opacity** (Knob 6) fully counterclockwise for maximum edge noise. The colony edges become wildly irregular, resembling real biological growth fronts.
4. Enable **Video Mod** (Switch 9) and set **Growth Sp** (Knob 1) to about 40% for moderate animation speed.
5. Widen the boundary lines with **Ring Sp** (Knob 3) at about 60%. The boundaries become broad, luminous rivers flowing between colored territories.
6. Pull **Mix** (Fader 12) to about 50% to blend the colony pattern with the input video, creating a colored territorial overlay.
7. Toggle **Pattern** (Switch 7) between **Colony** and **Moss** to compare sustained expansion with rhythmic pulsing.

#### Settings

| Control | Value |
|---------|-------|
| Growth Sp | ~40% |
| Colonies | 100% |
| Ring Sp | ~60% |
| Border W | 50% |
| Color Sp | 50% |
| Opacity | 0% |
| Pattern | Colony |
| Border | None |
| Video Mod | On |
| Reset | Off |
| Bypass | Off |
| Mix | ~50% |

---
## Glossary

- **DDS Accumulator**: A Direct Digital Synthesis phase accumulator; a counter that advances by a programmable step each cycle, used here to grow colony radii smoothly over time.

- **LFSR**: Linear Feedback Shift Register; a hardware pseudo-random number generator that produces a deterministic but seemingly random sequence of bits.

- **Manhattan Distance**: The distance between two points measured along axes at right angles; the sum of absolute horizontal and vertical differences. Named after the grid layout of Manhattan streets.

- **Mutual Exclusion Zone**: The boundary region between two colony territories where neither colony dominates, detected when the nearest and second-nearest distances are close.

- **Seed Point**: The fixed center from which a colony grows outward; Colony places seeds at the centers of each screen quadrant.

- **Triangle Wave**: A periodic waveform that ramps linearly up and then linearly down, used in pulse mode to make colony radii oscillate.

- **Voronoi Diagram**: A partition of a plane into regions based on proximity to seed points, where each region contains all points closest to its associated seed.

- **Wet/Dry Mix**: A blend between the processed (wet) signal and the original (dry) input signal, controlled by the Mix fader.

---
