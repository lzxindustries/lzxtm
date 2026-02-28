---
draft: true
sidebar_position: 196
slug: /instruments/videomancer/petrichor
title: "Petrichor"
image: /img/instruments/videomancer/petrichor/petrichor_hero.png
---

import petrichor_before_after from '/img/instruments/videomancer/petrichor/petrichor_before_after.png';
import petrichor_control_panel from '/img/instruments/videomancer/petrichor/petrichor_control_panel.png';
import petrichor_exercise1_result from '/img/instruments/videomancer/petrichor/petrichor_exercise1_result.png';
import petrichor_exercise2_result from '/img/instruments/videomancer/petrichor/petrichor_exercise2_result.png';
import petrichor_exercise3_result from '/img/instruments/videomancer/petrichor/petrichor_exercise3_result.png';
import petrichor_hero from '/img/instruments/videomancer/petrichor/petrichor_hero.png';
import petrichor_source1_kodim01 from '/img/instruments/videomancer/petrichor/petrichor_source1_kodim01.png';
import petrichor_source2_kodim02 from '/img/instruments/videomancer/petrichor/petrichor_source2_kodim02.png';
import petrichor_source3_stream_bridge_512 from '/img/instruments/videomancer/petrichor/petrichor_source3_stream_bridge_512.png';

# Petrichor

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={petrichor_hero} alt="Petrichor hero image"/>
*Petrichor splitting the frame at the horizon to produce rain-slicked pavement reflections, atmospheric haze, and animated rain streaks over a cityscape.*
<img src={petrichor_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Petrichor applied.*

---

## Overview

Video monitors show flat images. Rain turns the real world into a hall of mirrors — every wet surface doubles the scene, stretched and dimmed by viewing angle. Petrichor brings that optical phenomenon into the Videomancer signal chain as a real-time spatial processor.

The program divides the frame at a movable horizon line. Above the horizon, the image receives atmospheric haze and animated rain streaks. Below the horizon, a vertically-flipped, attenuated, blue-tinted copy of recently buffered scanlines simulates the reflection you would see in rain-slicked pavement. A 16-line BRAM ring buffer stores Y-channel scanlines for reflection readback: the buffer captures what passes above the horizon and replays it inverted below. The name comes from *petrichor* — the earthy scent produced when rain falls on dry soil — evoking the sensory experience of a sudden downpour transforming an everyday scene.

At subtle settings, Petrichor adds a gentle wet sheen and faint atmospheric depth. Pushed harder, it creates dramatic split-screen reflections, dense fog, and visible rain lines that animate across the frame. The six knobs, four toggles, and mix fader give continuous control over every aspect of the rain simulation.

---

## Background

### Wet-Surface Reflections

When rain coats a flat surface — pavement, a car hood, a tabletop — the thin water layer acts as a specular mirror. The reflection is not a perfect copy: it is dimmed by absorption, stretched by the oblique viewing angle, and tinted toward the ambient light color. Petrichor models this with a BRAM scanline ring buffer. The program writes incoming Y-channel data into a 16-line circular buffer and reads it back in reverse order below the horizon. A stretch parameter compresses the readback address mapping, simulating the geometric elongation of oblique reflections. Opacity falls off with distance from the horizon, mimicking how real reflections fade as the viewing angle steepens.

### Atmospheric Perspective and Haze

In meteorology, *aerial perspective* is the loss of contrast and saturation in distant objects due to scattering by water droplets and particles in the atmosphere. Petrichor implements this as a Y-channel compression toward mid-gray combined with a UV blend toward a configurable tint color. The haze can operate in two modes: depth-proportional (stronger at the top of frame, simulating distance) or uniform (constant density across the entire image, simulating thick fog).

### Rain Streak Animation

Real rain creates near-vertical bright streaks in photographic exposures. Petrichor generates these via DDS (Direct Digital Synthesis) phase accumulation across the pixel grid. The phase accumulator produces a spatial frequency pattern; only the peaks of a sine lookup table pass through a threshold, creating thin bright lines. A frame-rate phase offset animates the streaks downward. The streak angle can be vertical (calm rain) or diagonal (wind-driven rain), and the animation speed toggles between slow and fast advance rates.

### Puddle Modulation

Real puddles do not form a uniform mirror — they accumulate in depressions, separated by dry patches. Petrichor's puddle mode uses an LFSR (Linear Feedback Shift Register) combined with a spatial hash of the pixel position to create irregular zones where the reflection is active or suppressed. This breaks the reflection into an organic patchwork pattern that resembles real puddle distribution on uneven ground.

### BRAM Ring Buffer Architecture

The scanline buffer uses 4 BRAM tiles to store 16 lines of Y-channel data at up to 1024 pixels per line. The buffer is addressed as a 14-bit value: the upper 4 bits select the line (0–15 in the ring), the lower 10 bits select the column. Each frame, the write pointer advances to the next line in the ring. Reflection readback subtracts an offset from the current write pointer, so the most recently written lines appear closest to the horizon and older lines appear further away. The stretch parameter scales this offset mapping.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y Channel ──────────────────────────────────────────────────
│   │
│   ├─ 0. BRAM Write               (store Y scanlines in 16-line ring buffer)
│   ├─ 0. Horizon Compare          (above/below flag + distance)
│   ├─ 1. Reflection Readback      (stretched inverted read from ring buffer)
│   ├─ 1. Puddle Masking           (LFSR spatial hash for patchy mode)
│   ├─ 2. Reflection Blend         (opacity-weighted mix with original Y)
│   ├─ 3. Atmospheric Haze         (compress Y toward mid-gray)
│   ├─ 4. Rain Streak Composite    (DDS thin-line additive overlay)
│   └─ 5–8. Interpolator           (wet/dry mix, 4 clocks)
│
├── U/V Channels ───────────────────────────────────────────────
│   │
│   ├─ 2. Reflection Desaturation  (blend toward cool blue: U≈530, V≈495)
│   ├─ 3. Haze Tint                (blend toward Rain Color target)
│   └─ 5–8. Interpolator           (wet/dry mix, 4 clocks)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Delayed pass-through (9-clock pipeline match)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original or processed signal
```

The pipeline has two major spatial divisions. Above the horizon, pixels receive only haze and streaks — no reflection data. Below the horizon, the BRAM readback blends a vertically-flipped copy of buffered scanlines into the image before haze and streak stages. The reflection opacity attenuates with distance from the horizon line, so the strongest mirror effect appears immediately below the split. The puddle LFSR modulates *whether* the reflection appears at each pixel position, creating irregular wet/dry zones. Rain streaks are additive — they brighten pixels above a sine-LUT threshold, creating thin bright lines that scroll frame-to-frame via DDS phase advance.

---

## Parameter Reference

<img src={petrichor_control_panel} alt="Videomancer front panel with Petrichor loaded"/>
*Videomancer's front panel with Petrichor active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Horizon
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the vertical position of the horizon line that divides the frame into sky (above) and reflection surface (below). The register value maps to approximately row 100–620 on screen. At 0% the horizon sits near the top of the frame, maximizing the reflection area. At 100% it sits near the bottom, leaving almost no room for reflections. The horizon defines the boundary where BRAM readback activates.

---

#### Knob 2 — Reflection
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the opacity of the reflected image below the horizon. At 0% no reflection is visible — the below-horizon region shows only the original video with haze. At 100% the reflected scanlines replace the original image at full strength near the horizon, fading with distance. The opacity falloff is distance-dependent: pixels close to the horizon get the full Reflection value, while pixels far below receive a scaled-down fraction.

---

#### Knob 3 — Stretch
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 39.1% |
| Suffix | % |

Controls the vertical stretch (elongation) of the reflected image. Higher values compress the readback address mapping so that fewer buffer lines are spread across the below-horizon area, making the reflection appear stretched as if viewed at a steep oblique angle. Lower values use more buffer lines, giving a shorter, more compact reflection that shows more scanline detail.

---

#### Knob 4 — Haze Dens
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 29.3% |
| Suffix | % |

Controls the density of atmospheric haze applied to the entire image. The haze compresses the Y channel toward mid-gray and blends the UV channels toward the Rain Color tint. In Depth mode (Toggle 7 off), haze is strongest at the top of the frame and diminishes toward the bottom, simulating aerial perspective. In Uniform mode (Toggle 7 on), haze density is constant across the entire frame.

---

#### Knob 5 — Rain Clr
| Property | Value |
|----------|-------|
| Range | 0deg – 360deg |
| Default | 70deg |
| Suffix | deg |

Controls the color tint of the atmospheric haze. The register value shifts the haze target away from neutral gray in both U and V dimensions. Low values produce a cool blue-shifted atmosphere, mid values give neutral fog, and high values shift toward warm amber tones. This control uses a polar-degrees display mode (0–360°) on the front panel, suggesting a hue wheel interpretation, though the internal math is a simple signed offset from center.

---

#### Knob 6 — Streaks
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the intensity of animated rain streaks overlaid on the image. At 0% no streaks are visible. As you increase the value, thin near-vertical bright lines appear, generated by a DDS phase accumulator and sine LUT threshold. The streak brightness is the register value right-shifted by 4 (divided by 16), so even at maximum the streaks remain relatively subtle — additive highlights rather than opaque overlays.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Haze Mode** | Depth | Uniform |
| **8 — StreakAng** | Vertical | Diagonal |
| **9 — Puddle** | Full | Patchy |
| **10 — Rain Spd** | Slow | Fast |
| **11 — Bypass** | Off | On |

The four functional toggles configure the haze rendering mode, streak geometry, puddle pattern, and animation speed. They do not interact with each other combinatorially — each controls an independent aspect of the rain simulation. The fifth toggle is the standard bypass.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry mix between the original input video and the rain-processed output. At 0% the output is pure dry (original video). At 100% the output is pure wet (fully processed with reflections, haze, and rain streaks). At intermediate values the processed and original signals blend via interpolator_u, allowing subtle atmospheric additions without full commitment to the effect.

---

## Guided Exercises

These exercises build from simple horizon reflections through full rainstorm simulation, progressively engaging each stage of the processing chain.

### Exercise 1: Pavement Mirrors

<img src={petrichor_exercise1_result} alt="Pavement Mirrors result"/>
*Pavement Mirrors — simulated result across source images.*
**Source**: A camera feed or recorded footage with clear architectural or landscape content — buildings, trees, or geometric shapes in the upper portion of the frame.

**Objective**: Learn how the horizon, reflection, and stretch controls create wet-pavement mirror effects.

1. **Set the horizon**: Turn Horizon to about 50% so the frame splits roughly in half.
2. **Enable reflection**: Turn Reflection up to about 70%. Below the horizon, a vertically-flipped copy of the upper image appears.
3. **Adjust stretch**: Sweep Stretch from low to high. At low values the reflection is compact and detailed; at high values it elongates, simulating an oblique viewing angle.
4. **Move the horizon**: Sweep Horizon up and down. Watch how the reflection region grows and shrinks.
5. **Enable puddles**: Toggle Puddle to Patchy. The continuous reflection breaks into irregular zones.

**Key concepts**: BRAM ring buffer stores recent scanlines for vertical-flip readback, stretch compresses the buffer address mapping, reflection opacity attenuates with distance from horizon

---

### Exercise 2: Fog Machine

<img src={petrichor_exercise2_result} alt="Fog Machine result"/>
*Fog Machine — simulated result across source images.*
**Source**: Any video with visible depth — a corridor, a landscape, or a scene with near and far elements.

**Objective**: Explore the atmospheric haze system and its interaction with the rain color tint.

1. **Zero the reflection**: Set Reflection to 0%, Streaks to 0%. This isolates the haze stage.
2. **Depth haze**: Set Haze Dens to about 60% with Haze Mode on Depth. The top of the frame fades into mist while the bottom stays clear.
3. **Uniform fog**: Toggle Haze Mode to Uniform. The same density now covers the entire frame evenly.
4. **Tint the atmosphere**: Sweep Rain Clr across its full range. Watch the fog shift from cool blue through neutral gray to warm amber.
5. **Combine with reflection**: Add Reflection back to ~40%. The haze sits on top of the reflected image below the horizon, creating a foggy puddle effect.

**Key concepts**: Depth-proportional haze simulates aerial perspective, uniform haze simulates thick fog, rain color tint shifts the UV target of the haze blend

---

### Exercise 3: Full Downpour

<img src={petrichor_exercise3_result} alt="Full Downpour result"/>
*Full Downpour — simulated result across source images.*
**Source**: High-contrast footage — a night city scene with bright lights works especially well.

**Objective**: Combine all stages for a complete rainstorm simulation.

1. **Set base reflection**: Horizon ~45%, Reflection ~60%, Stretch ~50%.
2. **Add atmosphere**: Haze Dens ~40%, Haze Mode Depth, Rain Clr toward cool blue (~20%).
3. **Enable rain**: Increase Streaks to ~60%. Thin bright lines appear across the frame.
4. **Diagonal rain**: Toggle StreakAng to Diagonal. The streaks tilt, suggesting wind.
5. **Speed up**: Toggle Rain Spd to Fast. The streaks scroll rapidly.
6. **Puddle patches**: Toggle Puddle to Patchy to break the reflection into organic zones.
7. **Mix back**: Lower Mix to ~70% to let some original image through for a subtler look.

**Key concepts**: All stages compound — reflection, haze, and streaks layer on top of each other; the mix fader controls overall effect intensity without changing the internal stage balance

---


## Tips

- **Horizon placement is everything**: The horizon line determines the entire composition. Place it where a natural reflective surface would be — one-third from the bottom for pavement, mid-frame for a lake.
- **Stretch simulates viewing angle**: Low stretch = looking straight down at a puddle. High stretch = looking across a wet road at a shallow angle. Match the stretch to the implied camera perspective.
- **Rain streaks are additive**: They only brighten pixels, so they are most visible against dark areas. High-contrast night footage with dark backgrounds shows streaks best.
- **Puddle mode adds realism**: Full-mirror reflection looks artificial. Patchy puddle mode creates the organic irregularity of real wet ground.
- **Haze Depth mode = distance**: Use it when the top of the frame represents "far away" and the bottom represents "nearby." This is the default perspective assumption.
- **Cool tint for rain**: Real rain atmospheres tend toward blue-gray. Keep Rain Clr in the lower third of its range for naturalistic results.
- **Feedback loops**: Routing the output back to the input creates recursive reflections — the reflection reflects itself, building layered mirror corridors.
- **Mix for subtlety**: Even at 30–40% mix, the wet-surface sheen is perceptible. You do not need 100% to sell the rain effect.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM** | Block RAM; dedicated memory resources within the FPGA fabric used for the scanline ring buffer. |
| **DDS** | Direct Digital Synthesis; a technique for generating waveforms by accumulating a phase value each clock cycle and looking up the corresponding amplitude. |
| **Haze** | Simulated atmospheric scattering that compresses contrast and tints the image toward a target color. |
| **Horizon** | The horizontal dividing line between the sky region (above) and the reflective surface region (below). |
| **LFSR** | Linear Feedback Shift Register; a pseudo-random number generator used here for puddle zone modulation. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Reflection** | A vertically-flipped, attenuated copy of buffered scanlines displayed below the horizon to simulate wet-surface mirroring. |
| **Ring Buffer** | A circular memory structure where the write pointer wraps around to the beginning after reaching the end, continuously overwriting the oldest data. |
| **Sine LUT** | A lookup table storing pre-computed sine values used to generate the rain streak spatial pattern. |
| **Stretch** | Address compression applied to the reflection readback, simulating the geometric elongation of oblique-angle reflections. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |
