---
draft: false
sidebar_position: 3
slug: /instruments/videomancer/lumarian
title: "Lumarian"
---

import lumarian_hero from '/img/instruments/videomancer/lumarian/lumarian_hero.png';
import lumarian_proc_amp_reference from '/img/instruments/videomancer/lumarian/lumarian_proc_amp_reference.jpg';
import lumarian_control_panel from '/img/instruments/videomancer/lumarian/lumarian_control_panel.png';
import lumarian_gamma_curves from '/img/instruments/videomancer/lumarian/lumarian_gamma_curves.png';
import lumarian_edge_modes from '/img/instruments/videomancer/lumarian/lumarian_edge_modes.png';
import lumarian_exercise2_result from '/img/instruments/videomancer/lumarian/lumarian_exercise2_result.png';
import lumarian_exercise3_result from '/img/instruments/videomancer/lumarian/lumarian_exercise3_result.png';

# Lumarian

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={lumarian_hero} alt="Lumarian processed video output showing edge enhancement and luminance keying on a natural source"/>

*Lumarian applies tonal control, edge enhancement, and luminance keying to any video source in real time.*

---

## Overview

Every video image is made of three things: how bright each pixel is (luminance), what color it is (chrominance), and where the edges between regions fall. Lumarian gives you direct, real-time control over all three.

The program chains six processing stages together — contrast, brightness, saturation, gamma correction, edge enhancement, and luminance keying — and runs them simultaneously on every pixel of every frame. The name comes from *luminance*, the measurable brightness of light, which is the central quantity this program manipulates.

At one end of the spectrum, Lumarian can do straightforward image correction: fix a washed-out camera feed, sharpen soft footage, or pull a clean key from high-contrast material. At the other end, pushing the edge enhancer and gamma controls past their "correct" ranges produces entirely new graphic textures. The same signal chain does both — the difference is just how far you turn the knobs.

---

## Background

<img src={lumarian_proc_amp_reference} alt="Master control room of a Japanese broadcasting station, 1961"/>

*The processing amplifier — ancestor of Lumarian's tonal controls — was standard equipment in every television facility. Photo by Project Kei, CC BY-SA 4.0, via [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Master_room_1961-01.jpg).*

### What Is a Processing Amplifier?

Before a television signal left a broadcast station, it passed through a piece of equipment called a **processing amplifier** (or "proc amp"). The proc amp's job was to standardize the signal — adjusting contrast, brightness, and color saturation so that every camera, tape deck, and satellite feed looked consistent on air. Lumarian's Contrast, Brightness, and Saturation controls do exactly what a proc amp did, except digitally, operating in the YUV color space at 10-bit precision with no signal degradation.

### What Is Gamma Correction?

The Gamma control reshapes the *transfer curve* that maps input brightness values to output brightness values. Think of it this way: if you graphed "input brightness" on the x-axis and "output brightness" on the y-axis, a straight diagonal line would mean no change. Gamma bends that line into a curve — exponential (which crushes shadows and stretches highlights) or logarithmic (which lifts shadows and compresses highlights). This technique originates from the physics of CRT displays, which had a naturally nonlinear response to voltage. Lumarian lets you crossfade between both curve shapes in real time.

### What Is Edge Enhancement?

Lumarian's edge enhancement chain descends from a broadcast technique called **aperture correction**. Here is how it works: a high-pass filter extracts the spatial detail (the edges) from the luminance channel, a gain stage amplifies that detail, and the result is mixed back into the original signal. At modest settings, this simply sharpens the picture — exactly what broadcast engineers used it for. But at higher gains, the edge signal starts to overpower the source, and edges become bold graphic elements rather than subtle corrections. A rectifier with eight selectable modes (controlled by three toggle switches) determines the shape of the edge signal, turning a corrective tool into a creative one.

### What Is a Luminance Key?

The Luma Blank fader implements one of the oldest techniques in video: the **luminance key**. It sets a brightness threshold — every pixel darker than the threshold is replaced with pure black, and every pixel brighter than the threshold passes through untouched. Television engineers used luminance keys to isolate bright objects (white text on a dark background, for example) and composite them over other sources.

---

## Signal Flow

One of the most important things to understand about any signal processing chain is the **order of operations**. Each stage transforms the signal before passing it to the next, so changing an upstream control alters what every downstream stage "sees." The diagram below shows exactly how Lumarian routes the three YUV channels:

```
Input Video (YUV 4:4:4)
│
├── Y Channel ──────────────────────────────────────────────────
│   │
│   ├─ 1. Contrast / Brightness  (proc amp)
│   ├─ 2. Gamma Correction       (exponential ↔ logarithmic curve)
│   ├─ 3. Edge Enhancement       (high-pass filter → rectifier → gain mix)
│   ├─ 4. Luma Invert            (bitwise complement)
│   └─ 5. Luma Blank             (threshold key → black below cutoff)
│
├── U Channel ──────────────────────────────────────────────────
│   ├─ 1. Chroma Invert          (bitwise complement)
│   ├─ 2. Saturation             (proc amp around midpoint)
│   └─ 3. Delay Alignment        (compensates for Y processing latency)
│
├── V Channel ──────────────────────────────────────────────────
│   ├─ 1. Chroma Invert          (bitwise complement)
│   ├─ 2. Saturation             (proc amp around midpoint)
│   └─ 3. Delay Alignment        (compensates for Y processing latency)
│
└── Sync Signals ───────────────────────────────────────────────
    └─ Delay Alignment           (matched to total pipeline depth)
```

Notice that the Y channel has more processing stages than U and V. If all three channels arrived at the output at different times, the color would be misaligned with the brightness — you would see color fringes on every edge. To prevent this, the chroma and sync signals pass through **delay lines** that add exactly enough latency to match the Y channel. This alignment happens automatically inside the FPGA.

---

## Parameter Reference

<img src={lumarian_control_panel} alt="Videomancer front panel with Lumarian loaded, controls annotated"/>

*Videomancer's front panel with Lumarian active. Knobs 1–6 (rotary potentiometers), Switches 7–11 (toggles), and Fader 12 (linear potentiometer) are labeled with their Lumarian functions on the LCD screen.*

The sections below describe each physical control and what it does to the signal. Pay attention to the default values — they tell you where "no effect" is for each parameter.

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Contrast
| Property | Value |
|----------|-------|
| Range | 0.0% – 200.0% |
| Default | 100.0% (center) |
| Suffix | % |

Contrast is a **gain** control — it multiplies the luminance value of every pixel. At 100% (center), the multiplication factor is 1.0, so the signal passes unchanged. Turn clockwise and the factor increases: highlights get brighter while blacks stay anchored at zero. Turn counter-clockwise and the factor decreases: the entire image compresses toward black. At 0%, every pixel is black regardless of input. At 200%, every luminance value is doubled (and values that exceed the maximum are clipped).

---

#### Knob 2 — Brightness
| Property | Value |
|----------|-------|
| Range | −1.000 – 1.000 |
| Default | 0.000 (center) |

Brightness is a **DC offset** — it adds or subtracts a constant value from every pixel's luminance. Where Contrast scales the range (multiplication), Brightness shifts it (addition). Positive values lift the whole image uniformly; negative values push it darker. This is the control to reach for when your black level is wrong — turn counter-clockwise to restore solid blacks, or clockwise if shadow detail has been lost.

---

#### Knob 3 — Saturation
| Property | Value |
|----------|-------|
| Range | 0.0% – 200.0% |
| Default | 100.0% (center) |
| Suffix | % |

Saturation scales the U and V chrominance channels around their neutral midpoint. Because the scaling is centered on the midpoint (not zero), reducing saturation moves colors toward gray rather than toward a tinted value. At 0%, the output is purely monochrome — only the Y channel contributes. At 100%, color passes unchanged. At 200%, every color's distance from neutral is doubled, producing vivid, exaggerated hues.

---

#### Knob 4 — Gamma
| Property | Value |
|----------|-------|
| Range | −2.000 – 2.000 |
| Default | 0.000 (center) |

<img src={lumarian_gamma_curves} alt="Gamma curve illustration showing exponential, linear, and logarithmic transfer curves"/>

*The Gamma control crossfades between three tonal responses. Left: logarithmic (shadows lifted). Center: linear (unity). Right: exponential (shadows crushed).*

Gamma reshapes the **transfer curve** that converts input luminance to output luminance. At center (0.000), the curve is a straight line — output equals input. Turning clockwise bends the curve downward (exponential), which darkens shadows and midtones while leaving the brightest highlights relatively unchanged. Turning counter-clockwise bends it upward (logarithmic), which lifts shadows and compresses highlights.

Here is why this matters for the rest of the chain: edge enhancement runs *after* gamma. So if you darken midtones with gamma, edges in the shadow region become less prominent, while edges near highlights become more pronounced. This interaction gives you selective control over which parts of the image produce the strongest edge signals.

---

#### Knob 5 — Edge Gain
| Property | Value |
|----------|-------|
| Range | 0.0% – 400.0% |
| Default | 0.0% (fully CCW) |
| Suffix | % |

This control sets how much of the extracted edge signal gets mixed back into the Y channel. At 0%, no edge enhancement is applied at all — the edge processing chain is effectively off. As you increase the value, transitions in the image appear sharper and more defined. Past about 100%, the edge signal starts to become as strong as the original image content. Past 200%, edges dominate the output and the original tonal information recedes into the background. At 400%, you are looking almost entirely at the edge signal itself.

For reference: broadcast aperture correction typically used the equivalent of 10–30%. Anything above 100% is firmly in creative territory.

---

#### Knob 6 — Edge Cutoff
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% (fully CCW) |
| Suffix | % |

Edge Cutoff sets the **bandwidth** of the high-pass filter that extracts edges from the Y channel. At 0%, the filter passes nothing — no edge signal is produced regardless of the Edge Gain setting. As you turn clockwise, the filter begins passing spatial frequencies, starting with the finest detail. Higher values widen the passband to include broader transitions and larger-scale contours.

Edge Cutoff and Edge Gain work as a pair: Cutoff selects *which* edges are extracted, and Gain controls *how strongly* they appear. A useful experiment is to set Edge Gain to 200% or higher and then slowly sweep Edge Cutoff from minimum to maximum, watching how the character of the edge signal changes.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Luma Invert** | Normal luminance | Luminance inverted (negative) |
| **8 — Chroma Invert** | Normal hues | All hues shifted ~180° |
| **9 — Edge Invert** | Normal edge polarity | Edge polarity inverted |
| **10 — Edge Rectify** | Normal edge polarity | Edge polarity flipped |
| **11 — Edge Select** | Single (standard) | Both (full-wave rectification) |

**Luma Invert** applies a bitwise complement to the luminance channel after all other Y processing. Every bright pixel becomes dark and vice versa, producing a photographic negative. An important detail: because inversion happens *before* the Luma Blank threshold, flipping this switch lets you key on dark regions of the original image instead of bright ones.

**Chroma Invert** applies a bitwise complement to both U and V channels, which shifts every hue by approximately 180° — reds become cyans, blues become yellows, and so on. This inversion happens *before* the Saturation control, so you can adjust the intensity of the inverted colors afterward.

**The three edge toggles** (Switches 9, 10, and 11) form a three-bit selector that chooses one of eight edge processing modes. The raw edge signal is *bipolar* — a bright-to-dark transition produces a positive pulse on one side and a negative pulse on the other. Edge Invert clips one polarity. Edge Rectify flips the polarity of the remaining signal. Edge Select applies full-wave rectification, folding both polarities to the same sign, which produces symmetrical contour outlines. Together, these three switches give you $2^3 = 8$ distinct edge shapes from the same filter output.

<img src={lumarian_edge_modes} alt="Grid of edge processing modes — same source processed with eight toggle combinations"/>

*All eight edge mode combinations applied to the same source.*

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Luma Blank
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% (fully down) |
| Suffix | % |

The Luma Blank fader sets a luminance threshold. Any pixel whose Y value falls below the threshold is replaced with pure black (Y = 0) and neutral chroma (U = V = midpoint). Pixels above the threshold pass through unmodified. At 0%, the threshold is at the bottom of the range and everything passes. As you raise the fader, progressively darker portions of the image snap to black. At 100%, only the very brightest pixels survive.

Because Luma Blank sits at the end of the Y processing chain, everything upstream affects what it "sees":

- **Shape before you key**: Use Contrast and Gamma to push the desired subject into the bright range and the unwanted background into the dark range, then raise Luma Blank to carve away the background cleanly.
- **Invert-then-key**: Toggle Luma Invert before keying to select dark regions of the original source instead of bright ones.
- **Threshold graphics**: Position the waveform precisely with Contrast and Brightness, then slice at a specific level with Luma Blank to create hard-edged graphic mattes.
- **Waveform clipping in feedback**: When Videomancer's output is routed back to its input, Luma Blank acts as a hard clipper on the bottom of the signal, which can produce interesting self-evolving feedback textures.

---

## Guided Exercises

The exercises below walk through Lumarian's capabilities in increasing order of complexity. Each builds on concepts from the one before it. If you are new to video processing, start with Exercise 1 — the ideas introduced there (gain, offset, transfer curves) are foundational to everything that follows.

### Exercise 1: Correcting Camera Footage

**Source**: A live camera feed or recorded footage with natural scenes.

**Objective**: Learn what each of the four tonal controls does to a video signal and how they interact.

1. **Initialize**: Load Lumarian with all defaults — Contrast, Brightness, Saturation, and Gamma at center, Edge Gain and Cutoff at zero, all toggles off, Luma Blank at zero.

2. **Black level**: Look at the darkest parts of the image. If areas that should be black appear gray, they have a brightness offset. Turn **Brightness** counter-clockwise until blacks are solid. If too much shadow detail disappears, ease it back slightly.

3. **Contrast**: Turn **Contrast** clockwise past center. Notice how the gap between the lightest and darkest parts of the image widens — highlights get brighter while blacks stay anchored near zero. Aim for somewhere around 110–140% for a natural-looking correction.

4. **Gamma**: Slowly turn **Gamma** counter-clockwise. Shadow detail opens up because the logarithmic curve lifts dark values. Now try clockwise — midtones darken, giving the image a more dramatic character. Notice that Gamma changes the *distribution* of tones without changing the endpoints (black stays black, white stays white).

5. **Color**: Turn **Saturation** all the way counter-clockwise to see the image in monochrome. Now bring it back past center. Notice that at 100% the color looks natural; above 100% colors become increasingly vivid and eventually start to clip.

6. **Sharpening**: Set **Edge Cutoff** to about 20%, then slowly bring **Edge Gain** up to 30–50%. Transitions in the image become crisper — this is the digital equivalent of broadcast aperture correction.

:::tip
Contrast is gain (multiplication). Brightness is offset (addition). Gamma is a nonlinear curve (redistribution). Saturation is chroma gain (multiplication around midpoint).
:::

---

### Exercise 2: Graphic Textures from Edges

<img src={lumarian_exercise2_result} alt="Creative edge enhancement — architectural source transformed into bold graphic contours"/>

*Edge Gain at 300%, Edge Cutoff at 40%, Edge Select set to Both — architectural footage turned into contour graphics.*

**Source**: Footage with strong visual structure — architecture, typography, plants, fabric, or synthesized patterns.

**Objective**: Explore what happens when the edge enhancer is pushed beyond its "correct" operating range.

1. **Prepare**: Set Contrast to about 130% and all other tonal controls to center. Turn **Saturation** to 0% so you can observe the edge structures without the distraction of color.

2. **Set Cutoff**: Turn **Edge Cutoff** to about 40% — this selects a middle band of spatial frequencies for extraction.

3. **Increase Gain gradually**: Slowly turn **Edge Gain** toward 200%. Below 100%, the edges simply sharpen the original image. Above 100%, the edge signal starts to compete with the source. By 300–400%, the original tonal content is almost entirely replaced by edge outlines. What you are seeing is the high-pass filtered version of the luminance channel, amplified until it dominates.

4. **Full-wave rectification**: Flip **Edge Select** (Switch 11) to on. Instead of the bipolar edge signal (bright halo on one side, dark halo on the other), you now see symmetrical outlines — both polarities folded to the same sign.

5. **Explore all eight modes**: Try every combination of **Edge Invert**, **Edge Rectify**, and **Edge Select**. Each combination produces a different edge shape. Watch how some modes emphasize outline contours while others produce filled or hollow regions.

6. **Sweep the filter**: With Edge Gain set high, slowly sweep **Edge Cutoff** from 0% to 100%. You are scrolling through spatial frequencies — fine textures at one end, broad contours at the other.

7. **Interact with Gamma**: Turn **Gamma** clockwise to about 1.0. This darkens midtones *before* edge extraction, which changes which luminance transitions are above the noise floor when the filter sees them. Try counter-clockwise as well.

8. **Reintroduce color**: Raise **Saturation** back to 100% or above. The original color now rides on the edge-processed luminance channel, producing a colorized graphic texture. Try **Chroma Invert** for complementary color palettes.

:::tip
Edge Cutoff selects the filter bandwidth (which edges). Edge Gain controls mix intensity (how much edge). The three edge toggles form a 3-bit mode selector ($2^3 = 8$ modes). Gamma before edge extraction gives frequency-selective emphasis on outlines.
:::

---

### Exercise 3: Sculpting a Luminance Key

<img src={lumarian_exercise3_result} alt="Luminance keying — a candle flame isolated against pure black via Luma Blank"/>

*Contrast and Gamma shape the tonal range, then Luma Blank carves away the shadows, leaving only the brightest elements.*

**Source**: High-contrast footage — candle flames, theatrical lighting, silhouettes, or text on a plain background. The output of Exercise 2 also works well.

**Objective**: Use the full processing chain (tonal shaping → edge enhancement → inversion → threshold keying) together, and observe how upstream changes propagate to the final key.

1. **Prepare**: Load high-contrast footage. Set all tonal controls to center and Saturation to 0% so you can work in monochrome.

2. **Separate the subject from the background**: Use **Contrast** and **Brightness** to push the subject into the bright range and the background into the dark range. The wider the gap, the cleaner the key will be.

3. **Apply Gamma**: Turn Gamma clockwise to darken midtones. This compresses the mid-range values toward black, which widens the gap between "subject" and "background" in luminance space.

4. **Raise the threshold**: Slowly raise **Luma Blank**. Watch as progressively darker portions of the image snap to black. Keep going until only the key subject remains — a clean bright shape on a black field.

5. **Refine the key edge**: If the key edges are too soft or noisy, increase Contrast to widen the luminance gap. If you are losing wanted detail, ease off Gamma or lift Brightness slightly. Notice how each upstream change immediately affects the key — this is the "order of operations" principle from the Signal Flow section in action.

6. **Invert the key**: Flip **Luma Invert** on and raise Luma Blank again. Because inversion happens before the threshold, you are now selecting the *dark* regions of the original source instead of the bright ones. The same subject that was keyed out before is now the part that survives.

7. **Add edge outlines to the key**: Turn Luma Invert off. Set Edge Gain to about 200% and Edge Cutoff to 30%. The luminance channel now includes prominent edge outlines. Raise Luma Blank — the threshold key now carves away everything except the edge-enhanced regions. Try Edge Select set to Both for symmetrical outlines.

8. **Colorize**: Raise Saturation back up. Keyed-out regions are neutral (black with no chroma), while surviving regions retain their original color. Toggle Chroma Invert to shift the surviving colors to their complements. You have built a self-keyed color graphic using the entire signal chain.

:::tip
Luma Blank is a threshold comparator at the end of the chain. Every upstream control (Contrast, Brightness, Gamma, Edge, Invert) changes what the threshold "sees." Shaping the signal before keying is the fundamental technique for building clean, controllable keys.
:::

---

## Tips

- **Order matters**: The signal flows through Contrast/Brightness → Gamma → Edge → Invert → Key. Each stage transforms the signal before the next one sees it. When something unexpected happens, trace the signal path and ask: "What did the upstream stages do to the data before it reached this point?"

- **Gamma before edges**: Because Gamma reshapes the luminance curve *before* the edge filter runs, you can use it to emphasize different parts of the image selectively. Counter-clockwise (logarithmic) lifts shadows into the filter's sensitive range, emphasizing shadow-region edges. Clockwise (exponential) does the opposite, emphasizing highlight edges.

- **Feedback loops**: If Videomancer's output is routed back to its input, Lumarian becomes a feedback processor. Edge enhancement and gamma correction in a feedback loop tend to produce self-reinforcing, evolving textures — the edge signal on one pass becomes the source for edge extraction on the next, and small features accumulate into large structures.

- **Work in monochrome first**: When building a complex effect, start with Saturation at 0%. Tonal structures and edge relationships are much easier to evaluate without the added variable of color. Add color back once the luminance behavior is what you want.

- **Stacking programs**: Lumarian works well as either the first or last program in a multi-program chain. As the first program, it shapes the source before other processing. As the last program, it applies final correction, sharpening, and keying to whatever the upstream programs produced.
