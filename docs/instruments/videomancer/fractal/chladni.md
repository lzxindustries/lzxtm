---
draft: true
sidebar_position: 45
slug: /instruments/videomancer/chladni
title: "Chladni"
image: /img/instruments/videomancer/chladni/chladni_hero.png
---

import chladni_hero from '/img/instruments/videomancer/chladni/chladni_hero.png';
import chladni_animation from '/img/instruments/videomancer/chladni/chladni_animation.gif';
import chladni_control_panel from '/img/instruments/videomancer/chladni/chladni_control_panel.png';
import chladni_exercise1_result from '/img/instruments/videomancer/chladni/chladni_exercise1_result.gif';
import chladni_exercise2_result from '/img/instruments/videomancer/chladni/chladni_exercise2_result.gif';
import chladni_exercise3_result from '/img/instruments/videomancer/chladni/chladni_exercise3_result.gif';

# Chladni

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={chladni_hero} alt="Chladni hero image"/>
*Chladni projecting standing-wave nodal patterns onto a cathedral interior, revealing the hidden resonant geometry of the architecture.*
<img src={chladni_animation} alt="Chladni animated output"/>
*Chladni output evolving over multiple frames â€” synthesis programs generate imagery without requiring a video input source.*

---

## Overview

In 1787, the German physicist Ernst Chladni drew a violin bow across the edge of a metal plate dusted with fine sand. The sand migrated away from the vibrating regions and collected along the still lines â€” the *nodes* â€” where the plate's standing waves cancelled to zero. The patterns that emerged were intricate, symmetrical, and eerily beautiful: geometric lattices that depended only on the plate's shape and the frequency of excitation. For the first time, the invisible architecture of sound was made visible.

Chladni recreates this phenomenon in the pixel domain. Two triangle-wave oscillators â€” one horizontal, one vertical â€” sweep across the frame at independently controllable frequencies. Their absolute values are summed to produce a two-dimensional standing-wave field. Where the combined amplitude falls below a threshold, the program draws a nodal line; where it exceeds the threshold, the field is open. The result is a lattice of curves that tile the screen in patterns ranging from simple grids to complex interlocking diamonds, depending on the frequency ratio between the two axes. These patterns can overlay the input video as a white-on-black mask (Draw mode) or sculpt it by multiplying the video signal against the standing-wave field, selectively suppressing pixels that fall on the antinodes.

The frequency controls are continuous â€” not quantized to integer multiples â€” so the patterns evolve smoothly as you turn the knobs, passing through rational ratios (where the lattice locks into perfect periodicity) and irrational ratios (where the lattice drifts without repeating). Phase rotation and animation add temporal dimension, making the nodal lines sweep and breathe like the sand on Chladni's vibrating plate.

---

## Background

### Ernst Chladni and the Vibrating Plate

Ernst Florens Friedrich Chladni (1756â€“1827) is sometimes called the father of experimental acoustics. His plate experiments were a sensation across Europe â€” Napoleon himself attended a demonstration in 1809 and offered a prize for a mathematical explanation of the patterns. The key insight was that a vibrating surface does not move uniformly: it divides into regions of maximum displacement (antinodes) and regions of zero displacement (nodes), separated by curves whose geometry is determined by the boundary conditions and the excitation frequency. Higher frequencies produce more nodal lines and more complex patterns. Chladni catalogued hundreds of these figures, each a fingerprint of a specific vibrational mode.

### Standing Waves and Nodal Patterns

A standing wave arises when two waves of equal frequency and amplitude travel in opposite directions through the same medium. Their superposition creates a pattern that appears stationary â€” fixed positions of constructive interference (antinodes, where the amplitude is maximum) and destructive interference (nodes, where the amplitude is always zero). On a two-dimensional plate, the nodal lines form curves that divide the surface into vibrating cells. The mathematical description involves solutions to the wave equation on a bounded domain â€” Bessel functions for circular plates, products of trigonometric functions for rectangular ones. Chladni's video implementation uses the rectangular case: independent oscillators along X and Y, whose combined absolute values define the nodal field.

### Triangle Wave Approximation

A pure sine wave is the natural basis function for standing-wave analysis, but sine computation is expensive in digital hardware. The triangle wave is a first-order approximation: it shares the periodicity and symmetry of a sine wave, rising linearly to a peak, then falling linearly to a trough. Its absolute value produces a V-shaped waveform that closely resembles |sin(x)| in its zero crossings and general shape, while requiring only a binary fold of an accumulator's most significant bits â€” no lookup table, no multiplier, no BRAM. The Chladni program exploits this by running a frequency accumulator per axis and folding the top bits into a triangle function, yielding a computationally cheap approximation to the sinusoidal standing-wave field at the cost of slightly sharper nodal line profiles.

### Digital Frequency Synthesis (DDS)

Direct Digital Synthesis is the standard technique for generating periodic waveforms in digital hardware. A phase accumulator increments by a fixed frequency word on each clock cycle. The accumulator's most significant bits represent the instantaneous phase angle, which can be mapped to any desired waveform shape. In Chladni, two accumulators run per pixel â€” one accumulating phase proportional to the horizontal pixel position times the Freq X parameter, the other accumulating proportional to the vertical position times Freq Y. The phase offset knob adds a constant to the Y accumulator, rotating the entire pattern. When the Animate toggle is on, a separate frame-rate DDS advances the phase offset automatically, causing the nodal lines to drift across the screen.

### Video Sculpting with Amplitude Masks

The Chladni mask â€” a binary or graded field of nodal lines â€” can be applied to the input video in two ways. In Draw mode, the mask replaces the video entirely, rendering the standing-wave pattern as white lines on a black background â€” a pure visualization of the mathematical field. With Draw off, the mask *multiplies* the video signal: pixels on the nodal lines pass through at full brightness, while pixels on the antinodes are attenuated or suppressed. This sculpting technique is analogous to amplitude modulation in audio â€” the carrier (input video) is modulated by the envelope (Chladni field), producing spatial patterns that follow the video content's brightness structure while being shaped by the standing-wave geometry.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
â”‚
â”œâ”€â”€ Clock 0: Register Decode â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
â”‚   â”œâ”€ freq_x = registers_in(0)
â”‚   â”œâ”€ freq_y = registers_in(1)  [or freq_x if XY Link on]
â”‚   â”œâ”€ phase = registers_in(2)
â”‚   â”œâ”€ width = registers_in(3)
â”‚   â”œâ”€ contrast = registers_in(4)
â”‚   â”œâ”€ y_bright = registers_in(5)
â”‚   â””â”€ toggles: draw, invert, xy_link, animate, bypass
â”‚
â”œâ”€â”€ Clock 1: Frequency Accumulators â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
â”‚   â”œâ”€ acc_x = pixel_x Ã— freq_x  (20-bit horizontal accumulator)
â”‚   â”œâ”€ acc_y = pixel_y Ã— freq_y  (20-bit vertical accumulator)
â”‚   â””â”€ acc_y += phase + frame_phase  (phase offset + animation)
â”‚
â”œâ”€â”€ Clock 2: Triangle Wave Fold â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
â”‚   â”œâ”€ tri_x = fold(acc_x MSBs)  â†’ |triangle| value
â”‚   â””â”€ tri_y = fold(acc_y MSBs)  â†’ |triangle| value
â”‚
â”œâ”€â”€ Clock 3: Standing Wave Sum + Threshold â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
â”‚   â”œâ”€ wave = |tri_x| + |tri_y|
â”‚   â”œâ”€ mask = (wave < width) ? 1 : 0  (nodal line threshold)
â”‚   â””â”€ mask ^= invert  (optional polarity flip)
â”‚
â”œâ”€â”€ Clock 4: Draw / Sculpt Mux â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
â”‚   â”œâ”€ Draw On:  Y = mask Ã— 1023, U = 512, V = 512
â”‚   â””â”€ Draw Off: Y = Y_in Ã— mask, U = U_in, V = V_in
â”‚
â”œâ”€â”€ Clock 5: Contrast (proc_amp) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
â”‚   â””â”€ Y = (Y âˆ’ 512) Ã— contrast / 512 + 512
â”‚
â”œâ”€â”€ Clock 6: Brightness â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
â”‚   â””â”€ Y = Y + (y_bright âˆ’ 512)
â”‚
â”œâ”€â”€ Clock 7: Clamp + Output â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
â”‚   â””â”€ Clamp Y, U, V to [0, 1023]
â”‚
â”œâ”€â”€ Clocks 4â€“7: Interpolator (wet/dry Mix) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
â”‚   â””â”€ lerp(dry, wet, Mix)  Ã—3 channels  (4 clocks)
â”‚
â”œâ”€â”€ Sync Signals â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
â”‚   â””â”€ 8-stage delay pipeline (hsync, vsync, field)
â”‚
â””â”€â”€ Bypass â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    â””â”€ Select original or processed signal
```

The heart of the algorithm is the pair of frequency accumulators in Clock 1 and their triangle-wave fold in Clock 2. Because multiplication by position is linear, the accumulated phase increases steadily across the screen â€” producing evenly spaced oscillation cycles whose spatial frequency is directly proportional to the Freq X and Freq Y register values. The standing-wave sum in Clock 3 adds the two triangle magnitudes, creating a 2D field whose zero crossings trace the characteristic Chladni figures. The Width parameter determines how much of the field near these crossings is classified as a nodal line â€” low Width yields hair-thin lines, high Width yields broad bands. The entire pipeline uses zero BRAMs and roughly 800 logic cells, making it one of the more resource-efficient programs despite its visually complex output.

---

## Parameter Reference

<img src={chladni_control_panel} alt="Videomancer front panel with Chladni loaded"/>
*Videomancer's front panel with Chladni active. Knobs 1â€“6 (top two rows of left cluster), Toggle switches 7â€“11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1â€“6)

#### Knob 1 â€” Mode M
| Property | Value |
|----------|-------|
| Range | 1 â€“ 8 |
| Default | 3 |

Controls the horizontal spatial frequency of the standing-wave pattern. At zero the horizontal oscillator is frozen â€” no variation across the X axis, producing only horizontal bands driven by the Y oscillator. As Freq X increases, vertical nodal lines appear, spaced more closely together at higher values. The interaction with Freq Y determines the overall pattern geometry: equal frequencies produce diamond lattices, integer ratios produce regular tilings, and irrational ratios produce quasi-periodic patterns that never exactly repeat. Sweeping this knob slowly reveals the pattern locking and unlocking as it passes through harmonic ratios â€” a visual analog of musical intervals.

---

#### Knob 2 â€” Mode N
| Property | Value |
|----------|-------|
| Range | 1 â€“ 8 |
| Default | 4 |

Controls the vertical spatial frequency. Behaves identically to Freq X but along the Y axis. At zero, only vertical bands from the X oscillator are visible. Increasing Freq Y introduces horizontal nodal lines. The most visually rich patterns occur when both frequencies are moderate and slightly detuned from each other â€” the near-rational ratio produces a slowly evolving moirÃ© of interlocking curves. When XY Link is engaged, this control is overridden by Freq X, forcing both axes to the same frequency and producing strictly diagonal nodal patterns.

---

#### Knob 3 â€” Superpose
| Property | Value |
|----------|-------|
| Range | 0.0% â€“ 100.0% |
| Default | 50.0% |
| Suffix | % |

Adds a constant phase offset to the vertical accumulator. At 0Â°, the pattern is symmetric about the frame origin. Rotating the phase shifts the entire nodal lattice vertically â€” the lines slide up or down the screen as if the virtual plate were being tilted. At 180Â°, the pattern inverts its vertical alignment relative to 0Â°. This parameter interacts strongly with the Animate toggle: when Animate is off, Phase provides manual positional control; when Animate is on, Phase sets the starting offset for the automatic sweep.

---

#### Knob 4 â€” Threshold
| Property | Value |
|----------|-------|
| Range | 0.0% â€“ 100.0% |
| Default | 25.0% |
| Suffix | % |

Threshold width for nodal line detection. The standing-wave field value (|tri_x| + |tri_y|) is compared against this threshold to determine which pixels lie on a nodal line. At 0%, only the mathematical zero crossings are captured â€” infinitely thin lines that may flicker or alias. At 50%, a substantial band around each zero crossing is included, producing thick, painterly strokes. At 100%, nearly the entire field qualifies as a nodal line, collapsing the pattern into a nearly uniform mask. The Width control is the primary tool for adjusting the visual weight and graphic density of the Chladni pattern.

---

#### Knob 5 â€” Speed
| Property | Value |
|----------|-------|
| Range | 0.0% â€“ 100.0% |
| Default | 25.0% |
| Suffix | % |

Scales the luminance channel using proc_amp-style multiplication centered on mid-gray. At 50% (default), contrast is unity â€” the sculpted or drawn pattern retains its native brightness range. Below 50%, contrast compresses toward mid-gray, softening the edges of the nodal lines and reducing the visual punch of the pattern. Above 50%, contrast expands, pushing the pattern toward stark black-and-white with harder transitions. In Draw mode, this control adjusts the brightness of the white lines and the depth of the black background. In sculpt mode, it adjusts how aggressively the mask modulates the video signal's luminance.

---

#### Knob 6 â€” Brightness
| Property | Value |
|----------|-------|
| Range | 0.0% â€“ 100.0% |
| Default | 75.1% |
| Suffix | % |

Adds a DC brightness offset to the luminance channel after contrast scaling. At 50% (default), no offset is applied. Below 50%, the entire image darkens â€” useful for sinking the black regions of the mask to true black when contrast has lifted them. Above 50%, the image brightens â€” useful for revealing shadow detail in the sculpted regions or creating a luminous glow effect in Draw mode where the nodal lines appear as bright outlines on a gray background rather than stark white on black.

---

### Toggle Switches (Switches 7â€“11)

| Switch | Off | On |
|--------|-----|-----|
| **7 â€” Shape** | Square | Cross |
| **8 â€” Animate** | Static | Morph |
| **9 â€” Render** | Overlay | Replace |
| **10 â€” Invert** | Off | On |
| **11 â€” Bypass** | Off | On |

Switches 7â€“10 configure four orthogonal aspects of the Chladni engine. Draw (7) selects between mask overlay and video sculpting. Invert (8) flips the mask polarity. XY Link (9) locks both frequency axes together for diagonal patterns. Animate (10) enables continuous phase rotation. These toggles are independent â€” each controls a single binary decision in the pipeline â€” and all sixteen combinations produce distinct visual results. Switch 11 is the standard bypass.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 â€” Mix
| Property | Value |
|----------|-------|
| Range | 0.0% â€“ 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry mix at the end of the processing chain. At 100%, the output is fully processed â€” the Chladni pattern is at maximum strength. At 0%, the output is the unprocessed input. Intermediate values blend between the two via a 4-clock interpolator operating on all three channels simultaneously, producing a smooth crossfade with no color artifacts. This control is essential for dialing in subtle sculpting effects where the standing-wave pattern should texture the video without dominating it.

---

## Guided Exercises

These exercises progress from pure mathematical visualization through subtle video sculpting to dynamic animated resonance. Each reveals a different facet of the standing-wave geometry and its interaction with the input signal.

### Exercise 1: Static Chladni Plate

<img src={chladni_exercise1_result} alt="Static Chladni Plate result"/>
*Static Chladni Plate â€” simulated result across source images.*
**Objective**: Visualize the Chladni figure as a white-on-black pattern, exploring how frequency ratios and phase determine the geometry of nodal lines.

1. **Enable Draw mode**: Toggle Draw On. The input video disappears, replaced by the standing-wave pattern rendered as white curves on black.
2. **Set baseline frequencies**: Set Freq X and Freq Y to ~50%. A diamond-grid lattice should appear.
3. **Explore frequency ratios**: Slowly detune Freq Y while leaving Freq X fixed. Watch the pattern shift from regular diamonds through elongated rectangles to complex, non-repeating moirÃ©s.
4. **Adjust Width**: Increase Width from 0% to see the nodal lines thicken from hairlines to broad bands.
5. **Rotate Phase**: Sweep Phase from 0Â° to 360Â° and observe the entire pattern sliding vertically.
6. **Try XY Link**: Toggle XY Link On. Both axes lock to Freq X, producing perfect diagonal symmetry regardless of Freq Y.

**Key concepts**: Frequency ratio determines pattern geometry, Width thresholds the standing wave into visible lines, Phase shifts the pattern position, XY Link forces diagonal symmetry

---

### Exercise 2: Video Sculpting with Nodal Lines

<img src={chladni_exercise2_result} alt="Video Sculpting with Nodal Lines result"/>
*Video Sculpting with Nodal Lines â€” simulated result across source images.*
**Objective**: Use the Chladni mask to sculpt the input video, allowing it to pass only through the nodal lines â€” creating a lattice window into the source material.

1. **Disable Draw mode**: Toggle Draw Off. The Chladni mask now multiplies the input video â€” the image is visible only where the standing wave has a node.
2. **Set a medium pattern**: Freq X ~40%, Freq Y ~60% for a slightly asymmetric lattice. Width ~35% for moderate line thickness.
3. **Observe sculpting**: The source video appears segmented into curved strips following the nodal geometry. Dark areas of the video vanish where they coincide with antinodes; bright areas survive on the nodal lines.
4. **Adjust Contrast**: Push Contrast above 50% to sharpen the sculpted edges, or below 50% to soften them into a gentle lattice overlay.
5. **Try Invert**: Toggle Invert On. The previously dark antinode regions now pass the video, and the nodal lines suppress it â€” the positive/negative of the sculpted image.
6. **Blend with Mix**: Pull the Mix fader to ~60% for a subtle lattice texture overlaid on the full video.

**Key concepts**: Sculpt mode multiplies video by the standing-wave mask, Invert swaps figure and ground, Mix blends sculpted and original for subtlety

---

### Exercise 3: Animated Resonance

<img src={chladni_exercise3_result} alt="Animated Resonance result"/>
*Animated Resonance â€” simulated result across source images.*
**Objective**: Activate phase animation and explore how the Chladni pattern behaves as a living resonance field sweeping across the video.

1. **Start from Exercise 2 settings**: Sculpt mode, moderate frequencies, Width ~35%.
2. **Enable Animate**: Toggle Animate On. The nodal lines begin drifting steadily across the frame, as if the virtual plate were being continuously excited at a changing frequency.
3. **Adjust Phase as starting point**: The Phase knob now sets the initial phase offset for the animation. Sweep it to choose where the continuous motion begins.
4. **Increase Width for flow**: Set Width to ~55%. The thicker lines produce a flowing, liquid quality as they sweep and reform.
5. **Combine with Draw**: Toggle Draw On. The animated pattern renders as a pure white-on-black visualization â€” mesmerizing geometric choreography suitable for projection or overlay compositing.
6. **Push frequencies**: Set both Freq X and Freq Y to high values (~80%) for a dense, rapidly cycling pattern, then drop them to low values (~15%) for slow, monumental wave sweeps.

**Key concepts**: Animate drives continuous phase evolution via DDS, Phase sets animation start offset, high Width creates fluid motion quality, Draw mode isolates the mathematical field for visual analysis

---


## Tips

- **Rational frequency ratios are musical**: When Freq X and Freq Y are in simple integer ratios (1:1, 1:2, 2:3), the Chladni pattern locks into a perfectly repeating lattice. Irrational ratios produce quasi-periodic patterns that drift without repeating â€” visually richer but less stable.
- **Width is your graphic weight control**: Thin Width values produce delicate filigree; thick values produce bold, graphic masks. In sculpt mode, Width determines how much of the source video survives through each nodal window.
- **Draw mode is a pattern generator**: With Draw On, Chladni becomes a standalone synthesis program producing geometric overlays. Route its output into another Videomancer module for compositing, keying, or modulation.
- **XY Link for simplicity**: When you want clean, symmetric patterns without fussing over two frequency knobs, engage XY Link. The resulting diagonal lattices are the simplest Chladni figures â€” good starting points for sculpting.
- **Phase + Animate for choreography**: Set Animate On for continuous motion, then adjust Phase to choose the starting position. For rhythmic effects, momentarily toggle Animate On and Off to advance the pattern in controlled bursts.
- **Contrast and Brightness are post-mask**: These controls operate after the Chladni sculpting stage. Use Contrast to sharpen or soften the sculpted edges. Use Y Bright to lift the dark regions of the mask for a more translucent overlay effect.
- **Mix at 30â€“50% for texture**: Full-strength sculpting can obliterate the source image. For subtle integration, pull the Mix fader to 30â€“50% â€” the Chladni lattice becomes a translucent geometric texture overlaid on the full video.
- **Feedback creates fractal resonance**: Route Chladni's output back to its input. Each pass through the mask compounds the lattice geometry, producing dense, self-similar patterns reminiscent of cymbal plate vibration modes.

---

## Glossary

| Term | Definition |
|------|------------|
| **Amplitude modulation** | A technique where one signal (the carrier) is multiplied by another (the modulator), used in Sculpt mode to shape video brightness with the standing-wave field. |
| **Antinode** | A point on a standing wave where the oscillation amplitude is at its maximum, the complement of a node. |
| **Bessel function** | A family of mathematical functions that describe standing-wave patterns on circular plates; rectangular plates use trigonometric products instead. |
| **BRAM** | Block RAM; dedicated memory blocks within an FPGA used for look-up tables, line buffers, and data storage. |
| **DDS** | Direct Digital Synthesis; a technique for generating periodic waveforms using a phase accumulator, used here to animate the Chladni pattern over time. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that implements the video processing pipeline in hardware. |
| **MoirÃ©** | An interference pattern produced when two periodic structures overlap at slightly different frequencies or angles. |
| **Node** | A point on a standing wave where the oscillation amplitude is always zero; nodal lines on a Chladni plate are where sand collects. |
| **Proc amp** | Processing amplifier; a standard video circuit that adjusts contrast and brightness by scaling and offsetting the luminance signal. |
| **Standing wave** | A wave pattern formed by the superposition of two waves traveling in opposite directions, producing fixed nodes and antinodes. |
| **Triangle wave** | A periodic waveform that rises and falls linearly, used as a computationally cheap approximation to a sine wave in hardware. |
| **YUV** | A color space that separates luminance (Y) from chrominance (U, V), used as the native pixel format in the Videomancer processing pipeline. |

---
