---
draft: false
sidebar_position: 5
slug: /instruments/videomancer/faultplane
title: "Faultplane"
---

import faultplane_hero from '/img/instruments/videomancer/faultplane/faultplane_hero.png';
import faultplane_control_panel from '/img/instruments/videomancer/faultplane/faultplane_control_panel.png';
import faultplane_exercise2_result from '/img/instruments/videomancer/faultplane/faultplane_exercise2_result.png';
import faultplane_exercise3_result from '/img/instruments/videomancer/faultplane/faultplane_exercise3_result.png';

# Faultplane

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={faultplane_hero} alt="Faultplane processed video output showing spatial displacement, mirroring, and zone-based fracture effects"/>

---

## Overview

**Faultplane** is a spatial displacement and zone-blanking program that splits the video frame into alternating regions using two timing accumulators and applies independent horizontal pixel shifts, mirror flips, and color inversions to each region. The name refers to geological fault planes — surfaces where rock masses shift along a boundary. In Faultplane, the video image is fractured along oscillating boundaries and the fragments are displaced, mirrored, and inverted relative to one another.

The program divides the image into spatial zones using two frequency-driven accumulators — one operating at the line rate (creating horizontal bands) and one at the pixel rate (creating vertical columns). The XOR of these two oscillators produces a checkerboard-like pattern of alternating regions. Each region reads from a dual-port line buffer at a different horizontal offset, creating the visual impression of the image being fractured and shifted along fault lines.

Two independent parameter sets — **Top** and **Bottom** — control the displacement, mirroring, and inversion applied to each region. A blanking threshold gates both accumulators, allowing portions of the image to be replaced with black where both oscillator outputs are below a programmable level.

---

## Background

### Delay Lines and Spatial Displacement

At the heart of Faultplane is a **mirror delay line** — a dual-port line buffer that writes incoming pixels into RAM and reads them back at a different address. By varying the read offset, pixels are shifted horizontally within the scan line. Small offsets produce subtle echo effects; large offsets produce dramatic horizontal displacement where distant parts of the line wrap around and replace nearby content.

The delay line uses two independent RAMs (A and B) that alternate every scan line. While one RAM is being written with new data, the other holds the previous line's data and can be read freely. This dual-buffer architecture allows the FPGA to simultaneously write and read without conflicts, and enables different processing (mirror, invert) to be applied to each buffer independently.

### Timing Accumulators and Spatial Zoning

Faultplane's two **timing accumulators** generate oscillating signals at programmable frequencies:

- **Accumulator A** (Vert Freq, Knob 3) operates at the **line rate** — it increments once per scan line and resets at the start of each frame. The result is a periodic signal whose period spans multiple lines, creating **horizontal bands** across the image.
- **Accumulator B** (Horiz Freq, Knob 6) operates at the **pixel rate** — it increments every clock cycle and resets at the start of each line. This creates a periodic signal within each line, producing **vertical columns**.

The MSB (most significant bit) of each accumulator acts as a clock divider. The XOR of the two MSBs creates the **zone selection signal** (`ab_sel`), which alternates between selecting the Top parameter set and the Bottom parameter set. At low frequencies the zones are wide (large bands or columns); at high frequencies they are narrow (fine stripes).

### Mirror and Invert

Each zone can independently **mirror** (horizontally flip the write address) and **invert** (apply bitwise NOT to the pixel data). Mirroring causes the pixel data within a zone to be written in reverse order, so when read back at the same position it appears horizontally flipped. Inversion negates every bit of the YUV data, producing a color and luminance negative.

### Processing Amplifier (Displacement Control)

Each accumulator's output is fed through a **proc_amp** (processing amplifier) that applies brightness (DC offset) and contrast (gain) to compute the read offset for the delay line:

- **Delay** (Knob 1 / Knob 4) = brightness — sets the DC offset of the displacement. This shifts the entire zone's read position by a fixed amount.
- **Displace** (Knob 2 / Knob 5) = contrast — scales the accumulator's oscillating output to vary the displacement dynamically. Higher values create displacement that sweeps back and forth across the line as the accumulator oscillates.

---

## Signal Flow

```
Input Video (YUV 4:4:4 30-bit)
│
├── Timing ──────────────────────────────────────────────────────
│   │
│   ├─ Video Timing Generator (extract hsync, vsync, avid)
│   │
│   ├─ Accumulator A (Vert Freq — line rate, creates horiz bands)
│   │   ├── → proc_amp A (Top Delay = brightness, Top Displace = contrast)
│   │   └── → rd_offset_a (11-bit read offset for delay line)
│   │
│   ├─ Accumulator B (Horiz Freq — pixel rate, creates vert columns)
│   │   ├── → proc_amp B (Bot Delay = brightness, Bot Displace = contrast)
│   │   └── → rd_offset_b (11-bit read offset for delay line)
│   │
│   └─ ab_sel = MSB(acc_a) XOR MSB(acc_b) — zone selection
│
├── Mirror Delay Line (dual-port RAM, 2048 × 30-bit) ──────────
│   │
│   ├─ RAM A: writes on even lines
│   │   ├── Write addr: normal or mirrored (Top Flip)
│   │   └── Write data: normal or inverted (Top Invert)
│   │
│   ├─ RAM B: writes on odd lines
│   │   ├── Write addr: normal or mirrored (Bot Flip)
│   │   └── Write data: normal or inverted (Bottom Invert)
│   │
│   └─ Read: ab_sel selects RAM A or B, offset selects position
│
├── Zone Blanking ──────────────────────────────────────────────
│   └─ If both acc_a AND acc_b < Line Blank threshold:
│      ├── Blank: Y=0, U=512, V=512 (black, neutral chroma)
│      └── Blank Invert: reverses the blank condition
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Pass-through (hsync, vsync, field, avid)
│
└── Output Video (YUV 4:4:4 30-bit)
```

Key interactions:

1. **Zone geometry**: The two accumulators create a grid of zones. Vert Freq controls the height of horizontal bands. Horiz Freq controls the width of vertical columns. The XOR of their MSBs creates a checkerboard-like alternation where adjacent zones use opposite parameter sets.

2. **Displacement independence**: Each zone has its own delay (DC offset) and displace (oscillating amplitude). This means adjacent zones can show different horizontal shifts of the same source image, creating the visual illusion of the image being fractured along the zone boundaries.

3. **Mirror and invert are per-zone**: Top Flip and Top Invert affect even-line RAM writes. Bot Flip and Bottom Invert affect odd-line RAM writes. This means zones that read from different RAMs display differently mirrored or inverted content.

---

## Parameter Reference

<img src={faultplane_control_panel} alt="Videomancer front panel with Faultplane loaded, controls annotated"/>

*Videomancer's front panel with Faultplane active. Knobs 1–6, Switches 7–11, and Fader 12 are labeled with their Faultplane functions.*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Top Delay
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% (center) |
| Suffix | % |

Controls the **DC offset** of the horizontal displacement for zones reading from RAM A (the "Top" parameter set). This is the brightness input to proc_amp A. At 0%, the read position is shifted to one extreme. At 50% (center), the displacement is centered. At 100%, the read position is shifted to the opposite extreme. Combined with Top Displace, this sets the baseline around which the oscillating displacement varies.

Think of this as setting *where* the fracture displacement is centered — the fixed horizontal shift applied to one set of zones.

---

#### Knob 2 — Top Displace
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% (center) |
| Suffix | % |

Controls the **gain** (contrast) applied to Accumulator A's output before it becomes the read offset for the Top zones. This is the contrast input to proc_amp A. At 0%, the accumulator output is attenuated to zero — the displacement is purely the static offset from Top Delay. At 50%, moderate displacement variation. At 100%, maximum displacement variation — pixels in the Top zones sweep across a large horizontal range as the accumulator oscillates.

This control determines *how much* the displacement varies within a zone. Low values create uniform shifts; high values create dramatic sweeping distortions.

---

#### Knob 3 — Vert Freq
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% (center) |
| Suffix | % |

Controls the **frequency** of Accumulator A, which operates at the line rate. This determines the number of horizontal bands per frame. At low values, the accumulator cycles slowly — few wide bands. At high values, rapid cycling — many narrow bands. At 0%, the accumulator may not complete a single cycle, producing a single zone. At 100%, dozens of thin horizontal stripes alternate between Top and Bottom parameter sets.

This control sets the vertical spatial frequency of the zone pattern. Combined with Horiz Freq, it defines the overall grid geometry.

---

#### Knob 4 — Bot Delay
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% (center) |
| Suffix | % |

Controls the **DC offset** of the horizontal displacement for zones reading from RAM B (the "Bottom" parameter set). Same function as Top Delay but for the opposite set of zones. Setting Top Delay and Bot Delay to different values creates visible displacement discontinuities at zone boundaries — one set of zones is shifted one way, the adjacent set is shifted another way.

---

#### Knob 5 — Bot Displace
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% (center) |
| Suffix | % |

Controls the **gain** applied to Accumulator B's output for the Bottom zones. Same function as Top Displace but for the opposite set of zones. Independent control of Top and Bottom displacement gain creates asymmetric distortion — one set of zones can have subtle shifts while the other has dramatic sweeping displacement.

---

#### Knob 6 — Horiz Freq
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% (center) |
| Suffix | % |

Controls the **frequency** of Accumulator B, which operates at the pixel rate. This determines the number of vertical columns per line. At low values, wide vertical columns. At high values, many narrow vertical stripes. At 0%, the accumulator may not complete a cycle within a line, producing a single vertical zone. At 100%, fine vertical striping alternates between parameter sets.

Combined with Vert Freq, this creates the full zone grid. Equal settings produce roughly square zones. Unequal settings produce rectangular zones — tall and narrow, or short and wide.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Top Flip** | Normal write order (RAM A) | Mirrored write order (RAM A) |
| **8 — Bot Flip** | Normal write order (RAM B) | Mirrored write order (RAM B) |
| **9 — Top Invert** | Normal data (RAM A) | Bitwise NOT data (RAM A) |
| **10 — Bottom Invert** | Normal data (RAM B) | Bitwise NOT data (RAM B) |
| **11 — Blank Invert** | Blank when accumulators low | Blank when accumulators high |

**Top Flip** reverses the horizontal write address for RAM A. When a zone reads from mirrored RAM A data, the pixels appear horizontally flipped. The boundary between a mirrored zone and a normal zone creates a reflection axis — the image folds back on itself like a kaleidoscopic mirror.

**Bot Flip** does the same for RAM B. Enabling both flips creates mirroring in all zones. Enabling only one creates an asymmetry — half the zones reflect, half don't.

**Top Invert** applies bitwise NOT to the YUV data before writing to RAM A. Zones that read from inverted RAM A data display a color and luminance negative. This is a full 30-bit inversion (Y, U, and V channels), producing complementary colors and inverted brightness simultaneously.

**Bottom Invert** does the same for RAM B. Combining one inverted and one normal zone set creates alternating positive/negative stripes.

**Blank Invert** reverses the blanking condition. Normally, regions where both accumulators are below the Line Blank threshold are blanked to black. With Blank Invert on, regions where both accumulators are *above* the threshold are blanked instead — the visible and blanked regions swap.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Line Blank
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% (center) |
| Suffix | % |

The Line Blank fader sets a threshold for zone blanking. The threshold is compared against the upper 10 bits of both accumulator outputs. When **both** accumulators are below the threshold, the output is blanked — Y is forced to 0 (black) and U/V are forced to 512 (neutral chroma). At 0%, no blanking occurs. At 100%, the maximum threshold means large portions of the frame are blanked. The Blank Invert switch (Switch 11) reverses this logic.

Because the accumulators oscillate, the blanking creates periodic regions of black that align with the zone grid. This allows portions of the displaced/mirrored/inverted image to be selectively hidden, creating cutout and stencil effects.

---

## Guided Exercises

### Exercise 1: Horizontal Displacement Bands

**Source**: A live camera feed or footage with recognizable horizontal features — text, architecture, or landscapes with horizon lines.

**Objective**: Learn how the vertical accumulator creates horizontal bands of displaced image content.

1. **Initialize**: Load Faultplane with all defaults. The image should show some spatial distortion from the default displacements.

2. **Isolate the vertical bands**: Set **Horiz Freq** (Knob 6) fully CCW to disable horizontal zoning. Now only Accumulator A (vertical) is creating zones.

3. **Set the frequency**: Set **Vert Freq** (Knob 3) to about 30%. A few wide horizontal bands appear, alternating between Top and Bottom parameter zones.

4. **Displace one set**: Set **Top Delay** (Knob 1) fully CCW and **Top Displace** (Knob 2) to about 70%. Set **Bot Delay** (Knob 4) to center and **Bot Displace** (Knob 5) to 0%. Now one set of bands shows displaced image content (shifted horizontally) while the other set shows relatively undisplaced content.

5. **Vary the displacement**: Sweep **Top Delay** slowly. Watch the displaced bands shift their content left and right. The zone boundaries remain fixed (set by Vert Freq), but the image content within those zones slides horizontally.

6. **Add dynamics**: Increase **Top Displace** to 90%. The displacement now varies within the band as the accumulator oscillates, creating a sweeping distortion within each Top zone. Reduce Top Displace to 20% for a subtle, uniform shift.

7. **Increase frequency**: Sweep **Vert Freq** from 30% to 80%. The bands become narrower and more numerous. At high frequencies, the alternating displacement creates a fine horizontal grating of shifted image slices.

:::tip
Vert Freq controls band count. Top/Bot Delay set static displacement. Top/Bot Displace set dynamic displacement amplitude. Only the Top parameter set is active in Top zones; only the Bottom set in Bottom zones.
:::

---

### Exercise 2: Mirror and Invert Zones

<img src={faultplane_exercise2_result} alt="Mirrored and inverted alternating zones creating a kaleidoscopic fracture pattern"/>

*Top Flip on, Bottom Invert on, Vert Freq at 40%, Horiz Freq at 25% — alternating mirrored and color-inverted zones create a kaleidoscopic fracture pattern.*

**Source**: Camera feed with strong directional features — diagonal lines, faces, or asymmetric compositions.

**Objective**: Explore how mirror and invert create visual discontinuities at zone boundaries.

1. **Set up zones**: Set **Vert Freq** to about 40% and **Horiz Freq** to about 25%. A grid of rectangular zones is visible.

2. **Enable Top Flip**: Flip Switch 7 (Top Flip) to On. Half the zones now display horizontally mirrored content. At zone boundaries, the image folds back on itself — features that point left in one zone point right in the adjacent zone.

3. **Enable Bottom Invert**: Flip Switch 10 (Bottom Invert) to On. The other half of the zones now display color-inverted content. The result is a checkerboard of mirrored-positive and normal-inverted zones.

4. **Combine mirror and invert**: Enable both **Top Flip** and **Top Invert** (Switches 7 and 9). Top zones are now both mirrored and inverted. The visual effect is striking — mirrored negative images alternate with normal-inverted images.

5. **Add displacement**: Set **Top Delay** to about 30% and **Bot Delay** to about 70%. The mirrored/inverted zones are also horizontally displaced from each other, creating fracture lines where the image content jumps discontinuously.

6. **Add blanking**: Lower **Line Blank** (Fader 12) to about 40%. Portions of the grid are now replaced with black, creating a stenciled effect where only some zones are visible.

:::tip
Top Flip and Bot Flip mirror writes to their respective RAMs. Top Invert and Bottom Invert negate data. Combining mirror, invert, and displacement creates complex visual fracture patterns.
:::

---

### Exercise 3: Checkerboard Grid with Blanking

<img src={faultplane_exercise3_result} alt="Fine checkerboard grid with selective blanking creating a stenciled pattern"/>

*Vert Freq 60%, Horiz Freq 50%, both displacements active, Line Blank at 50% — a fine gridded fracture with blanked regions creating a stenciled pattern.*

**Source**: Any footage, but geometric patterns and high-contrast material make the grid structure most visible.

**Objective**: Create a fine-grid fracture pattern with selective blanking to produce stencil and cutout effects.

1. **Set the grid**: Set **Vert Freq** to about 60% and **Horiz Freq** to about 50%. A fine grid of zones is visible.

2. **Differentiate the zones**: Set **Top Delay** to 20%, **Top Displace** to 60%, **Bot Delay** to 80%, **Bot Displace** to 40%. Each zone type now shows distinctly different displacement — Top zones shift one way, Bottom zones shift another.

3. **Add mirror and invert**: Enable **Top Flip** (Switch 7) and **Bottom Invert** (Switch 10). The grid now shows a complex mix of mirrored, inverted, and displaced content.

4. **Apply blanking**: Lower **Line Blank** (Fader 12) from 100% to about 50%. Regions where both accumulators are below the threshold snap to black. The blanking follows the zone grid, creating a periodic pattern of visible and blanked zones.

5. **Invert the blanking**: Flip Switch 11 (Blank Invert) to On. The visible and blanked regions swap — the previously black zones now show content and the previously visible zones go black.

6. **Sweep the threshold**: Slowly move the **Line Blank** fader up and down. Watch the balance between visible and blanked regions shift. The threshold determines how much of each accumulator's cycle falls below the cutoff.

7. **Animate**: With all controls set, slowly vary **Vert Freq** or **Horiz Freq**. The grid geometry shifts in real time, and the blanking pattern follows. Moving footage through this grid creates an evolving mosaic of fractured, mirrored, inverted, and blanked image fragments.

:::tip
The two accumulators define a rectangular grid. Mirror, invert, displacement, and blanking all operate within this grid. The Line Blank threshold carves out regions of the grid. Blank Invert swaps the carving logic.
:::

---

## Tips

- **Start simple**: Set Horiz Freq to 0% to work with horizontal bands only. Once you understand how Vert Freq, Delay, and Displace interact, add the horizontal dimension.

- **Displacement is relative**: Top Delay and Bot Delay set *absolute* offsets, but the visual effect depends on the *difference* between them. Equal delays in Top and Bottom zones produce no visible displacement at zone boundaries. Different delays create the characteristic fault-line fracture.

- **Mirror creates symmetry**: Top Flip and Bot Flip mirror the write addresses, creating reflection axes at zone boundaries. Enable one flip to create asymmetric mirror — half the zones reflect, half don't. Enable both for full bilateral symmetry within the zone grid.

- **Invert is per-channel**: Top Invert and Bottom Invert apply bitwise NOT to all 30 bits of YUV data simultaneously. This inverts both luminance (bright↔dark) and chrominance (complementary colors) in one operation.

- **Blanking tracks the grid**: The Line Blank threshold compares against both accumulators. Because the accumulators define the zone grid, the blanking pattern inherits the grid geometry. This makes it easy to create periodic stencil patterns that align with the zone structure.

- **Blank Invert for negative space**: Use Blank Invert to display the "negative space" of the blanking pattern. This is useful when you want to show the displaced content only in the regions that would normally be blanked.

- **Frequency ratio matters**: When Vert Freq and Horiz Freq are set to similar values, the XOR pattern creates roughly square zones. When they differ greatly, the zones become long rectangles — tall and narrow (high Horiz, low Vert) or short and wide (low Horiz, high Vert).

- **Feedback loops**: Routing Faultplane's output back to its input creates recursive spatial displacement. Each feedback pass re-displaces the already-displaced image, creating complex layered fracture patterns that evolve over time.
