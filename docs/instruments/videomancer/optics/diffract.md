---
draft: true
sidebar_position: 81
slug: /instruments/videomancer/diffract
title: "Diffract"
image: /img/instruments/videomancer/diffract/diffract_hero_s1.png
description: "When white light passes through a diffraction grating — a surface scored with thousands of parallel slits — each wavelength bends at a slightly different angle."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import diffract_source1_car from '/img/instruments/videomancer/diffract/diffract_source1_car.png';
import diffract_source2_parrot from '/img/instruments/videomancer/diffract/diffract_source2_parrot.png';
import diffract_source3_clouds from '/img/instruments/videomancer/diffract/diffract_source3_clouds.png';
import diffract_source4_pattern from '/img/instruments/videomancer/diffract/diffract_source4_pattern.png';
import diffract_source5_girl from '/img/instruments/videomancer/diffract/diffract_source5_girl.png';
import diffract_source6_paint from '/img/instruments/videomancer/diffract/diffract_source6_paint.png';
import diffract_hero_s1 from '/img/instruments/videomancer/diffract/diffract_hero_s1.png';
import diffract_hero_s2 from '/img/instruments/videomancer/diffract/diffract_hero_s2.png';
import diffract_hero_s3 from '/img/instruments/videomancer/diffract/diffract_hero_s3.png';
import diffract_hero_s4 from '/img/instruments/videomancer/diffract/diffract_hero_s4.png';
import diffract_hero_s5 from '/img/instruments/videomancer/diffract/diffract_hero_s5.png';
import diffract_hero_s6 from '/img/instruments/videomancer/diffract/diffract_hero_s6.png';
import diffract_ex1_s1 from '/img/instruments/videomancer/diffract/diffract_ex1_s1.png';
import diffract_ex1_s2 from '/img/instruments/videomancer/diffract/diffract_ex1_s2.png';
import diffract_ex1_s3 from '/img/instruments/videomancer/diffract/diffract_ex1_s3.png';
import diffract_ex1_s4 from '/img/instruments/videomancer/diffract/diffract_ex1_s4.png';
import diffract_ex1_s5 from '/img/instruments/videomancer/diffract/diffract_ex1_s5.png';
import diffract_ex1_s6 from '/img/instruments/videomancer/diffract/diffract_ex1_s6.png';
import diffract_ex2_s1 from '/img/instruments/videomancer/diffract/diffract_ex2_s1.png';
import diffract_ex2_s2 from '/img/instruments/videomancer/diffract/diffract_ex2_s2.png';
import diffract_ex2_s3 from '/img/instruments/videomancer/diffract/diffract_ex2_s3.png';
import diffract_ex2_s4 from '/img/instruments/videomancer/diffract/diffract_ex2_s4.png';
import diffract_ex2_s5 from '/img/instruments/videomancer/diffract/diffract_ex2_s5.png';
import diffract_ex2_s6 from '/img/instruments/videomancer/diffract/diffract_ex2_s6.png';
import diffract_ex3_s1 from '/img/instruments/videomancer/diffract/diffract_ex3_s1.png';
import diffract_ex3_s2 from '/img/instruments/videomancer/diffract/diffract_ex3_s2.png';
import diffract_ex3_s3 from '/img/instruments/videomancer/diffract/diffract_ex3_s3.png';
import diffract_ex3_s4 from '/img/instruments/videomancer/diffract/diffract_ex3_s4.png';
import diffract_ex3_s5 from '/img/instruments/videomancer/diffract/diffract_ex3_s5.png';
import diffract_ex3_s6 from '/img/instruments/videomancer/diffract/diffract_ex3_s6.png';

# Diffract

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Car", before: diffract_source1_car, after: diffract_hero_s1 },
    { label: "Parrot", before: diffract_source2_parrot, after: diffract_hero_s2 },
    { label: "Clouds", before: diffract_source3_clouds, after: diffract_hero_s3 },
    { label: "Pattern", before: diffract_source4_pattern, after: diffract_hero_s4 },
    { label: "Girl", before: diffract_source5_girl, after: diffract_hero_s5 },
    { label: "Paint", before: diffract_source6_paint, after: diffract_hero_s6 },
  ]}
/>
*Diffract splitting edge transitions into prismatic color fringes through horizontal shift register tap differencing.*

---

## Overview

When white light passes through a diffraction grating — a surface scored with thousands of parallel slits — each wavelength bends at a slightly different angle. Red bends the most, violet the least, and the spectrum fans out into a rainbow of separated colors. Diffract recreates this phenomenon in the video domain by treating luminance transitions as optical edges that split incoming chrominance into colored fringes.

The program maintains a 32-entry horizontal shift register that stores recent Y (luminance) values as pixels stream through the pipeline. Three taps — near, mid, and far — read from configurable positions within the register. The signed differences between these taps produce the chromatic fringes: the primary fringe (near minus far) drives one color channel, while the secondary fringe (mid minus near) drives the other. Only the U and V channels are modified; luminance passes through untouched, preserving the structural clarity of the original image while wrapping its edges in spectral color.

The name evokes both the physical phenomenon of diffraction and the mathematical act of splitting a signal into constituent parts. At subtle settings, Diffract adds gentle rainbow halos to high-contrast edges — much like chromatic aberration in vintage lenses. At extreme settings, it transforms the entire UV plane into a chrominance map derived from horizontal or vertical luminance gradients, producing vivid prismatic textures that bear little resemblance to the source color.

---

## Background

### What Is a Diffraction Grating?

A diffraction grating is an optical element consisting of a large number of equally spaced parallel slits or grooves. When a beam of light strikes the grating, each slit acts as a point source of wavelets that interfere constructively and destructively depending on wavelength and angle. The result is spatial separation of the light into its constituent wavelengths — a spectrum. Unlike a prism, which separates colors through refraction (bending due to a change in medium), a grating separates colors through interference (superposition of waves). Diffraction gratings produce sharper, more evenly spaced spectra than prisms and are the basis of most modern spectrometers.

Diffract borrows this concept by treating horizontally adjacent luminance values as an edge — a boundary where brightness changes rapidly. The shift register taps at different horizontal offsets act like the slit spacing of a grating: wider separation produces broader spectral splitting, while narrower taps concentrate the fringes closer to the edge.

### Spectral Dispersion and Color Orders

In physical optics, a diffraction grating produces multiple **orders** of spectra. The zeroth order is the undeviated beam (no color separation). The first order fans the spectrum outward at a moderate angle. Higher orders spread the spectrum further, with diminishing intensity. The angular separation between orders depends on the grating's slit spacing and the wavelength of light.

Diffract's three-tap architecture loosely parallels this structure. The near tap captures differences close to the current pixel — a first-order fringe. The mid and far taps capture differences across wider spans — higher-order fringes with greater spatial separation but potentially different intensity. The Intensity control scales the fringe amplitude, mimicking the brightness falloff of higher diffraction orders.

### Chromatic Aberration in Optics

Chromatic aberration occurs when a lens fails to bring all wavelengths to the same focal point. Longitudinal chromatic aberration causes different colors to focus at different distances from the lens; lateral (transverse) chromatic aberration causes different colors to form images at different sizes or positions on the sensor. The visible result is colored fringing at high-contrast edges — purple halos on the bright side, green halos on the dark side.

Videographers and cinematographers have long exploited chromatic aberration deliberately: vintage lenses with uncorrected aberration produce a distinctive look prized for its organic imperfection. Diffract produces a similar aesthetic digitally. Because the fringes are derived from luminance differences, they appear only at transitions — exactly where optical chromatic aberration would manifest.

### Shift Registers as Delay Lines

In digital signal processing, a shift register is a chain of storage elements that passes data from one stage to the next on each clock cycle. In Diffract, the shift register stores 32 consecutive luminance values, creating a sliding window across the scan line. Reading from different positions within this register yields the same pixel's brightness as it appeared 1, 2, … 32 clock cycles ago — which, since pixels arrive sequentially along a scan line, corresponds to spatial offsets of 1 to 32 pixels to the left.

This is identical in principle to the analog bucket-brigade delay used in vintage audio effects: a chain of capacitors passes a sample from one to the next on each clock pulse. The BBD produced flanging and chorus by mixing the delayed signal with the original; Diffract produces colored fringes by differencing delayed luminance values and injecting the result into the chrominance channels.

### Horizontal vs Vertical Fringing

Most optical aberrations produce fringes along both axes simultaneously. Diffract provides two independent sources of fringe data. Horizontal mode (the default) derives fringes from the shift register, capturing left–right luminance transitions within a single scan line. Vertical mode derives fringes from a line buffer that stores the previous scan line's luminance, capturing top–bottom transitions between consecutive lines. Switching between modes changes the directional emphasis of the color splitting — horizontal mode creates side-by-side chromatic halos, while vertical mode creates vertically stacked fringes.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y Channel ──────────────────────────────────────────────────
│   │
│   ├─ 1. Input register (stage 1)
│   ├─ 2. Feed into 32-entry horizontal shift register
│   ├─ 3. Feed into video_line_buffer (previous-line Y storage)
│   └─ 4. Passthrough to output (Y unmodified)
│
├── Fringe Computation ─────────────────────────────────────────
│   │
│   ├─ 5a. H mode: Read 3 taps (near/mid/far) from shift register
│   │       diff_nf = tap_near − tap_far (primary fringe → U)
│   │       diff_mn = tap_mid − tap_near (secondary fringe → V)
│   │
│   ├─ 5b. V mode: Compare current Y vs previous-line Y
│   │       diff_nf = current − previous (primary fringe → U)
│   │       diff_mn = −(current − previous) (secondary fringe → V)
│   │
│   ├─ 6. Intensity scaling (right-shift 0–3)
│   ├─ 7. Falloff attenuation (additional right-shift 0–3)
│   ├─ 8. Order inversion (optional polarity flip)
│   ├─ 9. Color swap (optional U↔V exchange)
│   └─ 10. Double mode (optional: both channels get same fringe)
│
├── U/V Channels ───────────────────────────────────────────────
│   │
│   ├─ 11. Add fringes to source U and V
│   ├─ 12. Clamp to 0–1023
│   └─ 13. Wet/dry mix via 3× interpolator_u
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Delay pipeline (8 clocks)
│
└── Output ─────────────────────────────────────────────────────
    └─ Mixed Y, U, V + delayed sync
```

The critical design decision is that luminance passes through unmodified — only the chrominance channels are altered. This means Diffract never changes perceived brightness or spatial structure. All visible change occurs in the color domain, driven entirely by the shape of luminance transitions. Flat regions produce zero fringe (the tap differences are near zero), while sharp edges produce strong colored halos. The total fringe attenuation combines two independent right-shift stages (Intensity and Falloff), allowing six bits of range (divide by 1 through 64) for fine control over fringe visibility.

---

## Parameter Reference


### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Grating
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the base separation between the three shift register taps. At low values, all three taps cluster close together (base offset of 4 pixels), producing narrow, tight fringes concentrated at sharp edges. As the control increases, the base offset widens through 8, 12, 16, 20, 24, 28, and finally 31 pixels. Wider separation means the fringe computation compares pixels that are further apart, which broadens the color halo and causes even gradual transitions to produce visible splitting. At maximum, the near and far taps span the full 32-entry shift register, turning the entire horizontal neighborhood into a source of chromatic offset.

---

#### Knob 2 — Orders
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the fringe intensity by selecting how many bits of right-shift to apply to the raw difference values. At low settings, the shift is 3 (dividing the difference by 8), producing very subtle pastel fringes visible only at the hardest edges. At mid settings the shift decreases to 2 then 1, progressively strengthening the color deviation. At maximum, no shift is applied — the full signed difference is injected into the UV channels, producing vivid, saturated prismatic bands.

---

#### Knob 3 — Disperse
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Offsets the positions of all three taps within the shift register, shifting the fringe computation window left or right along the delay line. At zero, the near tap reads from position 1 (one pixel behind the current sample). As Disperse increases, a direction offset (derived from the top 3 bits, range 0–7) shifts all three tap positions deeper into the register. This moves the fringe spatially relative to the edge that produced it — at moderate settings the color halo leads or trails the luminance transition, creating an asymmetric chromatic split that mimics lateral chromatic aberration.

---

#### Knob 4 — Spread
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

The top bit of this control's register value determines whether the fringe polarity is inverted. Below 50%, fringes maintain their natural polarity — a bright-to-dark transition produces a specific color assignment. Above 50%, the polarity flips: the same transition produces the complementary color. This is analogous to viewing a spectrum through an inverting prism, swapping which side of an edge gets blue-shifted and which gets red-shifted. The lower 9 bits of the register are unused.

---

#### Knob 5 — Falloff
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Applies an additional attenuation stage after intensity scaling, further reducing fringe amplitude. At minimum, no extra attenuation is applied. As the control increases through its four steps (right-shift 0, 1, 2, 3), the fringes progressively fade. This interacts multiplicatively with the Intensity scaling — with both at their midpoints, the total attenuation is a right-shift of 3 (divide by 8), producing delicate pastel halos. With both at opposite extremes you can achieve either full-strength fringes or nearly invisible tinting.

---

#### Knob 6 — Angle
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the wet/dry crossfade between the processed signal (with chromatic fringes) and the original unprocessed signal. At 0%, the output is entirely dry — no fringes are visible. At 100%, the output is fully wet — the maximum fringe effect is applied. Intermediate values blend the two proportionally, allowing fine control over the overall prominence of the prismatic color splitting without changing the fringe structure itself. In the VHDL implementation, this control maps directly to the interpolator mix parameter.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Mode** | Split | Fan |
| **8 — Spectrum** | Full | Red |
| **9 — Blend** | Add | Screen |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

Three toggle bits control the fringe routing topology. Mode selects the source of fringe data (horizontal shift register or vertical line buffer). Spectrum selects whether each UV channel receives a distinct fringe or both receive the same fringe. Blend swaps which fringe feeds U and which feeds V. The three toggles interact combinatorially — there are eight possible routing configurations, each producing a distinct spatial and chromatic character. Animate and Bypass are reserved controls defined in the parameter map.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Overall output mix level. At full position, the processed signal with chromatic fringes is output at maximum. This control provides a master fade for the Diffract effect. In the current implementation the primary wet/dry crossfade is handled by the Angle knob (Pot 6), which directly drives the interpolator mix parameter; the fader may serve as an additional attenuation stage depending on firmware version.

---

## Guided Exercises

These exercises progress from basic horizontal chromatic fringes through vertical mode and advanced fringe routing, building familiarity with how each control shapes the prismatic color splitting.

### Exercise 1: Horizontal Edge Fringes

<BeforeAfterSlider
  sources={[
    { label: "Car", before: diffract_source1_car, after: diffract_ex1_s1 },
    { label: "Parrot", before: diffract_source2_parrot, after: diffract_ex1_s2 },
    { label: "Clouds", before: diffract_source3_clouds, after: diffract_ex1_s3 },
    { label: "Pattern", before: diffract_source4_pattern, after: diffract_ex1_s4 },
    { label: "Girl", before: diffract_source5_girl, after: diffract_ex1_s5 },
    { label: "Paint", before: diffract_source6_paint, after: diffract_ex1_s6 },
  ]}
/>
*Horizontal Edge Fringes — simulated result across source images.*
**Source**: High-contrast footage with strong vertical edges — architectural lines, window frames, or graphic text overlays.

**Objective**: Create rainbow-like chromatic halos along vertical edges using horizontal shift register differencing.

1. **Establish fringes**: Slowly increase Orders from 0% until colored halos become visible along vertical edges in the source. At about 75%, the fringes should be clearly saturated.
2. **Widen the grating**: Increase Grating from 50% upward. Watch the color halos broaden as the tap separation increases. At maximum, even gradual transitions produce wide chromatic bands.
3. **Shift the dispersion**: Sweep Disperse across its range. Notice how the fringe position slides relative to the edge that generated it — at one extreme the color leads the edge, at the other it trails.
4. **Invert polarity**: Turn Spread past 50%. The fringe colors flip — blue becomes orange, magenta becomes green. Return below 50% to restore.
5. **Attenuate**: Increase Falloff to soften the fringes into pastel tints. Combine with moderate Orders for delicate vintage-lens chromatic aberration.

**Key concepts**: Shift register taps at different offsets create spatial luminance differences that become UV color fringes, wider tap separation broadens fringes, intensity and falloff give two independent amplitude controls

---

### Exercise 2: Vertical Fringe Mode

<BeforeAfterSlider
  sources={[
    { label: "Car", before: diffract_source1_car, after: diffract_ex2_s1 },
    { label: "Parrot", before: diffract_source2_parrot, after: diffract_ex2_s2 },
    { label: "Clouds", before: diffract_source3_clouds, after: diffract_ex2_s3 },
    { label: "Pattern", before: diffract_source4_pattern, after: diffract_ex2_s4 },
    { label: "Girl", before: diffract_source5_girl, after: diffract_ex2_s5 },
    { label: "Paint", before: diffract_source6_paint, after: diffract_ex2_s6 },
  ]}
/>
*Vertical Fringe Mode — simulated result across source images.*
**Source**: Footage with strong horizontal edges — landscape horizons, stacked bookshelves, or horizontally striped patterns.

**Objective**: Switch to vertical fringe mode and observe how chromatic splitting follows horizontal edges instead of vertical ones.

1. **Start in H mode**: Set Grating ~50%, Orders ~75%, all other controls at defaults. Observe horizontal fringes along vertical edges.
2. **Switch to V mode**: Set Mode to Fan. The fringes now appear along horizontal edges — the program is differencing the current scan line against the previous one via the line buffer.
3. **Compare**: Toggle Mode back and forth between Split and Fan. Note that vertical edges produce fringes in H mode, horizontal edges in V mode.
4. **Combine with color swap**: Set Blend to Screen. The fringe hue rotates, shifting the color character of the vertical fringes.
5. **Double mode**: Set Spectrum to Red. Both U and V receive the same fringe, eliminating the complementary split and producing a single-hue tint that follows edge direction.

**Key concepts**: Vertical mode uses a line buffer instead of the shift register, H and V modes emphasize perpendicular edge orientations, color swap rotates the fringe hue axis

---

### Exercise 3: Prismatic Texture Synthesis

<BeforeAfterSlider
  sources={[
    { label: "Car", before: diffract_source1_car, after: diffract_ex3_s1 },
    { label: "Parrot", before: diffract_source2_parrot, after: diffract_ex3_s2 },
    { label: "Clouds", before: diffract_source3_clouds, after: diffract_ex3_s3 },
    { label: "Pattern", before: diffract_source4_pattern, after: diffract_ex3_s4 },
    { label: "Girl", before: diffract_source5_girl, after: diffract_ex3_s5 },
    { label: "Paint", before: diffract_source6_paint, after: diffract_ex3_s6 },
  ]}
/>
*Prismatic Texture Synthesis — simulated result across source images.*
**Source**: Any footage with rich tonal variation — nature scenes, skin tones, fabric textures.

**Objective**: Push all fringe controls to create vivid prismatic textures that transform the entire chrominance plane.

1. **Maximum splitting**: Set Grating to 100%, Orders to 100%, Falloff to 0%. The full raw fringe difference is applied with no attenuation.
2. **Color swap**: Set Blend to Screen to explore the complementary color palette.
3. **Double mode**: Set Spectrum to Red. Both channels receive the same fringe — the image takes on a strongly tinted look driven entirely by luminance gradients.
4. **Invert**: Toggle Spread past 50% to flip the entire color assignment.
5. **Mix back**: Reduce Angle to ~50% to blend the extreme prismatic effect with the original color, creating a more balanced, iridescent result.
6. **Disperse sweep**: Slowly sweep Disperse while watching the fringe offset slide across edges. At specific settings the fringes align with source features to produce unexpected constructive patterns.

**Key concepts**: At maximum intensity the UV plane becomes entirely luminance-gradient-derived, double mode eliminates complementary splitting, mix brings extreme effects back to usable territory

---


## Tips

- **Fringes only appear at edges**: Because Diffract derives color from luminance *differences*, flat regions of uniform brightness produce no visible effect. Feed it high-contrast material for maximum impact.
- **Two attenuation stages stack**: Intensity and Falloff each provide 0–3 bits of right-shift. Combined, you have up to 6 bits of attenuation (divide by 64) for ultra-subtle tinting, or zero attenuation for vivid prismatic bands.
- **Order inversion is binary**: The Spread pot's top bit is all that matters — the control flips fringe polarity at the 50% mark. Use it as a toggle, not a continuous sweep.
- **Vertical mode needs horizontal edges**: H mode creates fringes along vertical edges; V mode creates fringes along horizontal edges. Choose the mode that matches the dominant edge orientation in your source.
- **Double mode for tinted looks**: Setting Spectrum to the alternate position forces both U and V to the same fringe value, producing a monochromatic tint that follows edge structure — useful for subtle warm or cool lens-aberration effects.
- **Mix control for blending**: The Angle knob controls the wet/dry balance via the internal interpolators. Use moderate settings (40–60%) to layer prismatic fringes subtly over the original color.
- **Feedback loops**: Routing Diffract's output back to its input creates accumulating chromatic fringes — each pass adds another layer of spectral splitting, building into dense rainbow textures.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; dedicated memory resources within the FPGA fabric used for line buffer storage. |
| **Chromatic Aberration** | An optical defect where a lens fails to bring all wavelengths to the same focus, producing colored fringes at high-contrast edges. |
| **Diffraction** | The bending and spreading of waves around obstacles or through apertures, separating wavelengths by angle. |
| **Dispersion** | The separation of light into its constituent wavelengths, as by a prism or diffraction grating. |
| **Fringe** | A band of color produced by interference or diffraction, appearing at the boundary between bright and dark regions. |
| **Grating** | An optical element with periodic structure that diffracts light into multiple spectral orders. |
| **Interpolator** | A hardware module that computes weighted averages between two values, used here for wet/dry mixing. |
| **Line Buffer** | A single-line BRAM delay that stores one scan line of video data for vertical comparison. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next on each clock cycle. |
| **Shift Register** | A chain of storage elements that passes data from one stage to the next on each clock cycle, providing horizontal pixel delay. |
| **Tap** | A read point within a delay line or shift register, extracting a sample at a specific offset. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
