---
draft: true
sidebar_position: 17
slug: /instruments/videomancer/bezier
title: "Bezier"
image: /img/instruments/videomancer/bezier/bezier_hero.png
---

import bezier_hero from '/img/instruments/videomancer/bezier/bezier_hero.png';
import bezier_animation from '/img/instruments/videomancer/bezier/bezier_animation.gif';
import bezier_control_panel from '/img/instruments/videomancer/bezier/bezier_control_panel.png';
import bezier_exercise1_result from '/img/instruments/videomancer/bezier/bezier_exercise1_result.gif';
import bezier_exercise2_result from '/img/instruments/videomancer/bezier/bezier_exercise2_result.gif';
import bezier_exercise3_result from '/img/instruments/videomancer/bezier/bezier_exercise3_result.gif';

# Bezier

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={bezier_hero} alt="Bezier hero image"/>
*Bezier rendering animated cubic parametric curves with glow and rainbow color cycling over a live video source.*
<img src={bezier_animation} alt="Bezier animated output"/>
*Bezier output evolving over multiple frames â€” synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Most video synthesis programs generate imagery from simple geometric primitives â€” grids, circles, straight lines. Bezier takes a different approach. It draws curved lines defined by cubic BÃ©zier splines, a mathematical tool borrowed from computer-aided design and digital typography. Each curve is defined by four control points: two endpoints and two interior handles that pull the path into smooth arcs. By animating all sixteen control points â€” four per curve â€” the program produces an endlessly evolving tangle of organic, calligraphic strokes.

The curves are evaluated using the De Casteljau algorithm, a recursive sequence of linear interpolations that traces the exact path of a cubic polynomial without ever computing the polynomial itself. The FPGA performs this evaluation during the vertical blanking interval, writing 64 sample points per curve into a block RAM. During active video, each pixel measures its distance to every stored sample and renders a glow or hard-edged stroke based on the closest match. The result is a real-time parametric curve visualizer running entirely in hardware.

At gentle settings, Bezier produces a single softly glowing arc drifting across the screen. At extreme settings, four rainbow-colored curves weave and interlace in complex Lissajous-like patterns, their strokes thickened calligraphically at the endpoints and pulsing with color that cycles independently of animation. The Video Mod toggle allows the curves to interact with a live video input, brightening the source wherever curve energy is present.

---

## Background

### BÃ©zier Curves in History

The cubic BÃ©zier curve was independently developed by Paul de Casteljau at CitroÃ«n (1959) and Pierre BÃ©zier at Renault (1962) for automobile body design. The idea â€” defining a smooth curve by a small number of intuitive control points â€” proved so powerful that it became the foundation of PostScript fonts, vector graphics editors, and motion paths in animation software. A cubic BÃ©zier is defined by four points: P0 (start), P1 (first handle), P2 (second handle), P3 (end). The curve passes through P0 and P3 and is pulled toward P1 and P2 without necessarily touching them. Moving a single handle reshapes the curve smoothly â€” there are no discontinuities or sharp corners unless two control points coincide.

### The De Casteljau Algorithm

To find a point on the curve at parameter t âˆˆ [0, 1], the De Casteljau algorithm performs three levels of linear interpolation. First, it interpolates between each pair of adjacent control points: Q0 = lerp(P0, P1, t), Q1 = lerp(P1, P2, t), Q2 = lerp(P2, P3, t). Then it interpolates between consecutive Q values: R0 = lerp(Q0, Q1, t), R1 = lerp(Q1, Q2, t). Finally, the point on the curve is B(t) = lerp(R0, R1, t). This cascade of six lerps is numerically stable and maps directly to the FPGA's fixed-point multiply-accumulate pipeline. The VHDL implementation uses 10-bit fixed-point lerp: `a + ((b - a) * t) >> 10`, which fits within the iCE40's DSP multiplier resources.

### DDS-Based Control Point Animation

Each of the 16 control points has two independent phase accumulators â€” one for its x coordinate and one for its y coordinate. The phase accumulators increment every vertical blanking interval at rates determined by coprime frequency multipliers: x uses `i*3 + 2` and y uses `i*5 + 3`, where i is the control point index (0â€“15). Because these multipliers are coprime, no two control points ever synchronize â€” the curves continuously evolve without repeating. The accumulated phase is folded through a triangle wave function (quadrant-based folding of the upper bits) to produce a smooth oscillation that maps the phase ramp into a position coordinate via the Amplitude control.

### Calligraphic Stroke Rendering

In hand lettering, the width of a stroke varies with pen pressure. Bezier simulates this with its Calligraphic mode. Near the endpoints of each curve (where t approaches 0 or 63 in the 64-sample table), the effective stroke width is increased. The implementation uses the distance from the nearest endpoint scaled by the stroke width parameter, creating strokes that are thick at the tips and thin in the middle â€” like a broad-nib pen drawn across paper. This subtle effect transforms uniform-width vector curves into organic, hand-drawn marks.

### Glow and Distance Field Rendering

Rather than rendering curves as hard-edged one-pixel lines, Bezier computes a distance field. During active video, each pixel's coordinates are compared against all stored curve samples using Manhattan distance (|Î”x| + |Î”y|), which is cheaper than Euclidean distance but produces a diamond-shaped falloff. The closest distance across all samples determines the pixel brightness. If the distance is below the Stroke Width threshold, the pixel gets full brightness. Beyond that, the Glow control applies a gradual falloff â€” a soft halo that surrounds each curve. The result is that curves appear to emit light, fading smoothly into the background rather than ending at a sharp edge.


---

## Signal Flow

```
VERTICAL BLANKING INTERVAL
â”‚
â”œâ”€â”€ Phase Accumulators (16 CPs Ã— 2 axes)
â”‚   â””â”€â”€ Increment by coprime DDS rates Ã— Anim Spd
â”‚
â”œâ”€â”€ Triangle Wave Folding
â”‚   â””â”€â”€ Phase â†’ position via quadrant fold Ã— Amplitude
â”‚
â”œâ”€â”€ De Casteljau Evaluation (4 curves Ã— 64 t-values)
â”‚   â”œâ”€â”€ Stage 0: lerp(P0,P1), lerp(P1,P2), lerp(P2,P3)
â”‚   â”œâ”€â”€ Stage 1: lerp(Q0,Q1), lerp(Q1,Q2)
â”‚   â””â”€â”€ Stage 2: lerp(R0,R1) â†’ BRAM[curve*64+t]
â”‚
ACTIVE VIDEO (per pixel)
â”‚
â”œâ”€â”€ BRAM Scan (up to 256 entries)
â”‚   â”œâ”€â”€ Manhattan Distance: |px-bx| + |py-by|
â”‚   â”œâ”€â”€ Calligraphic Width (optional endpoint thickening)
â”‚   â””â”€â”€ Track Minimum Distance + associated t, curve_id
â”‚
â”œâ”€â”€ Stroke / Glow Rendering
â”‚   â”œâ”€â”€ dist < stroke_w â†’ full brightness
â”‚   â””â”€â”€ dist â‰¥ stroke_w â†’ brightness Ã— exp(-glow Ã— dist)
â”‚
â”œâ”€â”€ Color Mapping
â”‚   â”œâ”€â”€ Rainbow: t + color_phase â†’ 4-quadrant UV hue
â”‚   â””â”€â”€ Mono: Y-only, neutral UV
â”‚
â”œâ”€â”€ Video Mod (optional)
â”‚   â””â”€â”€ curve_luma + input_Y â†’ output_Y (additive)
â”‚
â”œâ”€â”€ Brightness Scaling
â”‚   â””â”€â”€ output Ã— Bright
â”‚
â”œâ”€â”€ Mix Crossfade
â”‚   â””â”€â”€ lerp(input, processed, Mix)
â”‚
â””â”€â”€ Bypass Mux
    â””â”€â”€ Bypass toggle â†’ pass input unchanged
```

The pipeline is split across two time domains. During vertical blanking, the FPGA runs a 3-stage state machine that evaluates De Casteljau for all four curves, writing 256 sample points into a single 256Ã—20-bit BRAM. During active video, each pixel reads through the entire BRAM to find its closest curve sample â€” a brute-force distance scan that trades memory bandwidth for simplicity. The glow rendering means that even pixels far from any curve still receive some brightness contribution, which creates the characteristic soft-edged luminous appearance. The rainbow color mode derives hue from the t parameter of the closest sample plus a continuously cycling color phase accumulator, so colors shift both along each curve and over time.

---

## Parameter Reference

<img src={bezier_control_panel} alt="Videomancer front panel with Bezier loaded"/>
*Videomancer's front panel with Bezier active. Knobs 1â€“6 (top two rows of left cluster), Toggle switches 7â€“11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1â€“6)

#### Knob 1 â€” Animation Speed
| Property | Value |
|----------|-------|
| Range | 0.0% â€“ 100.0% |
| Default | 25.0% |
| Suffix | % |

Animation speed. Controls the increment rate of all 16 phase accumulators during each vertical blanking interval. At 0%, the curves freeze in place â€” useful for examining a single frame or for static overlays. At 100%, the curves move rapidly, their Lissajous-like paths sweeping across the full screen. Because each control point has coprime frequency multipliers, increasing the speed amplifies all 16 oscillations proportionally while maintaining their relative phase relationships.

---

#### Knob 2 â€” Stroke Width
| Property | Value |
|----------|-------|
| Range | 0.0% â€“ 100.0% |
| Default | 37.5% |
| Suffix | % |

Stroke width. Sets the hard-edge threshold in the distance field. Pixels closer than this distance to a curve sample are rendered at full brightness. At 0%, curves are nearly invisible hairlines â€” only the glow component is visible. At 100%, strokes are wide bands that fill large areas of the screen. In Calligraphic mode, this parameter sets the base width that gets modulated by endpoint proximity.

---

#### Knob 3 â€” Amplitude
| Property | Value |
|----------|-------|
| Range | 0.0% â€“ 100.0% |
| Default | 50.0% |
| Suffix | % |

Amplitude. Controls how far the animated control points spread from the screen center. At 0%, all control points collapse to the center and curves degenerate to a point. At 100%, control points sweep across the full screen dimensions. This parameter scales the output of the triangle wave function applied to each phase accumulator. Moderate values (40â€“60%) produce curves that stay within the visible area; higher values allow control points to move off-screen, creating curves that enter and exit the frame.

---

#### Knob 4 â€” Glow
| Property | Value |
|----------|-------|
| Range | 0.0% â€“ 100.0% |
| Default | 25.0% |
| Suffix | % |

Glow falloff. Controls the rate at which brightness decreases beyond the stroke width threshold. At 0%, there is no glow â€” pixels beyond the stroke edge are black. At 100%, the glow extends far from the curve, creating broad luminous halos. The falloff is applied as a distance-dependent attenuation: larger values produce more gradual falloff, making the curves appear to radiate light over a wider area.

---

#### Knob 5 â€” Color Speed
| Property | Value |
|----------|-------|
| Range | 0.0% â€“ 100.0% |
| Default | 25.0% |
| Suffix | % |

Color cycling speed. Controls the increment rate of the color phase accumulator, which offsets the hue derived from the t parameter. At 0%, colors along each curve are static (though they still vary spatially along the curve length). At 100%, the rainbow pattern shifts rapidly along and between curves. This control is independent of animation speed â€” you can freeze curve positions while cycling colors, or animate positions with static colors.

---

#### Knob 6 â€” Brightness
| Property | Value |
|----------|-------|
| Range | 0.0% â€“ 100.0% |
| Default | 75.1% |
| Suffix | % |

Overall brightness. Scales the final luminance of all rendered curve pixels before the mix stage. At 0%, curves are invisible regardless of glow or stroke settings. At 100%, maximum brightness. This control acts as a master intensity, useful for balancing curve brightness against a video input when using Video Mod.

---

### Toggle Switches (Switches 7â€“11)

| Switch | Off | On |
|--------|-----|-----|
| **7 â€” Curves** | 1 | 2 |
| **8 â€” Color Mode** | Rainbow | Mono |
| **9 â€” Calligraphic** | Off | On |
| **10 â€” Video Mod** | Off | On |
| **11 â€” Bypass** | Off | On |

Switches 7 and 8 configure curve count and color mode as two independent selectors. Switch 9 enables a calligraphic stroke variation. Switch 10 activates video modulation for blending with input. Switch 11 is the standard bypass. Together, 7 and 8 define the visual character of the output (how many curves, what color), while 9 and 10 add optional rendering and compositing refinements.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 â€” Mix
| Property | Value |
|----------|-------|
| Range | 0.0% â€“ 100.0% |
| Default | 100.0% |
| Suffix | % |

Mix crossfade between the unprocessed input video and the rendered curve output. At 0%, only the input is visible. At 100%, only the curve rendering is visible. Intermediate values blend the two proportionally. When Video Mod is active, this fader controls how much of the curve-brightened composite is mixed with the dry input.

---

## Guided Exercises

These exercises progress from a single static curve to a full multi-curve animated composition with video interaction. Each exercise enables more of the parameter space.

### Exercise 1: A Single Glowing Arc

<img src={bezier_exercise1_result} alt="A Single Glowing Arc result"/>
*A Single Glowing Arc â€” simulated result across source images.*
**Objective**: Understand the basic curve rendering: one curve, glow, and brightness controls.

1. **Single curve**: Set Curves to 1 (Switch 7 position 1). One cubic BÃ©zier is drawn on screen.
2. **Freeze animation**: Turn Anim Spd to 0%. The curve holds its current shape.
3. **Stroke width**: Slowly increase Stroke W from 0%. A thin hairline thickens into a visible band.
4. **Glow**: Increase Glow to ~60%. The hard-edged stroke acquires a soft luminous halo.
5. **Brightness**: Sweep Bright from 0% to 100%. The entire curve brightens uniformly.
6. **Animate**: Slowly increase Anim Spd. The curve begins to drift and reshape. Note how the four control points move at different rates â€” the curve never repeats.

**Key concepts**: De Casteljau evaluation produces smooth cubic curves, glow creates distance-field halos, coprime DDS rates ensure non-repeating animation

---

### Exercise 2: Rainbow Weave

<img src={bezier_exercise2_result} alt="Rainbow Weave result"/>
*Rainbow Weave â€” simulated result across source images.*
**Objective**: Explore multi-curve rendering with rainbow color cycling and calligraphic strokes.

1. **Four curves**: Set Curves to 4 (Switch 7 position 4). Four independent BÃ©zier curves interleave on screen.
2. **Rainbow**: Switch Color Mode to Rainbow (Switch 8). Each curve displays a spectrum of colors that varies along its length.
3. **Color cycling**: Increase Color Spd to ~50%. The rainbow shifts along the curves over time.
4. **Calligraphic**: Enable Calligraphic (Switch 9 On). Notice the strokes thicken at their endpoints â€” a subtle pen-pressure effect.
5. **Amplitude**: Sweep Amplitude from 20% to 80%. At low amplitude, curves cluster near center. At high amplitude, they sweep across the full frame.
6. **Speed**: Increase Anim Spd to ~60%. The four curves weave through each other in complex patterns.

**Key concepts**: Coprime frequency multipliers prevent curve synchronization, rainbow hue derives from t parameter plus phase, calligraphic mode thickens endpoints

---

### Exercise 3: Video Overlay Composition

<img src={bezier_exercise3_result} alt="Video Overlay Composition result"/>
*Video Overlay Composition â€” simulated result across source images.*
**Objective**: Use Video Mod to composit animated curves over live video and balance brightness.

1. **Prepare curves**: Set Curves to 3, Anim Spd ~40%, Amplitude ~50%, Stroke W ~20%.
2. **Enable Video Mod**: Turn on Video Mod (Switch 10 On). The curve luminance now adds to the input video â€” bright areas of the video become brighter where curves pass.
3. **Balance brightness**: Reduce Bright to ~40%. Too much curve brightness washes out the video. Find a balance where curves are visible but the source image remains readable.
4. **Mix fader**: Sweep Mix from 0% to 100%. At intermediate values, the curve-on-video composite fades against the dry input â€” useful for subtle overlay effects.
5. **Glow interaction**: Increase Glow to ~70%. The soft halo wraps around video content, creating a luminous veil over the source.
6. **Color over video**: Switch to Rainbow mode and adjust Color Spd. Colored curves overlay the video, adding chromatic energy.

**Key concepts**: Additive blending brightens video at curve locations, brightness control balances curve vs. source, mix fader composites the result against dry input

---


## Tips

- **Freeze and study**: Set Anim Spd to 0% to hold curves in place. This makes it easy to understand how Stroke W, Glow, and Amplitude affect a single configuration before adding motion.
- **Mono for structure, Rainbow for spectacle**: Mono mode reveals the pure geometry of the curves. Switch to Rainbow only after you understand the spatial structure â€” the color can mask the underlying motion patterns.
- **Amplitude vs. Anim Spd**: Amplitude controls *where* the curves go; Anim Spd controls *how fast* they get there. Low amplitude with high speed produces tightly vibrating patterns. High amplitude with low speed produces sweeping arcs.
- **Video Mod balance**: When using Video Mod, reduce Bright to 30â€“40% to prevent the curves from washing out the source. The Mix fader gives an additional intensity control for the composite.
- **Calligraphic subtlety**: The endpoint thickening is most visible with moderate Stroke W (30â€“50%). Too thin and the variation is invisible; too thick and the entire curve appears uniformly wide.
- **Glow as atmosphere**: Even with Stroke W at 0%, the Glow parameter alone can render soft, nebula-like shapes. No hard edges â€” just luminous clouds following the curve paths.
- **Curve count and density**: Start with 1 curve to understand the motion, then increase. At 4 curves with high Amplitude, the overlapping glow fields create complex interference patterns.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; a dedicated memory block within the FPGA used to store the 256 evaluated curve sample points. |
| **Calligraphic stroke** | A rendering style where line width varies along the curve, thickening at endpoints to simulate pressure from a broad-nib pen. |
| **Coprime** | Two integers sharing no common factor greater than 1; used for DDS frequency multipliers to prevent control point synchronization. |
| **DDS** | Direct Digital Synthesis; a technique that generates a waveform by incrementing a phase accumulator at a fixed rate, here driving control point animation. |
| **De Casteljau algorithm** | A recursive sequence of linear interpolations that evaluates a point on a BÃ©zier curve without computing the polynomial directly. |
| **Distance field** | A scalar field where each pixel stores the distance to the nearest curve sample, used to render soft-edged glow and stroke thickness. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline in hardware. |
| **Lerp** | Linear interpolation; computing a weighted blend between two values based on a parameter t in the range [0, 1]. |
| **Lissajous pattern** | A complex curve formed by two perpendicular sinusoidal oscillations at different frequencies, here approximated by the multi-DDS animation system. |
| **Manhattan distance** | The sum of the absolute horizontal and vertical differences between two points (|Î”x| + |Î”y|); cheaper than Euclidean distance to compute in hardware. |
| **Phase accumulator** | A register that increments by a fixed step each cycle, wrapping at overflow to produce a continuous ramp for animation timing. |
| **Triangle wave** | A periodic waveform that ramps linearly up and down, used to fold phase into smooth oscillating position coordinates. |
| **YUV** | A color encoding that separates luminance (Y) from two chrominance components (U and V), used in broadcast video. |


---
