---
draft: true
sidebar_position: 155
slug: /instruments/videomancer/kaleid
title: "Kaleid"
image: /img/instruments/videomancer/kaleid/kaleid_hero.png
description: "In 1992, a shareware program called DAZZLE50 mesmerized DOS users with kaleidoscopic color patterns that required nothing more than a VGA card and a 386."
---

import kaleid_hero from '/img/instruments/videomancer/kaleid/kaleid_hero.png';
import kaleid_animation from '/img/instruments/videomancer/kaleid/kaleid_animation.gif';
import kaleid_control_panel from '/img/instruments/videomancer/kaleid/kaleid_control_panel.png';
import kaleid_exercise1_result from '/img/instruments/videomancer/kaleid/kaleid_exercise1_result.gif';
import kaleid_exercise2_result from '/img/instruments/videomancer/kaleid/kaleid_exercise2_result.gif';
import kaleid_exercise3_result from '/img/instruments/videomancer/kaleid/kaleid_exercise3_result.gif';

# Kaleid

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={kaleid_hero} alt="Kaleid hero image"/>
*Kaleid rendering a folded XOR fractal pattern with rainbow color cycling, evoking the hypnotic geometry of 1990s VGA screensavers.*
<img src={kaleid_animation} alt="Kaleid animated output"/>
*Kaleid output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

In 1992, a shareware program called DAZZLE50 mesmerized DOS users with kaleidoscopic color patterns that required nothing more than a VGA card and a 386. Pixels were plotted one at a time using simple coordinate arithmetic — XOR, absolute sums, max functions — then animated through palette cycling, the act of rotating a 256-color lookup table so that static geometry appeared to flow and shimmer. These programs were not just screensavers; they were an entire generation's introduction to generative art, mathematical beauty rendered in real time on hardware that had no business producing such visual richness.

Kaleid translates this tradition into the Videomancer's FPGA pixel pipeline. Four pattern algorithms — XOR fractal, Diamond (Manhattan distance), Rings (Chebyshev distance), and Moire (XOR-carry interference) — operate on symmetry-folded screen coordinates, producing the same families of geometric figures that captivated VGA-era audiences. A direct digital synthesis (DDS) phase accumulator advances the color palette each frame, and three triangle-wave evaluators spaced 120° apart generate smoothly cycling rainbow bands or monochrome luminance gradients. The result is a standalone video synthesizer that fills the screen with endlessly evolving geometric color, requiring no input signal at all.

The Overlay mode bridges synthesis and processing: rather than replacing the video, Kaleid can modulate the input signal's luminance through its pattern, sculpting incoming footage with kaleidoscopic geometry. Combined with the Invert toggle and wet/dry Mix fader, this creates a versatile visual instrument ranging from pure standalone synthesis to subtle video texturing.

---

## Background

### VGA Palette Cycling and the Illusion of Motion

Early VGA hardware offered 256 simultaneously displayable colors from an 18-bit palette (262,144 possible shades). Programs like DAZZLE50 exploited a crucial feature: the palette itself was writable in real time. By drawing a static image where each pixel's color index depended on its screen position, then rotating the palette entries each frame, the programmer created the illusion of flowing, animated imagery without redrawing a single pixel. This technique — palette cycling — was computationally free on the CPU side, limited only by the DAC update rate during vertical blanking. Kaleid's DDS-driven phase accumulator is the FPGA equivalent: instead of rotating a palette, it adds an ever-increasing offset to the color phase at each vertical sync, producing the same perceptual shift of flowing color across fixed geometry.

### Coordinate-Based Pattern Algorithms

The four algorithms in Kaleid belong to a family of integer functions on screen coordinates that produce complex geometry from trivial arithmetic. XOR (exclusive-or of x and y coordinates) generates Sierpinski-triangle-like fractal tilings at every scale — a consequence of XOR's bitwise carry structure. Manhattan distance (|x| + |y|) produces concentric diamond contours. Chebyshev distance (max(|x|, |y|)) produces concentric square rings. The Moire mode combines addition and XOR, creating interference fringes where the carry pattern of addition conflicts with the carry-free XOR — a visual analog of wave interference. All four operate on folded (absolute-value) coordinates, ensuring bilateral symmetry in both axes.

### Kaleidoscopic Symmetry Folding

A physical kaleidoscope uses angled mirrors to fold an image into rotational symmetry. Kaleid's digital equivalent is coordinate folding: the absolute value of centered coordinates produces 4-fold bilateral symmetry (quad mode), and an additional conditional swap (ensuring x ≤ y) adds 45-degree reflection for 8-fold symmetry (octagonal mode). This folding happens before any pattern computation, so every algorithm automatically inherits the selected symmetry. The octagonal mode is especially effective with the Diamond and Rings patterns, where it transforms concentric contours into star-like figures reminiscent of rose windows.

### Triangle Wave Color Synthesis

Sine waves are the natural basis for smooth color cycling, but hardware sine computation requires lookup tables or CORDIC iterations — both expensive on a resource-constrained iCE40. The triangle wave is a zero-cost alternative: a phase accumulator's top two bits select a quadrant, and a binary fold of the remaining bits produces a piecewise-linear ramp that closely mimics a cosine's zero crossings and extrema. Three such evaluators, spaced at 120° intervals (0, 1365, and 2730 out of 4096), generate the three components of an HSV-like color wheel — one channel per YUV axis. The result is smooth rainbow cycling that requires no BRAM, no multiplier, and no trigonometric function.

### From VGA Screensavers to Video Synthesis

The screensaver genre of the early 1990s occupied a unique cultural moment: personal computers were powerful enough to generate compelling visuals but not yet connected enough to stream them. Programs like After Dark, Electric Sheep, and DAZZLE50 turned idle monitors into ambient art installations. Kaleid inherits this spirit but transforms it from a display curiosity into a compositable video source. Routed through Videomancer's signal chain, a Kaleid pattern can key, modulate, or overlay other programs — functioning as a color-cycling LFO for the entire video synthesis ecosystem.


---

## Signal Flow

```
Video Timing (from data_in sync signals)
│
├── video_timing_generator ──── s_timing (avid, hsync_start, vsync_start, etc.)
│
├── Pixel Counters ──────────── s_h_count (12-bit), s_v_count (12-bit)
│
├── Animation DDS ───────────── s_anim_phase (16-bit accumulator, +speed each vsync)
│
├── Stage 1: Coord Fold + Zoom ─────────────────────────────────
│   ├─ v_sx = h_count − 640 (center X)
│   ├─ v_sy = v_count − 360 (center Y)
│   ├─ v_abs_x, v_abs_y = |v_sx|, |v_sy| (4-fold symmetry)
│   ├─ if fold_mode: swap so abs_x ≤ abs_y (8-fold symmetry)
│   └─ zoom: shift by 0..3 bits based on zoom(9:8)
│       → s_fold_x, s_fold_y (10-bit folded coordinates)
│
├── Stage 2: Pattern + Phase ───────────────────────────────────
│   ├─ Pattern select (4 modes):
│   │   Mode 1: fold_x XOR fold_y         (XOR fractal)
│   │   Mode 2: fold_x + fold_y           (Diamond)
│   │   Mode 3: max(fold_x, fold_y)       (Rings)
│   │   Mode 4: (fold_x+fold_y) XOR (fold_x XOR fold_y)  (Moire)
│   └─ color_phase = pattern + anim_phase(15:4) + hue  (12-bit)
│
├── Stage 3: Triangle Wave Evaluation ──────────────────────────
│   ├─ tri_y = triangle_wave(color_phase)           (Y channel)
│   ├─ tri_u = triangle_wave(color_phase + 1365)    (+120°)
│   └─ tri_v = triangle_wave(color_phase + 2730)    (+240°)
│       → signed 10-bit outputs (−512..+511)
│
├── Stage 4: Scale + Compose ───────────────────────────────────
│   ├─ Y = 512 + (tri_y × brightness) >> 10
│   ├─ if rainbow: U = 512 + (tri_u × saturation) >> 10
│   │              V = 512 + (tri_v × saturation) >> 10
│   │ else mono:   U = 512, V = 512
│   ├─ if invert:  Y = 1023 − Y
│   └─ if overlay: Y = (input_Y × pattern_Y) >> 10
│                  U = input_U, V = input_V
│       → s_comp_y, s_comp_u, s_comp_v (10-bit unsigned)
│
├── Interpolator (4 clocks) ────────────────────────────────────
│   └─ lerp(delayed_input, comp, mix_amount) × 3 channels
│
├── Sync Delay Pipeline (8 stages) ─────────────────────────────
│   └─ hsync_n, vsync_n, field_n, Y, U, V delayed to match
│
└── Output Mux ─────────────────────────────────────────────────
    └─ bypass ? delayed_input : interpolated_output
```

The pipeline's distinctive feature is the triangle-wave color synthesis in Stage 3. By evaluating three phase-shifted triangle waves — spaced at 120° (one-third of the 4096-count cycle) — the engine produces a smooth RGB-like color wheel in YUV space without any color-space conversion hardware. The Y channel receives the base triangle, while U and V receive the +120° and +240° offsets respectively. When Saturation is at maximum and Color is set to Rainbow, this produces vivid cycling bands; in Mono mode, U and V are held at neutral 512, collapsing the output to a grayscale luminance pattern. The DDS phase accumulator advances by the Speed register value at each vertical sync — about 60 Hz for HD — so the color cycling rate scales linearly with the control. At maximum speed (1023), the pattern cycles through approximately 15 full palette rotations per second.

---

## Parameter Reference

<img src={kaleid_control_panel} alt="Videomancer front panel with Kaleid loaded"/>
*Videomancer's front panel with Kaleid active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Pattern
| Property | Value |
|----------|-------|
| Range | 1 – 4 |
| Default | 2 |

Selects one of four coordinate-based pattern algorithms. Each mode applies a different integer function to the folded x and y coordinates, producing a distinct family of geometric figures. Mode 1 (XOR) generates Sierpinski-like fractal tilings with self-similar detail at every zoom level — the signature pattern of the VGA screensaver era. Mode 2 (Diamond) produces concentric diamond contours radiating from the center, reminiscent of Manhattan-distance Voronoi cells. Mode 3 (Rings) creates concentric square rings using the Chebyshev (chessboard) distance metric. Mode 4 (Moire) combines addition and XOR to create interference fringes where the carry propagation of binary addition produces beating patterns against the carry-free XOR — visually complex and mathematically rich. In octagonal fold mode, each algorithm gains additional diagonal symmetry, transforming diamonds into stars and rings into octagons.

---

#### Knob 2 — Zoom
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Controls the spatial scale of the pattern by shifting the folded coordinates before pattern computation. The control provides four discrete zoom levels mapped from the top two bits of the 10-bit register. At minimum (~0–255), coordinates are halved, producing large-scale features that span the full screen. At ~256–511, coordinates pass through at natural scale. At ~512–767, coordinates are doubled, revealing finer detail. At maximum (~768–1023), coordinates are quadrupled, producing dense, thin-band patterns. The zoom affects all four pattern modes equally and interacts strongly with the fold mode: octagonal folding at high zoom can produce intricate rosette patterns with dozens of radial arms.

---

#### Knob 3 — Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 13% |
| Suffix | % |

Controls the rate of color cycling animation. The Speed register value is added to a 16-bit DDS phase accumulator at each vertical sync pulse (approximately 60 Hz for HD video). At zero, the color palette is frozen — the pattern is static. At low values (1–100), colors shift slowly, producing a meditative drift. At mid-range, the palette rotates at a leisurely walking pace, ideal for ambient display. At maximum (1023), the palette cycles rapidly through approximately 15 complete rotations per second, producing a strobing, psychedelic effect. Because the accumulator is 16-bit and only the top 12 bits feed the triangle wave, even small Speed values produce visible motion over time.

---

#### Knob 4 — Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Adds a fixed phase offset to the color cycling, effectively rotating the starting position of the rainbow palette. At 0°, the pattern begins with the default color mapping. Rotating Hue shifts which color appears at which pattern value — a cyan band becomes green, a magenta band becomes red, and so on, uniformly across the entire frame. This control interacts additively with the animation phase: the DDS accumulator provides temporal evolution while Hue provides a static offset, allowing the user to "tune" the color palette to a preferred starting point. In Mono mode, Hue still shifts the luminance pattern's brightness contour.

---

#### Knob 5 — Saturation
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Scales the amplitude of the U and V chrominance channels in Rainbow mode. At maximum (1023), the triangle-wave outputs map to the full ±512 chroma range, producing vivid, saturated rainbow bands. At zero, U and V contributions are zero — the output collapses to monochrome regardless of the Color toggle. At intermediate values, the chroma amplitude is proportionally reduced, producing pastel or muted color cycling. In Mono mode, this control has no visible effect because the U and V channels are already held at neutral 512. Saturation interacts with Brightness to determine the overall visual intensity: high saturation with low brightness produces dark jewel tones, while high saturation with high brightness produces neon-vivid bands.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Scales the amplitude of the Y (luminance) channel after triangle-wave evaluation. The triangle wave output (signed, −512 to +511) is multiplied by the Brightness register, shifted right by 10, and offset to the unsigned midpoint of 512. At maximum brightness, the luminance swings through nearly the full 0–1023 range. At zero, the luminance collapses to a flat mid-gray (512). This control is independent of Saturation — even in Rainbow mode, reducing Brightness dims the pattern without desaturating it. In Overlay mode, Brightness determines how strongly the pattern modulates the input video: low brightness produces a subtle luminance texture, while high brightness produces dramatic video sculpting.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Color** | Mono | Rainbow |
| **8 — Fold** | Quad | Octagonal |
| **9 — Overlay** | Replace | Overlay |
| **10 — Invert** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles configure the pattern engine along orthogonal axes. Color (7) selects between monochrome luminance patterns and full rainbow cycling. Fold (8) chooses 4-fold or 8-fold symmetry. Overlay (9) switches between standalone synthesis and input video modulation. Invert (10) flips the luminance polarity. Bypass (11) is the standard signal bypass. All 32 toggle combinations produce distinct visual results, and the toggles interact meaningfully with each other — for example, Mono + Overlay + Invert produces a negative-image video sculpt where the pattern's dark regions reveal the input.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Wet/dry mix at the end of the processing chain. At maximum (100%), the output is the fully processed Kaleid signal — synthesized pattern at full intensity. At minimum (0%), the output is the unprocessed input passed through the delay pipeline. Intermediate values blend between the two via a 4-clock interpolator operating on all three YUV channels simultaneously. For pure synthesis, leave Mix at maximum. For subtle video texturing in Overlay mode, reduce Mix to 30–50% so the kaleidoscopic pattern appears as a translucent geometric overlay rather than a dominant effect.

---

## Guided Exercises

These exercises explore Kaleid's synthesis and compositing capabilities, progressing from pure pattern generation through animated color cycling to video overlay sculpting. Each exercise highlights a different pattern algorithm and interaction mode.

### Exercise 1: Fractal Kaleidoscope

<img src={kaleid_exercise1_result} alt="Fractal Kaleidoscope result"/>
*Fractal Kaleidoscope — simulated result across source images.*
**Objective**: Generate a static XOR fractal pattern with octagonal symmetry and rainbow color cycling, exploring the Sierpinski-like self-similarity across zoom levels.

1. **Select XOR pattern**: Set Pattern to Mode 1 (fully counter-clockwise). The screen fills with a fractal tiling of nested triangular shapes.
2. **Enable octagonal fold**: Toggle Fold to Octagonal. The fractal gains diagonal symmetry, transforming into an 8-fold mandala.
3. **Set medium zoom**: Zoom at ~40%. The pattern shows moderate detail — both large structural features and fine-grained self-similar detail are visible.
4. **Enable rainbow**: Toggle Color to Rainbow. The triangle-wave color engine paints the fractal in smooth cycling bands.
5. **Start animation**: Set Speed to ~30%. The rainbow palette rotates slowly across the fractal, revealing how different color bands highlight different structural levels of the self-similar tiling.
6. **Sweep zoom**: Slowly increase Zoom from minimum to maximum. Watch the fractal structure repeat at finer and finer scales — new copies of the pattern emerge within each band as the coordinate space expands.

**Key concepts**: XOR produces fractal self-similarity, octagonal fold creates mandala geometry, zoom reveals scale-invariant detail, color cycling highlights structural layers

---

### Exercise 2: Diamond Pulse

<img src={kaleid_exercise2_result} alt="Diamond Pulse result"/>
*Diamond Pulse — simulated result across source images.*
**Objective**: Create concentric diamond patterns with rapid color cycling, then explore how Invert and Mono mode alter the visual character.

1. **Select Diamond pattern**: Set Pattern to Mode 2. Concentric diamond-shaped contours radiate from the center.
2. **Set quad fold**: Toggle Fold to Quad for clean bilateral symmetry.
3. **High zoom**: Set Zoom to ~70%. Many thin diamond rings fill the screen.
4. **Fast animation**: Set Speed to ~60%. The color palette cycles quickly, creating a pulsing, breathing effect as bands sweep inward (or outward, depending on perspective).
5. **Engage Invert**: Toggle Invert On. The bright/dark relationship reverses — what were luminous bands become dark channels and vice versa. With rainbow color, this produces a complementary-color version of the same pattern.
6. **Switch to Mono**: Toggle Color to Mono. The pattern collapses to high-contrast black-and-white concentric diamonds — a stark, graphic visualization of the Manhattan distance function.
7. **Adjust Brightness**: Sweep Brightness from low to high. In Mono mode, this controls the contrast ratio between the bright and dark bands. Very low brightness produces a subtle, dark pattern. Very high brightness produces hard black-and-white stripes.

**Key concepts**: Diamond pattern is Manhattan distance, fast cycling creates pulsing motion, Invert produces complementary colors, Mono reveals pure geometry

---

### Exercise 3: Moire Video Sculpt

<img src={kaleid_exercise3_result} alt="Moire Video Sculpt result"/>
*Moire Video Sculpt — simulated result across source images.*
**Objective**: Use the Moire pattern in Overlay mode to sculpt incoming video, creating an interference texture that modulates the source signal's luminance.

1. **Connect video source**: Feed any recognizable video — portraits, landscapes, or abstract footage all work well.
2. **Select Moire pattern**: Set Pattern to Mode 4. Interference fringes appear based on the XOR-carry interaction.
3. **Enable Overlay**: Toggle Overlay to Overlay. The pattern now modulates the input video's luminance rather than replacing it.
4. **Set medium zoom**: Zoom at ~50%. The interference bands are moderately spaced.
5. **Slow animation**: Set Speed to ~15%. The moire pattern drifts slowly across the video, creating an evolving texture.
6. **Adjust Brightness**: This controls the modulation depth. High brightness (~80%) produces dramatic sculpting where dark pattern regions nearly black out the video. Low brightness (~30%) produces a subtle luminance texture.
7. **Reduce Mix**: Pull Mix to ~60% for a blended effect where the moire texture overlays the full-strength video.
8. **Try octagonal fold**: Toggle Fold to Octagonal. The interference pattern gains diagonal symmetry, creating a more complex web-like modulation grid.

**Key concepts**: Overlay mode modulates input luminance, Moire creates interference textures, Brightness controls modulation depth, Mix blends sculpted and original

---


## Tips

- **XOR is the classic screensaver pattern**: Mode 1 produces the signature Sierpinski-like fractal tiling that defined an entire genre of VGA-era generative art. Combine with octagonal fold for mandala geometry.
- **Zoom is stepwise, not continuous**: The four zoom levels double the coordinate scale each step. For fine spatial frequency tuning, combine Zoom with different pattern modes — Diamond at ×1 has similar density to Rings at ×2.
- **Rainbow spacing creates color complements**: Because the three triangle waves are spaced at 120° (one-third of a cycle), adjacent color bands are approximate complements. This naturally produces high color contrast across the pattern.
- **Overlay mode turns Kaleid into a video texture**: Switch from Replace to Overlay and feed any video source. The kaleidoscopic pattern modulates the input luminance, creating a geometric texture that follows the source brightness. Reduce Mix for subtlety.
- **Hue is your palette tuner**: The animation phase sets color position over time, but Hue lets you choose the starting palette. Sweep Hue slowly to find the most pleasing color alignment for a given pattern.
- **Mono + high brightness for graphic masks**: In Mono mode with Brightness near maximum, Kaleid produces stark black-and-white geometric patterns ideal for downstream keying, masking, or compositing with other Videomancer programs.
- **Low speed for ambient installation**: Set Speed to 5–10% for glacial color evolution. The pattern changes slowly enough that viewers notice the shift only over minutes — ideal for projection and gallery display.
- **Feedback amplifies complexity**: Route Kaleid's output back to its input via an external feedback loop. Each pass through the Overlay mode compounds the geometric modulation, rapidly generating fractal-like complexity.

---

## Glossary

| Term | Definition |
|------|------------|
| **Chebyshev distance** | A distance metric defined as max(|Δx|, |Δy|), which produces square-shaped iso-distance contours; used by the Rings pattern mode. |
| **Color cycling** | An animation technique from VGA-era graphics where rotating a color palette's index-to-color mapping creates the illusion of motion in a static image. |
| **DDS** | Direct Digital Synthesis; a technique for generating periodic waveforms using a phase accumulator incremented at a fixed rate. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that implements the video processing pipeline in hardware. |
| **Manhattan distance** | A distance metric defined as |Δx| + |Δy|, which produces diamond-shaped iso-distance contours; used by the Diamond pattern mode. |
| **Moire** | An interference pattern produced when two regular structures with similar spatial frequencies overlap, producing beating patterns at their difference frequency. |
| **Palette rotation** | See *color cycling*; specifically the act of cyclically shifting all color entries in a lookup table. |
| **Sierpinski triangle** | A fractal figure produced by recursively subdividing a triangle, related to the XOR function's binary carry structure. |
| **Symmetry folding** | A coordinate transform that maps multiple screen regions to a single canonical region, creating mirror symmetry; absolute value produces bilateral symmetry, conditional swap adds diagonal symmetry. |
| **Triangle wave** | A periodic piecewise-linear waveform that rises and falls at constant slope, used as a hardware-efficient approximation to a cosine function. |
| **VGA** | Video Graphics Array; the IBM display standard introduced in 1987, featuring 256-color indexed mode at 320×200 resolution, widely used by screensaver and demo programs. |
| **XOR** | Exclusive OR; a bitwise logical operation that outputs 1 when its inputs differ, producing fractal-like patterns when applied to screen coordinates. |
| **YUV** | A color space separating luminance (Y) from chrominance (U, V), used as the native pixel format in the Videomancer processing pipeline. |

---
