---
draft: true
sidebar_position: 186
slug: /instruments/videomancer/ouroboros
title: "Ouroboros"
image: /img/instruments/videomancer/ouroboros/ouroboros_hero.png
description: "Program guide for Ouroboros, a Videomancer render program for the LZX video synthesizer."
---

import ouroboros_animation from '/img/instruments/videomancer/ouroboros/ouroboros_animation.gif';
import ouroboros_control_panel from '/img/instruments/videomancer/ouroboros/ouroboros_control_panel.png';
import ouroboros_exercise1_result from '/img/instruments/videomancer/ouroboros/ouroboros_exercise1_result.gif';
import ouroboros_exercise2_result from '/img/instruments/videomancer/ouroboros/ouroboros_exercise2_result.gif';
import ouroboros_exercise3_result from '/img/instruments/videomancer/ouroboros/ouroboros_exercise3_result.gif';
import ouroboros_hero from '/img/instruments/videomancer/ouroboros/ouroboros_hero.png';

# Ouroboros

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={ouroboros_hero} alt="Ouroboros hero image"/>
*A luminous serpent traces a self-consuming circular orbit — its tapering tail segments spiral inward through color-shifted hue bands while the head completes another revolution, rendering the ancient ouroboros symbol as real-time video synthesis.*
<img src={ouroboros_animation} alt="Ouroboros animated output"/>
*Ouroboros output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

The ouroboros — the serpent that devours its own tail — is one of humanity's oldest symbols, appearing across Egyptian, Greek, Norse, and alchemical traditions as a representation of eternal cyclic renewal. This program renders the symbol as a real-time FPGA video synthesis pattern. A DDS phase accumulator drives the serpent's head along a circular orbital path, with configurable tail segments trailing behind at decreasing phase offsets. The Curl control frequency-modulates the orbital angle, adding sinusoidal wobble to the otherwise circular path — transforming the ouroboros from a perfect ring into a writhing, organic form.

The pipeline operates in 8 clock cycles with zero BRAM usage. A 16-bit LFSR provides sparkle noise across the frame. The six working potentiometers control head size, tail length, path curvature, animation speed, overall scale, and body hue. The five toggles enable fractal repetition, position-cycled rainbow hue, edge glow, bilateral mirror symmetry, and bypass. The fader controls wet/dry mix.

A critical ABI boundary bug limits the program's full potential. The VHDL attempts to read registers 8 through 11 for secondary color, fractal recursion depth, glow intensity, and background color — but the Videomancer ABI only provides 8 registers (indices 0–7). Registers 8–11 always read zero, which means fractal depth is stuck at 0 (the Fractal toggle has no visible effect), glow intensity is zero (the Glow toggle produces only trace-level bloom), the secondary color is permanently black, and the background cannot be colored. These four phantom parameters are mapped in the VHDL but unreachable through the hardware interface.

---

## Background

### The Ouroboros in Art and Mathematics

The ouroboros appears in the Book of the Dead (c. 1600 BCE), in Plato's *Timaeus* as the first living creature, and in Norse mythology as Jörmungandr encircling the Earth. In mathematics, self-referential structures echo the ouroboros: Gödel's incompleteness theorems, Penrose's impossible triangle, and the recursive Mandelbrot set all feature systems that fold back upon themselves. The serpent pattern in this program — where enough tail segments form a complete ring whose tip meets the head — directly mirrors this self-consuming symbolism in geometry.

### DDS Phase Accumulation for Animation

Direct Digital Synthesis uses a phase accumulator — a register that increments by a configurable step each clock cycle, wrapping at overflow. The upper bits of the accumulator provide the instantaneous phase, which drives the serpent's angular position on its circular orbit. The accumulator step size (controlled by Speed) determines the orbital velocity: small steps produce slow, meditative orbits while large steps create rapid, hypnotic spinning. Because the accumulator wraps naturally at its bit width, the orbital motion is perfectly cyclic — the serpent's path never drifts or accumulates error.

### Fractal Tail Repetition and the ABI Boundary

The Fractal toggle enables recursive duplication of the tail at progressively smaller scales — each recursion level copies the entire tail chain at half size and rotates it around the parent segment. However, the recursion depth parameter is mapped to register 9, which falls outside the 8-register ABI boundary. The depth value is permanently zero, so the fractal toggle produces no visible recursive geometry. If the ABI were extended or the register mapping corrected, this feature would create increasingly intricate self-similar patterns — ouroboros within ouroboros.

### The 6-Segment Hue Wheel

Color is generated via a 6-segment hue wheel that maps a 10-bit register value to Y, U, V triplets using shift-and-add arithmetic. The six segments correspond approximately to red, yellow, green, cyan, blue, and magenta. Transitions between segments are abrupt — there is no interpolation across boundaries. When the Rainbow toggle is enabled, each tail segment receives a hue offset proportional to its position along the body, creating a spectrum of color that flows from head to tail.

### LFSR Sparkle

A 16-bit Linear Feedback Shift Register free-runs at pixel rate, producing a pseudo-random bit sequence. When the LFSR output exceeds a threshold, the pixel brightness receives a small additive boost, creating a subtle sparkle effect across the frame. The sparkle is most visible against the black background and adds organic texture to the otherwise mathematically pure serpentine path.


---

## Signal Flow

```
Frame Clock (per vsync)
│
├── DDS Phase Accumulator ──────────────────────────────
│   └─ phase += speed_step (wraps at 2^16)
│
Per-Pixel Pipeline (8 clocks)
│
├── Stage 1: Position Computation ──────────────────────
│   ├─ head_angle = phase + curl × sin(phase × curl_freq)
│   ├─ head_x = cx + orbit_r × cos(head_angle)
│   └─ head_y = cy + orbit_r × sin(head_angle)
│
├── Stage 2: Tail Segment Chain ────────────────────────
│   ├─ For each segment i (0..tail_len):
│   │   ├─ seg_phase = phase − i × segment_spacing
│   │   ├─ seg_angle = seg_phase + curl × sin(seg_phase × curl_freq)
│   │   └─ seg_pos = center + orbit_r × (cos, sin)(seg_angle)
│   └─ Pixel distance test: dist < head_size × taper(i)
│
├── Stage 3: Fractal Recursion ─────────────────────────
│   └─ [INOPERATIVE — fractal_depth from reg(9) = 0]
│
├── Stage 4: Hue Wheel + Rainbow ───────────────────────
│   ├─ base_hue → 6-segment wheel → Y/U/V
│   ├─ Rainbow on: hue offset += index × 80
│   └─ Brightness taper along body (head brightest)
│
├── Stage 5: LFSR Sparkle ─────────────────────────────
│   └─ lfsr16 → threshold → additive luma boost
│
├── Stage 6: Bilateral Mirror ─────────────────────────
│   └─ Mirror on: right half = flipped left half
│
├── Stage 7: Glow ─────────────────────────────────────
│   └─ [NEAR-INOPERATIVE — glow_amount from reg(10) = 0]
│
├── Stage 8: Output Mux ───────────────────────────────
│   ├─ Bypass off: lerp(black, serpent, mix)
│   └─ Bypass on: black output (synthesis program)
│
└── Background: always black (reg(11) = 0)
```

The pipeline generates all imagery from scratch — no input video is used as source material. The DDS phase accumulator runs continuously, wrapping at its bit width to produce a perfectly cyclic orbital path. The Curl parameter applies frequency modulation to the orbital angle, creating sinusoidal deviations from circularity that make the serpent's path more organic. When Tail Len is set high enough that the total tail arc approaches $2\pi$ radians, the tail visually meets the head, completing the ouroboros circle.

The most significant architectural limitation is the ABI register boundary. Four intended parameters (Color B on register 8, Fractal Depth on register 9, Glow amount on register 10, Background on register 11) are mapped in the VHDL but fall outside the 8-register hardware interface. These always read zero: the Fractal toggle has no visible effect (recursion depth = 0), the Glow toggle produces only trace-level bloom (glow intensity = 0), the secondary color is always black, and the background is permanently black.

---

## Parameter Reference

<img src={ouroboros_control_panel} alt="Videomancer front panel with Ouroboros loaded"/>
*Videomancer's front panel with Ouroboros active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Frequency 1
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Head Size sets the radius of the serpent's head circle and proportionally scales the diameter of all tail segments. At low values (0–200), the head is a small point and the tail segments are barely visible — useful for fine, threadlike orbits. At mid values (400–600), the serpent has a clearly defined body thickness. At high values (800–1023), the head becomes a large disk and overlapping tail segments create a broad, ribbon-like trail. The head size directly affects visual density — larger heads at high tail counts can fill significant portions of the frame.

---

#### Knob 2 — Frequency 2
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Tail Len controls the number of segments trailing behind the head. At minimum (0), only the head is visible as a lone orbiting circle. As the value increases, segments are added at progressively earlier phase offsets along the orbital path. At maximum (1023), approximately 32 segments trace nearly the full circumference of the orbit, creating the complete ouroboros ring. Each segment is drawn at decreasing size (tapered from head to tail tip) and with decreasing brightness, giving the body a natural sense of depth and direction.

---

#### Knob 3 — Frequency 3
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Curl applies frequency modulation to the orbital angle, bending the serpent's circular path into a wobbling, sinusoidal trajectory. At zero, the orbit is a perfect circle. As Curl increases, the orbital angle receives a sinusoidal offset: `angle = phase + curl × sin(phase × curl_freq)`. At moderate values, the orbit develops a gentle serpentine wobble. At high values, the path becomes increasingly complex and self-intersecting, creating elaborate knot-like patterns where the body crosses over itself.

---

#### Knob 4 — Freq Mod 1
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Speed controls the DDS phase increment per frame, determining how fast the serpent's head orbits. At zero, the serpent is frozen in place. At low values (100–300), the head drifts slowly — meditative and contemplative. At mid values, the orbit is clearly animated. At maximum (1023), the head completes full revolutions rapidly, and with long tails the entire ouroboros pattern rotates as a unit. Speed interacts strongly with Curl: high speed with high curl produces rapid, chaotic trajectory changes, while low speed with high curl creates slow, serpentine undulations.

---

#### Knob 5 — Freq Mod 2
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Scale sets the radius of the orbital path, determining how much of the frame the serpent occupies. At minimum, the orbit is a tight circle near the center. At maximum, the orbit extends nearly to the frame edges. Scale does not affect segment size (that is Head Size) — it controls the diameter of the path itself. Small scale with large head size creates a dense central disk; large scale with small head size creates a wide, thin ring.

---

#### Knob 6 — Freq Mod 3
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Hue selects the base color from a 6-segment hue wheel. The 10-bit register is divided into six zones: red (0–170), yellow (171–341), green (342–512), cyan (513–682), blue (683–853), and magenta (854–1023). Transitions between zones are abrupt — sweeping the knob produces hard color jumps. The secondary color (Color B, register 8) is permanently black due to the ABI boundary bug, so the serpent is always monochromatic unless the Rainbow toggle is enabled.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Range 1** | Horizontal | Vertical |
| **8 — Range 2** | Horizontal | Vertical |
| **9 — Range 3** | Horizontal | Vertical |
| **10 — Pattern** | 1 > 2 > 3 | 1 > 2 & 3 |
| **11 — Waveshape** | Triangle | Sine |

The five toggles control fractal recursion, rainbow coloring, glow bloom, bilateral mirror, and bypass. Two of these — Fractal and Glow — are functionally impaired by the ABI register boundary bug. Their toggle bits are read correctly from register 6, but the associated intensity and depth parameters on registers 9 and 10 are always zero. Fractal has no visible effect. Glow produces only trace-level bloom. Mirror and Rainbow work fully as intended. Bypass outputs a black frame.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Luma Mod
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Mix crossfades between black (dry) and the fully rendered serpent pattern (wet). At 0% the output is solid black. At 100% the full serpent pattern is output at maximum brightness. Intermediate values produce a proportionally dimmed serpent — useful for subtle overlay when chaining with other programs. Chrominance scales proportionally: at 50% mix, U and V are halfway between neutral 512 and their computed hue values.

---

## Guided Exercises

These exercises explore the ouroboros from a simple orbiting circle through complex serpentine forms, working within the ABI-limited parameter space.

### Exercise 1: The Simple Orbit

<img src={ouroboros_exercise1_result} alt="The Simple Orbit result"/>
*The Simple Orbit — simulated result across source images.*
**Objective**: Create a single glowing circle orbiting the center of the frame to understand the DDS animation engine.

1. **Single head**: Set Tail Len to 0%. Only the head circle is visible.
2. **Moderate size**: Set Head Size to ~50%. A clearly visible circle.
3. **Slow orbit**: Set Speed to ~20%. Gentle, meditative motion.
4. **Wide path**: Set Scale to ~60%. The circle orbits at a comfortable radius.
5. **No curl**: Set Curl to 0%. A perfectly circular orbit.
6. **Pick a color**: Set Hue to ~30% for yellow-green.
7. **Observe**: A single colored circle orbits the center on a circular path against a black background.

**Key concepts**: DDS phase accumulator produces cyclic motion, head size determines visual weight, scale controls orbit diameter

---

### Exercise 2: The Complete Ouroboros

<img src={ouroboros_exercise2_result} alt="The Complete Ouroboros result"/>
*The Complete Ouroboros — simulated result across source images.*
**Objective**: Build a full serpent ring that visually consumes its own tail.

1. **Full tail**: Set Tail Len to ~95%. Maximum segments.
2. **Medium head**: Head Size at ~40%.
3. **Moderate orbit**: Scale at ~50%.
4. **Add curl**: Set Curl to ~30%. The circular path wobbles sinusoidally.
5. **Enable Rainbow**: Toggle Rainbow on. Each segment gets a different hue.
6. **Slow speed**: Speed at ~15%.
7. **Observe**: A complete ring of colored segments traces a wobbling circular path. The tail meets the head, completing the ouroboros. Rainbow coloring makes individual segments distinguishable.

**Key concepts**: Full tail length completes the ouroboros ring, curl adds organic wobble, rainbow reveals individual segment positions along the body

---

### Exercise 3: Mirror Mandala

<img src={ouroboros_exercise3_result} alt="Mirror Mandala result"/>
*Mirror Mandala — simulated result across source images.*
**Objective**: Use bilateral mirror with high curl to create symmetrical serpentine mandala patterns.

1. **Enable mirror**: Toggle Mirror on.
2. **High curl**: Set Curl to ~80%. Complex curved trajectories.
3. **Many segments**: Tail Len at ~85%.
4. **Small head**: Head Size at ~25%. Fine detail.
5. **Medium speed**: Speed at ~30%.
6. **Tight orbit**: Scale at ~35%. Keep the pattern centered.
7. **Rainbow on**: Toggle Rainbow on for color variation.
8. **Observe**: The mirror doubles the serpent into a symmetrical mandala pattern. High curl creates self-intersecting paths. The pattern evolves continuously as the head orbits.

**Key concepts**: Mirror creates bilateral symmetry, high curl produces complex self-intersecting paths, centered orbits generate mandala-like forms

---


## Tips

- **Fractal and Glow toggles are non-functional**: Due to the ABI register boundary bug, Fractal and Glow have no visible effect. Focus on the six working potentiometers, Rainbow, and Mirror for creative control.
- **Full tail = ouroboros**: Set Tail Len above 90% to create a complete ring where the tail meets the head — the iconic self-consuming form.
- **Curl creates organic motion**: Even small amounts (15–25%) transform the rigid circular orbit into a living, breathing path.
- **Rainbow + full tail = stained glass**: The 6-segment hue wheel's abrupt transitions produce banded color along the body, reminiscent of stained glass or film leader countdown strips.
- **Mirror for mandalas**: The Mirror toggle with centered, curled orbits produces symmetrical mandala patterns that evolve continuously.
- **Speed and Curl interact nonlinearly**: High Curl at low Speed produces slow, graceful undulations. High Curl at high Speed produces rapid, chaotic movement.
- **Background is always black**: Register 11 (Background) is unreachable, so the background is permanently black. Use Mix below 100% to dim the serpent for downstream compositing.
- **Scale below 20% collapses the pattern**: Very small Scale values compress the orbit to a few pixels. Keep Scale above 25% for clear visibility.

---

## Glossary

| Term | Definition |
|------|------------|
| **ABI** | Application Binary Interface; the fixed register layout through which the Videomancer firmware communicates parameter values to FPGA programs. Limited to 8 registers (indices 0–7). |
| **DDS** | Direct Digital Synthesis; a technique using a phase accumulator to generate periodic waveforms. The accumulator wraps at its bit width, producing inherently cyclic output. |
| **Fractal** | A mathematical pattern exhibiting self-similarity at progressively smaller scales. In Ouroboros, the intended fractal tail repetition is inoperative due to the ABI boundary bug. |
| **Hue wheel** | A circular color map divided into discrete segments. Ouroboros uses a 6-segment wheel (red, yellow, green, cyan, blue, magenta) with abrupt zone transitions. |
| **LFSR** | Linear Feedback Shift Register; a pseudo-random number generator used here for sparkle noise injection across the frame. |
| **Ouroboros** | An ancient symbol depicting a serpent or dragon consuming its own tail, representing cyclical renewal, eternity, and self-reference. |
| **Phase accumulator** | A register that increments by a fixed step each clock cycle and wraps at overflow, producing a sawtooth waveform whose frequency is proportional to the step size. |
| **YUV** | A color encoding separating luminance (Y) from chrominance (U, V), used as the native signal format in Videomancer. |
