---
draft: false
sidebar_position: 341
slug: /instruments/videomancer/yuv_phaser
title: "YUV Phaser"
image: /img/instruments/videomancer/yuv_phaser/yuv_phaser_hero_s1.png
description: "YUV Phaser applies independent horizontal displacement to each of the three YUV color channels."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import yuv_phaser_control_panel from '/img/instruments/videomancer/yuv_phaser/yuv_phaser_control_panel.png';
import yuv_phaser_source1_sunset from '/img/instruments/videomancer/yuv_phaser/yuv_phaser_source1_sunset.png';
import yuv_phaser_source2_field from '/img/instruments/videomancer/yuv_phaser/yuv_phaser_source2_field.png';
import yuv_phaser_source2_fruit from '/img/instruments/videomancer/yuv_phaser/yuv_phaser_source2_fruit.png';
import yuv_phaser_source3_collage from '/img/instruments/videomancer/yuv_phaser/yuv_phaser_source3_collage.png';
import yuv_phaser_source3_turtle from '/img/instruments/videomancer/yuv_phaser/yuv_phaser_source3_turtle.png';
import yuv_phaser_source4_pattern from '/img/instruments/videomancer/yuv_phaser/yuv_phaser_source4_pattern.png';
import yuv_phaser_source5_woman from '/img/instruments/videomancer/yuv_phaser/yuv_phaser_source5_woman.png';
import yuv_phaser_source6_paint from '/img/instruments/videomancer/yuv_phaser/yuv_phaser_source6_paint.png';
import yuv_phaser_hero_s1 from '/img/instruments/videomancer/yuv_phaser/yuv_phaser_hero_s1.png';
import yuv_phaser_hero_s2 from '/img/instruments/videomancer/yuv_phaser/yuv_phaser_hero_s2.png';
import yuv_phaser_hero_s3 from '/img/instruments/videomancer/yuv_phaser/yuv_phaser_hero_s3.png';
import yuv_phaser_hero_s4 from '/img/instruments/videomancer/yuv_phaser/yuv_phaser_hero_s4.png';
import yuv_phaser_hero_s5 from '/img/instruments/videomancer/yuv_phaser/yuv_phaser_hero_s5.png';
import yuv_phaser_hero_s6 from '/img/instruments/videomancer/yuv_phaser/yuv_phaser_hero_s6.png';
import yuv_phaser_ex1_s1 from '/img/instruments/videomancer/yuv_phaser/yuv_phaser_ex1_s1.png';
import yuv_phaser_ex1_s2 from '/img/instruments/videomancer/yuv_phaser/yuv_phaser_ex1_s2.png';
import yuv_phaser_ex1_s3 from '/img/instruments/videomancer/yuv_phaser/yuv_phaser_ex1_s3.png';
import yuv_phaser_ex1_s4 from '/img/instruments/videomancer/yuv_phaser/yuv_phaser_ex1_s4.png';
import yuv_phaser_ex1_s5 from '/img/instruments/videomancer/yuv_phaser/yuv_phaser_ex1_s5.png';
import yuv_phaser_ex1_s6 from '/img/instruments/videomancer/yuv_phaser/yuv_phaser_ex1_s6.png';
import yuv_phaser_ex2_s1 from '/img/instruments/videomancer/yuv_phaser/yuv_phaser_ex2_s1.png';
import yuv_phaser_ex2_s2 from '/img/instruments/videomancer/yuv_phaser/yuv_phaser_ex2_s2.png';
import yuv_phaser_ex2_s3 from '/img/instruments/videomancer/yuv_phaser/yuv_phaser_ex2_s3.png';
import yuv_phaser_ex2_s4 from '/img/instruments/videomancer/yuv_phaser/yuv_phaser_ex2_s4.png';
import yuv_phaser_ex2_s5 from '/img/instruments/videomancer/yuv_phaser/yuv_phaser_ex2_s5.png';
import yuv_phaser_ex2_s6 from '/img/instruments/videomancer/yuv_phaser/yuv_phaser_ex2_s6.png';
import yuv_phaser_ex3_s1 from '/img/instruments/videomancer/yuv_phaser/yuv_phaser_ex3_s1.png';
import yuv_phaser_ex3_s2 from '/img/instruments/videomancer/yuv_phaser/yuv_phaser_ex3_s2.png';
import yuv_phaser_ex3_s3 from '/img/instruments/videomancer/yuv_phaser/yuv_phaser_ex3_s3.png';
import yuv_phaser_ex3_s4 from '/img/instruments/videomancer/yuv_phaser/yuv_phaser_ex3_s4.png';
import yuv_phaser_ex3_s5 from '/img/instruments/videomancer/yuv_phaser/yuv_phaser_ex3_s5.png';
import yuv_phaser_ex3_s6 from '/img/instruments/videomancer/yuv_phaser/yuv_phaser_ex3_s6.png';

# YUV Phaser

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: yuv_phaser_source1_sunset, after: yuv_phaser_hero_s1 },
    { label: "Field", before: yuv_phaser_source2_field, after: yuv_phaser_hero_s2 },
    { label: "Fruit", before: yuv_phaser_source2_fruit, after: yuv_phaser_hero_s3 },
    { label: "Collage", before: yuv_phaser_source3_collage, after: yuv_phaser_hero_s4 },
    { label: "Turtle", before: yuv_phaser_source3_turtle, after: yuv_phaser_hero_s5 },
    { label: "Pattern", before: yuv_phaser_source4_pattern, after: yuv_phaser_hero_s6 },
    { label: "Woman", before: yuv_phaser_source5_woman, after: undefined },
    { label: "Paint", before: yuv_phaser_source6_paint, after: undefined },
  ]}
/>
*YUV Phaser displacing a studio portrait through independent per-channel horizontal delays, splitting luminance and chrominance into staggered echoes across the scan line.*

---

## Overview

YUV Phaser applies independent horizontal displacement to each of the three YUV color channels. Each channel passes through its own BRAM-based delay line, where the read position is determined by a base phase offset plus a data-dependent displacement component that modulates the delay according to the pixel's own value. Because Y, U, and V can be shifted by different amounts and in different directions, a single input image can be split into spatially separated color layers — luminance sliding away from chrominance, blue diverging from red, or all three channels converging and diverging based on their own content.

The name reflects the tool's fundamental operation: **phase shifting** each color channel horizontally by a controllable number of pixel positions. At small phase values, the effect is a subtle RGB fringing similar to chromatic aberration in cheap optics. At large values, the three channels separate visibly into distinct copies of the image, offset across the scanline. Adding displacement gain multiplies the delay by each pixel's brightness, creating a warped, content-dependent spatial distortion where bright areas push farther than dark areas — or vice versa when the channel is flipped.

At zero Phase and zero Displace on all channels, YUV Phaser passes the input unchanged. With only the Phase controls active, the effect is a clean spatial offset — a fixed horizontal shift per channel. Engaging the Displace controls adds a nonlinear, image-dependent warp that creates flowing, organic spatial distortions across the frame.

---

## Background

### Horizontal Displacement and Scan-Line Delay

In raster video, each scan line is drawn pixel-by-pixel from left to right. A **horizontal delay** shifts pixels along this scan direction by storing them in a buffer and reading them back at a later position. The effect is equivalent to sliding the image sideways — a 100-pixel delay shifts the entire picture 100 pixels to the right. In analog video systems, horizontal displacement occurred naturally when timing circuits drifted, producing the characteristic "skewing" visible on misadjusted monitors. YUV Phaser recreates this effect digitally using BRAM-based delay lines (variable_delay_u), each holding up to 2048 10-bit pixel values.

### Data-Dependent Modulation

The Displace controls add a multiplicative component to each channel's delay: `total_delay = phase + (pixel_value × displace_gain) >> 10`. This means the delay is no longer uniform across the scan line — bright pixels are pushed farther than dark ones (or the reverse when the channel is inverted). The result is a spatially varying warp where regions of consistent brightness shift together, creating a flowing, elastic distortion. This technique is closely related to **displacement mapping** in computer graphics, where a texture's brightness values drive the spatial offset of another surface. Here, the video itself is both the source and the displacement map.

### Per-Channel Color Separation

Because each YUV channel has its own independent delay line, YUV Phaser can separate the color components of a video signal in space. This is analogous to **chromatic aberration** in optics, where different wavelengths of light are refracted by different amounts through a lens, causing color fringes at high-contrast edges. In YUV space, separating U and V while leaving Y centered creates blue-red fringing without disturbing the luminance structure of the image. Separating Y while leaving U and V centered produces a grayscale ghost offset from the color content. The three Phase and three Displace controls give six independent axes of color-spatial manipulation.

### Channel Inversion as Phase Reversal

The Y Flip, U Flip, and V Flip toggles apply a bitwise NOT to the respective channel before it enters the delay line. For the luminance channel, this inverts the image tonality — white becomes black and vice versa. For the chrominance channels, inversion swaps color polarities — blues become oranges, reds become cyans. When combined with displacement, channel inversion also reverses the Displace modulation direction: since the pixel values driving the displacement are inverted, bright areas that would normally receive maximum delay now receive minimum delay, and vice versa.

### Fade-to-Color as Creative Attenuation

The Fade Amount fader crossfades each channel between the displaced signal and a fixed reference value. The Fade Color toggle selects whether the Y channel fades toward black (0) or white (1023), while U and V always fade toward neutral gray (512). At full Fade Amount, the displaced signal is fully present. As the fader is reduced, the output progressively bleeds to the fade color. At zero, the output is a solid field of the selected fade color regardless of the input or displacement settings. This creates a dissolve into or out of the displaced effect, or serves as a way to reduce the intensity of extreme displacement settings without changing the Phase or Displace controls.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
|
+-- Per Channel (Y, U, V independently) ----------------------------
|   |
|   +- 1. Channel Inversion        (bitwise NOT via Flip toggles)
|   +- 1. Delay Computation         (phase + pixel*displace >> 10)
|   +- 2-3. Variable Delay Line     (BRAM, 2048 samples, 2 clk)
|   +- 4-7. Interpolator            (fade to color, 4 clk)
|   |         a = fade target (Y: 0|1023, U/V: 512)
|   |         b = delayed channel
|   |         t = Fade Amount
|
+-- Sync Signals ---------------------------------------------------
|   +-- 7-clock delay pipeline (hsync, vsync, field, bypass data)
|
+-- Bypass ---------------------------------------------------------
    +-- Select original or processed signal via Switch 11
```

The processing architecture is simple and parallel: all three channels receive identical treatment through independent hardware instances, differing only in their parameter values and fade targets. The delay lines are BRAM-based with a depth of 2048 samples, meaning the maximum displacement is slightly over one full scan line at SD resolution. The delay computation combines two terms — a constant phase offset and a content-dependent displacement — in a single clock cycle using a 10×10 bit multiply and shift. The interpolator fade stage operates identically across all three channels but uses different "a" inputs: Y fades toward black (0) or white (1023) depending on the Fade Color toggle, while U and V always fade toward neutral chroma (512), ensuring the fade-to-color target is always a valid colorimetric value.

---

## Parameter Reference

<img src={yuv_phaser_control_panel} alt="Videomancer front panel with YUV Phaser loaded"/>
*Videomancer's front panel with YUV Phaser active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Y Phase
| Property | Value |
|----------|-------|
| Range | 0.0 – 1023.0 |
| Default | 0.0 |

Controls the base horizontal displacement of the luminance (Y) channel in pixels. At 0, the Y channel is not shifted. Increasing this value delays the luminance signal horizontally, sliding it to the right relative to U and V. At maximum (1023), the luminance image is offset by approximately 1023 pixels — effectively pushing it nearly a full scan line. When used alone (Y Displace at 0), Y Phase creates a clean, uniform luminance shift. Combined with non-zero Y Displace, the phase offset provides a starting point around which the data-dependent displacement varies.

---

#### Knob 2 — U Phase
| Property | Value |
|----------|-------|
| Range | 0.0 – 1023.0 |
| Default | 0.0 |

Controls the base horizontal displacement of the blue-difference chrominance (U) channel. Operates identically to Y Phase but affects only the U channel. Offsetting U while leaving Y and V at zero creates a blue-yellow fringing effect at high-contrast edges, because the blue component of the image slides away from the luminance and red-difference components. Small U Phase values (under 50) produce subtle chromatic aberration; large values create obvious color separation.

---

#### Knob 3 — V Phase
| Property | Value |
|----------|-------|
| Range | 0.0 – 1023.0 |
| Default | 0.0 |

Controls the base horizontal displacement of the red-difference chrominance (V) channel. Like the other Phase controls, this shifts a single color channel horizontally. Offsetting V while leaving Y and U centered produces red-cyan fringing. When both U Phase and V Phase are active but unequal, the two chrominance components separate from each other as well as from luminance, creating a three-layer chromatic split where each color layer occupies a different horizontal position.

---

#### Knob 4 — Y Displace
| Property | Value |
|----------|-------|
| Range | 0.0% – 200.0% |
| Default | 0.0% |
| Suffix | % |

Adds a data-dependent component to the Y channel's displacement. At 0%, only the base Y Phase offset is used and the delay is uniform across the line. As Y Displace increases, each pixel's Y value is multiplied by the displace gain and added to the base phase, creating a spatially varying delay: bright pixels are pushed farther to the right, dark pixels remain closer to their original position. At maximum (200%), the displacement modulation can add up to 1023 additional pixels of delay on top of the phase offset. The result is a flowing, luminance-driven warp where bright regions stretch away from dark regions.

---

#### Knob 5 — U Displace
| Property | Value |
|----------|-------|
| Range | 0.0% – 200.0% |
| Default | 0.0% |
| Suffix | % |

Adds a data-dependent displacement component to the U channel, operating identically to Y Displace but modulated by U pixel values rather than Y. Because U represents the blue-yellow axis of chroma information, the displacement follows the chrominance contours of the image: regions with strong blue content shift differently from neutral or yellow regions. This creates displacement patterns that are driven by color rather than brightness, producing distinctly different warp shapes than Y Displace.

---

#### Knob 6 — V Displace
| Property | Value |
|----------|-------|
| Range | 0.0% – 200.0% |
| Default | 0.0% |
| Suffix | % |

Adds a data-dependent displacement component to the V channel. Like U Displace, this modulates the V channel's delay according to its own pixel values. With U Displace and V Displace set to different values, the two chrominance channels warp in different directions and by different amounts, creating complex color separation patterns that evolve across the frame as the chroma content changes. Setting equal values on all three Displace controls produces a uniform, brightness-driven warp across all channels — the image distorts as a whole rather than splitting into color layers.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Y Flip** | Off | On |
| **8 — U Flip** | Off | On |
| **9 — V Flip** | Off | On |
| **10 — Fade Color** | Black | White |
| **11 — Bypass** | Off | On |

Switches 7-11 control five binary settings organized into two groups. The first three switches (Y Flip, U Flip, V Flip) independently invert each color channel before it enters the delay line, which both tonally inverts that channel and reverses the direction of its displacement modulation. Switches 10 and 11 control fade-to-color polarity and processing bypass, respectively. The Flip switches interact with Displace in an important way: because the pixel values driving the displacement are inverted by the flip, the direction of the data-dependent warp also reverses.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Fade Amount
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the overall intensity of the processed output via a fade-to-color crossfade. At 100% (default), the fully displaced and optionally inverted signal is output without attenuation. As Fade Amount is reduced, each channel crossfades linearly toward its fade target: Y toward black or white (selected by Fade Color), and U/V toward neutral 512. At 0%, the output is entirely the fade color — luminance at 0 or 1023, chrominance at 512 — regardless of input or displacement settings. Intermediate values produce a translucent version of the displaced effect, useful for blending extreme displacement settings into a composition without eliminating them entirely.





---

## Guided Exercises

These exercises explore YUV Phaser's displacement capabilities from simple phase offsets through complex data-dependent warping, each building on the channel-separation principles of the previous.

### Exercise 1: Chromatic Aberration

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: yuv_phaser_source1_sunset, after: yuv_phaser_ex1_s1 },
    { label: "Field", before: yuv_phaser_source2_field, after: yuv_phaser_ex1_s2 },
    { label: "Fruit", before: yuv_phaser_source2_fruit, after: yuv_phaser_ex1_s3 },
    { label: "Collage", before: yuv_phaser_source3_collage, after: yuv_phaser_ex1_s4 },
    { label: "Turtle", before: yuv_phaser_source3_turtle, after: yuv_phaser_ex1_s5 },
    { label: "Pattern", before: yuv_phaser_source4_pattern, after: yuv_phaser_ex1_s6 },
    { label: "Woman", before: yuv_phaser_source5_woman, after: undefined },
    { label: "Paint", before: yuv_phaser_source6_paint, after: undefined },
  ]}
/>
*Chromatic Aberration — simulated result across source images.*
**Source**: A high-contrast source with sharp edges — text on a light background, architectural footage, or a test pattern with fine lines.

1. **Default start**: Begin with all controls zeroed. The output should match the input perfectly.
2. **Offset U**: Slowly increase U Phase to about 50. Watch as a blue-yellow fringe appears at every vertical contrast edge. The luminance structure remains sharp, but the color bleeds horizontally.
3. **Offset V**: Now increase V Phase to about 50. Red-cyan fringes appear in addition to the blue-yellow ones. At sharp edges, you should see a rainbow progression of color fringes.
4. **Diverge U and V**: Set U Phase higher than V Phase (e.g., 80 vs. 30). The blue and red fringes separate by different amounts, creating asymmetric color smearing.
5. **Increase Y Phase**: Add about 30 to Y Phase. Now all three layers are offset from each other — the image breaks into three distinct spatial copies, each carrying one YUV component.
6. **A/B compare**: Toggle Bypass to compare the displaced output against the clean original. Notice how the luminance structure survives even heavy chrominance displacement.

**Key concepts**: Color fringing from differential channel delay, chrominance-luminance separation, the visual hierarchy (human vision prioritizes luminance sharpness over chrominance alignment)

---

### Exercise 2: Data-Dependent Warp

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: yuv_phaser_source1_sunset, after: yuv_phaser_ex2_s1 },
    { label: "Field", before: yuv_phaser_source2_field, after: yuv_phaser_ex2_s2 },
    { label: "Fruit", before: yuv_phaser_source2_fruit, after: yuv_phaser_ex2_s3 },
    { label: "Collage", before: yuv_phaser_source3_collage, after: yuv_phaser_ex2_s4 },
    { label: "Turtle", before: yuv_phaser_source3_turtle, after: yuv_phaser_ex2_s5 },
    { label: "Pattern", before: yuv_phaser_source4_pattern, after: yuv_phaser_ex2_s6 },
    { label: "Woman", before: yuv_phaser_source5_woman, after: undefined },
    { label: "Paint", before: yuv_phaser_source6_paint, after: undefined },
  ]}
/>
*Data-Dependent Warp — simulated result across source images.*
**Source**: A source with strong brightness variation — a spotlight on a dark stage, a face lit from one side, or any footage with clear bright and dark regions.

1. **Phase only**: Set Y Phase to about 100 with Displace at 0%. Notice the uniform shift — every pixel moves the same amount.
2. **Add Displace**: Slowly increase Y Displace. Bright regions begin to stretch farther to the right while dark regions stay closer to their original position. The image develops a flowing, elastic quality.
3. **Full Displace**: Push Y Displace to about 100%. The warp becomes dramatic — bright areas smear far across the line while dark areas barely move. The boundary between bright and dark creates a shearing distortion.
4. **Flip interaction**: Enable Y Flip. The brightness values are inverted before displacement, so now dark regions in the original are pushed farthest (they are bright after inversion). Compare with Y Flip off to see how the warp direction reverses.
5. **Multi-channel warp**: Add U Displace and V Displace at different values (e.g., U at 50%, V at 100%). Each color channel now warps independently based on its own content, creating complex chromatic shearing.
6. **Modulation feedback**: Route the output back to the input. Each pass applies another round of data-dependent displacement, creating increasingly abstract flowing distortions.

**Key concepts**: Displacement mapping using the video itself, brightness-to-position modulation, interaction between channel inversion and displacement direction, compounding nonlinear distortion through feedback

---

### Exercise 3: Inverted Channel Displacement with Fade

<BeforeAfterSlider
  sources={[
    { label: "Sunset", before: yuv_phaser_source1_sunset, after: yuv_phaser_ex3_s1 },
    { label: "Field", before: yuv_phaser_source2_field, after: yuv_phaser_ex3_s2 },
    { label: "Fruit", before: yuv_phaser_source2_fruit, after: yuv_phaser_ex3_s3 },
    { label: "Collage", before: yuv_phaser_source3_collage, after: yuv_phaser_ex3_s4 },
    { label: "Turtle", before: yuv_phaser_source3_turtle, after: yuv_phaser_ex3_s5 },
    { label: "Pattern", before: yuv_phaser_source4_pattern, after: yuv_phaser_ex3_s6 },
    { label: "Woman", before: yuv_phaser_source5_woman, after: undefined },
    { label: "Paint", before: yuv_phaser_source6_paint, after: undefined },
  ]}
/>
*Inverted Channel Displacement with Fade — simulated result across source images.*
**Source**: Any colorful source — nature footage, music performance, or abstract color patterns.

1. **Setup displacement**: Set all three Phase controls to different values (Y=0, U=100, V=200) and all three Displace controls to moderate values (about 40-60%).
2. **Enable U Flip and V Flip**: The chrominance channels invert, swapping the color palette of the offset chrominance layers. The displacement direction for U and V also reverses.
3. **Observe the result**: The output should show the luminance layer in its original position with two color-inverted chrominance layers offset to different positions, each warped according to its own inverted content.
4. **Add Y Flip**: Now all three channels are inverted. The entire image becomes a negative — but each channel is offset and warped differently, creating a surreal color separation that does not exist in normal negative processing.
5. **Fade control**: Reduce Fade Amount to about 50%. The displaced layers begin to dissolve toward the fade color, creating a translucent, ghostly version of the effect.
6. **Fade Color toggle**: Switch Fade Color to White. The dissolution target changes from black to white, brightening the fade-out effect. At about 25% Fade Amount, only hints of the displaced channels remain against the bright field.
7. **Mix and match**: Restore Fade Amount to about 75% and experiment with different combinations of Flip toggles and Fade Color to find compositions where the remaining displaced channels create interesting patterns against the partially faded background.

**Key concepts**: Channel inversion reverses displacement modulation, independent chrominance manipulation in YUV space, fade-to-color as creative dissolve, the interaction between inversion, displacement, and fade

---


## Tips

- **Phase for framing, Displace for texture**: Use the Phase controls to set a fixed offset for color separation, then add Displace for image-dependent warping on top. The two parameters serve different creative purposes and combine multiplicatively.
- **Small U+V Phase for optical simulation**: Offsetting U and V by 10-30 pixels while leaving Y at 0 creates convincing chromatic aberration that mimics cheap lenses. This is one of the most immediately useful effects.
- **Flip reverses the warp**: When Displace is active, enabling Flip doesn't just invert the color — it reverses which parts of the image are pushed farthest. Use this to change the "direction" of the warp without changing the Displace gain.
- **Equal Displace values preserve color alignment**: Setting all three Displace controls to the same value warps the entire image uniformly without creating color separation. Vary them independently to create chromatic distortion.
- **Fade as an intensity control**: Rather than reducing Phase or Displace values to soften the effect, use Fade Amount to blend the displaced output toward a neutral color. This preserves the spatial character of the displacement while reducing its visual intensity.
- **Feedback creates flowing abstraction**: Routing the output back to the input compounds the displacement on each pass. Start with moderate Phase and low Displace — feedback multiplies the effect rapidly.
- **Wrap-around is a feature**: At maximum Phase + Displace, the delay address wraps through the buffer, creating scan-line echo effects where content from earlier in the line reappears later. Exploit this for repeating pattern effects.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; dedicated memory blocks on the iCE40 FPGA, used here for the 2048-sample delay lines. |
| **Chromatic Aberration** | An optical phenomenon where different wavelengths of light are displaced differently by a lens, causing color fringes at edges. |
| **Displacement Mapping** | A technique where pixel values from one image control the spatial offset of another image. |
| **Fade-to-Color** | A crossfade between the processed signal and a fixed reference color, implemented via interpolators. |
| **Manhattan Distance** | Not used in YUV Phaser but related: a distance metric used in other programs for color matching. |
| **Phase** | A fixed horizontal delay offset applied uniformly across the scan line. |
| **Scan Line** | One horizontal row of pixels in a raster video signal, drawn from left to right. |
| **variable_delay_u** | A BRAM-based variable-depth delay line IP block provided by the Videomancer SDK. |
| **YUV** | A color encoding system separating luminance (Y) from chrominance (U blue-difference, V red-difference). |

---
