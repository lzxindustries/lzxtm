---
draft: true
sidebar_position: 255
slug: /instruments/videomancer/telegram
title: "Telegram"
image: /img/instruments/videomancer/telegram/telegram_hero.png
---

import telegram_before_after from '/img/instruments/videomancer/telegram/telegram_before_after.png';
import telegram_control_panel from '/img/instruments/videomancer/telegram/telegram_control_panel.png';
import telegram_exercise1_result from '/img/instruments/videomancer/telegram/telegram_exercise1_result.png';
import telegram_exercise2_result from '/img/instruments/videomancer/telegram/telegram_exercise2_result.png';
import telegram_exercise3_result from '/img/instruments/videomancer/telegram/telegram_exercise3_result.png';
import telegram_hero from '/img/instruments/videomancer/telegram/telegram_hero.png';
import telegram_source1_kodim15 from '/img/instruments/videomancer/telegram/telegram_source1_kodim15.png';
import telegram_source2_kodim15_bw from '/img/instruments/videomancer/telegram/telegram_source2_kodim15_bw.png';
import telegram_source3_male_1024 from '/img/instruments/videomancer/telegram/telegram_source3_male_1024.png';

# Telegram

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={telegram_hero} alt="Telegram hero image"/>
*Telegram rendering Morse code dot-dash patterns from source luminance as scrolling horizontal bars across configurable tape bands.*
<img src={telegram_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Telegram applied.*

---

## Overview

Before digital communication, before fax machines, before even the telephone reached most of the world, there was the telegraph. Messages reduced to a binary code — short and long pulses, dots and dashes — clicking across copper wire at the speed of light. Telegram takes that same principle and applies it to live video: the brightness of the source image is encoded into a visual Morse-like rhythm of bright dots and dashes scrolling across the screen.

The program samples the input luminance at regular intervals along horizontal scan bands. Bright source regions produce wide bars (dashes); dark regions produce narrow bars (dots). These bars scroll horizontally across the frame on configurable vertical "tape lines" — evocative of the paper strips that spooled out of telegraph receivers. Between the tape bands, the source video is dimmed to create visual separation. The result is a video signal that has been translated into a rhythmic pulse language, a machine reading of brightness rendered as telegraphy.

At subtle settings — low density, wide tape spacing, moderate speed — Telegram adds a gentle ticker-tape overlay to the source image. At extreme settings — high density, narrow spacing, fast scroll — the entire frame becomes a rushing wall of encoded brightness, an abstraction of the source reduced to pure on-off visual rhythm.

---

## Background

### Morse Code and Telegraphy

Samuel Morse's telegraph code, standardized in the 1840s, represented each letter of the alphabet as a sequence of short pulses (dots, or "dits") and long pulses (dashes, or "dahs"). A dash is conventionally three times the length of a dot. The space between elements within a character is one dot length; between characters, three dot lengths; between words, seven. Telegram borrows this temporal structure — the distinction between narrow and wide — but applies it to spatial brightness rather than temporal electrical pulses. Each "character" is determined by the input luminance at the symbol sampling point.

### DDS-Based Timing

The symbol timing in Telegram is driven by a Direct Digital Synthesis (DDS) phase accumulator. On each frame, the accumulator adds an increment determined by the Speed control. The accumulated phase sets the horizontal scroll offset, causing the dot-dash pattern to slide across the screen. The phase accumulator wraps naturally at its bit width, producing continuous cyclic scrolling with no discontinuity. The symbol period — how many pixels wide each dot-or-dash cell is — is set by a power-of-two shift, giving period options of 8, 16, 32, 64, or 128 pixels.

### Tape Band Architecture

Rather than covering the entire frame uniformly, Telegram divides the vertical axis into alternating "tape" and "gap" bands. Only pixels within tape bands display the Morse pattern; gap pixels show the source video dimmed to 25% brightness. The tape spacing is controlled by a shift register, giving band heights of 8, 16, 32, 64, or 128 lines. This creates the visual rhythm of a telegraph tape — parallel strips of encoded information separated by blank margins.

### Luminance-Driven Encoding

At each symbol boundary (where the horizontal phase wraps to zero), Telegram samples the input luminance and compares it to a threshold. Bright source regions (Y > 512 on a 10-bit scale) produce dashes — wide bars that fill most of the symbol cell. Dark regions produce dots — narrow bars that occupy a smaller fraction. This creates a direct visual encoding of the source brightness structure: areas of the video with high contrast create rapid alternation between dots and dashes, while uniform areas produce repetitive patterns.

### Color Modes and Compositing

The bars can render in two color modes. White mode produces neutral luminance bars (achromatic). Amber mode shifts the chroma to create warm-toned bars reminiscent of the amber phosphor displays used in early computer terminals and telegraph teletype machines. The composited output replaces active bar pixels with the bar color at the configured brightness level, while non-bar regions (gaps between symbols and off-tape areas) show the source video dimmed to one-quarter brightness to maintain visual separation.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Timing & Counters ────────────────────────────────────────
│   ├─ H/V pixel counters
│   └─ Per-frame scroll offset (DDS phase accumulator)
│
├── Parameter Derivation ─────────────────────────────────────
│   ├─ Speed → symbol period shift (3–7 → 8–128 px)
│   ├─ Pitch → tape band spacing shift (3–7 → 8–128 lines)
│   ├─ Density → dash bar width (0–63 px)
│   └─ Contrast → dot bar width (0–31 px)
│
├── Pipeline ─────────────────────────────────────────────────
│   │
│   ├─ Stage 1: Input register + scroll offset →
│   │           symbol phase + luma threshold → dash/dot flag
│   │           + tape band region test
│   │
│   ├─ Stage 2: Bar width select (dash or dot width) →
│   │           in-bar test (phase < width?)
│   │
│   ├─ Stage 3: Bar rendering (white or amber color) +
│   │           source dimming for off-tape/gap regions
│   │
│   └─ Stage 4: Final composite
│                (active → bar color, inactive → dimmed source)
│
├── Mix ──────────────────────────────────────────────────────
│   └─ Interpolator: dry (original) ↔ wet (composite)
│       NOTE: Mix is on Pot 6, not the fader
│
├── Contrast / Brightness (proc_amp) ─────────────────────────
│   └─ (contrast_reg − 512) × Y / 512 + brightness_reg
│
├── Invert (optional) ────────────────────────────────────────
│
├── Sync Signals ─────────────────────────────────────────────
│   └─ 8-clock delay shift registers (hsync, vsync, field)
│
└── Bypass ───────────────────────────────────────────────────
    └─ Select original or processed signal
```

Two aspects set Telegram apart from a simple stripe generator. First, the **luma-driven encoding**: the dot-versus-dash decision is made by sampling the source brightness at each symbol boundary, so the Morse pattern is not random — it is a direct spatial encoding of the input video's tonal structure. Panning the source or changing the scene content changes the pattern in real time. Second, the **non-standard mix location**: the wet/dry crossfade is on Pot 6 rather than the fader, freeing the fader for the Tone control that sets the overall intensity of the Morse overlay elements.

---

## Parameter Reference

<img src={telegram_control_panel} alt="Videomancer front panel with Telegram loaded"/>
*Videomancer's front panel with Telegram active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the DDS rate for Morse timing — how quickly the dot-dash pattern scrolls horizontally. At low values, the symbol period is short (8 pixels) and the pattern is fine-grained, creating dense columns of dots and dashes. At high values, the symbol period is long (128 pixels) and each symbol occupies a wide horizontal stripe. The speed control also affects how quickly the pattern scrolls across the frame when sync is set to free-running mode.

---

#### Knob 2 — Dash Len
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the vertical position and spacing frequency of the tape bands. At low values, the bands are closely spaced (8 lines per band), creating many thin horizontal stripes across the frame. At high values, the bands are widely spaced (128 lines), creating a few bold tape strips with large gaps between them. The pitch control determines how much of the frame is covered by Morse data versus dimmed source passthrough.

---

#### Knob 3 — Dot Size
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls how many of the available tape bands are active. At 0%, no bands are visible and the output is the dimmed source. As density increases, more tape bands become active from the top of the frame downward. At 100%, all available bands display the Morse pattern, filling the frame with encoded brightness data. Density and Pitch work together — Pitch sets the size and spacing of bands while Density determines how many of them are "turned on."

---

#### Knob 4 — Lines
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Processing amplifier contrast applied after the Morse compositing stage. At 50%, the signal passes at unity gain. Values below 50% compress the dynamic range, reducing the visual distinction between Morse bars and background. Values above 50% expand the contrast, making the dot-dash pattern stand out more sharply against the dimmed source regions.

---

#### Knob 5 — Sensitiv
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Processing amplifier brightness offset applied after the Morse compositing stage. At 50%, no offset is added. Lower values darken the entire output; higher values brighten it. This control shifts the overall luminance level of both the Morse bars and the dimmed background, which can be used to match the output level to the rest of a video chain.

---

#### Knob 6 — Clr
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Wet/dry crossfade between the original input video and the Morse-composited output. This is a non-standard control placement — the mix is on Pot 6 rather than the fader. At 0%, the output is the unprocessed source. At 100%, the full Morse overlay with dimmed backgrounds is applied. Intermediate values create a blend where the Morse pattern is a translucent overlay on the original video.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Mode** | Morse | Baudot |
| **8 — Display** | Horiz | Vert |
| **9 — Color** | Amber | Green |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control rendering style, source selection, timing synchronization, luminance inversion, and bypass. Mode determines the visual rendering of the Morse pattern. Source selects whether the dash/dot encoding comes from input luma or from a random noise generator. Sync locks the scroll to the frame rate or lets it free-run. Invert and Bypass are standard processing toggles.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the tone overlay intensity — the brightness level of the Morse bar elements. At 0%, the bars are black (invisible against the dimmed background). At 50%, the bars are at medium brightness. At 100%, the bars are at full white (or amber, depending on the color mode). This control sets the visual prominence of the Morse pattern independently of the Mix control. Tone modulates the brightness of the Morse "on" pixels before the mix stage composites them with the source.

---

## Guided Exercises

These exercises progressively build from simple Morse overlay recognition to complex signal-chain interactions, demonstrating how Telegram transforms brightness information into visual telegraphy.

### Exercise 1: Basic Telegraph Tape

<img src={telegram_exercise1_result} alt="Basic Telegraph Tape result"/>
*Basic Telegraph Tape — simulated result across source images.*
**Source**: A camera feed or image with clear areas of light and dark — a human face, text document, or high-contrast scene.

**Objective**: Understand the basic dot/dash encoding and tape band structure.

1. **Set the overlay**: Ensure Mode is Dot, Source is Video, and Bypass is Off.
2. **Open the mix**: Set Mix (Pot 6) to ~75%. The Morse pattern should be clearly visible over the dimmed source.
3. **Set Tone to ~80%** so the bars are bright against the dimmed background.
4. **Adjust Speed**: Sweep from low to high. Watch the symbol period change — small speed creates fine-grained dot patterns; large speed creates wide bars.
5. **Adjust Pitch**: Sweep from low to high. The tape bands change from many thin stripes to a few bold strips.
6. **Adjust Density**: Sweep from 0% to 100%. Watch tape bands activate one by one from top to bottom.

**Key concepts**: Symbol period determines dot/dash resolution, tape bands create the strip structure, density controls how many bands are visible, tone controls bar brightness

---

### Exercise 2: Luma-Driven Encoding

<img src={telegram_exercise2_result} alt="Luma-Driven Encoding result"/>
*Luma-Driven Encoding — simulated result across source images.*
**Source**: A scene with gradual brightness transitions — a gradient test pattern or a face lit from one side.

**Objective**: Observe how source luminance drives the dot/dash decision and creates a spatial encoding of brightness.

1. Start from Exercise 1 settings with moderate Speed and Pitch.
2. **Watch the bright areas**: Bright source regions should produce dashes (wide bars). Dark regions should produce dots (narrow bars).
3. **Slowly move the source** (if using a camera) and observe how the Morse pattern updates in real time as brightness regions shift.
4. **Switch Source to Noise** (Toggle 8 → Noise): The pattern becomes random — no correspondence to the source brightness. Compare with Video mode.
5. **Switch back to Video mode** and try Sync → Lock: The pattern freezes, updating once per frame instead of scrolling.

**Key concepts**: Video mode encodes brightness as dot/dash width, Noise mode generates random patterns, Lock mode creates a frozen snapshot of the current encoding

---

### Exercise 3: Full Transmission

<img src={telegram_exercise3_result} alt="Full Transmission result"/>
*Full Transmission — simulated result across source images.*
**Source**: Any dynamic footage with varying brightness — music performance, nature, or abstract video feedback.

**Objective**: Combine all controls for a dense, animated telegraph-tape composition.

1. Set Speed to ~30% for fine-grained symbols.
2. Set Pitch to ~25% for many closely spaced tape bands.
3. Set Density to 100% to activate all bands across the full frame.
4. Set Mode to Line for continuous ticker-tape appearance.
5. Set Source to Video for luma-driven encoding.
6. Set Sync to Free for continuous scrolling animation.
7. Push Contrast to ~70% and Brightness to ~55% for punchy output.
8. Set Tone to ~90% for bright, prominent Morse bars.
9. Set Mix to 100% for full Telegram effect.
10. Try Invert On — the bars become dark against a bright background, creating a photographic negative of the telegraph pattern.

**Key concepts**: High density and low pitch create full-frame coverage, contrast/brightness shape the final dynamic range, invert reverses the visual polarity of the entire composition

---


## Tips

- **Pot 6 is the mix**: Unlike most Videomancer programs, Telegram places the wet/dry crossfade on Pot 6 rather than the fader. The fader controls Tone (bar brightness) instead. Remember this when setting up the patch.
- **Video mode reveals source structure**: In Video mode, the dot/dash pattern is a direct encoding of the source luminance. Bright areas produce dashes, dark areas produce dots. This creates a visual readout of the source's tonal map.
- **Noise mode for texture**: Switch to Noise mode when you want abstract rhythmic patterns with no connection to the source content. The LFSR generates pseudo-random sequences that create organic, grain-like textures within the tape bands.
- **Pitch and Density interact**: Pitch sets the size and spacing of tape bands; Density controls how many are active. For full-frame coverage, use low Pitch (many narrow bands) and high Density. For a subtle ticker-tape overlay, use high Pitch (few wide bands) and low Density.
- **Lock mode for still analysis**: Setting Sync to Lock freezes the scroll and creates a static Morse pattern. This is useful for examining the luma encoding at specific positions in the frame.
- **Contrast shapes the final punch**: The proc_amp contrast stage after compositing can dramatically change the visual impact. High contrast makes the Morse bars pop sharply against the background; low contrast creates a subtle, washed-out overlay.
- **Invert for reversed polarity**: Enabling Invert after a fully composed Telegram creates a striking reversed-video look where the Morse bars appear as dark gaps in a bright field.
- **Feedback creates recursive encoding**: Routing the output back to the input means the Morse pattern encodes *itself* — the dots and dashes from the previous frame become the brightness source for the next frame's encoding, creating evolving self-referential telegraph patterns.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; dedicated memory in the FPGA fabric. Telegram uses zero BRAMs — all processing is register-based. |
| **DDS** | Direct Digital Synthesis; a phase-accumulator technique for generating continuous scroll from a fixed-rate increment counter. |
| **Dit / Dah** | Morse code terminology for short and long pulses (dots and dashes). Telegram uses the brightness threshold to decide between narrow bars (dits) and wide bars (dahs). |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit executing the Morse overlay pipeline in real time. |
| **LFSR** | Linear Feedback Shift Register; a pseudo-random number generator used in Noise mode to produce random dot/dash decisions. |
| **Luma** | The brightness component (Y) of a YUV video signal, used as the source for dash/dot encoding. |
| **Morse Code** | A binary signalling system using short and long pulses, invented by Samuel Morse in the 1840s, serving as the conceptual basis for Telegram's visual encoding. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next on each clock cycle. |
| **Proc Amp** | Processing Amplifier; the gain-and-offset stage (contrast and brightness) applied after compositing. |
| **Symbol Period** | The number of pixels occupied by one dot-or-dash element, determined by the Speed control's power-of-two shift. |
| **Tape Band** | A horizontal strip of the frame where Morse patterns are rendered, separated by dimmed-source gap regions. |
| **YUV** | A color encoding separating luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |
