---
draft: true
sidebar_position: 10
slug: /instruments/videomancer/attract
title: "Attract"
image: /img/instruments/videomancer/attract/attract_hero_s1.png
description: "Attract simulates the cumulative degradation of a CRT (cathode-ray tube) monitor that has been left running with a static image for extended periods — the \"attract mode\" phenomenon from decades-old arcade cabinets where demo loops would permanently etch game logos and score readouts into the phosphor screen."
---

![Attract hero image](/img/instruments/videomancer/attract/attract_hero_s1.png)
*A broadcast test pattern slowly fading into its own phosphor ghost, edges bleeding color under the weight of simulated decades of neglect.*

---

## Overview

Attract is a CRT aging simulator that recreates the visual degradation of old cathode-ray tube monitors left running for months or years without attention. Its name comes from the ***attract mode*** of arcade cabinets: demonstration loops that play endlessly when no one is playing, slowly burning their imagery into the phosphor coating of the screen. Attract composites five degradation effects together: phosphor burn-in, convergence error, radial vignette, color purity drift, and scanline dimming. Each effect is independently controllable and scaled by a master **Wear** parameter that determines how aged the simulated monitor appears.

At subtle settings, Attract adds gentle edge darkening and faint ghosting that evoke a well-used but not yet broken television. At extreme settings, it produces the full catastrophe: a persistent ghost image hovering beneath the live signal, color fringing at every edge, rainbow purity errors creeping in from the corners, and the warm, dim glow of a tube nearing the end of its life.

:::tip
Attract uses a ***line buffer*** in BRAM to accumulate the burn-in ghost. The ghost image builds up slowly over time and persists across frames. Use **Burn Reset** (Switch 9) to clear it and start fresh.
:::

### What's In a Name?

The name ***Attract*** refers to the ***attract mode*** of coin-operated arcade machines: the self-playing demonstration loop that runs on the screen when no credits have been inserted. These loops run for hours, days, sometimes years. On CRT displays, this repetitive imagery literally bakes itself into the phosphor coating, leaving a permanent ghost visible even when the machine is turned off. Attract recreates that ghost, and the broader palette of CRT degradation that accompanies it: the color fringing, the dim corners, the fading tube.

---

## Quick Start

1. Turn **Burn Rate** (Knob 1) to about 25% and **Burn Intns** (Knob 2) to about 50%. Feed a source with strong contrast: a title card or test pattern works well. Wait a few seconds, then switch to a different source. You'll see a faint ghost of the first image lingering beneath the new one.
2. Increase **Convergence** (Knob 3) to see colored fringing appear at sharp horizontal edges: the U chroma channel separates from Y and V, creating visible misregistration.
3. Turn up **Vignette** (Knob 4) and **Wear** (Knob 6) together. The edges of the picture darken, as if the tube's phosphor coating has faded unevenly from years of use.

---

## Parameters

![Videomancer front panel with Attract loaded](/img/instruments/videomancer/attract/attract_control_panel.png)
*Videomancer's front panel with Attract active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Burn Rate

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Burn Rate** controls how quickly the phosphor burn-in ghost accumulates. At minimum, the accumulator barely moves: the ghost builds extremely slowly, taking many seconds to register any change. As the value increases, the ghost responds more quickly to the input signal, tracking brightness changes within a few frames. At maximum, the accumulator updates rapidly, making the ghost nearly transparent and indistinguishable from the live signal.

:::note
Burn Rate controls the speed of the IIR filter, not the brightness of the ghost. To control how visible the ghost is, use **Burn Intns** (Knob 2).
:::

---

### Knob 2 — Burn Intns

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Burn Intns** (Burn Intensity) controls how much the accumulated ghost image adds to the output brightness. At minimum, the ghost contributes nothing: even if the burn buffer is fully saturated, no additional brightness appears. As the value increases, the ghost becomes more visible, added as extra luminance to the live signal. At maximum, the ghost image is at full strength, and regions that have accumulated persistent brightness can saturate to white.

---

### Knob 3 — Convergence

| Property | Value |
|----------|-------|
| Range | 0 – 8 |
| Default | 2 |

**Convergence** introduces horizontal misalignment between the U chroma channel and the Y/V channels, simulating the ***convergence error*** of a misaligned CRT. At minimum, all channels are aligned perfectly. As the value increases, the U channel shifts progressively further to the right, up to a maximum offset of eight pixels. This creates visible color fringing at sharp horizontal edges (a hallmark of old, poorly calibrated monitors.)

:::tip
For the most visible convergence fringing, feed a high-contrast source with sharp vertical edges. The color separation is most obvious where brightness changes abruptly.
:::

---

### Knob 4 — Vignette

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Vignette** controls the amount of brightness falloff toward the edges of the picture. At minimum, no edge darkening is applied. As the value increases, the corners and edges of the image grow dimmer, while the center remains at full brightness. This simulates the radial brightness falloff caused by phosphor aging on a CRT: the edges of the tube receive less electron beam energy over time and fade faster than the center.

The vignette distance is computed using an ***alpha-max-beta-min*** approximation for speed, giving it a slightly octagonal character rather than a perfectly round falloff.

---

### Knob 5 — Linearity

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |

**Linearity** is reserved for a future barrel/pincushion distortion effect. At present, adjusting this control has no visible effect on the output.

---

### Knob 6 — Wear

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Wear** is a master aging scaler that controls the overall intensity of the degradation effects. It scales three things simultaneously: the burn-in ghost brightness, the vignette edge darkening, and the purity color drift. At minimum, all three effects are suppressed regardless of their individual control settings. As the value increases, all three effects become more prominent. At maximum, the full degradation is applied.

:::tip
Think of **Wear** as a "years of neglect" knob. Turning it up is like fast-forwarding through a decade of 24/7 operation on a tube monitor.
:::

---

### Switch 7 — Purity

| Property | Value |
|----------|-------|
| Off | None |
| On | Rainbow |
| Default | None |

**Purity** selects between two base modes for the color purity drift effect. With the switch set to **None**, no purity shift is applied. With the switch set to **Rainbow**, the horizontal and vertical position of each pixel influences its chroma offset, creating a rainbow-like color fringing pattern that increases toward the edges of the screen. This simulates the ***purity error*** that occurs when CRT shadow mask alignment drifts, causing each electron gun to excite neighboring phosphor dots.

---

### Switch 8 — Distort

| Property | Value |
|----------|-------|
| Off | Barrel |
| On | Pincushon |
| Default | Barrel |

**Distort** selects a secondary purity variant. When combined with **Purity** (Switch 7), the two toggles form a four-mode selector for the color purity algorithm. The four resulting modes are:

| Purity | Distort | Effect |
|--------|---------|--------|
| None | Barrel | No purity shift |
| Rainbow | Barrel | Linear XY-position color offset |
| None | Pincushion | Radial inward color compression |
| Rainbow | Pincushion | Reflected XY-position color offset |

---

### Switch 9 — Burn Reset

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Burn Reset** clears the burn-in BRAM buffer, erasing all accumulated ghost imagery. Flip the switch to **On** to wipe the buffer to black, then flip it back to **Off** to let the accumulator begin building a new ghost. This is a momentary action (keep the switch at **Off** during normal operation.)

---

### Switch 10 — Scanlines

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Scanlines** dims alternating horizontal lines by approximately 12.5%, simulating the visible scan structure of an interlaced CRT display. With the switch set to **Off**, all lines are rendered at full brightness. With the switch set to **On**, every other line is slightly darkened, creating a subtle horizontal stripe pattern.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Attract processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use Bypass for instant A/B comparison between the raw input and the degraded result.

---

:::note Toggle Group Notes

**Purity** (Switch 7) and **Distort** (Switch 8) function as a combined two-bit mode selector for the color purity algorithm. The two toggle positions encode a binary number (Switch 7 = bit 0, Switch 8 = bit 1) that selects one of four purity behaviors:

- **Mode 0** (None + Barrel): No color purity shift applied.
- **Mode 1** (Rainbow + Barrel): Horizontal and vertical position create a gentle, linear rainbow fringe. The U channel shifts proportional to horizontal position; V shifts proportional to vertical position.
- **Mode 2** (None + Pincushion): Radial distance from center pushes both U and V inward, compressing chroma toward the center.
- **Mode 3** (Rainbow + Pincushion): Similar to Mode 1, but with the V axis reflected, creating an asymmetric rainbow pattern.

All four modes are further scaled by **Wear** (Knob 6). If Wear is at minimum, no purity shift is visible regardless of the mode selection.

:::

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (unprocessed) and wet (fully processed) signal. At minimum, the output is entirely dry: none of the CRT degradation effects are audible. At maximum, the output is entirely wet: the full processing chain is applied. Intermediate positions blend the two, allowing graduated amounts of aging.

---

## Background

### Phosphor burn-in

On a cathode-ray tube, the electron beam excites phosphor dots coated on the inside of the glass face. Over time, regions that display the same bright image continuously suffer ***phosphor burn-in***: the phosphor degrades and permanently retains a faint impression of the displayed content. This was a common problem on arcade monitors, ATM screens, airport departure boards, and early plasma televisions that displayed static logos or scoreboards for extended periods.

Attract simulates burn-in using an ***IIR*** (infinite impulse response) accumulator. A BRAM line buffer stores one accumulated brightness value per horizontal pixel position. Each frame, the stored value creeps toward the current input brightness at a rate determined by **Burn Rate**. The closer the rate is to maximum, the faster the ghost tracks the input. The ghost contribution is then scaled by **Burn Intns** and **Wear** before being added back to the live luminance signal as extra brightness: just as a real phosphor ghost brightens the screen where it has been burned.

### Convergence and purity

A color CRT uses three electron guns: one each for red, green, and blue: aimed through a shadow mask at phosphor triads on the screen face. ***Convergence*** is the precise alignment of these three beams so they strike the correct phosphor dots. When convergence drifts, the beams land on the wrong dots and colors separate visibly, creating colored fringes at edges.

***Purity*** describes how cleanly each beam excites only its intended color. When purity degrades, typically due to magnetization of the shadow mask or physical warping, the beam excites neighboring phosphors and the screen develops colored patches (particularly around the edges and corners.)

Attract simulates convergence by delaying the U chroma channel relative to Y and V, creating a horizontal color split. Purity is simulated by adding position-dependent chroma offsets that grow stronger toward the edges, tinted by the **Wear** parameter.

### Vignette and scanline structure

CRTs dim naturally toward their edges because the electron beam must sweep a longer path to reach the corners, losing energy along the way. Phosphor at the edges also degrades faster from the oblique beam angle. Attract models this as a radial distance function from the screen center, scaled by the **Vignette** and **Wear** controls: pixels farther from the center get darker.

The optional **Scanlines** effect darkens alternating lines to simulate the visible horizontal structure of an interlaced CRT. On real hardware, the electron beam paints only half the lines per field, and the gaps between painted lines create visible dark stripes (especially on larger screens or when viewed up close.)


---

## Signal Flow

### Signal Flow Notes

Three key interactions define Attract's processing chain:

1. **Wear as a master scaler.** The **Wear** parameter appears in three multiply stages: burn intensity, vignette attenuation, and purity offset. Setting Wear to zero suppresses all three degradation effects simultaneously, regardless of their individual control values. This makes Wear the single most impactful control for dialing the overall effect level.

2. **Burn-in is additive.** The phosphor ghost is *added* to the current luminance as extra brightness, not blended. This means the ghost can only brighten the image: it cannot darken anything. Regions where the accumulated burn value is high will appear brighter than the input, which can drive highlights to saturation at high **Burn Intns** and **Wear** settings.

3. **Convergence is chroma-only.** The convergence delay shifts only the U channel: Y and V pass through at the current sample position. This means convergence creates a one-sided color split, not a symmetric three-way separation. The visual effect is a colored fringe (primarily blue/yellow, since U encodes blue-difference) trailing to the right of sharp edges.

:::note
Unlike real CRT convergence where all three guns can drift independently, Attract's convergence shifts only one chroma axis. This is a deliberate simplification that captures the visible character of misalignment without requiring three independent delay lines.
:::


---

## Exercises

These exercises progress from simple burn-in observation to full CRT degradation. Each exercise layers additional aging effects onto the previous one, building toward a fully simulated vintage monitor.
### Exercise 1: Phosphor Ghost

![Phosphor Ghost result](/img/instruments/videomancer/attract/attract_ex1_s1.png)
*Phosphor Ghost — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A visible burn-in ghost that lingers after the input changes, demonstrating the phosphor memory accumulator.

#### Key Concepts

- Burn-in is an IIR accumulator that builds up over time
- Burn Rate controls accumulation speed; Burn Intns controls ghost brightness
- The ghost persists across input changes and can be cleared with Burn Reset

#### Video Source

Two contrasting video sources: a static high-contrast pattern (color bars, title card, or test chart) and a second, visually different source to switch to.

#### Steps

1. **Prepare**: Set **Burn Rate** (Knob 1) to about 40% and **Burn Intns** (Knob 2) to about 75%. Set **Wear** (Knob 6) to 50%. Set all other knobs to minimum and leave all toggles at their default positions.
2. **Burn**: Feed the high-contrast pattern and wait 10–15 seconds. The burn accumulator is silently recording the image.
3. **Reveal**: Switch to the second source. A ghostly afterimage of the first source lingers beneath the live signal. This is the phosphor ghost.
4. **Adjust**: Increase **Burn Intns** to make the ghost brighter. Decrease **Burn Rate** to make the ghost more persistent (slower to fade). Toggle **Burn Reset** (Switch 9) to On, then back to Off, and watch the ghost vanish instantly.

#### Settings

| Control | Value |
|---------|-------|
| Burn Rate | ~40% |
| Burn Intns | ~75% |
| Convergence | 0 |
| Vignette | 0% |
| Linearity | 0% |
| Wear | ~50% |
| Purity | None |
| Distort | Barrel |
| Burn Reset | Off |
| Scanlines | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: CRT Edge Decay

![CRT Edge Decay result](/img/instruments/videomancer/attract/attract_ex2_s1.png)
*CRT Edge Decay — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A picture with darkened edges and visible color fringing (the hallmarks of a tube that has been running for years.)

#### Key Concepts

- Vignette simulates radial brightness falloff from phosphor aging
- Convergence simulates beam misregistration (U channel shifted horizontally)
- Wear scales both effects simultaneously

#### Video Source

A live camera feed or footage with recognizable subjects, varied contrast, and visible edges.

#### Steps

1. **Prepare**: Set **Burn Rate** and **Burn Intns** to minimum (disable ghost). Set **Wear** (Knob 6) to about 60%.
2. **Vignette**: Turn **Vignette** (Knob 4) to about 50%. The edges and corners of the picture darken while the center stays bright.
3. **Convergence**: Increase **Convergence** (Knob 3) to about 4. Color fringing appears at sharp horizontal edges: the U chroma channel visibly separates from the luminance and V channels.
4. **Scanlines**: Enable **Scanlines** (Switch 10). A subtle stripe pattern appears, adding another layer of CRT character.
5. **Wear**: Sweep **Wear** from minimum to maximum. All three effects: vignette, convergence color impact, and scanlines: are unaffected by Wear directly, but vignette and purity both scale with it. Watch the vignette deepen as Wear increases.

#### Settings

| Control | Value |
|---------|-------|
| Burn Rate | 0% |
| Burn Intns | 0% |
| Convergence | ~4 |
| Vignette | ~50% |
| Linearity | 0% |
| Wear | ~60% |
| Purity | None |
| Distort | Barrel |
| Burn Reset | Off |
| Scanlines | On |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Full Attract Mode

![Full Attract Mode result](/img/instruments/videomancer/attract/attract_ex3_s1.png)
*Full Attract Mode — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

The full CRT degradation package: burn-in ghost, convergence fringing, darkened edges, rainbow purity drift, and scanline structure (all layered onto a live signal.)

#### Key Concepts

- All five degradation layers compose together
- Purity adds position-dependent color drift to the edges
- Mix allows graduated blending of the aging effect

#### Video Source

Any dynamic video source: ideally footage with movement, sharp edges, and color variety.

#### Steps

1. **Start with Exercise 2 settings**: Vignette at 50%, Convergence at 4, Wear at 60%, Scanlines on.
2. **Add burn-in**: Set **Burn Rate** (Knob 1) to about 25% and **Burn Intns** (Knob 2) to about 50%. Let the ghost accumulate for several seconds.
3. **Enable purity**: Set **Purity** (Switch 7) to **Rainbow**. A gentle rainbow fringe appears around the edges, strongest at the corners.
4. **Try purity modes**: Toggle **Distort** (Switch 8) to **Pincushion**. The purity pattern changes from a linear XY offset to a radial inward compression. Compare the two modes.
5. **Increase Wear**: Push **Wear** (Knob 6) to about 80%. All effects intensify: the ghost brightens, the edges darken further, and the color drift becomes more pronounced.
6. **Mix down**: Sweep the **Mix** fader (Fader 12) from 100% toward 0%. The degradation blends away, revealing the clean input beneath.
7. **A/B compare**: Toggle **Bypass** (Switch 11) for instant comparison between the fully degraded and clean signals.

#### Settings

| Control | Value |
|---------|-------|
| Burn Rate | ~25% |
| Burn Intns | ~50% |
| Convergence | ~4 |
| Vignette | ~50% |
| Linearity | 0% |
| Wear | ~80% |
| Purity | Rainbow |
| Distort | Pincushion |
| Burn Reset | Off |
| Scanlines | On |
| Bypass | Off |
| Mix | 100% |

---
## Glossary

- **Alpha-Max-Beta-Min**: A fast approximation algorithm for computing distance from the origin, using weighted sums of absolute coordinate values instead of the expensive square root required by the Pythagorean theorem.

- **Attract Mode**: The self-playing demonstration loop on arcade machines that runs continuously when no player has inserted a credit.

- **BRAM**: Block RAM; dedicated memory blocks on the FPGA used here to store one line of accumulated burn-in brightness values.

- **Convergence**: The alignment of a CRT's electron beams so that each color gun strikes its correct phosphor dot; misalignment produces visible color fringing at edges.

- **IIR Filter**: Infinite Impulse Response filter; a feedback-based filter where the output depends on both the current input and previous output values, creating a running weighted average.

- **Phosphor Burn-In**: Permanent degradation of CRT phosphor coating caused by prolonged display of a static image, leaving a visible ghost when the image changes.

- **Purity**: The quality of a CRT display where each electron gun excites only its intended phosphor color; purity errors cause colored patches, especially near edges.

- **Saturating Add**: An addition operation that clamps the result to a maximum value (here, 1023) instead of wrapping around when overflow occurs.

- **Scanline**: One horizontal line of a video raster; on CRT displays, visible gaps between lines create a characteristic striped texture.

- **Shadow Mask**: A perforated metal plate inside a CRT that ensures each electron beam hits only its corresponding colored phosphor dot.

- **Vignette**: A darkening effect at the edges and corners of an image, here simulating the radial brightness falloff of an aging CRT.

---
