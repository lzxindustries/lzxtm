---
draft: true
sidebar_position: 88
slug: /instruments/videomancer/doodle
title: "Doodle"
image: /img/instruments/videomancer/doodle/doodle_hero.png
description: "Doodle is an autonomous pixel-drawing synthesis inspired by the Cromemco Dazzler's DAZZLER-DOODLE program from 1976."
---

import doodle_hero from '/img/instruments/videomancer/doodle/doodle_hero.png';
import doodle_animation from '/img/instruments/videomancer/doodle/doodle_animation.gif';
import doodle_control_panel from '/img/instruments/videomancer/doodle/doodle_control_panel.png';
import doodle_exercise1_result from '/img/instruments/videomancer/doodle/doodle_exercise1_result.gif';
import doodle_exercise2_result from '/img/instruments/videomancer/doodle/doodle_exercise2_result.gif';
import doodle_exercise3_result from '/img/instruments/videomancer/doodle/doodle_exercise3_result.gif';

# Doodle

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={doodle_hero} alt="Doodle hero image"/>
*Doodle tracing Lissajous curves across the 64x64 Cromemco RGBI framebuffer, leaving trails of bright cyan, yellow, and red that slowly dissolve as the wipe sweeps new space for the next figure.*
<img src={doodle_animation} alt="Doodle animated output"/>
*Doodle output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Doodle is an autonomous pixel-drawing synthesis inspired by the Cromemco Dazzler's DAZZLER-DOODLE program from 1976. Where Kaleidoscope placed pixels through iterated coordinate feedback and four-way symmetry, DAZZLER-DOODLE handed that power directly to the user: with a joystick, you steered a drawing cursor through the Dazzler's 64x64 RGBI framebuffer, laying down trails of phosphor color across the chunky grid. Doodle reinvents this experience for Videomancer as pure synthesis — an invisible cursor follows Lissajous curves driven by two independent phase oscillators, painting continuous trails through the same 16-color classic palette. No user steering required; the curves unfold on their own, and a slow sequential wipe erases old marks as new ones accumulate.

The engine runs two phases per frame. In the draw phase, two 16-bit phase accumulators advance at independently selectable rates. Their values are folded through a triangle-wave function — when the accumulator's most significant bit is zero, the cursor rises from 0 to 63; when it flips to one, the value inverts and falls back from 63 to 0. The ratio of the two accumulator rates determines the Lissajous figure traced: integer ratios close simple curves (1:1 is a diagonal, 2:1 traces a figure-eight, 3:2 traces a trefoil), while irrational-like ratios produce slowly rotating, never-quite-repeating paths that fill the framebuffer over time. Colors advance through the 16-entry RGBI palette at a rate set by the Color Rate knob, so each closed Lissajous loop typically spans several palette entries. In the wipe phase, a clearing cursor sweeps a row of cells back to black — erasing the oldest marks and making room for the drawing to continue its cycle.

The Auto Freq mode adds a fourth oscillator layer: two slow background accumulators increment at different rates each vsync, slowly sweeping the effective Freq X and Freq Y values across all 16 possible settings. Over roughly 30 seconds, the Lissajous figure evolves from simple closed loops through increasingly complex figures and back again — a continuous, unattended demonstration exactly in the spirit of the original Dazzler showroom demos that once stopped Fifth Avenue traffic.

---

## Quick Start

1. **Try coprime ratios**: Set Freq X and Freq Y to values with no common factors (e.g., 3 and 7, 5 and 9, 4 and 11) for the most complex and slowly-repeating Lissajous figures. These take the longest to close and fill the most of the framebuffer.
2. **The 90-degree offset matters**: The initial phase_y offset of 16384 (one quarter of the 16-bit range) seeds a 90-degree phase difference at startup. This produces clean ellipses and figure-eights from the first draw step rather than degenerate diagonal lines. Toggle Reset to start fresh from this seeded state.
3. **Match Wipe Rate to Speed**: For a stable, rolling display where the framebuffer stays roughly half-full, set Wipe Rate to about half the Speed value. When Wipe Rate significantly exceeds Speed, marks disappear faster than they form and the display stays sparse.

---

## Background

### DAZZLER-DOODLE and the Birth of the Paint Program

The Cromemco Dazzler's software library in 1976 included several programs sold on paper tape. The most famous was Li-Chen Wang's Kaleidoscope, but the package also contained DAZZLER-DOODLE: a freehand drawing tool driven by a joystick connected to the D+7A I/O board's analog inputs. Users could steer a drawing cursor across the 64x64 RGBI framebuffer, change colors at will, and erase the screen with a button press. In an era without mice, touchscreens, or GUI paradigms, this was an astonishingly direct creative experience. DAZZLER-DOODLE anticipated the paint programs of the late 1970s and early 1980s — SuperPaint, MacPaint — by enabling spontaneous, freehand mark-making on a video screen in real time.

### Jules-Antoine Lissajous and Compound Harmonic Motion

The Lissajous figure was first demonstrated systematically by French physicist Jules-Antoine Lissajous in 1857 using a two-mirror optical system that projected reflected candlelight through vibrating tuning forks. By directing perpendicular oscillations of different frequencies onto a screen, the compound motion traced beautiful closed curves — ellipses, figure-eights, trefoils, stars — whose shape depended entirely on the frequency ratio and phase offset between the two oscillators. The figures became a standard demonstration in acoustics and mechanics labs, and later in electronics where oscilloscopes could display them by feeding two sinusoidal signals to the X and Y deflection plates.

### Triangle-Wave Lissajous Without Trigonometry

Classical Lissajous figures use sine waves, requiring either lookup tables or power-series approximations in digital systems. Doodle instead uses triangle waves — linear ramps produced by folding a binary counter at its midpoint. When a 16-bit accumulator's most significant bit is zero, the lower 6 bits give a direct rising ramp from 0 to 63. When the MSB flips to one, the lower 6 bits are bitwise-inverted, producing a falling ramp from 63 to 0. This fold operation is a single NOT gate in hardware — computationally trivial, requiring no multipliers, no lookup tables, and no intermediate registers beyond the accumulator itself. The resulting curves are Lissajous-like in structure but with the characteristic flat top/bottom of triangle waves instead of the smooth apex of sinusoids, giving the figures a slightly angular appearance that suits the pixel aesthetic.

### The 64×64 RGBI Framebuffer

The Cromemco Dazzler's 64x64 pixel mode organized its 2 KB frame buffer as four 32x32 pages, addressed with 6 bits per axis and 4 bits for color. The RGBI encoding used three bits for the base hue (eight combinations of red, green, and blue, including black and white) plus an intensity bit that doubled the luminance, producing 16 entries total. In practice the two blacks and two grays are nearly indistinguishable; the distinctive colors are the eight dim primaries and secondaries plus their eight bright variants. Doodle stores this 64x64x4-bit palette directly in four FPGA block RAMs (4 Kbits each, 16 Kbits total), then maps each cell to a 30x16 pixel block on the full 1920x1080 output — recreating the Dazzler's characteristic chunky, oversized-pixel aesthetic on modern HD video infrastructure.

### The Wipe as Generative Rhythm

DAZZLER-DOODLE had a clear screen button: one press wiped the entire framebuffer instantly. Doodle replaces this with a gradual sequential wipe — a clearing cursor that sweeps through the framebuffer row by row, writing black to each cell at a rate controlled by the Wipe Rate knob. At low wipe rates, drawings accumulate for many seconds before old marks begin to disappear; at high rates, the trailing edge of the wipe catches up to the drawing cursor and the screen never fills. The relationship between draw speed, Lissajous frequency, and wipe rate creates a three-body rhythm: the drawing cursor lays marks, the color cycle changes their identity, and the wipe erases them. When these three rates are in rough correspondence, the display appears to breathe — patterns emerge, color, age, and dissolve in a continuous cycle that mirrors the seasonal, cyclical quality of true doodle-making.


---

## Signal Flow

```
Synthesis Engine
|
+-- Parameter Mapping ------------------------------------------------
|   +- registers_in(0)  -> Speed (draw iterations per frame)
|   +- registers_in(1)  -> Freq X (X-axis phase rate 1-16)
|   +- registers_in(2)  -> Freq Y (Y-axis phase rate 1-16)
|   +- registers_in(3)  -> Color Rate (steps between color advance)
|   +- registers_in(4)  -> Wipe Rate (cells erased per frame)
|   +- registers_in(5)  -> Brightness (palette Y channel scale)
|   +- registers_in(6)  -> Toggles (run, auto_freq, reset, grid, bypass)
|   +- registers_in(7)  -> Mix
|
+-- Per-Vsync Engine (when Run active) --------------------------------
|   +-- Draw Phase (iters_per_frame iterations) --
|   |   +- 1. Phase Advance
|   |   |      phase_x += eff_freq_x   (16-bit, wraps)
|   |   |      phase_y += eff_freq_y   (16-bit, wraps)
|   |   +- 2. Triangle-Wave Fold
|   |   |      if phase_x[15]='0': cursor_x = phase_x[14:9]
|   |   |      if phase_x[15]='1': cursor_x = NOT phase_x[14:9]
|   |   |      (same for Y)
|   |   +- 3. Framebuffer Write
|   |   |      FB[cursor_y, cursor_x] := color_idx
|   |   +- 4. Color Advance
|   |          color_step++; if color_step >= color_rate:
|   |          color_idx := (color_idx % 15) + 1   (wraps 15->1, skip 0)
|   +-- Wipe Phase (wipes_per_frame cells) --
|       +- 5. Wipe Write
|       |      FB[wipe_row, wipe_col] := 0 (black)
|       +- 6. Wipe Advance
|              wipe_col++; if wipe_col=64: wipe_col=0, wipe_row++
|
+-- Auto Freq (once per vsync when Auto Freq active) -----------------
|   +- osc_x += 1  →  eff_freq_x = osc_x[9:6] + 1   (1-16)
|   +- osc_y += 3  →  eff_freq_y = osc_y[9:6] + 1   (1-16)
|
+-- Framebuffer (64x64 x 4-bit) -------------------------------------
|   +- Write: engine writes one pixel per clock during blanking
|   +- Read:  rasterizer reads sequentially during active video
|
+-- Rasterizer (per pixel) ------------------------------------------
|   +- 7. Cell Lookup      (cell_col, cell_row -> FB read address)
|   +- 8. Palette LUT      (4-bit index -> 10-bit YUV)
|   +- 9. Brightness Scale (palette Y * bright_pot / 1024)
|   +- 10. Grid Lines      (cell_px=0 or cell_py=0, when enabled)
|
+-- Output Stage ----------------------------------------------------
|   +- 11. Interpolator Mix (3x interpolator_u wet/dry)
|
+-- Sync Pipeline ---------------------------------------------------
|   +- 8-clock shift register (hsync, vsync, avid, field)
|
+-- Bypass ----------------------------------------------------------
    +- Select processed or input signal
```

The engine FSM has two sequential phases per frame. Phase 0 (draw) runs first, executing `speed_pot >> 3` cursor steps — each step advances both phase accumulators and writes the current color to the framebuffer at the computed triangle-wave position. Phase 1 (wipe) follows immediately, clearing `wipe_rate >> 4` cells to black by advancing a row/column pointer through the framebuffer linearly. The wipe pointer persists across frames — it remembers where it left off and continues from that row and column in the next frame's wipe phase.

The Auto Freq mode updates `eff_freq_x` and `eff_freq_y` once per vsync, deriving them from the top 4 bits of two 10-bit counters that accumulate at 1 and 3 per vsync respectively. This produces independent sweep rates: `eff_freq_x` cycles through all 16 values in 1024 frames (~34 seconds at 30fps), while `eff_freq_y` cycles in approximately 341 frames (~11 seconds). Their different periods mean the Lissajous figure ratio changes continuously, producing slow rotations through the entire catalog of 256 frequency-pair combinations over the course of several minutes.

---

## Parameter Reference

<img src={doodle_control_panel} alt="Videomancer front panel with Doodle loaded"/>
*Videomancer's front panel with Doodle active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Speed controls how many draw iterations execute each frame during the vsync blanking interval. The top 7 bits of the pot value are used directly, giving a range of 0 to 127 steps per frame. At minimum speed, the cursor advances so slowly that individual pixel placements can be watched one by one — useful for studying a specific Lissajous figure without the completed curve obscuring the motion path. At maximum speed, 127 pixels are placed per frame and complex figures fill rapidly. For sustained doodling at a pace resembling handheld drawing, moderate settings around 30–50% work well.

---

#### Knob 2 — Freq X
| Property | Value |
|----------|-------|
| Range | 1 – 16 |
| Default | 2 |

Freq X controls the rate at which the X-axis phase accumulator advances each draw step. It operates in 16 equal steps (step mode), giving integer rates from 1 to 16. Freq X alone does not determine the figure's shape — only the ratio of Freq X to Freq Y matters. Rate 1 is the slowest X oscillation; rate 16 is the fastest. When Freq X and Freq Y are equal, the cursor traces a diagonal line. When their difference is small (e.g., 3 and 4), the figure is a low-complexity closed curve; when the ratio is coprime with no common factors, the figure takes many cycles to close. This control is ignored when Auto Freq is active.

---

#### Knob 3 — Freq Y
| Property | Value |
|----------|-------|
| Range | 1 – 16 |
| Default | 4 |

Freq Y controls the rate at which the Y-axis phase accumulator advances each draw step, in the same 16-step range as Freq X. The key parameter is the ratio Freq X : Freq Y. A ratio of 1:2 produces a symmetric figure-eight (parabola). A ratio of 1:3 traces a trefoil. A ratio of 2:3 produces a complex oval-and-loop figure. Ratios with large common factors repeat quickly; ratios where gcd(Freq X, Freq Y) = 1 produce the most intricate closed figures. Exploring the 16×16 grid of Freq X and Freq Y combinations yields 256 distinct figure types — the Doodle's full vocabulary of shapes. This control is ignored when Auto Freq is active.

---

#### Knob 4 — Color Rate
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Color Rate controls how many draw steps pass before the system advances to the next palette color. When Color Rate is low, colors change rapidly — each segment of the Lissajous curve gets a different color, creating a rainbow stripe effect as the figure fills in. When Color Rate is high, the cursor paints long segments in the same color before advancing — producing bold, single-color loops. The 10-bit pot maps directly to this step counter: a value of 512 advances the color approximately every 512 draw steps, which at moderate Speed covers several frames and roughly one full Lissajous cycle for simple frequency ratios.

---

#### Knob 5 — Wipe Rate
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |
| Suffix | % |

Wipe Rate controls how many framebuffer cells the clearing cursor erases each frame. The top 6 bits of the 10-bit pot value determine the wipe count per frame, giving a range of 0 to 63 cells. At zero wipe rate, marks accumulate indefinitely until the framebuffer fills completely with the most recent color. At low wipe rates, drawings persist for many seconds before the clearing wave overtakes them. At high wipe rates, the wipe consumes cells faster than the draw cursor places them, keeping the screen partially clear and producing a more dynamic, transient appearance. The wipe cursor position persists between frames, continuing its sequential row-by-row sweep without gaps.

---

#### Knob 6 — Bright
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Bright scales the luminance of all palette colors before output. The palette Y value is multiplied by the Bright pot value (10-bit), and the top 10 bits of the 20-bit product are used as the output Y. At maximum brightness, the white palette entry approaches full signal level. At minimum, the display fades to black regardless of the drawn pattern. For most display contexts, settings between 70% and 85% produce vivid Dazzler-authentic luminance levels matching the look of phosphor-illuminated CRT screens rather than the clipped, blown-out maximum of modern displays.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Run** | Pause | Run |
| **8 — Auto Freq** | Manual | Auto |
| **9 — Reset** | Off | Reset |
| **10 — Grid** | Off | On |
| **11 — Bypass** | Active | Bypass |

The five toggles divide into two operational groups and one display group. Run and Reset control engine execution: Run gates the per-frame engine activation, and Reset re-initializes the phase accumulators and color state on its rising edge (it is edge-triggered, not level-sensitive). Auto Freq selects the frequency source: in Auto mode the internal oscillators drive Freq X and Freq Y, sweeping the Lissajous catalog automatically; in Manual mode the Freq X and Freq Y knobs provide direct control. Grid and Bypass are display modifiers: Grid draws cell boundary lines over the Doodle output, and Bypass routes input video directly through — useful for A/B comparisons or hiding the doodle while preserving its runtime state.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Mix controls the wet/dry blend between the Doodle synthesis output and the input video signal, interpolated independently across Y, U, and V channels via three `interpolator_u` instances. At full mix (fader up), only the Doodle framebuffer is visible against a black background. Pulling the fader toward zero fades the input video up behind and through the Doodle marks, creating an effect where Lissajous trails appear to be drawn on top of source footage. At moderate mix positions, the Doodle appears as a semi-transparent colored overlay — the chunky RGBI colors wash across the underlying video in a way that aesthetically echoes hand-painted animation cel overlays.



> See [Common Controls & Glossary Reference](../common_reference.md) for details.

---

## Guided Exercises

These exercises explore the Doodle's Lissajous figure vocabulary, the relationship between drawing speed and wipe rate, and the use of Auto Freq mode for evolving pattern sequences.

### Exercise 1: Geometric Figure-Eight

<img src={doodle_exercise1_result} alt="Geometric Figure-Eight result"/>
*Geometric Figure-Eight — simulated result across source images.*
**What You'll Create**: Produce a clean, slowly traced figure-eight curve in multiple colors using a 1:2 Lissajous ratio, letting the curve complete several color cycles before the wipe erases it.

1. Set Auto Freq to Manual.
2. Set Freq X to step 3 (approximately 28%) and Freq Y to step 6 (approximately 59%) — ratio 1:2 traces a figure-eight.
3. Set Speed to about 35% for a slow, deliberate trace.
4. Set Color Rate to about 40% for visible color changes within each pass.
5. Set Wipe Rate to about 15% so marks persist for multiple seconds.
6. Set Brightness to 80%.
7. Set Run to Run.
8. Toggle Reset, then return Reset to Off.
9. Observe the figure-eight form as two looping arcs in sequential palette colors. Watch the wipe gradually clear one end of the figure while the cursor continues drawing.
10. Increase Freq X to step 4 and watch the figure transform into a more complex knotted shape.

**Key concepts**: Lissajous frequency ratio, triangle-wave folding, figure-eight figure, color cycling rate, persistent trails

---

### Exercise 2: Dense Fill and Fast Wipe

<img src={doodle_exercise2_result} alt="Dense Fill and Fast Wipe result"/>
*Dense Fill and Fast Wipe — simulated result across source images.*
**What You'll Create**: Use a high-speed draw with an irrational-like frequency ratio and aggressive wipe rate to produce a space-filling, continuously dissolving doodle that never settles into a static composition.

1. Set Auto Freq to Manual.
2. Set Freq X to step 5 (approximately 40%) and Freq Y to step 8 (approximately 75%) — ratio 5:8 produces a complex Lissajous with many loops.
3. Set Speed to about 80% for rapid filling.
4. Set Color Rate to about 20% for rapid color cycling within each trace.
5. Set Wipe Rate to about 55% so the clearing wave moves quickly across the framebuffer.
6. Set Brightness to 85%.
7. Set Run to Run.
8. Observe: the high speed fills large regions quickly while the aggressive wipe prevents saturation. The result should look like colored ribbons perpetually forming and dissolving.
9. Try enabling Grid to see the discrete Dazzler pixel structure of the fast-moving trails.

**Key concepts**: Dense space-filling paths, draw-wipe balance, fast wipe transience, ribbon aesthetics, grid reveal

---

### Exercise 3: Auto Freq Slow Evolution

<img src={doodle_exercise3_result} alt="Auto Freq Slow Evolution result"/>
*Auto Freq Slow Evolution — simulated result across source images.*
**What You'll Create**: Use Auto Freq mode for an unattended, continuously evolving Lissajous sequence — observe the full progression from simple figures through complex ones and back, with slow color cycling and moderate wipe for a meditative rolling display.

1. Set Auto Freq to Auto.
2. Set Speed to about 40% for a moderate trace pace.
3. Set Color Rate to about 60% so colors change slowly — each figure form will have a characteristic palette.
4. Set Wipe Rate to about 25% for gentle erasure that allows figures to build up before disappearing.
5. Set Brightness to 90% for vivid, well-saturated colors.
6. Enable Grid for visible cell separation.
7. Set Run to Run.
8. Toggle Reset, then return to Off.
9. Let the program run for at least 90 seconds. The Auto Freq oscillators sweep independently, so the Lissajous ratio changes continuously: observe simple closed figures alternating with complex open paths alternating with space-filling near-chaotic traces.
10. Note the moments when the Y oscillator (faster, cycling at 1/3 the period) and X oscillator (slower) align on the same value — these produce the diagonal-line figure (1:1 ratio).

**Key concepts**: Auto freq sweep, independent oscillator rates, Lissajous catalog, ratio alignment, unattended generative loop

---


## Tips

- **Low Color Rate for rainbow trails**: Set Color Rate below 15% for multi-color trails that change hue many times along each Lissajous curve. This produces the most visually festive and DAZZLER-DOODLE-authentic appearance.
- **Auto Freq for installation**: Auto Freq mode produces a continuously evolving, 30+ minute cycle of figure variations without any user interaction. It is ideal for projection environments where the program must run unattended for hours.
- **Grid reveals the pixel structure**: Enable the Grid overlay to make the 64×64 framebuffer grid visible. At close viewing distances or on large screens, this recreates the tactile, pixelated character of actually looking at a Dazzler-connected CRT.
- **Partial mix for textured overlays**: Reduce Mix to 30–50% to blend Doodle marks as a translucent colored overlay on input video. The chunky RGBI palette creates a stained-glass effect over video content — particularly striking with natural imagery.
- **Reset without clearing**: Because Reset does not erase the framebuffer, toggling it while a figure is in mid-trace creates layered palimpsest effects where old and new Lissajous figures coexist until the wipe cycles through the shared cells.

---

## Glossary

| Term | Definition |
|------|------------|
| **Accumulator** | A register that is repeatedly added to; the 16-bit phase accumulators in Doodle wrap freely, producing continuous cycling motion without boundary checks. |
| **Cromemco Dazzler** | The 1976 S-100 bus graphics card that gave personal computers their first color framebuffer, displayed at 64×64 pixels in 16-color RGBI mode. |
| **CRT** | Cathode-ray tube; the display technology used with the original Cromemco Dazzler, whose phosphor glow and slight overscan characterize the aesthetic Doodle references. |
| **DAZZLER-DOODLE** | The freehand drawing program sold by Cromemco for the Dazzler, allowing joystick-driven cursor painting across the 64×64 RGBI framebuffer. |
| **GCD** | Greatest common divisor; when gcd(Freq X, Freq Y) = 1, the Lissajous figure is most complex, requiring both oscillators to complete a full cycle before the curve closes. |
| **Lissajous figure** | A curve traced by the simultaneous oscillation of X and Y coordinates at independently selectable frequencies and phases, named after Jules-Antoine Lissajous (1857). |
| **Palette** | The 16-entry color lookup table mapping 4-bit framebuffer indices to 10-bit YUV values, based on the Cromemco Dazzler's RGBI color encoding. |
| **Phase accumulator** | A binary counter whose output represents a phase position in a periodic waveform; used here to drive the triangle-wave cursor position on each axis. |
| **RGBI** | Red-Green-Blue-Intensity; the 4-bit color encoding of the Cromemco Dazzler, producing two intensity levels of eight base RGB hues. |
| **Triangle wave** | A periodic waveform that rises linearly from minimum to maximum and then falls linearly back — computationally generated here by folding the MSB of a phase accumulator. |
| **Wipe** | The sequential clearing operation that writes black to framebuffer cells row-by-row, erasing old doodle marks at a rate set by the Wipe Rate parameter. |

For common terms (YUV, FPGA, BRAM, Pipeline, etc.) see the [Common Glossary](../common_reference.md#common-glossary).

---
