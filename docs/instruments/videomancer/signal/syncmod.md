---
draft: true
sidebar_position: 292
slug: /instruments/videomancer/syncmod
title: "Sync Mod"
image: /img/instruments/videomancer/syncmod/syncmod_hero.png
description: "Sync Mod rewrites the television raster in real time."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import syncmod_hero from '/img/instruments/videomancer/syncmod/syncmod_hero.png';
import syncmod_control_panel from '/img/instruments/videomancer/syncmod/syncmod_control_panel.png';
import syncmod_exercise1_result from '/img/instruments/videomancer/syncmod/syncmod_exercise1_result.png';
import syncmod_exercise2_result from '/img/instruments/videomancer/syncmod/syncmod_exercise2_result.png';
import syncmod_exercise3_result from '/img/instruments/videomancer/syncmod/syncmod_exercise3_result.png';
import syncmod_source1_kodim15 from '/img/instruments/videomancer/syncmod/syncmod_source1_kodim15.png';
import syncmod_source2_kodim01 from '/img/instruments/videomancer/syncmod/syncmod_source2_kodim01.png';
import syncmod_source3_stream_bridge_512 from '/img/instruments/videomancer/syncmod/syncmod_source3_stream_bridge_512.png';

# Sync Mod

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: syncmod_source1_kodim15, after: syncmod_hero },
    { label: "Kodim01", before: syncmod_source2_kodim01, after: syncmod_hero },
    { label: "Stream Bridge", before: syncmod_source3_stream_bridge_512, after: syncmod_hero },
  ]}
/>
*Horizontal scanlines warp sinusoidally across the frame, tearing apart a stable image into undulating bands of displaced colour.*

---

## Overview

Sync Mod rewrites the television raster in real time. By modulating the horizontal read address with sine or ramp functions that vary along the vertical axis, the program compresses, stretches, and folds each scanline into a new position — producing the controlled geometric distortion that Steina and Woody Vasulka pioneered with modified monitors in the 1970s.

The core engine stores each incoming scanline in a 1280-sample line buffer and reads it back through a horizontally displaced pointer. The displacement is computed from a DDS-driven sine (or ramp) whose phase rotates per scanline, producing smooth undulations that scroll through the frame in real time. A separate vertical modulation axis selects between the current and previous line, introducing inter-line blending that subtly smears vertical detail. The Tear effect deliberately triples the offset in configurable vertical zones, simulating the violent horizontal discontinuities that occur when a sync signal is interrupted.

Because the modulation is purely address-based rather than amplitude-based, Sync Mod preserves the brightness and colour of every pixel — only its position changes. The result is a liquid, rubber-sheet image that breathes and folds while retaining all of its original detail.

---

## Background

### Vasulka Sync Manipulation

In the early 1970s, Steina and Woody Vasulka began feeding oscillator signals directly into the horizontal and vertical sync inputs of modified television monitors. The result was controlled geometric distortion — images compressed into narrow bands, expanded beyond the screen edge, or torn into jagged shards. This technique exploited the fact that a CRT's electron beam position is entirely determined by sync timing; altering the timing alters the geometry.

### Horizontal Displacement Mapping

Sync Mod approximates the Vasulka technique digitally. Rather than modifying actual sync signals, it stores each scanline in a line buffer and reads back from a displaced address. The displacement varies as a function of vertical position, producing per-line offsets that mirror the effect of feeding an oscillator into horizontal sync. The result is visually identical to hardware sync disruption but fully repeatable and controllable.

### DDS Phase Accumulation

A 16-bit phase accumulator advances per frame, providing the animation clock for both H and V modulation. The modulation frequency knobs scale the phase contribution of position within the frame: higher frequency means more oscillation cycles visible across the screen height (for H mod) or width (for V mod). This is the same DDS architecture used throughout the Videomancer audiovisualizer family.

### Sine vs Ramp Waveforms

The H Wave and V Wave toggles select between sinusoidal and sawtooth modulation. Sine produces smooth undulating folds; ramp produces linear compression-expansion that abruptly resets, creating a characteristic saw-tooth shearing effect. Both waveforms are derived from the same DDS phase but shaped differently — sine via a 64-entry quarter-wave LUT, ramp via direct phase-to-amplitude mapping.

### Tear Zones

The original Vasulka work often produced violent horizontal tears when sync was interrupted mid-frame. Sync Mod reproduces this with the Tear toggle: when enabled, any scanline whose low 8 bits of v_count fall below the Tear Width threshold has its horizontal offset tripled, producing a sudden lateral jump in a band across the frame. The tear band repeats every 256 lines, creating periodic rupture zones.


---

## Signal Flow

```
                    ┌─────────────────────────────────┐
  data_in ────────► │ Line Buffer Write (1280 × Y/U/V)│
                    │   ↓ copy at hsync_start          │
                    │ Previous Line Buffer (1280 × Y/U/V)│
                    └───────────┬─────────────────────┘
                                │
           ┌────────────────────▼────────────────────┐
           │  DDS Phase (v_count × freq + anim)      │
           │  ↓ Sine or Ramp waveform                │
           │  × H Mod Amt → v_h_offset               │
           │  ↓ Tear: ×3 in tear zones               │
           │  + h_count → clamped read address        │
           └───────────┬────────────────────────────┘
                       │
           ┌───────────▼────────────────────────────┐
           │  V Modulation (h_count × freq + anim)   │
           │  ↓ (+H phase if Phase Link)             │
           │  Sine or Ramp → blend select            │
           │  > 0 ? previous_line : current_line     │
           └───────────┬────────────────────────────┘
                       │
           ┌───────────▼──────┐    ┌──────────┐
           │ wet Y/U/V        ├───►│ Interp   ├──► data_out
           └──────────────────┘    │ (dry/wet) │
                                   └──────────┘
```

The horizontal and vertical modulation axes are computed from independent DDS phases but share the same animation clock, so they drift together. When Phase Link is enabled, the vertical phase accumulates the horizontal phase as an additional contribution, coupling the two axes into a single complex waveform that traces diagonal paths through the image.

The line buffer architecture means that the horizontal modulation is constrained to the current scanline — pixels cannot be displaced vertically by more than one line. Vertical displacement is approximated by switching between the current and previous line based on the V modulation waveform's sign, creating a coarse one-line vertical wobble that complements the smooth horizontal displacement.

---

## Parameter Reference

<img src={syncmod_control_panel} alt="Videomancer front panel with Sync Mod loaded"/>
*Videomancer's front panel with Sync Mod active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — H Mod Amt
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

H Mod Amt sets the maximum horizontal pixel displacement. At minimum the image is undistorted. As the knob increases, scanlines begin to shift left and right by increasing amounts, eventually folding back on themselves when the offset exceeds the visible width. The displacement is signed, so the image compresses in some regions and expands in others — a direct analog of feeding a larger-amplitude oscillator into hardware horizontal sync.

---

#### Knob 2 — H Mod Freq
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

H Mod Freq controls how many modulation cycles are visible across the screen height. Low values produce a single gentle arch across the entire frame; high values pack many undulations into the vertical extent, creating fine striped patterns where each group of scanlines is offset in alternating directions.

---

#### Knob 3 — V Mod Amt
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

V Mod Amt sets the depth of vertical modulation. When non-zero, the engine blends between the current scanline and the previous scanline based on a second DDS waveform that varies across horizontal position. At subtle settings this produces a gentle vertical smear; at higher values it creates distinct bands of line-doubled content.

---

#### Knob 4 — V Mod Freq
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

V Mod Freq controls the horizontal density of vertical modulation cycles. Low values cause the entire width to switch between current and previous line together; high values create rapid alternation across the scanline, producing comb-like interleaving of two adjacent lines.

---

#### Knob 5 — Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 20% |
| Suffix | % |

Speed sets the animation rate. The 16-bit DDS animation phase advances by (Speed + 1) per frame, so the modulation pattern scrolls through the image over time. Low speed creates slow breathing motion; high speed produces rapid oscillation that can blur into a shimmering texture.

---

#### Knob 6 — Tear Width
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 13% |
| Suffix | % |

Tear Width defines the vertical extent of the tear band, measured in scanlines (lower 8 bits of v_count). When Tear is enabled, any scanline within this band has its horizontal offset tripled. A narrow Tear Width produces thin shear lines; a wide one creates dramatic lateral jumps across large sections of the frame. The tear bands repeat every 256 lines, so multiple ruptures appear at regular intervals.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — H Wave** | Sine | Ramp |
| **8 — V Wave** | Sine | Ramp |
| **9 — Tear** | Off | On |
| **10 — Phase Link** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles configure waveform shape, special effects, and bypass. H Wave and V Wave independently select sine or ramp for their respective axes, and can be mixed — for example, sine H with ramp V creates smooth horizontal undulation with saw-tooth vertical interleaving. Tear adds the violent horizontal discontinuity that completes the Vasulka aesthetic. Phase Link couples the two modulation axes for diagonal displacement paths. Bypass returns the unprocessed signal.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Mix crossfades between the unprocessed input (dry) and the sync-modulated output (wet). At minimum the original image passes through; at maximum the full distortion is visible. Intermediate positions blend the two, which can produce a ghostly double-image effect as the displaced and undisplaced versions overlay.

---

## Guided Exercises

These exercises demonstrate the range of geometric distortion achievable with Sync Mod, progressing from gentle undulation to violent raster tearing.

### Exercise 1: Gentle Horizontal Waves

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: syncmod_source1_kodim15, after: syncmod_exercise1_result },
    { label: "Kodim01", before: syncmod_source2_kodim01, after: syncmod_exercise1_result },
    { label: "Stream Bridge", before: syncmod_source3_stream_bridge_512, after: syncmod_exercise1_result },
  ]}
/>
*Gentle Horizontal Waves — simulated result across source images.*
**Source**: A high-contrast graphic with strong horizontal and vertical edges (e.g., a title card or grid pattern).

**Objective**: Create slow, smooth sinusoidal displacement that makes the image breathe without tearing.

1. Set H Mod Amt to 30% for moderate displacement.
2. Set H Mod Freq to 15% for a single gentle arch across the frame.
3. Set Speed to 20% for slow animation.
4. Leave V Mod Amt at 0% to isolate horizontal motion.
5. Observe the image gently undulating — straight lines become sine curves.
6. Slowly increase H Mod Freq to see the undulations multiply.

**Key concepts**: Sinusoidal displacement preserves image content while reorganising spatial relationships. The number of visible cycles is determined by H Mod Freq.

---

### Exercise 2: Ramp Shear with Vertical Blend

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: syncmod_source1_kodim15, after: syncmod_exercise2_result },
    { label: "Kodim01", before: syncmod_source2_kodim01, after: syncmod_exercise2_result },
    { label: "Stream Bridge", before: syncmod_source3_stream_bridge_512, after: syncmod_exercise2_result },
  ]}
/>
*Ramp Shear with Vertical Blend — simulated result across source images.*
**Source**: A face or recognisable form — the shearing effect is most dramatic when the viewer can detect the spatial disruption.

**Objective**: Combine ramp H waveform with vertical modulation to create diagonal shearing.

1. Set H Wave to Ramp, V Wave to Ramp.
2. Set H Mod Amt to 50%, H Mod Freq to 40%.
3. Set V Mod Amt to 60%, V Mod Freq to 30%.
4. Enable Phase Link.
5. Set Speed to 35%.
6. Watch the image shear diagonally as the linked ramp waveforms create angled displacement bands.

**Key concepts**: Ramp waveforms create linear compression followed by abrupt reset, producing hard shear lines. Phase Link couples the axes so the shear follows a diagonal path rather than being purely horizontal.

---

### Exercise 3: Vasulka Tear Storm

<BeforeAfterSlider
  sources={[
    { label: "Kodim15", before: syncmod_source1_kodim15, after: syncmod_exercise3_result },
    { label: "Kodim01", before: syncmod_source2_kodim01, after: syncmod_exercise3_result },
    { label: "Stream Bridge", before: syncmod_source3_stream_bridge_512, after: syncmod_exercise3_result },
  ]}
/>
*Vasulka Tear Storm — simulated result across source images.*
**Source**: Any video signal — the tear effect is visually compelling regardless of content.

**Objective**: Create the violent horizontal tearing that characterises the Vasulka aesthetic.

1. Set H Mod Amt to 80%, H Mod Freq to 25%.
2. Enable Tear and set Tear Width to 50%.
3. Set Speed to 45% for rapid animation.
4. Set V Mod Amt to 20% for subtle vertical disruption.
5. Observe periodic tear bands ripping through the image every 256 lines.
6. Increase Tear Width to expand the rupture zones.

**Key concepts**: The tear effect triples the horizontal offset in configurable vertical bands, creating discontinuities that repeat every 256 scanlines. Combined with animation, these bands scroll through the frame, producing the characteristic horizontal shredding of early video art.

---


## Tips

- **Start with H only**: Set V Mod Amt to zero when learning the program to isolate horizontal displacement before adding vertical complexity.
- **Low Freq, High Amt for drama**: A single large-amplitude arch across the frame creates the most cinematic Vasulka-style compression effect.
- **Tear sparingly**: The tear effect is powerful —  a thin tear band (10–20%) adds punctuation without overwhelming the image.
- **Phase Link + Sine for organic motion**: Linked sine waveforms create complex Lissajous-like diagonal paths that feel natural.
- **Mix for layering**: At 50% mix, the displaced and original images overlay, creating ghostly doubled geometry.
- **Speed 0 for stills**: With Speed at zero the displacement is static — useful for controlled photographic distortion.
- **Ramp for retro video art**: Ramp waveforms most closely approximate the hard compression/expansion of real sync disruption.

---
