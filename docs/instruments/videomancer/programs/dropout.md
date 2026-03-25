---
draft: true
sidebar_position: 94
slug: /instruments/videomancer/dropout
title: "Dropout"
image: /img/instruments/videomancer/dropout/dropout_hero_s1.png
description: "Every VHS cassette is a battlefield between the recording and time itself."
---

![Dropout hero image](/img/instruments/videomancer/dropout/dropout_hero_s1.png)
*Dropout applying VHS tape degradation: tracking error bands, dropout streaks, and chroma blur: to dissolve a clean video signal into the warm chaos of worn magnetic tape.*

---

## Overview

Dropout is a VHS tape degradation simulator that faithfully recreates the analog artifacts of worn, damaged, or misaligned magnetic tape playback. It combines six independent degradation layers: tracking error bands, dropout streaks, time-base jitter, head switching noise, chroma bandwidth reduction, and chroma phase instability: into a single program that can range from subtle tape warmth to catastrophic playback failure.

At mild settings, Dropout adds gentle horizontal wobble and soft chroma blur, evoking the nostalgic warmth of a well-loved home video. At extreme settings, the image tears apart: white streaks flash across the screen, rolling noise bands obliterate whole regions, and the picture lurches sideways as if the tape transport is fighting a losing battle against gravity.

:::tip
***Dropout is a layered degradation engine.*** Each artifact operates independently, so you can dial in exactly the tape look you want: from a hint of chroma smear to full-blown tracking disaster.
:::

### What's In a Name?

A ***dropout*** is a brief loss of signal on magnetic tape caused by a tiny flaw in the oxide coating: a scratch, a crease, a speck of dust that prevents the video head from reading data. On playback, the result is a short horizontal streak of white or frozen pixels. Dropout was one of the defining imperfections of the VHS format, and its name became synonymous with tape damage. In Videomancer, **Dropout** recreates this artifact alongside every other quirk of VHS playback: the tracking bands you'd fix by pressing the button on your VCR, the head switching glitch at the bottom of the screen, and the smeared colors from VHS's limited chroma bandwidth.

---

## Quick Start

1. Turn **Tracking** (Knob 1) clockwise to about 30%. A horizontal band of noise begins scrolling vertically through the image: this is the tracking error bar, the same artifact you'd see when pressing the tracking button on a VCR.
2. Increase **Wear** (Knob 2) to about 30%. White streaks begin flashing across the picture: these are dropout events from simulated tape coating damage.
3. Turn **TBC Error** (Knob 3) to about 40%. The image develops a gentle horizontal wobble as each scan line shifts left or right by a small, random amount. This simulates the jitter of a worn tape transport.
4. Lower **Chroma BW** (Knob 4) toward 25%. Colors begin to smear horizontally, mimicking the limited bandwidth of VHS chroma-under recording.

---

## Parameters

![Videomancer front panel with Dropout loaded](/img/instruments/videomancer/dropout/dropout_control_panel.png)
*Videomancer's front panel with Dropout active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Tracking

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |

**Tracking** controls the scroll speed of the tracking error band. At 0%, fully counterclockwise, the tracking band is stationary (and effectively invisible unless you look at the very spot where it sits). As the value increases, the band scrolls faster through the image, sweeping vertically at an ever-increasing rate. At 100%, the band races through the frame many times per second.

The tracking band is a 24-line-tall horizontal bar filled with LFSR noise that adds to the underlying luminance, mimicking the characteristic bright, noisy stripe that appears when a VCR's tape-to-head alignment drifts. Chroma is forced to neutral within the band.

:::note
When **Speed Error** (Switch 10) is enabled, the **Tracking** control also determines the rate of vertical roll: the picture slowly scrolls upward as if the capstan motor speed is slightly wrong.
:::

---

### Knob 2 — Wear

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Wear** controls the density of dropout streaks. At 0%, no dropouts occur. As the value increases, dropouts become more frequent and the picture becomes increasingly damaged. At 100%, dropouts are nearly continuous, shredding the image into horizontal noise.

Each dropout event begins when an ***LFSR*** (linear feedback shift register) value falls below the **Wear** threshold, and it continues for a burst length also determined by the LFSR. This means dropouts vary in both frequency and duration: just like real tape damage, which creates streaks of unpredictable length.

---

### Knob 3 — TBC Error

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |

**TBC Error** controls the amplitude of horizontal time-base jitter. At 0%, every scan line is perfectly aligned. As the value increases, each line shifts left or right by a small, random amount, producing the wobbly, unstable look of a worn tape transport. At 100%, the jitter is extreme and the image appears to vibrate horizontally.

The jitter source is a smoothed LFSR: each new random value is blended into a running average using an ***IIR*** (infinite impulse response) low-pass filter, producing slow, organic drift rather than harsh per-line noise. This mimics the mechanical inertia of a real capstan and pinch roller.

---

### Knob 4 — Chroma BW

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |

**Chroma BW** controls the bandwidth of the chroma (color) channels. At 0%, chroma is maximally blurred: colors smear heavily from left to right. As the value increases, more chroma detail is preserved. At 100%, chroma passes through with full bandwidth.

This parameter simulates VHS ***color-under*** recording, where chroma was recorded at a much lower bandwidth (~629 kHz) than luminance. The implementation is a per-line IIR low-pass filter applied independently to both U and V channels. The filter resets at each line start to prevent inter-line color bleeding.

:::tip
Low **Chroma BW** with full luminance detail is the quintessential VHS look: sharp edges and contours, but colors that bleed and smear horizontally.
:::

---

### Knob 5 — Phase Noise

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 12.5% |

**Phase Noise** controls the amount of chroma phase instability. At 0%, color phase is stable. As the value increases, U and V values are offset by an LFSR-derived amount that changes per scan line, causing colors to shimmer and shift unpredictably. At 100%, the color instability is severe.

This simulates the ***azimuth error*** inherent in helical scan recording: slight variations in the angle between the spinning video head and the tape surface cause the recovered color subcarrier phase to wander, producing hue shifts that vary from line to line.

---

### Knob 6 — Head Switch

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Head Switch** controls the height of the head switching noise bar at the bottom of the frame. At 0%, no head switch artifact is visible. As the value increases, a band of random LFSR noise grows upward from the bottom of the active picture. At 100%, the noise bar consumes a significant portion of the frame.

In a real VCR, the spinning drum carries two video heads that alternate reading the tape. The brief moment when one head stops and the other takes over produces a burst of noise, usually hidden in the overscan region below the visible picture. **Head Switch** lets you drag that artifact into view.

---

### Switch 7 — Track Band

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Track Band** enables or disables the tracking error band. When set to **On** (the default), the scrolling noise band is active and its speed is controlled by **Tracking** (Knob 1). When set to **Off**, the band is suppressed entirely, but the **Tracking** knob still drives vertical roll if **Speed Error** is enabled.

---

### Switch 8 — Drop Mode

| Property | Value |
|----------|-------|
| Off | White |
| On | Hold |
| Default | White |

**Drop Mode** selects what replaces the image during a dropout event. When set to **White** (the default), dropouts appear as bright white streaks with neutral chroma: the classic VHS dropout look. When set to **Hold**, the program freezes the last valid pixel value from the start of the current line, creating a horizontal smear that extends the previous content through the damaged region.

:::tip
**Hold** mode produces subtler dropouts that can be mistaken for a malfunctioning ***time-base corrector*** struggling to reconstruct missing data. **White** mode is the more dramatic, immediately recognizable tape damage look.
:::

---

### Switch 9 — Chroma Kill

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Chroma Kill** forces both chroma channels to neutral (mid-scale), converting the output to monochrome. When set to **Off** (the default), chroma passes through all processing stages normally. When set to **On**, U and V are locked to 512 regardless of all other chroma processing.

This simulates a VCR with a failed color playback circuit, or a tape recorded in a format that didn't carry chroma information.

---

### Switch 10 — Speed Error

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Speed Error** enables a slow vertical roll that simulates a capstan motor running at the wrong speed. When set to **Off** (the default), the picture is vertically stable. When set to **On**, the image gradually scrolls upward, and the rate of scroll is controlled by the **Tracking** knob. A low **Tracking** value produces a barely perceptible drift; a high value produces a fast, disorienting roll.

The vertical roll is implemented by accumulating the **Tracking** value into a counter each frame, then adding the result to all vertical position calculations.

---

### Switch 11 — Luma Noise

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Luma Noise** adds a fine grain of random noise to the luminance channel. When set to **On** (the default), each pixel receives up to 15 levels of additive LFSR noise, producing a subtle sparkle across the picture. When set to **Off**, luma passes through the processing chain without grain.

The noise amplitude is intentionally small (4 bits out of a 10-bit range) to mimic the faint grain of analog tape rather than heavy digital noise.

---

:::note Toggle Group Notes

The five toggle switches are independent: each enables or disables a single artifact layer. There is no combined mode relationship between them.

:::

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the original (dry) input and the fully processed (wet) signal. At 0%, fully left, the output is the original unprocessed video. At 100%, fully right (the default), the output is entirely the processed tape degradation. Intermediate values blend the two, allowing you to dial in a subtle tape texture without fully committing to the effect.

---

## Background

### Magnetic tape recording

***VHS*** (Video Home System) was a consumer videotape format introduced by JVC in 1976. It recorded analog video onto half-inch magnetic tape using ***helical scan*** recording, where two video heads mounted on a spinning drum trace diagonal tracks across the tape as it moves slowly past. This mechanical dance between spinning heads and moving tape was an engineering marvel, but it was also the source of nearly every artifact that Dropout simulates: tracking errors from misalignment, dropouts from coating damage, jitter from transport speed variation, and chroma instability from azimuth error.

### Color-under recording

VHS used a technique called ***color-under*** to fit both luminance and chrominance onto a narrow tape track. The luminance signal was frequency-modulated and recorded directly, preserving most of its bandwidth. The chrominance signal, however, was down-converted to a much lower carrier frequency (~629 kHz) and recorded beneath the luminance: hence "color-under." This dramatically reduced the chroma bandwidth, which is why VHS color always looked softer and more smeared than the luminance detail. Dropout's **Chroma BW** control simulates this bandwidth limitation using an IIR low-pass filter.

### Time-base correction

A ***time-base corrector*** (TBC) is a device that compensates for the mechanical imprecision of tape playback by buffering each line and re-clocking it to a stable reference. Without a TBC, the picture wobbles horizontally because the tape doesn't move at a perfectly constant speed: the capstan motor has slight speed variations, the tape stretches differently across its length, and temperature changes alter the tape's dimensions. Dropout's **TBC Error** control reintroduces this wobble by reading each line from a buffer at a slightly offset position, controlled by a smoothed random source.


---

## Signal Flow

### Signal Flow Notes

The output composition stage uses a ***priority overlay*** structure: each artifact layer can overwrite the output of the previous one, and the last active layer wins. The priority order from lowest to highest is: base signal → luma noise → chroma kill → head switch → track band → dropout. This means a dropout streak will overwrite everything underneath it, including a tracking band or head switch noise, just as real tape damage would mask other artifacts.

The chroma path is notable for its two independent degradation stages. First, the IIR low-pass blur reduces bandwidth, simulating the physical limitation of color-under recording. Then, the phase noise stage adds per-line color instability on top of the already-blurred chroma. These two effects compound: blurred colors wobble more visibly because the smoothed signal changes slowly enough for the per-line offset to be visible as a coherent hue shift rather than random speckle.

:::note
The line buffer stores one full line of Y, U, and V in three separate BRAMs. The jitter offset shifts the *read* address, not the write address, so the stored line is always correct: only the playback position wobbles. This is exactly how a real time-base corrector works, just in reverse: instead of correcting jitter, Dropout introduces it.
:::


---

## Exercises

These exercises progress from isolated tape artifacts to full VHS degradation. Each one adds layers of damage until the image is thoroughly worn.
### Exercise 1: Tracking Trouble

![Tracking Trouble result](/img/instruments/videomancer/dropout/dropout_ex1_s1.png)
*Tracking Trouble — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A picture with a classically misaligned VCR tracking error: a scrolling noise band and horizontal jitter, just like pressing the tracking button on a VCR that won't cooperate.

#### Key Concepts

- Tracking error bands are scrolling noise regions
- Time-base jitter creates horizontal wobble
- These two artifacts together define the "bad tracking" look

#### Video Source

A clean camera feed or recorded footage with strong horizontal lines or text (these make the jitter and tracking band most visible.)

#### Steps

1. Confirm **Track Band** (Switch 7) is set to **On**.
2. Turn **Tracking** (Knob 1) to about 25%. A horizontal noise band begins scrolling slowly through the image.
3. Increase **TBC Error** (Knob 3) to about 30%. The image develops a subtle horizontal wobble (each line shifts slightly left or right.)
4. Notice how the tracking band displaces the picture more aggressively as it passes through: noise is additive, so the band tears the image apart more than the surrounding jitter does.
5. Slowly increase **Tracking** to see the band scroll faster. Find a speed that feels like a VCR struggling to lock onto the tape.

#### Settings

| Control | Value |
|---------|-------|
| Tracking | ~25% |
| Wear | 0% |
| TBC Error | ~30% |
| Chroma BW | 100% |
| Phase Noise | 0% |
| Head Switch | 0% |
| Track Band | On |
| Drop Mode | White |
| Chroma Kill | Off |
| Speed Error | Off |
| Luma Noise | On |
| Mix | 100% |

---

### Exercise 2: Worn Tape

![Worn Tape result](/img/instruments/videomancer/dropout/dropout_ex2_s1.png)
*Worn Tape — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

The look of a well-loved VHS tape that's been played hundreds of times: soft colors, occasional white streaks, and faintly shimmering hues.

#### Key Concepts

- Dropout streaks simulate physical tape coating damage
- Chroma bandwidth reduction is the signature VHS color look
- Phase noise adds color instability per scan line

#### Video Source

Footage with saturated colors and smooth gradients (skin tones, sunsets, or color bars work well.)

#### Steps

1. Set **Chroma BW** (Knob 4) to about 25%. Colors immediately soften and smear horizontally, especially at sharp color transitions.
2. Add **Phase Noise** (Knob 5) at about 20%. Colors begin to shimmer subtly from line to line (hues shift slightly between adjacent scan lines.)
3. Increase **Wear** (Knob 2) to about 20%. Occasional white streaks flash across the picture (these are dropout events.)
4. Toggle **Drop Mode** (Switch 8) to **Hold**. The white streaks become horizontal smears that extend the previous pixel, a subtler form of damage.
5. Enable **Head Switch** (Knob 6) at about 30%. A band of noise appears at the bottom of the picture where the spinning video heads swap.
6. Pull **Mix** (Fader 12) back to about 75% to blend a hint of the clean original through the degradation.

#### Settings

| Control | Value |
|---------|-------|
| Tracking | 0% |
| Wear | ~20% |
| TBC Error | ~15% |
| Chroma BW | ~25% |
| Phase Noise | ~20% |
| Head Switch | ~30% |
| Track Band | On |
| Drop Mode | Hold |
| Chroma Kill | Off |
| Speed Error | Off |
| Luma Noise | On |
| Mix | ~75% |

---

### Exercise 3: Total Tape Failure

![Total Tape Failure result](/img/instruments/videomancer/dropout/dropout_ex3_s1.png)
*Total Tape Failure — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A picture in catastrophic playback failure: the tape is chewed, the tracking is gone, the capstan is drifting, and the color circuit has given up. Pure VHS destruction.

#### Key Concepts

- All six degradation layers operate simultaneously
- Speed error adds vertical roll
- Chroma kill simulates a failed color circuit
- The priority overlay system determines which artifact is visible when multiple overlap

#### Video Source

Any footage (by the end, the source will be barely recognizable.)

#### Steps

1. Set **Tracking** (Knob 1) to about 50%. The tracking band scrolls aggressively.
2. Set **Wear** (Knob 2) to about 60%. Dropout streaks are frequent and long.
3. Set **TBC Error** (Knob 3) to about 70%. The picture wobbles dramatically.
4. Set **Chroma BW** (Knob 4) to about 10%. Colors smear into wide, soft bands.
5. Set **Phase Noise** (Knob 5) to about 50%. Color instability is now clearly visible.
6. Set **Head Switch** (Knob 6) to about 80%. A tall noise bar dominates the bottom of the frame.
7. Enable **Speed Error** (Switch 10). The picture begins to roll vertically, slowly scrolling upward.
8. Enable **Chroma Kill** (Switch 9). All color disappears (the picture is now monochrome static.)
9. Set **Mix** (Fader 12) to 100%. Fully commit to the destruction.

#### Settings

| Control | Value |
|---------|-------|
| Tracking | ~50% |
| Wear | ~60% |
| TBC Error | ~70% |
| Chroma BW | ~10% |
| Phase Noise | ~50% |
| Head Switch | ~80% |
| Track Band | On |
| Drop Mode | White |
| Chroma Kill | On |
| Speed Error | On |
| Luma Noise | On |
| Mix | 100% |

---
## Glossary

- **Azimuth Error**: A slight angular misalignment between the video head and the tape surface, causing the recovered chroma subcarrier phase to wander and producing per-line color shifts.

- **Capstan**: The driven roller in a tape transport that controls tape speed; variations in capstan speed produce time-base jitter and vertical roll.

- **Color-Under**: A VHS recording technique where the chrominance signal is down-converted to a low carrier frequency and recorded beneath the luminance signal, severely limiting chroma bandwidth.

- **Dropout**: A brief loss of signal on magnetic tape caused by a physical defect in the oxide coating, producing a horizontal streak of missing data.

- **Helical Scan**: A recording method where video heads on a spinning drum trace diagonal tracks across slowly moving tape, maximizing recorded bandwidth.

- **IIR Filter**: Infinite Impulse Response filter; a recursive digital filter where the output depends on both current input and previous output, producing an exponential smoothing effect.

- **LFSR**: Linear Feedback Shift Register; a shift register whose input bit is a function of its previous state, generating a pseudo-random sequence used for noise and jitter sources.

- **Time-Base Corrector**: A device that buffers each video line and re-clocks it to a stable reference, compensating for the mechanical speed variations of tape playback.

- **Tracking**: The alignment between the video playback head and the recorded tracks on tape; misalignment produces a scrolling band of noise across the picture.

- **VHS**: Video Home System; a consumer analog videotape format introduced by JVC in 1976, using half-inch tape with helical scan recording.

---
