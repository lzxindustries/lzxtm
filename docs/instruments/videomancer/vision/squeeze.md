---
draft: true
sidebar_position: 285
slug: /instruments/videomancer/squeeze
title: "Squeeze"
image: /img/instruments/videomancer/squeeze/squeeze_hero_s1.png
description: "In the era of analogue broadcast television, a dedicated hardware box called a DVE — Digital Video Effects unit — sat between the camera switcher and the transmitter."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import squeeze_control_panel from '/img/instruments/videomancer/squeeze/squeeze_control_panel.png';
import squeeze_source1_skull from '/img/instruments/videomancer/squeeze/squeeze_source1_skull.png';
import squeeze_source2_fruit from '/img/instruments/videomancer/squeeze/squeeze_source2_fruit.png';
import squeeze_source3_collage from '/img/instruments/videomancer/squeeze/squeeze_source3_collage.png';
import squeeze_source4_pattern from '/img/instruments/videomancer/squeeze/squeeze_source4_pattern.png';
import squeeze_source5_man from '/img/instruments/videomancer/squeeze/squeeze_source5_man.png';
import squeeze_source6_knit from '/img/instruments/videomancer/squeeze/squeeze_source6_knit.png';
import squeeze_hero_s1 from '/img/instruments/videomancer/squeeze/squeeze_hero_s1.png';
import squeeze_hero_s2 from '/img/instruments/videomancer/squeeze/squeeze_hero_s2.png';
import squeeze_hero_s3 from '/img/instruments/videomancer/squeeze/squeeze_hero_s3.png';
import squeeze_hero_s4 from '/img/instruments/videomancer/squeeze/squeeze_hero_s4.png';
import squeeze_hero_s5 from '/img/instruments/videomancer/squeeze/squeeze_hero_s5.png';
import squeeze_hero_s6 from '/img/instruments/videomancer/squeeze/squeeze_hero_s6.png';
import squeeze_ex1_s1 from '/img/instruments/videomancer/squeeze/squeeze_ex1_s1.png';
import squeeze_ex1_s2 from '/img/instruments/videomancer/squeeze/squeeze_ex1_s2.png';
import squeeze_ex1_s3 from '/img/instruments/videomancer/squeeze/squeeze_ex1_s3.png';
import squeeze_ex1_s4 from '/img/instruments/videomancer/squeeze/squeeze_ex1_s4.png';
import squeeze_ex1_s5 from '/img/instruments/videomancer/squeeze/squeeze_ex1_s5.png';
import squeeze_ex1_s6 from '/img/instruments/videomancer/squeeze/squeeze_ex1_s6.png';
import squeeze_ex2_s1 from '/img/instruments/videomancer/squeeze/squeeze_ex2_s1.png';
import squeeze_ex2_s2 from '/img/instruments/videomancer/squeeze/squeeze_ex2_s2.png';
import squeeze_ex2_s3 from '/img/instruments/videomancer/squeeze/squeeze_ex2_s3.png';
import squeeze_ex2_s4 from '/img/instruments/videomancer/squeeze/squeeze_ex2_s4.png';
import squeeze_ex2_s5 from '/img/instruments/videomancer/squeeze/squeeze_ex2_s5.png';
import squeeze_ex2_s6 from '/img/instruments/videomancer/squeeze/squeeze_ex2_s6.png';
import squeeze_ex3_s1 from '/img/instruments/videomancer/squeeze/squeeze_ex3_s1.png';
import squeeze_ex3_s2 from '/img/instruments/videomancer/squeeze/squeeze_ex3_s2.png';
import squeeze_ex3_s3 from '/img/instruments/videomancer/squeeze/squeeze_ex3_s3.png';
import squeeze_ex3_s4 from '/img/instruments/videomancer/squeeze/squeeze_ex3_s4.png';
import squeeze_ex3_s5 from '/img/instruments/videomancer/squeeze/squeeze_ex3_s5.png';
import squeeze_ex3_s6 from '/img/instruments/videomancer/squeeze/squeeze_ex3_s6.png';

# Squeeze

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: squeeze_source1_skull, after: squeeze_hero_s1 },
    { label: "Fruit", before: squeeze_source2_fruit, after: squeeze_hero_s2 },
    { label: "Collage", before: squeeze_source3_collage, after: squeeze_hero_s3 },
    { label: "Pattern", before: squeeze_source4_pattern, after: squeeze_hero_s4 },
    { label: "Man", before: squeeze_source5_man, after: squeeze_hero_s5 },
    { label: "Knit", before: squeeze_source6_knit, after: squeeze_hero_s6 },
  ]}
/>
*Squeeze compressing a live video source into a floating inset rectangle with a bright border and dark background, demonstrating classic DVE picture-in-picture composition.*

---

## Overview

In the era of analogue broadcast television, a dedicated hardware box called a DVE — Digital Video Effects unit — sat between the camera switcher and the transmitter. Its signature move was the *squeeze-back*: shrinking a full-frame video source into a smaller rectangle positioned anywhere on screen, usually with a bright border and a contrasting background. News anchors appeared in floating windows, sports replays hovered over live action, and picture-in-picture became a visual language viewers instinctively understood.

Squeeze recreates that effect entirely in FPGA logic, with zero BRAM. The program classifies every pixel into one of four regions — inset, border, shadow, or background — and composites the appropriate content in real time. The Scale control determines how large the inset rectangle appears (from a tiny stamp to full frame), while Pos X and Pos Y slide it freely across the screen. An optional bright border with configurable brightness frames the inset, and a drop shadow offset by 4 pixels adds a 3D floating appearance. The background can be either a solid luminance level or a dimmed copy of the input video, depending on the Bg Mode toggle.

Because the iCE40 FPGA has no line buffer, Squeeze does not perform true spatial resampling. Instead, the inset window acts as a viewport — pixels inside the inset are taken directly from the input stream at the corresponding position. The visual result is closest to a vintage broadcast DVE: clean geometric framing with pixel-rate boundaries, no anti-aliasing, and the characteristic look of hardware-composited picture-in-picture.

---

## Quick Start

1. **Classic PIP position**: Upper-right (Pos X ~80%, Pos Y ~20%) or lower-right (Pos X ~80%, Pos Y ~80%) are the broadcast standard positions for picture-in-picture.
2. **Border makes the difference**: A thin white border (Border W ~10%, Border Br ~100%) is the most effective way to separate the inset from the background, especially in Dim Vid mode.
3. **Drop shadow for depth**: Enable Shadow for a subtle 3D floating effect. It works best with Border also enabled and a dark background.

---

## Background

### What Is a DVE Squeeze-Back?

The squeeze-back is one of the oldest tricks in broadcast video production. A DVE (Digital Video Effects) unit compresses a full-resolution video signal into a smaller rectangle and positions it within a larger frame. The technology emerged in the late 1970s with units like the Quantel DPE 5000 and the Ampex ADO, which used dedicated frame stores and custom arithmetic hardware to perform real-time scaling and positioning. The name "squeeze" describes the visual impression: the image appears to be squeezed down into a smaller space, as though viewed through a reducing lens. Modern broadcast graphics systems perform the same operation in software, but the aesthetic of the hardware DVE — with its clean geometric edges and absence of anti-aliasing — remains distinctive and recognizable.

### Picture-in-Picture Composition

Picture-in-picture (PIP) is the simplest form of DVE composition: one video source appears as a reduced inset within another. The compositing engine must decide, for every pixel of every frame, which source to display. Squeeze implements this as a spatial classification problem. Each pixel's screen coordinates are tested against the inset rectangle boundaries. Pixels inside the rectangle show the input video; pixels outside show the background. The border is an expanded ring around the inset — a few pixels wider on each side — filled with a uniform brightness level. This region-based approach requires only comparators and multiplexers, no frame memory.

### Borders and Drop Shadows

The bright border around a PIP inset serves a perceptual function: it separates the inset content from the background, making the floating window visually distinct. Without a border, the inset edges can blend into the background when both contain similar brightness levels. Squeeze adds an optional drop shadow — a dark rectangle offset by 4 pixels down and to the right — that creates the illusion of the inset floating above the background plane. This shadow technique is borrowed from graphical user interfaces, where drop shadows are used to indicate depth and layering.

### Background Modes

Squeeze offers two background modes. In Black mode, everything outside the inset and border is filled with a configurable solid luminance level (from black to white). In Dim Vid mode, the background shows a dimmed version of the input video — the same content that appears inside the inset, but attenuated by the Bg Level control. This second mode is the broadcast standard for picture-in-picture: the main programme continues behind the inset window, visually subordinated by the dimming but still visible and contextually connected.

### Wet/Dry Mix

The three interpolator_u instances at the end of the pipeline perform a per-channel linear crossfade between the delayed (dry) input and the composed (wet) output. At Mix = 100%, the output is fully composed — inset, border, shadow, and background are all visible. At Mix = 0%, the output is the unprocessed input. Intermediate values blend the two, producing a semi-transparent overlay effect where the inset and border appear ghosted over the original video.


---

## Signal Flow

Region Classification → Compose Output

```
Input Video (YUV 4:4:4)
│
├── Register Mapping
│   ├─ reg(0) → Scale         (inset size)
│   ├─ reg(1) → Pos X         (horizontal position)
│   ├─ reg(2) → Pos Y         (vertical position)
│   ├─ reg(3) → Border W      (border width)
│   ├─ reg(4) → Border Br     (border brightness)
│   ├─ reg(5) → Bg Level      (background brightness / dim factor)
│   ├─ reg(6)(0) → Aspect     (free / locked)
│   ├─ reg(6)(1) → Bg Mode    (black / dim vid)
│   ├─ reg(6)(2) → Border     (off / on)
│   ├─ reg(6)(3) → Shadow     (off / on)
│   ├─ reg(6)(4) → Bypass
│   └─ reg(7) → Mix
│
├── Derive Inset Rectangle
│   ├─ inset_w = frame_w × scale / 1024
│   ├─ inset_h = frame_h × scale / 1024
│   ├─ inset_x = (frame_w − inset_w) × pos_x / 1024
│   ├─ inset_y = (frame_h − inset_h) × pos_y / 1024
│   └─ border_px = border_w >> 5
│
├── Timing Generator (hsync/vsync → h_count, v_count)
│
├── Stage 1: Region Classification (1 clk)
│   ├─ Test h_count, v_count against inset bounds
│   ├─ Test against border bounds (inset ± border_px)
│   ├─ Test against shadow bounds (border + 4px offset)
│   └─ Classify → region_inset / region_border / region_shadow / region_background
│
├── Stages 2–3: Pass-through (2 clk, reserved for coordinate mapping)
│
├── Stage 4: Compose Output (1 clk)
│   ├─ region_inset     → input Y/U/V
│   ├─ region_border    → border_br Y, neutral U/V
│   ├─ region_shadow    → Y=32, neutral U/V
│   └─ region_background:
│       ├─ Bg Mode = Black   → bg_level Y, neutral U/V
│       └─ Bg Mode = Dim Vid → Y × bg_level / 1024, input U/V
│
├── Stages 5–8: Interpolator Mix (3× channels, 4 clk each)
│   └─ mix = lerp(delayed_input, composed, mix_amount)
│
├── Sync Delay Pipeline (8-clock shift register)
│
└── Output Mux
    ├─ Bypass off → mixed Y/U/V + aligned sync
    └─ Bypass on  → delayed input Y/U/V + aligned sync
```

The core of Squeeze is the region classifier in Stage 1. Every pixel is tested against three nested rectangles: the inset itself, the border ring (inset expanded by border_px on each side), and the shadow (border ring offset by 4 pixels down and right). The priority order is critical: inset wins over border, border wins over shadow, and shadow wins over background. This ensures the input video always appears inside the inset without being overwritten by the border or shadow.

The inset rectangle dimensions are derived from the Scale parameter by multiplying the full frame dimensions (1280×720) by scale/1024. The position is then computed by distributing the remaining space according to Pos X and Pos Y, so that 512 (center) places the inset in the middle of the frame.

---

## Parameter Reference

<img src={squeeze_control_panel} alt="Videomancer front panel with Squeeze loaded"/>
*Videomancer's front panel with Squeeze active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Scale
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

At 100% (register 1023), the inset fills the entire frame and no border or background is visible. At 0% (register 0), the inset shrinks to zero size. The default value of 768 produces an inset roughly 75% of the frame dimensions — large enough to show detail but small enough that the border and background are clearly visible. The scaling is linear: doubling the register value doubles the inset dimensions. At very small values (below 10%), the inset becomes a tiny stamp where individual pixels of the source content are discernible. Internally, controls the size of the inset rectangle as a proportion of the full frame.

---

#### Knob 2 — Pos X
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

At 0%, the inset is flush against the left edge. At 100%, the inset is flush against the right edge. At 50% (register 512, the default), the inset is horizontally centered. The positioning is proportional to the available space, so the visual travel range depends on the Scale setting — a smaller inset has more room to move. Combined with Pos Y, this control allows the inset to be placed in any of the traditional broadcast PIP positions: upper-right, lower-left, center, or anywhere between. Internally, controls the horizontal position of the inset within the frame.

---

#### Knob 3 — Pos Y
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

At 0%, the inset is flush against the top edge. At 100%, the inset is flush against the bottom edge. At 50% (register 512, the default), the inset is vertically centered. This control works identically to Pos X but on the vertical axis. The classic broadcast convention places PIP windows in the upper-right or lower-right corner — approximately 80% on both axes. Internally, controls the vertical position of the inset within the frame.

---

#### Knob 4 — Border W
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 13% |
| Suffix | % |

At 0%, no border is drawn (even if the Border toggle is enabled, zero width produces no visible border). At 100%, the border extends approximately 32 pixels outward from the inset edges. The border width is derived by right-shifting the register value by 5, producing a 0–32 pixel range. The border must be enabled via toggle 9 to be visible. The border is drawn as a solid ring at the brightness set by Border Br, with neutral (gray) chroma. Internally, controls the width of the bright border surrounding the inset rectangle.

---

#### Knob 5 — Border Br
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

At 0%, the border is black — visually invisible against a black background but still present as a region that blocks the background content. At 100%, the border is maximum white. The border colour is always neutral gray (U=512, V=512) regardless of this setting — only the brightness varies. A bright white border against a dark background is the classic broadcast PIP look. Lower values produce a subtler frame that separates the inset from the background without drawing attention to itself. Internally, controls the luminance of the border ring.

---

#### Knob 6 — Bg Level
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 6% |
| Suffix | % |

Controls the background fill level. In Black mode (Bg Mode = Black), this sets the solid luminance value for all pixels outside the inset and border — 0% is pure black, 100% is maximum white. In Dim Vid mode (Bg Mode = Dim Vid), this value is used as a multiplication factor: the input video luminance is multiplied by bg_level/1024, producing a dimmed version of the source. At 0% in Dim Vid mode, the background is black (full attenuation). At 100%, the background shows the input video at full brightness, making the inset invisible unless a border is enabled.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Aspect** | Free | Lock |
| **8 — Bg Mode** | Black | Dim Vid |
| **9 — Border** | Off | On |
| **10 — Shadow** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control independent binary options. Aspect (toggle 7) is reserved for future aspect ratio locking. Bg Mode (toggle 8) selects between solid colour and dimmed video backgrounds. Border (toggle 9) enables or disables the bright border ring around the inset. Shadow (toggle 10) enables or disables the drop shadow offset behind the border. Bypass (toggle 11) overrides everything at the output mux. None of these toggles interact with each other — each controls a single, independent parameter.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfades between the delayed input video (dry) and the composed PIP output (wet). At 0% (fader down), the output is the unprocessed input — no inset, border, or background is visible. At 100% (fader up), the output is the fully composed PIP with all region rendering active. Intermediate values produce a semi-transparent overlay where the inset and border appear ghosted over the original video. The crossfade operates independently on Y, U, and V channels via three interpolator_u instances.



> See [Common Controls & Glossary Reference](../common_reference.md) for details.

---

## Guided Exercises

These exercises progress from basic PIP framing to full broadcast-style composition. Each builds on the previous, gradually engaging more of Squeeze's region rendering and compositing features.

### Exercise 1: Centered Picture-in-Picture

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: squeeze_source1_skull, after: squeeze_ex1_s1 },
    { label: "Fruit", before: squeeze_source2_fruit, after: squeeze_ex1_s2 },
    { label: "Collage", before: squeeze_source3_collage, after: squeeze_ex1_s3 },
    { label: "Pattern", before: squeeze_source4_pattern, after: squeeze_ex1_s4 },
    { label: "Man", before: squeeze_source5_man, after: squeeze_ex1_s5 },
    { label: "Knit", before: squeeze_source6_knit, after: squeeze_ex1_s6 },
  ]}
/>
*Centered Picture-in-Picture — simulated result across source images.*
**Source**: A live camera feed or recorded footage with recognizable subjects and varied brightness.

**What You'll Create**: Learn how Scale, Pos X, and Pos Y interact to create a basic PIP window, and how the border provides visual framing.

1. **Default PIP**: With Scale at ~75%, Pos X at ~50%, and Pos Y at ~50%, observe the centered inset with a border.
2. **Scale down**: Reduce Scale to ~30%. The inset shrinks, revealing more background.
3. **Move to corner**: Set Pos X to ~80% and Pos Y to ~20%. The inset moves to the upper-right — the classic broadcast PIP position.
4. **Remove border**: Toggle Border to Off. Notice how the inset blends into the background without the border frame.
5. **Re-enable border**: Toggle Border back to On. Adjust Border W to ~50% for a thick frame, then to ~10% for a thin line.
6. **Border brightness**: Sweep Border Br from 0% to 100%. Watch the border transition from invisible (black) to bright white.

**Key concepts**: Scale controls inset size proportionally, Pos X/Y position the inset within available space, border provides visual separation, border width and brightness are independent controls

---

### Exercise 2: Drop Shadow and Background Modes

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: squeeze_source1_skull, after: squeeze_ex2_s1 },
    { label: "Fruit", before: squeeze_source2_fruit, after: squeeze_ex2_s2 },
    { label: "Collage", before: squeeze_source3_collage, after: squeeze_ex2_s3 },
    { label: "Pattern", before: squeeze_source4_pattern, after: squeeze_ex2_s4 },
    { label: "Man", before: squeeze_source5_man, after: squeeze_ex2_s5 },
    { label: "Knit", before: squeeze_source6_knit, after: squeeze_ex2_s6 },
  ]}
/>
*Drop Shadow and Background Modes — simulated result across source images.*
**Source**: Footage with clear foreground subjects and varied background colours.

**What You'll Create**: Explore the drop shadow and background mode interactions for broadcast-style composition.

1. **Enable shadow**: Toggle Shadow to On. A dark offset rectangle appears behind the border, creating a floating 3D effect.
2. **Move inset**: Slide Pos X and Pos Y to various positions. Notice how the shadow is always offset down-right from the border.
3. **Switch to Dim Vid**: Toggle Bg Mode to Dim Vid. The background now shows a dimmed version of the input video.
4. **Adjust dimming**: Sweep Bg Level from 0% to ~50%. The background fades from black to a half-brightness copy of the source.
5. **Full background**: Push Bg Level to ~100%. The background shows full-brightness video — the border and shadow are the only visual cues separating the inset from the surrounding content.
6. **Compare modes**: Toggle Bg Mode between Black and Dim Vid. In Black mode, the Bg Level sets a solid gray. In Dim Vid mode, it multiplies the input video luminance.

**Key concepts**: Drop shadow adds depth illusion with 4-pixel offset, Bg Mode selects solid vs dimmed-video background, Bg Level functions differently in each mode (solid value vs multiplication factor)

---

### Exercise 3: Animated PIP Composition

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: squeeze_source1_skull, after: squeeze_ex3_s1 },
    { label: "Fruit", before: squeeze_source2_fruit, after: squeeze_ex3_s2 },
    { label: "Collage", before: squeeze_source3_collage, after: squeeze_ex3_s3 },
    { label: "Pattern", before: squeeze_source4_pattern, after: squeeze_ex3_s4 },
    { label: "Man", before: squeeze_source5_man, after: squeeze_ex3_s5 },
    { label: "Knit", before: squeeze_source6_knit, after: squeeze_ex3_s6 },
  ]}
/>
*Animated PIP Composition — simulated result across source images.*
**Source**: Dynamic footage — sports, music, or fast-moving content.

**What You'll Create**: Combine all Squeeze features for a full broadcast-style multi-layer composition using the Mix fader.

1. **Set up PIP**: Scale ~40%, Pos X ~75%, Pos Y ~75% (lower-right corner).
2. **Full framing**: Border On, Border W ~20%, Border Br ~100%, Shadow On.
3. **Dim background**: Bg Mode = Dim Vid, Bg Level ~15%.
4. **Fade in**: Slowly raise the Mix fader from 0% to 100%. Watch the PIP window fade into view over the full-frame source.
5. **Partial mix**: Set Mix to ~60%. The PIP is semi-transparent — both the composed output and the dry input are visible simultaneously.
6. **Move while mixed**: Sweep Pos X from ~20% to ~80%. The semi-transparent inset glides across the frame.
7. **Scale while mixed**: Sweep Scale from ~20% to ~80%. The semi-transparent inset grows and shrinks smoothly.

**Key concepts**: Mix fader crossfades between dry input and composed PIP, intermediate mix values create transparency, PIP position and scale can be swept dynamically for animated transitions

---


## Tips

- **Dim Vid for context**: Bg Mode = Dim Vid keeps the main programme visible behind the PIP window. Keep Bg Level around 15–25% for the classic broadcast look.
- **Mix for transitions**: Use the Mix fader to fade the PIP in and out smoothly. Sweep from 0% to 100% for a professional-looking PIP reveal.
- **Scale for emphasis**: A larger inset (Scale ~70–80%) makes the PIP content the focus; a smaller inset (Scale ~25–35%) subordinates it to the background.
- **Feedback routing**: Routing Squeeze's output back to its input creates recursive PIP — a shrinking series of nested rectangles receding toward the vanishing point.
- **Bypass for comparison**: Toggle Bypass for instant before/after comparison between the composed PIP and the clean source.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bg Mode** | Background mode: selects between a solid luminance fill and a dimmed copy of the input video for pixels outside the inset. |
| **Border** | A ring of pixels at configurable brightness drawn around the inset rectangle to provide visual separation from the background. |
| **Compositing** | The process of combining multiple visual elements (inset, border, shadow, background) into a single output frame. |
| **Drop Shadow** | A dark offset rectangle drawn behind the inset border to create the illusion of the window floating above the background plane. |
| **DVE** | Digital Video Effects; a dedicated hardware unit for real-time video scaling, positioning, and compositing, used extensively in broadcast television from the late 1970s onward. |
| **PIP** | Picture-in-Picture; a video composition technique where one source appears as a reduced inset within another. |
| **Region Classification** | The per-pixel process of determining whether a pixel falls inside the inset, border, shadow, or background region based on its screen coordinates. |
| **Squeeze-Back** | The broadcast term for compressing a full-frame video source into a smaller inset rectangle, named for the visual impression of the image being squeezed down. |

For common terms (YUV, FPGA, BRAM, Pipeline, etc.) see the [Common Glossary](../common_reference.md#common-glossary).

---
