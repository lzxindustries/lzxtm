---
draft: true
sidebar_position: 202
slug: /instruments/videomancer/nacre
title: "Nacre"
image: /img/instruments/videomancer/nacre/nacre_hero_s1.png
description: "Mother-of-pearl, the iridescent lining of a mollusc shell, gets its color not from pigment but from thin-film interference — light waves reflecting off microscopic layers of aragonite, interfering constructively and destructively so that the apparent hue shifts with viewing angle and position."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import nacre_control_panel from '/img/instruments/videomancer/nacre/nacre_control_panel.png';
import nacre_source1_parrot from '/img/instruments/videomancer/nacre/nacre_source1_parrot.png';
import nacre_source2_cat from '/img/instruments/videomancer/nacre/nacre_source2_cat.png';
import nacre_source3_elephant from '/img/instruments/videomancer/nacre/nacre_source3_elephant.png';
import nacre_source4_pattern from '/img/instruments/videomancer/nacre/nacre_source4_pattern.png';
import nacre_source5_boy from '/img/instruments/videomancer/nacre/nacre_source5_boy.png';
import nacre_source6_wood from '/img/instruments/videomancer/nacre/nacre_source6_wood.png';
import nacre_hero_s1 from '/img/instruments/videomancer/nacre/nacre_hero_s1.png';
import nacre_hero_s2 from '/img/instruments/videomancer/nacre/nacre_hero_s2.png';
import nacre_hero_s3 from '/img/instruments/videomancer/nacre/nacre_hero_s3.png';
import nacre_hero_s4 from '/img/instruments/videomancer/nacre/nacre_hero_s4.png';
import nacre_hero_s5 from '/img/instruments/videomancer/nacre/nacre_hero_s5.png';
import nacre_hero_s6 from '/img/instruments/videomancer/nacre/nacre_hero_s6.png';
import nacre_ex1_s1 from '/img/instruments/videomancer/nacre/nacre_ex1_s1.png';
import nacre_ex1_s2 from '/img/instruments/videomancer/nacre/nacre_ex1_s2.png';
import nacre_ex1_s3 from '/img/instruments/videomancer/nacre/nacre_ex1_s3.png';
import nacre_ex1_s4 from '/img/instruments/videomancer/nacre/nacre_ex1_s4.png';
import nacre_ex1_s5 from '/img/instruments/videomancer/nacre/nacre_ex1_s5.png';
import nacre_ex1_s6 from '/img/instruments/videomancer/nacre/nacre_ex1_s6.png';
import nacre_ex2_s1 from '/img/instruments/videomancer/nacre/nacre_ex2_s1.png';
import nacre_ex2_s2 from '/img/instruments/videomancer/nacre/nacre_ex2_s2.png';
import nacre_ex2_s3 from '/img/instruments/videomancer/nacre/nacre_ex2_s3.png';
import nacre_ex2_s4 from '/img/instruments/videomancer/nacre/nacre_ex2_s4.png';
import nacre_ex2_s5 from '/img/instruments/videomancer/nacre/nacre_ex2_s5.png';
import nacre_ex2_s6 from '/img/instruments/videomancer/nacre/nacre_ex2_s6.png';
import nacre_ex3_s1 from '/img/instruments/videomancer/nacre/nacre_ex3_s1.png';
import nacre_ex3_s2 from '/img/instruments/videomancer/nacre/nacre_ex3_s2.png';
import nacre_ex3_s3 from '/img/instruments/videomancer/nacre/nacre_ex3_s3.png';
import nacre_ex3_s4 from '/img/instruments/videomancer/nacre/nacre_ex3_s4.png';
import nacre_ex3_s5 from '/img/instruments/videomancer/nacre/nacre_ex3_s5.png';
import nacre_ex3_s6 from '/img/instruments/videomancer/nacre/nacre_ex3_s6.png';

# Nacre

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: nacre_source1_parrot, after: nacre_hero_s1 },
    { label: "Cat", before: nacre_source2_cat, after: nacre_hero_s2 },
    { label: "Elephant", before: nacre_source3_elephant, after: nacre_hero_s3 },
    { label: "Pattern", before: nacre_source4_pattern, after: nacre_hero_s4 },
    { label: "Boy", before: nacre_source5_boy, after: nacre_hero_s5 },
    { label: "Wood", before: nacre_source6_wood, after: nacre_hero_s6 },
  ]}
/>
*Nacre applying position-dependent hue rotation and pearlescent shimmer to create thin-film iridescence across the video signal.*

---

## Overview

Mother-of-pearl, the iridescent lining of a mollusc shell, gets its color not from pigment but from thin-film interference — light waves reflecting off microscopic layers of aragonite, interfering constructively and destructively so that the apparent hue shifts with viewing angle and position. Nacre recreates this optical phenomenon electronically. It rotates the chrominance vector of every pixel by an angle determined by that pixel's screen position, producing rainbow bands that sweep diagonally or radially across the image.

The program derives its name directly from the mineralogical term *nacre* (from Arabic *naqqārah*), the substance that forms the inner surface of pearls, abalone, and nautilus shells. In nature, nacre's color arises from layers thinner than the wavelength of visible light. Here the "layers" are created by an 8-entry sine/cosine lookup table indexed by a position-derived 3-bit angle, producing U and V chrominance offsets that cycle through the hue circle as the index advances across the frame.

A separate luma shimmer path adds subtle brightness modulation to complete the pearlescent illusion. Saturation control lets you scale the source chroma independently, and a pastel mode softens the rainbow into gentler tints. All scaling uses shift-and-add arithmetic — no generic multipliers — keeping resource usage low and timing reliable on the iCE40 HX4K at 74.25 MHz.

---

## Quick Start

1. **Start with monochrome sources**: Nacre's iridescence is most visible on desaturated or gray material where the rainbow overlay is the only color present.
2. **Match frequency axes for 45° bands**: Equal H and V Frequency values produce classic diagonal bands; unequal values tilt the bands toward horizontal or vertical.
3. **Use Saturation to control the competition**: Low Saturation lets the rainbow dominate; high Saturation forces the source color to compete with the overlay, creating mixed hues.

---

## Background

### Thin-Film Interference

When light hits a thin transparent film (oil on water, a soap bubble, the aragonite layers of nacre), some reflects from the top surface and some from the bottom. These two reflected beams travel slightly different distances. If the path difference equals a whole number of wavelengths, the beams add constructively and that color appears bright; if it equals a half-wavelength offset, they cancel. Because the path difference depends on the film's thickness and the viewing angle, the reflected hue changes across the surface. Nacre simulates this by sweeping a hue-rotation angle as a function of horizontal and vertical pixel position.

### Hue Rotation in YUV Space

In YUV color encoding, hue is the angle of the (U, V) chrominance vector around the achromatic axis. Rotating that vector by an angle θ remaps red to green, green to blue, blue to red — a smooth traversal of the hue circle. Rather than computing sin(θ) and cos(θ) on the fly, Nacre stores eight pre-computed (cos, sin) pairs in a lookup table, splitting the 360° circle into 45° steps. The 3-bit LUT index comes from the pixel position, so hue rotates in eight discrete bands as you move across the frame.

### Shift-and-Add Scaling

On the iCE40 FPGA, dedicated multiply blocks are scarce. Nacre avoids them entirely by implementing all amplitude and frequency controls as right-shift operations. Shifting a binary value right by N positions divides by 2^N. The pot-to-shift mapping quantizes each 10-bit pot range into threshold bands (128-count steps for frequency, 256-count steps for strength), each selecting a different shift amount. This gives coarse but reliable control with guaranteed single-cycle timing.

### Direct Digital Synthesis Animation

Nacre's animation system uses a DDS (Direct Digital Synthesis) phase accumulator. Each frame, the Anim Speed register value is added to a 16-bit accumulator. The top 12 bits of the accumulator become a phase offset added to the position-derived angle, effectively phase-shifting the entire rainbow pattern. Higher pot values produce faster accumulation and thus faster animation. Because the accumulator wraps naturally at 16 bits, the animation loops seamlessly.

### Luma-Linked Iridescence

In real nacre, the iridescent shimmer is more visible on the highlights and fades into shadow. The Video Mod toggle enables a crude approximation: pixels brighter than mid-gray (Y > 512) receive the chroma offset at half strength, while darker pixels receive it at one-eighth strength. This creates a brightness-dependent shimmer where iridescence concentrates on the lit surfaces of the source image.


---

## Signal Flow

Y Channel → U/V Channels → Sync Signals → Bypass

```
Input Video (YUV 4:4:4)
│
├── Y Channel ─────────────────────────────────────────────────
│   │
│   ├─ 1. Input Register         (latch Y, U, V)
│   ├─ 2. Angle Computation      (h_count >> h_shift + v_count >> v_shift + anim_phase)
│   │                             Direction: diagonal (add) or radial (XOR)
│   │                             Top 3 bits → 8-entry LUT index
│   ├─ 3. LUT Read + Scaling     (Y_LUT[idx] >> bright_shift)
│   │                             Pastel: Y offset × 1.5
│   ├─ 4. Y Adjust + Clamp       (Y + y_offset, clamped 0–1023)
│   ├─ 5. Output Register
│   └─ 6. Interpolator Mix       (4 clocks, dry/wet crossfade)
│
├── U/V Channels ──────────────────────────────────────────────
│   │
│   ├─ 1. Input Register         (latch U, V)
│   ├─ 2. Angle Computation      (shared with Y)
│   ├─ 3. LUT Read + Scaling     (U_LUT/V_LUT[idx] >> str_shift)
│   │                             Pastel: offsets halved
│   │                             Video Mod: scale by luma (Y>512 → /2, else → /8)
│   ├─ 4. Saturation Scale       (source chroma around 512 midpoint)
│   │     sat < 256: (ch-512)>>2 + 512
│   │     sat < 512: (ch-512)>>1 + 512
│   │     sat < 768: passthrough
│   │     sat ≥ 768: ch + (ch-512)>>1
│   ├─ 5. Add UV Offsets + Clamp  (clamped 0–1023)
│   ├─ 6. Output Register
│   └─ 7. Interpolator Mix       (4 clocks, dry/wet crossfade)
│
├── Sync Signals ──────────────────────────────────────────────
│   └─ 10-stage delay pipeline (hsync, vsync, field, Y/U/V for bypass)
│
└── Bypass ────────────────────────────────────────────────────
    └─ Select delayed original or mixed signal
```

The iridescence effect is built from one shared angle index that drives three parallel offset paths — U, V, and Y. Because the U and V LUT entries follow cosine and sine patterns respectively, the combined chroma offset traces a circle in chrominance space as the position index advances, producing a full hue rotation cycle every 8 LUT entries. The Y offset adds a subtle brightness shimmer whose phase is correlated but not identical to the chroma rotation, mimicking the way real thin-film surfaces show brightness variations alongside hue shifts.

The saturation control is applied to the *source* chroma before the iridescent offset is added. This means at low saturation, the source image is desaturated but the rainbow overlay remains at full strength — the iridescence becomes the dominant color. At high saturation, the source chroma is boosted and the rainbow competes with the original color content.

---

## Parameter Reference

<img src={nacre_control_panel} alt="Videomancer front panel with Nacre loaded"/>
*Videomancer's front panel with Nacre active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Band Sp
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

H Frequency controls the horizontal spacing of rainbow bands. The 10-bit pot value is mapped to a right-shift amount applied to the horizontal pixel counter: low values select a large shift (8 positions, dividing by 128), producing very wide bands that cross the frame slowly; high values select a small shift (1 position, dividing by 2), producing narrow bands packed tightly. Because the mapping uses 128-count threshold steps, there are 8 discrete frequency settings rather than a continuous sweep — the band spacing jumps between octaves as you turn the knob.

---

#### Knob 2 — Shimmer
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

V Frequency controls the vertical spacing by applying the same shift-based frequency mapping to the vertical line counter. Together with H Frequency, this determines the angle and spacing of the rainbow bands. Setting both to equal values produces 45° diagonal bands; setting one high and the other low produces nearly horizontal or vertical bands. Setting both very low produces broad, slowly-varying hue washes.

---

#### Knob 3 — Hue Speed
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Strength controls the amplitude of the U/V chrominance offsets by selecting a right-shift applied to the raw LUT values. At low pot values (shift 4, dividing by 16), the iridescence is barely visible — subtle tints over the source color. At high values (shift 1, dividing by 2), the offsets are at half the LUT magnitude (±64 counts), producing vivid, saturated rainbow bands that dominate the source chroma.

---

#### Knob 4 — Gradient
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Bright Mod controls the depth of the luma shimmer — the Y-channel modulation that adds pearlescent brightness variation. The pot selects a right-shift (6 at minimum, 2 at maximum) applied to the Y-offset LUT values. At low settings, the Y shimmer is nearly invisible. At high settings, brightness visibly undulates in sync with the hue bands, creating the illusion of curved or tilted reflective surfaces.

---

#### Knob 5 — Saturate
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Anim Speed sets the increment added to the DDS phase accumulator each frame. At zero, the rainbow pattern is static. As you increase the pot, the entire band pattern scrolls across the image — the hue cycle appears to flow like light moving across a nacre surface. Very high values produce rapid animation; because the accumulator wraps at 16 bits, the motion is seamless and periodic.

---

#### Knob 6 — Brightness
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Saturation scales the source chrominance around the 512 midpoint before the iridescent offset is applied. Below 256. chroma is strongly desaturated (shifted right by 2). Between 256 and 512, mildly desaturated (shifted right by 1). Between 512 and 768, unity passthrough. Above 768, chroma is boosted by 1.5× via shift-and-add. This lets you suppress or amplify the source color independently of the rainbow overlay, controlling how much the original hue shows through the iridescence.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Surface** | Nacre | Beetle |
| **8 — Direction** | Horiz | Diag |
| **9 — Anim** | Off | On |
| **10 — Video Mod** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles configure independent binary options. Direction and Pastel affect the character of the rainbow pattern — its spatial distribution and color intensity. Animate enables the DDS-driven scrolling. Video Mod links shimmer intensity to source brightness. Bypass is the standard signal bypass.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Mix controls the interpolator crossfade between the dry (original) and wet (processed) signals. At 0 the output is entirely dry; at 1023 entirely wet. The interpolator operates on all three channels (Y, U, V) independently with 4-clock latency.





---

## Guided Exercises

These exercises explore iridescence from broad color washes to intricate animated shimmer, progressively engaging more of the DSP chain.

### Exercise 1: Diagonal Rainbow Bands

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: nacre_source1_parrot, after: nacre_ex1_s1 },
    { label: "Cat", before: nacre_source2_cat, after: nacre_ex1_s2 },
    { label: "Elephant", before: nacre_source3_elephant, after: nacre_ex1_s3 },
    { label: "Pattern", before: nacre_source4_pattern, after: nacre_ex1_s4 },
    { label: "Boy", before: nacre_source5_boy, after: nacre_ex1_s5 },
    { label: "Wood", before: nacre_source6_wood, after: nacre_ex1_s6 },
  ]}
/>
*Diagonal Rainbow Bands — simulated result across source images.*
**Source**: A monochrome or desaturated camera feed — gray surfaces, concrete, skin, or fabric with subtle tonal variation.

**What You'll Create**: Create classic diagonal rainbow bands and learn how H Frequency and V Frequency interact to set band angle and spacing.

1. Start with both H Frequency and V Frequency at mid-position. Observe the diagonal band pattern crossing the image.
2. Turn H Frequency fully clockwise (high frequency). The horizontal band density increases — bands become narrow columns.
3. Return H Frequency to center; sweep V Frequency instead. Bands become narrow horizontal stripes.
4. Set both to matching moderate values. Observe the 45° diagonal pattern.
5. Increase Strength to make the bands more vivid. Note how the source gray tones receive overlaid color.

**Key concepts**: Shift-based frequency control has 8 discrete settings per axis, the 8-entry hue LUT produces repeating color cycles, diagonal mode adds H and V contributions

---

### Exercise 2: Animated Pearlescent Shimmer

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: nacre_source1_parrot, after: nacre_ex2_s1 },
    { label: "Cat", before: nacre_source2_cat, after: nacre_ex2_s2 },
    { label: "Elephant", before: nacre_source3_elephant, after: nacre_ex2_s3 },
    { label: "Pattern", before: nacre_source4_pattern, after: nacre_ex2_s4 },
    { label: "Boy", before: nacre_source5_boy, after: nacre_ex2_s5 },
    { label: "Wood", before: nacre_source6_wood, after: nacre_ex2_s6 },
  ]}
/>
*Animated Pearlescent Shimmer — simulated result across source images.*
**Source**: Smooth-toned footage with broad tonal gradations — clouds, water surfaces, flowing fabric.

**What You'll Create**: Combine animation, pastel mode, and luma-linked shimmer to simulate a mother-of-pearl surface.

1. Set moderate H and V Frequency for visible bands.
2. Enable Pastel — the rainbow softens to gentle tints with more visible brightness undulation.
3. Enable Animate; set Anim Speed to a low value (~20%). Watch the pattern drift across the image.
4. Enable Video Mod. Observe how the shimmer concentrates on bright areas and fades from shadows.
5. Increase Bright Mod to intensify the pearlescent brightness undulation.
6. Adjust Saturation to find the balance between source color and iridescent overlay.

**Key concepts**: Pastel mode trades chroma intensity for luma shimmer, Video Mod creates brightness-dependent iridescence, DDS animation scrolls the pattern seamlessly

---

### Exercise 3: Radial Diamond Iridescence

<BeforeAfterSlider
  sources={[
    { label: "Parrot", before: nacre_source1_parrot, after: nacre_ex3_s1 },
    { label: "Cat", before: nacre_source2_cat, after: nacre_ex3_s2 },
    { label: "Elephant", before: nacre_source3_elephant, after: nacre_ex3_s3 },
    { label: "Pattern", before: nacre_source4_pattern, after: nacre_ex3_s4 },
    { label: "Boy", before: nacre_source5_boy, after: nacre_ex3_s5 },
    { label: "Wood", before: nacre_source6_wood, after: nacre_ex3_s6 },
  ]}
/>
*Radial Diamond Iridescence — simulated result across source images.*
**Source**: A centered, high-contrast subject — a face, a flower, a circular object against a dark background.

**What You'll Create**: Use radial mode to create a non-linear iridescent pattern that wraps around the subject.

1. Enable Direction (radial mode). Observe how the parallel diagonal bands transform into intersecting diamond or checkerboard patterns.
2. Set H Frequency and V Frequency to different values. The diamond aspect ratio changes.
3. Increase Strength for vivid spectral diamonds.
4. Enable Animate and set moderate Anim Speed. The diamonds shift and shimmer.
5. Try full Saturation boost (above 75%) to see the original color compete with the iridescence.
6. Lower Mix to ~50% to blend the iridescent overlay with the clean source.

**Key concepts**: Radial mode XORs H and V contributions for a pseudo-radial pattern, saturation boost amplifies source chroma competition, mix blending controls effect intensity

---


## Tips

- **Pastel mode for realism**: Real nacre has soft, shifting tints — not vivid spectral bands. Pastel mode plus Video Mod produces the most naturalistic pearlescent look.
- **Animation speed is exponential**: Because the DDS accumulator adds the pot value every frame, the perceived animation rate grows linearly with the knob but wraps at 16-bit boundaries — keep speeds moderate for smooth scrolling.
- **Radial mode for complex patterns**: Direction mode switches from parallel bands to intersecting diamonds, doubling the visual complexity with a single toggle.
- **Layer with other programs**: Nacre's rainbow overlay is additive to source chroma. Running it after a desaturation or threshold program produces iridescent color on black-and-white structures.

---

## Glossary

| Term | Definition |
|------|------------|
| **BT.601** | ITU-R BT.601 standard defining the YUV color encoding used in the Videomancer video pipeline. |
| **Chrominance** | The color difference components (U and V) of a YUV signal, encoding hue and saturation. |
| **DDS** | Direct Digital Synthesis; a phase accumulator technique for generating periodic waveforms by adding a tuning word each cycle. |
| **Hue** | The angular position of the chrominance vector in the UV plane, determining the perceived color (red, green, blue, etc.). |
| **iCE40** | Lattice iCE40 HX4K FPGA used in Videomancer hardware. |
| **Luminance** | The brightness component (Y) of a YUV signal. |
| **LUT** | Lookup Table; pre-computed values stored in FPGA fabric, accessed by index for single-cycle retrieval. |
| **Nacre** | Mother-of-pearl; the iridescent inner lining of mollusc shells composed of layered aragonite crystals. |
| **Thin-Film Interference** | Optical phenomenon where light reflecting from two surfaces of a thin transparent layer produces position-dependent color. |

---
