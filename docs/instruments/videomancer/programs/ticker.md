---
draft: true
sidebar_position: 306
slug: /instruments/videomancer/ticker
title: "Ticker"
image: /img/instruments/videomancer/ticker/ticker_hero_s1.png
description: "Before digital screens, breaking news arrived on paper — a narrow ribbon of stock quotes and wire reports printed character by character on ticker tape machines."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import ticker_control_panel from '/img/instruments/videomancer/ticker/ticker_control_panel.png';
import ticker_source1_sunset from '/img/instruments/videomancer/ticker/ticker_source1_sunset.png';
import ticker_source2_parrot from '/img/instruments/videomancer/ticker/ticker_source2_parrot.png';
import ticker_source3_clouds from '/img/instruments/videomancer/ticker/ticker_source3_clouds.png';
import ticker_source4_pattern from '/img/instruments/videomancer/ticker/ticker_source4_pattern.png';
import ticker_source5_man from '/img/instruments/videomancer/ticker/ticker_source5_man.png';
import ticker_source6_wood from '/img/instruments/videomancer/ticker/ticker_source6_wood.png';
import ticker_hero_s1 from '/img/instruments/videomancer/ticker/ticker_hero_s1.png';
import ticker_hero_s2 from '/img/instruments/videomancer/ticker/ticker_hero_s2.png';
import ticker_hero_s3 from '/img/instruments/videomancer/ticker/ticker_hero_s3.png';
import ticker_hero_s4 from '/img/instruments/videomancer/ticker/ticker_hero_s4.png';
import ticker_hero_s5 from '/img/instruments/videomancer/ticker/ticker_hero_s5.png';
import ticker_hero_s6 from '/img/instruments/videomancer/ticker/ticker_hero_s6.png';
import ticker_ex1_s1 from '/img/instruments/videomancer/ticker/ticker_ex1_s1.png';
import ticker_ex1_s2 from '/img/instruments/videomancer/ticker/ticker_ex1_s2.png';
import ticker_ex1_s3 from '/img/instruments/videomancer/ticker/ticker_ex1_s3.png';
import ticker_ex1_s4 from '/img/instruments/videomancer/ticker/ticker_ex1_s4.png';
import ticker_ex1_s5 from '/img/instruments/videomancer/ticker/ticker_ex1_s5.png';
import ticker_ex1_s6 from '/img/instruments/videomancer/ticker/ticker_ex1_s6.png';
import ticker_ex2_s1 from '/img/instruments/videomancer/ticker/ticker_ex2_s1.png';
import ticker_ex2_s2 from '/img/instruments/videomancer/ticker/ticker_ex2_s2.png';
import ticker_ex2_s3 from '/img/instruments/videomancer/ticker/ticker_ex2_s3.png';
import ticker_ex2_s4 from '/img/instruments/videomancer/ticker/ticker_ex2_s4.png';
import ticker_ex2_s5 from '/img/instruments/videomancer/ticker/ticker_ex2_s5.png';
import ticker_ex2_s6 from '/img/instruments/videomancer/ticker/ticker_ex2_s6.png';
import ticker_ex3_s1 from '/img/instruments/videomancer/ticker/ticker_ex3_s1.png';
import ticker_ex3_s2 from '/img/instruments/videomancer/ticker/ticker_ex3_s2.png';
import ticker_ex3_s3 from '/img/instruments/videomancer/ticker/ticker_ex3_s3.png';
import ticker_ex3_s4 from '/img/instruments/videomancer/ticker/ticker_ex3_s4.png';
import ticker_ex3_s5 from '/img/instruments/videomancer/ticker/ticker_ex3_s5.png';
import ticker_ex3_s6 from '/img/instruments/videomancer/ticker/ticker_ex3_s6.png';

# Ticker

<span class="head2_nolink">Videomancer Program Guide</span>

:::warning
This document is still in progress, may contain errors, and is for preview only.
:::

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: ticker_source1_sunset, after: ticker_hero_s1 },
    { label: "Parrot", before: ticker_source2_parrot, after: ticker_hero_s2 },
    { label: "Clouds", before: ticker_source3_clouds, after: ticker_hero_s3 },
    { label: "Pattern", before: ticker_source4_pattern, after: ticker_hero_s4 },
    { label: "Man", before: ticker_source5_man, after: ticker_hero_s5 },
    { label: "Wood", before: ticker_source6_wood, after: ticker_hero_s6 },
  ]}
/>
*Ticker rendering a luminance-quantized scrolling tape band across a live video feed, with bright border lines framing the horizontal strip.*

---

## Overview

Before digital screens, breaking news arrived on paper — a narrow ribbon of stock quotes and wire reports printed character by character on ticker tape machines. The tape was the original continuous data stream: an unbroken horizontal scroll of information gliding past the reader's eyes. Ticker recreates this visual paradigm inside the video domain. It draws a configurable horizontal band across the frame, quantizes the source luminance within that band to create high-contrast "text-like" patterns, and dims the video outside the band to push attention inward.

The quantization engine is the heart of the effect. By progressively reducing the number of brightness levels inside the band, smooth gradients collapse into hard-edged regions that mimic the appearance of printed characters on paper. This is not OCR or font rendering — it is the source video itself being posterized so aggressively that natural shapes begin to resemble typographic forms. The four Style presets control how aggressively the region outside the band is dimmed, evoking different mechanical eras: stock ticker, telex, receipt printer, and television news crawl.

The Tape Spd control advances a horizontal scroll offset each frame, shifting the composite position so that the quantized content appears to scroll across the band. Combined with the Paper Hue and Ink Hue tint controls, Ticker can produce anything from a clean white news banner with black text to a warm sepia telegraph strip with golden ink borders.

---

## Quick Start

1. **Start with Contrast**: The quantization depth is the single most impactful control. Begin with moderate quantization and adjust band size around it.
2. **Border lines anchor the eye**: Enable Edge Show whenever the band overlays a bright source — without borders, the band edges can be hard to perceive.
3. **News mode is a transparent overlay**: Style = News keeps the outside source at full brightness, making the band read as a semi-opaque crawl over live video.

---

## Background

### The Ticker Tape Machine

The stock ticker was patented in 1867 by Edward Calahan and improved by Thomas Edison in 1871. It printed abbreviated company names and share prices on a narrow strip of paper tape that unspooled continuously from a glass dome. The visual signature — a thin horizontal strip of high-contrast characters on pale paper — became an icon of financial information. Ticker recreates this visual by drawing a band of quantized video across the screen, with the original signal dimmed outside the band to simulate the surrounding machinery.

### Luminance Quantization as Typography

When a continuous-tone image is posterized to two or three brightness levels, the resulting shapes lose their photographic character and begin to resemble printed matter. This is the same principle behind newspaper halftoning and woodcut illustration: reduce tonal complexity until only the most prominent edges and shapes survive. Ticker exploits this by quantizing the source luma inside the band — the Contrast knob controls how many levels remain. At maximum quantization (shift 8), only two levels survive, producing hard black-and-white "characters." At minimum quantization (shift 0), the full 10-bit source passes through unchanged.

### Horizontal Scrolling via Frame Offset

The scroll animation works by incrementing a horizontal pixel offset counter on each video frame. This offset shifts the composite position of the band content, so that over successive frames the quantized patterns appear to slide left or right. The scroll speed is controlled by the Tape Spd parameter, which determines how many pixels the offset advances per frame. Because the offset wraps at the edge of the active video region, the scroll is seamless and continuous.

### Band Composition and Dimming Styles

Outside the ticker band, the source video is dimmed by a configurable amount. The four Style presets control the dimming shift: Ticker applies a light dim (shift right by 1), Telex applies a medium dim (shift right by 2), Receipt applies a heavy dim (shift right by 3), and News applies no dimming at all. This creates the visual context for the band — at heavy dimming, the band stands out dramatically against a nearly black background; at no dimming, the band overlays the full-brightness source, resembling a translucent crawl.

### Border Lines and Framing

When Edge Show is enabled, bright horizontal lines are drawn at the top and bottom edges of the band. These borders are a fixed 2 pixels wide and use the Ink Hue color. They visually separate the quantized content from the dimmed background, reinforcing the "tape" metaphor. The borders also help anchor the band's vertical position when the viewer's eye is tracking scrolling content.


---

## Signal Flow

Input Register + Invert → Band Detection + Border → Content Compose → Output Composite

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Input Register + Invert ──────────────────────────
│   └─ If Invert enabled, Y ← bitwise NOT(Y)
│
├── Stage 2: Band Detection + Border ──────────────────────────
│   ├─ Is v_count between band_top and band_bottom?
│   │   ├── Yes: in_band = 1
│   │   └── No:  outside_band = 1
│   ├─ Is v_count within 2px of top/bottom edge? → on_border
│   └─ Pass through Y/U/V (no scroll re-addressing in stream)
│
├── Stage 3: Content Compose ──────────────────────────────────
│   ├─ In-band:
│   │   └─ Quantize Y by s_quant_shift (contrast → 9 steps)
│   │      (truncate lower bits, zero-fill)
│   └─ Chroma pass-through
│
├── Stage 4: Output Composite ─────────────────────────────────
│   ├─ Border pixel → Ink Hue YUV
│   ├─ In-band pixel → quantized Y + source UV
│   └─ Outside-band  → dimmed Y (style-dependent shift) + mid UV
│
├── Interpolator ──────────────────────────────────────────────
│   └─ Mix(dry=delayed_input, wet=composite, t=mix_amount)
│
└── Bypass Mux ────────────────────────────────────────────────
    └─ bypass=1 → delayed input; bypass=0 → mix result
```

The quantization stage is the core of the text-like effect. It works by truncating the lower bits of the 10-bit luma value — a shift of 8 leaves only 2 levels (binary), while a shift of 0 passes through all 1024 levels. The Contrast parameter maps into 9 discrete quantization steps via threshold comparisons, so the effect transitions in visible jumps rather than smooth gradients.

Outside the band, the source luma is dimmed by right-shifting (dividing by powers of 2), and chroma is forced to mid-level (512), producing a desaturated, dimmed background. This compositional strategy — bright quantized content on a dimmed field — is what creates the ticker-tape illusion.

---

## Parameter Reference

<img src={ticker_control_panel} alt="Videomancer front panel with Ticker loaded"/>
*Videomancer's front panel with Ticker active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Tape Spd
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the scroll animation speed. The register value is right-shifted by 3 to derive the per-frame pixel increment. At minimum, the scroll is essentially frozen. At maximum, the content races across the band at approximately 127 pixels per frame, producing a rapid blur of quantized shapes. The scroll direction is determined by the Style toggle's LSB. When Animate is disabled, the scroll offset holds steady regardless of this control's value.

---

#### Knob 2 — Tape H
| Property | Value |
|----------|-------|
| Range | 16 – 128 |
| Default | 72 |

Controls the vertical height of the ticker band in 8 discrete steps: 32, 64, 96, 128, 192, 256, 384, and 512 scan lines. The step is selected by the top 3 bits of the register. A narrow band (32 lines) creates a thin news-crawl strip; a tall band (512 lines) covers nearly half the 1080-line HD frame, creating a broad window of quantized content.

---

#### Knob 3 — Tape Pos
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the vertical position of the band's top edge. The register value is mapped to line numbers 0–1023, with automatic clamping so the band never extends below line 1079. At minimum the band sits at the top of frame; at maximum it rests near the bottom. Combined with Height, this positions the tape strip anywhere on screen.

---

#### Knob 4 — Contrast
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the luma quantization depth inside the band. The register is mapped to 9 threshold steps, each corresponding to a bit-shift amount from 0 (no quantization, full 10-bit pass-through) to 8 (extreme 2-level binary). At moderate settings the source degrades into visible posterization bands. At high settings the content reduces to pure black-and-white silhouettes — the most convincingly "typographic" look.

---

#### Knob 5 — Paper Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Tints the tape background. The register is divided into four hue regions. Below 256 the tape is warm off-white (slightly pink paper). From 256–511 the tape takes a neutral warm tone. From 512–767 it shifts to a cool blue-white tint. Above 768 it becomes a warm yellow-beige, evoking aged telegraph paper. The tape background Y is fixed at high brightness (880–920) so the "paper" always reads as bright.

---

#### Knob 6 — Ink Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Tints the border lines (Ink Hue). The register is divided into four hue regions. Below 256 the border takes a warm amber tint. From 256–511 borders are cyan-shifted. From 512–767 they shift to cool green. Above 768 they become magenta-touched. With borders disabled (Edge Show off), this parameter has no visible effect.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Style** | Ticker | News |
| **8 — Edge Show** | Off | On |
| **9 — Animate** | Off | On |
| **10 — Invert** | Off | On |
| **11 — Bypass** | Off | On |

Switches 7–11 control the style mode, border visibility, scroll animation, luma inversion, and bypass. Style (Switch 7, 2 bits) acts as a combined selector that determines both scroll direction and outside-band dimming intensity. Edge Show, Animate, Invert, and Bypass are independent binary switches.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfade between the unprocessed input (dry) and the fully processed ticker output (wet). At 0% the output is pure dry signal. At 100% the output is fully processed. Intermediate values create a ghost-overlay effect where the quantized band is partially transparent against the original video.





---

## Guided Exercises

These exercises progress from a simple static band to a fully animated scrolling ticker with styled borders and quantized content. Each exercise introduces additional controls to build familiarity with the processing chain.

### Exercise 1: Static Ticker Band

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: ticker_source1_sunset, after: ticker_ex1_s1 },
    { label: "Parrot", before: ticker_source2_parrot, after: ticker_ex1_s2 },
    { label: "Clouds", before: ticker_source3_clouds, after: ticker_ex1_s3 },
    { label: "Pattern", before: ticker_source4_pattern, after: ticker_ex1_s4 },
    { label: "Man", before: ticker_source5_man, after: ticker_ex1_s5 },
    { label: "Wood", before: ticker_source6_wood, after: ticker_ex1_s6 },
  ]}
/>
*Static Ticker Band — simulated result across source images.*
**Source**: A live camera feed or recorded footage with recognizable faces and varying brightness.

**What You'll Create**: Learn how band positioning, height, and quantization interact to create the basic ticker-tape look.

1. **Position the band**: Set Tape Pos to ~50% to center the band vertically on screen.
2. **Set band height**: Choose a moderate height (step 3 or 4, ~50%) for a visible strip.
3. **Observe the band**: Notice the source video inside the band and the dimmed region outside.
4. **Increase quantization**: Slowly increase Contrast from 0% toward 100%. Watch smooth tones inside the band collapse into hard-edged posterized shapes.
5. **Maximum quantization**: At full Contrast, only 2 brightness levels remain — the content becomes purely black-and-white silhouettes resembling printed text.

**Key concepts**: The ticker band is a spatial mask, quantization reduces tonal levels to simulate typography, the band position and height are independently controllable

---

### Exercise 2: Scrolling News Crawl

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: ticker_source1_sunset, after: ticker_ex2_s1 },
    { label: "Parrot", before: ticker_source2_parrot, after: ticker_ex2_s2 },
    { label: "Clouds", before: ticker_source3_clouds, after: ticker_ex2_s3 },
    { label: "Pattern", before: ticker_source4_pattern, after: ticker_ex2_s4 },
    { label: "Man", before: ticker_source5_man, after: ticker_ex2_s5 },
    { label: "Wood", before: ticker_source6_wood, after: ticker_ex2_s6 },
  ]}
/>
*Scrolling News Crawl — simulated result across source images.*
**Source**: A studio camera shot or talking-head video with consistent framing.

**What You'll Create**: Combine scroll animation, border lines, and style modes to create a live news-crawl effect.

1. **Start from Exercise 1 settings** with moderate height and strong quantization.
2. **Enable borders**: Turn Edge Show on. Bright lines frame the band top and bottom.
3. **Enable scroll**: Turn Animate on. The quantized content begins scrolling horizontally.
4. **Adjust speed**: Sweep Tape Spd from low to high. Notice how faster speeds blur the quantized content into streak-like patterns.
5. **Try News style**: Switch Style to News (11). The outside-band dimming disappears — the full source is visible behind the scrolling band.
6. **Try Receipt style**: Switch to Receipt (10). The outside dims to near-black, isolating the band on a dark field.

**Key concepts**: Scroll animation advances a pixel offset per frame, style modes combine dimming and direction, borders anchor the band visually

---

### Exercise 3: Vintage Telegraph Tape

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: ticker_source1_sunset, after: ticker_ex3_s1 },
    { label: "Parrot", before: ticker_source2_parrot, after: ticker_ex3_s2 },
    { label: "Clouds", before: ticker_source3_clouds, after: ticker_ex3_s3 },
    { label: "Pattern", before: ticker_source4_pattern, after: ticker_ex3_s4 },
    { label: "Man", before: ticker_source5_man, after: ticker_ex3_s5 },
    { label: "Wood", before: ticker_source6_wood, after: ticker_ex3_s6 },
  ]}
/>
*Vintage Telegraph Tape — simulated result across source images.*
**Source**: High-contrast black-and-white footage or a graphic test pattern with strong edges.

**What You'll Create**: Use Paper Hue, Ink Hue, Invert, and heavy quantization to evoke a vintage teleprinter aesthetic.

1. **Narrow the band**: Set Tape H to ~25% for a thin strip. Position near center.
2. **Maximum quantization**: Set Contrast to 100% for pure binary output.
3. **Warm paper**: Set Paper Hue to ~80% for warm yellow-beige paper color.
4. **Amber ink**: Set Ink Hue to ~20% for warm amber border lines. Enable Edge Show.
5. **Enable Invert**: Toggle Invert on. The quantization flips — previously dark shapes become bright text on dark paper.
6. **Slow scroll**: Enable Animate with Tape Spd at ~15%. The strip scrolls gently like a telegraph feed.
7. **Mix down**: Lower Mix to ~70% to let the original image ghost through the effect.

**Key concepts**: Paper Hue and Ink Hue tint the band and borders independently, Invert reverses the quantization mapping before all processing, Mix creates a transparency overlay

---


## Tips

- **Invert flips the "ink"**: Invert changes which brightness values read as foreground text and which read as background paper. Dark sources become light "characters" and vice versa.
- **Slow scroll for readability**: Very high Tape Spd values blur the quantized content into horizontal streaks. For the most legible ticker look, keep speed below 30%.
- **Paper Hue upper region for vintage look**: Values above 768 give a warm sepia paper tone that pairs well with amber Ink Hue borders.
- **Mix for layering**: Lowering Mix creates a ghost-overlay effect where the ticker band is partially transparent — useful for compositing multiple Ticker instances in a chain.
- **Feedback loops**: Routing the output back to the input creates recursively quantized content inside the band — the posterized patterns feed back and simplify further on each pass.

---

## Glossary

| Term | Definition |
|------|------------|
| **Band** | The horizontal strip on screen defined by band_top and band_bottom scanline positions, within which quantized content is rendered. |
| **BT.601** | ITU-R Recommendation BT.601, defining standard-definition color encoding with separate luminance (Y) and chrominance (U, V) components. |
| **DDS** | Direct Digital Synthesis; a technique for generating waveforms using a phase accumulator incremented at a fixed rate. |
| **Dimming** | Right-shifting (dividing by powers of 2) the luma value of pixels outside the band to darken them. |
| **Luma** | The brightness component (Y) of a YUV video signal. |
| **Posterization** | Reducing the number of distinct brightness levels, collapsing smooth gradients into flat steps. |
| **Quantization** | Mapping a continuous range of values to a smaller set of discrete levels by truncating lower-order bits. |
| **Sample-and-Hold** | A decimation technique where a single sample value is held constant across multiple pixel positions, creating uniform blocks. |
| **Scroll Offset** | A per-frame horizontal pixel counter that shifts the composite position of the band content to create scrolling animation. |

---
