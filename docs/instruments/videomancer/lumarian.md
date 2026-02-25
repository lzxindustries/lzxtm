---
draft: false
sidebar_position: 3
slug: /instruments/videomancer/lumarian
title: "Lumarian"
---

import lumarian_hero from '/img/instruments/videomancer/lumarian/lumarian_hero.png';
import lumarian_before_after from '/img/instruments/videomancer/lumarian/lumarian_before_after.png';
import lumarian_control_panel from '/img/instruments/videomancer/lumarian/lumarian_control_panel.png';
import lumarian_exercise1_result from '/img/instruments/videomancer/lumarian/lumarian_exercise1_result.png';
import lumarian_exercise2_result from '/img/instruments/videomancer/lumarian/lumarian_exercise2_result.png';
import lumarian_exercise3_result from '/img/instruments/videomancer/lumarian/lumarian_exercise3_result.png';

# Lumarian

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={lumarian_hero} alt="Lumarian processing a natural scene with subtle edge enhancement and shadow recovery via gamma correction"/>

<img src={lumarian_before_after} alt="Left: unprocessed source. Right: Lumarian applied"/>

*Left: unprocessed source. Right: Lumarian applied.*

**Source images used in this guide:**
- **1**. kodim04.png — Portrait of girl in red — wide dynamic range
- **2**. kodim23.png — Two macaws — saturated primary colors
- **3**. peppers_512.png — Peppers — tonal gradients

<details>
<summary>Hero image settings</summary>

| Control | Value |
|---------|-------|
| Contrast | ~130% |
| Brightness | center |
| Gamma | ~−0.5 (slightly counter-clockwise to open shadows) |
| Saturation | ~140% (vivid but not clipping) |
| Edge Gain | ~80% (visible sharpening, not dominant) |
| Edge Cutoff | ~25% |
| Luma Blank | ~15% (clean deepest shadows to black) |
| All toggles | Off |

</details>

---

## Overview

Every video image is made of three things: how bright each pixel is (luminance), what color it is (chrominance), and where the edges between regions fall. Lumarian gives you direct, real-time control over all three.

The program chains six processing stages together — contrast, brightness, saturation, gamma correction, edge enhancement, and luminance keying — and runs them simultaneously on every pixel of every frame. The name comes from *luminance*, the measurable brightness of light, which is the central quantity this program manipulates.

At one end of the spectrum, Lumarian can do straightforward image correction: fix a washed-out camera feed, sharpen soft footage, or pull a clean key from high-contrast material. At the other end, pushing the edge enhancer and gamma controls past their "correct" ranges produces entirely new graphic textures. The same signal chain does both — the difference is just how far you turn the knobs.

---

## Background

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

*Videomancer's front panel with Lumarian active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Contrast
| Property | Value |
|----------|-------|
| Range | 0.0% – 200.0% |
| Default | 100.1% |
| Suffix | % |

Contrast is a **gain** control — it multiplies the luminance value of every pixel. At 100% (center), the multiplication factor is 1.0, so the signal passes unchanged. Turn clockwise and the factor increases: highlights get brighter while blacks stay anchored at zero. Turn counter-clockwise and the factor decreases: the entire image compresses toward black. At 0%, every pixel is black regardless of input. At 200%, every luminance value is doubled (and values that exceed the maximum are clipped).

---

#### Knob 2 — Brightness
| Property | Value |
|----------|-------|
| Range | -1.000 – 1.000 |
| Default | 0.001 |

Brightness is a **DC offset** — it adds or subtracts a constant value from every pixel's luminance. Where Contrast scales the range (multiplication), Brightness shifts it (addition). Positive values lift the whole image uniformly; negative values push it darker. This is the control to reach for when your black level is wrong — turn counter-clockwise to restore solid blacks, or clockwise if shadow detail has been lost.

---

#### Knob 3 — Saturation
| Property | Value |
|----------|-------|
| Range | 0.0% – 200.0% |
| Default | 100.1% |
| Suffix | % |

Saturation scales the U and V chrominance channels around their neutral midpoint. Because the scaling is centered on the midpoint (not zero), reducing saturation moves colors toward gray rather than toward a tinted value. At 0%, the output is purely monochrome — only the Y channel contributes. At 100%, color passes unchanged. At 200%, every color's distance from neutral is doubled, producing vivid, exaggerated hues.

---

#### Knob 4 — Gamma
| Property | Value |
|----------|-------|
| Range | -2.000 – 2.000 |
| Default | 0.002 |

Gamma reshapes the **transfer curve** that converts input luminance to output luminance. At center (0.000), the curve is a straight line — output equals input. Turning clockwise bends the curve downward (exponential), which darkens shadows and midtones while leaving the brightest highlights relatively unchanged. Turning counter-clockwise bends it upward (logarithmic), which lifts shadows and compresses highlights. Here is why this matters for the rest of the chain: edge enhancement runs *after* gamma. So if you darken midtones with gamma, edges in the shadow region become less prominent, while edges near highlights become more pronounced. This interaction gives you selective control over which parts of the image produce the strongest edge signals.

---

#### Knob 5 — Edge Gain
| Property | Value |
|----------|-------|
| Range | 0.0% – 400.0% |
| Default | 0.0% |
| Suffix | % |

This control sets how much of the extracted edge signal gets mixed back into the Y channel. At 0%, no edge enhancement is applied at all — the edge processing chain is effectively off. As you increase the value, transitions in the image appear sharper and more defined. Past about 100%, the edge signal starts to become as strong as the original image content. Past 200%, edges dominate the output and the original tonal information recedes into the background. At 400%, you are looking almost entirely at the edge signal itself. For reference: broadcast aperture correction typically used the equivalent of 10–30%. Anything above 100% is firmly in creative territory.

---

#### Knob 6 — Edge Cutoff
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Edge Cutoff sets the **bandwidth** of the high-pass filter that extracts edges from the Y channel. At 0%, the filter passes nothing — no edge signal is produced regardless of the Edge Gain setting. As you turn clockwise, the filter begins passing spatial frequencies, starting with the finest detail. Higher values widen the passband to include broader transitions and larger-scale contours. Edge Cutoff and Edge Gain work as a pair: Cutoff selects *which* edges are extracted, and Gain controls *how strongly* they appear.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Luma Invert** | Off | On |
| **8 — Chroma Invert** | Off | On |
| **9 — Edge Invert** | Off | On |
| **10 — Edge Rectify** | Off | On |
| **11 — Edge Select** | Single | Both |

Switches 9, 10, and 11 form a three-bit selector that chooses one of eight edge processing modes. The raw edge signal is *bipolar* — a bright-to-dark transition produces a positive pulse on one side and a negative pulse on the other. Edge Invert clips one polarity. Edge Rectify flips the polarity of the remaining signal. Edge Select applies full-wave rectification, folding both polarities to the same sign, which produces symmetrical contour outlines. Together, these three switches give you 2³ = 8 distinct edge shapes from the same filter output.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Luma Blank
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Sets a luminance threshold. Any pixel whose Y value falls below the threshold is replaced with pure black (Y = 0) and neutral chroma (U = V = midpoint). Pixels above the threshold pass through unmodified. At 0%, everything passes. As you raise the fader, progressively darker portions of the image snap to black. At 100%, only the very brightest pixels survive. Because Luma Blank sits at the end of the Y processing chain, everything upstream affects what it "sees."

---

## Guided Exercises

These exercises progress from corrective to creative, gradually exploring more of Lumarian's processing chain. Start with a clean input and build up.

### Exercise 1: Correcting Camera Footage

<img src={lumarian_exercise1_result} alt="Correcting Camera Footage — simulated result across source images"/>

*Correcting Camera Footage — simulated result across source images.*

**Source**: A live camera feed or recorded footage with natural scenes.

**Objective**: Learn what each of the four tonal controls does to a video signal and how they interact.

1. **Initialize**: Load Lumarian with all defaults — Contrast, Brightness, Saturation, and Gamma at center, Edge Gain and Cutoff at zero, all toggles off, Luma Blank at zero.
2. **Black level**: Look at the darkest parts of the image. If areas that should be black appear gray, they have a brightness offset. Turn **Brightness** counter-clockwise until blacks are solid. If too much shadow detail disappears, ease it back slightly.
3. **Contrast**: Turn **Contrast** clockwise past center. Notice how the gap between the lightest and darkest parts of the image widens — highlights get brighter while blacks stay anchored near zero. Aim for somewhere around 110–140% for a natural-looking correction.
4. **Gamma**: Slowly turn **Gamma** counter-clockwise. Shadow detail opens up because the logarithmic curve lifts dark values. Now try clockwise — midtones darken, giving the image a more dramatic character. Notice that Gamma changes the *distribution* of tones without changing the endpoints (black stays black, white stays white).
5. **Color**: Turn **Saturation** all the way counter-clockwise to see the image in monochrome. Now bring it back past center. Notice that at 100% the color looks natural; above 100% colors become increasingly vivid and eventually start to clip.
6. **Sharpening**: Set **Edge Cutoff** to about 20%, then slowly bring **Edge Gain** up to 30–50%. Transitions in the image become crisper — this is the digital equivalent of broadcast aperture correction.

:::tip
Contrast is gain (multiplication), Brightness is offset (addition), Gamma is a nonlinear curve (redistribution), Saturation is chroma gain (multiplication around midpoint).
:::

---

### Exercise 2: Graphic Textures from Edges

<img src={lumarian_exercise2_result} alt="Graphic Textures from Edges — simulated result across source images"/>

*Graphic Textures from Edges — simulated result across source images.*

**Source**: Footage with strong visual structure — architecture, typography, plants, fabric, or synthesized patterns.

**Objective**: Explore what happens when the edge enhancer is pushed beyond its "correct" operating range.

1. **Prepare**: Set Contrast to about 130% and Saturation to 0% (monochrome). This gives the edge filter a strong signal to work with.
2. **First edges**: Set Edge Cutoff to about 40%, then slowly increase Edge Gain. Below 100%, you will see sharpening; above 100%, edges start to compete with the source material.
3. **Maximum edge**: Push Edge Gain to 300–400%. Edges now replace most of the tonal content — the image is almost entirely made of its own contours.
4. **Symmetrical outlines**: Enable Edge Select (Switch 11). The output changes from single-sided edges to symmetrical contour outlines.
5. **Mode exploration**: Cycle through all eight combinations of Switches 9, 10, and 11. Each combination produces a different visual shape.
6. **Cutoff sweep**: With Edge Gain high, sweep Edge Cutoff from minimum to maximum. At low cutoff, only the finest detail edges appear. At high cutoff, broader transitions join in.
7. **Gamma interaction**: With edge enhancement active, turn Gamma clockwise to about 1.0. Midtones darken, and the edge filter responds differently to the redistributed tonal values.
8. **Color reintroduction**: Bring Saturation back up. Enable Chroma Invert (Switch 8) for a complementary color effect over the edge texture.

:::tip
Edge Cutoff selects the filter bandwidth (which edges), Edge Gain controls mix intensity (how much edge), the three edge toggles form a 3-bit mode selector (2³ = 8 modes), Gamma before edge extraction gives frequency-selective emphasis on outlines.
:::

---

### Exercise 3: Sculpting a Luminance Key

<img src={lumarian_exercise3_result} alt="Sculpting a Luminance Key — simulated result across source images"/>

*Sculpting a Luminance Key — simulated result across source images.*

**Source**: High-contrast footage — candle flames, theatrical lighting, silhouettes, or text on a plain background.

**Objective**: Use the full processing chain (tonal shaping → edge enhancement → inversion → threshold keying) together.

1. **Monochrome**: Start with Saturation at 0%. Working in monochrome makes it easier to see what the luminance key is doing.
2. **Separate subject and background**: Use Contrast and Brightness to push your subject's brightness away from the background. Increase Contrast to widen the gap; shift Brightness to move the boundary.
3. **Gamma shape**: Turn Gamma clockwise to darken midtones, making the boundary between "subject" and "background" sharper.
4. **Threshold**: Raise the Luma Blank fader. As the threshold rises, darker parts of the image snap to black. Adjust until the background disappears and only the subject remains.
5. **Refine**: Go back to Contrast and Brightness to clean up the key edge. Small adjustments here can eliminate fringing.
6. **Invert**: Enable Luma Invert (Switch 7). The key flips — what was visible becomes black, and what was black becomes visible.
7. **Add edge outlines**: With the key active, set Edge Gain to about 200% and Edge Cutoff to 30%. Edges appear *within* the keyed subject, adding contour detail to the silhouette.
8. **Colorize**: Bring Saturation back up and enable Chroma Invert (Switch 8). The keyed subject now has complementary colors overlaid with edge outlines.

:::tip
Luma Blank is a threshold comparator at the end of the chain, every upstream control changes what the threshold "sees", shaping the signal before keying is the fundamental technique for building clean controllable keys.
:::

---

## Tips

- **Order matters**: The signal flows through Contrast/Brightness → Gamma → Edge → Invert → Key. Each stage transforms the signal before the next one sees it.
- **Gamma before edges**: Because Gamma reshapes the luminance curve *before* the edge filter runs, you can use it to emphasize different parts of the image selectively. Counter-clockwise (logarithmic) lifts shadows into the filter's sensitive range, emphasizing shadow-region edges. Clockwise (exponential) does the opposite, emphasizing highlight edges.
- **Feedback loops**: If Videomancer's output is routed back to its input, Lumarian becomes a feedback processor. Edge enhancement and gamma correction in a feedback loop tend to produce self-reinforcing, evolving textures.
- **Work in monochrome first**: When building a complex effect, start with Saturation at 0%. Remove the color variable until your tonal chain is set, then reintroduce it.
- **Stacking programs**: Lumarian works well as either the first or last program in a multi-program chain. As the first program, it shapes the signal for downstream effects. As the last, it corrects or stylizes the final output.
