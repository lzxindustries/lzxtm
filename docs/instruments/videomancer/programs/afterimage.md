---
draft: true
sidebar_position: 2
slug: /instruments/videomancer/afterimage
title: "Afterimage"
image: /img/instruments/videomancer/afterimage/afterimage_hero_s1.png
description: "Afterimage recreates the physiological phenomenon where prolonged viewing of a stimulus produces a persistent colour-negative ghost when the stimulus is removed or the gaze shifts."
---

![Afterimage hero image](/img/instruments/videomancer/afterimage/afterimage_hero_s1.png)
*Afterimage conjuring spectral color-negative trails that linger behind moving subjects like retinal ghosts burned into the screen.*

---

## Overview

Afterimage recreates the physiological phenomenon that happens when you stare at a bright, saturated image and then look away: you see a lingering phantom in the opposite colors. The program tracks the temporal average of each video channel using a digital ***IIR (infinite impulse response)*** filter, computes the color negative of that running average, and blends the result back into the live signal. Moving subjects leave behind shimmering, complementary-colored trails that fade over time.

At gentle settings, Afterimage produces subtle spectral halos around objects in motion: a bluish tint trailing a warm face, a magenta whisper following green foliage. Push the controls harder and the afterimages become dominant, saturating the frame with inverted color fields that fight against the live picture. A secondary Ghost mode abandons the negative and simply lets the temporal average bleed through, creating translucent motion trails like long-exposure photography rendered in real time.

:::tip
Afterimage is most dramatic with ***slow-moving, high-contrast*** subjects. Fast motion blurs the IIR accumulator too quickly for the negative to build up. Try slow pans, dissolving graphics, or a single hand moving across a static background.
:::

### What's In a Name?

An ***afterimage*** is a visual illusion caused by the fatigue of photoreceptor cells in your retina. When you stare at a saturated red patch and then shift your gaze to a white surface, you see a cyan ghost: the complementary color: because the red-sensitive cones have temporarily exhausted their response. This program simulates that retinal adaptation digitally. Instead of tired cone cells, an IIR accumulator tracks the temporal average; instead of your optic nerve producing the complement, arithmetic negation creates it. The result is the same: a phantom in opposite colors, haunting the screen.

---

## Quick Start

1. Feed a video source with some movement. Set **Persist** (Knob 1) to about 50% and **Neg Str** (Knob 2) fully counterclockwise. You should see faint color-negative trails behind moving objects.
2. Slowly turn **Persist** clockwise. The trails become longer-lived and more prominent as the IIR filter adapts more slowly to changes.
3. Increase **Decay** (Knob 3) toward 100%. The trails now fade away faster between movements, keeping the afterimage crisp instead of building into a muddy blur.
4. Toggle **Mode** (Switch 7) to **Ghost**. The color-negative trails vanish, replaced by transparent echoes of past frames (like ghostly double exposures trailing behind the action.)

---

## Parameters

![Videomancer front panel with Afterimage loaded](/img/instruments/videomancer/afterimage/afterimage_control_panel.png)
*Videomancer's front panel with Afterimage active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Persist

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Persist** controls the adaptation speed of the IIR filter that tracks the temporal average of the video signal. At 0%, the filter adapts quickly, tracking rapid changes and producing only brief afterimage flashes. As **Persist** increases toward 100%, the filter responds more sluggishly: the running average changes slowly, and afterimage trails linger much longer before catching up to the current frame. The **Speed** toggle (Switch 9) selects between two ranges of persistence: Slow mode (the default) provides longer, more dramatic trails; Fast mode keeps things snappy.

:::tip
For the most visible afterimage effect, set **Persist** above 60%. Below that, the filter adapts too quickly for the negative to build noticeable contrast against the live signal.
:::

---

### Knob 2 — Neg Str

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Neg Str** (Negative Strength) controls how intensely the computed negative imprint is applied to the output image. At 0%, fully counterclockwise, the negative is at maximum intensity: the full computed difference between the afterimage and the live input is applied, producing vivid, saturated complementary-color trails. As you turn the knob clockwise toward 100%, the negative contribution is progressively attenuated, producing a softer, more delicate afterimage. At 100%, the afterimage is barely perceptible: a faint tint rather than a bold color shift.

---

### Knob 3 — Decay

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Decay** controls how quickly the IIR accumulators fade back toward a neutral midpoint between frames. At 0%, decay is very slow: the temporal average holds its value stubbornly, and afterimages can persist almost indefinitely even after the source changes. Increasing **Decay** toward 100% causes the accumulators to relax more quickly toward neutral gray, so afterimages naturally dissolve even when the input is static. Think of it as a "memory expiration" control: low decay yields a long memory, high decay yields a short one.

---

### Knob 4 — Blend

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Blend** controls the ratio between the current live input and the computed afterimage composite. At 0%, the output is dominated by the live video with minimal afterimage contribution. At 100%, the afterimage composite takes over. At the default 50%, both the live signal and the afterimage share equal presence in the output frame.

---

### Knob 5 — Saturate

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Saturate** adjusts the color saturation of the processed output. Below 50%, chroma is reduced: the afterimage trails and the live signal both become desaturated, trending toward monochrome. At the midpoint (50%), saturation crosses a threshold and begins boosting: above 50%, chroma deviation from neutral is amplified by 50%, producing more vivid complementary colors in the afterimage trails and richer hues in the live signal alike.

:::note
Because saturation operates as a two-level control (reduce or boost), you'll notice a visible step at the 50% midpoint rather than a perfectly smooth gradient.
:::

---

### Knob 6 — Bright

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Bright** applies a luminance offset to the processed output. At 50% (the default), brightness is unchanged. Turning counterclockwise toward 0% darkens the entire image; turning clockwise toward 100% brightens it. This is a simple DC offset added after all afterimage processing, so it shifts the overall exposure without affecting the color balance of the afterimage trails.

---

### Switch 7 — Mode

| Property | Value |
|----------|-------|
| Off | Negative |
| On | Ghost |
| Default | Negative |

**Mode** selects between two fundamental behaviors. In the **Negative** position (default), Afterimage computes the color complement of the temporal average and blends it into the output: this is the classic afterimage effect where trails appear in the opposite color of the original subject. In the **Ghost** position, the negative computation is bypassed entirely: the temporal average itself is blended with the live input, producing translucent motion trails that echo the original colors rather than inverting them.

:::tip
Ghost mode is especially beautiful with slow, deliberate camera movements. It creates a dreamy, long-exposure quality reminiscent of light painting or pinhole photography.
:::

---

### Switch 8 — Channel

| Property | Value |
|----------|-------|
| Off | All |
| On | Hue |
| Default | All |

**Channel** modifies the behavior of the negative computation. In the **All** position (default), the selected mode operates normally. In the **Hue** position, the negative computation changes character: when combined with **Mode** set to Negative, the output becomes a real-time inversion of the current frame rather than a temporal afterimage. When combined with Ghost mode, the temporal average passes through directly as a smooth ghost trail. See the Toggle Group Notes below for the full four-mode combination table.

---

### Switch 9 — Speed

| Property | Value |
|----------|-------|
| Off | Slow |
| On | Fast |
| Default | Slow |

**Speed** selects between two ranges of IIR filter response time. In the **Slow** position (default), the persistence range spans longer time constants: trails linger and build up over many frames, ideal for slow-moving subjects and meditative compositions. In the **Fast** position, the persistence range is compressed into shorter time constants, making the afterimage respond more quickly to changes. Fast mode is better suited to energetic footage with rapid motion.

---

### Switch 10 — Animate

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Animate** enables or disables the internal frame counter. When set to **On** (default), the frame counter advances on each vertical sync pulse. When set to **Off**, the counter holds its current value. This parameter is available for future animation features.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Afterimage processing stages. The sync delay pipeline still aligns timing, so toggling **Bypass** produces a clean, glitch-free transition. Use it for instant A/B comparison between the raw input and the processed result.

---

:::note Toggle Group Notes

**Mode** (Switch 7) and **Channel** (Switch 8) together form a combined four-mode selector. While each toggle has two positions, their combination produces four distinct processing behaviors:

| Mode (Switch 7) | Channel (Switch 8) | Behavior |
|---|---|---|
| Negative | All | **Classic afterimage** — complement of the temporal average, producing trails in the opposite color of the source. The signature mode. |
| Ghost | All | **Complement mirror** — luminance is reflected around mid-gray while chrominance is negated. A variation on the negative with different tonal character. |
| Negative | Hue | **Live inversion** — real-time negative of the current frame, without temporal accumulation. The output is a continuously updated color negative. |
| Ghost | Hue | **Ghost trail** — the raw temporal average is passed through. Moving objects leave translucent echoes in their original colors. |

:::note
When **Channel** is set to **Hue**, the temporal characteristics change dramatically. In the Negative+Hue combination, there is no afterimage persistence at all: the output is a straightforward frame inversion. The Ghost+Hue combination produces the purest motion trail because it outputs the temporal average directly without any negation.
:::

:::

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** is the master wet/dry crossfade between the original input and the fully processed output. At 0%, the output is entirely dry: you hear (see) only the unprocessed input. At 100% (the default), the output is fully wet: the complete afterimage processing chain is applied. Intermediate values blend the two proportionally, allowing you to dial in exactly how much afterimage tinting you want layered over the source.

---

## Background

### Afterimages and retinal adaptation

The afterimage is one of the oldest observations in visual science. Aristotle noted that staring at the sun left a lingering phantom, and Goethe devoted extensive passages in his *Theory of Colours* to describing the complementary afterimages produced by saturated stimuli. The mechanism is straightforward: photoreceptor cells in the retina become fatigued by sustained stimulation and temporarily reduce their sensitivity. When the stimulus is removed, the fatigued cells respond less strongly than their neighbors, creating a phantom image in the complementary color.

This program creates an electronic analog of that process. Where the retina uses chemical adaptation, Afterimage uses an IIR low-pass filter. Where cone cell fatigue produces the negative, arithmetic subtraction from full-scale does the same. The result is functionally identical: a ghost in opposite colors that fades as the "retinal" memory decays.

### IIR temporal filtering

The core of Afterimage is an ***infinite impulse response*** (IIR) filter: the simplest form of low-pass filtering. On each clock cycle, the filter updates its running average using the formula:

```
average ← average + (input − average) >> shift
```

The `shift` value (controlled by **Persist** and **Speed**) determines how heavily each new input sample influences the running average. A large shift means the average changes very slowly: it "remembers" past values for a long time. A small shift means it tracks the input closely. This single-pole IIR filter is the same structure used in audio envelope followers and exponential moving averages in signal processing.

Because the iCE40 FPGA has no large frame buffer, the IIR accumulators are maintained as single registers rather than per-pixel memory. This means the temporal averaging applies to the signal globally rather than spatially: all pixels at a given moment share the same accumulator state. The visual result is a columnar temporal smear reminiscent of CRT phosphor persistence.

### Negative complement computation

Once the temporal average is established, Afterimage computes a negative by subtracting the average from full-scale (1023 for 10-bit video). For luminance, this maps white to black and vice versa. For chrominance (U and V channels), the subtraction from 1023 mirrors color values across the neutral axis, swapping warm for cool, red for cyan, yellow for blue. The result is exactly the complementary color that retinal fatigue would produce.

The Ghost mode bypasses the negation step entirely, passing the raw temporal average to the blending stage. This creates motion trails without color inversion: objects leave behind fading echoes in their original colors, like a long-exposure photograph.

### Persistence in analog video history

The concept of image persistence has deep roots in video art and analog television. CRT phosphors naturally exhibit persistence: the glowing phosphor dot continues to emit light briefly after the electron beam has moved on, creating subtle motion trails. Early video synthesizers exploited this by using ***feedback loops***, routing the output back to the input through a camera pointed at a monitor, building up layers of recursive imagery. Afterimage captures the essence of this recursive memory without requiring a physical feedback loop. The IIR accumulator serves the same role as the phosphor's glow: a fading record of what was, overlaid on what is.


---

## Signal Flow

### Signal Flow Notes

Two critical interactions define the character of Afterimage's output:

1. **IIR persistence vs. decay**: The IIR filter and the decay mechanism work in opposition. The IIR filter accumulates toward the input signal: it builds up the temporal average. Decay pulls the accumulator back toward mid-gray at each vertical sync pulse. The balance between **Persist** (how fast the IIR tracks) and **Decay** (how fast it forgets) determines the lifespan and intensity of the afterimage trails. High persistence with low decay creates long-lived, saturated trails. Low persistence with high decay creates brief, subtle flickers.

2. **Negative strength as attenuation**: The negative computation produces a full-strength color complement, but the **Neg Str** control attenuates it before blending. The attenuation operates as a right-shift on the absolute difference between the negative and the input: effectively dividing the contribution by powers of two. This means the transition from strong to subtle is not perfectly linear; it steps through halving stages.

:::tip
**Decay happens once per frame**, not once per pixel. This means the accumulators hold steady throughout each frame and only relax toward neutral during the vertical blanking interval. The decay rate is frame-rate-dependent: at higher frame rates, decay steps accumulate faster, shortening the effective afterimage lifespan.
:::


---

## Exercises

These exercises explore Afterimage's temporal processing chain, from basic afterimage trails to complex multi-mode compositions. Each exercise builds confidence with different aspects of persistence, negation, and blending.
### Exercise 1: Classic Afterimage Trails

![Classic Afterimage Trails result](/img/instruments/videomancer/afterimage/afterimage_ex1_s1.png)
*Classic Afterimage Trails — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A classic afterimage effect where moving subjects leave behind vivid complementary-color trails that gradually fade to neutral.

#### Key Concepts

- IIR temporal filtering creates a running average of the video signal
- The color negative of the average produces complementary afterimage trails
- Persist and Decay together control trail lifespan

#### Video Source

A live camera feed pointed at a subject making slow, deliberate hand gestures or movements against a plain, contrasting background.

#### Steps

1. **Establish persistence**: Set **Persist** (Knob 1) to about 70%. Move a brightly colored object slowly across the frame. You should see the beginnings of a faint color trail.
2. **Strengthen the negative**: Turn **Neg Str** (Knob 2) fully counterclockwise to 0%. The afterimage trails become vivid: a red object leaves cyan trails, a yellow object leaves blue.
3. **Tune the decay**: Adjust **Decay** (Knob 3). At low values, the trails accumulate and never fully disappear. Increase Decay until the trails fade away within two to three seconds (this is the sweet spot for a natural-looking afterimage.)
4. **Polish**: Set **Bright** (Knob 6) to taste if the overall image is too dark or bright. Use **Mix** (Fader 12) to blend the afterimage effect against the clean input if the trails are too dominant.

#### Settings

| Control | Value |
|---------|-------|
| Persist | 70% |
| Neg Str | 0% |
| Decay | ~40% |
| Blend | 50% |
| Saturate | 50% |
| Bright | 50% |
| Mode | Negative |
| Channel | All |
| Speed | Slow |
| Animate | On |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Ghost Trail Long Exposure

![Ghost Trail Long Exposure result](/img/instruments/videomancer/afterimage/afterimage_ex2_s1.png)
*Ghost Trail Long Exposure — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A dreamlike long-exposure effect where moving objects leave behind fading, translucent echoes in their original colors (like a time-lapse photograph captured in real time.)

#### Key Concepts

- Ghost mode passes the temporal average without negation
- High persistence creates smooth, translucent motion blur
- Saturation and brightness shape the ghost character

#### Video Source

A camera feed with a single slowly moving subject: a dancer's hand, a swinging pendulum, or someone walking across the frame.

#### Steps

1. **Enter Ghost mode**: Set **Mode** (Switch 7) to **Ghost** and **Channel** (Switch 8) to **Hue**. This selects pure ghost trail mode: the temporal average passes through without color inversion.
2. **Maximize persistence**: Set **Persist** (Knob 1) to about 85% and **Speed** (Switch 9) to **Slow**. The IIR filter will hold past frames for a long time, creating extended trails.
3. **Slow the decay**: Set **Decay** (Knob 3) to about 20%. The trails should linger for many seconds before fading.
4. **Shape the trail**: Reduce **Saturate** (Knob 5) slightly below 50% to desaturate the ghost trails, giving them a washed-out, ethereal quality. Adjust **Bright** (Knob 6) slightly above 50% to lift the shadows in the trailing echoes.
5. **Blend to taste**: Use **Mix** (Fader 12) at about 80% to let a bit of the clean input shine through, anchoring the live subject against the ghostly background.

#### Settings

| Control | Value |
|---------|-------|
| Persist | 85% |
| Neg Str | 50% |
| Decay | 20% |
| Blend | 50% |
| Saturate | 40% |
| Bright | 55% |
| Mode | Ghost |
| Channel | Hue |
| Speed | Slow |
| Animate | On |
| Bypass | Off |
| Mix | 80% |

---

### Exercise 3: Chromatic Negative Feedback

![Chromatic Negative Feedback result](/img/instruments/videomancer/afterimage/afterimage_ex3_s1.png)
*Chromatic Negative Feedback — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

An aggressive, psychedelic color-cycling effect where the afterimage negative and the live input compete for dominance, creating swirling complementary color fields that shift and pulse with the content.

#### Key Concepts

- Combining strong negative persistence with saturation boost creates intense chromatic effects
- Fast speed with high persistence creates rapidly cycling color shifts
- Mode and Channel combinations alter the character of the color interactions

#### Video Source

High-contrast footage: colored geometric shapes, bright text on a dark background, or a face under strong directional colored light.

#### Steps

1. **Strong foundation**: Set **Persist** (Knob 1) to about 60% and **Speed** (Switch 9) to **Fast**. Set **Neg Str** (Knob 2) fully counterclockwise to 0% for maximum negative intensity.
2. **Boost saturation**: Turn **Saturate** (Knob 5) above 50% to amplify the complementary colors. The afterimage trails should become vividly chromatic.
3. **Minimize decay**: Set **Decay** (Knob 3) near 0%. The IIR accumulators will hold their values stubbornly, building up layers of complementary color.
4. **Explore modes**: With the effect running, toggle through the mode combinations. Start with **Negative** + **All** (the classic), then try **Ghost** + **All** (complement mirror) to see how the tonal balance shifts. Each combination produces a distinctly different chromatic texture.
5. **Real-time inversion**: Set **Mode** to **Negative** and **Channel** to **Hue**. The output becomes a continuous color negative of the live input: no temporal accumulation, just pure inversion. Notice how this mode responds instantly to changes with no trailing.
6. **Sculpt with brightness**: Use **Bright** (Knob 6) to shift the overall exposure, finding the point where the negative and positive colors achieve maximum visual tension.

#### Settings

| Control | Value |
|---------|-------|
| Persist | 60% |
| Neg Str | 0% |
| Decay | ~5% |
| Blend | 50% |
| Saturate | 75% |
| Bright | 50% |
| Mode | Negative |
| Channel | All |
| Speed | Fast |
| Animate | On |
| Bypass | Off |
| Mix | 100% |

---
## Glossary

- **Accumulator**: A register that adds incoming values to its stored total over time, used here to track the running temporal average of the video signal.

- **Afterimage**: A visual illusion where a phantom image persists after the original stimulus is removed, typically appearing in complementary colors due to photoreceptor fatigue.

- **Chroma**: The color information in a video signal, encoded as U and V deviation from a neutral midpoint in YUV color space.

- **Complementary Color**: The color produced by subtracting a hue from white; red and cyan, blue and yellow, green and magenta are complementary pairs.

- **Decay**: The gradual return of a signal or accumulator toward a resting value (neutral midpoint) over time, controlling how quickly past information is forgotten.

- **IIR Filter**: Infinite Impulse Response filter; a feedback-based filter whose output depends on both the current input and its own previous output, creating exponential smoothing.

- **Interpolator**: A component that computes weighted blends between two input values, used here for the wet/dry mix crossfade.

- **Luma**: The brightness component (Y) of a YUV video signal, representing perceived lightness independent of color.

- **Persistence**: The tendency of a signal or image to remain visible after its source has changed, here implemented as slow IIR filter adaptation.

- **Temporal Average**: A running mean of a signal computed across successive frames over time, rather than across spatial pixels within a single frame.

---
