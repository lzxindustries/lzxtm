---
draft: true
sidebar_position: 58
slug: /instruments/videomancer/colorgan
title: "Colorgan"
image: /img/instruments/videomancer/colorgan/colorgan_hero.png
description: "Colorgan transforms incoming video luminance into a three-band colour organ display reminiscent of 1970s CEL Chromascope disco lighting units."
---

import colorgan_hero from '/img/instruments/videomancer/colorgan/colorgan_hero.png';
import colorgan_animation from '/img/instruments/videomancer/colorgan/colorgan_animation.gif';
import colorgan_control_panel from '/img/instruments/videomancer/colorgan/colorgan_control_panel.png';
import colorgan_exercise1_result from '/img/instruments/videomancer/colorgan/colorgan_exercise1_result.gif';
import colorgan_exercise2_result from '/img/instruments/videomancer/colorgan/colorgan_exercise2_result.gif';
import colorgan_exercise3_result from '/img/instruments/videomancer/colorgan/colorgan_exercise3_result.gif';

# Colorgan

<span class="head2_nolink">Videomancer Program Guide</span>

:::warning
This document is still in progress, may contain errors, and is for preview only.
:::

<img src={colorgan_hero} alt="Colorgan hero image"/>
*Three pulsing colour zones — red bass wash, green mid glow, and blue treble flash — merge additively in concentric rings driven by video luminance.*
<img src={colorgan_animation} alt="Colorgan animated output"/>
*Colorgan output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Colorgan transforms incoming video luminance into a three-band colour organ display reminiscent of 1970s CEL Chromascope disco lighting units.  The program analyses the average brightness of each frame through a pair of IIR envelope followers running at different speeds.  A slow integrator extracts the "bass" — the broad, lazy drift of overall scene brightness — while a faster integrator catches the "mid" range.  The difference between the fast integrator and the instantaneous frame average yields "treble" — the sharp spikes of flickering detail and motion edges.

Each frequency band drives a coloured zone on screen.  In Concentric mode the zones form nested rings expanding outward from the screen centre: treble at the core, mid in a surrounding annulus, bass as the outermost wash.  In Layered mode the zones stack horizontally in thirds: treble at the top, mid in the middle, bass at the bottom.  Per-band sensitivity knobs let the operator emphasise or mute any frequency, the Zone Width control sets the spatial extent of each region, and two palette switches choose between warm (red/magenta bass, green mid, blue treble) and cool (cyan bass, green mid, magenta treble) colour mappings.

When no video is present the organ falls silent — a dark screen.  Feed it a flickering candle and the bass zone breathes gently; feed it a strobing pattern and the treble zone fires in rapid pulses while the bass barely moves.  The Decay knob controls an animation phase accumulator, adding slow drift to the envelope followers' temporal smoothing, while the React toggle switches between the full IIR response (smooth) and a sharper, more percussive feel.

---

## Quick Start

1. **Start with one band:** Solo each frequency band by setting the other two sensitivities to zero — this reveals what each IIR filter is actually tracking.
2. **Match decay to tempo:** For rhythmic sources, lower Decay values keep the colour organ tight and punchy; for ambient footage, higher values produce a slow, meditative glow.
3. **Concentric for projection:** The radial geometry works particularly well when projected onto a wall or screen, where the expanding rings create a stadium-spotlight effect.

---

## Background

### Colour Organs and Lumia

The concept of translating sound — or, more broadly, changing stimuli — into coloured light dates to the 18th century clavier à lumières.  Thomas Wilfred's Clavilux (1919) elevated the idea into an art form called Lumia, projecting slowly evolving colour fields from hand-operated mechanisms.  By the 1960s, electronic colour organs like the CEL Chromascope analysed audio frequency bands and drove coloured lamp circuits: bass → red, mid → green, treble → blue.

### IIR Envelope Followers

Colorgan borrows the colour organ's band-splitting concept but applies it spatially and temporally to video luminance.  A first-order IIR low-pass filter `y[n] = (1−α)·y[n-1] + α·x[n]` with α=1/16 provides bass (very slow tracking), while α=1/4 gives the mid band faster response.  Treble is the residual: the absolute difference between the fast IIR output and the instantaneous frame average.  These digital envelope followers are the same topology used in analogue VU meters and automatic gain controls.

### Concentric Zone Mapping

In Concentric mode, the screen is divided into nested regions defined by Manhattan distance from centre.  This rectangular distance metric (|Δx|+|Δy|) produces diamond-shaped contours on a raster display — a deliberate aesthetic nod to early video synthesisers that favoured integer-only arithmetic and axis-aligned geometry.  Zone Width scales the boundary thresholds, making the concentric rings larger or smaller.

### Additive Colour Mixing

Each band generates a luminance contribution proportional to its envelope level multiplied by its sensitivity knob.  The three contributions are summed additively into a single Y channel, while each band shifts the U/V chroma plane toward its assigned colour.  Where zones overlap, colours blend — bass red meeting mid green produces yellow; treble blue meeting mid green produces cyan.  This additive model mirrors the RGB phosphor mixing of CRT displays and theatrical stage lighting.

### Warm and Cool Palettes

The two palette modes remap the chroma assignments.  Warm palette pushes bass toward red (+V), mid toward green (−U), and treble toward blue (+U).  Cool palette rotates the assignments: bass → cyan (+U), mid → green (−V), treble → magenta (−U, +V).  Switching palettes mid-performance can dramatically shift the mood from firelit intimacy to cold electronic precision.


---

## Signal Flow

```
               Input Video (Y/U/V)
                       │
            ┌──────────┴──────────┐
            │   Frame Average     │
            │   (accumulate Y,    │
            │    divide at vsync) │
            └──────────┬──────────┘
                       │
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
   ┌──────────┐  ┌──────────┐  ┌──────────┐
   │ Slow IIR │  │ Fast IIR │  │ Residual │
   │  α=1/16  │  │  α=1/4   │  │ |fast−avg|│
   │  (bass)  │  │  (mid)   │  │ (treble) │
   └────┬─────┘  └────┬─────┘  └────┬─────┘
        │              │              │
        ▼              ▼              ▼
   ┌──────────┐  ┌──────────┐  ┌──────────┐
   │ × Sens 1 │  │ × Sens 2 │  │ × Sens 3 │
   └────┬─────┘  └────┬─────┘  └────┬─────┘
        │              │              │
        └──────────────┼──────────────┘
                       │
         ┌─────────────▼─────────────┐
         │    Zone Mapping           │
         │  (Concentric / Layered)   │
         │  per-pixel contribution   │
         └─────────────┬─────────────┘
                       │
         ┌─────────────▼─────────────┐
         │  Additive Y + Colour Map  │
         │  (Warm / Cool palette)    │
         └─────────────┬─────────────┘
                       │
         ┌─────────────▼─────────────┐
         │     Interpolator Mix      │
         │     (dry/wet fader)       │
         └─────────────┬─────────────┘
                       │
                    Output Y/U/V
```

The pipeline is unusual in that no per-pixel source data flows through the processing chain — only aggregate statistics.  The entire frame's luminance is averaged during active video, then at each vsync the IIR filters update their band levels.  All pixels in a given frame share the same bass/mid/treble levels; spatial variation comes entirely from the zone geometry (distance from centre or vertical position).  This means the output image for any single frame is a static colour pattern whose brightness modulates frame-to-frame — much like a real colour organ lamp panel, where bulbs glow uniformly but pulse at different rates.

The Video Mod toggle provides a way to re-inject source video structure by blending the generated zones with the delayed input via the mix interpolators.

---

## Parameter Reference

<img src={colorgan_control_panel} alt="Videomancer front panel with Colorgan loaded"/>
*Videomancer's front panel with Colorgan active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Bass Zone
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Bass Zone controls the sensitivity of the low-frequency band.  At zero the bass zone contributes no light; as the knob increases, the outer ring (or bottom strip in Layered mode) glows more brightly in response to slow luminance drift.  High settings cause even modest scene-average changes to saturate the bass zone, producing a constant warm wash.  Moderate settings around 50 % let the bass breathe naturally.

---

#### Knob 2 — Mid Zone
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Mid Zone sets the sensitivity of the medium-frequency band.  This band responds to luminance changes that are faster than the bass IIR but slower than instantaneous flicker.  Boosting Mid Zone fills the middle ring (or centre strip) with green-tinted light that follows scene dynamics at a conversational pace.  When all three bands are set equally the colour organ responds uniformly across the spectrum; pulling Mid Zone down isolates bass and treble for a more dramatic two-colour contrast.

---

#### Knob 3 — Treble Zone
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Treble Zone controls the high-frequency band — the sharp edges and rapid flicker extracted as the residual between the fast IIR and the frame average.  At high settings even subtle motion produces bright treble flashes in the centre zone.  At low settings only dramatic cuts or strobing sources trigger the treble.  Treble tends to produce the most visually percussive effect, adding sparkle and rhythm to the colour organ display.

---

#### Knob 4 — Zone Width
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Zone Width adjusts the spatial extent of each colour zone.  At low values the zones are tightly packed around the centre (Concentric) or compressed into thin horizontal slices (Layered).  Increasing Zone Width spreads the regions outward, allowing broader overlap and more additive blending between adjacent bands.  Very wide settings push the outer bass zone well off-screen, effectively turning the entire display into a mid/treble field.

---

#### Knob 5 — Hue Offset
| Property | Value |
|----------|-------|
| Range | 0d – 360d |
| Default | 0d |
| Suffix | d |

Hue Offset rotates the base hue through 360 degrees of the colour wheel.  While the Palette toggle sets the fundamental colour assignments, Hue Offset lets the operator fine-tune the tint — shifting warm reds toward orange or magenta, for example.  Because the offset is applied uniformly to all three bands, relative colour relationships are preserved; the entire organ simply rotates around the colour wheel.

---

#### Knob 6 — Decay
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 59% |
| Suffix | % |

Decay controls temporal smoothing via the animation phase accumulator.  Higher values advance the phase faster, adding a subtle drift to the envelope response.  At minimum the IIR filters dominate, producing smooth, predictable band tracking.  At maximum the phase accumulator introduces visible undulation, giving the colour zones a slow organic pulse even when the input luminance is static.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Layout** | Concentric | Layered |
| **8 — Palette** | Warm | Cool |
| **9 — React** | Smooth | Sharp |
| **10 — Video Mod** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles divide into functional pairs: Layout and Palette control geometry and colour mapping; React adjusts temporal dynamics; Video Mod re-injects source imagery.  Bypass disables all processing.  Layout and Palette can be switched freely during performance to shift between radial and striped geometries or warm and cool colour schemes.  React is best toggled during high-energy source material where the difference between smooth IIR tracking and sharp response is most audible — that is, most visible.  Video Mod provides a quick way to ground the abstract colour zones in recognisable source structure without adjusting the mix fader.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Mix crossfades between the dry input signal and the wet colour organ output.  At zero the output is pure dry video; at maximum it is entirely the generated colour zones.  Intermediate positions blend the two, allowing the colour organ to function as a translucent overlay.  When Video Mod is active, the mix fader provides an additional layer of control over how much source structure bleeds into the colour zones.





---

## Guided Exercises

These exercises demonstrate Colorgan's three-band spectral separation, zone geometry, and palette selection.  Each produces a distinct visual character from the same underlying luminance analysis.

### Exercise 1: Warm Concentric Rings

<img src={colorgan_exercise1_result} alt="Warm Concentric Rings result"/>
*Warm Concentric Rings — simulated result across source images.*
**What You'll Create**: Produce nested concentric colour rings that pulse gently with broad luminance changes.

1. Set Bass Zone to 70 %, Mid Zone to 50 %, and Treble Zone to 30 % to emphasise low-frequency response.
2. Set Zone Width to 60 % to give the rings generous spacing.
3. Confirm Layout is Concentric and Palette is Warm.
4. Feed a slowly moving source — a candle flame or lava lamp works well.
5. Observe the outer red ring breathing with overall brightness while the centre flickers blue with motion edges.
6. Sweep Hue Offset through 360° and note how all three ring colours rotate together.

**Key concepts**: - IIR time constants create band separation from a single luminance signal
- Concentric geometry uses Manhattan distance from screen centre
- Additive colour mixing where zones overlap

---

### Exercise 2: Layered Stroboscope

<img src={colorgan_exercise2_result} alt="Layered Stroboscope result"/>
*Layered Stroboscope — simulated result across source images.*
**What You'll Create**: Create horizontal colour bands that respond percussively to rapid flicker.

1. Set all three band sensitivities to 80 % for uniform response.
2. Set Zone Width to 50 % and Decay to 20 % for tight, fast zones.
3. Switch Layout to Layered and React to Sharp.
4. Feed a strobe or rapidly editing source.
5. Observe how the three horizontal bands flash independently — treble fires first, mid follows, bass last.
6. Switch Palette to Cool and compare the colour temperature shift.

**Key concepts**: - Layered geometry divides the screen into three horizontal strips
- Sharp React reduces IIR smoothing for percussive response
- Cool palette reassigns bass to cyan and treble to magenta

---

### Exercise 3: Video Mod Overlay

<img src={colorgan_exercise3_result} alt="Video Mod Overlay result"/>
*Video Mod Overlay — simulated result across source images.*
**What You'll Create**: Blend colour organ zones with recognisable source video to create a tinted composite.

1. Set Bass Zone to 60 %, Mid Zone to 40 %, Treble Zone to 50 %.
2. Set Zone Width to 80 % for broad coverage.
3. Enable Video Mod and set Mix to 70 %.
4. Feed a camera source with strong foreground-background contrast.
5. Observe how source shapes appear within the colour zones, tinted by bass/mid/treble activity.
6. Adjust Decay upward to add slow undulation to the overlay.

**Key concepts**: - Video Mod re-injects delayed source luminance into the colour output
- Mix fader controls the blend ratio between generated zones and source
- Decay adds animation phase drift for organic pulsing

---


## Tips

- **Layered for installations:** Horizontal bands pair naturally with wide-format displays and multi-screen setups where each band occupies a distinct physical zone.
- **Video Mod for narrative:** When you want the audience to still see what is happening in the source material, Video Mod overlays the colour organ as a tinted filter rather than replacing the image entirely.
- **Hue Offset for variety:** Even small rotations of 30–60° shift the perceived warmth/coolness dramatically, providing palette variety without switching the Warm/Cool toggle.
- **Chain with effects:** Feed Colorgan's output into a feedback or blur program to smear the sharp zone boundaries into soft, painterly gradients.

---
