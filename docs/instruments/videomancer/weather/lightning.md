---
draft: true
sidebar_position: 148
slug: /instruments/videomancer/lightning
title: "Lightning"
image: /img/instruments/videomancer/lightning/lightning_hero.png
---

import lightning_before_after from '/img/instruments/videomancer/lightning/lightning_before_after.png';
import lightning_control_panel from '/img/instruments/videomancer/lightning/lightning_control_panel.png';
import lightning_exercise1_result from '/img/instruments/videomancer/lightning/lightning_exercise1_result.png';
import lightning_exercise2_result from '/img/instruments/videomancer/lightning/lightning_exercise2_result.png';
import lightning_exercise3_result from '/img/instruments/videomancer/lightning/lightning_exercise3_result.png';
import lightning_hero from '/img/instruments/videomancer/lightning/lightning_hero.png';
import lightning_source1_kodim01 from '/img/instruments/videomancer/lightning/lightning_source1_kodim01.png';
import lightning_source2_kodim02 from '/img/instruments/videomancer/lightning/lightning_source2_kodim02.png';
import lightning_source3_stream_bridge_512 from '/img/instruments/videomancer/lightning/lightning_source3_stream_bridge_512.png';

# Lightning

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={lightning_hero} alt="Lightning hero image"/>
*Lightning bolt effect overlaid on video, jagged LFSR-driven discharge paths cutting down the screen with distance-based brightness falloff and periodic flash modulation.*
<img src={lightning_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Lightning applied.*

---

## Overview

Lightning is a processing program that renders one or two bright, jagged bolt paths from the top to the bottom of the frame, overlaid additively onto the input video. Each bolt follows a vertical path whose horizontal position wanders randomly from scanline to scanline, driven by a 16-bit LFSR. The bolt's visual intensity falls off with horizontal distance from its centre, creating a glowing discharge effect. A branch fork splits from the primary bolt partway down the screen, diverging with doubled jitter to simulate the forking structure of real lightning.

The entire bolt assembly "flashes" periodically, controlled by a DDS (Direct Digital Synthesis) phase accumulator that increments once per frame. When the upper bits of the accumulator reach a threshold, the bolt fires at full brightness; between flashes, it dims to one quarter intensity. This creates a rhythmic strobe-like discharge pattern. A random flash mode adds LFSR noise to the DDS increment, producing irregular timing that more closely resembles natural electrical discharge.

At minimum settings, Lightning produces a thin, barely visible line with subtle jitter. At maximum, it creates a wide, bright, violently jagged bolt that floods the screen with light during flash peaks. A colour tint toggle shifts the bolt from pure white to a purple-blue cast, and double bolt mode adds a mirrored second bolt that wanders with inverted jitter.

---

## Background

### What Is a Bolt Distance Falloff?

The lightning effect is built on a simple principle: each pixel's brightness contribution from the bolt is determined by its horizontal distance from the bolt's position on that scanline. The VHDL computes the absolute difference $|h\_count - bolt\_x|$ and subtracts a scaled version of this distance from the peak brightness. Pixels at the bolt centre (distance 0–1) receive full brightness. Pixels further away receive progressively less, until the brightness drops to zero at the bolt width limit. This creates the characteristic glow that widens as you increase the Width control.

### LFSR Jitter Accumulation

Instead of computing a bolt path mathematically, Lightning builds it incrementally. At each horizontal sync pulse (start of a new scanline), the VHDL adds a small signed random offset from the LFSR to a running x-position accumulator. The Jitter control selects how many of the LFSR's 8 bits are used by applying a right-shift — more shift means smaller jitter, producing a straighter bolt. Less shift (higher jitter) produces violent horizontal wandering. The accumulator is clamped to the screen width (0–1919) to prevent the bolt from disappearing off-screen.

### DDS Flash Timing

A 16-bit DDS phase accumulator increments by a scaled version of the Flash Rate control on every vertical sync. The flash fires when the upper 3 bits of the accumulator are all ones (reaching the top 1/8 of the phase cycle). Larger increments advance the phase faster, producing more frequent flashes. Smaller increments slow the accumulation, spacing flashes further apart. The random flash mode adds LFSR noise to the increment value, making the flash timing irregular and unpredictable — closer to natural lightning, which discharges at pseudo-random intervals.

### Branch Forking

Below a certain scanline (set by the Branch control), a secondary bolt path forks from the primary bolt's position. The branch drifts with doubled jitter — twice the horizontal wandering per scanline — causing it to diverge rapidly from the main bolt. This creates the characteristic Y-shaped or tree-like structure of real lightning discharge. The branch start position varies with the Branch Density parameter, placing the fork higher or lower on screen.

### Additive Compositing

Lightning uses additive compositing: the bolt brightness is *added* to the source video luma, then clamped at 1023 (maximum white). This means the bolt always brightens the image — it never darkens or replaces the source. Dark areas of the input receive the most visible bolt; bright areas may clip to white. The colour tint mode shifts the bolt's chroma away from neutral white toward purple-blue by increasing U and V above the 512 midpoint proportionally to the bolt brightness.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Video Timing Generator ──────────────────────────────────
│   └── h_count, v_count (pixel/line counters)
│
├── LFSR(16) ────────────────────────────────────────────────
│   └── Jitter source (per scanline) + flash noise
│
├── DDS Phase Accumulator (vsync-driven) ────────────────────
│   └── s_dds_phase → s_is_flash (1 when upper 3 bits = 111)
│
├── Bolt Position Accumulator (hsync-driven) ────────────────
│   ├── Primary bolt:  x += LFSR(7:0) >> jitter_shift
│   ├── Secondary bolt: x -= jitter (opposite direction)
│   └── Branch:        x += 2× jitter (from fork point)
│
├── Stage 1: Input Register + Distance ──────────────────────
│   ├── dist1 = |h_count - bolt_x_primary|
│   ├── dist2 = |h_count - bolt_x_secondary|  (if double)
│   └── dist_branch = |h_count - branch_x|    (if active)
│
├── Stage 2: Distance Falloff ───────────────────────────────
│   ├── min_dx = min(dist1, dist2, dist_branch)
│   └── bolt_bright = bright_scale - (min_dx << 3)  [clamped]
│
├── Stage 3: Flash Modulation ───────────────────────────────
│   └── flash_bright = bolt_bright (flash) or bolt_bright>>2 (dim)
│
├── Stage 4: Brightness Add + Colour Tint + Compose ─────────
│   ├── Y: source_y + flash_bright  [clamped 0..1023]
│   ├── U: +flash_bright>>2 toward blue  (if tint on)
│   └── V: +flash_bright>>3 toward blue  (if tint on)
│
├── Interpolator (4 clks): wet/dry mix ──────────────────────
│   └── lerp(source_delayed, composed, mix_amount)
│
└── Output (bypass mux) ─────────────────────────────────────
```

The key architectural feature is that the bolt path is built *incrementally* via a per-scanline accumulator, not computed as a closed-form function. This means the bolt shape is history-dependent — each scanline's position depends on all preceding scanlines' accumulated jitter. The branch fork is particularly interesting: it captures the primary bolt's x-position at the fork point and then diverges with doubled jitter, creating a naturally splitting path. The flash modulation operates frame-by-frame via the DDS, which is independent of the per-pixel pipeline — it gates the overall bolt brightness as a temporal envelope.

---

## Parameter Reference

<img src={lightning_control_panel} alt="Videomancer front panel with Lightning loaded"/>
*Videomancer's front panel with Lightning active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Bolt W
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the bolt glow width — the horizontal distance over which the bolt brightness falls off to zero. The VHDL maps this as $4 + \text{pot}>>3$, giving a range from 4 to roughly 131 pixels. At minimum, the bolt is a thin, precise line. At maximum, it produces a wide, diffused glow that can span a significant portion of the screen. The falloff within the width is approximately linear: brightness decreases by 8 units per pixel of distance, so wider bolts have gentler gradients.

---

#### Knob 2 — Branch P
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Despite its TOML label "Branch P" (suggesting branch probability), this register actually controls the horizontal jitter amplitude. The VHDL signal `s_jitter_amt` maps to a right-shift selector (0–7) applied to the 8-bit signed LFSR output. At maximum pot value, shift is 0 — full ±127 pixel jitter per scanline, producing an extremely jagged, wildly wandering bolt. At minimum, shift is 7 — jitter of ±1 pixel per scanline, producing a nearly straight vertical line. The jitter accumulates over hundreds of scanlines, so even a small per-line offset creates visible wandering over the full frame height.

---

#### Knob 3 — Bright
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Despite its TOML label "Bright" (suggesting brightness), this register controls the flash rate — the DDS phase accumulator increment per frame. The VHDL signal `s_flash_rate` is shifted left by 5 and added to the 16-bit phase accumulator at each vsync. Higher values produce faster accumulation and more frequent flashes. At maximum, flashes occur nearly every frame. At minimum, the accumulator crawls and flashes are separated by many seconds. The DDS architecture means the flash frequency is precisely controllable and repeatable.

---

#### Knob 4 — Flash Frq
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Despite its TOML label "Flash Frq" (suggesting flash frequency), this register controls the branch fork density. The VHDL signal `s_branch_density` determines where the branch fork begins on screen: $100 + \text{pot}>>1$ scanlines from the top, placing the branch start between lines 100 and 611. Higher values push the fork further down the screen, giving the branch less vertical distance to diverge. The branch threshold also influences the branch's visual density — a branch that starts earlier has more scanlines to accumulate jitter, creating more dramatic forking.

---

#### Knob 5 — Jitter
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Despite its TOML label "Jitter," this register controls the bolt's peak brightness. The VHDL signal `s_bright` directly sets the maximum brightness value at the bolt's centre (distance = 0). Higher values produce a more intense bolt; lower values produce a subtle, dim discharge. This interacts with the flash modulation — during flash, the full brightness is used; between flashes, the brightness is shifted right by 2 (divided by 4). A dim bolt with frequent flashes can produce a pleasant flickering effect.

---

#### Knob 6 — Tint
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

This register is mapped to `registers_in(5)` in the TOML as "Tint," but the VHDL does not connect it to any signal. The register is not read, and the value has no effect on the output. The colour tint is controlled by Toggle 8 (a binary on/off), not by this continuous control.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Style** | Bolt | Sheet |
| **8 — Color** | White | Blue |
| **9 — Flash** | Off | On |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

Toggles 7 and 8 each use only the lowest bit of their respective 10-bit registers, despite the TOML defining four value labels for each. The VHDL uses `registers_in(6)(0)` and `registers_in(6)(1)` as single-bit selectors. Toggle 9 controls the flash pattern (regular vs random). Toggle 10 ("Animate") is completely unused in the VHDL; the register bit is not connected to any logic.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Master wet/dry crossfade. At 0%, the output is the original source video with no bolt overlay. At 100%, the output is the fully composed lightning effect over the source. Intermediate values blend between the two, allowing the bolt to be mixed in at any intensity. The interpolation is linear across all three YUV channels simultaneously.

---

## Guided Exercises

These exercises progress from a simple static bolt to complex multi-bolt flashing lightning effects, building familiarity with jitter, branching, flash timing, and colour tinting.

### Exercise 1: Simple Bolt

<img src={lightning_exercise1_result} alt="Simple Bolt result"/>
*Simple Bolt — simulated result across source images.*
**Source**: A dark background — either black or low-contrast footage.

**Objective**: Understand basic bolt rendering, width control, and jitter.

1. Set Width (Knob 1) to ~50% for a clearly visible glow band.
2. Set Jitter (Knob 2 — labelled "Branch P") to ~30% for moderate wandering.
3. Set Brightness (Knob 5 — labelled "Jitter") to ~70% for a bright bolt.
4. Disable flash: set Flash Rate (Knob 3 — labelled "Bright") to 0% and Flash toggle (Switch 9) to Off.
5. Observe the bolt: a single jagged vertical line of light wandering down the screen.
6. Sweep Width from minimum to maximum — watch the glow band widen.
7. Sweep Jitter from minimum to maximum — watch the bolt path go from nearly straight to violently jagged.

**Key concepts**: Distance falloff creates the glow width, LFSR jitter accumulates per scanline, brightness sets the peak intensity

---

### Exercise 2: Flash and Fork

<img src={lightning_exercise2_result} alt="Flash and Fork result"/>
*Flash and Fork — simulated result across source images.*
**Source**: Mid-brightness footage — cityscapes, landscapes, or abstract video.

**Objective**: Explore flash timing, branching, and the difference between regular and random flash.

1. Set Width to ~40%, Jitter to ~50%, Brightness to ~80%.
2. Set Flash Rate (Knob 3 — labelled "Bright") to ~50%. Observe periodic flashing.
3. Toggle Flash mode (Switch 9) between regular and random. Notice how the timing becomes unpredictable in random mode.
4. Set Branch Density (Knob 4 — labelled "Flash Frq") to ~40%. The fork appears partway down the screen.
5. Move Branch Density from minimum to maximum — watch the fork point slide from near the top to near the bottom.
6. With the branch active, increase Jitter — the branch diverges dramatically because it uses doubled jitter.

**Key concepts**: DDS accumulator creates periodic flash, LFSR noise irregularises timing, branch forks from primary bolt and diverges with 2× jitter

---

### Exercise 3: Electric Storm

<img src={lightning_exercise3_result} alt="Electric Storm result"/>
*Electric Storm — simulated result across source images.*
**Source**: Any footage — the effect will be dramatic regardless of source content.

**Objective**: Combine double bolts, colour tint, heavy jitter, and random flash for a full storm effect.

1. Enable double bolt (Switch 7 on). Two bolts appear, wandering in opposite directions.
2. Enable colour tint (Switch 8 on). Bolts shift from white to purple-blue.
3. Set Width to ~70%, Jitter to ~80%, Brightness to ~90%.
4. Set Flash Rate to ~60% with random flash (Switch 9 on). Bolts flash irregularly.
5. Set Branch Density to ~30% so branches fork early and diverge dramatically.
6. Reduce Mix to ~70% to let some of the source video show through the storm.
7. Observe how the double bolts, their branches, and the colour tint combine to fill the screen with forking electrical discharge.

**Key concepts**: Double bolt mirrors jitter for symmetric divergence, additive compositing means bolts always brighten, colour tint adds chroma shift proportional to brightness

---


## Tips

- **Labels are scrambled**: The TOML labels for Knobs 2–5 do not match the VHDL signal assignments. Use the hardware behaviour (described above) rather than the panel labels when adjusting controls.
- **Dark sources work best**: Lightning uses additive compositing, so the bolt is most visible against dark backgrounds. Against bright sources, the bolt may clip to white and lose definition.
- **Jitter accumulates**: Even small per-scanline jitter produces significant wandering over 1080 lines. Start with low Jitter values to understand the accumulation before going extreme.
- **Flash Rate is tempo**: Think of the Flash Rate control as a tempo knob — it sets the rhythm of the lightning flashes. Random flash mode adds syncopation.
- **Branch = 2× jitter**: The branch forks from the main bolt with doubled jitter amplitude, so it diverges rapidly. Use low Branch Density values (fork near top) for maximum branching drama.
- **Colour tint is brightness-proportional**: The purple-blue shift only appears where the bolt is bright. Dim inter-flash areas retain their source colour, creating a natural colour gradient along the bolt's falloff.
- **Mix for subtlety**: At full mix, the bolt overlay is dramatic. Reduce Mix to 40–60% for a more atmospheric, background-lightning effect.
- **Unused controls**: Knob 6 ("Tint") and Switch 10 ("Animate") have no effect in the current VHDL implementation.

---

## Glossary

| Term | Definition |
|------|------------|
| **Additive Compositing** | Combining two signals by adding their values, clamping at the maximum. The bolt brightness is added to the source luma. |
| **BRAM** | Block RAM; dedicated FPGA memory resources. Lightning uses zero BRAM. |
| **DDS** | Direct Digital Synthesis; a technique using a phase accumulator to generate periodic signals at arbitrary frequencies. |
| **Distance Falloff** | The decrease in brightness with increasing distance from the bolt centre, creating a glow effect. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit executing the video processing pipeline. |
| **LFSR** | Linear Feedback Shift Register; produces pseudo-random bit sequences used for bolt jitter and flash randomisation. |
| **Luma** | The brightness component (Y) of a YUV video signal. |
| **Manhattan Distance** | The sum of absolute coordinate differences, $|x_1-x_2|+|y_1-y_2|$. |
| **Phase Accumulator** | A register that increments by a fixed amount each clock cycle, wrapping at its maximum value, used in DDS to control frequency. |
| **Pipeline** | A series of sequential processing stages, each operating in one clock cycle. |
| **YUV** | A colour encoding separating luminance (Y) from chrominance (U, V), used throughout the Videomancer pipeline. |
