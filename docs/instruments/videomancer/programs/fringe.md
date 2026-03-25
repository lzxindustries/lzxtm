---
draft: true
sidebar_position: 123
slug: /instruments/videomancer/fringe
title: "Fringe"
image: /img/instruments/videomancer/fringe/fringe_hero_s1.png
description: "Before the era of component video and digital interfaces, nearly all consumer video passed through a single wire — the composite cable."
---

![Fringe hero image](/img/instruments/videomancer/fringe/fringe_hero_s1.png)
*Fringe simulating NTSC composite artifact color on a high-contrast source, producing rainbow fringes, dot crawl shimmer, and chroma smear at sharp luminance edges.*

---

## Overview

Fringe is a composite video artifact simulator. It recreates the strange, beautiful color phenomena that defined the look of early home computers, game consoles, and VHS tapes: not by applying a color filter, but by actually re-encoding your video into a simulated ***composite signal*** and then imperfectly decoding it. The decoding errors are the point: color appears where none was intended, edges shimmer with wandering dots, and fine patterns dissolve into rainbows.

At subtle settings, Fringe adds a gentle analog warmth: a soft haze of color fringing at edges and a slight horizontal smear to chroma detail. At extreme settings, it transforms clean digital video into a vivid hallucination of false color, with chroma bleeding across the screen and the subcarrier pattern visibly crawling through every frame.

:::tip
Fringe is a ***processing*** program. It transforms an incoming video signal: the richer and sharper the source, the more dramatic the artifacts. High-contrast edges and fine textures produce the strongest effects.
:::

### What's In a Name?

The name ***Fringe*** refers to ***color fringing***, the false color halos that appear at sharp luminance transitions when a composite video decoder mistakes luma detail for chroma information. It also evokes the idea of operating at the fringes of signal integrity: the boundary where a clean picture starts to break down and something unexpected emerges.

---

## Quick Start

1. Turn **Artifact** (Knob 1) fully clockwise. You should see rainbow-colored halos blooming at every sharp edge in the image (this is the composite modulation at full strength.)
2. Slowly sweep **Subcarrier** (Knob 2) from left to right. The spacing and color of the fringes change as the simulated carrier frequency shifts. Find a sweet spot where the fringing is visible but not overwhelming.
3. Adjust **Chroma BW** (Knob 3) to control how much the false color smears horizontally. Lower values produce tighter, more defined color artifacts; higher values blur the chroma into wide, soft bands.
4. Set **Mix** (Fader 12) to about halfway and compare the processed signal with the dry input as you sweep the fader back and forth.

---

## Parameters

![Videomancer front panel with Fringe loaded](/img/instruments/videomancer/fringe/fringe_control_panel.png)
*Videomancer's front panel with Fringe active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Artifact

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Artifact** controls the depth of composite modulation: how much chroma information is mixed into the simulated composite signal before separation. At 0%, no chroma is modulated onto the carrier, so the decoder sees only luma and produces no color artifacts. As you increase Artifact, the quadrature-modulated chroma component grows stronger, and the imperfect Y/C separator begins generating visible fringing, rainbow moiré, and false color. At 100%, the modulation is at full depth, producing dramatic composite artifacts across the entire image.

The modulation is implemented as a shift-and-add approximation using the top three bits of the control value, which means the response has slight staircase quantization rather than being perfectly smooth. In practice, you'll find the sweet spot somewhere between 40% and 80%, depending on source content.

---

### Knob 2 — Subcarrier

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Subcarrier** sets the spatial frequency of the simulated color subcarrier oscillator. In real NTSC, the color subcarrier runs at exactly 3.579545 MHz: a frequency carefully chosen to interleave with the luma spectrum. Fringe replaces that fixed frequency with a ***direct digital synthesis*** (DDS) accumulator that you control.

At low values, the subcarrier completes fewer cycles per scan line, producing wide, slow-moving fringe patterns. At high values, the subcarrier runs fast, creating fine, tightly spaced color bands that more closely resemble real NTSC artifacts. The subcarrier frequency also determines the spacing of dot crawl and the pitch of rainbow moiré patterns on fine textures.

:::note
The DDS accumulator resets at the start of each scan line, so the subcarrier phase is always coherent within a line. Between lines, the phase relationship depends on the **Dot Crawl** setting.
:::

---

### Knob 3 — Chroma BW

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Chroma BW** adjusts the cutoff frequency of the ***IIR lowpass filter*** used during chroma demodulation. This filter determines how much of the extracted chroma signal passes through to the output (it is the bandwidth of the chroma decoder.)

At 0%, the filter tracks the input instantly with no smoothing, passing every high-frequency chroma fluctuation through to the output. This produces sharp, noisy color artifacts with hard edges. As you increase Chroma BW, the filter responds more slowly, blurring the demodulated chroma horizontally. At 100%, the filter has maximum smoothing, producing soft, wide bands of color that smear across edges like paint dragged with a wet brush.

The control is quantized into four levels internally. Each level doubles the smoothing by shifting the IIR step size one bit to the right.

---

### Knob 4 — Dot Crawl

| Property | Value |
|----------|-------|
| Range | 0 – 7 |
| Default | 2 |

**Dot Crawl** sets the per-frame subcarrier phase offset that produces the characteristic wandering-dot pattern seen on color boundaries in NTSC video. In a real composite signal, the subcarrier phase alternates between frames, causing color transition dots to shift position and appear to "crawl" along edges.

This control has eight discrete steps (0 to 7). At step 0, the subcarrier phase resets identically every frame and the dot pattern is static. At higher steps, a progressively larger phase offset is loaded into the DDS accumulator at each vertical sync, causing the dot pattern to shift by a larger amount per frame. Higher values produce faster crawl and more agitated shimmer at color boundaries.

:::tip
Dot crawl is most visible on sharp horizontal color transitions. Try it with a source that has strong vertical edges between differently colored regions: the crawling dots will be clearly visible along those boundaries.
:::

---

### Knob 5 — Luma Notch

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Luma Notch** controls how aggressively the Y/C separator removes chroma residue from the extracted luminance channel. In a real composite decoder, a ***notch filter*** is used to reject the color subcarrier from the luma path: but a stronger notch also removes legitimate luma detail at that frequency, softening the picture.

The control blends between the original (unfiltered) luma and the comb/notch-filtered luma estimate in four steps. At 0%, the original luma passes through untouched: maximum sharpness, but any subcarrier residue shows through as visible dot patterns in the brightness channel. At about 33%, a 50/50 blend between original and estimated luma. At about 66%, the estimated luma dominates (75% estimated, 25% original). At 100%, the filtered estimate completely replaces the original luma: cleanest separation, but softest picture.

---

### Knob 6 — Cross Color

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Cross Color** amplifies the extracted chroma signal before demodulation, boosting false color artifacts. In real composite video, ***cross-color*** is the phenomenon where fine luma detail (like the pattern on a striped shirt) is misinterpreted as color information by the decoder, producing shimmering rainbow patterns.

The control has four effective levels. At 0%, the extracted chroma passes through at unity gain. At about 33%, the signal is boosted by 25%. At about 66%, a 50% boost. At 100%, the chroma is doubled. Higher cross-color settings exaggerate rainbow moiré on fine textures and make color fringing at edges more saturated and vivid.

:::warning
At high Cross Color settings with a high Artifact level, the color artifacts can become very intense: fully saturated false color bands that dominate the image. Dial back Artifact or increase Chroma BW to tame the effect.
:::

---

### Switch 7 — Standard

| Property | Value |
|----------|-------|
| Off | NTSC |
| On | PAL |
| Default | NTSC |

**Standard** selects between NTSC and PAL composite encoding behavior. With the switch set to **NTSC**, the subcarrier phase is consistent across all lines. With the switch set to **PAL**, the V-axis phase alternates on every other scan line: a technique real PAL systems use to cancel hue errors. In Fringe, the PAL mode produces a different pattern of color artifacts: vertical fringing tends to cancel out, and the visible artifact structure becomes more symmetrical. The NTSC mode produces the classic one-sided color fringing familiar from American home computers and game consoles.

---

### Switch 8 — Comb Filter

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Comb Filter** selects between two Y/C separation algorithms. With the switch set to **Off**, a simple two-sample notch filter estimates luma by averaging adjacent composite samples. This is the primitive approach used by inexpensive decoders: it works, but it bleeds luma detail into the chroma path and vice versa. With the switch set to **On**, a three-sample ***comb filter*** uses the current sample plus two delayed samples to more accurately separate Y and C. The comb filter produces cleaner separation with fewer cross-color artifacts, but it can introduce vertical softening because it averages across multiple subcarrier cycles.

:::tip
The comb filter dramatically reduces rainbow moiré artifacts. Toggle it on and off while viewing a high-detail source to hear the difference: er, ***see*** the difference: between cheap and decent composite decoding.
:::

---

### Switch 9 — Mono Source

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Mono Source** strips all incoming chroma information before composite encoding, treating the input as a monochrome signal. With the switch set to **Off**, the full-color input (Y, U, and V) is modulated onto the composite carrier. With the switch set to **On**, U and V offsets are forced to zero before modulation, so only luma enters the composite encoder.

This simulates the scenario that made Apple II artifact color famous: a monochrome signal where all color comes from the encoding/decoding artifacts themselves. Sharp luma transitions at the right spatial frequency trick the decoder into seeing colors that were never in the original signal.

---

### Switch 10 — Edge Boost

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Edge Boost** applies a first-order high-frequency emphasis to the luma channel before composite encoding. With the switch set to **Off**, the input luma passes through unchanged. With the switch set to **On**, the difference between the current pixel and the previous pixel is added to the current value, sharpening transitions and exaggerating edges. The result is clamped to the valid range (0 to 1023).

Because composite artifacts are most visible at sharp transitions, boosting edges before encoding significantly increases the intensity of color fringing and rainbow moiré. Edge Boost turns subtle effects into dramatic ones.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Fringe processing stages. The sync delay pipeline still aligns timing, so the transition is glitch-free. Use Bypass for instant A/B comparison between the raw input and the artifact-processed result.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (original) and wet (processed) signal. At 0%, the output is 100% dry: the original, unprocessed input video. At 100%, the output is 100% wet: the fully artifact-processed signal with all composite encoding, Y/C separation, and chroma demodulation applied. Intermediate positions blend the two proportionally, allowing you to dial in exactly the right amount of composite character.

:::tip
Mix is useful for subtle effects. Even a small amount of wet signal (10–20%) adds a gentle analog warmth to clean digital video: a hint of color fringing at edges without overwhelming the image.
:::

---

## Background

### Composite video and its artifacts

Before component video and HDMI separated brightness from color, television signals traveled as a single ***composite*** waveform. In the NTSC system adopted by the United States in 1953, the color information (chroma) was encoded as a high-frequency signal modulated onto the ***color subcarrier*** at 3.579545 MHz, then added on top of the brightness (luma) signal. The receiver's decoder had to separate these two interleaved components (and that separation was never perfect.)

The artifacts of imperfect Y/C separation became a defining aesthetic of early video technology. CRT televisions, VHS tapes, game consoles, and home computers all displayed characteristic color fringing, rainbow patterns, and crawling dots that were technically errors: but which generations of viewers absorbed as the natural look of video. Fringe recreates that look by simulating the encode-decode process inside the FPGA.

### Quadrature modulation

Composite encoding uses ***quadrature amplitude modulation (QAM)*** to pack two color signals into one carrier. The U (blue-difference) and V (red-difference) components are each multiplied by a carrier wave at 90-degree phase offsets: one by cosine, the other by sine. The resulting modulated signals are summed with the luma to form the composite waveform.

Fringe implements this with a four-phase pattern driven by a DDS accumulator. The top two bits of the accumulator select one of four quadrature phases: +V, +U, −V, −U. This discrete four-phase approach is a classic FPGA technique: no sine lookup table is needed, just sign selection and multiplexing.

### Comb filtering and notch filtering

Separating Y from C in a composite signal is an inherently lossy process. Two main approaches exist:

A ***notch filter*** removes a narrow band of frequencies centered on the subcarrier from the composite signal, yielding an estimate of luma. Everything rejected by the notch is assumed to be chroma. This is simple but crude: legitimate luma detail near the subcarrier frequency is lost, and chroma extraction is noisy.

A ***comb filter*** exploits the fact that the subcarrier phase alternates between adjacent samples. By averaging the current composite sample with samples from exactly one subcarrier cycle earlier and later, the chroma component cancels out (because it alternates sign), leaving clean luma. The chroma is recovered from the difference. Comb filtering produces much cleaner separation but requires a delay line and works best when the picture doesn't change too rapidly between the averaged samples.

Fringe provides both methods, selectable via the **Comb Filter** toggle.

### IIR lowpass demodulation

After Y/C separation, the extracted chroma must be demodulated: the quadrature modulation reversed to recover U and V. Fringe demodulates by reversing the sign of the extracted chroma based on the subcarrier phase, then runs each axis (U and V) through a single-pole ***infinite impulse response (IIR) lowpass filter***.

The IIR filter smooths the demodulated chroma over time, averaging out the subcarrier oscillation to reveal the underlying color signal. The **Chroma BW** control adjusts the filter's step size: a larger step means faster tracking (sharper color, more noise), while a smaller step means slower tracking (smoother color, more smear). The filter state resets at the start of each scan line to prevent color from bleeding across line boundaries.


---

## Signal Flow

### Signal Flow Notes

The core idea is encode-then-decode: the input YUV video is first composite-encoded by modulating U and V onto a DDS-driven subcarrier using quadrature phase selection, then the composite signal is separated back into Y and C using either a comb filter or a simple notch filter. The separation is intentionally imperfect, governed by user controls, and the errors in separation *are* the desired artifacts.

Two interactions are especially important. First, the **Artifact** and **Subcarrier** controls together determine the raw character of the composite encoding: Artifact sets how much chroma lands on the carrier, and Subcarrier sets the carrier's spatial frequency. Second, the **Luma Notch** and **Chroma BW** controls operate on opposite sides of the Y/C boundary: one cleans up luma at the cost of detail, the other smooths chroma at the cost of sharpness. Balancing these four controls defines the overall artifact profile.

:::note
The chroma IIR filters reset at the beginning of every scan line. This means color artifacts cannot bleed from one line to the next: each line is demodulated independently, matching the behavior of real line-by-line composite decoders.
:::


---

## Exercises

These exercises progress from basic composite artifact exploration to advanced creative techniques. Each one engages a different subset of Fringe's controls to highlight a specific aspect of composite video behavior.
### Exercise 1: Classic Composite Look

![Classic Composite Look result](/img/instruments/videomancer/fringe/fringe_ex1_s1.png)
*Classic Composite Look — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Recreate the look of watching a sharp digital source through a vintage composite video decoder (soft color fringing at edges with gentle chroma smear.)

#### Key Concepts

- Composite modulation creates color fringing at sharp edges
- Subcarrier frequency determines the spacing of fringe patterns
- Chroma bandwidth controls horizontal color smear

#### Video Source

A live camera feed or recorded footage with strong, well-defined edges and varied colors: text overlays, geometric shapes, or architectural subjects with clean lines.

#### Steps

1. **Engage the encoder**: Turn **Artifact** (Knob 1) to about 60%. Faint rainbow fringes should appear at sharp edges in the image.
2. **Find the carrier**: Sweep **Subcarrier** (Knob 2) slowly. At low values, the fringe bands are wide and obvious. At high values, they become fine and tight. Find a mid-range setting where the fringes resemble real composite artifacts.
3. **Soften the chroma**: Increase **Chroma BW** (Knob 3) to about 70%. The color fringes blur into soft halos, simulating the bandwidth-limited chroma path of a real decoder.
4. **Clean up luma**: Set **Luma Notch** (Knob 5) to about 50%. The brightness channel loses a little sharpness, but subcarrier dot patterns disappear from the luma.
5. **Compare**: Sweep **Mix** (Fader 12) back and forth to compare the composite look against the clean original.

#### Settings

| Control | Value |
|---------|-------|
| Artifact | 60% |
| Subcarrier | 50% |
| Chroma BW | 70% |
| Dot Crawl | 0 |
| Luma Notch | 50% |
| Cross Color | 0% |
| Standard | NTSC |
| Comb Filter | Off |
| Mono Source | Off |
| Edge Boost | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Apple II Artifact Color

![Apple II Artifact Color result](/img/instruments/videomancer/fringe/fringe_ex2_s1.png)
*Apple II Artifact Color — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Simulate the iconic Apple II artifact color phenomenon: a monochrome source that produces vivid false colors purely through composite encoding errors.

#### Key Concepts

- Monochrome signals can produce false color through composite encoding artifacts
- Edge boost intensifies the fringing by sharpening transitions before encoding
- Cross-color amplification exaggerates rainbow moiré

#### Video Source

High-contrast black-and-white footage or a test pattern with fine vertical stripes and sharp geometric edges. The CGA Artifact preset is a good starting point.

#### Steps

1. **Strip color**: Enable **Mono Source** (Switch 9). All incoming chroma is zeroed (only brightness enters the composite encoder.)
2. **Full artifacts**: Turn **Artifact** (Knob 1) to about 90%. Vivid false colors appear at edges and on fine textures (colors that were never in the original signal.)
3. **Sharpen edges**: Enable **Edge Boost** (Switch 10). The first-order emphasis exaggerates every luma transition, dramatically increasing the false color intensity.
4. **Boost cross-color**: Turn **Cross Color** (Knob 6) to about 70%. The rainbow moiré on fine textures becomes more saturated and vivid.
5. **Adjust subcarrier**: Sweep **Subcarrier** (Knob 2) to change which pixel patterns produce which colors. Different frequencies create entirely different color palettes from the same monochrome source.
6. **Try PAL**: Toggle **Standard** (Switch 7) to PAL. The artifact pattern changes because PAL alternates the V-axis phase on alternate lines, partially canceling certain fringe colors.

#### Settings

| Control | Value |
|---------|-------|
| Artifact | 90% |
| Subcarrier | 50% |
| Chroma BW | 50% |
| Dot Crawl | 0 |
| Luma Notch | 50% |
| Cross Color | 70% |
| Standard | NTSC |
| Comb Filter | Off |
| Mono Source | On |
| Edge Boost | On |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Animated Dot Crawl

![Animated Dot Crawl result](/img/instruments/videomancer/fringe/fringe_ex3_s1.png)
*Animated Dot Crawl — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Generate visible, animated dot crawl along color boundaries (the wandering dot pattern familiar from NTSC television.)

#### Key Concepts

- Dot crawl is caused by frame-to-frame subcarrier phase offset
- The comb filter reduces cross-color artifacts but introduces vertical softening
- PAL and NTSC produce different dot crawl patterns

#### Video Source

Footage with strong, saturated color boundaries: a red shape on a blue background, color bars, or a graphic with large flat-colored regions meeting at clean edges.

#### Steps

1. **Moderate artifacts**: Set **Artifact** (Knob 1) to about 50% and **Subcarrier** (Knob 2) to about 50%.
2. **Engage dot crawl**: Turn **Dot Crawl** (Knob 4) up from 0 to about step 3 or 4. Watch the edges of color regions carefully: small dots should visibly shift position from frame to frame, crawling along the boundaries.
3. **Increase dot crawl speed**: Continue increasing Dot Crawl to higher steps. The crawling accelerates and becomes more agitated.
4. **Comb filter comparison**: Enable **Comb Filter** (Switch 8). The dot crawl pattern should become cleaner and more defined as cross-color rainbow artifacts are suppressed by the three-sample comb.
5. **NTSC vs. PAL**: Toggle **Standard** (Switch 7) between NTSC and PAL. PAL's line-alternating phase produces a different crawl structure: the dots may appear to cancel vertically rather than crawl horizontally.
6. **Wet/dry blend**: Pull **Mix** (Fader 12) down to about 30% to add just a hint of animated dot crawl texture to the original image.

#### Settings

| Control | Value |
|---------|-------|
| Artifact | 50% |
| Subcarrier | 50% |
| Chroma BW | 50% |
| Dot Crawl | 4 |
| Luma Notch | 30% |
| Cross Color | 30% |
| Standard | NTSC |
| Comb Filter | On |
| Mono Source | Off |
| Edge Boost | Off |
| Bypass | Off |
| Mix | 100% |

---
## Glossary

- **Chroma**: The color information in a video signal, encoded as U (blue-difference) and V (red-difference) components in YUV color space.

- **Comb Filter**: A Y/C separation technique that uses delayed samples to exploit the subcarrier's phase alternation, canceling chroma in the luma path and extracting cleaner color.

- **Composite Video**: An analog video format where brightness (luma) and color (chroma) are combined into a single signal by modulating chroma onto a high-frequency subcarrier.

- **Cross-Color**: A composite video artifact where fine luma detail near the subcarrier frequency is falsely interpreted as color information, producing rainbow patterns on textured areas.

- **DDS (Direct Digital Synthesis)**: A method for generating waveforms by incrementing a digital accumulator at a programmable rate, producing precise and tunable frequency output.

- **Dot Crawl**: Visible wandering dots at color boundaries caused by frame-to-frame subcarrier phase offset in composite video, appearing as a shimmering edge effect.

- **IIR (Infinite Impulse Response)**: A type of digital filter that uses feedback from its own output, providing efficient lowpass filtering with minimal hardware resources.

- **Luma**: The brightness component (Y) of a YUV video signal, representing perceived lightness independent of color.

- **Notch Filter**: A band-reject filter that removes a narrow range of frequencies, used in composite decoders to strip the subcarrier from the luma channel.

- **QAM (Quadrature Amplitude Modulation)**: A modulation technique that encodes two independent signals onto a single carrier by using cosine and sine (90-degree phase offset) components.

- **Subcarrier**: A secondary carrier wave at a specific frequency used to encode color information within the composite video signal; 3.58 MHz for NTSC, 4.43 MHz for PAL.

---
