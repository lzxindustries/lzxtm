---
draft: true
sidebar_position: 97
slug: /instruments/videomancer/elastica
title: "Elastica"
image: /img/instruments/videomancer/elastica/elastica_hero_s1.png
description: "In the 1970s, a single machine dominated the world of broadcast motion graphics."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import elastica_control_panel from '/img/instruments/videomancer/elastica/elastica_control_panel.png';
import elastica_source1_house from '/img/instruments/videomancer/elastica/elastica_source1_house.png';
import elastica_source2_boat from '/img/instruments/videomancer/elastica/elastica_source2_boat.png';
import elastica_source3_collage from '/img/instruments/videomancer/elastica/elastica_source3_collage.png';
import elastica_source4_pattern from '/img/instruments/videomancer/elastica/elastica_source4_pattern.png';
import elastica_source5_woman from '/img/instruments/videomancer/elastica/elastica_source5_woman.png';
import elastica_source6_wood from '/img/instruments/videomancer/elastica/elastica_source6_wood.png';
import elastica_hero_s1 from '/img/instruments/videomancer/elastica/elastica_hero_s1.png';
import elastica_hero_s2 from '/img/instruments/videomancer/elastica/elastica_hero_s2.png';
import elastica_hero_s3 from '/img/instruments/videomancer/elastica/elastica_hero_s3.png';
import elastica_hero_s4 from '/img/instruments/videomancer/elastica/elastica_hero_s4.png';
import elastica_hero_s5 from '/img/instruments/videomancer/elastica/elastica_hero_s5.png';
import elastica_hero_s6 from '/img/instruments/videomancer/elastica/elastica_hero_s6.png';
import elastica_ex1_s1 from '/img/instruments/videomancer/elastica/elastica_ex1_s1.png';
import elastica_ex1_s2 from '/img/instruments/videomancer/elastica/elastica_ex1_s2.png';
import elastica_ex1_s3 from '/img/instruments/videomancer/elastica/elastica_ex1_s3.png';
import elastica_ex1_s4 from '/img/instruments/videomancer/elastica/elastica_ex1_s4.png';
import elastica_ex1_s5 from '/img/instruments/videomancer/elastica/elastica_ex1_s5.png';
import elastica_ex1_s6 from '/img/instruments/videomancer/elastica/elastica_ex1_s6.png';
import elastica_ex2_s1 from '/img/instruments/videomancer/elastica/elastica_ex2_s1.png';
import elastica_ex2_s2 from '/img/instruments/videomancer/elastica/elastica_ex2_s2.png';
import elastica_ex2_s3 from '/img/instruments/videomancer/elastica/elastica_ex2_s3.png';
import elastica_ex2_s4 from '/img/instruments/videomancer/elastica/elastica_ex2_s4.png';
import elastica_ex2_s5 from '/img/instruments/videomancer/elastica/elastica_ex2_s5.png';
import elastica_ex2_s6 from '/img/instruments/videomancer/elastica/elastica_ex2_s6.png';
import elastica_ex3_s1 from '/img/instruments/videomancer/elastica/elastica_ex3_s1.png';
import elastica_ex3_s2 from '/img/instruments/videomancer/elastica/elastica_ex3_s2.png';
import elastica_ex3_s3 from '/img/instruments/videomancer/elastica/elastica_ex3_s3.png';
import elastica_ex3_s4 from '/img/instruments/videomancer/elastica/elastica_ex3_s4.png';
import elastica_ex3_s5 from '/img/instruments/videomancer/elastica/elastica_ex3_s5.png';
import elastica_ex3_s6 from '/img/instruments/videomancer/elastica/elastica_ex3_s6.png';

# Elastica

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "House", before: elastica_source1_house, after: elastica_hero_s1 },
    { label: "Boat", before: elastica_source2_boat, after: elastica_hero_s2 },
    { label: "Collage", before: elastica_source3_collage, after: elastica_hero_s3 },
    { label: "Pattern", before: elastica_source4_pattern, after: elastica_hero_s4 },
    { label: "Woman", before: elastica_source5_woman, after: elastica_hero_s5 },
    { label: "Wood", before: elastica_source6_wood, after: elastica_hero_s6 },
  ]}
/>
*Elastica applying sine-wave horizontal displacement to create Scanimate-style rubber-sheet distortion with animated phase scrolling.*

---

## Overview

In the 1970s, a single machine dominated the world of broadcast motion graphics. The Scanimate — built by Computer Image Corporation — could stretch, bend, and animate video in real time by manipulating the deflection signals of a CRT monitor. Its signature trick was **per-scanline displacement**: each horizontal line of the video could be shifted left or right by a different amount, creating fluid, rubber-sheet distortions that turned flat logos into undulating, living things. Elastica recreates that core technique in the digital domain.

The program writes each incoming scanline into a dual-bank BRAM line buffer, then reads it back at a displaced address computed by a DDS (Direct Digital Synthesis) phase accumulator. The displacement waveform — selectable between sine, triangle, sawtooth, and square — determines the shape of the distortion. A second DDS provides vertical squeeze and stretch by selectively repeating or skipping scanlines. The two oscillators can be cross-modulated, and an animation accumulator scrolls the phase over time, recreating the Scanimate's signature ripple crawl. The name *Elastica* evokes both the elastic, rubber-sheet nature of the transformation and the mathematical *elastica* — the shape a flexible rod assumes under bending forces.

At low amplitudes and frequencies, Elastica produces gentle undulations and subtle wobbles. At high settings, the image shears apart into abstract bands, folds over itself, and compresses into dense accordion-like structures. The wet/dry mix fader allows any degree of blending between the original and warped signal.

---

## Background

### The Scanimate Legacy

The Scanimate was an analog computer that manipulated the electron beam of a high-resolution CRT monitor. By injecting function-generator signals into the CRT's horizontal and vertical deflection amplifiers, it could distort the raster pattern itself — stretching, squeezing, and bending the image in real time. The operator controlled the distortion with knobs and sliders, and the result was captured by a camera pointed at the CRT face. This analog feedback loop produced the iconic flowing, organic motion graphics seen in 1970s television — show openings, commercial logos, and network IDs. Only eight Scanimate machines were ever built.

### Rubber-Sheet Transforms

Mathematically, the Scanimate performs a **coordinate remapping**: each output pixel's position is displaced by a function of its original position. When the displacement varies smoothly across the image, the result looks like the image has been printed on a rubber sheet and then stretched. Elastica implements this as a per-scanline horizontal read-address offset — on each line, every pixel is read from a position shifted left or right by the displacement value. Because the displacement changes from line to line (driven by the DDS), different parts of the image shift by different amounts, producing the characteristic bowing, rippling, and shearing effects.

### Direct Digital Synthesis

DDS is a technique for generating arbitrary waveforms from a digital phase accumulator. A fixed-width register (32 bits in Elastica) is incremented by a tuning word on each clock event. The upper bits of the accumulator address a lookup table or are used directly to compute the waveform. The frequency of the output is determined by the ratio of the tuning word to the accumulator width and the clock rate. Because the accumulator wraps around naturally at its maximum value, the output is perfectly periodic. Elastica uses DDS for three oscillators: the horizontal warp (advances per scanline), the vertical warp (advances per scanline), and the animation phase (advances per frame).

### Per-Scanline Displacement

In a raster-scanned video system, the image is drawn one horizontal line at a time, from top to bottom. Elastica exploits this structure: as each new scanline arrives, the DDS phase accumulator advances by one step, producing a new displacement value. That value controls where in the line buffer each pixel is read from. The result is that the horizontal shift varies smoothly (or abruptly, depending on waveshape) down the vertical extent of the image. Sine waves produce smooth S-curves and undulations. Triangle waves produce zigzag folds. Sawtooth waves produce diagonal shear. Square waves produce hard left-right jumps, splitting the image into displaced blocks.

### Analog Video Synthesis History

Video synthesis — the creation and manipulation of imagery using electronic circuits rather than cameras — has deep roots in experimental art and broadcast television. Artists like Nam June Paik, the Vasulka brothers, and Dan Sandin built custom analog circuits that bent, colorized, and distorted video signals. Commercial systems like the Scanimate, Rutt/Etra, and Jones Colorizer brought these techniques to broadcast. Elastica sits squarely in this tradition: it treats the video signal not as a picture to be preserved but as a waveform to be sculpted. The DDS oscillators, waveshape selectors, and cross-modulation controls are direct analogs of the oscillators, waveshapers, and ring modulators found in analog video synthesizers.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Video Timing Generator ─────────────────────────────────────
│   └─ Edge detection: hsync, vsync, avid, field
│
├── DDS Oscillators ────────────────────────────────────────────
│   ├─ H-Warp DDS     (advances per scanline, freq = H Frequency)
│   ├─ Anim DDS       (advances per frame, rate = Anim Speed)
│   └─ V-Warp DDS     (advances per scanline, freq = V Frequency)
│
├── Waveshape Select ───────────────────────────────────────────
│   └─ Phase → displacement: sine(LUT) / triangle / sawtooth / square
│
├── Amplitude & Cross-Mod ─────────────────────────────────────
│   ├─ Cross-mod: |V-wave| × Cross-Mod scales H Amplitude
│   └─ Scaled displacement = waveshape × modulated amplitude
│
├── Read Address Calc ──────────────────────────────────────────
│   ├─ raw = pixel_index + scaled_displacement
│   └─ Clamp to [0, 2047] or Wrap (modular)
│
├── Line Buffer (mirror_delay_line_slv) ────────────────────────
│   ├─ Write: incoming scanline → Bank A/B (ping-pong)
│   └─ Read: displaced address → Bank B/A
│
├── Vertical Warp ──────────────────────────────────────────────
│   └─ V-wave × V Amplitude > threshold → repeat previous line
│
├── Wet/Dry Mix ────────────────────────────────────────────────
│   └─ interpolator_u × 3 (Y, U, V): dry(delayed) ↔ wet(warped)
│
└── Output (YUV 4:4:4)
```

The horizontal displacement path and the vertical warp path are largely independent but interact through cross-modulation. The H-Warp DDS produces a displacement waveform whose shape is set by Wave Sel A/B and whose frequency is set by H Frequency. This displacement is scaled by H Amplitude — but when Cross-Mod is above zero, the V-Warp DDS triangle output modulates the effective H Amplitude, creating 2D Lissajous-like distortion patterns. The vertical warp operates on a different principle: rather than displacing pixels, it repeats or skips entire scanlines based on a threshold comparison, creating vertical squeeze and stretch zones. Both horizontal displacement and vertical warp evolve over time when the Animate toggle is enabled, via a third DDS that adds a frame-rate phase offset to the horizontal accumulator.

---

## Parameter Reference

<img src={elastica_control_panel} alt="Videomancer front panel with Elastica loaded"/>
*Videomancer's front panel with Elastica active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — H Frequency
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the spatial frequency of the horizontal displacement waveform. At zero, the DDS tuning word is zero and no phase advancement occurs — the displacement is constant across all scanlines. As the knob increases, the waveform completes more cycles across the vertical extent of the frame. Low values produce broad, gentle bowing; mid-range values produce several visible undulations; high values create dense corrugation that can alias and beat against the scanline structure. The relationship between knob position and visible cycles is linear in the DDS tuning domain.

---

#### Knob 2 — H Amplitude
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Sets the peak horizontal displacement in pixels. At zero, the waveshape has no effect regardless of its frequency — the image passes through undistorted. Small values produce subtle shimmer and wobble. Moderate values create clearly visible bowing and shear. At maximum, pixels can be displaced by hundreds of positions, folding the image dramatically or pushing large portions off-screen (clamped) or wrapping them around (wrap mode). This is the primary "intensity" control for the horizontal warp effect.

---

#### Knob 3 — Anim Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the rate at which the displacement waveform scrolls vertically through the image over time. The animation DDS advances once per frame; this knob sets its tuning word. At zero, the warp pattern is frozen in place. At low values, the pattern drifts slowly — the signature Scanimate "ripple crawl." At high values, the pattern races through the image, creating rapid undulation. The animation phase is additive with the spatial phase, so the waveform shape and frequency remain constant while its vertical position scrolls.

---

#### Knob 4 — V Frequency
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |
| Suffix | % |

Controls the frequency of the vertical warp DDS, which generates a triangle wave used for vertical squeeze and stretch effects. Higher values create more zones of compression and expansion across the frame height. This oscillator also feeds the cross-modulation path — its output can modulate the horizontal displacement amplitude when Cross-Mod is above zero. Like H Frequency, the relationship between knob position and cycle count is linear in the DDS tuning domain.

---

#### Knob 5 — Cross-Mod
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls how strongly the vertical warp oscillator's triangle output modulates the horizontal displacement amplitude. At zero, the horizontal amplitude is uniform across all scanlines (set purely by H Amplitude). As Cross-Mod increases, scanlines near the peaks of the vertical triangle wave receive amplified horizontal displacement while scanlines near the zero-crossings receive reduced displacement. The result is a 2D distortion pattern where horizontal bowing concentrates in bands — creating egg-crate, diamond, or checkerboard-like warping depending on the H and V frequencies.

---

#### Knob 6 — V Amplitude
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Sets the intensity of the vertical warp effect — the degree of scanline repetition and skipping. At zero, all scanlines pass through normally. As the knob increases, regions where the V-wave triangle output is large cause scanlines to be repeated (the previous line is held and re-output), compressing the image vertically in those zones. The affected regions alternate with unaffected regions at a rate determined by V Frequency, creating bands of vertical squeeze separated by bands of normal resolution.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Wave Sel A** | Off | On |
| **8 — Wave Sel B** | Off | On |
| **9 — Edge Mode** | Clamp | Wrap |
| **10 — Animate** | Off | On |
| **11 — V-Warp** | Off | On |

Toggles 7 and 8 form a 2-bit waveshape selector (4 shapes) that determines the character of the horizontal distortion. Toggle 9 selects between two edge-handling behaviors for out-of-bounds read addresses. Toggle 10 enables or disables the animation phase scrolling. Toggle 11 enables the vertical warp pathway. There is no bypass toggle — the Mix fader at minimum serves the same purpose by crossfading fully to the dry signal.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0 – 100 |
| Default | 100 |

Wet/dry crossfade between the original (delayed) input and the warped output. At maximum (1023), the output is fully warped. At zero, the output is the unprocessed input — effectively a bypass. Intermediate positions blend the two, which can produce ghosting or double-exposure effects as the displaced and undisplaced images superimpose. Because the delayed dry signal is time-aligned with the wet output (both pass through the same pipeline depth), there is no temporal smearing at intermediate mix positions.

---

## Guided Exercises

These exercises progress from basic horizontal displacement through vertical warp and cross-modulation, building toward the full Scanimate experience. Each exercise specifies all twelve controls.

### Exercise 1: Classic Scanimate Ripple

<BeforeAfterSlider
  sources={[
    { label: "House", before: elastica_source1_house, after: elastica_ex1_s1 },
    { label: "Boat", before: elastica_source2_boat, after: elastica_ex1_s2 },
    { label: "Collage", before: elastica_source3_collage, after: elastica_ex1_s3 },
    { label: "Pattern", before: elastica_source4_pattern, after: elastica_ex1_s4 },
    { label: "Woman", before: elastica_source5_woman, after: elastica_ex1_s5 },
    { label: "Wood", before: elastica_source6_wood, after: elastica_ex1_s6 },
  ]}
/>
*Classic Scanimate Ripple — simulated result across source images.*
**Source**: A live camera feed or recorded footage with strong vertical lines — architecture, text, or geometric patterns.

**Objective**: Recreate the signature Scanimate horizontal ripple crawl using sine waveshape and animated phase scrolling.

1. **Set the waveshape**: Ensure Wave Sel A and Wave Sel B are both Off (sine waveshape).
2. **Base warp**: Set H Frequency to about 25% for two or three visible undulations across the frame height.
3. **Add amplitude**: Slowly increase H Amplitude from zero. Watch the vertical lines begin to bow left and right.
4. **Animate**: Confirm Animate is On (default). Set Anim Speed to about 25%. The warp pattern begins scrolling — this is the ripple crawl.
5. **Adjust speed**: Sweep Anim Speed. Low values give a lazy drift; high values give rapid undulation.
6. **Try Wrap mode**: Toggle Edge Mode to Wrap. Pixels that shift past the edge reappear on the opposite side — seamless looping distortion.

**Key concepts**: DDS phase accumulator drives displacement frequency, sine waveshape from quarter-wave LUT creates smooth organic bowing, animation phase offsets the waveform per frame

---

### Exercise 2: Vertical Squeeze and Cross-Modulation

<BeforeAfterSlider
  sources={[
    { label: "House", before: elastica_source1_house, after: elastica_ex2_s1 },
    { label: "Boat", before: elastica_source2_boat, after: elastica_ex2_s2 },
    { label: "Collage", before: elastica_source3_collage, after: elastica_ex2_s3 },
    { label: "Pattern", before: elastica_source4_pattern, after: elastica_ex2_s4 },
    { label: "Woman", before: elastica_source5_woman, after: elastica_ex2_s5 },
    { label: "Wood", before: elastica_source6_wood, after: elastica_ex2_s6 },
  ]}
/>
*Vertical Squeeze and Cross-Modulation — simulated result across source images.*
**Source**: Footage with horizontal features — landscape horizons, striped patterns, or text crawls.

**Objective**: Explore vertical warp and cross-modulation to create 2D distortion patterns.

1. **Start with H-warp**: Set H Frequency ~15%, H Amplitude ~30%, sine waveshape, Animate Off.
2. **Enable V-Warp**: Toggle V-Warp On. Set V Frequency to about 15% and V Amplitude to about 40%.
3. **Observe vertical compression**: Bands of the image squeeze and stretch vertically. Some scanlines repeat while others are skipped.
4. **Add cross-modulation**: Slowly increase Cross-Mod from zero. The horizontal displacement amplitude now varies vertically — it is strongest where the V-wave peaks and weakest at V-wave zero-crossings.
5. **Increase complexity**: Raise both H and V Frequency. The cross-modulation creates egg-crate or diamond patterns of distortion.
6. **Re-enable animation**: Toggle Animate On and set Anim Speed ~20%. The 2D pattern begins crawling through the image.

**Key concepts**: Vertical warp repeats/skips scanlines for compression, cross-modulation multiplies V-wave into H-amplitude for 2D patterns, combined frequencies create Lissajous-like spatial beats

---

### Exercise 3: Waveshape Comparison and Extreme Warp

<BeforeAfterSlider
  sources={[
    { label: "House", before: elastica_source1_house, after: elastica_ex3_s1 },
    { label: "Boat", before: elastica_source2_boat, after: elastica_ex3_s2 },
    { label: "Collage", before: elastica_source3_collage, after: elastica_ex3_s3 },
    { label: "Pattern", before: elastica_source4_pattern, after: elastica_ex3_s4 },
    { label: "Woman", before: elastica_source5_woman, after: elastica_ex3_s5 },
    { label: "Wood", before: elastica_source6_wood, after: elastica_ex3_s6 },
  ]}
/>
*Waveshape Comparison and Extreme Warp — simulated result across source images.*
**Source**: Any footage with recognizable content — faces, text, or graphic patterns.

**Objective**: Compare all four waveshapes at high amplitude and explore wrap-mode folding for abstract textures.

1. **High amplitude setup**: Set H Frequency ~20%, H Amplitude ~80%, Animate On, Anim Speed ~15%.
2. **Sine**: Wave Sel A Off, Wave Sel B Off. Observe smooth S-curve distortion.
3. **Triangle**: Wave Sel A On, Wave Sel B Off. The distortion becomes a zigzag — sharper folds, linear segments.
4. **Sawtooth**: Wave Sel A Off, Wave Sel B On. The image shears diagonally — an italic-like lean that reverses at the wrap point.
5. **Square**: Wave Sel A On, Wave Sel B On. The image splits into hard-displaced horizontal blocks — half shift left, half shift right.
6. **Wrap mode**: Toggle Edge Mode to Wrap. At high amplitude, the wrapping creates kaleidoscopic folding as displaced pixels tile around.
7. **Mix blend**: Pull Mix to about 50%. The warped and unwarped images superimpose, creating ghostly double-exposure textures.

**Key concepts**: Waveshape determines distortion character (organic vs geometric vs shear vs blocky), wrap mode creates seamless tiling at high displacement, partial mix creates double-exposure layering

---


## Tips

- **Start with sine**: Sine waveshape gives the most natural, Scanimate-authentic results. Dial in frequency and amplitude before exploring other waveshapes.
- **Low Anim Speed for elegance**: The classic ripple crawl is a slow, hypnotic drift. Anim Speed around 10–15% captures the vintage feel; higher speeds are useful for frenetic effects.
- **Cross-mod creates 2D patterns**: Even without V-Warp enabled, Cross-Mod routes the V-DDS triangle into the horizontal amplitude path, creating spatial amplitude modulation. V-Warp adds the separate scanline-repetition effect on top.
- **Wrap mode for feedback**: When routing the output back to the input, Wrap mode prevents edge-clamped color from accumulating and instead creates seamless tileable feedback patterns.
- **Mix for double exposure**: Intermediate mix positions superimpose the warped and unwarped images, useful for creating ghostly layering effects or motion-blur-like smears.
- **Square wave for rhythmic displacement**: Square waveshape splits the image into two hard-displaced halves — excellent for glitch aesthetics and blocky displacement keyed to a beat.
- **V-Warp alone for vertical effects**: Toggle V-Warp On with H Amplitude at zero to isolate pure vertical squeeze/stretch without horizontal distortion.
- **Frequency ratio matters**: The ratio of H Frequency to V Frequency determines the 2D pattern when cross-modulation is active. Simple ratios (1:1, 1:2, 2:3) produce stable patterns; complex ratios create evolving moire-like textures.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; dedicated memory resources within the FPGA fabric used to store one full scanline for displaced readback. |
| **Cross-Modulation** | Using the output of one oscillator to control a parameter of another; here the V-wave triangle modulates the H-warp amplitude. |
| **DDS** | Direct Digital Synthesis; a technique for generating periodic waveforms using a phase accumulator and lookup table or arithmetic. |
| **Displacement** | Shifting pixel read positions horizontally by an offset derived from the warp waveform, causing spatial distortion. |
| **Lissajous** | Complex 2D patterns formed by combining two perpendicular oscillations at different frequencies, analogous to the cross-modulated H/V warp. |
| **Phase Accumulator** | A register that increments by a tuning word each clock event; its upper bits encode the instantaneous phase of the output waveform. |
| **Ping-Pong** | Alternating between two memory banks so that one can be written while the other is read, avoiding read-write conflicts. |
| **Quarter-Wave LUT** | A sine lookup table storing only one quarter of the full cycle; symmetry properties reconstruct the remaining three quarters. |
| **Rubber-Sheet Transform** | A continuous spatial distortion where output pixel positions are displaced versions of input positions, as if the image were printed on elastic material. |
| **Scanimate** | An analog video computer built by Computer Image Corporation in the 1970s, capable of real-time per-scanline video distortion. |
| **Tuning Word** | The increment value added to a DDS phase accumulator on each clock event; determines the output frequency. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
