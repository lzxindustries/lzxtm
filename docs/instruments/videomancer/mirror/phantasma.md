---
draft: true
sidebar_position: 197
slug: /instruments/videomancer/phantasma
title: "Phantasma"
image: /img/instruments/videomancer/phantasma/phantasma_hero.png
description: "Phantasma is a pattern generator disguised as a video processor."
---

import phantasma_before_after from '/img/instruments/videomancer/phantasma/phantasma_before_after.png';
import phantasma_control_panel from '/img/instruments/videomancer/phantasma/phantasma_control_panel.png';
import phantasma_exercise1_result from '/img/instruments/videomancer/phantasma/phantasma_exercise1_result.png';
import phantasma_exercise2_result from '/img/instruments/videomancer/phantasma/phantasma_exercise2_result.png';
import phantasma_exercise3_result from '/img/instruments/videomancer/phantasma/phantasma_exercise3_result.png';
import phantasma_hero from '/img/instruments/videomancer/phantasma/phantasma_hero.png';
import phantasma_source1_kodim01 from '/img/instruments/videomancer/phantasma/phantasma_source1_kodim01.png';
import phantasma_source2_kodim02 from '/img/instruments/videomancer/phantasma/phantasma_source2_kodim02.png';
import phantasma_source3_kodim01_bw from '/img/instruments/videomancer/phantasma/phantasma_source3_kodim01_bw.png';

# Phantasma

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={phantasma_hero} alt="Phantasma hero image"/>
*Phantasma generating luma-reactive warped horizontal stripe patterns that blend with the source video via DDS phase accumulation and proc_amp modulation.*
<img src={phantasma_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Phantasma applied.*

---

## Overview

Phantasma is a pattern generator disguised as a video processor. It synthesises horizontal stripe patterns using DDS (Direct Digital Synthesis) phase accumulators and then blends those patterns with the input video at a controllable depth. The stripes are not static — they respond to the brightness of the source image through three independent luma-modulation paths, making the pattern wrap, bend, and animate in response to video content.

The name *Phantasma* — Greek for "apparition" — fits the visual result: translucent geometric striations that appear to float over or within the source image, shifting as the luma contours of the video shift. The program sits in the Mirror category because its warp and flip controls create symmetric, reflected patterns reminiscent of kaleidoscopic mirror effects.

At low Luma Depth settings, Phantasma adds subtle stripe textures to the source. At full depth, it replaces the video entirely with a monochrome pattern — a pure synthesis output driven by the DDS oscillators. The six knobs control stripe frequency, warp displacement, phase offset, and their respective luma-modulation depths, giving precise control over how strongly the input video influences the generated pattern.


---

## Background

### Direct Digital Synthesis (DDS)

DDS is a technique for generating precise waveforms by accumulating a phase value on every clock tick and using the accumulated phase to look up an amplitude. In Phantasma, two 16-bit phase accumulators run at different rates — one advances per pixel (horizontal stripes) and one advances per line (vertical warp). The upper 10 bits of each accumulator produce a 10-bit ramp that sweeps repeatedly from 0 to 1023. The frequency word (derived from the Width and Warp knobs) controls how fast the ramp repeats: higher values mean more stripe cycles per screen width or more warp cycles per screen height.

### Proc Amp Modulation

Phantasma uses three instances of `proc_amp_u` — the standard Videomancer processing amplifier — to modulate the DDS output with the input video's luminance. The proc_amp formula is: `result = (luma − 512) × contrast / 512 + brightness`. Here, `contrast` is the Luma-to-Width/Warp/Phase depth control, and `brightness` is the base DDS ramp value. When the modulation depth is at center (512 = zero contrast), the proc_amp passes the base ramp unchanged. As you increase the depth, bright and dark regions of the input video push the ramp value in opposite directions, making the stripe pattern warp according to the image content.

### Frequency Doubling and Waveform Shaping

The raw DDS output is a sawtooth (ramp) waveform. The `frequency_doubler` module folds the ramp into a triangle wave by reflecting values above the midpoint. Phantasma uses two frequency doublers: one for the warp displacement (controlled by the Mirror and Warp Shape toggles) and one for the stripe output (controlled by Flip). A ramp warp produces asymmetric, sweeping displacements. A triangle warp produces symmetric, mirror-like displacements. Similarly, ramp stripes have a sharp dark-to-bright transition, while triangle (flipped) stripes are symmetrically graded.

### Phase Modulation and Warping

The final stripe pattern is the sum of three phase components: the luma-modulated horizontal ramp, the warp-shaped vertical displacement, and the luma-modulated phase offset. This additive phase combination is the same principle used in FM synthesis — one oscillator modulates the phase of another. The wrapping unsigned addition creates smooth cyclic patterns with no discontinuities, even when the modulation pushes values past the 10-bit boundary.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Timing Extraction ──────────────────────────────────────────
│   └─ video_timing_generator → h/v/avid timing signals
│
├── DDS Phase Accumulators ─────────────────────────────────────
│   ├─ Horizontal accumulator (pixel-rate, Width freq word)
│   └─ Vertical accumulator (line-rate, Warp freq word)
│
├── Luma Modulation (3× proc_amp_u) ────────────────────────────
│   ├─ Luma→Width:  (Y−512)×L2W/512 + ramp_h → s_mod_width
│   ├─ Luma→Warp:   (Y−512)×L2Warp/512 + ramp_v → s_mod_warp
│   └─ Luma→Phase:  (Y−512)×L2Ph/512 + phase → s_mod_phase
│
├── Warp Waveshaping ───────────────────────────────────────────
│   └─ frequency_doubler (bypass = NOT(mirror OR warp_shape))
│       → s_warp_shaped (ramp or triangle)
│
├── Phase Combination ──────────────────────────────────────────
│   └─ s_warped_phase = s_mod_width + s_warp_shaped
│                      + s_mod_phase − 512  (wrapping add)
│
├── Stripe Waveshaping ─────────────────────────────────────────
│   └─ frequency_doubler (bypass = NOT flip)
│       → s_stripe_shaped (ramp or triangle stripes)
│
├── Output Inversion ───────────────────────────────────────────
│   └─ s_output_y = 1023 − s_stripe_shaped  (if Luma Invert)
│
├── Mix (3× interpolator_u) ────────────────────────────────────
│   ├─ Y: lerp(input_y, output_y, luma_depth)
│   ├─ U: lerp(input_u, 512, luma_depth)  → desaturate
│   └─ V: lerp(input_v, 512, luma_depth)  → desaturate
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or mixed signal
```

The key architectural insight is that Phantasma is a *three-oscillator FM synthesizer* projected onto the pixel grid. The horizontal accumulator is the carrier, the vertical accumulator is the modulator, and the phase offset is a static bias. Input video luma acts as a fourth modulation source that affects all three oscillator parameters simultaneously via proc_amp_u. The UV channels of the output are not generated — instead, the mix interpolator crossfades the input UV toward center (512), progressively desaturating the image as the pattern replaces it. At full Luma Depth the output is monochrome stripes; at zero depth the output is the untouched input video.

---

## Parameter Reference

<img src={phantasma_control_panel} alt="Videomancer front panel with Phantasma loaded"/>
*Videomancer's front panel with Phantasma active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Width
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the horizontal stripe frequency via the DDS phase accumulator. Higher values produce more stripe cycles across the screen width — thin, closely-spaced stripes. Lower values produce fewer, wider stripes. The frequency word is constructed as the 10-bit register value padded into a 16-bit accumulator, so the stripe count scales linearly with the knob position. At zero, the accumulator barely advances and the pattern is a single broad gradient.

---

#### Knob 2 — Warp
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the vertical warp frequency. This DDS accumulator runs at line rate, producing a warp displacement that varies from top to bottom of the frame. Higher values create more warp oscillation cycles, making the stripes undulate rapidly across the vertical axis. Lower values produce slow, broad warp sweeps. Combined with waveshaping (Mirror/Warp Shape), this creates the characteristic sinuous stripe distortion.

---

#### Knob 3 — Phase
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

A static phase offset added to the warped stripe pattern. Sweeping this knob scrolls the entire stripe pattern horizontally without changing its frequency or warp shape. At center (512), the phase offset is neutral. Because the addition wraps cyclically (unsigned overflow produces smooth wraparound), the phase control provides continuous scrolling without discontinuities.

---

#### Knob 4 — Luma to Width
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls how strongly the input video's luminance modulates the stripe width (horizontal DDS frequency). This is the `contrast` input to the Width proc_amp_u. At center (512), no modulation occurs and the stripe frequency is uniform across the image. Moving away from center makes bright regions of the input produce different stripe spacing than dark regions, creating content-adaptive patterns that follow the video's tonal structure.

---

#### Knob 5 — Luma to Warp
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls luma modulation depth for the vertical warp displacement. At center, the warp pattern is uniform regardless of video content. Away from center, bright and dark regions of the input shift the warp displacement in opposite directions, making the stripe distortion follow the image brightness contours.

---

#### Knob 6 — Luma to Phase
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls luma modulation depth for the phase offset. At center, the phase is spatially uniform (only the static Phase knob matters). Away from center, the phase shifts per-pixel based on input brightness, creating position-dependent stripe shifts that make the pattern appear to slide or shimmer across the video content.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Flip** | Off | On |
| **8 — Mirror** | Off | On |
| **9 — Warp Shape** | Ramp | Triangle |
| **10 — Luma Invert** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control waveshaping and output polarity options. Flip and Mirror/Warp Shape affect the frequency doubler modules that convert ramp waveforms to triangle waves. Luma Invert flips the output brightness. Each toggle is independently wired — they do not form a combined mode selector. **Important**: Phantasma uses an unpacked toggle ABI where each toggle occupies its own register (7–10) rather than being packed into bits of register 6.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Luma Depth
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the depth of the pattern blend (Luma Depth). At 0% (register = 0), the output is pure input video — the stripes are invisible. At 100% (register = 1023), the output is fully replaced by the generated stripe pattern (Y channel) and neutral gray (UV channels = 512). At intermediate values, the stripes appear as a semi-transparent overlay that progressively desaturates the source image as depth increases.

---

## Guided Exercises

These exercises progress from simple stripe generation to complex luma-reactive pattern synthesis, building familiarity with each stage of the DDS + proc_amp modulation chain.

### Exercise 1: Basic Stripes

<img src={phantasma_exercise1_result} alt="Basic Stripes result"/>
*Basic Stripes — simulated result across source images.*
**Source**: Any color video footage — a face, landscape, or colorful test pattern.

**Objective**: Understand the DDS stripe generator and waveshaping controls.

1. **Full pattern**: Set Luma Depth to 100% to see the raw pattern with no video blend.
2. **Stripe frequency**: Sweep Width from low to high. Watch the stripe count increase from a single broad gradient to dozens of thin stripes.
3. **Ramp vs triangle**: Toggle Flip. Observe the sawtooth-to-triangle transition.
4. **Add warp**: Increase Warp to ~50%. Vertical displacement curves appear in the stripes.
5. **Mirror warp**: Toggle Mirror on. The sweeping warp becomes symmetric and kaleidoscopic.
6. **Scroll**: Sweep Phase to scroll the pattern smoothly.

**Key concepts**: DDS frequency controls stripe count, frequency doubler (Flip) converts ramp to triangle, warp adds vertical displacement, Phase scrolls the entire pattern

---

### Exercise 2: Luma-Reactive Patterns

<img src={phantasma_exercise2_result} alt="Luma-Reactive Patterns result"/>
*Luma-Reactive Patterns — simulated result across source images.*
**Source**: High-contrast footage with clear tonal regions — a face with highlights and shadows, or a black-and-white graphic.

**Objective**: Explore how input video brightness modulates the stripe pattern via the three proc_amp paths.

1. **Prepare**: Set Width ~30%, Warp ~30%, Phase ~50%, Flip on, Luma Depth 100%.
2. **Width modulation**: Sweep Luma to Width away from center. Watch the stripe spacing change according to the video brightness — bright areas get different stripe density than dark areas.
3. **Warp modulation**: Return L2W to center, sweep Luma to Warp. The vertical warp displacement now follows the video content — stripes bend around bright/dark boundaries.
4. **Phase modulation**: Return L2Warp to center, sweep Luma to Phase. The pattern slides laterally based on brightness.
5. **Combine**: Set all three modulation depths to moderate values (~60%). The pattern becomes a complex, content-adaptive structure.

**Key concepts**: Proc_amp modulation uses (luma − 512) × depth / 512 + base, center depth = neutral (no modulation), away from center = video-reactive pattern

---

### Exercise 3: Pattern Overlay

<img src={phantasma_exercise3_result} alt="Pattern Overlay result"/>
*Pattern Overlay — simulated result across source images.*
**Source**: Colorful video footage — performance footage, animation, or nature scenes with saturated colors.

**Objective**: Blend the generated pattern with the source video at various depths, exploring the desaturation behaviour.

1. **Set a pattern**: Width ~40%, Warp ~40%, Flip on, Mirror on.
2. **Reduce depth**: Lower Luma Depth to ~50%. The stripes become a translucent overlay on the source video.
3. **Watch color**: As Luma Depth increases, the source desaturates because the UV mix crossfades toward center (512). At full depth, the output is monochrome.
4. **Invert**: Toggle Luma Invert. The stripe polarity flips, changing which areas are dark vs bright.
5. **Content modulation**: Set Luma to Width ~70% at ~40% depth. The stripes wrap around the video content while remaining semi-transparent.
6. **Edge highlight**: Use low Width, low Warp, high Luma to Width. The pattern emphasises tonal edges in the video.

**Key concepts**: Luma Depth crossfades Y with pattern and UV with center (512), progressive desaturation as depth increases, overlay creates ghostly stripe textures

---


## Tips

- **Luma Depth is the master blend**: At zero, Phantasma does nothing visible. Start at 100% to design the pattern, then pull back to find the ideal overlay strength.
- **Center = neutral for modulation knobs**: All three Luma-to-* knobs cancel their modulation at the 50% mark. Sweep them symmetrically above and below center to see opposite modulation polarities.
- **Flip for symmetry**: Ramp stripes have a hard edge; triangle (Flip on) stripes are smooth and symmetric. Triangle mode is usually more visually pleasing for overlays.
- **Mirror for kaleidoscopes**: Mirror creates symmetric warp patterns that evoke lens or mirror effects, which is why the program sits in the Mirror category.
- **Feedback loops**: Routing the output back to the input creates recursive luma modulation — the stripes react to themselves, producing complex self-organising patterns.
- **Monochrome at full depth**: At 100% Luma Depth, the UV channels are fully desaturated. Use this for intentional monochrome pattern replacement.
- **Unpacked toggles**: If building custom control mappings, remember that Phantasma's toggles use registers 7–10 individually, not packed into register 6 bits.

---

## Glossary

| Term | Definition |
|------|------------|
| **DDS** | Direct Digital Synthesis; a technique for generating waveforms by incrementing a phase accumulator and using the result to index a lookup table. |
| **Frequency Doubler** | A waveshaping module that folds a ramp (sawtooth) waveform into a triangle by reflecting values above the midpoint, effectively doubling the apparent frequency. |
| **LFSR** | Linear-Feedback Shift Register; a shift register whose input bit is a function of its previous state, producing pseudo-random sequences. |
| **Luma Depth** | The crossfade parameter controlling how much of the generated pattern replaces the input video. |
| **Phase Accumulator** | A counter that adds a frequency word each tick, producing a repeating ramp whose rate is proportional to the word value. |
| **Proc amp** | Processing amplifier; a gain-and-offset stage that applies contrast (multiplication) and brightness (addition) to a signal. |
| **Ramp** | A sawtooth waveform that rises linearly from 0 to maximum, then jumps back to 0. |
| **Triangle** | A waveform that rises linearly from 0 to maximum, then falls linearly back to 0, producing symmetric peaks. |
| **Unpacked Toggle ABI** | A non-standard register layout where each toggle switch uses its own full register, rather than sharing bit positions within a single packed register. |
| **Warp** | Vertical displacement applied to the horizontal stripe pattern, causing straight lines to undulate. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V); the native format of Videomancer's 30-bit video pipeline. |
