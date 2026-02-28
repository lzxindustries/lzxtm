---
draft: true
sidebar_position: 146
slug: /instruments/videomancer/lenticular
title: "Lenticular"
image: /img/instruments/videomancer/lenticular/lenticular_hero.png
---

import lenticular_before_after from '/img/instruments/videomancer/lenticular/lenticular_before_after.png';
import lenticular_control_panel from '/img/instruments/videomancer/lenticular/lenticular_control_panel.png';
import lenticular_exercise1_result from '/img/instruments/videomancer/lenticular/lenticular_exercise1_result.png';
import lenticular_exercise2_result from '/img/instruments/videomancer/lenticular/lenticular_exercise2_result.png';
import lenticular_exercise3_result from '/img/instruments/videomancer/lenticular/lenticular_exercise3_result.png';
import lenticular_hero from '/img/instruments/videomancer/lenticular/lenticular_hero.png';
import lenticular_source1_kodim01 from '/img/instruments/videomancer/lenticular/lenticular_source1_kodim01.png';
import lenticular_source2_kodim02 from '/img/instruments/videomancer/lenticular/lenticular_source2_kodim02.png';
import lenticular_source3_kodim01_bw from '/img/instruments/videomancer/lenticular/lenticular_source3_kodim01_bw.png';

# Lenticular

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={lenticular_hero} alt="Lenticular hero image"/>
*Lenticular dividing a portrait into alternating shifted stripes, creating a shimmering parallax depth effect reminiscent of holographic trading cards.*
<img src={lenticular_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Lenticular applied.*

---

## Overview

Lenticular prints are those plastic-ridged cards that seem to shift or animate when you tilt them. Under each tiny cylindrical lens, two or more images are interleaved in narrow strips. Tilt one way and you see image A; tilt the other and you see image B. The brain fuses the alternation into a sense of depth or motion, even though the card is perfectly flat.

Lenticular simulates this optical trick electronically. It divides the video frame into vertical (or horizontal) stripes and shows alternating views within each stripe — the current pixel in one stripe, a horizontally shifted copy in the next. A 64-sample shift register provides the delay source, so the "second view" is the same image displaced by a selectable number of pixels. The result is a synthetic parallax: objects appear to hover at different depths depending on how far left or right their shifted copy lands.

The effect ranges from subtle — narrow stripes with a small shift produce a gentle shimmer that suggests holographic film — to aggressive, where wide stripes and large shifts shatter the image into a venetian-blind mosaic of displaced fragments. A wiggle mode alternates the view selection on frame parity instead of stripe position, creating a temporal flicker that mimics the experience of physically rocking a lenticular card back and forth.

---

## Background

### Lenticular Printing

Lenticular technology dates to the 1940s, when inventor Victor Anderson patented a method for creating images with an illusion of depth using an array of cylindrical lenses bonded over a specially prepared print. Each lens acts as a tiny window that shows a different vertical slice of the underlying image depending on the viewing angle. By interlacing two or more perspectives beneath the lens sheet, the print can display flip effects (two distinct images), animation (a sequence of frames), and stereoscopic 3D (left-right eye parallax).

### Parallax and Stereopsis

Depth perception from binocular vision relies on parallax — the slight horizontal displacement between what each eye sees. Lenticular 3D prints exploit this by directing different images to each eye through the lens array. Lenticular the program creates a similar displacement digitally: alternating stripes show the image at two different horizontal offsets, and the viewer's brain can interpret the displacement as depth information, especially when the stripe width is small enough that individual stripes are hard to resolve.

### Shift Registers in Video Processing

The horizontal displacement is implemented with a 64-sample shift register — a chain of 64 storage slots that each hold one pixel's YUV values. Every clock cycle, each slot passes its contents to the next, and the newest pixel enters slot 0. By reading from a selectable tap (slot N), the circuit retrieves the pixel that was N positions to the left on the same scan line. This is a classic FPGA pattern for horizontal delay because it requires no BRAM — just flip-flops — and provides random access to any tap with no read latency.

### Line Buffers and Vertical Relationships

A video line buffer stores one complete scan line. By writing the current line's Y values and reading back the previous line's Y values at the same horizontal position, the circuit can compare or blend vertically adjacent lines. Lenticular uses this to optionally average the shifted view's luminance with the previous line's luminance on alternate stripes, adding a vertical smearing component to the parallax effect.

### Wiggle Mode

Real lenticular cards animate when you tilt them — the image flips back and forth between views. Wiggle mode recreates this temporal alternation digitally. Instead of selecting views based on stripe position (spatial interleaving), it selects based on frame parity (temporal interleaving). On even frames, the entire screen shows view A; on odd frames, view B. For a still-image simulator, the effect collapses to a single frame showing one view, but on live video the result is a rapid flicker between the original and shifted image.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Input Register + Shift Register Write ─────────────
│   ├─ Register input Y/U/V
│   ├─ Write pixel into 64-sample Y/U/V shift register
│   ├─ Compute stripe_shift (4/8/16/32/64 px from pot)
│   ├─ Compute shift_tap (0–63 from pot high bits)
│   └─ Line buffer write (current line Y for next-line read)
│
├── Stage 2: Stripe Selection ──────────────────────────────────
│   ├─ Vertical stripes: stripe_bit = h_count(stripe_shift)
│   ├─ Horizontal stripes: stripe_bit = v_count(stripe_shift)
│   ├─ Wiggle mode: use frame_count(0) instead of stripe_bit
│   ├─ Direction: optionally invert alt selection
│   └─ Fractional position within stripe (for transition)
│
├── Stage 3: Shift Register Tap + Line Buffer Read ─────────────
│   ├─ Read shifted pixel from SR at shift_tap index
│   └─ Line buffer previous-line Y data arrives
│
├── Stage 4: Source Select + Vertical Blend ────────────────────
│   ├─ Alt stripe → shifted pixel; Primary → current pixel
│   └─ If alt AND vert_shift > 16: average Y with prev-line Y
│
├── Stage 5: Depth Scaling ─────────────────────────────────────
│   ├─ depth ≤ 512: Y = (depth × selected_Y) >> 10
│   └─ depth > 512: Y = selected_Y (pass-through)
│
├── Stage 6: Output Compose + Clamp ────────────────────────────
│   └─ Final Y/U/V output
│
├── Interpolator (4 clk): Wet/dry mix ─────────────────────────
│   └─ lerp(dry, processed, mix_amount) per channel
│
└── Bypass Mux ─────────────────────────────────────────────────
    └─ Select original or processed signal
```

The shift register provides zero-latency random access to any of 64 preceding pixels on the same scan line, which is key to fast horizontal displacement without BRAM addressing overhead. The stripe selection logic uses a single bit of the position counter — the bit at the stripe_shift position — to determine odd/even stripe identity, making the stripe width always a power of two. The depth scaling stage applies a brightness attenuation to the selected view when the depth pot is in its lower half, creating a dimming effect that can suggest receding depth; when the pot is above midpoint, the view passes through at full brightness.

---

## Parameter Reference

<img src={lenticular_control_panel} alt="Videomancer front panel with Lenticular loaded"/>
*Videomancer's front panel with Lenticular active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Stripe W
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the stripe period — the width of each lenticular lens in pixels. The pot is quantized into five steps: values below 205 give 4-pixel stripes (very fine, nearly invisible interleaving), 205–409 give 8-pixel stripes, 410–613 give 16-pixel stripes, 614–818 give 32-pixel stripes, and above 818 give 64-pixel stripes (coarse, obvious venetian-blind-like bands). Smaller stripes produce a more convincing depth illusion because the eye cannot resolve individual bands; larger stripes create a graphic split-screen effect.

---

#### Knob 2 — Shift
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the horizontal pixel displacement — how far the alternate-stripe view is shifted from the current pixel. The pot's upper 6 bits select a tap index from 0 to 63 in the shift register, so the shift ranges from 0 pixels (no displacement, both views identical) to 63 pixels. Larger shifts create stronger parallax but also more visible duplication artifacts. Subtle shifts of 2–8 pixels produce a gentle holographic shimmer; shifts above 20 pixels fracture the image into obviously displaced slices.

---

#### Knob 3 — Views
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Labeled "Views" in the TOML interface but mapped to the transition crossfade width in the VHDL. In the current hardware implementation, the transition value is registered but not used in the stripe selection logic — the stripe boundary is always a hard cut. The pot value is captured for future firmware revisions that could implement soft crossfade zones between stripes.

---

#### Knob 4 — Angle
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Labeled "Angle" in the TOML interface but controls the vertical shift blend in the VHDL. When this pot is above a minimum threshold (register value > 16), alternate stripes blend their shifted Y value with the previous scan line's Y value from the line buffer, creating a vertical smearing component on alternate stripes. This adds a subtle vertical motion blur to the parallax effect. Below the threshold, no vertical blending occurs.

---

#### Knob 5 — Sharp
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Labeled "Sharp" in the TOML interface but controls the parallax depth scaling in the VHDL. When the pot is in its lower half (0–512), the selected stripe's luminance is multiplied by the pot value and right-shifted by 10 bits, attenuating the brightness. This creates a depth-fading effect where the alternate view appears dimmer, suggesting distance. When the pot is above midpoint, the view passes through at full brightness with no attenuation.

---

#### Knob 6 — Depth
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Not connected in the VHDL implementation. The register value is received but not mapped to any processing signal. The control is reserved for future use.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Mode** | Flip | Morph |
| **8 — Direction** | Vert | Horiz |
| **9 — Source** | Luma | Edge |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

Toggles 7, 8, and 9 each occupy a single bit in the toggle register despite having multi-value TOML labels. The TOML presents 4-option labels for Toggles 7 and 8, but the VHDL reads only 1 bit each, treating them as binary switches. Toggle 10 is declared in the TOML but not connected in the VHDL. Toggle 11 (Bypass) is at the standard bit 4 position.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry crossfade between the original input and the processed output. At 0% the output is entirely dry (unprocessed video). At 100% the output is entirely wet (the lenticular-processed image). Intermediate values blend the two, allowing the stripe interleaving to be subtly mixed in rather than applied at full strength.

---

## Guided Exercises

These exercises explore the lenticular effect from subtle depth shimmer to aggressive image fragmentation, building familiarity with stripe width, shift distance, and the various mode options.

### Exercise 1: Holographic Shimmer

<img src={lenticular_exercise1_result} alt="Holographic Shimmer result"/>
*Holographic Shimmer — simulated result across source images.*
**Source**: A portrait or close-up with a clear foreground subject and blurred background.

**Objective**: Create a subtle holographic shimmer that suggests depth without obvious stripe artifacts.

1. **Fine stripes**: Set Stripe W to about 15% (8-pixel stripes).
2. **Small shift**: Set Shift to about 10% (a few pixels of displacement).
3. **Vertical orientation**: Set Mode to Flip (toggle off).
4. **Interleave mode**: Set Direction to Vert (toggle off).
5. **Default direction**: Set Source to Luma (toggle off).
6. **Full depth**: Set Sharp to about 75% (above midpoint for full brightness).
7. **No vertical blend**: Set Angle to 0%.
8. **Mix fully wet**: Push Mix to 100%.
9. **Observe**: The foreground subject should have a slight double-vision shimmer while the background, being out of focus, shows a soft haze.
10. **Sweep shift**: Slowly increase Shift — watch the parallax grow from imperceptible to clearly visible.

**Key concepts**: Small stripes and small shifts create a near-invisible parallax, the brain interprets horizontal displacement as depth, fine stripes are harder to resolve perceptually

---

### Exercise 2: Venetian Blind Split

<img src={lenticular_exercise2_result} alt="Venetian Blind Split result"/>
*Venetian Blind Split — simulated result across source images.*
**Source**: Any high-contrast footage with horizontal and vertical detail.

**Objective**: Create an obvious stripe-based image split with large displacement.

1. **Wide stripes**: Set Stripe W to about 85% (64-pixel stripes).
2. **Large shift**: Set Shift to about 60% (roughly 40 pixels).
3. **Vertical stripes**: Keep Mode at Flip (toggle off).
4. **Observe**: The image splits into alternating bands — even stripes show the current view, odd stripes show a displaced copy. It looks like peering through a venetian blind where each slat shows a different perspective.
5. **Switch to horizontal**: Toggle Mode to on for horizontal stripes. The bands now run left to right — top and bottom halves show different views.
6. **Flip direction**: Toggle Source on to swap which stripes show which view.
7. **Depth dim**: Pull Sharp below 50% to dim the alternate stripes, making them recede visually.

**Key concepts**: Large stripes make the interleaving visible as a graphic split, horizontal vs vertical stripe orientation rotates the effect 90 degrees, direction toggle swaps which view is primary

---

### Exercise 3: Wiggle and Vertical Blur

<img src={lenticular_exercise3_result} alt="Wiggle and Vertical Blur result"/>
*Wiggle and Vertical Blur — simulated result across source images.*
**Source**: Animated content or a slowly moving camera feed.

**Objective**: Explore temporal wiggle mode and the vertical line-buffer blend.

1. **Medium stripes**: Set Stripe W to about 50% (16-pixel stripes).
2. **Moderate shift**: Set Shift to about 30%.
3. **Enable wiggle**: Toggle Direction on (wiggle mode).
4. **Observe on live video**: The entire frame alternates between original and shifted views on alternate fields. On a still image, only one view is visible.
5. **Add vertical blend**: Turn Angle to about 50%. On live video, alternate frames now blend the shifted Y with the previous line's Y, adding a vertical smear.
6. **Switch back to interleave**: Toggle Direction off. Now the vertical blend applies to the spatially interleaved stripes, creating a combined parallax + vertical-smear texture.
7. **Depth scaling**: Pull Sharp to about 25%. The alternate stripes dim, making the vertical-blend smear more apparent as a ghostly underlayer.

**Key concepts**: Wiggle mode creates temporal alternation mimicking physical card tilting, vertical blend adds line-buffer smearing to alternate views, depth scaling can dim alternate views for emphasis

---


## Tips

- **Stripe width controls the illusion**: Narrow stripes (4–8 pixels) produce the most convincing depth effect because the eye cannot resolve individual bands. Wide stripes (32–64 pixels) create an obvious split-image look.
- **Shift distance is in pixels, not percentage**: The Shift pot maps directly to the shift register tap index (0–63 pixels). Small values like 3–5 pixels create subtle parallax; above 20 it becomes an obvious displacement.
- **Views and Depth pots have limited effect**: Views (pot 3) is registered but unused — the stripe boundary is always hard. Depth (pot 6) is unconnected. Future firmware may activate these controls.
- **Wiggle mode needs live video**: On a still image, wiggle mode shows only one view (frame 0 is always even). Feed live or animated content to see the temporal flicker.
- **Vertical blend is an on/off threshold**: The Angle pot acts as a gate — above ~1.5% it enables a 50/50 average with the previous line on alt stripes. The pot value beyond the threshold does not change the blend ratio.
- **Direction swap mirrors depth**: Toggling Source on inverts which stripes show original vs. shifted views, effectively flipping the perceived depth direction — objects that popped out now recede.
- **TOML labels differ from VHDL function**: Pots 3–5 and toggles 7–9 have TOML labels that describe intended features (Views, Angle, Sharp, Mode, Direction, Source) but map to different VHDL signals (transition, vert_shift, depth, orient, wiggle, direction). Trust the pot behavior description, not the label name.
- **Feedback creates recursive parallax**: Routing the output back to the input produces an echoing lenticular effect where each pass adds another layer of horizontal displacement, building toward a kaleidoscopic fragmentation.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; dedicated FPGA memory tiles used for line buffers and large delay structures. |
| **Chroma** | The color information in a video signal, encoded as U and V components in YUV color space. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Interleave** | Spatially alternating between two views stripe-by-stripe within a single frame. |
| **Lenticular** | A printing technology using cylindrical lens arrays to create images with depth or animation effects. |
| **Line Buffer** | A memory that stores one complete scan line for comparison or mixing with adjacent lines. |
| **Luma** | The brightness component (Y) of a YUV video signal, representing perceived lightness. |
| **Parallax** | The apparent displacement of an object when viewed from different positions; the basis of stereoscopic depth perception. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Shift Register** | A chain of storage elements that passes data from one stage to the next on each clock cycle, providing selectable time delay. |
| **Stereopsis** | The brain's ability to perceive depth by comparing the slightly different images received by each eye. |
| **Wiggle** | Temporal alternation between views on successive frames, mimicking the effect of tilting a lenticular card. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |
