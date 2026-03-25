---
draft: true
sidebar_position: 170
slug: /instruments/videomancer/lichen
title: "Lichen"
image: /img/instruments/videomancer/lichen/lichen_hero.png
description: "Lichen is a synthesis program that grows circular patches from random positions on a blank canvas, frame by frame."
---

![Lichen hero image](/img/instruments/videomancer/lichen/lichen_hero_s1.png)
*Slowly expanding lichen colonies encrust the screen with tinted patches whose irregular, LFSR-broken edges creep outward frame by frame.*

---

## Overview

**Lichen** is an organic synthesis program that generates slowly spreading patches of color across the video frame. Four independent colonies start from seed points and grow outward over time, tinting everything they touch toward muted green or warm amber hues. Where colonies meet and overlap, the image darkens further, building up layers of visual depth the way real lichen thickens as it ages.

The program creates its signature crusty texture by using a ***linear feedback shift register*** (LFSR) to break up what would otherwise be smooth, diamond-shaped patch contours. The noise fragments the boundaries into irregular, organic profiles that look remarkably like the ragged margins of a real crustal colony. The result is a slowly evolving generative pattern that colonizes the screen over many seconds, eventually covering the entire image in overlapping tinted growth.

:::note
Because Lichen is a ***synthesis*** program, the generated patch pattern is overlaid onto whatever input signal is present. You can use it as a standalone color generator by feeding black, or as a tinting overlay on live video.
:::

### What's In a Name?

***Lichen*** are composite organisms formed by a symbiotic partnership between a fungus and a photosynthetic alga or cyanobacterium. They colonize exposed surfaces: rocks, bark, concrete: spreading outward as irregular, crusty patches over months and years. The program's four expanding colonies mimic this patient botanical conquest. The patches grow as ***encrusting thalli***, the flat vegetative bodies that adhere tightly to stone, and the irregular edge patterns produced by LFSR noise replicate the ragged, fractal margins of a living lichen specimen.

---

## Quick Start

1. On startup, **Lichen** seeds four patch centers across the frame. Watch as small diamond-shaped colonies begin to grow outward, tinting pixels toward soft green.
2. Turn **Grow Rat** (Knob 1) clockwise to speed up the expansion. The colonies race toward the edges of the screen.
3. Increase **Edge Irr** (Knob 3) to break up the smooth diamond contours into jagged, organic edges (this is where the lichen texture comes alive.)
4. Flip **Species** (Switch 7) from **Crust** to **Map** to double the number of active patches from two to four, filling the frame with overlapping colonies.

---

## Parameters

![Videomancer front panel with Lichen loaded](/img/instruments/videomancer/lichen/lichen_control_panel.png)
*Videomancer's front panel with Lichen active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Grow Rat

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Grow Rat** controls how many pixels each colony's radius increases per video frame. At low values the patches expand slowly, giving you time to watch individual boundary details form. At high values the colonies race outward, covering the screen in seconds.

:::tip
If you want to observe the edge texture in detail, keep Grow Rat low and watch the boundary evolve frame by frame. Speed it up once you've dialed in the noise and color settings you want.
:::

---

### Knob 2 — Patches

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Patches** sets the maximum radius each colony can reach before it stops growing. Small values produce compact islands of lichen that never quite cover the frame. Large values allow colonies to expand until they overlap heavily, eventually tinting every pixel on screen. Think of this as the "real estate" available to each colony: it does not change the number of patches, only how far each one can spread.

---

### Knob 3 — Edge Irr

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Edge Irr** (Edge Irregularity) adjusts how much the LFSR noise breaks up the patch boundaries. At minimum, edges are smooth geometric diamonds defined by the ***Manhattan distance*** metric. As you increase this control, more LFSR bits pass through the noise mask, creating increasingly ragged, crusty contours. At maximum, the boundaries become deeply irregular, with tendrils and inlets that look convincingly organic.

:::note
The irregularity is applied every clock cycle, so the edge texture varies spatially across the frame. Two adjacent boundary pixels may be classified differently, producing the fine-grained crustiness that defines the lichen aesthetic.
:::

---

### Knob 4 — Bnd Width

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Bnd Width** governs the color tinting intensity applied to pixels inside a colony. At low values the tint is subtle: a gentle wash of green or amber barely visible over the source image. As you increase this control, the chroma shift becomes more saturated and the luma darkening more pronounced. Where multiple colonies overlap, the darkening compounds: a pixel inside two overlapping patches is noticeably darker than one inside a single patch, and four-way intersections are darkest of all.

---

### Knob 5 — Color Var

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Color Var** sets the width of the transition zone at each colony's edge. A narrow zone creates sharp, well-defined borders between colonized and uncolonized areas. A wider zone creates a graduated fringe where LFSR noise has more room to sculpt irregular edges, and boundary pixels receive a subtle luma highlight that emphasizes the colony margins.

:::tip
**Color Var** and **Edge Irr** work together. Edge Irr determines ***how rough*** the boundary is, while Color Var determines ***how wide*** the boundary region is. Try a narrow Color Var with high Edge Irr for tight, jagged edges, or a wide Color Var with moderate Edge Irr for soft, fuzzy fringes.
:::

---

### Knob 6 — Texture

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Texture** is reserved for future expansion and has no visible effect in the current version. Adjusting this control does not alter the output.

---

### Switch 7 — Species

| Property | Value |
|----------|-------|
| Off | Crust |
| On | Map |
| Default | Crust |

**Species** selects the number of active colonies. In the **Crust** position, two patches grow outward from seed points on the left and right sides of the frame. In the **Map** position, all four patches are active, filling the screen with more overlapping colonies and richer layered darkening.

:::tip
Start with **Crust** (two patches) to study individual colony behavior, then switch to **Map** (four patches) for denser compositions.
:::

---

### Switch 8 — Surface

| Property | Value |
|----------|-------|
| Off | Rock |
| On | Glass |
| Default | Rock |

**Surface** selects the lichen color family. In the **Rock** position, colonies tint toward a cool green: the hue of crustose lichen on granite. In the **Glass** position, colonies shift to a warm amber, evoking the golden-orange tones of foliose lichen on sun-exposed surfaces.

---

### Switch 9 — Merge

| Property | Value |
|----------|-------|
| Off | Border |
| On | Blend |
| Default | Border |

**Merge** triggers a colony reset. Flipping this switch from **Border** to **Blend** immediately re-seeds all four colony positions using LFSR-derived coordinates. Radii reset to one pixel and the expansion begins again from new locations. Flip it back and then forward again to scatter the colonies once more.

:::warning
Resetting colonies is a one-shot event triggered by the toggle transition. Once the colonies begin growing from their new positions, the switch must be returned to **Border** and then flipped back to **Blend** to trigger another reset.
:::

---

### Switch 10 — Animate

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Animate** is reserved for future expansion and has no visible effect in the current version.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Lichen processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the original input and the lichen-tinted composite. At minimum, the output is the unmodified input: no lichen tinting is visible. At maximum, the output is the fully processed colony overlay. Intermediate positions blend the two, allowing you to dial in the exact overlay intensity independently of the **Bnd Width** tinting control.

---

## Background

### Lichen biology and visual analogy

Real-world ***lichen*** are among the slowest-spreading visible organisms on Earth. A crustal colony might grow only a few millimeters per year, yet over decades it paints boulders and tombstones with vivid patches of chartreuse, rust, and silver. The program borrows three properties from actual lichen growth: expansion from point sources, irregular boundary morphology, and color tinting that intensifies in older, thicker regions (modeled here by overlap darkening).

### Manhattan distance

The program uses ***Manhattan distance*** (also called ***taxicab distance*** or ***L1 norm***) to determine whether a pixel falls inside a patch. Instead of the familiar circular Euclidean distance $\sqrt{dx^2 + dy^2}$, Manhattan distance is simply $|dx| + |dy|$. The resulting contours are diamond-shaped rather than circular, which is computationally inexpensive on an FPGA: it requires only addition and absolute difference, with no multipliers or square roots. The LFSR noise then roughens these diamonds into organic shapes.

### LFSR edge noise

A 16-bit ***linear feedback shift register*** (LFSR) produces a continuous stream of pseudo-random bits synchronized to the pixel clock. Near each colony boundary, these noise bits are AND-masked with the **Edge Irr** parameter and compared against the boundary width to decide whether a given pixel flips from inside to outside (or vice versa). The effect is that some boundary pixels are randomly reclassified, creating the signature crusty, ragged edges. Just outside the radius, a secondary fringe check can pull stray pixels inward, producing irregular tendrils and peninsulas.

### Overlap and tinting

When a pixel sits inside one or more colonies, the program applies two modifications. First, ***chroma tinting*** shifts the U and V channels partway toward a target color: cool green (U ≈ 420, V ≈ 480) or warm amber (U ≈ 440, V ≈ 580): with the shift magnitude controlled by **Bnd Width**. Second, ***luma darkening*** reduces brightness in proportion to the overlap count: one colony produces a subtle dim, two a moderate dim, three a heavier dim, and four the strongest darkening. Boundary pixels receive a small luma boost (+32) that acts as a rim highlight, keeping colony edges visible even under heavy tinting.


---

## Signal Flow

### Signal Flow Notes

The pipeline divides into two time scales. At the ***frame level***, colony positions are seeded once on the first frame after power-up (or after a **Merge** reset), and radii grow by a fixed increment each vsync. At the ***pixel level***, each clock cycle independently classifies the current pixel against all four patches, computes overlap depth, and applies tinting.

Two interactions are worth noting. First, because the LFSR runs continuously at the pixel clock, its noise pattern is ***spatially varying***: every pixel gets a different noise sample, creating fine-grained edge texture rather than uniform randomness. Second, the overlap count drives a stepped darkening schedule that produces subtle relief shading: the flat interior of a single colony is lighter than the intersection of two colonies, which in turn is lighter than a three-way or four-way overlap. The thin rim highlight at each boundary reinforces this stratified appearance, much like the pale margin visible at the edge of a crustose lichen in nature.


---

## Exercises

These exercises explore colony growth, edge shaping, and color layering. Each builds on the previous, introducing more controls and more complex patch interactions.
### Exercise 1: Colony Expansion

![Colony Expansion result](/img/instruments/videomancer/lichen/lichen_ex1_s1.png)
*Colony Expansion — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Watch two colonies grow from seed points and observe how growth rate and maximum size interact to set the pace and extent of colonization.

#### Key Concepts

- Patches grow outward from seed points each frame
- Manhattan distance creates diamond-shaped contours
- Growth rate and maximum radius are independent controls

#### Steps

1. Start with default settings. Two small diamond-shaped colonies appear near the center-left and center-right of the frame.
2. Slowly increase **Grow Rat** (Knob 1) and watch the colonies expand outward. Note the diamond shape of the contours (this is the Manhattan distance at work.)
3. Set **Patches** (Knob 2) to a low value. The colonies stop growing once they reach a small maximum radius. The frame remains mostly uncovered.
4. Increase **Patches** toward maximum. The radius ceiling lifts and the colonies expand until they overlap at the center of the frame.
5. Toggle **Bypass** (Switch 11) to compare the lichen overlay with the clean input signal.

#### Settings

| Control | Value |
|---------|-------|
| Grow Rat | ~50% |
| Patches | ~80% |
| Edge Irr | 0% |
| Bnd Width | ~50% |
| Color Var | ~50% |
| Texture | 50% |
| Species | Crust |
| Surface | Rock |
| Merge | Border |
| Animate | On |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Crusty Edges

![Crusty Edges result](/img/instruments/videomancer/lichen/lichen_ex2_s1.png)
*Crusty Edges — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Transform smooth diamond patches into irregular, crusty lichen colonies with visible edge detail and layered overlap darkening.

#### Key Concepts

- LFSR noise breaks diamond contours into organic edges
- Boundary width controls the transition zone thickness
- Boundary pixels receive a luma highlight as a rim accent

#### Steps

1. Set **Edge Irr** (Knob 3) to maximum. The diamond edges shatter into jagged, organic contours.
2. Reduce **Edge Irr** to about 30% for a more subtle effect. Notice how different noise mask values produce different spatial frequencies of edge detail.
3. Increase **Color Var** (Knob 5) to widen the boundary transition zone. The crusty fringe region becomes broader, with more pixels participating in the irregular edge.
4. Lower **Color Var** to minimum. The boundary tightens to a razor-thin ring of irregularity.
5. Bring **Bnd Width** (Knob 4) to maximum. The tinting inside each colony deepens (overlapping areas become noticeably darker.)
6. Flip **Species** (Switch 7) to **Map** to add two more colonies. The additional overlaps create a richer layered pattern with deeper darkening at intersections.

#### Settings

| Control | Value |
|---------|-------|
| Grow Rat | ~30% |
| Patches | ~70% |
| Edge Irr | ~60% |
| Bnd Width | ~80% |
| Color Var | ~60% |
| Texture | 50% |
| Species | Map |
| Surface | Rock |
| Merge | Border |
| Animate | On |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Amber Territories

![Amber Territories result](/img/instruments/videomancer/lichen/lichen_ex3_s1.png)
*Amber Territories — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A slowly emerging landscape of warm amber territories with irregular borders, using Merge resets to compose the most pleasing colony arrangement.

#### Key Concepts

- Merge reset scatters colonies to new LFSR-derived positions
- Color mode shifts the entire palette from green to amber
- Mix crossfade controls overall overlay intensity

#### Steps

1. Flip **Surface** (Switch 8) to **Glass**. The colony color shifts from cool green to warm amber.
2. Set **Bnd Width** (Knob 4) to about 70%. The amber tint is visible but not overwhelming.
3. Flip **Merge** (Switch 9) from **Border** to **Blend**. All colonies reset to new LFSR-derived positions and start growing again from radius one.
4. If you don't like the layout, flip **Merge** back to **Border** and then to **Blend** again. Each reset produces a different colony arrangement.
5. Once the colonies have grown, pull **Mix** (Fader 12) to about 60%. The amber overlay becomes translucent, letting the input signal show through underneath.
6. Experiment with **Grow Rat** and **Patches** to control how quickly the territories fill in and how large they ultimately get.

#### Settings

| Control | Value |
|---------|-------|
| Grow Rat | ~40% |
| Patches | ~60% |
| Edge Irr | ~50% |
| Bnd Width | ~70% |
| Color Var | ~50% |
| Texture | 50% |
| Species | Map |
| Surface | Glass |
| Merge | Blend |
| Animate | On |
| Bypass | Off |
| Mix | ~60% |

---
## Glossary

- **Encrusting**: A growth form that adheres tightly to a surface, spreading outward as a flat, irregular patch.

- **LFSR (Linear Feedback Shift Register)**: A shift register whose input bit is a function of its previous state, producing a repeating sequence of pseudo-random values.

- **Manhattan Distance**: The distance between two points measured by summing their absolute coordinate differences: |dx| + |dy|. Produces diamond-shaped contours.

- **Overlap Count**: The number of colony patches that simultaneously cover a given pixel, used to determine the depth of luma darkening.

- **Patch**: A region of the frame associated with one lichen colony, defined by a center point and a growing radius.

- **Seed Point**: The initial center coordinates from which a lichen colony begins expanding.

- **Synthesis Program**: A Videomancer program that generates visual patterns algorithmically rather than transforming an input signal.

- **Thallus**: The vegetative body of a lichen organism, used here as a metaphor for an individual growing patch colony.

- **Tinting**: Shifting pixel color values toward a target hue and reducing luminance, simulating the appearance of a colored overlay.

---
