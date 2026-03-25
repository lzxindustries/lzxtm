---
draft: true
sidebar_position: 279
slug: /instruments/videomancer/spectron
title: "Spectron"
image: /img/instruments/videomancer/spectron/spectron_hero.png
description: "Spectron is a multi-oscillator interference synthesizer that generates slowly evolving moire patterns, standing waves, and diagonal colour bands purely from the interaction of three DDS sine or square waves with the raster scan."
---

![Spectron hero image](/img/instruments/videomancer/spectron/spectron_hero_s1.png)
*Three DDS oscillators beating against the pixel clock to produce crawling diagonal moiré interference patterns and evolving geometric textures.*

---

## Overview

Spectron is a multi-oscillator interference pattern synthesizer. Three independent ***direct digital synthesis*** oscillators run at slightly different frequencies, creating complex beating patterns against the raster scan. Because the oscillators are nearly harmonic: but not quite: their combined output drifts slowly across the screen, producing hypnotic crawling moiré fringes, standing waves, and evolving geometric fields. You can think of Spectron as a digital loom, weaving diagonal stripes of light that shimmer and shift on their own.

At its simplest, Spectron produces gently undulating bands of color. At its most complex, it generates dense, crystalline interference lattices that morph in real time. The three oscillators can be summed for smooth additive textures or ring-modulated for harsh metallic harmonics. A waveform toggle switches between rounded sine contours and hard-edged square waves, and a video modulation option lets the input signal sculpt the synthesis in real time.

:::tip
Spectron is a ***synthesis*** program: it generates its own imagery from scratch. No input video is required. However, toggling **Video Mod** on lets you blend live video into the synthesis for hybrid textures.
:::

### What's In a Name?

The name ***Spectron*** carries a double meaning. The first is a nod to the EMS Spectron, an early electronic video synthesizer built in the 1970s by ***Electronic Music Studios***, the same British company responsible for the legendary VCS3 audio synthesizer. The second meaning is literal: "spectr-" (from ***spectrum***) and "-on" (the suffix used for particles and electronic instruments: like electron, positron, or Mellotron). Spectron is a spectrum machine.

---

## Quick Start

1. With all controls at their defaults, observe the slowly crawling diagonal pattern on screen. Three oscillators are already beating against one another, producing drifting fringes.
2. Turn **Osc 1 Freq** (Knob 1) slowly clockwise. The spacing of the interference bands tightens as the first oscillator's pitch rises. Turn it back and sweep slowly (watch the moiré crawl.)
3. Now adjust **Osc 2 Freq** (Knob 2) and **Osc 3 Freq** (Knob 3) independently. Each oscillator contributes its own set of diagonal stripes. When two oscillators approach similar frequencies, their patterns beat together, producing large-scale pulsing.
4. Flip the **Routing** toggle (Switch 7) to **Ring Mod** and raise **Coupling** (Knob 4). The smooth additive pattern collapses into harsher, more complex textures as the oscillator waveforms multiply together.

---

## Parameters

![Videomancer front panel with Spectron loaded](/img/instruments/videomancer/spectron/spectron_control_panel.png)
*Videomancer's front panel with Spectron active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Osc 1 Freq

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |

**Osc 1 Freq** sets the spatial frequency of the first oscillator. At 0%, the oscillator runs at its lowest pitch, producing the widest possible stripe pattern. As the value increases, the stripes become narrower and more numerous. Because the oscillator phase is computed from the screen position: horizontal pixel count plus vertical line count: the resulting pattern always forms diagonal bands across the raster.

Oscillator 1 is the "anchor" oscillator. Unlike oscillators 2 and 3, it does not drift over time; its pattern is locked to the raster and remains static when **Saturation** (Knob 5) is at zero.

---

### Knob 2 — Osc 2 Freq

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |

**Osc 2 Freq** sets the spatial frequency of the second oscillator. Its behavior mirrors **Osc 1 Freq**: higher values produce finer stripes: but oscillator 2 participates in the drift system. When **Saturation** (Knob 5) is above zero, oscillator 2's phase shifts a small amount each video frame, causing its stripe pattern to crawl across the screen.

Oscillator 2 also drives the U (blue-difference) chroma channel, painting the interference pattern in color. Adjusting Osc 2 Freq changes both the spatial pattern and the color character of the output simultaneously.

---

### Knob 3 — Osc 3 Freq

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Osc 3 Freq** sets the spatial frequency of the third oscillator. Like oscillator 2, it drifts over time: but at twice the rate. This means oscillator 3's stripes crawl faster than oscillator 2's, creating a constantly evolving phase relationship between all three layers.

Oscillator 3 drives the V (red-difference) chroma channel. The three-oscillator combination: one for luminance anchoring, one for cool-toned drift, one for warm-toned drift: is what gives Spectron its signature slowly rotating color fields.

:::tip
Try setting all three oscillator frequencies to nearly equal values. The close-but-not-identical frequencies produce large, slow-moving ***beats*** (enormous moiré shapes that drift across the entire screen.)
:::

---

### Knob 4 — Coupling

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 25% |

**Coupling** controls the depth of oscillator interaction in **Ring Mod** mode. At 0%, the ring modulation product is silent. As coupling increases, the three-way multiplicative product: oscillator 1 times oscillator 2 times oscillator 3: becomes louder and more complex. At 100%, the full ring modulation signal is present.

:::note
Coupling has no effect in **Sum** mode (Switch 7 set to **Sum**). In Sum mode, the three oscillators are added together directly and the Coupling parameter is bypassed.
:::

---

### Knob 5 — Saturation

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |

**Saturation** controls the drift speed of the interference pattern. At 0%, the pattern is completely static: the oscillators' phases are locked to the raster position and nothing changes frame to frame. As Saturation increases, oscillators 2 and 3 accumulate a small phase offset each video frame, causing their stripe patterns to slide slowly across the screen. At 100%, the drift is at maximum speed and the pattern crawls rapidly.

The drift creates the program's signature "living" quality. Oscillator 3 always drifts at twice the rate of oscillator 2, so the two color-carrying oscillators separate and reconverge in a slow, complex dance.

:::tip
At very low Saturation values (around 5 to 15%), the pattern barely moves: it breathes. This creates meditative, slowly evolving textures ideal for ambient visual installations.
:::

---

### Knob 6 — Brightness

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Brightness** controls the color spread of the output. At 0%, the chroma channels (U and V) are driven purely by the oscillator waveforms, centered at neutral. As Brightness increases, a fixed offset is added to U and subtracted from V, pushing the color palette toward warmer tones. At 100%, the offset is at maximum strength, producing vivid tinted patterns.

The offset acts as a chroma bias: it shifts the entire color field away from neutral gray, adding a persistent tint that combines with the oscillator-driven color modulation.

---

### Switch 7 — Routing

| Property | Value |
|----------|-------|
| Off | Sum |
| On | Ring Mod |
| Default | Sum |

**Routing** selects how the three oscillators are combined. With the switch set to **Sum**, the oscillator outputs are added together. Additive combination produces smooth, layered patterns where each oscillator's stripes remain individually visible as overlapping bands. With the switch set to **Ring Mod**, the outputs are multiplied together in a three-way ***ring modulation*** chain: oscillator 1 times oscillator 2, then the result times oscillator 3. Ring modulation produces sum-and-difference frequencies, creating dense harmonic textures with a metallic, crystalline quality.

:::note
In **Sum** mode, the **Coupling** parameter (Knob 4) has no effect. In **Ring Mod** mode, Coupling scales the intensity of the multiplicative product.
:::

---

### Switch 8 — Waveform

| Property | Value |
|----------|-------|
| Off | Sine |
| On | Square |
| Default | Sine |

**Waveform** selects the oscillator waveshape. With the switch set to **Sine**, the oscillators produce smooth, rounded waveforms from a quarter-wave lookup table. The visual result is soft, flowing bands with gentle transitions between light and dark. With the switch set to **Square**, the waveforms are hard-clipped to maximum positive or negative values. The visual result is razor-sharp stripes with abrupt edges (a dramatic, high-contrast look.)

Square wave mode is especially powerful with **Ring Mod** routing, producing hard-edged checkerboard and plaid-like patterns.

---

### Switch 9 — Color Map

| Property | Value |
|----------|-------|
| Off | RGB |
| On | YUV |
| Default | RGB |

**Color Map** changes the geometric angle of the interference pattern. With the switch set to **RGB**, the oscillator phase is computed from the sum of horizontal pixel position and vertical line count, producing steep 45-degree diagonal fringes. With the switch set to **YUV**, the vertical component is halved before being added to the horizontal position, producing shallower diagonal fringes at roughly 27 degrees. The result is wider, more horizontally oriented stripes.

:::tip
Switching between **RGB** and **YUV** while the pattern drifts creates an abrupt geometric shift: the field snaps to a new angle, revealing different interference structures hidden in the same oscillator frequencies.
:::

---

### Switch 10 — Video Mod

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Video Mod** enables input video modulation of oscillator 1's amplitude. With the switch set to **Off**, oscillator 1 runs at full amplitude regardless of input. With the switch set to **On**, oscillator 1's output is scaled by the input video's luminance: bright areas drive the oscillator at full strength, while dark areas suppress it toward silence. This imprints the shape of the video source onto the synthesis pattern.

Video modulation affects both **Sum** and **Ring Mod** routing paths because oscillator 1 is the first element in both chains.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input video directly to the output, bypassing all Spectron synthesis and mixing. The sync delay pipeline still aligns timing, ensuring a clean transition. Use Bypass for instant A/B comparison between the raw input and the synthesized output.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**Mix** crossfades between the input video (dry) and the synthesized pattern (wet). At 0%, only the input video passes through. At 100%, only the synthesized pattern is visible. Intermediate values blend both signals together, allowing the oscillator pattern to be layered over live video as a translucent overlay.

:::tip
At moderate **Mix** values (around 40 to 60%), the synthesized pattern becomes a color wash that tints and textures the input video. Combined with **Video Mod**, this creates a feedback-like interaction where the video shapes the synthesis and the synthesis colors the video.
:::

---

## Background

### Direct Digital Synthesis

***Direct digital synthesis*** (DDS) is a technique for generating periodic waveforms using arithmetic instead of analog oscillators. A phase accumulator counts upward at a programmable rate, and its value is used to index a waveform lookup table: typically a sine table. The key advantage is that frequency can be set with arbitrary precision simply by changing the accumulator's increment value. In Spectron, the "accumulator" is the pixel's screen position multiplied by the frequency parameter, so the oscillator phase advances spatially across the raster rather than in time. This produces visible stripe patterns whose spatial frequency matches the oscillator setting.

### Moiré Interference

When two or more periodic patterns overlap at slightly different frequencies, they produce ***moiré interference***: large-scale beating structures that appear at the difference frequency. You've seen moiré patterns in everyday life: overlapping wire fences, folded window screens, or the shimmering bands that appear when scanning a striped shirt on a TV camera. Spectron exploits this effect deliberately. Three oscillators at different frequencies create a layered interference field where the beating between each pair of oscillators generates its own slow-moving moiré, and the three-way interaction produces even more complex evolving structures.

### Ring Modulation

***Ring modulation*** multiplies two signals together, producing outputs at the sum and difference of their input frequencies. If you multiply a 3 Hz wave by a 5 Hz wave, you get components at 2 Hz and 8 Hz: but not the original 3 Hz or 5 Hz. This creates inharmonic, metallic-sounding spectra in audio; in the visual domain, it produces dense lattice textures where the original stripe patterns are replaced by their geometric sum-and-difference products. Spectron extends this to three-way ring modulation: oscillator 1 is multiplied by oscillator 2, and that product is multiplied by oscillator 3, generating a rich web of intermodulation frequencies.


---

## Signal Flow

### Signal Flow Notes

Three interactions are central to Spectron's behavior:

1. **Oscillator-to-color mapping**: The luminance (Y) channel is driven by the combined oscillator output: either additive sum or ring modulation product. The chroma channels are driven independently by oscillators 2 (U) and 3 (V), with a color spread offset from **Brightness** (Knob 6). This means the color and brightness patterns move at different rates, creating shifting hue relationships as the oscillators drift.

2. **Asymmetric drift**: Oscillator 1 never drifts: its pattern is locked to the raster. Oscillator 2 drifts at the rate set by **Saturation** (Knob 5), and oscillator 3 drifts at twice that rate. This asymmetry ensures the three oscillators are perpetually changing their phase relationships, preventing the pattern from ever settling into a static state (as long as drift is nonzero).

3. **Two-stage ring modulation**: The ring modulation path uses two sequential multiply stages: first Osc1 × Osc2, then the result × Osc3. Each multiply generates sum-and-difference frequencies, so the second multiply operates on the intermodulation products of the first. This cascaded approach produces a much denser frequency spectrum than a single multiply would.

:::tip
**Coupling acts as a volume control for ring mod.** In Sum mode, all three oscillators contribute equally and Coupling is ignored. In Ring Mod mode, the Coupling knob is essentially the "loudness" of the three-way product (at zero, the output is silent.)
:::


---

## Exercises

These exercises progress from basic oscillator exploration to complex modulated synthesis. Each exercise introduces new controls while building on the patterns discovered in the previous one.
### Exercise 1: Crawling Moiré Fields

![Crawling Moiré Fields result](/img/instruments/videomancer/spectron/spectron_ex1_s1.png)
*Crawling Moiré Fields — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Discover the fundamental moiré interference behavior by adjusting three oscillators to produce slowly crawling diagonal stripe fields.

#### Key Concepts

- DDS oscillators produce spatial stripe patterns
- Near-harmonic frequencies create slow moiré beating
- Drift creates evolving, living patterns

#### Steps

1. **Single oscillator**: Set **Osc 2 Freq** (Knob 2) and **Osc 3 Freq** (Knob 3) fully counterclockwise (0%). Only oscillator 1 is contributing. Sweep **Osc 1 Freq** (Knob 1) from 0% to 100% (watch diagonal stripes appear and tighten.)
2. **Two-oscillator beating**: Return Osc 1 Freq to about 25%. Slowly increase Osc 2 Freq. As oscillator 2's frequency approaches oscillator 1's, large moiré shapes form and drift across the screen.
3. **Three-way interference**: Add oscillator 3 by increasing Osc 3 Freq to about 40%. The pattern becomes more intricate: three overlapping stripe fields create a lattice of interference.
4. **Drift speed**: Adjust **Saturation** (Knob 5). At low values, the pattern barely breathes. At high values, it crawls quickly. Find a speed that feels meditative.
5. **Geometric angle**: Toggle **Color Map** (Switch 9) between the two positions. Notice how the stripe angle shifts, revealing completely different moiré structures from the same oscillator settings.

#### Settings

| Control | Value |
|---------|-------|
| Osc 1 Freq | ~25% |
| Osc 2 Freq | ~30% |
| Osc 3 Freq | ~40% |
| Coupling | 0% |
| Saturation | ~20% |
| Brightness | 50% |
| Routing | Sum |
| Waveform | Sine |
| Color Map | RGB |
| Video Mod | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Ring Modulation Textures

![Ring Modulation Textures result](/img/instruments/videomancer/spectron/spectron_ex2_s1.png)
*Ring Modulation Textures — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Explore the metallic, crystalline textures produced by multiplying the oscillator waveforms together.

#### Key Concepts

- Ring modulation creates sum-and-difference frequencies
- Coupling scales the ring mod depth
- Square waves produce hard-edged checkerboard lattices

#### Steps

1. **Enter ring mod**: Flip **Routing** (Switch 7) to **Ring Mod**. The smooth additive pattern may vanish (ring modulation at low coupling is silent.)
2. **Raise coupling**: Increase **Coupling** (Knob 4) until the pattern reappears. The texture is denser and more geometric than additive mode (notice the lattice-like quality.)
3. **Frequency sweep**: Slowly adjust **Osc 1 Freq** while watching the ring mod pattern. The intermodulation products shift in unexpected ways: frequencies that felt smooth in Sum mode become jagged and complex.
4. **Square waves**: Toggle **Waveform** (Switch 8) to **Square**. The ring modulation of square waves produces hard-edged plaid and checkerboard patterns with razor-sharp boundaries.
5. **Color sweep**: Increase **Brightness** (Knob 6) to push color into the ring mod texture. The chroma offset tints the pattern in warm or cool hues.
6. **Return to sine**: Toggle Waveform back to **Sine** and compare. Sine ring mod is smoother, more organic. Square ring mod is architectural, rigid.

#### Settings

| Control | Value |
|---------|-------|
| Osc 1 Freq | ~40% |
| Osc 2 Freq | ~50% |
| Osc 3 Freq | ~65% |
| Coupling | ~80% |
| Saturation | ~30% |
| Brightness | 60% |
| Routing | Ring Mod |
| Waveform | Square |
| Color Map | RGB |
| Video Mod | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Video-Modulated Synthesis

![Video-Modulated Synthesis result](/img/instruments/videomancer/spectron/spectron_ex3_s1.png)
*Video-Modulated Synthesis — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Use a live video input to shape and blend with the oscillator pattern, creating a hybrid of synthesis and camera imagery.

#### Key Concepts

- Video modulation imprints input imagery onto the synthesis
- Mix crossfade blends synthesis over live video
- Combining modulation and mix creates layered hybrid textures

#### Steps

1. **Connect video**: Ensure a video source is connected to Videomancer's input. Flip **Bypass** (Switch 11) on to confirm the input signal, then flip it off.
2. **Pure synthesis**: With **Video Mod** (Switch 10) off and **Mix** (Fader 12) at 100%, set up an interesting oscillator pattern using Knobs 1 through 3. The output is pure synthesis.
3. **Enable video mod**: Toggle **Video Mod** on. The oscillator 1 amplitude is now sculpted by the input video's brightness: bright areas of the video source "punch through" the synthesis, while dark areas suppress it.
4. **Blend with mix**: Lower **Mix** (Fader 12) to about 50%. The input video becomes visible underneath the synthesis pattern, creating a colored-glass overlay effect.
5. **Shape the overlay**: Adjust **Saturation** (Knob 5) to control how fast the overlay crawls. Adjust **Brightness** (Knob 6) to tint the overlay color.
6. **Ring mod hybrid**: Switch **Routing** to **Ring Mod** and raise **Coupling**. The video-modulated ring texture creates complex, input-reactive structures impossible with either video or synthesis alone.

#### Settings

| Control | Value |
|---------|-------|
| Osc 1 Freq | ~40% |
| Osc 2 Freq | ~35% |
| Osc 3 Freq | ~60% |
| Coupling | ~50% |
| Saturation | ~25% |
| Brightness | 50% |
| Routing | Sum |
| Waveform | Sine |
| Color Map | RGB |
| Video Mod | On |
| Bypass | Off |
| Mix | ~50% |

---
## Glossary

- **Beat Frequency**: The slow pulsation that appears when two periodic signals at slightly different frequencies combine; equal to the difference between the two frequencies.

- **Coupling**: The depth or intensity of interaction between two or more oscillators, controlling how strongly one modulates or multiplies another.

- **Direct Digital Synthesis (DDS)**: A technique for generating periodic waveforms using a phase accumulator and lookup table rather than analog circuitry.

- **Drift**: A slow, continuous change in oscillator phase over time, causing spatial patterns to crawl across the screen.

- **Interference**: The phenomenon that occurs when two or more periodic patterns overlap, producing visible beating structures at their sum and difference frequencies.

- **Moiré**: A large-scale visual pattern created by the interference of two or more overlapping periodic structures; named after the wavy appearance of moiré silk fabric.

- **Phase**: The current position within a periodic waveform's cycle, typically measured from 0 to 360 degrees or 0 to 2π radians.

- **Raster**: The pattern of horizontal scan lines that compose a video frame, traced left to right, top to bottom.

- **Ring Modulation**: Multiplying two signals together, producing output components at the sum and difference of their input frequencies while suppressing the originals.

- **Spatial Frequency**: The number of cycles of a periodic pattern per unit of screen distance; higher spatial frequency means finer, more closely spaced stripes.

---
