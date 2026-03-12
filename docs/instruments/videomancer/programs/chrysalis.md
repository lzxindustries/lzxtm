---
draft: true
sidebar_position: 52
slug: /instruments/videomancer/chrysalis
title: "Chrysalis"
image: /img/instruments/videomancer/chrysalis/chrysalis_hero_s1.png
description: "A chrysalis is the transitional shell between caterpillar and butterfly — ordinary tissue reorganised into something with entirely new symmetry."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import chrysalis_control_panel from '/img/instruments/videomancer/chrysalis/chrysalis_control_panel.png';
import chrysalis_source1_ballerina from '/img/instruments/videomancer/chrysalis/chrysalis_source1_ballerina.png';
import chrysalis_source2_castle from '/img/instruments/videomancer/chrysalis/chrysalis_source2_castle.png';
import chrysalis_source3_collage from '/img/instruments/videomancer/chrysalis/chrysalis_source3_collage.png';
import chrysalis_source4_pattern from '/img/instruments/videomancer/chrysalis/chrysalis_source4_pattern.png';
import chrysalis_source5_boy from '/img/instruments/videomancer/chrysalis/chrysalis_source5_boy.png';
import chrysalis_source6_berries from '/img/instruments/videomancer/chrysalis/chrysalis_source6_berries.png';
import chrysalis_hero_s1 from '/img/instruments/videomancer/chrysalis/chrysalis_hero_s1.png';
import chrysalis_hero_s2 from '/img/instruments/videomancer/chrysalis/chrysalis_hero_s2.png';
import chrysalis_hero_s3 from '/img/instruments/videomancer/chrysalis/chrysalis_hero_s3.png';
import chrysalis_hero_s4 from '/img/instruments/videomancer/chrysalis/chrysalis_hero_s4.png';
import chrysalis_hero_s5 from '/img/instruments/videomancer/chrysalis/chrysalis_hero_s5.png';
import chrysalis_hero_s6 from '/img/instruments/videomancer/chrysalis/chrysalis_hero_s6.png';
import chrysalis_ex1_s1 from '/img/instruments/videomancer/chrysalis/chrysalis_ex1_s1.png';
import chrysalis_ex1_s2 from '/img/instruments/videomancer/chrysalis/chrysalis_ex1_s2.png';
import chrysalis_ex1_s3 from '/img/instruments/videomancer/chrysalis/chrysalis_ex1_s3.png';
import chrysalis_ex1_s4 from '/img/instruments/videomancer/chrysalis/chrysalis_ex1_s4.png';
import chrysalis_ex1_s5 from '/img/instruments/videomancer/chrysalis/chrysalis_ex1_s5.png';
import chrysalis_ex1_s6 from '/img/instruments/videomancer/chrysalis/chrysalis_ex1_s6.png';
import chrysalis_ex2_s1 from '/img/instruments/videomancer/chrysalis/chrysalis_ex2_s1.png';
import chrysalis_ex2_s2 from '/img/instruments/videomancer/chrysalis/chrysalis_ex2_s2.png';
import chrysalis_ex2_s3 from '/img/instruments/videomancer/chrysalis/chrysalis_ex2_s3.png';
import chrysalis_ex2_s4 from '/img/instruments/videomancer/chrysalis/chrysalis_ex2_s4.png';
import chrysalis_ex2_s5 from '/img/instruments/videomancer/chrysalis/chrysalis_ex2_s5.png';
import chrysalis_ex2_s6 from '/img/instruments/videomancer/chrysalis/chrysalis_ex2_s6.png';
import chrysalis_ex3_s1 from '/img/instruments/videomancer/chrysalis/chrysalis_ex3_s1.png';
import chrysalis_ex3_s2 from '/img/instruments/videomancer/chrysalis/chrysalis_ex3_s2.png';
import chrysalis_ex3_s3 from '/img/instruments/videomancer/chrysalis/chrysalis_ex3_s3.png';
import chrysalis_ex3_s4 from '/img/instruments/videomancer/chrysalis/chrysalis_ex3_s4.png';
import chrysalis_ex3_s5 from '/img/instruments/videomancer/chrysalis/chrysalis_ex3_s5.png';
import chrysalis_ex3_s6 from '/img/instruments/videomancer/chrysalis/chrysalis_ex3_s6.png';

# Chrysalis

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Ballerina", before: chrysalis_source1_ballerina, after: chrysalis_hero_s1 },
    { label: "Castle", before: chrysalis_source2_castle, after: chrysalis_hero_s2 },
    { label: "Collage", before: chrysalis_source3_collage, after: chrysalis_hero_s3 },
    { label: "Pattern", before: chrysalis_source4_pattern, after: chrysalis_hero_s4 },
    { label: "Boy", before: chrysalis_source5_boy, after: chrysalis_hero_s5 },
    { label: "Berries", before: chrysalis_source6_berries, after: chrysalis_hero_s6 },
  ]}
/>
*Chrysalis splitting a portrait into radial kaleidoscope segments, each mirrored fold reflecting the source into symmetrical geometry that spirals diagonally across the frame.*

---

## Overview

A chrysalis is the transitional shell between caterpillar and butterfly — ordinary tissue reorganised into something with entirely new symmetry. This program performs an analogous transformation on video. It takes a conventional left-to-right scanline and remaps its pixel addresses through a DDS (direct digital synthesis) accumulator, folding the horizontal axis into repeating, mirrored segments that turn mundane source material into radial kaleidoscope patterns.

The core technique is address-domain transformation: rather than altering pixel values (brightness, colour, contrast), Chrysalis alters *where* each pixel is read from within the scanline buffer. A DDS frequency accumulator divides the horizontal span into a configurable number of segments. Within each segment, a triangle-wave fold causes the read address to sweep forward and then reverse, producing a mirror-image repeat. A per-line phase slant offsets the pattern progressively down the frame, tilting the symmetry axis from vertical toward diagonal or spiral. The result is a real-time kaleidoscope processor — every frame of incoming video is refracted through a crystalline symmetry structure.

At conservative settings — two or four segments with gentle slant — Chrysalis produces clean bilateral or quadrilateral symmetry that enhances the compositional balance of ordinary footage. At extreme settings — sixteen segments with high slant and animation enabled — the image shatters into a rotating mandala of mirrored shards, each one a tiny window into the source material, spinning continuously as the DDS phase accumulator advances frame by frame.

---

## Quick Start

1. **Start with 2 segments**: The bilateral mirror at 2 segments is the most legible starting point. Once you understand the fold, increase the segment count gradually.
2. **Fold at 50% for clean symmetry**: Off-centre fold values produce asymmetric reflections that can be interesting, but 50% gives the cleanest kaleidoscope geometry.
3. **Slant creates diagonals**: Even a small amount of slant (10–20%) adds dramatic diagonal structure. Use it to break the rigidity of purely vertical segment boundaries.

---

## Background

### Kaleidoscopes and Optical Symmetry

Sir David Brewster patented the kaleidoscope in 1817 after studying the behaviour of light between inclined mirrors. Two mirrors set at an angle of 360°/N produce N-fold rotational symmetry from whatever objects lie between them. The apparatus is simple — two strips of mirror, a tube, and loose beads — but the mathematics of reflection guarantees that every random arrangement of fragments becomes a perfectly symmetric pattern. Chrysalis implements this principle electronically: the DDS segment count is the digital equivalent of Brewster's mirror angle, and the fold operation within each segment is the equivalent of reflection at the mirror boundary.

### Direct Digital Synthesis for Address Generation

Direct digital synthesis is a technique borrowed from RF engineering, where a phase accumulator increments by a tunable frequency word on every clock cycle. The accumulator's MSBs form a sawtooth wave whose frequency is precisely controlled by the increment. In Chrysalis, the DDS accumulator runs at the pixel clock rate (74.25 MHz for HD), and the frequency word is derived from the Segments and Zoom controls. Instead of generating a sine wave for an RF carrier, the accumulator's output becomes a *read address* — the position in the scanline buffer from which the current output pixel is fetched. This repurposing of DDS from the frequency domain to the spatial domain is the program's central insight.

### Fold and Mirror Operations

A raw DDS accumulator produces a sawtooth — addresses that ramp up and then wrap abruptly. The fold operation converts this sawtooth into a triangle wave: addresses ramp up to the segment midpoint, then ramp back down. The effect is that each segment of the output contains a forward-then-reversed copy of a portion of the scanline, producing mirror symmetry at every segment boundary. The Mirror toggle controls whether alternating segments are reversed relative to their neighbours. With Mirror on, adjacent segments are reflections of each other (true kaleidoscope behaviour). With Mirror off, every segment is an identical forward copy — repetition without reflection.

### Per-Line Slant and Spiral Symmetry

In a physical kaleidoscope, the mirrors run parallel to the viewing axis — the symmetry is the same on every horizontal cross-section. Chrysalis breaks this constraint with the Slant control, which adds a per-line phase offset to the DDS accumulator. Each successive scanline starts its address sweep at a slightly different phase, causing the segment boundaries to shift progressively down the frame. At low slant values, the segments tilt gently, producing diagonal symmetry axes. At high slant values, the offset accumulates enough over the full frame height to shift by one or more full segment widths, creating spiral or helical symmetry patterns that have no analogue in physical mirror optics.

### Real-Time Address Remapping on FPGA

The entire address transformation — DDS accumulation, segment division, triangle fold, slant offset — must complete within a single pixel clock period (≈13.5 ns at 74.25 MHz). The iCE40 FPGA implements this as a pipeline of registered arithmetic stages: multiply, shift, fold, and address clamp/wrap execute in sequence across approximately 8–10 clock cycles. A small BRAM-backed shift register stores the input scanline so that the transformed address can look up any pixel within the current line. The result is zero-latency address remapping — every output pixel is computed in real time from the live input, with no frame buffer and minimal BRAM usage.


---

## Signal Flow

Input Register → Pixel Counter → DDS Phase Accumulator → ... → Scanline Lookup → Interpolator Mix

```
Input Video (YUV 4:4:4)
│
├─ 1. Input Register + Scanline Buffer     (BRAM shift register captures current line)
│
├─ 2. Pixel Counter (X position)            (horizontal position, 0 to active width)
│
├─ 3. DDS Phase Accumulator                 (X × frequency_word + slant_offset + global_offset)
│      ├─ frequency_word ← Segments × Zoom
│      ├─ slant_offset ← Y_line × Slant
│      ├─ global_offset ← Offset + (Animate ? frame_counter × Speed : 0)
│      └─ Invert toggle reverses accumulator direction
│
├─ 4. Segment Extraction                    (divide phase into segment index + position within segment)
│
├─ 5. Fold / Mirror                         (triangle-wave fold within segment)
│      ├─ Mirror on → alternating segments reversed (true kaleidoscope)
│      └─ Mirror off → all segments identical (tiled repetition)
│
├─ 6. Address Transform                     (fold output → scanline buffer read address)
│      ├─ Wrap on → modular wrap at boundaries
│      └─ Wrap off → clamp to edge pixel
│
├─ 7. Scanline Lookup                       (read Y/U/V from BRAM at transformed address)
│
├─ 8. Interpolator Mix (×3 channels)        (4 clocks — dry/wet crossfade)
│      └─ t = Mix: 0 = dry (original), 1023 = wet (kaleidoscope)
│
├─ Sync/Data Delay Pipeline                 (shift register for sync alignment)
│
└─ Output Mux
    ├─ Bypass off → mixed Y/U/V + aligned sync
    └─ Bypass on  → delayed input Y/U/V + aligned sync
```

The DDS accumulator at stage 3 is the heart of the algorithm. Its frequency word determines how quickly the phase advances per pixel — higher frequency means more segments (smaller angular slices) packed into one scanline. The fold at stage 5 converts each segment's linear ramp into a back-and-forth sweep, which is what creates the mirror-image effect. Without the fold, the output would be simple tiled repetition; with it, adjacent segments are reflections of each other, producing the characteristic kaleidoscope symmetry.

The Slant offset is computed once per line (Y × slant coefficient) and added to the accumulator's initial phase for that line. This means the entire segment structure shifts laterally as you move down the frame. The visual effect is that the vertical symmetry axes become diagonal lines — or, at high slant values, spirals that wrap around multiple segment widths. Combined with animation (frame counter × Speed), the diagonal pattern scrolls continuously, creating a rotating mandala effect.

---

## Parameter Reference

<img src={chrysalis_control_panel} alt="Videomancer front panel with Chrysalis loaded"/>
*Videomancer's front panel with Chrysalis active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Fold Point
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Sets the number of kaleidoscope segments — the angular divisions of the transformed image. The stepped control snaps to values between 2 and 16 in 8 discrete steps: at the lowest setting, the scanline is divided into two mirrored halves (bilateral symmetry); at the highest, sixteen narrow segments tile across the frame (fine crystalline facets). This control directly sets the DDS frequency word's coarse component — doubling the segment count doubles the spatial frequency of the address sweep, halving the width of each segment. Fewer segments produce bold, recognisable reflections of the source; more segments produce intricate, gem-like patterns where the source becomes almost abstract.

---

#### Knob 2 — Segments
| Property | Value |
|----------|-------|
| Range | 0 – 7 |
| Default | 0 |

Controls the fold point — the position within each segment where the address sweep reverses direction. At 50% (centre), the fold is symmetric: the forward and reverse halves of each segment are equal in width, producing perfect bilateral symmetry. Moving the fold point off-centre makes one half wider than the other, so each segment contains an asymmetric reflection — a longer ramp up and a shorter ramp back, or vice versa. At the extremes (0% or 100%), the fold collapses entirely and the segment becomes a one-directional ramp with no mirror, effectively converting the kaleidoscope into a simple tiled repeat.

---

#### Knob 3 — H Offset
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Adds a per-line phase offset that tilts the symmetry axis away from vertical. At 0% (fully counter-clockwise), the slant is zero — all scanlines share the same phase, and segment boundaries run perfectly vertical. At 50% (centre), a moderate offset accumulates line by line, producing diagonal segment boundaries. At 100%, the slant is maximum — segment boundaries may wrap around one or more full periods across the frame height, creating spiral or helical symmetry. Slant transforms the output from a static mirror pattern into a dynamic, directional structure that suggests rotation even in still frames.

---

#### Knob 4 — Luma Mod
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Scales the DDS frequency, acting as a spatial zoom control. At 50% (centre), the frequency word matches the Segments control — the configured number of segments fits exactly within the active picture width. Turning below centre reduces the frequency (zoom in): segments become wider, fewer fit on screen, and individual reflections are larger and more recognisable. Turning above centre increases the frequency (zoom out): segments become narrower, more repetitions pack into the frame, and the pattern becomes finer and more abstract. Zoom interacts multiplicatively with Segments — 4 segments at 2× zoom looks identical to 8 segments at 1× zoom.

---

#### Knob 5 — Zoom
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Shifts the entire kaleidoscope pattern horizontally by adding a global phase offset to the DDS accumulator. At 0% (fully counter-clockwise), no offset is applied — the pattern is anchored to the left edge of the frame. Increasing the offset slides the entire symmetry structure to the right, revealing different portions of the source scanline through each segment window. This is a static offset; for continuous scrolling, use the Animate toggle with the Speed control. Offset is useful for framing a specific part of the source at the centre of a symmetric segment.

---

#### Knob 6 — Slant
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the rate of animation when the Animate toggle is engaged. The Speed value sets the per-frame increment of a free-running phase counter that is added to the DDS accumulator's global offset. At 0%, animation is frozen even with Animate on. At low values, the kaleidoscope pattern drifts slowly across the source — a meditative, glacial rotation. At high values, the pattern scrolls rapidly, producing a spinning mandala effect. The animation is purely in the address domain — no pixel values change, only the mapping from output position to source position advances each frame.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — H Mirror** | Off | On |
| **8 — Alt Lines** | Off | On |
| **9 — Boundary** | Tile | Mirror |
| **10 — Invert** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control independent binary features whose combinations produce distinct visual behaviours. Mirror (7) determines whether adjacent segments are reflections or identical copies — the difference between a kaleidoscope and a tiled wallpaper. Animate (8) engages the free-running phase counter for continuous motion; without it, Speed has no effect. Wrap (9) controls boundary behaviour: wrapping creates seamless tiling at address edges, while clamping smears the edge pixel. Invert (10) reverses the entire address sweep direction, flipping the pattern left-to-right. Bypass (11) overrides all processing. Mirror + Animate + Wrap together produce a fluid, seamlessly scrolling kaleidoscope. Mirror off + Animate + Invert creates a reversed scrolling tile. All toggles can be combined freely; Bypass always takes priority.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfades between the dry input signal and the kaleidoscope-processed signal. At 0% (fader down), the output is pure dry — the original, unmodified video. At 100% (fader up), the output is pure wet — the full kaleidoscope transformation. Intermediate positions blend the two, creating a ghostly overlay where the original image shows through the symmetric pattern. This is useful for performance — you can bring the kaleidoscope effect in and out smoothly, or hold it at a partial blend where the source remains recognisable inside the symmetry structure.


#### Switch 11 — Bypass
| Property | Value |
|----------|-------|
| Off | Processing active |
| On | Bypass engaged |

Routes the unprocessed input signal directly to the output, bypassing all Chrysalis processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.---
## Guided Exercises

These exercises progress from simple bilateral symmetry through animated mandalas to full spiral kaleidoscope structures. Each introduces new controls while building on the spatial intuition developed in earlier steps.

### Exercise 1: Bilateral Mirror

<BeforeAfterSlider
  sources={[
    { label: "Ballerina", before: chrysalis_source1_ballerina, after: chrysalis_ex1_s1 },
    { label: "Castle", before: chrysalis_source2_castle, after: chrysalis_ex1_s2 },
    { label: "Collage", before: chrysalis_source3_collage, after: chrysalis_ex1_s3 },
    { label: "Pattern", before: chrysalis_source4_pattern, after: chrysalis_ex1_s4 },
    { label: "Boy", before: chrysalis_source5_boy, after: chrysalis_ex1_s5 },
    { label: "Berries", before: chrysalis_source6_berries, after: chrysalis_ex1_s6 },
  ]}
/>
*Bilateral Mirror — simulated result across source images.*
**Source**: A portrait or face — the bilateral symmetry of human features makes the mirror effect immediately legible.

**What You'll Create**: Understand how segment count and the fold/mirror controls create basic kaleidoscope symmetry.

1. **Two-segment mirror**: Set Segments to the lowest step (2 segments). Enable Mirror (Toggle 7). Set Mix fader to 100%. The image splits into two mirrored halves — a Rorschach-like bilateral symmetry.
2. **Adjust fold point**: Sweep the Fold knob from 0% to 100%. Watch how the mirror axis shifts within each segment — at 50%, perfect symmetry; off-centre, one half dominates.
3. **Increase segments**: Step Segments up to 4, then 8. The image refracts into progressively more facets, each one a mirrored slice of the source.
4. **Zoom in**: Turn Zoom below centre to enlarge the segments. Each facet now shows a larger portion of the source, making individual reflections more recognisable.
5. **Offset framing**: Adjust Offset to slide the pattern until an interesting feature (an eye, a colour boundary) sits at the centre of a fold axis.

**Key concepts**: Segment count sets the angular divisions, fold point controls the symmetry balance within each segment, mirror enables reflection vs tiled repetition, zoom scales segment width, offset frames the source

---

### Exercise 2: Diagonal Slant and Spiral

<BeforeAfterSlider
  sources={[
    { label: "Ballerina", before: chrysalis_source1_ballerina, after: chrysalis_ex2_s1 },
    { label: "Castle", before: chrysalis_source2_castle, after: chrysalis_ex2_s2 },
    { label: "Collage", before: chrysalis_source3_collage, after: chrysalis_ex2_s3 },
    { label: "Pattern", before: chrysalis_source4_pattern, after: chrysalis_ex2_s4 },
    { label: "Boy", before: chrysalis_source5_boy, after: chrysalis_ex2_s5 },
    { label: "Berries", before: chrysalis_source6_berries, after: chrysalis_ex2_s6 },
  ]}
/>
*Diagonal Slant and Spiral — simulated result across source images.*
**Source**: Footage with strong horizontal or vertical lines — architecture, fences, window blinds.

**What You'll Create**: Explore how the per-line slant control tilts the symmetry axis and creates spiral patterns.

1. **Prepare**: Set 8 segments, Mirror on, Mix 100%, Fold 50%, Zoom 50%.
2. **Introduce slant**: Slowly increase Slant from 0%. Watch the vertical segment boundaries tilt diagonally. Horizontal lines in the source begin to curve.
3. **Moderate slant**: At ~40%, the segment boundaries form clear diagonal lines across the frame. The kaleidoscope pattern now has a rotational quality.
4. **High slant**: Push Slant toward 80–100%. The boundaries wrap around, creating spiral or helical patterns — the symmetry axis corkscrews down the frame.
5. **Zoom interaction**: Reduce Zoom to enlarge the spiral structure. Increase Zoom to tighten it into fine helical threads.
6. **Wrap vs clamp**: Toggle Wrap (Toggle 9). With Wrap on, the spiral tiles seamlessly. With Wrap off, clamped edges create bands of solid colour at the spiral boundaries.

**Key concepts**: Slant adds per-line phase offset tilting the symmetry axis, high slant creates spiral/helical patterns, slant and zoom interact to control spiral pitch, wrap ensures seamless tiling at boundaries

---

### Exercise 3: Animated Mandala

<BeforeAfterSlider
  sources={[
    { label: "Ballerina", before: chrysalis_source1_ballerina, after: chrysalis_ex3_s1 },
    { label: "Castle", before: chrysalis_source2_castle, after: chrysalis_ex3_s2 },
    { label: "Collage", before: chrysalis_source3_collage, after: chrysalis_ex3_s3 },
    { label: "Pattern", before: chrysalis_source4_pattern, after: chrysalis_ex3_s4 },
    { label: "Boy", before: chrysalis_source5_boy, after: chrysalis_ex3_s5 },
    { label: "Berries", before: chrysalis_source6_berries, after: chrysalis_ex3_s6 },
  ]}
/>
*Animated Mandala — simulated result across source images.*
**Source**: Colourful, textured footage — nature scenes, fabrics, or abstract video feedback.

**What You'll Create**: Combine animation, slant, and high segment counts to create a continuously rotating mandala.

1. **High segments**: Set Segments to 12 or 16. Mirror on. Mix 100%.
2. **Moderate slant**: Set Slant ~40% to establish diagonal symmetry.
3. **Enable animation**: Turn on Animate (Toggle 8).
4. **Set speed**: Increase Speed from 0% to ~30%. The kaleidoscope pattern begins scrolling through the source, creating the illusion of rotation.
5. **Fine-tune speed**: Adjust Speed for a meditative, slow rotation. Very low values (~5–10%) produce a glacial drift; higher values (~60%+) spin rapidly.
6. **Add zoom variation**: Sweep Zoom while animation runs. Zooming in creates large, slow-moving reflections; zooming out tightens the pattern into a dense, fast-spinning rosette.
7. **Invert direction**: Toggle Invert (Toggle 10) to reverse the scroll direction — the mandala now rotates the opposite way.
8. **Partial mix**: Pull the Mix fader to ~60%. The original source ghosts through the kaleidoscope, grounding the abstract pattern in recognisable imagery.

**Key concepts**: Animation adds per-frame phase offset for continuous scrolling, speed controls the rotation rate, high segment counts create dense mandala geometry, invert reverses rotation direction, partial mix reveals the source inside the pattern

---


## Tips

- **Zoom and Segments interact**: Doubling segments at fixed zoom is equivalent to halving zoom at fixed segments. Use Segments for coarse control and Zoom for fine adjustment.
- **Wrap for seamless patterns**: Always enable Wrap unless you specifically want the clamped-edge glitch effect. Wrap ensures clean tiling at all segment boundaries.
- **Animate for performance**: The Animate + Speed combination turns Chrysalis into a self-running visual instrument. Set a speed and let the mandala evolve — no hands required.
- **Partial mix grounds the image**: At 50–70% mix, the source remains visible inside the kaleidoscope pattern. This creates a layered effect where symmetrical geometry overlays recognisable imagery.
- **Invert for instant variety**: Toggling Invert flips the entire pattern horizontally. In animation mode, this reverses the rotation direction for an immediate visual change.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bilateral symmetry** | Symmetry across a single axis, producing two mirror-image halves; the simplest kaleidoscope mode with two segments. |
| **Crossfade** | A gradual blend between two signals (dry and wet) controlled by the Mix fader, allowing partial transparency between the original and processed images. |
| **DDS (Direct Digital Synthesis)** | A technique using a phase accumulator with a tunable frequency word to generate precise waveforms; repurposed here to produce scanline read addresses instead of RF carriers. |
| **Dry/wet** | Signal routing terminology where "dry" is the unprocessed original and "wet" is the effect-processed output. |
| **Frequency word** | The fixed increment added to a DDS phase accumulator on each clock cycle, determining the output waveform's spatial frequency and thus the number of segments. |
| **iCE40** | The Lattice Semiconductor FPGA family used in Videomancer; provides the logic fabric, BRAM, and DSP resources for real-time video processing. |
| **N-fold symmetry** | Rotational symmetry of order N, where a pattern repeats N times around a central point; set by the Segments control. |
| **Phase accumulator** | A register that increments by the frequency word each clock cycle, producing a sawtooth ramp whose MSBs encode the current segment position. |
| **Pixel clock** | The clock signal that drives one pixel per cycle; 74.25 MHz for HD video, defining the time budget for all per-pixel arithmetic. |
| **Scanline** | One horizontal row of pixels in a video frame; Chrysalis operates on a per-scanline basis using a BRAM line buffer. |
| **Triangle wave** | A waveform that ramps linearly up then linearly down, used here as the fold function that converts a sawtooth address sweep into a mirror-symmetric sweep within each segment. |

---
