---
draft: true
sidebar_position: 50
slug: /instruments/videomancer/cleave
title: "Cleave"
image: /img/instruments/videomancer/cleave/cleave_hero.png
---

import cleave_hero from '/img/instruments/videomancer/cleave/cleave_hero.png';
import cleave_before_after from '/img/instruments/videomancer/cleave/cleave_before_after.png';
import cleave_control_panel from '/img/instruments/videomancer/cleave/cleave_control_panel.png';
import cleave_exercise1_result from '/img/instruments/videomancer/cleave/cleave_exercise1_result.png';
import cleave_exercise2_result from '/img/instruments/videomancer/cleave/cleave_exercise2_result.png';
import cleave_exercise3_result from '/img/instruments/videomancer/cleave/cleave_exercise3_result.png';

# Cleave

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={cleave_hero} alt="Cleave hero image"/>
*Cleave splitting a live video feed at a PPU-jittered raster boundary, applying distinct brightness and hue rotation to each region with a visible glitch artifact bar at the seam.*
<img src={cleave_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Cleave applied.*

---

## Overview

The Nintendo Entertainment System's Picture Processing Unit had a peculiar timing trick: the PPU could detect the moment a special "sprite zero" pixel overlapped the background, and the CPU would spin in a tight polling loop waiting for that flag. When the hit was detected, the game could change scroll registers mid-frame, creating a raster split — the top of the screen shows one scene (a status bar, a title) while the bottom shows another (the scrolling game world). Cleave recreates this concept as a video processing effect.

Cleave divides each output frame into two (or three) horizontal regions at a configurable scanline boundary. Each region receives its own independent brightness scaling and hue rotation, allowing radically different color treatments above and below the split. An LFSR provides per-frame pseudo-random jitter on the split point, authentically replicating the imprecise timing of the NES CPU's polling loop — where DMA transfers, NMI handlers, or instruction alignment could delay detection by several scanlines - creating a wobbling, organic boundary.

At the split boundary itself, an optional glitch bar artifact injects a bright horizontal line — replicating the visible register-rewrite artifact familiar from games like Battletoads and Castlevania III, where the brief period of invalid register state produced a visible horizontal stripe. The double-split mode mirrors the boundary to create three regions (edge/center/edge), enabling symmetric color zoning. Combined with the wet/dry mix fader, Cleave can range from subtle split-toning to aggressive retro raster destruction.

---

## Background

### The NES PPU and Sprite Zero Hit

The NES PPU (2C02) rendered two independent layers: a scrolling background tilemap and up to 64 hardware sprites. Sprite zero — the first entry in the Object Attribute Memory — had a special property: the PPU set a flag in its status register ($2002, bit 6) on exactly the pixel clock cycle where sprite zero's first non-transparent pixel overlapped a non-transparent background pixel. Games placed sprite zero at a known vertical position and then spun in a `BIT $2002` / `BNE` loop, waiting for the flag. The moment the flag set, the CPU knew it was at that exact scanline and could safely rewrite the scroll registers for the lower portion of the screen.

### Raster Effects and Mid-Frame Register Changes

The sprite-zero technique is one example of a broader category called **raster effects** — tricks that change rendering parameters (scroll position, palette, bank-switching) at precise moments during the CRT's horizontal retrace. On the NES, the CPU and PPU shared a single clock domain but operated asynchronously: the CPU latency in detecting the sprite-zero flag varied by ±2–8 scanlines depending on instruction alignment, DMA timing, and whether an NMI interrupted the polling loop. This imprecision is the source of the characteristic "wobble" at raster split boundaries in NES games, which Cleave replicates with its LFSR jitter.

### Hue Rotation via Sine/Cosine Matrix

Hue rotation in video processing applies a 2×2 rotation matrix to the chrominance (U, V) pair while leaving luminance (Y) unchanged. The transformation is:

    U' = U·cos(θ) − V·sin(θ)
    V' = U·sin(θ) + V·cos(θ)

Cleave implements this using a quarter-wave sine lookup table (64 entries × 10-bit) stored in a single BRAM tile. The cosine is derived by shifting the phase by 90°. The 10-bit register maps linearly to 0–360° of rotation, so sweeping the hue knob smoothly cycles through the entire color wheel.

### Posterization as Bit Truncation

Digital posterization reduces the number of tonal levels by zeroing out the least significant bits of each pixel value. Cleave's posterization mode keeps only the top 4 bits of each 10-bit channel, reducing 1024 possible levels to 16 — producing the flat, poster-like color bands characteristic of early digital graphics hardware. The posterization is applied after brightness and hue processing, so it quantizes the already-transformed signal.

### Glitch Artifacts at Split Boundaries

In real NES hardware, the brief period between detecting sprite-zero hit and completing the scroll register writes left the PPU in a partially-updated state. During those few pixel clocks, the output could show corrupted or intermediate values — a bright or dark horizontal bar a few pixels tall. Cleave's glitch bar emulates this by additively boosting the Y channel on the exact scanline(s) of the split boundary, creating a visible horizontal artifact whose intensity is controlled by the Glitch knob.


---

## Signal Flow

```
Input Video (YUV 4:4:4 30-bit)
│
├── Timing ──────────────────────────────────────────────────────
│   └─ video_timing_generator → v_count, h_count
│
├── Split Detect ────────────────────────────────────────────────
│   ├─ registers_in(0) → base split position (0-1023)
│   ├─ lfsr16 → jitter offset (±8 lines, if enabled)
│   ├─ actual_split = base ± jitter
│   └─ double split → split_2 = 1023 − actual_split
│
├── Region Detect ───────────────────────────────────────────────
│   ├─ Single: upper (region 0: v < split) / lower (region 1)
│   ├─ Double: edge (0) / center (1: split ≤ v < split_2) / edge (0)
│   └─ on_split_line pulse (split boundary scanline)
│
├── Parameter Mux ───────────────────────────────────────────────
│   ├─ Region 0 → upper_brt, upper_hue, upper_post_en
│   └─ Region 1 → lower_brt, lower_hue, lower_post_en
│
├── Stage 1: Brightness & Hue ──────────────────────────────────
│   ├─ Y' = Y × sel_brt >> 9  (brightness scaling)
│   ├─ U_cen = U − 512,  V_cen = V − 512
│   ├─ U' = U_cen·cos(hue) − V_cen·sin(hue) + 512
│   ├─ V' = U_cen·sin(hue) + V_cen·cos(hue) + 512
│   └─ Posterize: keep top 4 bits if enabled
│
├── Stage 2: Glitch Bar ────────────────────────────────────────
│   └─ if on_split_line: Y' += glitch_intensity (clamped)
│
├── Sync Delay Pipeline (6 clocks) ─────────────────────────────
│   └─ Shift registers for hsync, vsync, field, Y, U, V
│
├── Wet/Dry Mix ─────────────────────────────────────────────────
│   └─ 3× interpolator_u: lerp(dry, wet, mix_amount)
│
└── Output (YUV 4:4:4 30-bit)
```

The pipeline is structured around a per-scanline region detection that drives a parameter multiplexer — at every pixel clock, the active brightness, hue, and posterization parameters are selected based on which region the current scanline falls in. This mux feeds a single shared processing path, avoiding the need for duplicate brightness/hue hardware. The glitch bar stage is the last processing step before the wet/dry mix, ensuring the artifact appears on top of the already-processed signal. The LFSR advances once per frame (on vsync), so the jitter offset is constant within a single frame but changes frame-to-frame, producing the characteristic per-frame wobble of NES raster splits.

---

## Parameter Reference

<img src={cleave_control_panel} alt="Videomancer front panel with Cleave loaded"/>
*Videomancer's front panel with Cleave active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Split Pos
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the vertical position of the raster split boundary. At 0% the split is at the very top of the frame (all pixels in the lower region); at 100% the split is at the bottom (all pixels in the upper region). At 50% the screen is divided evenly in half. The split position maps directly to scanline count (0–1023 of active video). When Jitter is enabled, the LFSR applies ±8 lines of random offset to this base position each frame, so the boundary wobbles organically like a real NES sprite-zero split.

---

#### Knob 2 — Upper Brt
| Property | Value |
|----------|-------|
| Range | 0.0% – 200.0% |
| Default | 100.1% |
| Suffix | % |

Sets the brightness gain for the upper region (region 0). The register value maps to a 0–200% brightness range — at 50% (register 512) the brightness is unity (no change). Below 50% the upper region darkens; above 50% it brightens, clamping at full white. This allows dramatic tonal contrast between upper and lower regions, simulating the look of NES games where the status bar and game world had different brightness characteristics.

---

#### Knob 3 — Upper Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Controls hue rotation for the upper region. The full 10-bit register range maps to 0–360° of rotation through the color wheel. At 0° (default), chrominance passes unmodified. At 180° all colors invert (red becomes cyan, blue becomes orange). At intermediate angles, colors shift smoothly around the color wheel. The rotation is implemented as a 2×2 matrix multiply using sine/cosine values from the quarter-wave LUT, operating on the centered U/V pair before re-adding the 512 offset.

---

#### Knob 4 — Lower Brt
| Property | Value |
|----------|-------|
| Range | 0.0% – 200.0% |
| Default | 100.1% |
| Suffix | % |

Sets the brightness gain for the lower region (region 1), with the same 0–200% range as Upper Brt. In double-split mode, this controls the center region brightness. Setting Upper Brt to one extreme and Lower Brt to the other creates a stark tonal boundary at the split — a bright sky over a dark ground, or a dark header over a bright body.

---

#### Knob 5 — Lower Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Controls hue rotation for the lower region, identical in range and behavior to Upper Hue. In combination with Upper Hue, you can create complementary color splits (e.g., 0° upper / 180° lower for a complementary toning effect), analogous color harmonies (30° offset), or triadic schemes (120° offset) across the raster boundary.

---

#### Knob 6 — Glitch
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the intensity of the glitch artifact bar that appears at the split boundary scanline(s). At 0% no artifact is visible. As the control increases, a progressively brighter horizontal bar appears at the split point — the Y channel is additively boosted, clamped at full white. At maximum, the split boundary becomes a blindingly bright stripe. In double-split mode, a glitch bar appears at both the upper and lower split boundaries.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Jitter** | Off | On |
| **8 — Up Post** | Off | On |
| **9 — Low Post** | Off | On |
| **10 — Dbl Split** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control independent binary features: per-frame raster jitter (replicating NES timing wobble), per-region posterization (upper and lower independently), the double-split mirror mode, and a global bypass. The posterization toggles are independently switchable so you can posterize only the upper region, only the lower region, both, or neither — enabling asymmetric digital/analog texture combinations across the split boundary.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade between the processed and original signal. At 0% the output is fully dry (unprocessed input). At 100% the output is fully wet (processed). Intermediate values blend the two using three independent interpolator_u instances (one per Y, U, V channel). This allows subtle integration of the raster split effect into a mix chain — a partially-mixed split is less jarring and more suitable for layered compositions.

---

## Guided Exercises

These exercises explore Cleave's raster-split processing from basic split-toning through retro NES artifacts to expressive three-zone color composition. Each exercise uses a different combination of controls to reveal different aspects of the processing chain.

### Exercise 1: Retro Status Bar Split

<img src={cleave_exercise1_result} alt="Retro Status Bar Split result"/>
*Retro Status Bar Split — simulated result across source images.*
**Source**: A live camera feed or recorded footage of a scene with clear vertical structure (sky and ground, ceiling and floor).

**Objective**: Create a classic NES-style raster split with a bright status bar region and a darker game world region, complete with jitter wobble.

1. **Set the split position**: Turn Split Pos to about 25%, placing the boundary near the top quarter of the frame.
2. **Brighten the upper region**: Set Upper Brt to about 75%, creating a brighter top strip.
3. **Darken the lower region**: Set Lower Brt to about 35%, dimming the lower three-quarters.
4. **Add jitter**: Enable the Jitter toggle. Watch the split boundary wobble by a few scanlines each frame — this is the authentic NES polling-loop timing drift.
5. **Add the glitch bar**: Turn Glitch to about 30%. A bright horizontal stripe appears at the split, replicating the register-rewrite artifact.
6. **Tune the mix**: Set Mix to 100% to see the full effect.

**Key concepts**: Split position maps directly to scanline count, LFSR jitter replicates NES timing imprecision, glitch bar is an additive brightness artifact at the boundary

---

### Exercise 2: Complementary Color Split

<img src={cleave_exercise2_result} alt="Complementary Color Split result"/>
*Complementary Color Split — simulated result across source images.*
**Source**: Footage with rich color content — flowers, graffiti, or colorful fabrics.

**Objective**: Apply complementary hue rotations to the upper and lower halves of the frame, creating a split-tone color grading effect.

1. **Center the split**: Set Split Pos to 50% for an even division.
2. **Unity brightness**: Set both Upper Brt and Lower Brt to 50% (unity gain).
3. **Rotate upper hue**: Turn Upper Hue to about 120° (shift toward the green/cyan range).
4. **Rotate lower hue**: Turn Lower Hue to about 300° (shift toward magenta/pink — roughly complementary).
5. **Posterize the lower**: Enable Low Post to give the lower half a flat, graphic quality while the upper remains smooth.
6. **Disable jitter**: Keep Jitter off for a clean, stable boundary.
7. **Compare**: Toggle Bypass to see the original versus the split-toned version.

**Key concepts**: Hue rotation applies a 2×2 matrix to the UV pair, complementary hues are 180° apart on the color wheel, posterization can be applied asymmetrically across the split

---

### Exercise 3: Three-Zone Vignette

<img src={cleave_exercise3_result} alt="Three-Zone Vignette result"/>
*Three-Zone Vignette — simulated result across source images.*
**Source**: Any footage — talking head, landscape, or abstract pattern.

**Objective**: Use double-split mode to create a three-zone symmetric color composition with posterized edges and a clean center.

1. **Enable double split**: Turn on the Dbl Split toggle.
2. **Position the split**: Set Split Pos to about 30%. The upper split will be at ~30%, the mirrored lower split at ~70%, creating a center region occupying roughly the middle 40% of the frame.
3. **Edge treatment**: Set Upper Brt to about 25% (darken edges) and Upper Hue to about 60° (warm shift). Enable Up Post for bit-crushed edges.
4. **Center treatment**: Set Lower Brt to about 65% (bright center) and Lower Hue to 0° (neutral).
5. **Glitch bars**: Turn Glitch to about 50% for prominent boundary artifacts at both split lines.
6. **Add jitter**: Enable Jitter for organic boundary wobble.
7. **Blend**: Set Mix to about 75% to let some of the original signal through.

**Key concepts**: Double split mirrors the boundary for symmetric three-zone composition, edge and center regions have independent parameter sets, glitch bars appear at both boundaries

---


## Tips

- **Split position is direct scanline mapping**: The 10-bit register maps to 0–1023 scanlines. On 1080p content, values above ~1080 are equivalent to placing the split below the visible frame.
- **Jitter authenticity**: The LFSR-driven wobble is frame-coherent (constant within a frame) but changes every frame — exactly matching the per-frame timing variation of NES sprite-zero polling. Disable jitter for clean, stable split-toning work.
- **Double split for symmetric framing**: Double-split mode creates a center window flanked by identically-processed edges — useful for vignette-like tonal framing or centering a subject in a clean color zone surrounded by processed borders.
- **Posterization is channel-wide**: The 4-bit truncation applies equally to Y, U, and V, so both brightness and chrominance are quantized. This matches the NES PPU's limited color depth.
- **Glitch bar scales with intensity**: At low Glitch values, the bar is a subtle horizontal shimmer. At maximum, it saturates to full white — useful as a deliberate compositional element or horizontal rule.
- **Mix for subtlety**: Rather than committing fully to the split effect, use the Mix fader at 30–50% to blend the split-toned version with the original. This creates a more photographic split-grading look.
- **Hue knobs are independent color wheels**: Upper Hue and Lower Hue can be set to any angle independently. Try analogous harmonies (30° apart), complementary (180° apart), or triadic (120° apart) for different color relationships across the split.
- **Feedback routing**: Sending the output back to the input creates recursive split processing — each pass applies the split again, building up layered tonal bands and accumulating hue rotation.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; dedicated memory resources within the FPGA fabric, used here for the quarter-wave sine lookup table. |
| **Chroma** | The color information in a video signal, encoded as U and V components offset around 512 in the 10-bit domain. |
| **Glitch Bar** | A bright horizontal artifact at the raster split boundary, replicating the register-rewrite artifact from NES hardware. |
| **Hue Rotation** | A 2×2 matrix transformation applied to the U/V chrominance pair, rotating colors around the color wheel by a specified angle. |
| **Interpolator** | A pipelined hardware module that computes linear interpolation between two values, used for the wet/dry mix. |
| **LFSR** | Linear Feedback Shift Register; a pseudo-random number generator that produces a deterministic but seemingly random sequence of bits, used for split-line jitter. |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **NES** | Nintendo Entertainment System; the 8-bit console whose PPU inspired the raster-split concept. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next on each clock cycle; Cleave uses a 6-clock pipeline. |
| **Posterization** | Reducing the number of distinct tonal levels by truncating least significant bits, producing flat color bands. |
| **PPU** | Picture Processing Unit; the NES's dedicated video rendering chip (Ricoh 2C02). |
| **Quarter-Wave LUT** | A lookup table storing only 0°–90° of the sine function; the remaining quadrants are derived by symmetry, saving 75% of storage. |
| **Raster Split** | A mid-frame change of rendering parameters at a specific scanline, dividing the display into independently-controlled horizontal regions. |
| **Sprite Zero Hit** | A hardware flag in the NES PPU that signals when sprite zero's opaque pixel overlaps an opaque background pixel, used for scanline-precise split detection. |
| **YUV** | A color encoding separating luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |


---
