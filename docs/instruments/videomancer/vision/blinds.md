---
draft: true
sidebar_position: 21
slug: /instruments/videomancer/blinds
title: "Blinds"
image: /img/instruments/videomancer/blinds/blinds_hero.png
description: "Every broadcast engineer knows the venetian blind wipe — a grid of horizontal or vertical slats that open or close to reveal or conceal a video source."
---

import blinds_hero from '/img/instruments/videomancer/blinds/blinds_hero.png';
import blinds_before_after from '/img/instruments/videomancer/blinds/blinds_before_after.png';
import blinds_control_panel from '/img/instruments/videomancer/blinds/blinds_control_panel.png';
import blinds_exercise1_result from '/img/instruments/videomancer/blinds/blinds_exercise1_result.png';
import blinds_exercise2_result from '/img/instruments/videomancer/blinds/blinds_exercise2_result.png';
import blinds_exercise3_result from '/img/instruments/videomancer/blinds/blinds_exercise3_result.png';

# Blinds

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={blinds_hero} alt="Blinds hero image"/>
*Blinds splitting a broadcast frame into cascading horizontal slats with soft edges, revealing a dimmed background through partially open gaps.*
<img src={blinds_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Blinds applied.*

---

## Overview

Every broadcast engineer knows the venetian blind wipe — a grid of horizontal or vertical slats that open or close to reveal or conceal a video source. Blinds takes that classic DVE transition and turns it into a continuously controllable instrument. Instead of a one-shot effect triggered between two sources, every parameter is live: the number of slats, how far they open, how the opening cascades across the frame, and how soft the edges are.

The name is literal. The program simulates the mechanics of window blinds: parallel slats that rotate open from their centers, each potentially offset in phase from its neighbors. A cascade control staggers the opening across slats so they peel apart in sequence rather than all at once — precisely the visual language of a broadcast wipe, but frozen at any point and modulated in real time.

At one extreme, Blinds is a hard geometric mask — solid bars of video separated by solid bars of black. At the other extreme, with high edge softness and cascade, it produces flowing organic reveals where the video seems to breathe through a series of translucent curtains. An auto-animation mode drives the opening with a triangle wave, creating continuous back-and-forth motion without any external control.

---

## Background

### Venetian Blind Transitions in Broadcast

The venetian blind wipe is one of the original SMPTE wipe patterns defined in the earliest broadcast standards. It divides the frame into parallel bands and progressively reveals the incoming source by widening each band from its center. Hardware DVE units in the 1980s and 1990s implemented it with dedicated scan-line counters and comparators — the same approach Blinds uses in FPGA logic. Unlike software compositors that render the effect in a frame buffer, Blinds computes the transition per-pixel in real time, at the native video clock rate.

### Digital Video Effects History

DVE (Digital Video Effects) processors emerged in the late 1970s with systems like the Quantel DPE 5000 and the Ampex ADO. These machines could squeeze, rotate, and wipe video sources in ways that were impossible with analog switchers. The venetian blind was a staple of every DVE's wipe pattern library, alongside barn doors, iris wipes, and diamond patterns. Blinds distills the venetian blind wipe down to its essential geometry and makes every parameter continuously variable — something the original hardware could not do.

### Slat Geometry

Blinds divides the frame into 2–16 equally-sized slats. The division must be exact to avoid visible seams, which is non-trivial in hardware because integer division by arbitrary numbers requires multiplication by reciprocals. The VHDL implementation uses a lookup table of reciprocal constants (e.g., ×171≫10 for division by 6, ×85≫10 for division by 12) to compute slat boundaries without a hardware divider. Each slat's opening is measured from its center outward — a half-open slat reveals the middle portion and hides the edges, exactly like a physical venetian blind rotating around its center rod.

### Cascade Mechanics

The cascade control adds a per-slat phase offset to the opening value. If cascade is zero, all slats open simultaneously. As cascade increases, each successive slat lags behind the previous one, creating a wave-like reveal that sweeps across the frame. The offset is proportional to the slat index: slat 0 opens first, slat 1 opens slightly later, slat 2 later still, and so on. This produces the classic "peeling" motion of a broadcast blind wipe. Combined with auto-animation, cascade creates a continuous ripple pattern across the slat array.

### Edge Softness

Hard-edged slat boundaries look clean and graphic but can alias harshly on interlaced displays. The edge softness control adds a linear ramp at the boundary between the visible and hidden regions of each slat. Instead of an instantaneous transition from full video to full background, pixels near the boundary fade smoothly. This transforms the hard geometric wipe into an organic curtain effect. At maximum softness with moderate opening, the slats overlap in transparency, creating a layered gauze-like appearance.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Coordinate Selection & Slat Division ──────────────
│   ├─ Select coordinate axis (v_count for Horiz, h_count for Vert)
│   ├─ Determine frame size (720 or 1280)
│   ├─ Look up slat count from Slats step table [2,4,6,8,10,12,14,16]
│   ├─ Compute slat_size = frame_size / num_slats (reciprocal multiply)
│   └─ Compute slat_idx and position within slat
│
├── Stage 2: Cascade Phase Offset ──────────────────────────────
│   ├─ DDS animation: 16-bit phase accumulator (triangle wave)
│   ├─ Manual/Auto select (Open pot or triangle wave)
│   ├─ Cascade offset = (cascade × slat_idx) >> 4
│   └─ Effective opening = anim_open − cascade_offset (clamped 0–1023)
│
├── Stage 3: Opening & Edge Softness ───────────────────────────
│   ├─ Opening pixels = (slat_size × effective_open) >> 10
│   ├─ half_open = opening_pixels / 2
│   ├─ center = slat_size / 2
│   ├─ Distance from center → reveal mask (1023 inside, 0 outside)
│   ├─ Edge softness ramp at reveal boundary
│   └─ Invert toggle swaps reveal polarity
│
├── Stage 4: Composition ───────────────────────────────────────
│   ├─ Y: (video_y × reveal + bg_y × (1023 − reveal)) >> 10
│   ├─ Background: Black mode → bg_level; Dim Vid → (input_y × bg_level) >> 10
│   ├─ UV: source chroma if reveal > 512, else bg-mode dependent
│   └─ 3× interpolator_u for final mix (linear_potentiometer_12)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Pass-through (hsync, vsync, field, avid)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The critical interaction is between cascade and edge softness. Cascade distributes the opening offset across slats so they appear to open in sequence; edge softness then blurs the boundary of each individual slat's opening. Together they produce a rippling, semi-transparent curtain effect that would be impossible with either control alone. The background composition in Stage 4 offers two distinct personalities: Black mode produces clean graphic bars against darkness, while Dim Vid mode lets the source bleed through at reduced brightness, maintaining visual continuity during the transition.

---

## Parameter Reference

<img src={blinds_control_panel} alt="Videomancer front panel with Blinds loaded"/>
*Videomancer's front panel with Blinds active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Open
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls how far each slat opens, measured as a percentage of the slat width. At 0% every slat is fully closed — the entire frame is replaced by the background. At 100% every slat is fully open and the source video passes through unobstructed. In auto-animation mode this control is overridden by the triangle-wave oscillator, but in manual mode it is the primary transition control. Sweeping Open from 0 to 100% performs the classic venetian blind reveal.

---

#### Knob 2 — Slats
| Property | Value |
|----------|-------|
| Range | 2 – 16 |
| Default | 7 |

Selects the number of slats from a fixed set: 2, 4, 6, 8, 10, 12, 14, or 16. Low slat counts produce bold, dramatic bars. High slat counts create a fine-grained lattice. Because the VHDL uses a step-quantized lookup with 128-count thresholds, intermediate pot positions snap to the nearest valid count — there are no in-between values. The slat size is computed as the frame dimension divided by the count, using reciprocal-multiply approximation for non-power-of-two divisors.

---

#### Knob 3 — Cascade
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Adds a progressive phase offset to each slat's opening value. At 0% all slats open and close together. As cascade increases, slat 0 leads and each subsequent slat opens later, creating the signature wave-like reveal of a broadcast blind wipe. At high cascade values with moderate opening, some slats are fully open while others are still closed, producing a staggered bar pattern across the frame.

---

#### Knob 4 — Edge Soft
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 6% |
| Suffix | % |

Controls the width of the linear fade ramp at the edge of each slat's opening. At 0% the boundary is a hard pixel-level cut — fully visible on one side, fully hidden on the other. As edge softness increases, the transition zone widens into a smooth gradient. This softens the geometric harshness of the slat edges and creates translucent overlap zones when combined with high cascade values.

---

#### Knob 5 — Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Sets the rate of the auto-animation triangle-wave oscillator. The DDS phase accumulator advances by this value each vertical sync pulse, so higher values produce faster oscillation. The triangle wave sweeps the effective opening from 0 to 1023 and back, creating continuous blind-open/blind-close motion. This control has no effect when the Animate toggle is set to Manual.

---

#### Knob 6 — Bg Level
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Sets the brightness of the background visible through closed portions of the slats. In Black mode, this directly controls the background luminance — 0% is pure black, 100% is full white. In Dim Vid mode, it acts as a gain multiplier on the input video, so 0% is black and 100% passes the source at full brightness. Low values create a dramatic reveal against darkness; higher values keep the background visible as a dimmed underlay.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Orient** | Horiz | Vert |
| **8 — Animate** | Manual | Auto |
| **9 — Bg Mode** | Black | Dim Vid |
| **10 — Invert** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control orientation, animation source, background behavior, mask polarity, and bypass. Orient and Animate define the fundamental character of the effect. Bg Mode determines whether the hidden regions are a flat color or dimmed video, which dramatically changes the visual feel. Invert swaps which portions of the slat are visible versus hidden. Bypass provides instant A/B comparison.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Dry/wet mix between the processed blind effect and the original source video. At 100% the full blind effect is visible. At 0% the original video passes through unchanged. Intermediate positions blend the two, which can create interesting semi-transparent overlay effects where the slat structure is ghosted over the source.

---

## Guided Exercises

These exercises progress from a basic manual wipe to animated cascade effects to textured background compositions, exploring Blinds as both a broadcast tool and a creative video instrument.

### Exercise 1: Manual Venetian Blind Wipe

<img src={blinds_exercise1_result} alt="Manual Venetian Blind Wipe result"/>
*Manual Venetian Blind Wipe — simulated result across source images.*
**Source**: A live camera feed or recorded footage with recognizable subjects and clear mid-frame structure.

**Objective**: Learn the core slat geometry and opening mechanics by performing a manual blind wipe.

1. **Set up slats**: Set Slats to about 50% to get 8 horizontal bars across the frame.
2. **Close the blinds**: Set Open to 0%. The entire frame should be replaced by the background (black by default).
3. **Open gradually**: Slowly sweep Open from 0% to 100%. Watch the slats split open from their centers, progressively revealing the source video.
4. **Change orientation**: Toggle Orient to Vert. The bars rotate 90° to vertical strips. Sweep Open again and observe the vertical reveal.
5. **Adjust slat count**: Try 2 slats (Slats at minimum) versus 16 slats (Slats at maximum). Notice how low counts create dramatic wide bars while high counts create a fine louvered texture.
6. **Invert**: Toggle Invert On. The geometry reverses — now the edges open while centers stay hidden.

**Key concepts**: Slats open from center outward, slat count is quantized to even values 2–16, orientation swaps the coordinate axis, invert reverses the reveal polarity

---

### Exercise 2: Cascading Wipe with Soft Edges

<img src={blinds_exercise2_result} alt="Cascading Wipe with Soft Edges result"/>
*Cascading Wipe with Soft Edges — simulated result across source images.*
**Source**: Footage with a mix of detail and open areas — landscape or studio content.

**Objective**: Explore cascade phase offset and edge softness to create flowing, organic wipe motions.

1. **Prepare**: Set 6 slats (Slats ~35%), Open ~40%, Cascade 0%, Edge Soft 0%.
2. **Add cascade**: Slowly increase Cascade. Each slat now opens at a different time — slat 0 is widest, and each subsequent slat narrows progressively. The frame shows a gradient from open to closed.
3. **Sweep with cascade**: Hold Cascade at ~60% and slowly sweep Open from 0% to 100%. Watch the staggered wave of opening roll across the slats.
4. **Soften edges**: Increase Edge Soft to ~50%. The hard boundaries between visible and hidden regions smooth into gradients. The slats now feel like translucent curtains rather than hard bars.
5. **Maximum softness**: Push Edge Soft to 100%. Adjacent slats overlap in transparency, creating a layered gauze effect.
6. **Auto-animate**: Toggle Animate to Auto and set Speed to ~30%. The triangle wave sweeps the opening continuously, and the cascade creates a rippling motion across the frame.

**Key concepts**: Cascade offsets opening per-slat by index, edge softness adds a linear ramp at reveal boundaries, combined cascade and softness produce organic flowing reveals, auto-animation drives continuous motion

---

### Exercise 3: Dimmed Video Background Composition

<img src={blinds_exercise3_result} alt="Dimmed Video Background Composition result"/>
*Dimmed Video Background Composition — simulated result across source images.*
**Source**: High-contrast footage — strong subjects against distinct backgrounds.

**Objective**: Use Dim Vid background mode with moderate opening to create layered compositions where the source is visible at two brightness levels simultaneously.

1. **Set up**: 10 slats (Slats ~60%), Open ~50%, Cascade ~30%.
2. **Switch to Dim Vid**: Toggle Bg Mode to Dim Vid.
3. **Raise background**: Increase Bg Level to ~40%. The closed portions of the slats now show the source video at reduced brightness instead of black. The frame has a striped brightness pattern — full video in the open regions, dimmed video in the closed regions.
4. **Soften**: Increase Edge Soft to ~40%. The brightness transitions become gradual, creating a rolling luminance pattern across the frame.
5. **Vertical orientation**: Switch Orient to Vert. The same layered composition now runs in vertical columns.
6. **Add invert**: Toggle Invert. The bright and dim regions swap — the geometric pattern inverts but the overall composition retains its layered quality.
7. **Mix back**: Lower Mix to ~60% to blend the effect with the unprocessed source, softening the overall contrast.

**Key concepts**: Dim Vid mode shows the source at two brightness levels simultaneously, Bg Level acts as a gain multiplier on the dimmed copy, edge softness creates gradual brightness transitions across the frame, mix blends the final effect with the dry source

---


## Tips

- **Start with Cascade at zero**: Learn the basic open/close geometry first, then add cascade to stagger the slats. Cascade without understanding the base opening can be confusing.
- **Edge Soft transforms the effect**: At zero softness, Blinds is a hard geometric mask. At high softness, it becomes an organic luminance modulator. These are almost two different programs controlled by one knob.
- **Dim Vid for layered compositions**: Black background gives clean graphic bars. Dim Vid background maintains the source at reduced brightness, creating dual-exposure layered effects.
- **Auto-animation is hands-free**: Set Animate to Auto, dial in a Speed, and let the triangle wave drive continuous motion. Free up your hands for other controls.
- **Cascade + auto-animation = ripple**: When both cascade and auto-animation are active, the staggered phase offset creates a ripple wave that rolls across the frame continuously.
- **Low slat count for drama**: Two or four slats create bold, cinematic bars. Sixteen slats create a fine venetian-blind texture. Match the count to the scale of your composition.
- **Invert for negative space**: Invert swaps which parts of the frame are visible. Use it to shift the focus from the revealed content to the revealed background.
- **Mix for ghosting**: Intermediate mix values overlay the slat structure semi-transparently over the source, creating a ghost-bar texture that can be very effective as a subtle overlay.

---

## Glossary

| Term | Definition |
|------|------------|
| **Cascade** | A progressive phase offset applied to each successive slat so they open or close in sequence rather than simultaneously, producing a wave-like reveal. |
| **DDS** | Direct Digital Synthesis; a technique that generates periodic waveforms by advancing a phase accumulator by a fixed increment each cycle. |
| **DVE** | Digital Video Effects; a hardware processor for real-time video transformations such as wipes, squeezes, and rotations, common in broadcast production. |
| **Interpolator** | A hardware mixing block that crossfades between two input signals using a weighted average, used here for dry/wet and foreground/background blending. |
| **Phase accumulator** | A register that increments by a fixed step each vertical sync pulse; its value drives the triangle wave oscillator for auto-animation. |
| **Reciprocal multiply** | A division approximation that replaces expensive hardware division with multiplication by a pre-computed reciprocal constant followed by a right shift. |
| **Reveal mask** | A per-pixel value (0–1023) indicating the proportion of source video visible versus background at that pixel location. |
| **Slat** | One horizontal or vertical band in a venetian blind division of the frame, analogous to a single louver in a physical window blind. |
| **SMPTE** | Society of Motion Picture and Television Engineers; the standards body that defines broadcast wipe patterns, timecode, and video signal formats. |
| **Triangle wave** | A periodic waveform that ramps linearly up then linearly down, used by the auto-animation oscillator to sweep slat opening back and forth. |
| **YUV** | A colour encoding system that separates brightness (Y) from two colour-difference components (U and V), used as the native signal format in Videomancer. |

---
