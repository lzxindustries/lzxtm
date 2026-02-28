---
draft: true
sidebar_position: 121
slug: /instruments/videomancer/hologram
title: "Hologram"
image: /img/instruments/videomancer/hologram/hologram_hero.png
description: "Program guide for Hologram, a Videomancer optics program for the LZX video synthesizer."
---

import hologram_hero from '/img/instruments/videomancer/hologram/hologram_hero.png';
import hologram_before_after from '/img/instruments/videomancer/hologram/hologram_before_after.png';
import hologram_control_panel from '/img/instruments/videomancer/hologram/hologram_control_panel.png';
import hologram_exercise1_result from '/img/instruments/videomancer/hologram/hologram_exercise1_result.png';
import hologram_exercise2_result from '/img/instruments/videomancer/hologram/hologram_exercise2_result.png';
import hologram_exercise3_result from '/img/instruments/videomancer/hologram/hologram_exercise3_result.png';

# Hologram

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={hologram_hero} alt="Hologram hero image"/>
*Hologram applying rainbow holographic bands to a video source, with hue-shifting stripes tracing a diamond path through UV color space.*
<img src={hologram_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Hologram applied.*

---

## Overview

Hologram overlays rainbow-colored bands onto a video signal, simulating the iridescent shimmer of holographic foil. Horizontal or vertical stripes cycle through hues as a function of scan-line position, creating the appearance of a transmission diffraction grating printed over the image. The hue rotation is not a true circular path through UV color space — instead, the VHDL uses a **diamond approximation**, where the U and V values follow linear ramps through four quadrants, tracing a square-ish path that produces four distinct color transitions per cycle.

The name *Hologram* evokes the rainbow reflections seen on holographic security stickers and credit card holograms. These real-world effects arise from microscopic diffraction gratings that split white light into its spectral components at angles determined by the grating pitch. The program approximates this visually by computing a phase value from the scan position — shifted by a spacing parameter, offset by a static hue control, and optionally animated by a per-frame accumulator — then mapping that phase into UV color deltas via quadrant-based sign flipping.

At subtle settings — narrow spread, moderate brightness — Hologram adds a gentle pastel tint that shifts gradually across the frame. At extreme settings — maximum spread, full brightness modulation — the image is dominated by saturated rainbow bands that completely override the source chrominance. The additive/replace toggle determines whether the rainbow colors blend with the existing video chrominance or override it entirely.

---

## Background

### What Is Holographic Diffraction?

A **hologram** in the optical sense is an interference pattern recorded on a photosensitive medium. When illuminated, it reconstructs a wavefront that produces a three-dimensional image. The rainbow reflections commonly associated with holograms — on credit cards, security stickers, and novelty items — are actually produced by **diffraction gratings**: periodic microscopic structures that split white light into spectral components. The angle of each color component depends on the grating pitch and the wavelength, producing the characteristic rainbow sweep as the viewing angle changes. Hologram simulates this spectral sweep digitally, mapping scan-line position to hue angle.

### Diamond Approximation of UV Rotation

True hue rotation in YUV color space requires computing sine and cosine functions to trace a circle in the UV plane. On a resource-constrained FPGA without dedicated DSP multipliers, this is expensive. Hologram uses a **diamond approximation** — a piecewise-linear path through four quadrants that traces a diamond (rotated square) shape in UV space instead of a circle. The phase is split into a 2-bit quadrant selector and an 8-bit linear ramp. In each quadrant, U and V are assigned simple ascending or descending ramps with appropriate sign flips. The result is visually convincing: four smooth color transitions per full revolution, with slightly sharper transitions at the quadrant boundaries than a true sinusoidal rotation would produce.

### Phase Computation and Animation

The rainbow effect's spatial frequency and position are controlled by a **phase accumulator**. The scan-line position (vertical for horizontal bands, horizontal for vertical bands) is right-shifted by a spacing parameter to control band width, then added to a static hue offset and an optional per-frame animation accumulator. The animation accumulator advances once per video frame by the scan speed register value, creating a scrolling rainbow effect. The 16-bit phase value wraps naturally, producing seamless cycling.

### Additive vs Replace Color Modes

The program offers two modes for applying the computed UV deltas to the source video. In **additive** mode, the rainbow UV deltas are added to the existing chrominance of the input signal — the source colors are tinted by the holographic pattern. In **replace** mode, the source chrominance is discarded and replaced with the rainbow pattern centered on neutral (U=512, V=512) — creating pure spectral bands regardless of the original color content. Replace mode produces more vivid, saturated rainbow effects; additive mode preserves more of the source's color identity.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y Channel ──────────────────────────────────────────────────
│   │
│   ├─ 1. Input Register         (latch Y from data_in)
│   ├─ 2. Pass-through           (Y delayed 1 stage)
│   └─ 3. Brightness Adjust      (Y ± luma modulation from U delta, attenuated by Bright)
│
├── U/V Channels ───────────────────────────────────────────────
│   │
│   ├─ 1. Input Register         (latch U, V from data_in)
│   ├─ 2. Quadrant UV Delta      (phase → quadrant + ramp → U/V deltas, spread-attenuated)
│   └─ 3. Compose                (additive: source + delta; replace: 512 + delta; clamp 0-1023)
│
├── Phase Engine ───────────────────────────────────────────────
│   │
│   ├─ Position Select           (v_count for H-bands, h_count for V-bands)
│   ├─ Spacing Shift             (right-shift 0-4 for wider bands)
│   ├─ Hue Offset Add            (static phase rotation)
│   └─ Animation Accum           (per-frame phase increment when Animate on)
│
├── Interpolator Stage ─────────────────────────────────────────
│   └─ 4–7. Wet/dry mix          (3× interpolator_u, 4 clocks)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ 8-clock delay pipeline (hsync, vsync, field)
│
└── Output ─────────────────────────────────────────────────────
    └─ Mix result (no VHDL bypass — Pot 6 at 0% = full dry)
```

Two important discrepancies between the TOML and VHDL: First, the VHDL maps `registers_in(5)` (TOML Pot 6 "Diffract") as the mix amount for the interpolator — making Pot 6 the effective wet/dry crossfade rather than a "diffraction" control. Second, only three toggle bits are read from `registers_in(6)` — bits 0 (H/V mode), 1 (additive/replace), and 2 (animate). TOML toggles 10 (Animate), 11 (Bypass), and Fader 12 (Mix) have no corresponding register reads in the VHDL. The brightness modulation in stage 3 is derived from the U delta value (not an independent luma pattern), creating a coupling between the rainbow hue and the luminance shimmer — brighter shimmer at quadrant transitions where the U ramp changes fastest.

---

## Parameter Reference

<img src={hologram_control_panel} alt="Videomancer front panel with Hologram loaded"/>
*Videomancer's front panel with Hologram active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Line Sp
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the width of the rainbow bands by right-shifting the scan position counter before phase computation. The 10-bit register is mapped to five discrete shift values (0 through 4). At shift 0 (low pot), each scan line gets a different phase — producing very narrow, tightly packed rainbow stripes. At shift 4 (high pot), 16 adjacent scan lines share the same phase — producing wide, slowly varying color bands. The effect is analogous to changing the pitch of a diffraction grating: finer pitch produces more closely spaced spectral lines.

---

#### Knob 2 — Spread
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the magnitude of the UV color deviation. The 10-bit register is mapped to four discrete attenuation levels via right-shift (3, 2, 1, or 0). At minimum (shift 3), the UV deltas are divided by 8, producing very subtle pastel tinting. At maximum (shift 0), the full ±255 ramp values are applied, producing deeply saturated rainbow bands. This control determines how vivid or subdued the holographic coloring appears.

---

#### Knob 3 — Hue Off
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Adds a static phase offset to the rainbow pattern. The register value is left-shifted by 6 bits and added to the position-derived phase, effectively rotating the entire rainbow through hue space. Sweeping this knob smoothly scrolls the color bands through their full cycle — all four quadrants of the diamond UV path — without changing the spatial frequency. At 512 (default), the offset positions the rainbow at a neutral starting phase.

---

#### Knob 4 — Bright
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the depth of the luminance modulation that accompanies the rainbow chrominance effect. The 10-bit register is mapped to four discrete attenuation levels (shift 3–0). The luma modulation is derived from the U delta signal — the same value used for chrominance. At minimum attenuation (high pot), the brightness varies significantly with the rainbow band position, creating a visible shimmer. At maximum attenuation (low pot), the luma remains close to the source, and only color changes.

---

#### Knob 5 — Scan Dir
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

In the TOML this is labeled "Scan Dir," suggesting a scan direction control. In the VHDL, `registers_in(4)` is mapped to `s_scan_speed` — the per-frame increment added to the animation phase accumulator when the Animate toggle is active. At zero, the rainbow is static (even with Animate on). At maximum, the rainbow scrolls rapidly across the frame. The control has no effect when Animate is off. Contrary to the TOML label, this does not control scan direction — it controls animation speed.

---

#### Knob 6 — Diffract
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Labeled "Diffract" in the TOML, but in the VHDL this register (`registers_in(5)`) is mapped to `s_mix_amount` — the interpolation parameter for the wet/dry crossfade. At minimum, the output is entirely the delayed original signal (dry). At maximum, the output is entirely the rainbow-processed signal (wet). This is the effective mix/blend control for the Hologram effect. Because the VHDL has no separate bypass path, this control at 0% functions as a de facto bypass.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Type** | Rainbow | Silver |
| **8 — Lines** | Horiz | Vert |
| **9 — Motion** | Off | Scan |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

Only three of the five toggle bits are read from `registers_in(6)` in the VHDL. Bit 0 selects between horizontal and vertical band orientation. Bit 1 selects between additive and replace chrominance modes. Bit 2 enables or disables animation. Bits 3 and 4 (TOML toggles 10 and 11) are not mapped — `registers_in(6)(3)` and `registers_in(6)(4)` are never assigned to any signal. Similarly, `registers_in(7)` (TOML Fader 12 "Mix") is not read. The TOML's multi-value labels for toggles 7 and 8 (four options each) are also aspirational — the VHDL reads single bits, producing only two states per toggle.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Labeled "Mix" in the TOML, but `registers_in(7)` is not read by the VHDL. This fader has no effect on the output. The actual wet/dry mix is controlled by Pot 6 (mapped to `s_mix_amount` in the VHDL). Adjusting this fader produces no visible change.

---

## Guided Exercises

These exercises explore the rainbow holographic effect from simple band generation through animation and composition modes, using the controls that are actually functional in the VHDL.

### Exercise 1: Rainbow Bands

<img src={hologram_exercise1_result} alt="Rainbow Bands result"/>
*Rainbow Bands — simulated result across source images.*
**Source**: A camera feed or recorded footage with recognizable subjects and moderate color content.

**Objective**: Understand how line spacing, spread, and hue offset create the basic holographic band pattern.

1. **Set up the effect**: Turn Pot 6 (Diffract/mix) to maximum to see the full holographic processing. Set Spread to about 75%.
2. **Wide bands**: Set Line Spacing high (~80%). The frame shows broad, slowly varying color regions that shift gradually from warm to cool and back.
3. **Narrow bands**: Reduce Line Spacing to minimum. The frame fills with tightly packed rainbow stripes — each scan line is a different hue.
4. **Moderate bands**: Set Line Spacing to about 50% for clearly visible but not overwhelming bands.
5. **Hue rotation**: Slowly sweep the Hue Offset knob. The entire rainbow slides through its full cycle — you can position a specific hue at any scan line.
6. **Spread control**: Reduce Spread to minimum. The rainbow bands become pastel tints barely visible over the source. Increase to maximum for deeply saturated spectral bands.

**Key concepts**: Line spacing controls band width via position right-shift, spread controls UV deviation magnitude, hue offset rotates the entire rainbow pattern

---

### Exercise 2: Animation and Orientation

<img src={hologram_exercise2_result} alt="Animation and Orientation result"/>
*Animation and Orientation — simulated result across source images.*
**Source**: Static or slow-moving footage so the scrolling rainbow effect is clearly visible.

**Objective**: Explore the animation system and horizontal/vertical band orientation.

1. **Enable animation**: Activate the Motion toggle (Switch 9). Set Scan Dir (Knob 5) to about 40%. The rainbow bands begin scrolling vertically across the frame.
2. **Speed control**: Sweep Scan Dir from minimum to maximum. At zero the pattern is frozen even with Motion on. At maximum the rainbow races.
3. **Vertical bands**: Toggle Type (Switch 7) to its second position. The rainbow bands now run vertically — column-aligned stripes that scroll horizontally when animated.
4. **Brightness shimmer**: Increase Bright (Knob 4) to maximum. The luminance now modulates in time with the rainbow, creating a visible brightness shimmer that tracks the hue bands.
5. **Replace mode**: Toggle Lines (Switch 8) to its second position. The source chrominance disappears — the rainbow bands are now pure spectral stripes overlaid on the source luminance. Compare with additive mode.

**Key concepts**: Animation advances phase accumulator per frame, horizontal and vertical orientation swap the position axis, brightness modulation is coupled to the UV delta, replace mode discards source color

---

### Exercise 3: Holographic Composition

<img src={hologram_exercise3_result} alt="Holographic Composition result"/>
*Holographic Composition — simulated result across source images.*
**Source**: A video source with strong visual structure — high contrast, recognizable geometry.

**Objective**: Combine all functional controls for a full holographic composition, understanding the mix and composition interactions.

1. **Full rainbow**: Spread at maximum, Line Spacing at about 50%, Hue Offset at default, Bright at about 60%.
2. **Animated scroll**: Motion on, Scan Dir at about 30% for a gentle scroll.
3. **Replace mode**: Toggle Lines (Switch 8) on for pure spectral bands over the source luminance.
4. **Mix back**: Reduce Diffract (Pot 6 — the effective mix) to about 60%. The holographic bands become semi-transparent, blending with the source video.
5. **Hue sweep**: While animated, slowly sweep Hue Offset to shift the starting point of the rainbow. Notice how the animation speed remains constant but the color mapping changes.
6. **Vertical orientation**: Toggle Type for vertical bands. The scrolling direction follows the band orientation.

**Key concepts**: Replace mode produces the strongest holographic effect, the mix control (Pot 6) blends the holographic and source signals, hue offset and animation are independent phase contributions

---


## Tips

- **Pot 6 is the real mix control**: Despite its TOML label "Diffract," Pot 6 controls the wet/dry crossfade in the VHDL. Set it to 0% for a clean bypass, or use intermediate values for transparent rainbow overlays. The TOML Fader 12 (Mix) has no effect.
- **Only three toggles work**: Switches 7, 8, and 9 are functional. Switch 10 and 11 are not mapped in the VHDL. Switch 7 is H/V orientation (not a color palette), and Switch 8 is additive/replace (not a line direction selector).
- **Spread controls saturation intensity**: This is the key "how much rainbow" control. Use low spread values for subtle holographic tints that preserve the source character; use maximum for saturated spectral dominance.
- **Hue Offset for color positioning**: Sweeping Knob 3 rotates the entire rainbow through all hues without changing the spatial pattern. Use this to place a specific color at a desired screen position.
- **Replace mode for strongest effect**: Toggle 8 in replace mode discards the source chrominance entirely, creating pure rainbow bands over the source luminance. This produces the most convincing holographic foil appearance.
- **Brightness shimmer follows hue**: The luma modulation is derived from the U delta, not computed independently. This means the brightness pattern is always coupled to the chrominance pattern — you cannot have shimmer without color shift.
- **Feedback amplifies the rainbow**: Routing the output back to the input applies the rainbow chrominance shift recursively, building increasingly saturated and complex color patterns with each pass.

---

## Glossary

| Term | Definition |
|------|------------|
| **Additive Mode** | Chrominance composition where the rainbow UV deltas are added to the source video's existing U and V values, tinting the original colors. |
| **Diamond Approximation** | A piecewise-linear path through UV color space that approximates circular hue rotation using four linear ramp segments, one per quadrant. |
| **Diffraction Grating** | A periodic structure that separates white light into spectral components; the physical phenomenon that holographic foils exploit for rainbow reflections. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Interpolator** | A linear crossfade module that blends between two input signals based on a mix parameter. |
| **LUT** | Look-Up Table; a basic logic element in FPGA fabric used to implement combinational functions. |
| **Phase Accumulator** | A register that increments by a fixed amount each frame, producing a sawtooth ramp that wraps at 16-bit overflow to drive cyclic animation. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Quadrant** | One of four 90-degree sectors of the UV color plane, each with a distinct sign combination for the U and V linear ramps. |
| **Replace Mode** | Chrominance composition where the source U and V are discarded and replaced with the rainbow pattern centered on neutral (512, 512). |
| **Spread** | The magnitude of UV deviation from neutral, controlling how saturated the rainbow bands appear. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
