---
draft: true
sidebar_position: 43
slug: /instruments/videomancer/chatoyant
title: "Chatoyant"
image: /img/instruments/videomancer/chatoyant/chatoyant_hero.png
description: "Certain gemstones — tiger's eye, chrysoberyl, moonstone — contain parallel fibrous inclusions that act as a natural diffraction grating."
---

import chatoyant_hero from '/img/instruments/videomancer/chatoyant/chatoyant_hero.png';
import chatoyant_before_after from '/img/instruments/videomancer/chatoyant/chatoyant_before_after.png';
import chatoyant_control_panel from '/img/instruments/videomancer/chatoyant/chatoyant_control_panel.png';
import chatoyant_exercise1_result from '/img/instruments/videomancer/chatoyant/chatoyant_exercise1_result.png';
import chatoyant_exercise2_result from '/img/instruments/videomancer/chatoyant/chatoyant_exercise2_result.png';
import chatoyant_exercise3_result from '/img/instruments/videomancer/chatoyant/chatoyant_exercise3_result.png';

# Chatoyant

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={chatoyant_hero} alt="Chatoyant hero image"/>
*Chatoyant drawing a warm specular streak across a landscape, the highlight band tracing the axis of light like a cat's-eye cabochon tilted under a single point source.*
<img src={chatoyant_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Chatoyant applied.*

---

## Overview

Certain gemstones — tiger's eye, chrysoberyl, moonstone — contain parallel fibrous inclusions that act as a natural diffraction grating. When a point light source illuminates the polished surface, these aligned fibres reflect a single bright band of light perpendicular to their axis. Rotate the stone under the lamp and the band slides across the dome, always perpendicular to the fibre direction, always sharpest where the curvature meets the light at the critical angle. Gemologists call this *chatoyancy*, from the French *œil de chat* — the eye of the cat.

Chatoyant recreates this optical phenomenon in the digital video domain. A virtual streak line is positioned across the frame, and every pixel's distance to that line is computed in real time. Pixels within the streak band receive a brightness boost proportional to their source luminance — bright areas catch the highlight like the facets of a cabochon, while dark areas remain unaffected. A line buffer stores the previous scanline's Y channel to compute a vertical gradient, which can be folded into the highlight to emphasise edges and surface transitions within the streak zone. The streak can be locked to horizontal, vertical, or diagonal orientations, or allowed to sweep freely at angles controlled by the Axis Angle knob.

At subtle settings, Chatoyant adds a delicate specular sheen — a luminous stripe that makes the video surface appear polished, capturing a sense of reflected light that shifts with the source content. At extreme settings the streak becomes a hot band of clipped white or tinted colour that burns across the frame, splitting the image into illuminated and shadowed halves like a gem rotated past its critical angle. Double-streak mode mirrors the highlight across the frame centre, and the animation toggle sets the streak bouncing back and forth — a slow, hypnotic sweep that evokes a jeweller's loupe swaying over a display case.

---

## Background

### Chatoyancy and Asterism in Gemology

The chatoyant effect requires three conditions: a cabochon cut (domed, not faceted), parallel fibrous or needle-like inclusions within the stone, and a single point light source. The inclusions — typically rutile needles in quartz, or asbestos fibres in tiger's eye — create a cylinder of reflection perpendicular to the fibre axis. The result is a narrow, bright band that appears to float above the surface. When the stone contains multiple sets of intersecting needle inclusions (as in star sapphire or star ruby), the effect multiplies: two sets produce a four-rayed star, three sets a six-rayed star. This multi-ray phenomenon is called *asterism*, and it is the inspiration for Chatoyant's multi-streak mode. The program abstracts the physical optics into a geometric distance computation: each pixel's proximity to one or more virtual streak lines determines how much specular energy it receives.

### Line Buffers and Vertical Gradient Detection

To detect vertical structure in the video — edges, transitions, surface contours — Chatoyant stores the previous scanline's luma in a dual-bank BRAM line buffer. On each clock, the current pixel's Y value is written to one bank while the corresponding position from the previous line is read from the other. The vertical gradient is the absolute difference between current and previous luma: `|Y_current - Y_prev|`. This gradient is zero in flat regions and peaks at horizontal edges. By mixing the gradient signal into the highlight computation, the Softness parameter lets the streak interact with the source's vertical structure — emphasising contours within the highlight band, much as a real chatoyant highlight catches the ridges of a carved cabochon.

### Streak Geometry and Direction Modes

The streak is a mathematical line across the frame. Each pixel's perpendicular distance to this line determines whether it falls within the highlight band. The direction mode (Gem Type toggle) defines how the line is oriented: horizontal produces a streak parallel to the scan lines at a controllable vertical position; vertical produces a streak perpendicular to the scan lines; diagonal places it at 45 degrees. The free mode (Tigers) allows the Axis Angle knob to continuously vary the slope, sweeping the streak from nearly horizontal through steep diagonals. The position and angle are combined with an optional sweep offset from the animation accumulator, creating a streak that can drift across the frame over time. Double-streak mode places a second line mirrored about the frame centre, and the highlight computation uses whichever line is closer to each pixel — producing a symmetric pair of converging or diverging bands.

### Distance-Based Highlight Falloff

The highlight intensity is not uniform across the streak band. At the centre of the band — where the pixel's distance to the streak line is near zero — the boost is at full strength. As the distance increases toward the edge of the band, the Falloff control attenuates the highlight by shifting the luma contribution rightward (dividing by powers of two). A sharp falloff produces a hard-edged stripe with a distinct border; a gradual falloff feathers the edges into a soft glow that tapers smoothly into the unaffected background. The Streak Width knob sets the total radius of the band, while Falloff controls the transition profile within it — analogous to the sharpness of a real chatoyant band, which depends on how tightly the fibrous inclusions are aligned.

### Colour Temperature and Specular Tinting

Real chatoyant highlights are rarely pure white. Tiger's eye produces warm golden-amber streaks; moonstone glows with a cool blue adularescence; opal scatters the full spectrum. Chatoyant simulates this by optionally tinting the highlight in the UV colour plane. When the colour highlight toggle is active and the boost exceeds a minimum threshold, the program shifts U and V away from neutral: warm tint pulls U below centre and pushes V above (toward amber-gold), while cool tint does the reverse (toward ice-blue). The tint is proportional to the boost amount — stronger highlights receive deeper colour, weaker highlights remain closer to neutral. The tinted chroma is blended 50/50 with the source chroma, preserving some of the original colour character while adding the specular hue.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├─ 1. Input Register + Parameter Latch + Pixel Counters      (1 clk)
│      ├─ Latch Y, U, V
│      ├─ Write current Y → line buffer (BRAM bank A/B)
│      └─ Maintain h_count, v_count, sweep accumulator
│
├─ 2. Address Compute + Line Buffer Read Issued               (1 clk)
│      ├─ BRAM read address = h_count
│      └─ Pipeline Y, U, V, h_count, v_count forward
│
├─ 3–4. Line Buffer BRAM Read Latency                         (2 clk)
│      └─ Previous-line Y retrieved from opposite BRAM bank
│
├─ 5. Gradient + Streak Distance                              (1 clk)
│      ├─ Vertical gradient = |current_Y − prev_line_Y|
│      ├─ Streak position from Gem Type mode:
│      │   ├─ Tigers (free): position + h_count × angle_slope + sweep
│      │   ├─ Star (horiz):  position + sweep
│      │   ├─ Moon (vert):   angle × 1.5 + sweep
│      │   └─ Opal (diag):   |v + h − (position + 960)| / 2 + sweep
│      ├─ Distance A = |pixel_position − streak_position|
│      ├─ Double streak: Distance B = |pixel − mirrored_streak|
│      │   └─ Use min(A, B)
│      └─ In-streak flag = (distance < width_threshold)
│
├─ 6. Highlight Compose + Colour Tint                         (1 clk)
│      ├─ Inside streak band:
│      │   ├─ luma_scale = source_Y >> 2
│      │   ├─ Centre half: full luma_scale
│      │   ├─ Outer half: attenuate by falloff_shift
│      │   ├─ + gradient contribution (if softness > 512)
│      │   ├─ Apply highlight_shift (intensity control)
│      │   ├─ Y_out = Y_in + boost  (clamped 0–1023)
│      │   └─ If boost > 16 and colour highlight on:
│      │       ├─ Warm: U = mid − boost/4, V = mid + boost/4
│      │       └─ Cool: U = mid + boost/4, V = mid − boost/4
│      │       └─ Blend 50/50 with source chroma
│      └─ Outside streak: pass Y, U, V through unchanged
│
├─ 7–10. Interpolator Mix (×3 channels, 4 clk each)
│      └─ Dry/wet crossfade: t = Mix fader (0 = dry, 1023 = wet)
│
├─ Sync / Data Delay Pipeline (10-clock shift register)
│
└─ Output Mux
    ├─ Bypass off → mixed Y/U/V + aligned sync
    └─ Bypass on  → delayed input Y/U/V + aligned sync
```

The critical path runs through the line buffer: current Y is written on stage 1, read back two clocks later from the opposite BRAM bank, and the gradient is available at stage 5 alongside the streak distance computation. Because the read address matches the write address (both keyed to `h_count`), the buffer returns the same horizontal position from the previous scanline, giving a pure vertical difference. This one-line delay is fundamental to the edge-detection quality of the gradient — it measures change over exactly one line period, producing a signal that peaks at horizontal edges and texture boundaries.

The streak distance computation in stage 5 is the most logic-intensive step, with a four-way case statement selecting the geometry based on Gem Type. The free mode (Tigers) uses a shift-selected slope approximation: the three MSBs of the angle register select one of eight discrete slope levels for the horizontal contribution, avoiding a full multiply. This shift-and-add approach keeps the design within the iCE40 HX4K's LUT budget while providing enough angular resolution for smooth visual sweeps.

The colour tinting in stage 6 only activates when the boost exceeds 16 (out of 1023), preventing noise-level highlights from introducing chroma artefacts. When active, the tint magnitude scales with the boost — a subtle highlight gets a subtle colour shift, while a strong highlight gets a deep tint. This proportional coupling mirrors real chatoyancy, where the colour saturation of the band depends on how directly the light strikes the fibre axis.

---

## Parameter Reference

<img src={chatoyant_control_panel} alt="Videomancer front panel with Chatoyant loaded"/>
*Videomancer's front panel with Chatoyant active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Streak W
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the width of the specular streak band — the spatial extent of the highlight region measured perpendicular to the streak axis. At minimum the band is just a few pixels wide, producing a razor-thin line of light. As the knob is advanced, the band widens into a broad luminous swathe that covers a significant portion of the frame. The width is applied symmetrically around the streak centre, with the Falloff parameter controlling how the highlight intensity tapers toward the edges. A wide streak with soft falloff produces a diffuse glow; a narrow streak with sharp falloff produces a hard specular line. The width value also determines the position of the centre-to-edge transition zone — pixels within the inner half receive full highlight, while those in the outer half are attenuated.

---

#### Knob 2 — Axis Ang
| Property | Value |
|----------|-------|
| Range | 0° – 180° |
| Default | 90° |
| Suffix | ° |

Sets the angular orientation of the streak axis across the frame. At 0° the streak aligns with one edge; at 180° it has swept to the opposite orientation. In the free Gem Type mode (Tigers), this knob continuously varies the slope of the streak line by controlling how much horizontal pixel position contributes to the streak's effective vertical coordinate. The angle is discretized into eight slope levels internally — enough for a visually smooth sweep but implemented via shift operations rather than a full trigonometric computation. In the locked Gem Type modes (Star, Moon, Opal), this control influences the streak position along the locked axis, allowing placement adjustment within the constrained orientation.

---

#### Knob 3 — Threshold
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the brightness threshold that determines how much luma boost the highlight contributes. The threshold is mapped to four intensity levels internally, ranging from subtle (a gentle brightening that barely lifts the highlight above the source) to strong (an aggressive boost that drives the streak toward peak white). The boost is always proportional to the source luminance — bright pixels receive a larger absolute increase than dark ones, preserving the natural tonal hierarchy of the image within the highlight band. At maximum intensity, pixels already near peak white will clip to 1023, creating a hard saturated streak that reads as a specular reflection.

---

#### Knob 4 — Intensity
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the highlight edge softness — how rapidly the specular boost attenuates as pixel distance increases from the streak centre toward the band edge. At low values the falloff is sharp: the highlight drops off steeply, producing a hard-bordered stripe with a distinct boundary against the unaffected background. At high values the falloff is gradual: the highlight feathers gently outward, creating a soft luminous glow that blends smoothly into the surrounding image. The falloff is implemented as a shift-based attenuation — four discrete softness levels that progressively halve the highlight contribution in the outer half of the streak band. Combined with the streak width, this control shapes the perceived sharpness of the chatoyant band.

---

#### Knob 5 — Streak L
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the length or extent of the streak across the frame by controlling its base vertical position. This knob positions the streak line in the vertical dimension, sliding it from the top of the frame to the bottom. In horizontal Gem Type mode, this directly sets the scanline where the streak sits. In free mode, it sets the vertical intercept of the angled streak line. In vertical mode it influences horizontal placement instead. When animation is active, this position serves as the starting offset for the bounce sweep — the streak oscillates around this home position, and the knob's setting determines where on the frame the sweep is centred.

---

#### Knob 6 — Hue Tint
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Shifts the colour temperature of the specular highlight by controlling how much vertical gradient information contributes to the highlight computation. When turned past centre, the gradient signal — the vertical edge energy detected from the line buffer — is folded into the highlight intensity, causing the streak to respond more strongly to textured and edge-rich areas of the source image. This creates a surface-aware highlight that catches the contours and transitions within the streak band, producing a more complex, organic chatoyant appearance reminiscent of inclusions scattering light at slightly different angles. Below centre, the gradient contribution is suppressed and the highlight responds only to raw source brightness.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Gem Type** | Tigers | Star |
| **8 — Streaks** | 1 | 2 |
| **9 — Color Hlt** | Off | On |
| **10 — Anim** | Off | On |
| **11 — Bypass** | Off | On |

The five toggle switches address independent aspects of the streak's character. Gem Type (Toggle 7) and Streaks (Toggle 8) are the primary shape controls — Gem Type sets the geometric orientation of the streak line, while Streaks multiplies the number of visible bands. Colour Highlight (Toggle 9) activates chromatic tinting in the UV plane, adding warm or cool hue to the specular band. Animation (Toggle 10) sets the streak in motion with a bounce sweep. Bypass (Toggle 11) overrides all processing. The toggles combine freely: a four-streak animated configuration with colour highlighting in Opal diagonal mode produces a complex, shimmering pattern of intersecting coloured bands sweeping across the frame.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfades between the dry input signal and the specular-highlighted signal. At 0% (fader down), the output is pure dry — no streak is visible. At 100% (fader up), the output is fully processed — the highlight band appears at full intensity. Intermediate positions blend the two, letting you dial in the desired prominence of the chatoyant effect. This is the master intensity control: even with strong highlight settings, a low mix value keeps the effect subtle. At full mix, the streak dominates the image and the dry signal disappears entirely into the specular composition.

---

## Guided Exercises

These exercises build from a simple single-streak highlight through multi-mode exploration to animated, tinted asterism patterns. Each one introduces a new facet of the chatoyant engine while reinforcing the controls learned earlier.

### Exercise 1: Single Specular Band

<img src={chatoyant_exercise1_result} alt="Single Specular Band result"/>
*Single Specular Band — simulated result across source images.*
**Source**: A portrait or still life with clear tonal gradients — smooth skin, fabric folds, or polished surfaces.

**Objective**: Understand how the streak width, position, intensity, and mix controls shape a basic specular highlight.

1. **Position the streak**: Set Gem Type to Star (horizontal). Turn Streak L (Position) to ~50% to place the streak near the centre of the frame. Push Mix to ~70%.
2. **Set width**: Turn Streak W to ~40%. A luminous horizontal band appears across the image, brightest where the source is bright.
3. **Adjust intensity**: Sweep Threshold (Intensity) from minimum to maximum. Observe how the highlight grows from a subtle glow to a hot saturated stripe.
4. **Control falloff**: Sweep Intensity (Falloff) from sharp to gradual. Watch the streak's edges transition from hard-bordered to soft-feathered.
5. **Move the streak**: Slowly turn Streak L up and down. The band slides vertically across the frame, catching different tonal regions of the source as it passes.

**Key concepts**: The highlight band is additive — it boosts existing brightness rather than replacing it; streak width sets the spatial extent while falloff controls the edge profile; moving the streak position reveals how source content interacts with the highlight zone.

---

### Exercise 2: Gem Modes and Colour Tinting

<img src={chatoyant_exercise2_result} alt="Gem Modes and Colour Tinting result"/>
*Gem Modes and Colour Tinting — simulated result across source images.*
**Source**: Colourful footage with strong edges — a garden scene, textured fabrics, or stained glass.

**Objective**: Explore the four Gem Type orientations and add warm or cool chromatic tinting to the specular band.

1. **Prepare baseline**: Set Streak W ~50%, Threshold ~60%, Mix ~75%. Start with Gem Type = Tigers (free mode).
2. **Sweep the angle**: Turn Axis Ang slowly from 0° to 180°. The streak tilts across the frame, pivoting through various diagonals.
3. **Lock to horizontal**: Switch Gem Type to Star. The streak snaps to a horizontal band regardless of the Axis Ang setting.
4. **Lock to vertical**: Switch to Moon. The streak rotates to a vertical column of light.
5. **Try diagonal**: Switch to Opal. The streak settles at 45 degrees, cutting diagonally across the frame.
6. **Enable colour**: Toggle Color Hlt on. The highlight acquires a warm amber tint in warm mode. Observe how the tint intensifies with the highlight boost — strong specular areas glow golden while weaker areas remain nearly neutral.
7. **Adjust hue contribution**: Turn Hue Tint past centre. The streak begins responding to vertical edge structure in the source, creating a more textured, organic highlight pattern.

**Key concepts**: Gem Type selects the streak geometry — free mode gives continuous angle control while locked modes constrain to H/V/diagonal; colour tinting is proportional to highlight intensity, preserving source hue in weak highlights; gradient contribution adds surface-awareness to the highlight.

---

### Exercise 3: Animated Asterism

<img src={chatoyant_exercise3_result} alt="Animated Asterism result"/>
*Animated Asterism — simulated result across source images.*
**Source**: A high-contrast scene with mixed bright and dark areas — city lights at night, a sunlit landscape, or stage lighting.

**Objective**: Combine double-streak mirroring with animated sweep to create a shimmering asterism effect reminiscent of a star sapphire.

1. **Prepare twin streaks**: Set Streak W ~35%, Threshold ~70%, Mix ~80%. Enable Streaks = 2 (double streak). A mirrored pair of bands appears, symmetric about the frame centre.
2. **Start animation**: Toggle Anim on. The streak pair begins a slow bounce sweep, drifting from the centre toward the edges and back.
3. **Add colour**: Toggle Color Hlt on. The sweeping bands acquire chromatic tinting, creating twin coloured reflections that slide across the source.
4. **Try Opal mode**: Switch Gem Type to Opal (diagonal). The streaks lock to 45 degrees and sweep diagonally, crossing the frame at an angle.
5. **Widen and soften**: Increase Streak W to ~60% and set Intensity (Falloff) to maximum (gradual). The streaks become broad, soft glows that overlap as they approach the centre — creating a luminous crossover zone.
6. **Return to Tigers**: Switch back to free mode and sweep Axis Ang. The animated double streak tilts as you turn, creating a continuously evolving pattern of intersecting highlights.

**Key concepts**: Double-streak mirrors the primary highlight about the frame centre, producing symmetry from a single streak computation; animation adds temporal variation via a bounce accumulator; combining colour, animation, and multiple streaks builds complex asterism-like patterns.

---


## Tips

- **Start with Star mode**: Horizontal streaks are the easiest to understand. Place the band across a face or landscape horizon, then experiment with width and intensity before moving to free mode.
- **Source brightness matters**: The highlight is multiplicative with source luma — it boosts what is already bright. Feed high-contrast material for the most dramatic results; low-contrast sources produce subtler, more diffuse highlights.
- **Falloff shapes the character**: A sharp falloff with narrow width creates a laser-thin specular line. A gradual falloff with wide width creates a soft bloom. The combination of these two knobs determines whether the effect reads as a sharp reflection or a glowing aura.
- **Gradient for texture**: Turn Hue Tint past centre to fold vertical edge energy into the highlight. This makes the streak respond to surface detail — fabric weave, hair strands, architectural lines — rather than raw brightness alone.
- **Double for symmetry**: Double streak creates instant symmetry without needing to duplicate any processing. The two bands share the same width, intensity, and colour settings, so the look remains balanced.
- **Animate for life**: Even a slow sweep transforms a static highlight into a living shimmer. Combine animation with colour tinting for the full chatoyant experience — a warm band drifting across the frame like light across a polished cabochon.
- **Mix as master intensity**: Use the fader to balance the effect against the dry signal. A low mix (20–30%) adds a subtle specular sheen; a high mix (80–100%) makes the streak the dominant visual feature.
- **Combine modes freely**: Try animated double streaks in Opal mode with colour highlighting. The diagonal mirrored bands create an X-shaped pattern that sweeps back and forth — a simple but visually rich asterism.

---

## Glossary

| Term | Definition |
|------|------------|
| **Adularescence** | The billowy, floating light effect seen in moonstone, caused by light scattering from alternating layers of feldspar minerals within the gem. |
| **Asterism** | A star-shaped light pattern produced by multiple intersecting sets of fibrous inclusions in a gemstone, creating two or more chatoyant bands. |
| **BRAM (Block RAM)** | Dedicated memory blocks embedded in the FPGA fabric, used here for the dual-bank line buffer that stores previous-scanline luma. |
| **Cabochon** | A gemstone cut with a smooth, domed top and flat bottom (as opposed to faceted), the required shape for displaying chatoyancy. |
| **Chatoyancy** | The cat's-eye optical effect produced by parallel fibrous inclusions in a polished gemstone reflecting a single band of light perpendicular to the fibre axis. |
| **Falloff** | The rate at which highlight intensity diminishes with increasing distance from the streak centre, controlling the edge sharpness of the specular band. |
| **Line buffer** | A BRAM-based storage element that holds one complete scanline of video data, enabling comparison between the current and previous lines for gradient detection. |
| **Luma** | Short for luminance; the brightness component (Y channel) of a YUV video signal. |
| **Specular highlight** | A bright reflection of a light source on a surface, appearing as a localised region of increased brightness. |
| **UV colour plane** | The two-dimensional space defined by the U and V chrominance axes, in which hue and saturation are represented independently of brightness. |
| **Vertical gradient** | The absolute difference in luminance between a pixel and the pixel directly above it, used to detect horizontal edges and surface transitions. |
| **YUV** | A colour model that separates luminance (Y) from two chrominance components (U and V), widely used in video signal processing. |

---
