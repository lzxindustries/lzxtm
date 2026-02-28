---
draft: true
sidebar_position: 58
slug: /instruments/videomancer/corona
title: "Corona"
image: /img/instruments/videomancer/corona/corona_hero.png
description: "Corona synthesizes the radial streamer field of a total solar eclipse — the ethereal halo of plasma that becomes visible only when the Moon's disk occul..."
---

import corona_hero from '/img/instruments/videomancer/corona/corona_hero.png';
import corona_before_after from '/img/instruments/videomancer/corona/corona_before_after.png';
import corona_control_panel from '/img/instruments/videomancer/corona/corona_control_panel.png';
import corona_exercise1_result from '/img/instruments/videomancer/corona/corona_exercise1_result.png';
import corona_exercise2_result from '/img/instruments/videomancer/corona/corona_exercise2_result.png';
import corona_exercise3_result from '/img/instruments/videomancer/corona/corona_exercise3_result.png';

# Corona

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={corona_hero} alt="Corona hero image"/>
*A radiant solar corona erupts from behind a dark lunar disk, pearl-white streamers fanning outward through amber into blue-green at the limb, the asymmetric lobe structure drifting slowly as three phase accumulators evolve the coronal field.*
<img src={corona_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Corona applied.*

---

## Overview

Corona synthesizes the radial streamer field of a total solar eclipse — the ethereal halo of plasma that becomes visible only when the Moon's disk occults the Sun's photosphere. A multi-frequency angular lobe function generates the asymmetric petal structure characteristic of the real solar corona, while an inverse-distance radial falloff attenuates the streamers from brilliant inner white to faint outer glow. A configurable dark disk masks the center to simulate the lunar silhouette, and an optional prominence ring adds a bright edge at the disk boundary.

The name refers to the Latin *corona* ("crown"), the term astronomers use for the Sun's outer atmosphere. During totality, the corona's appearance ranges from a compact symmetric halo near solar minimum to a wildly asymmetric structure with long equatorial streamers and short polar brushes near solar maximum. Corona's three-harmonic lobe function captures this variability: the Streamers knob selects the base angular frequency (2–16 lobes), while the Asymmetry knob weights a third harmonic that breaks the pattern's rotational symmetry. Three phase accumulators drift at different rates controlled by the Rotation knob, ensuring the coronal structure evolves continuously rather than remaining static.

The full dynamic range spans from a tight, symmetric two-lobe dipole resembling a solar-minimum corona to a complex sixteen-lobe sunflower pattern that fills the screen with interlocking radial spokes. Butler color mode applies a distance-dependent palette inspired by Howard Russell Butler's eclipse paintings — pearl-white near the disk transitioning through amber to blue-green at the outer limb — while monochrome mode lets the user sweep a single hue across the entire structure.

---

## Background

### Solar Physics and Coronal Structure

The solar corona is a magnetically structured plasma extending millions of kilometers from the Sun's surface. Its temperature exceeds one million kelvin — paradoxically hotter than the photosphere below — and its shape is governed by the Sun's magnetic field topology. During solar minimum, the corona is dominated by a simple dipole field with two equatorial streamers extending outward like wings. During solar maximum, the field becomes complex and multipolar, producing streamers at many latitudes. Corona's variable-frequency lobe function models this transition: low Streamers counts produce the dipole geometry of a quiet Sun, while high counts create the complex multi-streamer patterns of an active Sun.

### Radial Streamers and the K-Corona

Eclipse observers distinguish several components of the corona by their emission mechanisms. The K-corona (from German *Kontinuierlich*, continuous) is produced by Thomson scattering of photospheric light off free electrons in the coronal plasma. It dominates the inner corona and produces the bright, structured streamers that give each eclipse its unique visual fingerprint. The intensity of the K-corona falls off approximately as the inverse of the radial distance from the solar limb — a relationship that Corona's pipeline implements via a shift-based approximation of 1/r, multiplied by the angular lobe function to sculpt the streamer geometry.

### Coronagraph History and Artificial Eclipses

Before Bernard Lyot invented the coronagraph in 1930, the corona could only be studied during the few minutes of totality in a natural eclipse. Lyot's instrument used an internal occulting disk to block the photosphere, combined with careful baffling to suppress scattered light, creating an artificial eclipse inside the telescope. Corona's Eclipse toggle mirrors this concept: when set to Disk mode, a dark circular mask occludes the center of the streamer field, revealing only the surrounding corona. When set to NoDisk, the full radial pattern is visible without occlusion — an idealized view that no real instrument can achieve because the photosphere is a million times brighter than the corona.

### Butler Color Map and Eclipse Art

Howard Russell Butler (1856–1934) was an American painter who attended five total solar eclipses between 1918 and 1932, producing large oil paintings commissioned by the American Museum of Natural History. Working from memory notes made during the brief minutes of totality (photography of the era could not capture the corona's full dynamic range), Butler rendered the inner corona in pearl-white and warm amber, transitioning to blue-green and violet at the outer limb. His palette became the canonical artistic representation of coronal color. Corona's Butler color mode implements this gradient using a three-zone distance mapping: inner pixels are warm (high Y, near-neutral UV), mid-range pixels blend warm and cool, and outer pixels shift toward blue-green (lower Y, elevated U, reduced V).

### Lissajous Figures and Center Drift

The optional center drift uses a Lissajous figure — the trajectory produced by two sinusoidal oscillations at incommensurable frequencies. Named after Jules Antoine Lissajous (1822–1880), these figures produce closed loops when the frequency ratio is rational and space-filling curves when it is irrational. Corona uses phase increments of 73 and 97 (both prime) per vsync, producing a slowly evolving quasi-periodic orbit that prevents the corona from settling into a fixed position. The drift amplitude is determined by the sine LUT's 8-bit range (±127 pixels from center), creating a gentle wandering motion that adds organic life to the radial structure.


---

## Signal Flow

```
Video Input (YUV 4:4:4)
│
├── Register Decode ────────────────────────────────────────────
│   ├─ rotation     = registers_in(0) → s_rotation (phase drift speed)
│   ├─ streamers    = registers_in(1) → s_streamer_sel → s_freq_main (2..12)
│   ├─ asymmetry    = registers_in(2) → s_asymmetry (3rd harmonic weight)
│   ├─ disk_size    = registers_in(3) → s_disk_size (occluding radius)
│   ├─ brightness   = registers_in(4) → s_brightness (corona intensity)
│   ├─ color        = registers_in(5) → s_corona_color (monochrome hue)
│   └─ toggles: eclipse, prominences, center_drift, butler_color, bypass
│       mix_amount  = registers_in(7)
│
├── Position Counters ──────────────────────────────────────────
│   └─ hsync/vsync edge detection → s_h_count, s_v_count
│
├── Phase Drift + Lissajous Center (per vsync) ─────────────────
│   ├─ s_phase0 += rotation
│   ├─ s_phase1 += rotation×0.625
│   ├─ s_phase2 += rotation×0.3125
│   └─ Lissajous: phase_x += 73, phase_y += 97
│       center = (640,360) + SIN_LUT(phase) − 128
│
├── Clock 1: Position Delta + Octant Classify ──────────────────
│   ├─ dx = h_count − center_x, dy = v_count − center_y
│   ├─ Octant: 3-bit classify from sign(dx,dy) + |dx|≥|dy|
│   ├─ Fraction: 8-bit atan2 approximation within octant
│   ├─ s_angle = octant || fraction (11-bit)
│   └─ s_distance = max(|dx|,|dy|) + |min|/2 − |min|/8
│
├── Clock 2: 3-Frequency Lobe Function ─────────────────────────
│   ├─ θ₁ = angle × freq_main + phase0
│   ├─ θ₂ = angle × (freq_main+3) + phase1
│   ├─ θ₃ = angle × (freq_main+6) + phase2
│   ├─ sin1 = SIN_LUT[θ₁], sin2 = SIN_LUT[θ₂], sin3 = SIN_LUT[θ₃]
│   ├─ lobe = sin1 + sin2/2 + (sin3 × asymmetry) >> 10
│   └─ s_lobe_length = clamp(lobe, 0..1023)
│
├── Clock 3: Radial Falloff × Lobe + Disk Mask ────────────────
│   ├─ disk_r = disk_size/2 + disk_size/8
│   ├─ inv_dist ≈ 640×1023 / distance (shift approx)
│   ├─ masked = (inv_dist × lobe_length) >> 10
│   ├─ Disk mask: if eclipse='Disk' AND dist < disk_r → 0
│   │   └─ Prominences: if dist in [disk_r−8, disk_r] → 800
│   └─ s_corona_val = clamp((masked + prom) × brightness >> 10)
│
├── Clock 4: Color Mapping ─────────────────────────────────────
│   ├─ Butler mode (distance zones):
│   │   ├─ dist < 200: inner=900, outer=100
│   │   ├─ dist < 400: inner=500, outer=500
│   │   └─ dist ≥ 400: inner=200, outer=800
│   │   Y = corona_val
│   │   U = 490 + outer×40/1024, V = 520 − outer×30/1024
│   └─ Mono mode: Y = corona_val
│       U = 512 + (color−512)/4, V = 512 − (color−512)/8
│
├── Clock 5: Additive Composite ────────────────────────────────
│   ├─ Y = clamp(input_Y + corona_Y, 0..1023)
│   └─ U,V = input + (corona − input) × corona_val / 1024
│
├── Clocks 6–9: Interpolator (wet/dry Mix) ─────────────────────
│   └─ lerp(dry, wet, mix_amount) ×3 channels (4 clocks)
│
├── Sync Delay Pipeline (9 clocks) ─────────────────────────────
│   └─ hsync, vsync, field, Y, U, V delayed to match
│
└── Bypass Mux ─────────────────────────────────────────────────
    └─ Select delayed source or processed signal
```

The computational core of Corona is the per-pixel angular lobe evaluation in Clock 2 combined with the radial falloff multiplication in Clock 3. The three sine harmonics at frequencies N, N+3, and N+6 (where N is the Streamers setting) produce interference patterns that break the simple rotational symmetry of a single-frequency sinusoid. The Asymmetry knob controls only the amplitude of the third harmonic — the first two harmonics are fixed at full and half amplitude respectively — so at zero Asymmetry the lobe pattern is determined by just two frequencies, while at maximum Asymmetry the third frequency creates deep notches and sharp peaks in the radial streamer field. The three phase accumulators drift at rates proportional to the Rotation setting but at different multipliers (1.0, 0.625, 0.3125), ensuring that the three harmonic components evolve at incommensurable rates and the corona never exactly repeats.

---

## Parameter Reference

<img src={corona_control_panel} alt="Videomancer front panel with Corona loaded"/>
*Videomancer's front panel with Corona active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Rotation
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the rate at which the three phase accumulators advance per frame, determining how quickly the corona's streamer pattern rotates and evolves. At zero, the corona is completely frozen — a static radial pattern with no animation. At low values, the streamers drift almost imperceptibly, shifting over tens of seconds in the slow, majestic rotation of a real coronal structure. At high values the pattern spins rapidly, the three harmonics visibly sliding past each other and creating dynamic moiré-like interference as the lobe function reshapes itself frame by frame.

---

#### Knob 2 — Streamers
| Property | Value |
|----------|-------|
| Range | 2 – 16 |
| Default | 9 |

Selects the base angular frequency of the streamer lobe function, quantized to eight steps mapping to 2, 3, 4, 5, 6, 8, 10, and 12 lobes. Low values produce broad, sweeping streamer fans reminiscent of a solar-minimum dipole corona. High values create dense, fine-toothed radial spokes that subdivide the full 360° into narrow sectors. The second and third harmonics are automatically offset by +3 and +6 from the base frequency, so even a 2-lobe base setting actually produces a multi-frequency pattern with components at 2, 5, and 8 — the simplest setting is already richer than a pure sinusoid.

---

#### Knob 3 — Asymmetry
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Weights the amplitude of the third harmonic in the lobe sum. At zero, only the first two harmonics contribute (full-amplitude base frequency plus half-amplitude second frequency), producing a relatively smooth, gently modulated streamer field. As Asymmetry increases, the third harmonic grows in strength, introducing sharp angular peaks and deep valleys that break the pattern's bilateral symmetry. At maximum, the third harmonic dominates and the corona develops pronounced directional streamers separated by dark angular gaps — the complex, asymmetric geometry characteristic of a magnetically active Sun near solar maximum.

---

#### Knob 4 — Disk Size
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 29.3% |
| Suffix | % |

Sets the radius of the central occluding disk that simulates the lunar silhouette during a total eclipse. The disk radius is computed as half the register value plus one-eighth, providing a range from a tiny central dot to a large circle that fills much of the frame. At small sizes, the disk is a compact dark nucleus surrounded by an expansive corona. At large sizes, the disk swallows most of the inner corona, leaving only the outermost streamers visible at the frame edges — the view from an eclipse where the Moon appears larger than the Sun. This parameter has no effect when Eclipse is set to NoDisk.

---

#### Knob 5 — Brightness
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 68.4% |
| Suffix | % |

Scales the overall intensity of the corona after the radial falloff and lobe function have been computed. The corona value is multiplied by this register, so at zero the corona is invisible regardless of other settings. At moderate values the corona has a natural luminance rolloff from inner brightness to outer dimness. At maximum the entire streamer field is driven bright, washing out the radial falloff gradient and producing a more uniformly luminous disc. This parameter interacts multiplicatively with the radial distance falloff — even at maximum brightness, distant pixels remain dimmer than inner pixels due to the 1/r attenuation.

---

#### Knob 6 — Color
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 106° |
| Suffix | ° |

In monochrome mode, sweeps the corona's chrominance across the hue wheel. The register value drives both U and V offsets symmetrically from the neutral point (512): U shifts by one-quarter of the deviation and V by one-eighth in the opposite direction, producing a gentle color rotation from warm amber through blue-green. In Butler mode this parameter has no effect — the color is entirely determined by the distance-based inner/outer palette. At the default value of 300 the monochrome corona renders in a warm amber tone; sweeping toward 0 shifts cooler, and toward 1023 shifts warmer.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Eclipse** | Disk | NoDisk |
| **8 — Promin.** | Off | On |
| **9 — CtrLock** | Center | Drift |
| **10 — ColorMode** | Mono | Butler |
| **11 — Bypass** | Off | On |

The five toggles partition into four functional groups. Eclipse (7) and Prominences (8) control the disk masking — Eclipse enables or disables the central occluding disk, while Prominences adds a bright ring at the disk edge when the disk is visible. CtrLock (9) enables or disables the Lissajous center drift. ColorMode (10) switches between the user-controlled monochrome palette and the historically accurate Butler distance gradient. Bypass (11) is the standard signal bypass. Eclipse and Prominences interact: prominences are only visible when the disk is present, since the bright ring is drawn at the disk boundary.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade at the final pipeline stage. At maximum (default), the output is the fully processed corona composite. At minimum, the output is the unprocessed input video delayed by the 9-clock pipeline. Since Corona is a synthesis program, the dry signal is typically black — pulling Mix to zero fades the corona to darkness. Intermediate values produce a dimmed corona useful for subtle background glow effects behind other video content.

---

## Guided Exercises

These exercises progress from basic corona construction through eclipse composition to animated drift and Butler color mapping, revealing how the multi-frequency lobe function, disk masking, and color modes interact to produce a range of astronomical and abstract radial structures.

### Exercise 1: Symmetric Dipole Corona

<img src={corona_exercise1_result} alt="Symmetric Dipole Corona result"/>
*Symmetric Dipole Corona — simulated result across source images.*
**Objective**: Create a simple two-lobed coronal structure resembling a solar-minimum dipole, with a central dark disk and prominence ring.

1. Set Streamers to the lowest position (2 lobes) for a simple dipole.
2. Set Asymmetry to 0% — only the first two harmonics contribute, producing a smooth bilateral pattern.
3. Set Disk Size to about 30% for a moderate occluding disk.
4. Enable Eclipse in Disk mode and toggle Prominences On to see the bright limb ring.
5. Set Brightness to about 70% and observe the radial falloff from inner glow to outer dimness.
6. Set Rotation to about 10% and watch the dipole slowly rotate.

**Key concepts**: Low Streamers counts produce broad, sweeping lobes characteristic of a quiet Sun, the two fixed harmonics (N and N+3) create gentle modulation even without the asymmetry harmonic, the prominence ring decorates only the disk boundary, and slow rotation reveals the smooth phase evolution.

---

### Exercise 2: Complex Multi-Streamer with Butler Palette

<img src={corona_exercise2_result} alt="Complex Multi-Streamer with Butler Palette result"/>
*Complex Multi-Streamer with Butler Palette — simulated result across source images.*
**Objective**: Build a complex, asymmetric corona with many radial streamers and the historically accurate Butler color gradient.

1. Set Streamers to about 75% (10 or 12 lobes) for a dense radial pattern.
2. Increase Asymmetry to about 70% — the third harmonic creates sharp angular peaks and deep notches.
3. Set Disk Size to about 40% for a substantial occluding disk.
4. Switch ColorMode to Butler — observe the pearl-white inner corona transitioning to blue-green at the outer limb.
5. Set Brightness to about 80% and Rotation to about 25%.
6. Compare Butler mode to Mono mode by toggling ColorMode back and forth.

**Key concepts**: High Streamers counts with strong Asymmetry create the complex multi-streamer geometry of an active Sun near solar maximum, the Butler palette applies distance-dependent color zones matching Howard Russell Butler's eclipse paintings, and the three drifting phase accumulators ensure the dense pattern evolves without repetition.

---

### Exercise 3: Drifting Starburst without Disk

<img src={corona_exercise3_result} alt="Drifting Starburst without Disk result"/>
*Drifting Starburst without Disk — simulated result across source images.*
**Objective**: Use center drift and NoDisk mode to create an animated starburst that wanders across the screen.

1. Set Eclipse to NoDisk to remove the occluding disk entirely.
2. Set CtrLock to Drift — the corona's center begins a slow Lissajous orbit.
3. Set Streamers to about 50% (6 or 8 lobes) and Asymmetry to about 50%.
4. Set Rotation to about 40% for visible angular evolution.
5. Set Brightness to about 60% — moderate intensity lets the radial falloff create a natural glow.
6. Observe how the wandering center causes the streamer pattern to sweep across the frame, creating dynamic composition changes.

**Key concepts**: NoDisk mode reveals the full radial pattern including the bright central peak, center drift produces organic motion via incommensurable Lissajous frequencies (73 and 97), the combination of angular rotation and spatial drift creates complex apparent motion, and moderate Asymmetry balances regularity with visual interest.

---


## Tips

- **Low Streamers for elegance**: A 2- or 3-lobe setting produces broad, sweeping fans that read clearly even at small screen sizes. Reserve high lobe counts for dense, textural patterns.
- **Asymmetry for realism**: Real solar coronas are never perfectly symmetric. Even a small amount of Asymmetry (20–30%) introduces the angular irregularity that makes the pattern feel natural rather than geometric.
- **Butler mode for astronomy**: When simulating a realistic eclipse, use Butler color mode with Prominences enabled and a disk size that matches the apparent lunar diameter — the result closely matches photographic references of totality.
- **Rotation near zero for prints**: Set Rotation to 0% to freeze the corona in a static state suitable for still image capture or slow-scanning video synthesis where frame-to-frame coherence matters.
- **Brightness and radial falloff interact**: High Brightness compresses the dynamic range of the radial falloff — the difference between inner and outer corona diminishes. For maximum depth, use moderate Brightness (50–70%) to preserve the natural 1/r luminance gradient.
- **Mix for layered compositions**: Pull Mix to 40–60% to use the corona as a translucent glow layer behind other video content, creating a celestial backdrop effect.
- **Center drift for installations**: Enable Drift for long-running installations where a static centered corona would feel lifeless. The Lissajous motion is subtle enough to go unnoticed on short time scales but prevents the eye from habituating to a fixed position.
- **NoDisk for abstract starburst**: Removing the occluding disk transforms the eclipse into a radial starburst pattern — useful as a graphic element, transition wipe, or animated texture that has no astronomical pretension.

---

## Glossary

| Term | Definition |
|------|------------|
| **Butler palette** | A distance-dependent color gradient inspired by the eclipse paintings of Howard Russell Butler (1856–1934), transitioning from pearl-white at the inner corona through amber to blue-green at the outer limb. |
| **Coronagraph** | An instrument that creates an artificial eclipse by blocking the solar disk with an internal occulting element, allowing observation of the corona without waiting for a natural total solar eclipse. |
| **DDS** | Direct Digital Synthesis; a technique for generating waveforms by incrementing a phase accumulator and using the result to index a lookup table. |
| **Dipole** | A two-pole magnetic field configuration; during solar minimum, the Sun's corona is dominated by a dipole field with two broad equatorial streamers. |
| **K-corona** | The component of the solar corona produced by Thomson scattering of photospheric light off free electrons, responsible for the bright structured streamers visible during totality. |
| **Lissajous figure** | The trajectory produced by two sinusoidal oscillations at different frequencies; used here to drive the corona's center drift in an evolving quasi-periodic orbit. |
| **Lobe function** | The angular modulation applied to the radial streamer field, computed as a weighted sum of three sine harmonics at frequencies N, N+3, and N+6. |
| **Octant** | One of eight 45° sectors used to classify pixel positions for the integer atan2 approximation; the 3-bit octant combined with an 8-bit fraction yields an 11-bit angle. |
| **Prominence** | A loop of ionized gas arcing above the solar chromosphere, visible as a bright feature at the limb during totality; simulated by a narrow bright ring at the disk boundary. |
| **Radial falloff** | The inverse-distance attenuation that dims the corona with increasing distance from the center, approximating the 1/r intensity profile of the real K-corona. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V); the native format of Videomancer's 30-bit video pipeline. |

---
