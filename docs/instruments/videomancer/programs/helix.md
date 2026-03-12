---
draft: true
sidebar_position: 135
slug: /instruments/videomancer/helix
title: "Helix"
image: /img/instruments/videomancer/helix/helix_hero.png
description: "Before digital displays, oscilloscopes were the only way to visualize electronic signals as images."
---

import helix_hero from '/img/instruments/videomancer/helix/helix_hero.png';
import helix_animation from '/img/instruments/videomancer/helix/helix_animation.gif';
import helix_control_panel from '/img/instruments/videomancer/helix/helix_control_panel.png';
import helix_exercise1_result from '/img/instruments/videomancer/helix/helix_exercise1_result.gif';
import helix_exercise2_result from '/img/instruments/videomancer/helix/helix_exercise2_result.gif';
import helix_exercise3_result from '/img/instruments/videomancer/helix/helix_exercise3_result.gif';

# Helix

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={helix_hero} alt="Helix hero image"/>
*Helix tracing a Lissajous curve with phosphor-decay afterglow and rainbow hue mapping.*
<img src={helix_animation} alt="Helix animated output"/>
*Helix output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Before digital displays, oscilloscopes were the only way to visualize electronic signals as images. By feeding sine waves of different frequencies into the horizontal and vertical deflection plates, an oscilloscope traces **Lissajous figures** — the looping, interlocking curves that became the visual signature of mid-century electronic music and science fiction. Helix recreates this aesthetic on the Videomancer platform, computing parametric curves during the vertical blanking interval and rendering them with a beam-and-phosphor model that faithfully emulates a CRT oscilloscope's visual behavior.

The name *Helix* refers to the spiraling three-dimensional appearance that Lissajous figures take on when the frequency ratio is non-integer — the path appears to twist through space like a helix, even though it is projected on a flat screen. The program also offers a true spiral mode where the curve's amplitude oscillates with the sample index, producing spirograph-like rosette patterns.

At conservative settings — low frequencies, wide beam, high afterglow — Helix produces a gently glowing, slowly rotating figure-eight or circle. At extreme settings — high frequencies, narrow beam, low afterglow, rainbow coloring — the screen fills with intricate, rapidly evolving curve structures that leave only the faintest phosphor trail behind them.

---

## Quick Start

1. **Frequency ratios are the key**: The visual complexity of a Lissajous figure is entirely determined by the ratio of Freq X to Freq Y. Start with simple ratios (1:1, 2:1, 3:2) and gradually increase complexity.
2. **Afterglow is accumulative**: High afterglow values cause the screen to fill over time. If the image becomes too dense, briefly set Afterglow to zero to clear the buffer, then raise it again.
3. **Phase Link creates coupled animation**: With Phase Link enabled, Hue Shift simultaneously rotates the color palette and the curve's spatial orientation — one knob drives two visual transformations.

---

## Background

### What Are Lissajous Figures?

In 1857, French physicist Jules Antoine Lissajous described the curves produced by combining two perpendicular sinusoidal motions. The simplest case uses equal frequencies: $X(t) = \cos(t)$, $Y(t) = \sin(t)$, which traces a circle. When the frequencies differ — $X(t) = \cos(a \cdot t + \varphi)$, $Y(t) = \sin(b \cdot t)$ — the resulting path loops and folds into complex figures whose shape depends on the frequency ratio $a:b$ and the phase offset $\varphi$. Integer ratios produce closed curves; non-integer ratios produce patterns that drift and evolve continuously. Helix computes 256 sample points of this parametric equation each frame, using a sin/cos lookup table and a DDS phase accumulator to animate the phase offset over time.

### What Is Phosphor Afterglow?

On a real CRT oscilloscope, the electron beam excites phosphor coating on the inside of the screen. The phosphor glows at the point of impact and then fades over time — this is **phosphor persistence** or afterglow. Short-persistence phosphors (P1, green) fade in microseconds, producing sharp traces. Long-persistence phosphors (P7, blue-white) glow for seconds, leaving visible trails. Helix simulates this by maintaining a per-column brightness buffer. Each frame, the buffer is decayed by multiplying by the Afterglow parameter (IIR feedback), then max-blended with the new beam brightness. High afterglow values produce long glowing trails; low values produce a sharp dot that fades quickly.

### What Is Beam Falloff?

A real oscilloscope beam is not a mathematical point — it has a physical width determined by the electron optics. Pixels near the center of the beam are brighter than pixels at the edge. Helix models this with a distance-based falloff function. In **Soft** mode, brightness decreases linearly with distance from the curve: $\text{brightness} = \max(0, W - d) / W$, where $W$ is the beam width and $d$ is the distance. In **Hard** mode, all pixels within the beam width are at full brightness — a binary threshold. Hard mode produces crisp lines; soft mode produces anti-aliased glowing traces.

### What Is a Phase Accumulator?

Helix animates its curves using a **phase accumulator** — a register that increments by a fixed amount each frame. The accumulated value becomes the phase offset $\varphi$ in the Lissajous equation, causing the curve to rotate and evolve over time. The Speed control sets the increment value. At zero the curve is static; at maximum it evolves rapidly. Because the accumulator wraps around at its maximum bit width, the animation repeats after a very long cycle — long enough that the repetition is imperceptible. The Phase Link toggle add the Hue Shift offset to the X phase, coupling the color rotation to the curve's spatial rotation.


---

## Signal Flow

Phase Accumulator Update → Parametric Sample Loop → Coordinate Setup → ... → Output Compose → Interpolator × 3

```
Vertical Blanking ──────────────────────────────────────────────
│
├─ 1. Phase Accumulator Update      (speed increment per frame)
├─ 2. Parametric Sample Loop ×256   (4-phase state machine)
│      ├─ Phase 0: X angle → sin_cos_full_lut_10x10
│      ├─ Phase 1: Read cos → X pixel, Y angle → LUT
│      ├─ Phase 2: Read sin → Y pixel, write to curve BRAM
│      └─ Phase 3: Advance sample index
│
Active Video ───────────────────────────────────────────────────
│
├─ 3. Coordinate Setup              (read curve Y from BRAM)
├─ 4. Distance Computation          (|v_count - curve_y|)
├─ 5. Beam Falloff                   (Soft=linear, Hard=step)
├─ 6. Afterglow Blend               (IIR decay → max blend)
├─ 7. Color Mapping                  (Mono=green, Rainbow=H+shift)
├─ 8. Output Compose                (Y, U, V assignment)
│
├─ Mix Stage ───────────────────────────────────────────────────
│   └─ 9. Interpolator × 3          (wet/dry crossfade, 4 clocks)
│
├─ Sync Signals ────────────────────────────────────────────────
│   └─ Delay-aligned pass-through (6 clocks)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

Helix divides its work into two temporal phases. During the **vertical blanking interval**, the curve sample loop runs a 4-phase state machine 256 times, computing parametric curve coordinates and writing the Y position of the nearest curve point into a BRAM indexed by X column. This precomputation avoids the need to evaluate trigonometric functions at pixel rate during active video. During **active video**, each pixel reads its column's curve-Y value from BRAM, computes the vertical distance to the curve, applies beam falloff, blends with the decayed afterglow buffer, and maps the final brightness to a color. The afterglow buffer is a second BRAM that persists across scanlines within a frame — the IIR decay operates per-column per-scanline, so vertical persistence trails appear naturally. Color mapping differs between Mono (green phosphor tint derived from brightness) and Rainbow (hue derived from horizontal position plus the Hue Shift offset). The Spiral mode modulates amplitude by sample index, producing expanding/contracting patterns unlike Lissajous's fixed-radius motion.

---

## Parameter Reference

<img src={helix_control_panel} alt="Videomancer front panel with Helix loaded"/>
*Videomancer's front panel with Helix active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Freq X
| Property | Value |
|----------|-------|
| Range | 1 – 16 |
| Default | 3 |

Sets the X-axis frequency of the parametric curve as a stepped selector from 1 to 16. This is the coefficient $a$ in $X(t) = \cos(a \cdot t + \varphi)$. The frequency ratio between Freq X and Freq Y determines the fundamental Lissajous pattern — equal frequencies produce circles or ellipses, a 2:1 ratio produces a figure-eight, a 3:2 ratio produces a trefoil. At higher frequencies the curve has more lobes, and at non-integer ratios the figure drifts open and never exactly closes.

---

#### Knob 2 — Freq Y
| Property | Value |
|----------|-------|
| Range | 1 – 16 |
| Default | 5 |

Sets the Y-axis frequency from 1 to 16, the coefficient $b$ in $Y(t) = \sin(b \cdot t)$. Changing Freq Y while keeping Freq X fixed transforms the Lissajous figure's topology. A 1:1 ratio produces a circle (or ellipse with phase offset), 1:2 produces a figure-eight rotated 90 degrees from the 2:1 case, and higher ratios produce increasingly complex patterns. In Spiral mode, the frequency still determines the oscillation rate, but the amplitude modulation creates spiraling petals instead of closed loops.

---

#### Knob 3 — Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 20% |
| Suffix | % |

At zero the curve is frozen in place — useful for studying a static Lissajous pattern. As Speed increases, the phase offset $\varphi$ advances faster each frame, causing the curve to rotate, breathe, and evolve. The visual effect depends strongly on the frequency ratio: integer ratios produce periodic rotations while non-integer ratios produce aperiodic drift. High Speed values combined with high afterglow create dense, glowing traces that fill the screen. Internally, controls the phase accumulator increment.

---

#### Knob 4 — Beam Width
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 29% |
| Suffix | % |

Sets the beam width — the distance from the curve within which pixels are illuminated. Narrow beams produce fine, precise lines; wide beams produce thick, diffuse traces. In Soft mode, beam width controls the falloff zone — brighter at center, dimming to zero at the edge. In Hard mode, beam width defines the binary threshold — all pixels within the width are at full brightness. The beam width is computed from the upper 6 bits of the register, giving approximately 1 to 64 pixels of width.

---

#### Knob 5 — Afterglow
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 59% |
| Suffix | % |

At zero, only the current frame's beam is visible — no persistence. As afterglow increases, previous frames' beam positions fade more slowly, leaving glowing trails behind the moving curve. At maximum, the trails barely fade at all, and the screen fills with accumulated brightness over time. The IIR computation multiplies the previous glow value by the afterglow register and shifts right by 10 bits — at the maximum value of 1023, the decay is nearly unity and trails persist indefinitely. Internally, controls the IIR afterglow decay factor.

---

#### Knob 6 — Hue Shift
| Property | Value |
|----------|-------|
| Range | 0d – 360d |
| Default | 0d |
| Suffix | d |

Rotates the color palette by the specified angle. In Rainbow mode, the base hue is derived from horizontal screen position — this control shifts that mapping, so red might start at the left edge, center, or right edge depending on the setting. In Mono mode, hue shift has no visible effect because the green phosphor tint is derived solely from brightness. When Phase Link is enabled, this offset is also added to the X-axis phase accumulator, coupling color rotation and spatial rotation into a single control.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Curve** | Lissajous | Spiral |
| **8 — Beam** | Soft | Hard |
| **9 — Color** | Mono | Rainbow |
| **10 — Phase Link** | Free | Linked |
| **11 — Bypass** | Off | On |

Switches 7–10 control four independent aspects of the curve synthesis. Switch 7 selects the parametric curve type (Lissajous vs Spiral). Switch 8 selects the beam rendering model (Soft vs Hard). Switch 9 selects the color mode (Mono vs Rainbow). Switch 10 enables phase linking, which couples Hue Shift to the curve's X phase. Switch 11 is the standard bypass. These are fully independent binary options — each controls one aspect of the synthesis chain without affecting the others.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Crossfades between the pass-through video input (dry) and the generated Lissajous/spiral output (wet) via three interpolator instances. At maximum the generated curve is at full strength on a black background. At minimum the output is the unmodified input video. Intermediate values superimpose the curve as a translucent overlay on the input signal — useful for compositing Lissajous graphics over live video.


#### Switch 11 — Bypass
| Property | Value |
|----------|-------|
| Off | Processing active |
| On | Bypass engaged |

Routes the unprocessed input signal directly to the output, bypassing all Helix processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.---
## Guided Exercises

These exercises progress from a simple static Lissajous figure to a complex, color-cycling spirograph with long afterglow trails.

### Exercise 1: Classic Lissajous Figures

<img src={helix_exercise1_result} alt="Classic Lissajous Figures result"/>
*Classic Lissajous Figures — simulated result across source images.*
**What You'll Create**: Explore how Freq X and Freq Y ratios determine the shape of Lissajous figures.

1. **Circle**: Set Freq X to 1 and Freq Y to 1 with Speed at 0%. A stationary circle (or ellipse) appears at the center of the screen.
2. **Figure-eight**: Change Freq X to 2 while keeping Freq Y at 1. The circle transforms into a figure-eight pattern.
3. **Trefoil**: Set Freq X to 3, Freq Y to 2. A three-lobed trefoil pattern appears.
4. **Complex ratios**: Try Freq X = 5, Freq Y = 4. Count the lobes — the pattern becomes increasingly intricate with higher frequency ratios.
5. **Animation**: Slowly increase Speed from 0%. Watch the curve rotate and evolve. Integer frequency ratios produce periodic rotations; non-integer ratios produce drifting patterns.
6. **Beam width**: Sweep Beam Width from minimum to maximum. Narrow beams produce fine mathematical traces; wide beams produce thick, glowing shapes.

**Key concepts**: Lissajous figures are determined by frequency ratio, phase offset animates the curve orientation, beam width controls trace thickness

---

### Exercise 2: Phosphor Afterglow and Beam Modes

<img src={helix_exercise2_result} alt="Phosphor Afterglow and Beam Modes result"/>
*Phosphor Afterglow and Beam Modes — simulated result across source images.*
**What You'll Create**: Understand how the IIR afterglow system creates persistence trails and how beam mode affects their appearance.

1. **No afterglow**: Set Afterglow to 0%. Only the current frame's curve is visible — a sharp, flickering trace with no trail.
2. **Short persistence**: Increase Afterglow to ~30%. A short tail appears behind the moving curve, like a P1 phosphor.
3. **Long persistence**: Increase Afterglow to ~80%. The entire recent history of the curve's path is visible as a fading trail. The screen fills with glowing traces over time.
4. **Soft vs Hard beam**: With moderate afterglow (~50%), switch between Soft and Hard beam modes. Soft produces smooth, anti-aliased trails with varying brightness. Hard produces crisp, uniform-brightness trails.
5. **Near-infinite persistence**: Set Afterglow to ~95%. Previous traces barely fade. The screen slowly fills with accumulated curve positions, creating dense, complex textures.

**Key concepts**: IIR afterglow decays previous frame brightness exponentially, Soft beam creates gradient falloff while Hard beam creates binary traces, high afterglow accumulates history

---

### Exercise 3: Rainbow Spirograph

<img src={helix_exercise3_result} alt="Rainbow Spirograph result"/>
*Rainbow Spirograph — simulated result across source images.*
**What You'll Create**: Combine Spiral mode, Rainbow color, Phase Link, and high afterglow for maximum visual complexity.

1. **Enable Spiral mode**: Switch Curve to Spiral. The fixed-radius Lissajous transforms into a spirograph rosette with oscillating amplitude.
2. **Rainbow color**: Switch Color to Rainbow. The monochromatic green trace becomes a spectrum sweep from left to right.
3. **Hue Shift rotation**: Slowly sweep Hue Shift through its full range. Watch the color palette rotate. The left-to-right gradient shifts its starting hue.
4. **Phase Link**: Enable Phase Link. Now Hue Shift also affects the curve's spatial orientation — rotating both color and shape simultaneously.
5. **High frequency**: Set Freq X to 7, Freq Y to 5 for a complex multi-lobed rosette.
6. **Maximize afterglow**: Set Afterglow to ~90%. The spiral's history accumulates on screen, creating a dense mandala of interlocking colored traces.
7. **Speed variation**: Increase Speed to ~60% to watch the pattern evolve rapidly, leaving trails in every hue.

**Key concepts**: Spiral mode modulates amplitude by sample index, Rainbow maps hue to horizontal position, Phase Link couples color and spatial orientation, high afterglow creates accumulated trace mandalas

---


## Tips

- **Spiral mode breaks Lissajous symmetry**: Where Lissajous figures have uniform radii, Spiral mode creates rosettes with petals of varying size. This produces more organic, less geometric patterns.
- **Beam width vs afterglow tradeoff**: Wide beams with high afterglow quickly saturate the screen to white. Use narrow beams when afterglow is high, or wide beams when afterglow is low.
- **Feedback loops**: Routing Helix's output back to its input adds video-reactive brightness to the generated curves — the afterglow trails interact with themselves, creating evolving recursive patterns.
- **Bypass for A/B comparison**: Switch 11 instantly shows the pass-through video for before/after evaluation.
- **Compositing overlay**: Set Mix to ~50% to superimpose the Lissajous trace over live video, creating an oscilloscope-on-video effect.

---

## Glossary

| Term | Definition |
|------|------------|
| **Afterglow** | The visible persistence of phosphor excitation after the electron beam has passed, simulated here via IIR feedback on a per-column brightness buffer. |
| **DDS** | Direct Digital Synthesis; generating a periodic waveform by incrementing a phase accumulator and indexing a lookup table. |
| **Falloff** | The rate at which beam brightness decreases with distance from the curve center; linear in Soft mode, step function in Hard mode. |
| **IIR** | Infinite Impulse Response; a feedback filter whose output depends on both current input and its own previous output. |
| **Lissajous figure** | A parametric curve produced by combining two perpendicular sinusoidal motions at different frequencies; named after Jules Antoine Lissajous (1857). |
| **LUT** | Lookup Table; a precomputed array of function values. Helix uses a 1024-entry sin/cos LUT for parametric curve evaluation. |
| **Phase accumulator** | A register that increments by a fixed value per frame; its running total provides the continuously advancing phase for curve animation. |
| **Phosphor persistence** | The duration a CRT phosphor continues to glow after excitation; Helix simulates this with IIR decay. |
| **Spirograph** | A geometric drawing toy that produces hypotrochoid and epitrochoid curves; Helix's Spiral mode produces similar rosette patterns. |

---
