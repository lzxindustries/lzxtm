---
draft: true
sidebar_position: 164
slug: /instruments/videomancer/linotype
title: "Linotype"
image: /img/instruments/videomancer/linotype/linotype_hero.png
description: "In 1886, Ottmar Mergenthaler's Linotype machine revolutionized printing by casting entire lines of metal type in a single operation — \"line o' type.\" An operator would key in text, and the machine would assemble brass matrices, cast a lead slug of the complete line, then advance to the next."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import linotype_hero from '/img/instruments/videomancer/linotype/linotype_hero.png';
import linotype_control_panel from '/img/instruments/videomancer/linotype/linotype_control_panel.png';
import linotype_exercise1_result from '/img/instruments/videomancer/linotype/linotype_exercise1_result.png';
import linotype_exercise2_result from '/img/instruments/videomancer/linotype/linotype_exercise2_result.png';
import linotype_exercise3_result from '/img/instruments/videomancer/linotype/linotype_exercise3_result.png';
import linotype_source1_kodim15 from '/img/instruments/videomancer/linotype/linotype_source1_kodim15.png';
import linotype_source2_kodim15_bw from '/img/instruments/videomancer/linotype/linotype_source2_kodim15_bw.png';
import linotype_source3_male_1024 from '/img/instruments/videomancer/linotype/linotype_source3_male_1024.png';

# Linotype

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: linotype_source1_kodim15, after: linotype_hero },
    { label: "Kodim15 B&W", before: linotype_source2_kodim15_bw, after: linotype_hero },
    { label: "Male", before: linotype_source3_male_1024, after: linotype_hero },
  ]}
/>
*Linotype progressively composing a cityscape line by line, the bright cursor bar advancing downward as inked content darkens above.*

---

## Overview

In 1886, Ottmar Mergenthaler's Linotype machine revolutionized printing by casting entire lines of metal type in a single operation — "line o' type." An operator would key in text, and the machine would assemble brass matrices, cast a lead slug of the complete line, then advance to the next. The process was sequential, mechanical, and irreversible: each line was committed to metal before the next could begin.

This program applies the same principle to video. A cursor bar advances down (or up) the frame at a configurable speed, capturing the live input one horizontal strip at a time into a BRAM line buffer. Above the cursor, previously captured content is displayed from the buffer — frozen in time, progressively darkened by the ink control as if the hot lead were cooling and oxidizing. Below the cursor, the output is either blank (like an unset galley) or passes the live source through. At the cursor position itself, a bright highlight bar marks the active composition edge — the point where new content is being "set."

The result is a temporal scroll effect that builds an image progressively from live video. Fast-moving subjects leave smeared horizontal traces as the cursor sweeps through them. Static subjects are captured faithfully but darken over time. The leading control introduces blank gaps between captured lines, evoking the vertical spacing between lines of set type. Direction, wrap mode, and speed controls let you shape the scroll's behavior from a slow, deliberate mechanical reveal to a rapid continuous loop.

---

## Background

### Hot-Metal Typesetting

The Linotype machine was the dominant method of setting text for newspapers, books, and magazines from the 1890s through the 1970s. Its key innovation was the *line slug* — an entire line of text cast as a single piece of lead alloy rather than assembled from individual movable type characters. The operator typed at a keyboard, and brass letter molds (matrices) dropped into an assembler. When a line was complete, molten lead was injected to cast the slug, which was then deposited into a galley tray while the matrices were automatically redistributed for reuse. The process was fast (5–7 lines per minute) but strictly sequential: each line had to be composed, cast, and placed before the next could begin. This sequential commitment — the impossibility of editing a line already cast — is the conceptual heart of the Videomancer program.

### Scan-Line Accumulation

Television and video signals are inherently line-sequential: the electron beam traces one horizontal line at a time, from top to bottom, field after field. Early video effects exploited this structure through **scan-line manipulation** — delaying, repeating, or replacing individual lines to create scrolls, wipes, and freeze effects. The Quantel DPE 5000 (1980) and Fairlight CVI (1984) both offered line-by-line capture modes where a frozen region expanded progressively across the frame. Linotype implements a similar technique in FPGA hardware: a dual-bank BRAM captures one line at the cursor position while the alternate bank supplies the previously captured content for display above it.

### The Cursor as Composition Edge

The bright bar at the cursor position serves a dual purpose. Visually, it marks the boundary between composed (above) and uncomposed (below) regions — analogous to the composition stick in hand typesetting or the casting slot in a Linotype machine. Technically, it identifies which scan lines are currently being written into the buffer. The cursor brightness control lets you set this bar from invisible (black) through a subtle marker to a dominant white flash, depending on whether you want the mechanical edge to be part of the visual composition or hidden.

### Ink Darkness and Temporal Decay

In physical typesetting, freshly cast lead type has a bright metallic surface that dulls and darkens as it oxidizes. Printed impressions made from worn type are lighter — the ink doesn't fill the eroded letter forms as completely. The ink darkness control simulates this temporal decay digitally: captured content is progressively attenuated by right-shifting the luminance channel. At full ink, captured lines are darkened to one-eighth brightness; at zero ink, they retain their original luminance. The effect is a visual gradient of age — the most recently captured lines are brightest, and everything above them fades into deepening shadow.

### Leading and Vertical Rhythm

In typography, *leading* (rhymes with "heading") is the vertical space between lines of text — named for the thin strips of lead inserted between rows of type to increase readability. Linotype's leading control inserts blank scan lines between the cursor and the previously captured content, creating a visual gap that separates each compositional strip. High leading produces a venetian-blind effect where strips of captured video alternate with black gaps; zero leading packs the strips tightly together into a continuous scroll.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Clock 1: Input Register + Buffer Address ───────────────────
│   ├─ Y₁, U₁, V₁ = data_in latched
│   ├─ buf_wr_addr = h_count (on cursor line) or 2047 (park)
│   ├─ buf_wr_data = {Y, U, V} packed 30-bit (on cursor line)
│   └─ buf_rd_addr = h_count (always)
│
├── Cursor Management (per-frame at vsync) ─────────────────────
│   ├─ frame_counter increments each frame
│   ├─ when frame_counter ≥ advance_threshold:
│   │   ├─ toggle bank_sel (swap BRAM banks)
│   │   └─ advance cursor_pos by line_height
│   └─ direction: top→bottom or bottom→top (with wrap option)
│
├── Clock 2: Region Determination ──────────────────────────────
│   ├─ v_count < cursor_pos:
│   │   ├─ dist = cursor_pos − v_count
│   │   ├─ dist ≤ leading → region = "01" (blank leading gap)
│   │   └─ dist > leading → region = "00" (captured content)
│   ├─ cursor_pos ≤ v_count < cursor_end → region = "10" (cursor)
│   └─ v_count ≥ cursor_end → region = "11" (below cursor)
│
├── Clock 3: Buffer Readback + Compose ─────────────────────────
│   ├─ Unpack buf_rd_data → raw_Y, raw_U, raw_V
│   └─ Pass Y₂, U₂, V₂ forward for below-cursor source
│
├── Clock 4: Apply Modifiers + Region Mux ──────────────────────
│   ├─ region "00": ink-darkened buffer {ink_Y, buf_U, buf_V}
│   ├─ region "01": blank {0, 512, 512}
│   ├─ region "10": cursor highlight {cursor_bright, 512, 512}
│   └─ region "11": blank {0, 512, 512} or source {Y₃, U₃, V₃}
│
├── Clocks 5–8: Interpolator (wet/dry Mix) ─────────────────────
│   └─ lerp(dry, wet, mix_amount) ×3 channels (4 clocks)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ 8-stage delay pipeline (hsync, vsync, field)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The dual-bank BRAM is the critical resource. While one bank is being read for display (above the cursor), the other bank captures the current cursor line's pixels. At each cursor advance the banks swap, so the newly captured line becomes the displayed content and the old display bank is available for the next capture. This ping-pong arrangement means the buffer only stores a single line at a time — the vertical scroll effect comes from the region determination logic, which simply replays that one captured line for every scan line above the cursor. The ink darkness attenuator then applies progressive right-shifting to the luminance of the replayed content, creating the illusion of temporal fading without requiring any additional storage.

---

## Parameter Reference

<img src={linotype_control_panel} alt="Videomancer front panel with Linotype loaded"/>
*Videomancer's front panel with Linotype active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Line H
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the cursor advance step — how many scan lines the cursor moves each time it advances. The raw register value is right-shifted by 4 and incremented, producing a range of 1 to 65 lines per step. At minimum, the cursor inches forward one line at a time, capturing a high-resolution progressive scan of the input. At maximum, it leaps forward in broad 65-line strips, producing a coarse venetian-blind composition where each captured band is a thick horizontal slice of whatever was on screen at that moment. Larger steps also mean the cursor traverses the full frame height in fewer advances, completing the scroll cycle faster.

---

#### Knob 2 — Comp Spd
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the composition speed — how many frames elapse between cursor advances. The raw value plus one gives a range of 1 to 1024 frames. At minimum (1 frame per advance), the cursor races down the screen, completing a full scroll in under a second at HD frame rates. At maximum, the cursor moves once every 1024 frames — roughly 17 seconds at 60 fps — producing an extremely slow, contemplative reveal where each captured line persists for a long time before the next arrives. This control interacts directly with Line Height: together they determine the scroll velocity in pixels per second.

---

#### Knob 3 — Scroll R
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls ink darkness — the degree to which captured content is attenuated in luminance. Despite the TOML label "Scroll R," this register maps to the ink darkening stage in the VHDL pipeline. The attenuation uses a stepped right-shift: values 0–255 apply no darkening (full brightness), 256–511 halve the luminance, 512–767 quarter it, and 768–1023 reduce it to one-eighth. The effect simulates the oxidation and wear of cast metal type — freshly captured content gleams, then progressively fades into shadow. At maximum ink darkness, the captured region appears nearly black, with only the faintest ghost of the original image visible.

---

#### Knob 4 — Ink Dark
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls leading — the blank gap between the cursor and the previously captured content. Despite the TOML label "Ink Dark," this register maps to the leading computation in the VHDL pipeline. The raw value is right-shifted by 3, producing 0 to 127 blank lines. At zero, captured content packs tightly up to the cursor with no gap. At higher values, an expanding band of black separates the cursor from the composed region above, evoking the lead spacer strips used between lines of metal type. The leading region outputs black (Y=0) with neutral chroma (U=V=512), creating a clean visual separation.

---

#### Knob 5 — Leading
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls cursor highlight brightness — the luminance level of the bright bar at the cursor position. Despite the TOML label "Leading," this register maps directly to the cursor bar's Y output value. At 0, the cursor is invisible — no visual distinction between the cursor zone and the blank region below. At 512 (mid-gray), the cursor is a subtle marker. At 1023 (full white), the cursor is a vivid white bar that dominates the composition edge. The cursor bar always outputs neutral chroma (U=V=512), producing a monochrome highlight regardless of the input video's color content.

---

#### Knob 6 — Column W
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the wet/dry mix amount for the final interpolator stage. Despite the TOML label "Column W," this register feeds the mix interpolator's blend factor. At 0, the output is entirely dry (unprocessed input). At 1023, the output is entirely wet (the Linotype composition). Intermediate values crossfade between the two, allowing you to overlay the progressive scroll effect at partial opacity on top of the live video. This is useful for creating ghostly reveal effects where the composed content emerges gradually from the full-motion source.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Style** | Roman | Gothic |
| **8 — Paper** | White | News |
| **9 — Feed** | Down | Up |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

Switches 7–10 configure four aspects of the scroll mechanism. Despite the TOML labels suggesting typographic styles ("Roman," "Gothic," etc.) and paper types, the actual VHDL mapping uses only the low bit of each toggle register for binary decisions. Switch 7 controls scroll direction (top-to-bottom or bottom-to-top). Switch 8 controls what appears below the cursor (blank or source passthrough). Switch 9 controls edge behavior (stop or wrap). Switch 10 is the bypass toggle — notably mapped to bit 3 rather than the conventional bit 4. The TOML-defined Switch 11 "Bypass" at bit 4 is never read by the VHDL and has no effect.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Listed in the TOML as "Mix" but the fader register (registers_in(7)) is never read by the VHDL implementation. The wet/dry mix function is instead performed by Knob 6 (registers_in(5)), which feeds the interpolator's blend factor. Moving this fader has no effect on the output.

---

## Guided Exercises

These exercises progress from a basic slow scroll through speed and direction variations to creative applications of the leading and ink controls. Each reveals a different aspect of the line-by-line composition process.

### Exercise 1: Slow Reveal

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: linotype_source1_kodim15, after: linotype_exercise1_result },
    { label: "Kodim15 B&W", before: linotype_source2_kodim15_bw, after: linotype_exercise1_result },
    { label: "Male", before: linotype_source3_male_1024, after: linotype_exercise1_result },
  ]}
/>
*Slow Reveal — simulated result across source images.*
**Source**: A static scene with rich detail — a bookshelf, a garden, or a cityscape.

**Objective**: Experience the basic line-by-line composition at slow speed, observing how the cursor captures and freezes content.

1. **Set slow speed**: Turn Comp Spd to ~80% for a very slow cursor advance.
2. **Medium line height**: Set Line H to ~25% for fine capture strips.
3. **No ink darkening**: Set Scroll R (ink) to 0% so captured content retains full brightness.
4. **No leading**: Set Ink Dark (leading) to 0% for tight line packing.
5. **Full cursor brightness**: Set Leading (cursor bright) to ~80% for a visible composition edge.
6. **Full wet mix**: Set Column W (mix) to ~100%.
7. **Downward direction**: Set Style to the first position (top-to-bottom).
8. **Blank below**: Set Paper to the first position.
9. **Stop at edge**: Set Feed to the first position.
10. **Watch the reveal**: Observe the cursor slowly descending, capturing each horizontal strip of the static scene. The composition builds like a photograph developing in a tray.

**Key concepts**: Cursor advance is frame-counted, line height determines strip thickness, speed determines temporal resolution of the capture

---

### Exercise 2: Ink Fade and Leading

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: linotype_source1_kodim15, after: linotype_exercise2_result },
    { label: "Kodim15 B&W", before: linotype_source2_kodim15_bw, after: linotype_exercise2_result },
    { label: "Male", before: linotype_source3_male_1024, after: linotype_exercise2_result },
  ]}
/>
*Ink Fade and Leading — simulated result across source images.*
**Source**: A moving subject — a person walking, traffic, or flowing water.

**Objective**: Explore how ink darkness and leading create temporal layering and visual rhythm in the composed image.

1. **Start from Exercise 1 settings** but with faster speed: Comp Spd ~40%.
2. **Moderate line height**: Line H ~30%.
3. **Enable ink darkening**: Increase Scroll R (ink) to ~70%. Watch as previously captured content progressively darkens, creating a gradient of temporal recency — recent captures bright, old captures dark.
4. **Add leading**: Increase Ink Dark (leading) to ~50%. Black gaps appear between captured strips, creating a venetian-blind rhythm.
5. **Enable source passthrough**: Set Paper to the second position. The live video now shows below the cursor, creating a split-screen between frozen composition and live feed.
6. **Try upward scrolling**: Switch Style to the second position. The cursor now builds from bottom to top.
7. **Enable wrap**: Set Feed to the second position. The cursor loops continuously, replacing old content with new captures on each pass.

**Key concepts**: Ink darkness simulates temporal decay, leading creates vertical rhythm, source passthrough enables split-screen composition, wrapping creates continuous cycling

---

### Exercise 3: Rapid Composition Loop

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: linotype_source1_kodim15, after: linotype_exercise3_result },
    { label: "Kodim15 B&W", before: linotype_source2_kodim15_bw, after: linotype_exercise3_result },
    { label: "Male", before: linotype_source3_male_1024, after: linotype_exercise3_result },
  ]}
/>
*Rapid Composition Loop — simulated result across source images.*
**Source**: Fast-moving footage — dance performance, sports, or rapid camera movement.

**Objective**: Use rapid scrolling with coarse line height to create abstract temporal smearing effects.

1. **Maximum speed**: Set Comp Spd to 0% (1 frame per advance — fastest possible).
2. **Large line height**: Set Line H to ~80% for thick 50+ line strips.
3. **Heavy ink**: Set Scroll R (ink) to ~90% for aggressive darkening.
4. **Moderate leading**: Ink Dark (leading) ~30% for subtle gaps.
5. **Dim cursor**: Set Leading (cursor bright) to ~20% for a subtle marker.
6. **Enable wrap**: Set Feed to the second position for continuous looping.
7. **Partial mix**: Set Column W (mix) to ~60% to blend the composition with the live source.
8. **Observe**: The rapid cursor creates thick horizontal bands that capture motion blur artifacts. Fast movement produces ghostly smears; the ink darkening pushes older bands into near-black. The overall effect resembles a mechanical shutter scanning across the frame.

**Key concepts**: Speed and line height together determine scroll velocity, large line height creates coarse temporal sampling, partial mix blends composition with live source, wrap mode creates continuous temporal record

---


## Tips

- **Speed × Line Height = scroll velocity**: These two controls are multiplicative. For ultra-slow reveals, combine minimum line height with maximum speed delay. For rapid scanning, use fast speed with large line height.
- **Ink darkness is stepped, not smooth**: The four attenuation levels (1×, ½×, ¼×, ⅛×) create visible brightness bands in the composed region. Use this intentionally by setting ink to a value near a threshold boundary for a specific target attenuation.
- **Leading creates rhythm**: Even a small amount of leading transforms the composition from a continuous scroll into a stacked-strip structure with visual breathing room between captured bands.
- **Source passthrough for preview**: Enable Paper's second position to see live video below the cursor — useful for anticipating what the next captured line will contain.
- **Wrap mode for live looping**: In continuous wrap mode, the program becomes a perpetual temporal scanner, endlessly cycling through the frame and replacing old captures with new ones. The ink darkening makes older captures fade before they're overwritten.
- **Bypass is on Switch 10, not Switch 11**: The VHDL maps bypass to bit 3 (Switch 10 "Animate"), not bit 4 (Switch 11 "Bypass"). The TOML labels are misleading — trust the hardware behavior.
- **The fader does nothing**: The Mix fader (linear_potentiometer_12) is cosmetically present but electrically disconnected in the VHDL. Use Knob 6 for wet/dry mix instead.
- **Feedback creates temporal fractals**: Route the output back to the input. Each scroll pass captures the previous pass's composition, producing nested temporal layers that darken and compress with each cycle.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bank swap** | Alternating between two memory banks so one can be written while the other is read, preventing read-write conflicts in the line buffer. |
| **BRAM** | Block RAM; dedicated memory blocks within the FPGA used here as a dual-bank video line buffer for capturing and replaying horizontal strips. |
| **Cursor** | The active composition edge that marks where new video content is being captured into the line buffer. |
| **DDS** | Direct Digital Synthesis; a phase-accumulator technique for generating periodic signals, used here for frame counting. |
| **FPGA** | Field-Programmable Gate Array; the reconfigurable hardware that implements the video processing pipeline. |
| **Galley** | In typesetting, a tray that holds composed lines of type; analogously, the region above the cursor where captured content is displayed. |
| **Ink darkness** | Luminance attenuation applied to captured content, simulating the darkening of cast metal type as it ages. |
| **Leading** | The vertical space between lines of composed text (or captured video strips), named for the lead spacer strips used in metal typesetting. |
| **Linotype** | A hot-metal typesetting machine (1886) that cast entire lines of text as single metal slugs; the namesake and conceptual model for this program. |
| **Pipeline** | A sequence of processing stages where each stage's output feeds the next on each clock cycle. |
| **Proc amp** | Processing amplifier; a gain-and-offset video circuit used here within the interpolator stage for wet/dry mixing. |
| **Scan line** | A single horizontal row of pixels in a video frame; the fundamental unit of capture in this program. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used as the native pixel format in the Videomancer processing pipeline. |

---
