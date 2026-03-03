---
draft: true
sidebar_position: 119
slug: /instruments/videomancer/fogbank
title: "Fogbank"
image: /img/instruments/videomancer/fogbank/fogbank_hero_s1.png
description: "Fog is the atmosphere made visible."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import fogbank_control_panel from '/img/instruments/videomancer/fogbank/fogbank_control_panel.png';
import fogbank_source1_skull from '/img/instruments/videomancer/fogbank/fogbank_source1_skull.png';
import fogbank_source2_dog from '/img/instruments/videomancer/fogbank/fogbank_source2_dog.png';
import fogbank_source3_collage from '/img/instruments/videomancer/fogbank/fogbank_source3_collage.png';
import fogbank_source4_pattern from '/img/instruments/videomancer/fogbank/fogbank_source4_pattern.png';
import fogbank_source5_man from '/img/instruments/videomancer/fogbank/fogbank_source5_man.png';
import fogbank_source6_knit from '/img/instruments/videomancer/fogbank/fogbank_source6_knit.png';
import fogbank_hero_s1 from '/img/instruments/videomancer/fogbank/fogbank_hero_s1.png';
import fogbank_hero_s2 from '/img/instruments/videomancer/fogbank/fogbank_hero_s2.png';
import fogbank_hero_s3 from '/img/instruments/videomancer/fogbank/fogbank_hero_s3.png';
import fogbank_hero_s4 from '/img/instruments/videomancer/fogbank/fogbank_hero_s4.png';
import fogbank_hero_s5 from '/img/instruments/videomancer/fogbank/fogbank_hero_s5.png';
import fogbank_hero_s6 from '/img/instruments/videomancer/fogbank/fogbank_hero_s6.png';
import fogbank_ex1_s1 from '/img/instruments/videomancer/fogbank/fogbank_ex1_s1.png';
import fogbank_ex1_s2 from '/img/instruments/videomancer/fogbank/fogbank_ex1_s2.png';
import fogbank_ex1_s3 from '/img/instruments/videomancer/fogbank/fogbank_ex1_s3.png';
import fogbank_ex1_s4 from '/img/instruments/videomancer/fogbank/fogbank_ex1_s4.png';
import fogbank_ex1_s5 from '/img/instruments/videomancer/fogbank/fogbank_ex1_s5.png';
import fogbank_ex1_s6 from '/img/instruments/videomancer/fogbank/fogbank_ex1_s6.png';
import fogbank_ex2_s1 from '/img/instruments/videomancer/fogbank/fogbank_ex2_s1.png';
import fogbank_ex2_s2 from '/img/instruments/videomancer/fogbank/fogbank_ex2_s2.png';
import fogbank_ex2_s3 from '/img/instruments/videomancer/fogbank/fogbank_ex2_s3.png';
import fogbank_ex2_s4 from '/img/instruments/videomancer/fogbank/fogbank_ex2_s4.png';
import fogbank_ex2_s5 from '/img/instruments/videomancer/fogbank/fogbank_ex2_s5.png';
import fogbank_ex2_s6 from '/img/instruments/videomancer/fogbank/fogbank_ex2_s6.png';
import fogbank_ex3_s1 from '/img/instruments/videomancer/fogbank/fogbank_ex3_s1.png';
import fogbank_ex3_s2 from '/img/instruments/videomancer/fogbank/fogbank_ex3_s2.png';
import fogbank_ex3_s3 from '/img/instruments/videomancer/fogbank/fogbank_ex3_s3.png';
import fogbank_ex3_s4 from '/img/instruments/videomancer/fogbank/fogbank_ex3_s4.png';
import fogbank_ex3_s5 from '/img/instruments/videomancer/fogbank/fogbank_ex3_s5.png';
import fogbank_ex3_s6 from '/img/instruments/videomancer/fogbank/fogbank_ex3_s6.png';

# Fogbank

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: fogbank_source1_skull, after: fogbank_hero_s1 },
    { label: "Dog", before: fogbank_source2_dog, after: fogbank_hero_s2 },
    { label: "Collage", before: fogbank_source3_collage, after: fogbank_hero_s3 },
    { label: "Pattern", before: fogbank_source4_pattern, after: fogbank_hero_s4 },
    { label: "Man", before: fogbank_source5_man, after: fogbank_hero_s5 },
    { label: "Knit", before: fogbank_source6_knit, after: fogbank_hero_s6 },
  ]}
/>
*Dense rolling fog banks drift across a sunlit landscape, swallowing colour and detail into soft luminous white — only the faintest outlines survive beneath the blanket.*

---

## Overview

Fog is the atmosphere made visible. When water vapour condenses into fine droplets suspended in air, the result is a curtain of diffused light that flattens contrast, bleaches colour, and reduces the visible world to a narrow range of pale luminance. In cinematography, fog is both a practical effect and a narrative device — rolling ground fog signals danger, rising mist conveys dawn, settling haze suggests memory. Fogbank recreates this atmospheric phenomenon in the FPGA pipeline, generating procedural fog density bands that drift across the video frame and blend the source image toward white or grey obscurity.

The fog pattern is a vertical triangle wave whose phase scrolls frame by frame via a DDS accumulator, producing the appearance of rolling fog banks that traverse the image. An LFSR turbulence generator adds randomised noise to the fog boundary, breaking the mathematically perfect wave into organic, billowing edges. Density controls how much luma the fog adds, opacity governs the strength of the blend, and band width sets the vertical period of the fog pattern — narrow bands create fine horizontal striations, wide bands produce broad atmospheric blankets. The chroma channels are simultaneously desaturated toward neutral grey proportional to fog intensity, simulating the colour-robbing effect of particulate scattering.

The name *Fogbank* refers to the dense, wall-like formations of fog that roll in from the sea along coastlines — an impenetrable blanket of suspended moisture that consumes everything in its path.

---

## Background

### Atmospheric Fog in Cinematography

Fog has been a staple of visual storytelling since the earliest days of cinema. Directors use fog machines, glycol haze, and dry ice to fill sets with particulate scattering, softening hard edges and creating depth layers that separate foreground from background. In John Carpenter's *The Fog* (1980), rolling banks of coastal fog become the primary antagonist — an enveloping presence that obscures and reveals in equal measure. In colour science, fog reduces scene contrast by adding a uniform luminance offset (airlight) while simultaneously desaturating colours through wavelength-independent Mie scattering. Fogbank models both effects: luma is pushed toward a bright target while chroma is pulled toward the neutral axis, all modulated by a spatially varying density function.

### Rolling Fog and Ground Fog Phenomena

In meteorology, advection fog forms when warm, moist air moves horizontally over a cooler surface — the cooling condenses moisture into a low-lying blanket that rolls forward with the wind. Radiation fog forms when the ground cools overnight and the air above it condenses from the bottom up, producing bands of dense fog at ground level that thin with altitude. Both phenomena produce horizontally stratified density patterns — the fog is thickest at certain vertical positions and thinner at others. Fogbank's vertical triangle wave emulates this stratification, with the band width control setting the spacing between peak-density layers and the DDS scroll simulating the horizontal advection of the fog mass across the frame.

### DDS-Based Scroll Animation

Direct Digital Synthesis is a frequency generation technique where a fixed-width accumulator is incremented by a tuning word on each trigger event. The accumulator wraps naturally at its bit width, producing seamless cyclical progression without explicit bounds checking. In Fogbank, the DDS accumulator advances once per vertical sync pulse (once per frame), and its upper bits are added to the scanline counter to produce a phase-shifted triangle wave. This makes the fog pattern scroll vertically through the image at a rate proportional to the drift speed knob. The direction toggle selects addition or subtraction, reversing the drift. A speed mode flag doubles the increment for faster animation. Because the DDS wraps at 16 bits, the fog pattern cycles seamlessly without discontinuity.

### Turbulence via LFSR Noise

A 16-bit linear feedback shift register (LFSR) generates a maximal-length pseudo-random sequence that runs continuously at the pixel clock rate. The LFSR output provides high-frequency noise that is AND-masked by the turbulence parameter — at zero turbulence, the mask is all zeros and no noise passes through; at maximum, the full 10-bit noise amplitude is added to the triangle wave. The result breaks the smooth fog boundary into irregular, billowing edges that suggest the organic fractal structure of real atmospheric turbulence. The LFSR runs free and is not synchronised to the frame, so the turbulence pattern evolves naturally at the pixel rate, producing a different noise texture on every frame.

### Fog Compositing and Aerial Perspective

In computer graphics, fog compositing blends each pixel toward a fog colour based on a depth or density function: `output = mix(scene, fog_colour, fog_density)`. Aerial perspective — the observation that distant objects appear lighter, bluer, and less saturated — is the photographic basis for this technique. Fogbank implements a simplified version: the fog density function is the processed triangle wave (with turbulence), and the blend pushes luma toward a bright target (white or grey) while pulling chroma toward the neutral axis at 512. Higher fog intensity produces stronger blending — the image appears to recede into the fog. The opacity control scales the blend strength independently of the density pattern, allowing fine adjustment of how aggressively the fog obscures the source.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├─ 1. Input Register + Position Counters      (1 clock)
│      ├─ Y/U/V registered
│      ├─ h_count incremented per active pixel
│      └─ v_count incremented per hsync
│
├─ DDS Phase Accumulator                      (per vsync)
│      ├─ increment = drift_speed << 6 (normal) or << 7 (speed mode)
│      ├─ direction=0: phase += increment
│      └─ direction=1: phase -= increment
│
├─ Parameter Pre-Registration                 (1 clock)
│      ├─ band_shift: band_width → shift 2–9
│      ├─ turb_mask: turbulence register (AND mask)
│      ├─ fog_target_y: 1023 (white) or 768 (grey)
│      └─ opacity_shift: opacity → shift 0–4
│
├─ 2. Wave Function + Turbulence              (1 clock)
│      ├─ wave_input = v_count + dds_phase[15:4]
│      ├─ wave_shifted = wave_input >> band_shift
│      ├─ triangle: if MSB set → invert lower bits
│      └─ turb_noise = LFSR[9:0] AND turb_mask
│
├─ 3. Fog Intensity Compute                   (1 clock)
│      ├─ wave_turb = wave_val + turb_noise (saturate at 1023)
│      ├─ density scaling: shift right 0/1/2/3 based on density pot
│      └─ fog_intensity = scaled result
│
├─ 4. Fog Blend + Desaturate Compose          (1 clock)
│      ├─ fog_add = Y + fog_intensity >> opacity_shift
│      ├─ clamp Y to fog_target (1023 or 768)
│      ├─ heavy fog (>512): U/V → 512 + (chroma−512)>>2
│      ├─ medium fog (>256): U/V → 512 + (chroma−512)>>1
│      └─ light fog (<256): U/V passthrough
│
├─ 5–8. Interpolator Mix (×3 channels)        (4 clocks)
│      └─ mix = lerp(delayed_input, composed, mix_amount)
│
├─ Sync/Data Delay Pipeline                   (8-clock shift register)
│
└─ Output Mux
    ├─ Bypass off → mixed Y/U/V + aligned sync
    └─ Bypass on  → delayed input Y/U/V + aligned sync
```

The fog density pattern is computed entirely from vertical position and the DDS phase accumulator — it has no horizontal variation apart from the LFSR turbulence. This produces horizontally continuous fog bands whose vertical structure is defined by the triangle wave period and whose edges are softened by the noise mask. The DDS accumulator advances once per frame on the vsync falling edge, scrolling the fog pattern through the image at a rate controlled by Drift Speed. Because the DDS is 16 bits and only the upper 12 bits are used as a phase offset, the scroll is sub-scanline smooth.

The fog blend stage pushes luma toward the target brightness while simultaneously desaturating chroma. These two operations together simulate the visual effect of real fog: bright, colourless obscurity. The desaturation is intensity-dependent — regions under heavy fog lose three quarters of their colour, medium fog loses half, and light fog passes chroma unchanged. This stepped desaturation avoids the computational cost of a full per-pixel multiplier while providing a convincing approximation.

---

## Parameter Reference

<img src={fogbank_control_panel} alt="Videomancer front panel with Fogbank loaded"/>
*Videomancer's front panel with Fogbank active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Density
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the peak intensity of the fog effect by scaling the combined wave-plus-turbulence value. At minimum, the fog intensity is attenuated by a right-shift of 3 — barely visible brightening even in the densest fog bands. As the knob increases through four discrete threshold steps, the scaling increases to full amplitude at maximum, where the fog can push luma close to the white or grey target. This control determines how opaque the fog appears at its densest — think of it as the thickness of the fog layer. At low values, the fog is a thin haze that slightly washes out the image; at high values, it is an impenetrable blanket.

---

#### Knob 2 — Band W
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the vertical period of the fog band triangle wave by selecting a bit-shift amount applied to the vertical position counter. Small values produce narrow, closely spaced fog bands — fine horizontal striations across the frame. Large values produce wide, sweeping bands that span hundreds of scanlines — broad atmospheric blankets that engulf large portions of the image. The mapping divides the register range into eight zones, each selecting a shift from 2 to 9, producing wave periods from approximately 4 scanlines (fastest cycle) to 512 scanlines (slowest cycle). Mid-range values create fog bands roughly 30–60 scanlines wide, a natural-looking formation scale for HD video.

---

#### Knob 3 — Drift Spd
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the rate at which the fog pattern scrolls through the frame. The register value is left-shifted by 6 bits (or 7 in speed mode) and added to or subtracted from the 16-bit DDS accumulator on each vsync. At zero, the fog pattern is static — bands remain fixed in vertical position. At moderate values, the fog drifts slowly upward or downward, simulating rolling advection. At maximum, the fog races through the frame in rapid bands. The visual character changes dramatically with speed: slow drift creates contemplative atmosphere, fast scroll creates strobing horizontal washes.

---

#### Knob 4 — Opacity
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Governs how strongly the fog blends into the source image by selecting the right-shift applied to the fog intensity before it is added to the input luma. At maximum opacity (shift 0), the full fog intensity is added to the luma — the fog is at full strength. Each step down doubles the attenuation: shift 1 halves the fog contribution, shift 2 quarters it, and so on down to shift 4 where only one-sixteenth of the fog intensity survives. This controls the translucency of the fog independently of its density — you can have a dense fog pattern (high Density) that is applied lightly (low Opacity), producing subtle brightening in the fog bands without washing out the image.

---

#### Knob 5 — Coverage
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Adds LFSR-generated pseudo-random noise to the fog wave boundary. At zero, the fog bands have perfectly smooth, mathematically defined edges — the triangle wave is pristine. As the knob increases, more bits of the LFSR output pass through the AND mask, adding progressively stronger random perturbation to the fog density at each pixel. Moderate values break the band edges into organic scallops and wisps. Maximum values inject full-amplitude noise, creating a chaotic, turbulent fog texture where the band structure is barely recognisable beneath the random fluctuations.

---

#### Knob 6 — Tint
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

This control is reserved and has no effect on the VHDL processing pipeline. The register is mapped but not connected to any internal signal. Future firmware revisions may assign this parameter to fog colour tinting or other extensions. In its current state, adjusting this knob produces no visible change in the output.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Pattern** | Rolling | Rising |
| **8 — Color** | White | Grey |
| **9 — Edge** | Soft | Sharp |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

The toggle switches divide into two functional clusters. Pattern (7) and Color (8) map to VHDL bits that control fog behaviour — direction of drift and fog brightness target. Edge (9) and Animate (10) are defined in the TOML interface but are not connected to active VHDL processing — they are reserved for future use. Bypass (11) routes the delayed input directly to the output, overriding all fog processing. The connected toggles (7 and 8) combine freely: rising grey fog or settling white fog are equally valid configurations.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfades between the delayed dry input and the fog-composited output. At 0% (fader down), the output is pure dry — no fog is visible. At 100% (fader up), the output is the fully fog-blended image. Intermediate positions provide proportional blending, allowing the fog to appear as a semi-transparent overlay. This control operates after the fog composition stage, so it uniformly scales the fog effect across the entire frame regardless of the fog density pattern.

---

## Guided Exercises

These exercises progress from a static fog overlay through animated rolling fog to turbulent atmospheric effects. Each introduces a new control while building on the settings learned in the previous exercise.

### Exercise 1: Static Fog Blanket

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: fogbank_source1_skull, after: fogbank_ex1_s1 },
    { label: "Dog", before: fogbank_source2_dog, after: fogbank_ex1_s2 },
    { label: "Collage", before: fogbank_source3_collage, after: fogbank_ex1_s3 },
    { label: "Pattern", before: fogbank_source4_pattern, after: fogbank_ex1_s4 },
    { label: "Man", before: fogbank_source5_man, after: fogbank_ex1_s5 },
    { label: "Knit", before: fogbank_source6_knit, after: fogbank_ex1_s6 },
  ]}
/>
*Static Fog Blanket — simulated result across source images.*
**Source**: A landscape photograph or footage with good tonal range — mountains, city skyline, or outdoor scene with clear detail.

**Objective**: Understand how Density, Band Width, and Opacity interact to create a static fog overlay without animation.

1. **Broad fog bands**: Set Band W to ~75% for wide fog bands that span large vertical regions.
2. **Moderate density**: Set Density to ~50%. Fog bands become visible as brightened horizontal zones across the image.
3. **Full opacity**: Set Opacity to ~75%. The fog blending is strong — bright regions are clearly washed toward white.
4. **Observe desaturation**: Notice that colours within the fog bands are muted — chroma is pulled toward neutral grey proportional to fog intensity.
5. **Reduce band width**: Lower Band W to ~25%. The fog bands become narrow horizontal stripes — fine striations across the frame.
6. **Vary density**: Sweep Density from 0% to 100%. At low values, the fog is a faint haze; at maximum, the fog bands are dense white blankets.

**Key concepts**: Density controls peak fog intensity, Band Width sets vertical wave period, Opacity scales the blend strength, desaturation increases with fog intensity, no animation when Drift Speed is at 0%

---

### Exercise 2: Rolling Fog Drift

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: fogbank_source1_skull, after: fogbank_ex2_s1 },
    { label: "Dog", before: fogbank_source2_dog, after: fogbank_ex2_s2 },
    { label: "Collage", before: fogbank_source3_collage, after: fogbank_ex2_s3 },
    { label: "Pattern", before: fogbank_source4_pattern, after: fogbank_ex2_s4 },
    { label: "Man", before: fogbank_source5_man, after: fogbank_ex2_s5 },
    { label: "Knit", before: fogbank_source6_knit, after: fogbank_ex2_s6 },
  ]}
/>
*Rolling Fog Drift — simulated result across source images.*
**Source**: A static or slow-moving video scene — architectural footage, landscape, or a still frame.

**Objective**: Add DDS-driven animation to the fog bands and explore direction, speed mode, and drift rate.

1. **From Exercise 1**: Keep Density ~50%, Band W ~60%, Opacity ~70%.
2. **Add drift**: Increase Drift Spd to ~30%. The fog bands begin scrolling vertically through the image — rolling fog.
3. **Observe wrapping**: Watch as the fog pattern exits one edge of the frame and re-enters from the other — the DDS wrap is seamless.
4. **Reverse direction**: Toggle Pattern to Rising. The fog now drifts in the opposite vertical direction.
5. **Speed mode**: Toggle Edge to Sharp (this activates speed mode in the VHDL). The drift rate doubles — fog races through the frame.
6. **Slow romantic drift**: Set Drift Spd to ~10%, Edge back to Soft. The fog drifts slowly — contemplative and atmospheric.
7. **Grey fog**: Toggle Color to Grey. The fog target drops from white to a dimmer grey — the atmosphere shifts from bright steam to twilight mist.

**Key concepts**: DDS scroll creates seamless animated fog drift, direction toggle reverses scroll, speed mode doubles the rate, grey fog target produces darker atmospheric effects, drift speed controls animation pace

---

### Exercise 3: Turbulent Fogbank

<BeforeAfterSlider
  sources={[
    { label: "Skull", before: fogbank_source1_skull, after: fogbank_ex3_s1 },
    { label: "Dog", before: fogbank_source2_dog, after: fogbank_ex3_s2 },
    { label: "Collage", before: fogbank_source3_collage, after: fogbank_ex3_s3 },
    { label: "Pattern", before: fogbank_source4_pattern, after: fogbank_ex3_s4 },
    { label: "Man", before: fogbank_source5_man, after: fogbank_ex3_s5 },
    { label: "Knit", before: fogbank_source6_knit, after: fogbank_ex3_s6 },
  ]}
/>
*Turbulent Fogbank — simulated result across source images.*
**Source**: High-contrast footage with strong edges — faces, text, or geometric patterns.

**Objective**: Add LFSR turbulence to break the fog band edges into organic, billowing shapes and explore the interplay between turbulence and density.

1. **From Exercise 2**: Keep Density ~60%, Band W ~50%, Drift Spd ~20%, Opacity ~65%.
2. **Add turbulence**: Increase Coverage to ~40%. The fog band edges begin to break apart — irregular noise creates billowing, organic boundaries.
3. **Increase turbulence**: Push Coverage to ~80%. The noise dominates — fog bands become chaotic, textured clouds rather than smooth horizontal zones.
4. **Reduce density to compensate**: Lower Density to ~30%. The turbulent fog becomes a delicate veil of noise-textured haze — organic and subtle.
5. **Maximum turbulence**: Push Coverage to 100% and Density to ~70%. The fog is now a dense, churning mass of randomised brightness — heavy atmospheric interference.
6. **Mix for subtlety**: Pull Mix fader to ~50%. The turbulent fog blends half-strength with the input, creating a foggy overlay that lets the source show through.
7. **White vs Grey turbulence**: Compare Color White and Color Grey at high turbulence. White produces bright noisy fog; grey produces a darker, smokier texture.

**Key concepts**: Turbulence adds LFSR noise to the wave boundary, noise amplitude is AND-masked by the Coverage parameter, high turbulence breaks band structure into chaotic clouds, density and turbulence interact multiplicatively, mix fader controls overall fog overlay strength

---


## Tips

- **Start with static fog**: Set Drift Spd to 0% to study the fog pattern without motion. This makes it easy to observe how Density, Band Width, and Opacity interact before adding animation.
- **Wide bands for atmosphere**: Band W above 70% produces broad, cinematic fog blankets. Narrow bands create fine horizontal striations that feel more artificial — useful for a digital aesthetic but less atmospheric.
- **Grey fog for subtlety**: The Grey colour target (768) is noticeably less aggressive than White (1023). Use it when you want fog atmosphere without completely bleaching the image.
- **Turbulence transforms the character**: Even a small amount of Coverage (20–30%) breaks the mathematical perfection of the triangle wave and makes the fog look organic. Maximum turbulence creates chaotic noise textures.
- **Opacity and Density are independent**: Density sets how much fog intensity the wave generates; Opacity sets how much of that intensity reaches the luma blend. High Density with low Opacity creates a fog pattern that is defined but subtle.
- **Speed mode via Edge toggle**: The Edge Soft/Sharp toggle actually controls the DDS speed mode in the VHDL — Sharp doubles the scroll rate. Use it for fast fog animation.
- **Mix for compositing**: The Mix fader is the master control for fog visibility. Pull it to 50% for a translucent fog overlay that lets the source show through clearly.
- **Bypass for comparison**: Toggle Bypass for instant before/after comparison. The DDS continues advancing during bypass, so the fog will have moved when you re-engage.

---

## Glossary

| Term | Definition |
|------|------------|
| **Advection fog** | Fog formed when warm, moist air moves horizontally over a cooler surface, causing condensation into a low-lying blanket of water droplets. |
| **Airlight** | The luminance contributed to a pixel by light scattered from atmospheric particles between the camera and the scene object, causing distant objects to appear brighter and lower in contrast. |
| **DDS (Direct Digital Synthesis)** | A technique for generating cyclical waveforms or smooth scrolling using a fixed-width accumulator incremented by a tuning word; the accumulator wraps naturally at its bit width. |
| **Desaturation** | Reducing the chroma (colour intensity) of a signal toward the neutral axis, making colours appear washed out or grey. |
| **Interpolator** | A hardware crossfade unit that blends two signals by a configurable ratio, used here for wet/dry mixing between the dry input and fog-composited output. |
| **LFSR (Linear Feedback Shift Register)** | A shift register whose input bit is a linear function of its previous state, producing a maximal-length pseudo-random binary sequence used for turbulence noise. |
| **Luma** | Short for luminance; the brightness component (Y channel) of a YUV video signal. |
| **Mie scattering** | Light scattering by particles comparable in size to the wavelength of light, responsible for the white appearance of fog and clouds (as opposed to the blue of Rayleigh scattering). |
| **Opacity** | The degree to which the fog blend attenuates or obscures the source image; higher opacity means more fog influence on the output. |
| **Triangle wave** | A periodic waveform that rises linearly to a peak and then falls linearly, producing smooth ramp-up and ramp-down patterns; used here to define the fog density profile. |
| **Turbulence** | Randomised perturbation added to the fog density function to break smooth mathematical edges into organic, irregular boundaries. |
| **YUV** | A colour model separating luminance (Y) from two chrominance components (U and V), used throughout Videomancer's video pipeline. |

---
