---
draft: true
sidebar_position: 236
slug: /instruments/videomancer/psychedelia
title: "Psychedelia"
image: /img/instruments/videomancer/psychedelia/psychedelia_hero.png
description: "Psychedelia recreates Jeff Minter's 1984 light synthesiser of the same name, originally released for the Commodore 64."
---

import psychedelia_hero from '/img/instruments/videomancer/psychedelia/psychedelia_hero.png';
import psychedelia_animation from '/img/instruments/videomancer/psychedelia/psychedelia_animation.gif';
import psychedelia_control_panel from '/img/instruments/videomancer/psychedelia/psychedelia_control_panel.png';
import psychedelia_exercise1_result from '/img/instruments/videomancer/psychedelia/psychedelia_exercise1_result.gif';
import psychedelia_exercise2_result from '/img/instruments/videomancer/psychedelia/psychedelia_exercise2_result.gif';
import psychedelia_exercise3_result from '/img/instruments/videomancer/psychedelia/psychedelia_exercise3_result.gif';

# Psychedelia

<span class="head2_nolink">Videomancer Program Guide</span>

:::warning
This document is still in progress, may contain errors, and is for preview only.
:::

<img src={psychedelia_hero} alt="Psychedelia hero image"/>
*Luminous stamp shapes radiate outward from multiple emitter points, painting trails of cycling colour across a persistently decaying framebuffer — a faithful recreation of Jeff Minter's 1984 Psychedelia light synthesiser.*
<img src={psychedelia_animation} alt="Psychedelia animated output"/>
*Psychedelia output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Psychedelia recreates Jeff Minter's 1984 light synthesiser of the same name, originally released for the Commodore 64. The program renders stamp shapes onto a persistent framebuffer, where each stamp is placed at the current emitter position and previous stamps gradually fade through a colour palette toward black. The result is a trail of radiating colour that responds to the emitter's motion — either controlled manually via Cursor X/Y or driven automatically by an internal Lissajous oscillator.

The name is Minter's original title for the program, which he described as a "light synthesiser" rather than a game. Released through Llamasoft in 1984, Psychedelia was one of the earliest pieces of interactive visual software designed purely for aesthetic experience. Minter's design philosophy — real-time generative visuals controlled by simple input gestures — anticipated the modern VJ and live visuals movement by decades.

Videomancer's FPGA implementation faithfully reproduces the core mechanics: a 64×64 framebuffer with 4-bit-per-pixel indexed colour, 8 stamp shapes with optional 4-way or 8-way symmetry, palette cycling with configurable pulse rate, and a Lissajous-driven automatic cursor mode. The Pulse Rate knob drives periodic colour injection, while the Decay control determines how quickly old stamps fade.

---

## Quick Start

1. **Reset is your friend**: The framebuffer accumulates indefinitely — use Reset to start fresh compositions rather than waiting for decay to clear old content.
2. **Pulse Rate and Speed interact**: High pulse rate with low speed fills the framebuffer quickly. Low pulse rate with high speed creates dotted spirograph-like lines.
3. **8-Way for mandalas**: 8-Way symmetry with auto cursor produces the most complex radial patterns — the Lissajous curve creates 8 simultaneous traces.

---

## Background

### Llamasoft Light Synthesisers

Jeff Minter's Llamasoft produced a series of light synthesiser programs throughout the 1980s. Psychedelia (1984) was the first, followed by Colourspace (1985), Trip-a-Tron (1987), and the Virtual Light Machine (1990s). Each built on the core concept of real-time framebuffer painting with persistence and palette cycling. The series evolved from simple stamp-and-trail effects to multi-layer composites, but all shared the principle that simple parameters should yield complex, evolving visual results. Videomancer implements this complete lineage as individual FPGA programs.

### Framebuffer Persistence and Decay

The 64×64 framebuffer acts as a visual memory: stamps are written at maximum brightness and gradually decrement toward zero over successive frames. The Decay knob controls how many brightness levels are decremented per frame — fast decay creates brief, sharp trails while slow decay builds up dense, long-lasting colour fields. This persistence model creates the characteristic "painting with light" aesthetic where emitter motion is traced as fading colour ribbons.

### Stamp Shapes and Symmetry

Eight stamp shapes are available, ranging from a single pixel to patterns spanning several cells. When symmetry is enabled, each stamp is replicated in 4 or 8 positions mirrored around the framebuffer centre, so a single emitter creates radiating mandala-like patterns. The combination of shape, symmetry, and Lissajous motion produces spirograph-like figures that evolve as the trajectory progresses.

### Lissajous Emitter Trajectories

In automatic cursor mode, the emitter follows a Lissajous curve — the superposition of two sinusoidal oscillations at different frequencies along the x and y axes. The Shape knob controls the frequency ratio, producing circles, figure-eights, and more complex interlocking loops. The Speed knob sets the traversal rate. This parametric trajectory, combined with framebuffer decay, generates the complex evolving mandalas that characterise the program's output.


---

## Signal Flow

```
 registers_in(0) ── Speed ─────────────────────────────────────────────────┐
 registers_in(1) ── Cursor X ──────────────────────────────────────────────┤
 registers_in(2) ── Cursor Y ──────────────────────────────────────────────┤
 registers_in(3) ── Pattern (8 steps) ─────────────────────────────────────┤
 registers_in(4) ── Bright ────────────────────────────────────────────────┤
 registers_in(5) ── Pulse Rate ────────────────────────────────────────────┤
 registers_in(6) ── Toggles [Cursor Man/Auto|Symmetry 4/8|Reset|ModVid|Bypass]
 registers_in(7) ── Mix Fader ─────────────────────────────────────────────┤
                                                                            │
 ┌─────────────────────────────────────────────────────────────────────────┘
 │
 │    ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
 ├───►│  EMITTER POS     │────►│  STAMP WRITE     │────►│  FRAMEBUFFER     │
 │    │  manual X/Y or   │     │  pattern shape    │     │  64×64 × 4bpp   │
 │    │  Lissajous auto  │     │  4/8-way symmetry │     │  palette decay   │
 │    └──────────────────┘     └──────────────────┘     └───────┬──────────┘
 │                                                              │
 │    ┌──────────────────┐     ┌──────────────────┐             │ 4-bit index
 │    │  PALETTE LOOKUP  │◄────│  DECAY ENGINE    │◄────────────┘
 │    │  16-colour table │     │  decrement per   │
 │    │  → YUV 10-bit   │     │  frame by decay  │
 │    └───────┬──────────┘     └──────────────────┘
 │            │
 │    ┌───────┴──────────┐
 │    │  PULSE & BRIGHT  │
 │    │  colour inject   │
 │    │  × brightness    │
 │    └───────┬──────────┘
 │            │
 │    ┌───────┴──────────┐
 └───►│  INTERPOLATOR    │
      │  dry/wet mix     │
      └──────────────────┘
               │
               ▼
          data_out (YUV)
```

On each frame, the emitter position is determined either by the Cursor X/Y knobs (Manual mode) or by a Lissajous oscillator (Auto mode). The stamp shape is plotted at the emitter position and, if symmetry is enabled, at its 4 or 8 mirror reflections. Stamp cells are written to maximum brightness.

Between stamp writes, the entire framebuffer undergoes a decay pass: each cell's 4-bit value is decremented by the Decay amount (clamped at zero). The Pulse Rate controls how frequently new stamps are injected — faster pulse rates write stamps more often, intensifying the trail density. The resulting 4-bit index is looked up in a 16-entry colour palette that maps brightness levels to spectral hues, creating the rainbow trail effect as stamps age.

---

## Parameter Reference

<img src={psychedelia_control_panel} alt="Videomancer front panel with Psychedelia loaded"/>
*Videomancer's front panel with Psychedelia active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Speed controls the rate of the Lissajous oscillator in Auto cursor mode — how quickly the emitter traverses its elliptical or figure-eight trajectory. In Manual mode this knob has no effect. Higher speeds produce tighter spiral-like trails with more overlapping stamps, while lower speeds allow individual stamp placements to be distinguishable.

---

#### Knob 2 — Cursor X
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Cursor X sets the horizontal emitter position in Manual cursor mode. In Auto mode this knob is overridden by the Lissajous x-oscillator. Sweeping X while Y is stationary produces a horizontal line of stamps.

---

#### Knob 3 — Cursor Y
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Cursor Y sets the vertical emitter position in Manual cursor mode. In Auto mode this knob is overridden by the Lissajous y-oscillator. Combining X and Y sweeps manually creates freehand drawing on the persistent framebuffer.

---

#### Knob 4 — Pattern
| Property | Value |
|----------|-------|
| Range | 0 – 7 |
| Default | 0 |

Pattern selects one of 8 stamp shapes that the emitter plots onto the framebuffer. Shape 0 is a single pixel, while higher patterns produce increasingly complex multi-cell stamps. Larger stamps create wider colour trails and fill the framebuffer more quickly. The visual character changes dramatically between patterns — compact dots create pointillistic fields while sprawling shapes produce broad washes.

---

#### Knob 5 — Bright
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Bright is a global luminance multiplier applied to the palette output. At zero the framebuffer content is invisible. At maximum the palette colours appear at their full designed intensity. This control interacts with the decay — brighter settings make older (lower-index) palette entries more visible, effectively extending the visible trail length.

---

#### Knob 6 — Pulse Rate
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Pulse Rate controls how frequently stamps are injected into the framebuffer. At minimum, stamps are written rarely, producing sparse trails with visible individual stamps. At maximum, stamps are written every frame, creating dense, continuous colour ribbons. This interacts strongly with Speed — fast movement with low pulse rate produces dotted lines, while slow movement with high pulse rate creates solid colour fills.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Cursor** | Manual | Auto |
| **8 — Symmetry** | 4-Way | 8-Way |
| **9 — Reset** | Off | Reset |
| **10 — Mod Vid** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles configure the emitter behaviour and rendering mode. Cursor switches between manual and automatic Lissajous control. Symmetry selects 4-way or 8-way mirroring. Reset clears the framebuffer. Mod Video and Bypass handle video compositing.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Mix crossfades between the dry input and the synthesised psychedelia output. At minimum the output is entirely dry. At maximum the output is entirely wet. Intermediate values overlay the colour trails onto the source video.





---

## Guided Exercises

These exercises progress from understanding the basic stamp mechanics to creating complex symmetric mandalas and video-composite performances.

### Exercise 1: Manual Single-Point Trail

<img src={psychedelia_exercise1_result} alt="Manual Single-Point Trail result"/>
*Manual Single-Point Trail — simulated result across source images.*
**What You'll Create**: Learn the stamp, palette, and decay mechanics by manually painting a trail across the framebuffer.

1. Set Cursor to Manual.
2. Set Pattern to 0 (single pixel stamp).
3. Set Symmetry to 4-Way.
4. Set Pulse Rate to approximately 60%.
5. Set Bright to approximately 80%.
6. Set Mix to 100%.
7. Slowly sweep Cursor X from left to right while holding Cursor Y at centre.
8. Observe the colour trail fading behind the emitter position.
9. Pause and note the decay gradient — newest stamps are brightest, oldest fade through the palette.
10. Toggle Reset to clear and try a diagonal sweep with both X and Y.

**Key concepts**: Stamp placement, palette decay, manual emitter control, 4-way symmetry.

---

### Exercise 2: Automatic Lissajous Mandala

<img src={psychedelia_exercise2_result} alt="Automatic Lissajous Mandala result"/>
*Automatic Lissajous Mandala — simulated result across source images.*
**What You'll Create**: Create an evolving symmetric mandala using automatic Lissajous cursor motion.

1. Set Cursor to Auto.
2. Set Symmetry to 8-Way for maximum radial symmetry.
3. Set Pattern to 4 (medium stamp).
4. Set Speed to approximately 30%.
5. Set Pulse Rate to approximately 50%.
6. Set Bright to full.
7. Set Mix to 100%.
8. Observe the emitter tracing a Lissajous figure, with 8-way symmetry creating mandala patterns.
9. Slowly adjust Speed to change the trajectory shape.
10. Let the pattern evolve for 30 seconds to see how decay creates depth.

**Key concepts**: Lissajous trajectories, 8-way symmetry, trail accumulation, speed and trajectory shape.

---

### Exercise 3: Video-Modulated Mandala Overlay

<img src={psychedelia_exercise3_result} alt="Video-Modulated Mandala Overlay result"/>
*Video-Modulated Mandala Overlay — simulated result across source images.*
**What You'll Create**: Layer a Lissajous mandala over live video for a performance-ready composite.

1. Continue from Exercise 2 with Auto cursor and 8-Way symmetry.
2. Enable Mod Video.
3. Set Mix to approximately 65%.
4. Feed a video source with strong contrast.
5. Observe how the video luminance masks the mandala pattern.
6. Adjust Bright and Pulse Rate to balance pattern density with video visibility.
7. Try toggling between 4-Way and 8-Way symmetry to compare kaleidoscopic effects.
8. Use Reset periodically to clear accumulated trails and start fresh compositions.

**Key concepts**: Video modulation, overlay compositing, symmetry comparison, dynamic reset.

---


## Tips

- **Manual for drawing**: Switch to Manual mode to hand-draw patterns. Sweep both X and Y slowly for curved lines, or move one axis quickly for horizontal/vertical stripes.
- **Larger stamps fill faster**: Pattern 7 covers many cells per write, filling the framebuffer and creating broad colour washes. Pattern 0 produces fine pointillistic detail.
- **Bright extends trail visibility**: Higher brightness makes older (lower palette index) stamps visible longer, effectively lengthening the apparent trail without changing the actual decay rate.
- **Use video modulation for masking**: Mod Video creates windows into the psychedelia pattern shaped by the input video — high-contrast sources like silhouettes work best.

---
