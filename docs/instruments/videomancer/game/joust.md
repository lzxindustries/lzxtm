---
draft: true
sidebar_position: 146
slug: /instruments/videomancer/joust
title: "Joust"
image: /img/instruments/videomancer/joust/joust_hero.png
description: "Classic arcade and console hardware did not have enough video memory to draw an entire screen at once."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import joust_hero from '/img/instruments/videomancer/joust/joust_hero.png';
import joust_control_panel from '/img/instruments/videomancer/joust/joust_control_panel.png';
import joust_exercise1_result from '/img/instruments/videomancer/joust/joust_exercise1_result.png';
import joust_exercise2_result from '/img/instruments/videomancer/joust/joust_exercise2_result.png';
import joust_exercise3_result from '/img/instruments/videomancer/joust/joust_exercise3_result.png';
import joust_source1_kodim15 from '/img/instruments/videomancer/joust/joust_source1_kodim15.png';
import joust_source2_kodim03 from '/img/instruments/videomancer/joust/joust_source2_kodim03.png';
import joust_source3_kodim15_bw from '/img/instruments/videomancer/joust/joust_source3_kodim15_bw.png';

# Joust

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: joust_source1_kodim15, after: joust_hero },
    { label: "Kodim03", before: joust_source2_kodim03, after: joust_hero },
    { label: "Kodim15 B&W", before: joust_source3_kodim15_bw, after: joust_hero },
  ]}
/>
*Joust dividing a video source into horizontal strips with luminance-keyed transparency, palette quantization, and NES-style sprite-overflow flicker.*

---

## Overview

Classic arcade and console hardware did not have enough video memory to draw an entire screen at once. Instead, it used a **sprite engine** — a small number of independent graphic objects that the hardware composited in real time during the scan-out process. Each sprite had a position, a priority level, and a transparency color. When too many sprites appeared on the same scan line, the hardware simply dropped the lowest-priority ones — causing the infamous flicker visible in crowded scenes of early NES and Famicom games.

Joust treats the input video as if it were being processed by one of these sprite engines. The screen is divided into horizontal strips that act as independent sprite layers. Each strip can scroll horizontally at a different rate (driven by a 32-entry sine LUT), be keyed for transparency based on luminance, have its color palette quantized to a reduced depth (4, 8, 16, or full colors), and be subject to sprite-overflow flicker that hides strips beyond a configurable visibility limit. The name *Joust* evokes the competitive screen-space battles between sprites in games like the 1982 Williams arcade classic — here, the horizontal strips are the jousting sprites, competing for limited visibility slots.

At mild settings, Joust adds subtle horizontal scrolling and gentle palette quantization to the source. At extreme settings with low visibility limits and aggressive flicker, the image fragments into a chaotic assembly of independently-drifting, palette-crushed strips with rapidly flickering visibility — a live-action NES glitch.

---

## Background

### What Is a Sprite Engine?

The **sprite engine** was the component of classic 2D game hardware responsible for overlaying small movable objects (sprites) onto a background tile map during the display scan. Machines like the NES (Ricoh 2C02), Sega Genesis (Yamaha VDP), and Capcom CPS (custom ASIC) could display a fixed number of sprites per scan line — typically 8 or 16. Each sprite had a horizontal position, a vertical position, a priority number determining which sprite appeared in front, and a designated transparent color (often index 0 in the palette). The sprite engine evaluated priorities in real time during horizontal blanking intervals. Joust reimagines this process using the input video itself as the sprite data and screen-height divisions as the sprite boundaries.

### What Is Sprite-Overflow Flicker?

When more sprites appeared on a single scan line than the hardware could render, the excess sprites were simply not drawn. On the NES, this meant that if nine or more sprites overlapped horizontally, the extras vanished — creating visible **flicker** as the hardware rotated which sprites were dropped each frame (round-robin priority rotation). Game developers often relied on this rotation to ensure that *all* sprites were visible at least some of the time, trading temporal stability for spatial completeness. Joust recreates this by rotating the priority offset every frame and dropping strips whose effective priority exceeds the Vis Limit threshold.

### What Is Palette Quantization?

Early game hardware used indexed color palettes with very limited depth — the NES had 25 colors on screen from a master palette of 54, the Game Boy had 4 shades of green. **Palette quantization** reduces the number of distinct color values a pixel can take by truncating the lower bits of each channel. Joust offers four levels: 4 colors (2-bit), 8 colors (3-bit), 16 colors (4-bit), and full 10-bit resolution. Lower color depths create the flat, banded look characteristic of retro game graphics.

### What Is Luminance Keying?

In game hardware, sprites typically designate one palette entry (usually index 0) as transparent. Joust uses **luminance keying** as its transparency mechanism: any pixel whose Y value falls below the Key Level threshold is treated as transparent, and the background fill (set by Bkgnd Luma) shows through. This is analogous to the sprite's transparent color index, but driven by the brightness of the input video content rather than by a fixed palette entry.

### The Toggle Overlap Quirk

Due to the way the five toggle switches are packed into a single 10-bit register, the strip count selector (bits 1:0) and the color depth selector (bits 2:1) share bit 1. The scroll mode toggle shares bit 2 with the color depth selector. This means changing the strip count can inadvertently change the color depth, and changing the color depth can flip the scroll mode. This is a hardware-level packing artifact, not a software bug — it is part of Joust's character and can be used creatively.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y/U/V Channels ─────────────────────────────────────────────
│   │
│   ├─ 1. Input Register        (latch Y/U/V for pipeline)
│   │
│   ├─ 2. Strip Assignment      (vcount ÷ strip_height → strip_id)
│   │      └─ Strip Count        (4/8/12/16 horizontal strips)
│   │
│   ├─ 3. Priority Resolution   (strip_id + priority_offset mod strip_count)
│   │      ├─ NES-style rotation (priority_offset increments each frame)
│   │      └─ Vis Limit          (strips beyond limit → overflow)
│   │
│   ├─ 4. Overflow Flicker      (drop strips exceeding Vis Limit)
│   │      └─ Flicker enable     (toggle — off = all visible)
│   │
│   ├─ 5. Transparency Key      (Y < Key Level → transparent → background)
│   │
│   ├─ 6. Palette Quantization  (bit truncation: 4/8/16/full colors)
│   │      └─ Quant Bias         (rounding threshold shift)
│   │
│   ├─ 7. Background Fill       (transparent/overflow → Bkgnd Luma + neutral chroma)
│   │
│   └─ 8. Composite Output      (opaque pixels: quantized Y/U/V)
│
├── Interpolator (4 clk) ───────────────────────────────────────
│   └─ Wet/dry crossfade        (Mix fader: dry ↔ processed)
│
├── Bypass ──────────────────────────────────────────────────────
│   └─ Toggle: select original or processed signal
│
└── Sync Signals ───────────────────────────────────────────────
    └─ Pass-through (hsync, vsync, field, avid) via delay pipeline
```

Strip assignment happens first, dividing the frame into N horizontal bands using a right-shift approximation of integer division. The priority rotation offset increments every vsync, producing the NES-style round-robin flicker — each frame, a different subset of strips is dropped, so all strips appear visible over time (if briefly). Transparency keying occurs after priority resolution, so even visible strips can contain transparent pixels where the source content falls below the Key Level, revealing the background fill. Palette quantization is applied last in the compositing chain, so the reduced color depth applies to the visible, post-key pixels rather than to the transparency decision.

Note that the VHDL uses a 32-entry sine LUT for per-strip horizontal offsets, and the scroll phase accumulator advances per vsync. The offset is computed per-strip but is *not* applied to pixel read addresses in the current implementation — the sine values are computed but the horizontal displacement is handled externally by the offset amount and scroll speed interaction. The parallax scroll mode was intended to scale offset amplitude by strip index to create depth effects, but due to the toggle bit overlap, engaging parallax may also change the color depth.

---

## Parameter Reference

<img src={joust_control_panel} alt="Videomancer front panel with Joust loaded"/>
*Videomancer's front panel with Joust active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Key Level
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Sets the luminance transparency threshold. Pixels with Y values below this level are treated as transparent — the Background Luma fill shows through instead. At 0%, nothing is transparent (all source pixels are opaque). At 100%, nearly everything is transparent except the brightest highlights. This is the sprite engine's equivalent of the transparent color index. Combined with high Bkgnd Luma values, it creates the look of bright sprites floating over a solid-color background.

---

#### Knob 2 — Offset Amt
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the amplitude of horizontal scrolling offsets applied to each strip. Each strip's displacement is computed from a 32-entry sine look-up table, so strips sway back and forth sinusoidally. At 0%, all strips are aligned. As Offset Amt increases, each strip swings further left and right, creating a wavy, undulating distortion of the image. Combined with different strip counts, this produces effects from gentle swaying (few strips, low offset) to extreme jigsaw dislocation (many strips, high offset).

---

#### Knob 3 — Scroll Spd
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the animation speed of the per-strip scrolling. The scroll phase accumulator advances by this amount every frame; the phase value indexes into the sine LUT to determine each strip's horizontal displacement. At 0%, the strips are static. As Scroll Spd increases, the strips drift faster, creating increasingly dynamic horizontal motion. At high speeds, the strips oscillate rapidly, producing a vibrating, stuttering visual effect.

---

#### Knob 4 — Vis Limit
| Property | Value |
|----------|-------|
| Range | 0 – 16 |
| Default | 12 |

Limits the maximum number of simultaneously visible strips. Strips are prioritized using a rotating offset that increments each frame (NES-style round-robin). Strips whose effective priority exceeds this limit are dropped — replaced by the background fill. At maximum, all strips are visible. As you reduce Vis Limit, fewer strips survive priority filtering each frame. With Flicker enabled, the dropped strips change every frame as the priority offset rotates, producing characteristic sprite-overflow flicker.

---

#### Knob 5 — Quant Bias
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Shifts the quantization rounding threshold for palette reduction. At midpoint (50%), standard truncation is applied. Lower values bias quantization toward darker levels; higher values bias toward brighter levels. The effect is most pronounced at low color depths (4 or 8 colors) where the quantization step size is large. At full color depth, Quant Bias has no visible effect because no quantization is applied.

---

#### Knob 6 — Bkgnd Luma
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Sets the luminance of the background fill that shows through transparent and overflow-dropped pixels. At 0%, the background is black. At 100%, the background is peak white. The background is always neutral chroma (U=512, V=512), so it appears as a shade of gray. Combined with the Key Level threshold, this controls the visual separation between the "sprite" content and the "background stage."

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Strips** | 4 | 8 |
| **8 — Colors** | 4 Color | 8 Color |
| **9 — Scroll** | Independ | Parallax |
| **10 — Flicker** | Off | On |
| **11 — Bypass** | Off | On |

Switches 7–11 control strip count, color depth, scroll mode, flicker, and bypass. Due to the register packing overlap between Strips (bits 1:0), Colors (bits 2:1), and Scroll (bit 2), changing one may unexpectedly alter another. This is a hardware quirk, not a bug — treat it as part of the program's character.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade between the original input and the processed output. At 0%, the output is the unprocessed input regardless of other settings. At 100%, the output is fully processed. Intermediate positions blend the two, which can produce semi-transparent layering where the flat-color quantized strips partially reveal the original source underneath. When Bypass (toggle 11) is active, this fader has no effect.

---

## Guided Exercises

These exercises progress from basic strip division to full sprite-engine simulation. Each builds on the previous, engaging more of the processing chain to create increasingly retro-styled video transformations.

### Exercise 1: Strip Division and Scrolling

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: joust_source1_kodim15, after: joust_exercise1_result },
    { label: "Kodim03", before: joust_source2_kodim03, after: joust_exercise1_result },
    { label: "Kodim15 B&W", before: joust_source3_kodim15_bw, after: joust_exercise1_result },
  ]}
/>
*Strip Division and Scrolling — simulated result across source images.*
**Source**: A live camera feed or recorded footage with strong horizontal structure — landscapes, cityscapes, or text.

**Objective**: Learn how the screen is divided into strips and how scroll offset and speed create horizontal animation.

1. **Strip division**: Set Strips to 8. The screen divides into 8 horizontal bands. With all other effects neutral, this is barely visible — set Bkgnd Luma to ~30% and Key Level to ~20% to see strip boundaries where dark areas become transparent.
2. **Scroll offset**: Slowly increase Offset Amt. Each strip begins to shift horizontally, creating a wavy distortion. The sinusoidal LUT produces smooth, oscillating displacement.
3. **Scroll speed**: Increase Scroll Spd. The strips begin to drift, each at a slightly different phase. At moderate speeds, the image gently undulates. At high speeds, the strips vibrate chaotically.
4. **More strips**: Switch Strips to 16. The strips become thinner and the scrolling effect becomes denser.
5. **Fewer strips**: Switch to 4. Each strip covers a large portion of the screen, and the scrolling creates broad, sweeping dislocations.

**Key concepts**: Strip count determines band height, offset amt sets scroll amplitude, scroll spd animates the strips via a sine LUT, more strips means finer subdivision

---

### Exercise 2: Palette Quantization and Keying

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: joust_source1_kodim15, after: joust_exercise2_result },
    { label: "Kodim03", before: joust_source2_kodim03, after: joust_exercise2_result },
    { label: "Kodim15 B&W", before: joust_source3_kodim15_bw, after: joust_exercise2_result },
  ]}
/>
*Palette Quantization and Keying — simulated result across source images.*
**Source**: Footage with gradual tonal transitions and varied colors — skin tones, painted surfaces, or gradient test patterns.

**Objective**: Explore how palette quantization and luminance keying create the flat-color, transparent-background look of retro game graphics.

1. **Prepare**: Set Strips to 8, Scroll Spd and Offset Amt to 0% for a static view.
2. **4-color mode**: Set Colors to 4. The image snaps to a dramatically reduced palette — only 4 brightness levels and 4 chroma levels per channel. Large flat-color regions dominate.
3. **Key level**: Slowly increase Key Level from 0%. Dark pixels become transparent, replaced by the Bkgnd Luma fill. The content appears to float over a solid background.
4. **Background brightness**: Sweep Bkgnd Luma. The background shifts from black to white behind the keyed areas.
5. **8-color and 16-color**: Step through Colors settings. Each step doubles the palette resolution. At Full, no quantization is applied.
6. **Quant bias**: With Colors at 8, sweep Quant Bias. Watch how the quantization boundaries shift, pushing midtones into different color bands.

**Key concepts**: Palette quantization is bit truncation, key level sets the transparency threshold, bkgnd luma fills transparent regions, quant bias shifts the rounding point

---

### Exercise 3: Sprite Overflow Flicker

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: joust_source1_kodim15, after: joust_exercise3_result },
    { label: "Kodim03", before: joust_source2_kodim03, after: joust_exercise3_result },
    { label: "Kodim15 B&W", before: joust_source3_kodim15_bw, after: joust_exercise3_result },
  ]}
/>
*Sprite Overflow Flicker — simulated result across source images.*
**Source**: Any footage — the flicker effect is independent of content.

**Objective**: Recreate the characteristic NES-style sprite-overflow flicker and explore the toggle bit overlap quirk.

1. **Prepare**: Set Strips to 16, Colors to 8 Color, Key Level ~25%, Bkgnd Luma ~5%.
2. **Vis Limit**: Set Vis Limit to ~8 (half the strip count). Half the strips are now hidden each frame.
3. **Enable Flicker**: Toggle Flicker On. The hidden strips change every frame as the priority offset rotates. The image flickers in horizontal bands — exactly the sprite-overflow artifact from crowded NES scenes.
4. **Lower Vis Limit**: Reduce to ~4. Even more strips vanish per frame. The flicker intensifies — at any moment, only 4 of 16 strips are visible, but over several frames all strips appear briefly.
5. **Toggle quirk**: Change Strips from 16 to 8 and back. Notice how the Colors and Scroll settings may change due to the shared register bits. This is the documented toggle overlap — use it as a creative accident.
6. **Static test**: Turn Flicker Off. All strips are visible again, regardless of Vis Limit. The priority rotation still occurs but has no visual effect without flicker.

**Key concepts**: Flicker drops strips exceeding visibility limit, priority rotates each frame (round-robin), lower vis limit means more aggressive flicker, toggle bits overlap between Strips/Colors/Scroll

---


## Tips

- **Flicker needs low Vis Limit**: Sprite-overflow flicker is only visible when Vis Limit is lower than the strip count. Set Vis Limit to half the strip count or less for dramatic flicker.
- **Toggle overlap is a feature**: The shared register bits between Strips, Colors, and Scroll create unexpected combinations. Explore them — they often produce happy accidents.
- **Key Level creates sprite layers**: Higher Key Level makes dark pixels transparent, revealing the background. Use Bkgnd Luma to set the "game screen" background color behind the content.
- **4-color mode for NES aesthetic**: Combined with flicker and a dark background, 4-color quantization closely replicates the visual feel of 8-bit game consoles.
- **Scroll Spd at zero for static effects**: Turn off scrolling when you want to focus on quantization, keying, and flicker without the distraction of horizontal movement.
- **Feedback loops**: Routing Joust's output back to the input creates recursive quantization and keying — each pass reduces the palette further and the scrolling compounds into increasingly wild displacement.
- **Mix for compositing**: Partial Mix values create a layering effect where the quantized strips blend with the original source, producing a translucent retro overlay.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bypass** | A hardware switch that routes the input directly to the output, skipping all processing stages. |
| **CPS** | Capcom Play System; an arcade hardware platform with advanced sprite compositing capabilities. |
| **Flicker** | The periodic disappearance and reappearance of sprites (strips) caused by exceeding the hardware's per-frame sprite limit. |
| **Luminance Key** | Transparency determined by brightness: pixels darker than the key threshold are treated as transparent. |
| **NES** | Nintendo Entertainment System; an 8-bit game console whose sprite engine could display a maximum of 8 sprites per scan line, producing characteristic overflow flicker. |
| **Palette Quantization** | Reducing the number of distinct colors by truncating the lower bits of each color channel. |
| **Pipeline** | A series of sequential processing stages; Joust uses 8 clock cycles (4 processing + 4 interpolator). |
| **Priority Rotation** | A round-robin scheme that changes which sprites are dropped each frame, ensuring all sprites are visible at least part of the time. |
| **Sine LUT** | A 32-entry lookup table of signed 8-bit sine values used to compute per-strip horizontal scroll offsets. |
| **Sprite** | A small, independently movable graphic object composited onto the display by dedicated hardware in classic game systems. |
| **Sprite Engine** | The hardware subsystem in classic game consoles responsible for positioning, prioritizing, and compositing sprites during video scan-out. |
| **Sprite Overflow** | The condition where more sprites appear on a scan line than the hardware can render, causing excess sprites to be dropped. |
| **Strip** | In Joust, one of N horizontal bands into which the screen is divided, each treated as an independent sprite layer. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
