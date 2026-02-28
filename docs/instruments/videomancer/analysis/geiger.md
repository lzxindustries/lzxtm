---
draft: true
sidebar_position: 111
slug: /instruments/videomancer/geiger
title: "Geiger"
image: /img/instruments/videomancer/geiger/geiger_hero.png
---

import geiger_hero from '/img/instruments/videomancer/geiger/geiger_hero.png';
import geiger_before_after from '/img/instruments/videomancer/geiger/geiger_before_after.png';
import geiger_control_panel from '/img/instruments/videomancer/geiger/geiger_control_panel.png';
import geiger_exercise1_result from '/img/instruments/videomancer/geiger/geiger_exercise1_result.png';
import geiger_exercise2_result from '/img/instruments/videomancer/geiger/geiger_exercise2_result.png';
import geiger_exercise3_result from '/img/instruments/videomancer/geiger/geiger_exercise3_result.png';

# Geiger

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={geiger_hero} alt="Geiger hero image"/>
*Geiger detecting luminance events across a video signal, scattering stochastic particle flashes over the source with a running activity meter.*
<img src={geiger_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Geiger applied.*

---

## Overview

A Geiger counter measures invisible radiation by converting particle impacts into audible clicks and visual needle deflections. Geiger does the same thing to a video signal. It treats the luminance of every pixel as a form of radiant energy — brighter pixels are more "radioactive" and trigger detection events at a higher rate. When a pixel fires, a brief flash appears at that location, colored according to the Flash Hue control. The result is a stochastic sparkle pattern that maps the brightness structure of the video into a field of glowing particle events.

The detection mechanism uses a 16-bit linear feedback shift register (LFSR) to generate a pseudo-random threshold every pixel clock. If the source luminance (biased by Sensitivity) exceeds the LFSR threshold (scaled by the Threshold control), a detection event fires. A separate spatial gate, also driven by the LFSR, sub-samples the detection field so that Click Rate controls the overall density of events. The result is a natural-looking, spatially irregular pattern of flashes whose density is proportional to image brightness.

The program composites flash events over either the original video (Over Video on) or a black background. An activity meter bar can be overlaid at the bottom of the screen, showing the detection count from the previous frame. All eight pipeline stages fit within purely combinational and register logic — zero BRAM, zero DSP blocks — making Geiger one of the lightest programs in the library despite its visual complexity.

---

## Background

### The Geiger-Müller Counter and Particle Detection

The Geiger-Müller tube is a sealed chamber filled with an inert gas at low pressure. A thin wire running through the center serves as the anode, held at several hundred volts. When an ionizing particle — a gamma ray, a beta particle, an alpha particle — enters the tube and strikes a gas atom, it knocks an electron free. That electron accelerates toward the anode, colliding with other atoms along the way and triggering an avalanche of ionizations. The resulting current pulse produces the characteristic click. The tube cannot distinguish between different types or energies of radiation; it simply counts events. The Geiger program applies the same principle: every pixel is a potential ionization site, and the source luminance determines the probability of a detection event firing.

### Stochastic Event Generation Using LFSR

A linear feedback shift register generates a deterministic but pseudo-random sequence of binary values by feeding a XOR of selected tap positions back into the shift input. The 16-bit LFSR in Geiger produces a new 10-bit pseudo-random number every pixel clock. This value serves as the detection threshold: if the (sensitivity-biased) source luminance exceeds the LFSR output (scaled by the Threshold parameter), the pixel fires. Because the LFSR sequence is deterministic, the detection pattern is reproducible from frame to frame for static input — but visually it appears completely random and spatially uncorrelated, which is exactly the behavior of real particle detection.

### Luminance-Proportional Detection Probability

The detection probability at each pixel is not uniform. Sensitivity scales the source luminance upward before comparison: higher sensitivity means that dimmer pixels can still exceed the threshold. Threshold scales the random value downward: higher threshold makes it harder for any pixel to fire. The interplay between these two controls sets the dynamic range of the detector. At one extreme, only the brightest specular highlights trigger events. At the other, even mid-tones produce a dense sparkle. The product of sensitivity and source luminance forms the "biased luma," which is compared against the product of threshold and the LFSR value. Both multiplications use the top 5 bits of the parameter registers to fit within iCE40 timing constraints.

### Flash Visualization Types

Four flash rendering modes determine how a detection event appears. **Point** draws a single bright pixel at full Brightness — the closest analogy to a scintillation counter dot. **Ring** reduces brightness to 75% and in multi-pixel contexts produces a hollow circle impression through spatial sub-sampling. **Bloom** halves the brightness for a softer, broader glow. **Invert** uses the complement of the source luminance as the flash brightness, producing bright flashes in dark regions and dim flashes in bright regions — a negative-image scintillation effect. All four modes use the same Flash Hue color mapping, so the visual character changes while the color palette remains consistent.

### IIR Decay and Persistence of Vision

Real phosphor screens and scintillation detectors exhibit persistence — a flash does not vanish instantly but fades over several frames. Geiger implements this with a single-pole IIR (infinite impulse response) lowpass on the flash brightness. Each frame, the stored flash value decays by an amount inversely proportional to Flash Dur. A new detection replaces the decayed value only if it is brighter. The result is that flashes build up in areas of sustained detection activity and fade away when the source darkens. At high Flash Dur, flashes linger and overlap, creating a phosphorescent glow. At low Flash Dur, each flash is a brief spark that vanishes within a frame or two.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Input Register + Counters ─────────────────────────
│   │  Latch Y/U/V, generate h_count / v_count
│   │
├── Stage 2: LFSR Compare + Detection ─────────────────────────
│   │  LFSR(15:0) → 10-bit rand threshold
│   │  scaled_thr = rand * threshold(9:5)
│   │  biased_luma = Y_in * sensitivity(9:5)
│   │  detection = (biased_luma > scaled_thr) AND spatial_gate
│   │  spatial_gate = (LFSR(15:6) < click_rate)
│   │
├── Stage 3: Flash Compose + Counter Update ────────────────────
│   │  Flash brightness by type (Point/Ring/Bloom/Invert)
│   │  IIR decay: iir_y = max(flash, iir_y - decay_amount)
│   │  Event counter: count++ per detection, latch on new frame
│   │  Hue mapping: flash_hue → U/V sector color
│   │
├── Stage 4: Composite Output ─────────────────────────────────
│   │  Base = source (Over Video) or black
│   │  Layer flashes over base
│   │  Meter bar in bottom 32 rows (if Display ≠ Clicks)
│   │  Sound vis: scanline brightness pulse
│   │
├── Stage 5–8: Interpolator Wet/Dry Mix (4 clk) ───────────────
│   │  3× interpolator_u (Y, U, V)
│   │  Mix amount from fader
│   │
├── Sync Delay Pipeline ────────────────────────────────────────
│   │  hsync_n, vsync_n, field_n delayed 8 clocks
│   │
└── Bypass Mux ─────────────────────────────────────────────────
    └─ Select processed or delayed original
```

The critical interaction is between the two LFSR-derived gates in Stage 2. The detection comparison tests luminance against a random threshold, producing brightness-proportional event probability. The spatial gate independently sub-samples using a different range of LFSR bits, controlling overall event density without changing the brightness bias. These two gates AND together, so detection requires both conditions to pass. Click Rate thus acts as a global density control that preserves the luminance-proportional character of the detection pattern.

The IIR decay in Stage 3 operates on a single register (`s_iir_y`) rather than a per-pixel frame buffer. This means the decay state is shared across all pixels within a scanline — a deliberate resource trade-off for zero-BRAM operation. In practice, the visual effect is that persistence builds cumulatively across each frame rather than tracking individual flash sites.

---

## Parameter Reference

<img src={geiger_control_panel} alt="Videomancer front panel with Geiger loaded"/>
*Videomancer's front panel with Geiger active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Sensitiv
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the sensitivity of the luminance detector. Higher values bias the source luma upward before comparison with the random threshold, causing dimmer pixels to trigger detection events. At low sensitivity, only specular highlights and peak whites produce flashes. As you increase the knob, mid-tones begin sparkling, and at maximum, even moderately dark areas contribute events. This is the primary control for setting the "activity level" of the Geiger display.

---

#### Knob 2 — Flash Dur
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the flash decay rate — how long each flash persists before fading. The IIR decay subtracts a small amount from the stored flash brightness each frame, with the rate inversely proportional to this control. At 0%, flashes are instantaneous single-frame sparks. At 100%, flashes linger for many frames, building up a phosphorescent glow in regions of sustained detection. Long persistence creates a smoky, trailing luminance that reveals the cumulative detection history.

---

#### Knob 3 — Threshold
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Scales the random threshold from the LFSR before it is compared to the biased luminance. Higher threshold values make detection harder — the random bar is raised, so only very bright pixels exceed it. Lower values lower the bar, increasing the overall detection rate. This interacts with Sensitivity to set the operating point of the detector: Sensitivity controls how much the source luminance matters, while Threshold controls the absolute baseline difficulty of triggering an event.

---

#### Knob 4 — Flash Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Selects the color of detection flashes by mapping the knob position to a sector on the YUV color wheel. The VHDL divides the 0–1023 range into four color sectors: green (0–255), cyan-blue (256–511), red (512–767), and white/neutral (768–1023). All flashes within a given sector share the same hue. Rotating through the range shifts the phosphor glow from green (classic oscilloscope) through blue (Cherenkov radiation) to red (infrared sensor) to white (pure luminance).

---

#### Knob 5 — Click Rate
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the spatial sub-sampling gate that determines which pixels are eligible for detection. A separate set of LFSR bits is compared against this value — higher Click Rate means more pixels pass through the gate, producing denser flash fields. At low values, only a sparse scattering of pixels can fire, regardless of their brightness. At high values, every pixel that passes the luminance threshold comparison will flash. This is a density control independent of the brightness-proportional detection logic.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the peak brightness of detection flashes. In Point mode, this is the literal flash intensity. In Ring mode, the brightness is scaled to 75%. In Bloom mode, it is halved. In Invert mode, this parameter is overridden — flash brightness comes from the inverted source luma instead. Brightness also controls the intensity of the meter bar fill and the scanline glow when Sound Vis is enabled.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Display** | Clicks | Count |
| **8 — Flash Type** | Point | Ring |
| **9 — Sound Vis** | Off | On |
| **10 — Over Video** | Off | On |
| **11 — Bypass** | Off | On |

Toggles 7 and 8 are packed as 2-bit fields in `registers_in(6)`, each selecting from four modes. Toggle 7 controls what overlay information is displayed (flash events, a numeric counter, both, or a graphical meter). Toggle 8 selects the visual rendering style of each flash. Toggles 9–11 are single-bit on/off switches controlling the sound visualization effect, the video background pass-through, and full bypass respectively.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry mix between the processed composite and the delayed original signal via three interpolator instances (Y, U, V). At 0%, the output is the unprocessed source. At 100%, the output is the full Geiger composite. Intermediate values blend the two, allowing detection flashes to appear as a subtle translucent overlay rather than a full replacement of the source.

---

## Guided Exercises

These exercises progress from basic radiation detection to composite visualization techniques. Each explores a different interaction between the stochastic detection engine and the display system.

### Exercise 1: Radiation Mapping

<img src={geiger_exercise1_result} alt="Radiation Mapping result"/>
*Radiation Mapping — simulated result across source images.*
**Source**: A live camera feed with a mix of bright highlights and dark shadows — a window scene, a desk lamp, or high-contrast subject lighting.

**Objective**: Learn how Sensitivity and Threshold interact to control detection density, and observe how brightness drives event probability.

1. **Baseline detection**: Set Sensitivity and Threshold to mid-range (~50%). Watch for flashes appearing primarily in the bright regions of the image.
2. **Increase sensitivity**: Sweep Sensitivity upward. Gradually, mid-tones and eventually shadows begin producing events.
3. **Raise the threshold**: Now increase Threshold while keeping Sensitivity high. The detection rate drops even for bright pixels — the random bar is raised.
4. **Sparse field**: Reduce Click Rate to ~20%. The spatial gate thins out the event field, leaving only scattered flashes even in bright areas.
5. **Dense field**: Push Click Rate to maximum. Every pixel that passes the luminance test now fires, creating dense clusters in highlights.
6. **Persistence**: Increase Flash Dur to ~80%. Flashes begin to accumulate and linger, creating a glowing map of the brightest image regions.

**Key concepts**: Sensitivity biases source luminance upward, Threshold scales the random comparison value, Click Rate sub-samples spatially, Flash Dur controls temporal persistence

---

### Exercise 2: Phosphor Color and Flash Modes

<img src={geiger_exercise2_result} alt="Phosphor Color and Flash Modes result"/>
*Phosphor Color and Flash Modes — simulated result across source images.*
**Source**: Black-and-white or desaturated footage with strong tonal variation — surveillance camera footage, infrared, or a grayscale test pattern.

**Objective**: Explore the four flash types and the hue color wheel to create different detector aesthetics.

1. **Green phosphor**: Set Flash Hue to 0° (green). With Point flash type, the result resembles a classic oscilloscope or radar display.
2. **Blue Cherenkov**: Rotate Flash Hue to ~180° (cyan-blue sector). The flashes take on the blue glow of Cherenkov radiation.
3. **Ring mode**: Switch Flash Type to Ring. Flashes become slightly dimmer and visually suggest hollow circles or rings.
4. **Bloom mode**: Switch to Bloom. The brightness drops to 50%, creating a softer, more diffuse glow — phosphorescent rather than scintillating.
5. **Invert mode**: Switch to Invert. Flash brightness now comes from the complement of the source luma — dark areas flash brightly, bright areas flash dimly.
6. **White flashes**: Rotate Flash Hue past 270° into the white/neutral sector. Flashes become achromatic, emphasizing pure luminance.

**Key concepts**: Hue maps to four YUV color sectors, Flash Type controls brightness scaling and visual character, Invert mode creates a negative-image detector

---

### Exercise 3: Analytical Overlay with Meter

<img src={geiger_exercise3_result} alt="Analytical Overlay with Meter result"/>
*Analytical Overlay with Meter — simulated result across source images.*
**Source**: Moving video with varying brightness — a performer under stage lights, a cityscape with headlights, or fireworks footage.

**Objective**: Use Geiger as an analytical tool to visualize brightness activity in real time, with the meter bar quantifying detection density.

1. **Over video**: Enable Over Video to see flashes composited on the source. Set Display to Meter.
2. **Calibrate**: Adjust Sensitivity and Threshold until the flash density visually tracks the brightest moving elements. The meter bar at the bottom should fluctuate as bright objects enter and leave the frame.
3. **Sound vis**: Enable Sound Vis (Toggle 9). A subtle frame-rate flicker appears, adding a background "hiss" that contrasts with the stochastic flash events.
4. **Mix blend**: Lower the Mix fader to ~60%. The source becomes more visible through the flash overlay, creating a translucent analytical layer.
5. **Both display**: Switch Display to Both. The counter and meter appear simultaneously, providing numeric and graphical readouts.
6. **Observe dynamics**: As bright objects move through the frame, watch the meter bar respond. The flash density follows the motion — Geiger becomes a real-time brightness tracker.

**Key concepts**: Over Video composites flashes on source, Display modes provide different activity readouts, Mix fader controls overlay transparency, Sound Vis adds frame-correlated flicker

---


## Tips

- **Start with Over Video on**: Seeing flashes in context with the source image makes it much easier to calibrate Sensitivity and Threshold. Switch to black background once you have the detection density you want.
- **Use the Meter for calibration**: Set Display to Meter and adjust Sensitivity until the bar responds proportionally to scene brightness changes. This gives you a quantitative readout of detection activity.
- **Green phosphor is classic**: Flash Hue at 0° with Point flash type on a black background perfectly recreates the look of a scintillation counter or classic radar display.
- **Invert mode for X-ray**: Flash Type Invert with Over Video off creates a negative-image particle detector where dark source regions glow brightly — an X-ray or autoradiography aesthetic.
- **Flash Dur for atmosphere**: Long persistence (high Flash Dur) creates a smoky, phosphorescent glow that accumulates in bright areas. Short persistence keeps the display crisp and snappy.
- **Click Rate vs Sensitivity**: Both control density, but differently. Sensitivity changes *which* brightness levels trigger events (brightness-dependent). Click Rate changes *how many* pixels are eligible (brightness-independent spatial sub-sampling).
- **Mix for layered compositions**: At 40–60% Mix with Over Video on, Geiger becomes a translucent analytical overlay — useful for understanding the brightness distribution of the source in real time.
- **Feedback routing**: Sending the Geiger output back to the input creates cascading detection — flashes from the first pass become bright source pixels that trigger more detections, building recursive sparkle structures.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; dedicated memory resources within the FPGA fabric. Geiger uses zero BRAM. |
| **Chroma** | The color information in a video signal, encoded as U and V components in YUV color space. |
| **Flash Type** | One of four rendering modes (Point, Ring, Bloom, Invert) controlling the brightness and character of detection event visualization. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **IIR** | Infinite Impulse Response; a filter topology where the output feeds back into the computation, creating exponential decay or persistence. |
| **LFSR** | Linear Feedback Shift Register; a shift register with XOR taps that generates a pseudo-random binary sequence. Geiger uses a 16-bit LFSR for threshold generation and spatial gating. |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **Meter** | A horizontal brightness bar rendered at the bottom 32 rows of the screen, showing detection count from the previous frame. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Scintillation** | A brief flash of light produced when a particle strikes a phosphor or crystal; the visual metaphor behind Geiger's flash rendering. |
| **Spatial Gate** | A secondary LFSR-based filter that randomly sub-samples which pixels are eligible for detection, controlled by Click Rate. |
| **Stochastic** | Involving randomness; Geiger's detection is stochastic because a pseudo-random threshold is compared against luminance each pixel clock. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
