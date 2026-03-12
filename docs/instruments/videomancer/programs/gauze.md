---
draft: true
sidebar_position: 125
slug: /instruments/videomancer/gauze
title: "Gauze"
image: /img/instruments/videomancer/gauze/gauze_hero_s1.png
description: "Video images contain spatial detail at every scale — broad gradients, mid-frequency textures, and fine pixel-level edges."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import gauze_control_panel from '/img/instruments/videomancer/gauze/gauze_control_panel.png';
import gauze_source1_house from '/img/instruments/videomancer/gauze/gauze_source1_house.png';
import gauze_source2_dog from '/img/instruments/videomancer/gauze/gauze_source2_dog.png';
import gauze_source3_turtle from '/img/instruments/videomancer/gauze/gauze_source3_turtle.png';
import gauze_source4_pattern from '/img/instruments/videomancer/gauze/gauze_source4_pattern.png';
import gauze_source5_woman from '/img/instruments/videomancer/gauze/gauze_source5_woman.png';
import gauze_source6_berries from '/img/instruments/videomancer/gauze/gauze_source6_berries.png';
import gauze_hero_s1 from '/img/instruments/videomancer/gauze/gauze_hero_s1.png';
import gauze_hero_s2 from '/img/instruments/videomancer/gauze/gauze_hero_s2.png';
import gauze_hero_s3 from '/img/instruments/videomancer/gauze/gauze_hero_s3.png';
import gauze_hero_s4 from '/img/instruments/videomancer/gauze/gauze_hero_s4.png';
import gauze_hero_s5 from '/img/instruments/videomancer/gauze/gauze_hero_s5.png';
import gauze_hero_s6 from '/img/instruments/videomancer/gauze/gauze_hero_s6.png';
import gauze_ex1_s1 from '/img/instruments/videomancer/gauze/gauze_ex1_s1.png';
import gauze_ex1_s2 from '/img/instruments/videomancer/gauze/gauze_ex1_s2.png';
import gauze_ex1_s3 from '/img/instruments/videomancer/gauze/gauze_ex1_s3.png';
import gauze_ex1_s4 from '/img/instruments/videomancer/gauze/gauze_ex1_s4.png';
import gauze_ex1_s5 from '/img/instruments/videomancer/gauze/gauze_ex1_s5.png';
import gauze_ex1_s6 from '/img/instruments/videomancer/gauze/gauze_ex1_s6.png';
import gauze_ex2_s1 from '/img/instruments/videomancer/gauze/gauze_ex2_s1.png';
import gauze_ex2_s2 from '/img/instruments/videomancer/gauze/gauze_ex2_s2.png';
import gauze_ex2_s3 from '/img/instruments/videomancer/gauze/gauze_ex2_s3.png';
import gauze_ex2_s4 from '/img/instruments/videomancer/gauze/gauze_ex2_s4.png';
import gauze_ex2_s5 from '/img/instruments/videomancer/gauze/gauze_ex2_s5.png';
import gauze_ex2_s6 from '/img/instruments/videomancer/gauze/gauze_ex2_s6.png';
import gauze_ex3_s1 from '/img/instruments/videomancer/gauze/gauze_ex3_s1.png';
import gauze_ex3_s2 from '/img/instruments/videomancer/gauze/gauze_ex3_s2.png';
import gauze_ex3_s3 from '/img/instruments/videomancer/gauze/gauze_ex3_s3.png';
import gauze_ex3_s4 from '/img/instruments/videomancer/gauze/gauze_ex3_s4.png';
import gauze_ex3_s5 from '/img/instruments/videomancer/gauze/gauze_ex3_s5.png';
import gauze_ex3_s6 from '/img/instruments/videomancer/gauze/gauze_ex3_s6.png';

# Gauze

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "House", before: gauze_source1_house, after: gauze_hero_s1 },
    { label: "Dog", before: gauze_source2_dog, after: gauze_hero_s2 },
    { label: "Turtle", before: gauze_source3_turtle, after: gauze_hero_s3 },
    { label: "Pattern", before: gauze_source4_pattern, after: gauze_hero_s4 },
    { label: "Woman", before: gauze_source5_woman, after: gauze_hero_s5 },
    { label: "Berries", before: gauze_source6_berries, after: gauze_hero_s6 },
  ]}
/>
*Gauze applying per-channel cascaded IIR filtering with fade — softening chrominance while sharpening luminance to reveal hidden edge structure.*

---

## Overview

Video images contain spatial detail at every scale — broad gradients, mid-frequency textures, and fine pixel-level edges. Gauze separates these scales channel by channel, letting you independently soften or sharpen the luminance and chrominance components of the signal. The result can range from a subtle diffusion filter that gently rolls off high-frequency detail to an aggressive edge extractor that strips away everything except transitions.

The name evokes the semi-transparent fabric used in photography and stage lighting to soften harsh detail. Like physical gauze placed over a lens, the program blurs and veils — but it can also do the opposite, removing the smooth content and exposing only the edges underneath. Because each YUV channel has independent horizontal and vertical controls, you can create highly selective filtering topologies: soften color while sharpening luma, blur horizontally while extracting vertical edges, or cascade two filter stages to build bandpass responses that isolate specific spatial frequency bands.

At default settings (all cutoffs centered, low-pass mode, no fade), Gauze passes the signal through unchanged. As you move the cutoff knobs away from their centers, filtering progressively reshapes the image. The six-knob, three-toggle, two-stage architecture provides 64 distinct filter topology combinations per channel — a level of spatial control rarely available in a single module.

---

## Quick Start

1. **Center is zero**: The three vertical cutoff knobs are bipolar — center position means no vertical filtering. Think of them as a "dead zone" in the middle with LP on one side and HP on the other.
2. **Cascade for steeper rolloff**: A single LP filter gives a gentle rolloff. Cascading two LP stages (LP horizontal + LP vertical) gives a much steeper, more dramatic blur. The same applies to HP — cascading two HP stages gives sharper edge extraction.
3. **Chroma blur is your friend**: Blurring U and V while keeping Y sharp is one of the most universally useful processing patches. It reduces color noise and creates a painterly softness without sacrificing luminance detail.

---

## Background

### IIR Digital Filters: Low-Pass and High-Pass

Gauze's core building block is an **Infinite Impulse Response** (IIR) low-pass filter. The filter maintains an internal state value that chases the input signal: on each clock cycle, the state moves toward the current input by a fraction determined by the cutoff coefficient. When the cutoff is high, the state tracks the input closely and passes most detail through. When the cutoff is low, the state changes slowly, averaging out rapid fluctuations and producing a smooth, blurred output. The high-pass output is simply the input minus the low-pass output — whatever the low-pass filter removes, the high-pass filter retains. Together, they form a complementary pair: the low-pass contains the slowly varying content, and the high-pass contains the rapidly varying edges and texture.

### Per-Channel Spatial Filtering in YUV

Videomancer processes video in YUV 4:4:4 color space, where Y carries brightness and U/V carry color difference information. Gauze applies separate, independent filters to each of these three channels. This is significant because the human visual system is far more sensitive to luminance detail than to chrominance detail. Blurring the U and V channels while leaving Y sharp produces a soft, painterly color field with crisp luminance edges — a technique used in broadcast television to reduce chroma noise. Conversely, blurring Y while sharpening U and V produces an unusual effect where color boundaries become more prominent than brightness boundaries, reversing normal perceptual expectations.

### Cutoff Frequency and Sigma-Delta Dithering

The cutoff parameter controls how aggressively the filter smooths the signal. Internally, the 10-bit knob value is split into two parts: the upper 8 bits set a coarse shift amount that determines the filter's step size, and the lower bits drive a sigma-delta modulator that averages between adjacent shift values over time. This dithering technique creates 16 sub-steps between each coarse level, giving the cutoff control a smooth, continuous feel rather than the stepped jumps that a pure bit-shift approach would produce. The result is fine-grained control over the degree of blur or edge extraction, with no audible or visible quantization artifacts in the filter response.

### Horizontal and Vertical Filtering Dimensions

Each channel passes through two cascaded filter stages. The first stage operates **horizontally** — it processes pixels left to right within each scan line, smoothing (or sharpening) spatial detail along the horizontal axis. The second stage operates **vertically** — it processes the output of the horizontal stage across successive pixels in the same column position, smoothing (or sharpening) across scan lines. Cascading two filters creates four possible topologies per channel: LP→LP produces a two-pole low-pass with steeper rolloff, HP→HP produces a two-pole high-pass that extracts only the sharpest edges, LP→HP and HP→LP each produce bandpass responses that pass mid-frequency detail while rejecting both the broadest gradients and the finest texture.

### Fade-to-Color as Creative Effect

After filtering, Gauze offers a crossfade stage that interpolates between the processed signal and a solid color target. For the Y channel, the target is either black or white (selected by the Fade Color toggle). For the U and V channels, the target is always neutral gray (code 512), which corresponds to zero saturation. At maximum fade, the output is a uniform flat field. At intermediate fade values, the processed image bleeds through as a ghost — edges and texture float over a colored background. This is especially powerful in combination with high-pass filtering: extracting edges and then fading toward black produces a dark field with luminous edge traces, reminiscent of wireframe renders or etched metal.


---

## Signal Flow

Input Capture → Horizontal IIR Filter → Vertical IIR Filter → V Mux → Fade Interpolator

```
Input Video (YUV 4:4:4, 10-bit unsigned)
│
├── Stage 1: Input Capture ──────────────────────── 1 clk
│   unsigned 10-bit → signed 12-bit (zero-extend + resize)
│
├── Stage 2: Horizontal IIR Filter ──────────────── 1 clk
│   3× variable_filter_s (Y, U, V)
│   ├── Cutoff: YH Cutoff / UH Cutoff / VH Cutoff (upper 8 bits)
│   ├── Outputs: LP + HP per channel
│   └── Mode mux: Y Mode / U Mode / V Mode toggle selects LP or HP
│
├── Stage 3: Vertical IIR Filter ────────────────── 1 clk
│   3× variable_filter_s (Y, U, V) cascaded from H-mux output
│   ├── Cutoff: distance from center of YV / UV / VV knob
│   └── Outputs: LP + HP per channel
│
├── Stage 4: V Mux + Unsigned Conversion ────────── 1 clk
│   ├── Direction mux: knob above center → LP, below center → HP
│   └── Signed 12-bit → unsigned 10-bit (clamped [0, 1023])
│
├── Stage 5: Fade Interpolator ──────────────────── 4 clk
│   3× interpolator_u (Y, U, V)
│   ├── Y: crossfade between filtered Y and fade color (0 or 1023)
│   ├── U: crossfade between filtered U and neutral (512)
│   ├── V: crossfade between filtered V and neutral (512)
│   └── Mix amount: Fade Amount fader
│
├── Sync Delay Compensation ─────────────────────── 8-stage shift register
│   └── hsync, vsync, field, original Y/U/V delayed to match pipeline
│
└── Output with Bypass Mux
    └── Bypass toggle selects processed or delayed original
```

The horizontal mode toggles and the vertical cutoff knobs work at different points in the cascade. The mode toggle (LP/HP) determines which output of the *horizontal* filter feeds into the vertical stage. The vertical knob position determines both the cutoff frequency *and* the direction (LP or HP) of the second filter stage. This means the horizontal toggle and vertical knob interact to produce four distinct topologies — LP→LP, LP→HP, HP→LP, HP→HP — each with independently variable cutoff frequencies for both stages.

The fade interpolator sits after all filtering and operates in unsigned 10-bit space. Its `a` input is the fade target (constant) and its `b` input is the filtered pixel, with `t` (the Fade Amount fader) controlling the mix. When the fader is at maximum (1023), the output equals the filtered signal. When the fader is at minimum (0), the output is the constant fade color. This is a linear crossfade with 4-stage pipelined multiply-and-add, matching the `interpolator_u` entity at full 10-bit fractional precision.

---

## Parameter Reference

<img src={gauze_control_panel} alt="Videomancer front panel with Gauze loaded"/>
*Videomancer's front panel with Gauze active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — YH Cutoff
| Property | Value |
|----------|-------|
| Range | 0.0% – 200.0% |
| Default | 100.1% |
| Suffix | % |

Controls the horizontal filter cutoff for the Y (luminance) channel. As the knob increases from the minimum position, the IIR filter tracks the input more closely, passing progressively finer horizontal detail. At lower settings, the luminance is heavily blurred in the horizontal direction — broad gradients survive but texture and edges are smoothed away. At higher settings, the filter is nearly transparent and the original horizontal detail is preserved. This is the primary control for the overall sharpness or softness of the brightness component.

---

#### Knob 2 — UH Cutoff
| Property | Value |
|----------|-------|
| Range | 0.0% – 200.0% |
| Default | 100.1% |
| Suffix | % |

Controls the horizontal filter cutoff for the U (blue-difference chrominance) channel. Because human vision is less sensitive to chroma detail, even moderate settings produce a visible softening of blue-cyan-magenta color transitions. Setting this low while keeping YH Cutoff high creates a classic broadcast-style chroma blur — sharp luma edges with smooth, diffused color. Setting it high preserves the full sharpness of the U channel's color transitions.

---

#### Knob 3 — VH Cutoff
| Property | Value |
|----------|-------|
| Range | 0.0% – 200.0% |
| Default | 100.1% |
| Suffix | % |

Controls the horizontal filter cutoff for the V (red-difference chrominance) channel. This operates identically to UH Cutoff but on the red-yellow-green axis. Reducing V horizontal cutoff independently from U lets you blur warm color transitions while keeping cool colors sharp, or vice versa — an unusual chromatic separation that can produce distinctive color-fringing effects at edges.

---

#### Knob 4 — YV Cutoff
| Property | Value |
|----------|-------|
| Range | -100.0% – 100.0% |
| Default | 0.1% |
| Suffix | % |

Controls the vertical (second-stage) filter for the Y channel. The knob has a bipolar behavior centered at its midpoint. At the center position, the vertical filter is fully attenuated and the stage passes the horizontal output unchanged. Turning the knob clockwise from center engages a vertical low-pass filter with increasing strength — the image blurs vertically, smearing detail across scan lines. Turning counter-clockwise from center engages a vertical high-pass filter — the image sharpens vertically, extracting horizontal edges. Combined with the horizontal mode toggle, this creates four distinct Y-channel filter topologies.

---

#### Knob 5 — UV Cutoff
| Property | Value |
|----------|-------|
| Range | -100.0% – 100.0% |
| Default | 0.1% |
| Suffix | % |

Controls the vertical filter for the U channel with the same bipolar center-null behavior as YV Cutoff. The center position passes the horizontal U output unchanged. Clockwise adds vertical low-pass (vertical chroma blur); counter-clockwise adds vertical high-pass (horizontal chroma edge extraction). Because U carries the blue-yellow color axis, vertical high-pass on U reveals horizontal boundaries where the image transitions between warm and cool tones.

---

#### Knob 6 — VV Cutoff
| Property | Value |
|----------|-------|
| Range | -100.0% – 100.0% |
| Default | 0.1% |
| Suffix | % |

Controls the vertical filter for the V channel with the same bipolar center-null behavior. Clockwise adds vertical low-pass; counter-clockwise adds vertical high-pass. Because V carries the red-cyan color axis, vertical filtering on V selectively blurs or sharpens red-green transitions in the vertical dimension. Setting all three vertical cutoffs to different positions and directions creates complex per-channel spatial responses that are difficult to achieve with conventional video processors.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Y Mode** | Low Pass | High Pass |
| **8 — U Mode** | Low Pass | High Pass |
| **9 — V Mode** | Low Pass | High Pass |
| **10 — Fade Color** | Black | White |
| **11 — Bypass** | Off | On |

Toggles 7–9 control the horizontal filter mode for each YUV channel independently. They determine whether the horizontal stage outputs the low-pass (smoothed) or high-pass (edge-extracted) signal to the cascaded vertical stage. Toggle 10 selects the fade target color, and toggle 11 provides instant bypass for A/B comparison. The mode toggles interact with the vertical cutoff knobs: switching from LP to HP changes the entire character of the cascaded filter, since the vertical stage then processes edges instead of the smoothed signal.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Fade Amount
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the crossfade amount between the filtered signal and the fade color target. At maximum, the output is the fully filtered signal with no fade applied. At minimum, the output is the constant fade color (black or white for Y, neutral for U/V). Intermediate positions blend the two, creating a partially transparent overlay of the filtered image on a solid background. This is particularly effective with edge-extracted signals — a partial fade lets edges float as translucent traces over a colored field.





---

## Guided Exercises

These exercises build from simple single-channel blur to complex multi-topology filtering with fade effects. Each one introduces a new dimension of the program's filtering architecture.

### Exercise 1: Soft Focus Portrait

<BeforeAfterSlider
  sources={[
    { label: "House", before: gauze_source1_house, after: gauze_ex1_s1 },
    { label: "Dog", before: gauze_source2_dog, after: gauze_ex1_s2 },
    { label: "Turtle", before: gauze_source3_turtle, after: gauze_ex1_s3 },
    { label: "Pattern", before: gauze_source4_pattern, after: gauze_ex1_s4 },
    { label: "Woman", before: gauze_source5_woman, after: gauze_ex1_s5 },
    { label: "Berries", before: gauze_source6_berries, after: gauze_ex1_s6 },
  ]}
/>
*Soft Focus Portrait — simulated result across source images.*
**Source**: A talking-head or portrait shot with skin tones and fine texture detail (hair, fabric).

**What You'll Create**: Create a soft-focus diffusion effect by selectively blurring chrominance while preserving luminance edges.

1. Start with all controls at default (cutoffs centered, LP mode, no fade).
2. Lower UH Cutoff and VH Cutoff to approximately one-quarter. Watch the color information blur while luminance stays sharp.
3. Gently lower YH Cutoff to add a subtle luminance softening without destroying edge detail.
4. Leave all vertical cutoffs at center (no second-stage filtering).
5. Toggle Bypass to compare the soft result with the original.

**Key concepts**: Chroma blur with luma preservation, IIR low-pass filtering, independent channel control

---

### Exercise 2: Luminance Edge Extraction

<BeforeAfterSlider
  sources={[
    { label: "House", before: gauze_source1_house, after: gauze_ex2_s1 },
    { label: "Dog", before: gauze_source2_dog, after: gauze_ex2_s2 },
    { label: "Turtle", before: gauze_source3_turtle, after: gauze_ex2_s3 },
    { label: "Pattern", before: gauze_source4_pattern, after: gauze_ex2_s4 },
    { label: "Woman", before: gauze_source5_woman, after: gauze_ex2_s5 },
    { label: "Berries", before: gauze_source6_berries, after: gauze_ex2_s6 },
  ]}
/>
*Luminance Edge Extraction — simulated result across source images.*
**Source**: High-contrast footage with strong geometric shapes — architecture, signage, or test patterns.

**What You'll Create**: Extract luminance edges and fade them against a dark background to create a wireframe-like image.

1. Set Y Mode to High Pass. The image immediately shows only horizontal Y edges.
2. Lower YH Cutoff to approximately one-third. The edge lines become bolder as the filter removes more low-frequency content.
3. Turn YV Cutoff counter-clockwise from center to engage vertical high-pass — this adds vertical edge extraction, completing the full edge map.
4. Keep U Mode and V Mode on Low Pass, and reduce UH/VH Cutoff to blur color.
5. Lower the Fade Amount fader to approximately 50%. The edges now float on a dark background.
6. Set Fade Color to White and observe how the same edges now appear as dark traces on a bright field.

**Key concepts**: High-pass filtering as spatial differentiation, HP→HP topology for two-axis edge extraction, fade as background control

---

### Exercise 3: Bandpass Color Isolation

<BeforeAfterSlider
  sources={[
    { label: "House", before: gauze_source1_house, after: gauze_ex3_s1 },
    { label: "Dog", before: gauze_source2_dog, after: gauze_ex3_s2 },
    { label: "Turtle", before: gauze_source3_turtle, after: gauze_ex3_s3 },
    { label: "Pattern", before: gauze_source4_pattern, after: gauze_ex3_s4 },
    { label: "Woman", before: gauze_source5_woman, after: gauze_ex3_s5 },
    { label: "Berries", before: gauze_source6_berries, after: gauze_ex3_s6 },
  ]}
/>
*Bandpass Color Isolation — simulated result across source images.*
**Source**: Colorful footage with both broad gradients and fine texture — nature scenes, paintings, or color bars.

**What You'll Create**: Use cascaded LP→HP filtering to create a bandpass response that isolates mid-frequency color structure while rejecting both broad gradients and fine noise.

1. Set all three Mode toggles to Low Pass.
2. Lower all three horizontal cutoffs (YH, UH, VH) to approximately the first quarter. This smooths the signal broadly.
3. Turn all three vertical cutoffs counter-clockwise from center to engage vertical high-pass with moderate strength. The vertical stage now extracts edges from the already-smoothed horizontal output — this is a bandpass response.
4. Observe how mid-frequency structure (medium-sized shapes, soft edges) survives while both fine texture and broad gradients are rejected.
5. Experiment with different cutoff ratios between the horizontal and vertical stages to shift the center frequency of the bandpass.
6. Apply a moderate fade toward black to float the bandpass-filtered structure on a dark field.

**Key concepts**: Cascaded LP→HP creates bandpass response, cutoff ratio determines center frequency, per-channel bandpass allows selective color structure extraction

---


## Tips

- **High-pass + fade = wireframe**: Extracting edges with HP mode and then fading toward black creates a wireframe aesthetic. Fade toward white for an etched or embossed look.
- **Bandpass with LP→HP**: Set the horizontal stage to low-pass (smooth) and the vertical stage to high-pass (extract edges). The vertical stage extracts edges from the *smoothed* signal, isolating mid-frequency structure. Adjust the ratio of cutoffs to shift the center frequency.
- **Per-channel topology mixing**: You can run Y in HP→HP (edge extraction) while running U and V in LP→LP (heavy blur). The result is sharp luminance edges with soft, diffused color halos.
- **Fade interacts with level**: When high-pass filtering, the signal swings around zero (or 512 in unsigned space). Fading toward black pulls these edge traces toward darkness. Fading toward white lifts them. Use Fade Color and Fade Amount together to control the "pedestal" level of edge-extracted outputs.
- **Bypass for reference**: Use the Bypass toggle frequently to compare your filtered result against the original. The delay-matched bypass ensures no timing shift.

---

## Glossary

| Term | Definition |
|------|------------|
| **Bandpass Filter** | A filter that passes a band of spatial frequencies while rejecting both lower and higher frequencies; created by cascading a low-pass and a high-pass stage. |
| **Bipolar Control** | A knob where the center position is neutral, with opposite effects on either side of center. |
| **Cascaded Filter** | Two or more filter stages connected in series, where the output of one feeds the input of the next, producing a steeper overall frequency response. |
| **Cutoff Frequency** | The frequency at which a filter begins to attenuate the signal; controlled by the knob position. |
| **High-Pass Filter (HPF)** | A filter that removes low-frequency (smooth) content and passes high-frequency (edge/texture) content. Output = input − low-pass output. |
| **IIR (Infinite Impulse Response)** | A filter whose output depends on both the current input and its own previous output (state), creating a recursive smoothing or sharpening effect. |
| **Low-Pass Filter (LPF)** | A filter that passes low-frequency (smooth) content and attenuates high-frequency (edge/texture) content. |
| **Sigma-Delta Dithering** | A technique that averages between adjacent quantization levels over time by accumulating a fractional error, producing smoother parameter control without visible stepping. |
| **Spatial Filtering** | Processing that operates on the spatial dimensions (horizontal and vertical) of an image rather than on time or color space. |

---
