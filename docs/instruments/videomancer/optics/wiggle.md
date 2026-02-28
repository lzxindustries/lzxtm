---
draft: true
sidebar_position: 284
slug: /instruments/videomancer/wiggle
title: "Wiggle"
image: /img/instruments/videomancer/wiggle/wiggle_hero.png
---

import wiggle_before_after from '/img/instruments/videomancer/wiggle/wiggle_before_after.png';
import wiggle_control_panel from '/img/instruments/videomancer/wiggle/wiggle_control_panel.png';
import wiggle_exercise1_result from '/img/instruments/videomancer/wiggle/wiggle_exercise1_result.png';
import wiggle_exercise2_result from '/img/instruments/videomancer/wiggle/wiggle_exercise2_result.png';
import wiggle_exercise3_result from '/img/instruments/videomancer/wiggle/wiggle_exercise3_result.png';
import wiggle_hero from '/img/instruments/videomancer/wiggle/wiggle_hero.png';
import wiggle_source1_kodim15 from '/img/instruments/videomancer/wiggle/wiggle_source1_kodim15.png';
import wiggle_source2_kodim01 from '/img/instruments/videomancer/wiggle/wiggle_source2_kodim01.png';
import wiggle_source3_kodim01_bw from '/img/instruments/videomancer/wiggle/wiggle_source3_kodim01_bw.png';

# Wiggle

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={wiggle_hero} alt="Wiggle hero image"/>
*Autostereoscopic depth wobble: luminance-proportional displacement on alternating fields conjures illusory depth from flat video.*
<img src={wiggle_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Wiggle applied.*

---

## Overview

Wiggle displaces pixels horizontally by an amount proportional to their brightness. On even video fields bright areas shift left while dark areas shift right; on odd fields the displacement reverses. When the two views alternate at field rate—50 or 60 Hz—the eye fuses them into a stereoscopic depth cue, making bright subjects pop forward and darker backgrounds recede. The result recalls lenticular postcards and Victorian parlour stereo viewers, except the illusion emerges entirely from temporal modulation rather than physical optics.

The displacement is read from three parallel video line buffers (one per YUV channel) so every pixel can be repositioned independently along the scan direction. A shaping stage blends linear and exponential depth curves, allowing the artist to control how gradually depth tapers off. An IIR smoothing filter suppresses the jitter that would otherwise appear at hard luminance edges, and a threshold gate silences displacement below a configurable luma floor.

The name "Wiggle" references the convergence micro-oscillations the brain performs when judging binocular depth: the program automates a digital version of that tiny shake, producing a convincing z-axis motion from purely two-dimensional imagery.

---

## Background

### Autostereoscopy and Lenticular Imaging

Autostereoscopy creates depth perception without glasses by presenting different views to each eye. Lenticular printing achieves this with an array of cylindrical lenses laminated over interleaved strips; tilting the print swaps views. In video, temporal lenticularity can accomplish the same trick: alternating two slightly different images faster than the eye can follow fuses them into a single volumetric impression. Wiggle exploits this principle at field rate, where "slightly different" means horizontally shifted proportional to luminance.

### Displacement Mapping

Displacement mapping is a technique borrowed from 3D rendering and terrain modelling. A greyscale height field drives geometric deformation—bright pixels push outward, dark ones remain flush or recede. In the context of a 2D video scanline, the height field becomes a horizontal read-offset applied to the line buffer: rather than reading pixel N, the system reads pixel N ± Δ, where Δ derives from luma. Large displacements produce dramatic warps; small ones yield subtle shimmer.

### Depth Shaping Curves

A linear mapping from luminance to displacement gives uniform sensitivity across the tonal range, but perceptual depth response is not linear. By squaring the input before scaling, the exponential curve compresses low-luminance displacement and expands highlights, mimicking the way objects in the real world attenuate with distance squared. Wiggle's Depth Curve control morphs between these two responses, letting the artist tune how quickly depth falls off from bright to dark.

### Field-Rate Temporal Modulation

Interlaced video transmits even and odd scan lines on alternating fields at double the frame rate. Wiggle piggybacks on this mechanism: even fields apply positive displacement and odd fields apply negative, so the viewer sees a left-right oscillation at 50 or 60 Hz—well above flicker threshold but fast enough to trick binocular fusion. On progressive displays the effect manifests as a per-frame wiggle that creates a fluid, undulating depth plane.

### IIR Smoothing for Edge Anti-Jitter

Hard luminance transitions—text borders, window edges, silhouettes—produce abrupt displacement jumps that read as high-frequency noise rather than smooth depth. A first-order IIR low-pass filter applied to the displacement signal damps these transients, spreading the depth gradient over several pixels. At high smoothing values the displacement field becomes a gentle terrain; at zero it tracks every high-contrast edge exactly.


---

## Signal Flow

```
data_in ─┬──────────────────────────────────────────────── delay pipe ──► s_y_d, s_u_d, s_v_d
         │                                                                     │
         ├── luma ──► invert? ──► threshold ──► depth_curve ──► scale ──►      │
         │                                                       │             │
         │                               smoothing IIR ◄─────────┘             │
         │                                     │                               │
         │                            address_compute ──► rd_addr              │
         │                                                   │                 │
         ├── Y ─► video_line_buffer ─┬────────────────── compositor ──►        │
         ├── U ─► video_line_buffer ─┤                      │                  │
         └── V ─► video_line_buffer ─┘                 brightness ──►          │
                                                            │                  │
                                                  interpolator_u (Y) ──►──┐   │
                                                  interpolator_u (U) ──►──┤   │
                                                  interpolator_u (V) ──►──┤   │
                                                                          ▼   ▼
                                                                     bypass mux ──► data_out
```

The input luma drives an entire displacement side-chain—inversion, thresholding, curve shaping, and scale—before the resulting offset feeds an address computation that reads displaced pixels from the three line buffers. A separate delay pipe carries the original YUV data through the same number of clocks so the dry signal aligns perfectly with the wet displaced signal at the interpolator mix stage. The field-alternating sign flip in the address stage is the core mechanism that generates depth: positive displacement on one field and negative on the next creates the pseudo-stereo wobble.

Brightness gain is applied after the line-buffer read and before the mix, so it scales only the displaced signal. At unity (512) the effect brightness matches the input; above unity it intentionally overexposes displaced regions, which can reinforce the illusion that bright areas are closer.

---

## Parameter Reference

<img src={wiggle_control_panel} alt="Videomancer front panel with Wiggle loaded"/>
*Videomancer's front panel with Wiggle active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Depth Amt
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Depth Amt controls the maximum pixel displacement applied to bright areas. At zero the image passes through unaltered; at full scale the displacement can reach dozens of pixels, producing a dramatic warp. Moderate values (40–60 %) suit naturalistic depth illusions where subjects gently lift off the background. Extreme settings intentionally break the stereo metaphor and enter abstract warp territory, pulling luminance peaks into long smeared streaks.

---

#### Knob 2 — Osc Rate
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

Osc Rate sets the speed at which the displacement direction oscillates when Strobe mode is active. In the default field-alternating mode this control has no visible effect because parity is locked to the video field. When Strobe is enabled the oscillation phase accumulator increments by this amount each vertical sync, allowing the wobble frequency to range from a barely perceptible drift to rapid flutter. Faster oscillation rates create more aggressive depth pulsing.

---

#### Knob 3 — Depth Curve
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Depth Curve blends the displacement response between linear (fully CCW) and exponential (fully CW). Linear response gives uniform depth sensitivity across all brightness levels: a mid-grey pixel displaces half as far as peak white. Exponential response compresses displacement for mid-tones and expands it for highlights, concentrating the depth pop on the brightest elements while leaving shadows and mid-greys relatively flat. Intermediate settings provide a gentle roll-off that often looks most natural.

---

#### Knob 4 — Smooth
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Smooth applies an IIR low-pass filter to the per-pixel displacement offset before it enters the address computation. At minimum the displacement tracks the input luma exactly—every edge in the source produces a matching displacement step. Increasing Smooth averages the displacement across neighbouring pixels, softening jagged displacement edges and reducing the "tearing" artefact that appears at sharp contrast boundaries. At extreme values the displacement becomes a broad, slow-rolling wave that ignores fine detail.

---

#### Knob 5 — Threshold
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Threshold sets the minimum luma value that will produce any displacement at all. Pixels darker than the threshold contribute zero offset, effectively anchoring the dark end of the image. This is useful for isolating depth to bright subjects—foreground performers, light sources, text—while keeping the background perfectly still. Raising the threshold narrows the active depth window; lowering it allows even shadows to participate in the wobble.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Brightness scales the luma of displaced pixels after the line-buffer read and before the wet/dry mix. The default centre position (512) provides unity gain. Below centre, the displaced image darkens, making the depth effect more subtle; above centre it brightens, visually pushing displaced regions forward in the depth field. At maximum the effect intentionally clips highlights, creating a blown-out halo on the brightest areas.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Axis** | Horiz | Vert |
| **8 — Depth Src** | Luma | Chroma |
| **9 — Invert Depth** | Off | On |
| **10 — Strobe** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles configure the displacement engine's operating mode. Axis selects horizontal or vertical displacement geometry via a four-option selector with two functional extremes. Depth Src inverts the luminance-to-displacement mapping so dark areas push forward instead of bright. Invert Depth freezes the oscillation accumulator, locking the displacement to a fixed direction. Strobe switches from field-locked alternation to phase-accumulator-driven oscillation controlled by Osc Rate. Bypass disconnects the processing chain entirely.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Mix crossfades between the unprocessed dry input and the fully displaced wet output. At minimum only the dry signal passes; at maximum only the displaced, brightness-adjusted signal is heard. Intermediate positions blend the two, which can produce a ghostly double-exposure look as the displaced copy overlaps the undisplaced original. The mix is applied per-channel via three parallel interpolator_u instances.

---

## Guided Exercises

These exercises explore Wiggle's depth illusion from subtle naturalism to extreme warp, each building familiarity with the displacement chain and its controls.

### Exercise 1: Gentle Portrait Depth

<img src={wiggle_exercise1_result} alt="Gentle Portrait Depth result"/>
*Gentle Portrait Depth — simulated result across source images.*
**Source**: Feed a talking-head camera shot or portrait with a well-lit face against a darker background.

**Objective**: Create a subtle 3D pop that makes the face appear to float in front of the background.

1. Set Depth Amt to 30 % and Threshold to 25 % so only skin-tone highlights displace.
2. Push Depth Curve to 70 % for exponential roll-off that concentrates depth on the brightest facial highlights.
3. Raise Smooth to 60 % to eliminate the hard-edge jitter around hair and jawline.
4. Leave Brightness at 50 % for unity gain.
5. Slowly increase Mix from 0 to 80 % and notice how the face gradually lifts off the backdrop.
6. Toggle Depth Src between Luma and Chroma to see the concave/convex reversal.

**Key concepts**: Threshold isolates depth to bright subjects. Depth Curve's exponential response naturally maps to the way real-world depth-of-field focuses on highlights.

---

### Exercise 2: Abstract Warp Field

<img src={wiggle_exercise2_result} alt="Abstract Warp Field result"/>
*Abstract Warp Field — simulated result across source images.*
**Source**: Use a high-contrast graphic pattern—black-and-white stripes, a checkerboard, or bold typography.

**Objective**: Push displacement to extremes to create a liquid warp field where the pattern stretches and compresses rhythmically.

1. Max out Depth Amt to 100 %.
2. Set Threshold to 0 % so the entire tonal range participates.
3. Depth Curve at 50 % for a balanced response.
4. Smooth at 10 % to keep displacement sharp.
5. Enable Strobe and set Osc Rate to 35 % for a slow, deliberate oscillation.
6. Bring Mix to 100 %.
7. Watch the stripes breathe as the displacement reverses direction.

**Key concepts**: Large displacement on high-contrast material produces visible pixel stretching. Strobe mode decouples oscillation from field timing, allowing manual control of wobble speed.

---

### Exercise 3: Frozen Parallax Layer

<img src={wiggle_exercise3_result} alt="Frozen Parallax Layer result"/>
*Frozen Parallax Layer — simulated result across source images.*
**Source**: A landscape or cityscape with distinct foreground and background planes.

**Objective**: Create a static parallax offset—a fixed spatial shift between bright and dark regions—rather than a temporal wobble.

1. Set Depth Amt to 45 % for a moderate offset.
2. Enable Invert Depth (Freeze) to halt the oscillation phase.
3. Set Threshold to 15 % to anchor shadows.
4. Depth Curve at 80 % for strong exponential fall-off.
5. Smooth at 40 % for gentle edges.
6. Mix at 70 % to let some dry image show through for registration reference.
7. Compare with Bypass to see the static shift.

**Key concepts**: Freezing the oscillation removes the temporal wobble and produces a single-direction displacement—a parallax offset that separates brightness planes spatially rather than temporally.

---


## Tips

- **Start subtle**: 20–30 % Depth Amt with moderate Threshold creates convincing naturalistic depth on camera footage without obvious warping.
- **CRT viewing**: The autostereoscopic illusion is strongest on CRT displays where field alternation is a true temporal split; on LCDs with sample-and-hold the effect reads more as a shimmer.
- **Combine with Cascade**: Feed Wiggle's output into Cascade's echo chain to build recursive depth layers that compound the parallax.
- **Use Smooth for clean text**: High Smooth values prevent text edges from shattering into jagged displacement steps, keeping legibility while adding gentle undulation.
- **Threshold isolates performers**: On stage or studio footage, setting Threshold above the background brightness level restricts depth wobble to lit subjects.
- **Brightness for emphasis**: Push Brightness above 50 % to intentionally blow out displaced highlights—this creates a glowing halo effect on bright objects.
- **Freeze for static offsets**: Using Invert Depth (Freeze) disables the wobble entirely, turning Wiggle into a static luminance-driven displacement map useful for lenticular-style parallax frames.
- **Strobe slow roll**: Osc Rate below 10 % in Strobe mode creates a very slow, meditative depth breathing that works well for ambient installations.
