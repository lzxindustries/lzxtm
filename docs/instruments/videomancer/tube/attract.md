---
draft: true
sidebar_position: 10
slug: /instruments/videomancer/attract
title: "Attract"
image: /img/instruments/videomancer/attract/attract_hero_s1.png
description: "Attract simulates the cumulative degradation of a CRT (cathode-ray tube) monitor that has been left running with a static image for extended periods — the \"attract mode\" phenomenon from decades-old arcade cabinets where demo loops would permanently etch game logos and score readouts into the phosphor screen."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import attract_source1_boat from '/img/instruments/videomancer/attract/attract_source1_boat.png';
import attract_source2_cat from '/img/instruments/videomancer/attract/attract_source2_cat.png';
import attract_source3_turtle from '/img/instruments/videomancer/attract/attract_source3_turtle.png';
import attract_source4_pattern from '/img/instruments/videomancer/attract/attract_source4_pattern.png';
import attract_source5_man from '/img/instruments/videomancer/attract/attract_source5_man.png';
import attract_source6_berries from '/img/instruments/videomancer/attract/attract_source6_berries.png';
import attract_hero_s1 from '/img/instruments/videomancer/attract/attract_hero_s1.png';
import attract_hero_s2 from '/img/instruments/videomancer/attract/attract_hero_s2.png';
import attract_hero_s3 from '/img/instruments/videomancer/attract/attract_hero_s3.png';
import attract_hero_s4 from '/img/instruments/videomancer/attract/attract_hero_s4.png';
import attract_hero_s5 from '/img/instruments/videomancer/attract/attract_hero_s5.png';
import attract_hero_s6 from '/img/instruments/videomancer/attract/attract_hero_s6.png';
import attract_ex1_s1 from '/img/instruments/videomancer/attract/attract_ex1_s1.png';
import attract_ex1_s2 from '/img/instruments/videomancer/attract/attract_ex1_s2.png';
import attract_ex1_s3 from '/img/instruments/videomancer/attract/attract_ex1_s3.png';
import attract_ex1_s4 from '/img/instruments/videomancer/attract/attract_ex1_s4.png';
import attract_ex1_s5 from '/img/instruments/videomancer/attract/attract_ex1_s5.png';
import attract_ex1_s6 from '/img/instruments/videomancer/attract/attract_ex1_s6.png';
import attract_ex2_s1 from '/img/instruments/videomancer/attract/attract_ex2_s1.png';
import attract_ex2_s2 from '/img/instruments/videomancer/attract/attract_ex2_s2.png';
import attract_ex2_s3 from '/img/instruments/videomancer/attract/attract_ex2_s3.png';
import attract_ex2_s4 from '/img/instruments/videomancer/attract/attract_ex2_s4.png';
import attract_ex2_s5 from '/img/instruments/videomancer/attract/attract_ex2_s5.png';
import attract_ex2_s6 from '/img/instruments/videomancer/attract/attract_ex2_s6.png';
import attract_ex3_s1 from '/img/instruments/videomancer/attract/attract_ex3_s1.png';
import attract_ex3_s2 from '/img/instruments/videomancer/attract/attract_ex3_s2.png';
import attract_ex3_s3 from '/img/instruments/videomancer/attract/attract_ex3_s3.png';
import attract_ex3_s4 from '/img/instruments/videomancer/attract/attract_ex3_s4.png';
import attract_ex3_s5 from '/img/instruments/videomancer/attract/attract_ex3_s5.png';
import attract_ex3_s6 from '/img/instruments/videomancer/attract/attract_ex3_s6.png';

# Attract

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Boat", before: attract_source1_boat, after: attract_hero_s1 },
    { label: "Cat", before: attract_source2_cat, after: attract_hero_s2 },
    { label: "Turtle", before: attract_source3_turtle, after: attract_hero_s3 },
    { label: "Pattern", before: attract_source4_pattern, after: attract_hero_s4 },
    { label: "Man", before: attract_source5_man, after: attract_hero_s5 },
    { label: "Berries", before: attract_source6_berries, after: attract_hero_s6 },
  ]}
/>
*Attract rendering a static image as a degraded CRT display — phosphor burn-in ghosting doubles the subject, radial vignette darkens the edges, convergence error shifts the chroma channels horizontally, and alternating scanline dimming adds horizontal structure.*

---

## Overview

Attract simulates the cumulative degradation of a CRT (cathode-ray tube) monitor that has been left running with a static image for extended periods — the "attract mode" phenomenon from decades-old arcade cabinets where demo loops would permanently etch game logos and score readouts into the phosphor screen. The program composites five distinct aging effects: phosphor burn-in via an IIR accumulator, convergence error (horizontal chroma channel offset), radial vignette brightness falloff, colour purity drift (position-dependent hue corruption), and scanline dimming.

The burn-in effect uses BRAM as a per-scanline accumulator: each pixel's brightness is slowly blended into a persistent memory that represents the "ghost" burned into the phosphor. The burn rate controls how quickly new content writes into the accumulator, and the burn intensity controls how visible the ghost is in the output. The convergence effect simulates the misalignment of the three electron guns (R, G, B) in a colour CRT by horizontally offsetting the U and V chroma channels via 8-deep shift register delay lines.

At moderate settings, the program adds authentic CRT aging character — darkened edges, subtle colour fringing, and a faint ghost of bright areas. At extreme settings, the image is dramatically degraded: heavy vignette tunnels vision to the centre, strong purity drift shifts colours across the screen, and visible scanlines impose horizontal structure.

---

## Background

### What Is Phosphor Burn-In?

**Burn-in** (also called "screen burn" or "image retention") occurs when a static image is displayed on a CRT for extended periods. The phosphor coating on the CRT faceplate loses efficiency in areas that are continuously excited by the electron beam. These degraded phosphor regions glow less brightly than surrounding areas, creating a permanent negative ghost of the static image. The effect is cumulative and irreversible — once burned, the phosphor cannot recover.

The name "attract mode" comes from arcade game terminology: when no one was playing, the cabinet would run an automated demo loop (the "attract mode") to draw players' attention. Because many arcade operators left cabinets running 24/7, the demo loop — typically showing the game's title screen, high scores, and brief gameplay — would gradually burn into the monitor.

### What Is Convergence Error?

A colour CRT uses three electron guns (red, green, blue) that must be precisely aligned so their beams strike the correct phosphor dots simultaneously. **Convergence error** occurs when the guns go out of alignment — typically due to drift in the magnetic deflection system, physical shock, or thermal expansion over decades. The result is visible colour fringing: red, green, and blue components of the image don't quite overlap, creating coloured halos around high-contrast edges. In this program, convergence is simulated by horizontally delaying the U and V chroma channels relative to Y luma using shift registers.

### What Is Colour Purity?

**Colour purity** refers to whether each electron gun's beam strikes only its assigned phosphor dots. On a CRT with perfect purity, each gun illuminates only its colour. With degraded purity, beams drift and begin to excite neighbouring phosphor dots of other colours. This creates colour casts that vary across the screen — one corner might shift warm (reddish), another cool (bluish), and the edges might gain a green tint. In this program, purity drift is simulated by applying position-dependent UV offsets based on the pixel's distance and direction from the screen centre.

### What Is Radial Vignette?

CRT displays naturally darken at the edges because the electron beam must travel further from the deflection yoke to reach the corners, spreading the beam and reducing phosphor excitation. Additionally, the flat (or slightly curved) glass faceplate attenuates light more at shallow viewing angles near the edges. This creates a natural brightness falloff from centre to edge called **vignette**. The program simulates this by computing each pixel's distance from the screen centre using an alpha-max-beta-min approximation and subtracting a proportional brightness reduction.


---

## Signal Flow

```
Input Video (YUV 4:4:4 30-bit)
│
├── Y Channel ──────────────────────────────────────────────────────
│   │
│   ├─ 1.  Input register + convergence delay writes
│   ├─ 2.  Convergence reads (U/V from shift register)
│   │       + linearity DDA
│   ├─ 3a. Burn-in IIR accumulator        (BRAM read → IIR update →
│   │       + burn × intensity multiply    BRAM write; burn_rate controls
│   │                                       shift 4-12)
│   ├─ 3b. Burn wear scaling              (burn_contrib × wear → scale
│   │       + saturating add               on Y burned)
│   ├─ 4a. Distance computation            (alpha-max + beta-min from
│   │       + purity case select           screen centre; position UV bias)
│   ├─ 4b. Vignette first multiply        (distance × vignette_amt)
│   └─ 4c. Wear scaling + purity apply    (vig × wear subtracted from Y;
│           + scanline dim                  purity added to U/V;
│                                           alternating-line Y reduction)
│
├── Sync Signals ───────────────────────────────────────────────────
│   └─ 12-clock delay pipeline             (align with processing depth)
│
├── Interpolator (4 clocks per channel) ────────────────────────────
│   └─ Mix = lerp(input_delayed, processed, mix_amount)
│
└── Output ─────────────────────────────────────────────────────────
    └─ Y/U/V from interpolator mix
```

The burn-in accumulator uses BRAM as a 2048×10-bit memory that persists across lines. On each pixel clock, the current accumulator value is read, updated via IIR (blending a small fraction of the current input Y), and written back. The burn rate pot maps to a shift amount (4-12): higher pot = smaller shift = faster accumulation. The burn contribution is then multiplied by the intensity pot and scaled by the wear master pot.

The purity modes are selected by the bottom 2 bits of the toggle register. Each mode computes a signed UV offset from the pixel's screen position: "Warm/Cool" uses dx and dy directly, "Green Drift" uses negative distance for both channels, and "Rainbow" uses dx and -dy. The offsets are scaled by the wear pot before application.

---

## Parameter Reference

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Burn Rate
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the speed at which the burn-in accumulator absorbs new content. At low values, the IIR shift is large (12) — the burn builds very slowly over many frames, creating a delayed ghost that takes a long time to form. At high values, the shift is small (4) — the burn accumulates quickly, with the ghost following the input closely. Moderate values (25-50%) create a realistic slow burn where static elements gradually imprint.

---

#### Knob 2 — Burn Intns
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the visibility of the burn-in ghost in the output image. At 0%, the burn accumulator runs internally but does not affect the output — no ghost is visible. At higher values, the accumulated burn pattern is multiplied by the intensity and added to the luma, making the ghost brighter. At maximum, the ghost is very prominent and adds significant brightness to the image.

---

#### Knob 3 — Convergence
| Property | Value |
|----------|-------|
| Range | 0 – 8 |
| Default | 2 |

Controls the convergence error — the horizontal pixel offset between the Y (luma) and U/V (chroma) channels. At 0, there is no offset and all channels are perfectly aligned. At maximum, the U channel is delayed by up to 8 pixels relative to Y, creating visible colour fringing on vertical edges. The V channel remains aligned with Y, so the shift is asymmetric — this simulates how CRT convergence error typically affects one gun more than the others.

---

#### Knob 4 — Vignette
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the intensity of the radial vignette effect — the brightness falloff from centre to edge. At 0%, there is no falloff and brightness is uniform. At moderate values, the edges and corners darken, creating a natural CRT-like circular viewing area. At maximum, the vignette is very strong and only the central area retains significant brightness.

---

#### Knob 5 — Linearity
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the linearity distortion — barrel or pincushion geometric warping of the scan pattern. This emulates the geometric distortion caused by the interaction between flat faceplate geometry and the curved magnetic deflection field in CRT displays. The Distort toggle selects between barrel (edges pushed in) and pincushion (edges pulled out) distortion direction.

---

#### Knob 6 — Wear
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the master aging wear level. This scales multiple effects simultaneously: the burn-in contribution, the vignette attenuation, and the purity shift magnitude all multiply through the wear pot. At 0%, no aging effects are visible regardless of other settings. At 50%, effects are moderate. At 100%, effects are at full strength. Think of this as "how many years has this monitor been running?"

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Purity** | None | Warm/Cool |
| **8 — Distort** | Barrel | Pincushon |
| **9 — Burn Reset** | Off | On |
| **10 — Scanlines** | Off | On |
| **11 — Bypass** | Off | On |

Toggle 7 is a **4-position purity mode selector** using the bottom 2 bits of the toggle register: None (00), Warm/Cool (01), Green Drift (10), Rainbow (11). Toggle 8 selects distortion direction (barrel vs pincushion). Toggle 9 is the burn reset control. Toggle 10 enables scanline dimming.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade between the original input video (delayed to match the 12-clock processing pipeline plus 4-clock interpolator) and the CRT aging output. At 0%, pure unprocessed input. At 100%, fully processed CRT degradation.

---

## Guided Exercises

These exercises progress from individual CRT aging effects through combined degradation to the full attract mode simulation, building an understanding of how each effect contributes to the overall CRT aging character.

### Exercise 1: Vignette and Scanlines

<BeforeAfterSlider
  sources={[
    { label: "Boat", before: attract_source1_boat, after: attract_ex1_s1 },
    { label: "Cat", before: attract_source2_cat, after: attract_ex1_s2 },
    { label: "Turtle", before: attract_source3_turtle, after: attract_ex1_s3 },
    { label: "Pattern", before: attract_source4_pattern, after: attract_ex1_s4 },
    { label: "Man", before: attract_source5_man, after: attract_ex1_s5 },
    { label: "Berries", before: attract_source6_berries, after: attract_ex1_s6 },
  ]}
/>
*Vignette and Scanlines — simulated result across source images.*
**Source**: Any well-exposed image — uniform brightness distribution is ideal for vignette observation.

**Objective**: Understand the radial vignette and scanline effects that define the basic CRT viewing experience.

1. **Isolate vignette**: Set Vignette to ~50%, all other effects to 0 (Burn Rate 0, Burn Intns 0, Convergence 0, Wear at 100% to allow effects through).
2. **Observe falloff**: The image darkens toward all four edges and corners. The centre remains at full brightness.
3. **Increase vignette**: Push to ~80%. Strong tunnel vision effect — only the central area is bright.
4. **Add scanlines**: Toggle Scanlines On. Alternating horizontal lines darken, adding visible scan structure.
5. **Low vignette + scanlines**: Reduce Vignette to ~25% but keep Scanlines On. Subtle but authentic CRT look.
6. **Zoom observation**: Look closely at horizontal edges — the scanline effect is most visible on bright horizontal features.

**Key concepts**: Radial distance from centre (alpha-max + beta-min), vignette as subtractive brightness, scanline alternating-line dimming

---

### Exercise 2: Convergence Error and Purity Drift

<BeforeAfterSlider
  sources={[
    { label: "Boat", before: attract_source1_boat, after: attract_ex2_s1 },
    { label: "Cat", before: attract_source2_cat, after: attract_ex2_s2 },
    { label: "Turtle", before: attract_source3_turtle, after: attract_ex2_s3 },
    { label: "Pattern", before: attract_source4_pattern, after: attract_ex2_s4 },
    { label: "Man", before: attract_source5_man, after: attract_ex2_s5 },
    { label: "Berries", before: attract_source6_berries, after: attract_ex2_s6 },
  ]}
/>
*Convergence Error and Purity Drift — simulated result across source images.*
**Source**: Image with high-contrast vertical edges and varied colours — architecture, text overlays, or graphic patterns.

**Objective**: Explore how convergence error and purity drift introduce colour artefacts typical of aging CRT monitors.

1. **Add convergence**: Set Convergence to ~50% (about 4 pixels). Look at vertical edges — you should see colour fringing.
2. **Maximum convergence**: Push to 100% (8 pixel delay). Very obvious colour separation.
3. **Subtle convergence**: Back to ~25% (2 pixels). Barely visible but adds character on fine detail.
4. **Add purity**: Toggle Purity to Warm/Cool. Notice colour casts that vary across the screen — warmer in one direction, cooler in the other.
5. **Green drift**: Toggle Purity to Grn Drift. The edges gain a green tint that increases toward the corners.
6. **Rainbow**: Toggle Purity to Rainbow. The full spectrum rotates around the screen centre.
7. **Scale with wear**: Reduce Wear to ~50%. The purity effect halves in strength.

**Key concepts**: Convergence as chroma delay, purity as position-dependent UV offset, wear as master scale

---

### Exercise 3: Full Attract Mode Simulation

<BeforeAfterSlider
  sources={[
    { label: "Boat", before: attract_source1_boat, after: attract_ex3_s1 },
    { label: "Cat", before: attract_source2_cat, after: attract_ex3_s2 },
    { label: "Turtle", before: attract_source3_turtle, after: attract_ex3_s3 },
    { label: "Pattern", before: attract_source4_pattern, after: attract_ex3_s4 },
    { label: "Man", before: attract_source5_man, after: attract_ex3_s5 },
    { label: "Berries", before: attract_source6_berries, after: attract_ex3_s6 },
  ]}
/>
*Full Attract Mode Simulation — simulated result across source images.*
**Source**: Static image with high-contrast elements — game screenshot, text overlay, or graphic with bright logos on dark background.

**Objective**: Create the complete attract mode effect by combining burn-in with all other CRT aging artefacts.

1. **Enable burn-in**: Set Burn Rate to ~40%, Burn Intns to ~50%.
2. **Add aging**: Convergence ~25%, Vignette ~35%, Wear ~70%.
3. **Purity and scanlines**: Purity to Warm/Cool, Scanlines On.
4. **Observe burn**: With a static source, the burn accumulator is continuously reinforced. The burn ghost adds a brightness overlay proportional to source content.
5. **Reset burn**: Toggle Burn Reset On and back Off. The ghost is cleared — observe the output without burn, then watch it slowly rebuild.
6. **Adjust burn rate**: Try fast burn (Burn Rate ~80%) — the ghost forms quickly. Try slow burn (~15%) — the ghost builds imperceptibly over time.
7. **Full degradation**: All effects moderate, Wear at ~60%. Authentic aged arcade monitor.

**Key concepts**: Burn-in IIR accumulator, burn rate as temporal smoothing, burn reset, combined aging effects, wear as global modulator

---


## Tips

- **Wear is the master**: Set Wear first — it scales burn, vignette, and purity together. Start at ~50% and adjust individual effects from there.
- **Subtle convergence is most realistic**: Real CRT convergence error is typically 1-3 pixels at most. Values above 4 are exaggerated for creative effect.
- **Warm/Cool purity is the most common**: Most real CRT purity drift creates warm/cool corners. Green Drift and Rainbow are more extreme and artistic.
- **Slow burn for realism**: Real phosphor burn-in takes hours or days. A burn rate of 10-25% creates a slow, gradual ghost that feels authentic.
- **Burn Reset for fresh starts**: If the burn ghost becomes too strong or undesirable, toggle Burn Reset to clear it and start accumulating anew.
- **Scanlines sell the CRT look**: Even without other effects, scanline dimming immediately reads as "CRT monitor" to most viewers.
- **Vignette enhances other effects**: The darkened edges created by vignette make convergence and purity effects more visible at the periphery.
- **Combine with feedback**: Routing Attract's output back as input creates recursive burn that converges to a self-reinforcing ghost.
- **Low wear + scanlines only**: For a clean CRT look without degradation, set Wear to 0% and enable only Scanlines.

---

## Glossary

| Term | Definition |
|------|------------|
| **Alpha-max beta-min** | A fast approximation algorithm for computing distance from the origin without square roots, used here for radial vignette distance calculation. |
| **BRAM** | Block RAM; dedicated memory blocks within the FPGA used for the per-scanline burn-in accumulator. |
| **Burn-in** | Permanent degradation of CRT phosphor coating where a static image reduces phosphor efficiency, leaving a visible ghost of the displayed content. |
| **Colour purity** | The accuracy with which each CRT electron gun excites only its assigned phosphor dots; degraded purity causes position-dependent colour casts across the screen. |
| **Convergence** | The alignment of the three colour electron gun beams in a CRT; convergence error produces visible colour fringing when beams strike misaligned phosphor dots. |
| **CRT** | Cathode-Ray Tube; a vacuum tube display technology that produces images by scanning an electron beam across a phosphor-coated screen. |
| **DDA** | Digital Differential Analyzer; an incremental algorithm for computing evenly spaced coordinate steps, used here for linearity distortion. |
| **IIR** | Infinite Impulse Response; a filter structure where output depends on both current input and previous output, creating the temporal smoothing used in the burn-in accumulator. |
| **Phosphor** | The luminescent coating on the inside of a CRT faceplate that glows when struck by an electron beam and degrades with prolonged use. |
| **Scanline** | A single horizontal line traced by the electron beam during one pass across the CRT screen; alternating-line dimming simulates the visible gaps between scan lines. |
| **Vignette** | A gradual darkening of the image from centre to edges, caused on CRT displays by electron beam spread and glass attenuation at the screen periphery. |
| **YUV** | A colour model separating luminance (Y) from chrominance (U, V); the native format of Videomancer's 30-bit video pipeline. |

---
