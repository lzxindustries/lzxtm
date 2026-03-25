---
draft: true
sidebar_position: 263
slug: /instruments/videomancer/sfumato
title: "Sfumato"
image: /img/instruments/videomancer/sfumato/sfumato_hero_s1.png
description: "Leonardo da Vinci described sfumato as painting \"in the manner of smoke, beyond the plane of focus\" — the technique of eliminating hard outlines between tones and colours so that forms appear to emerge from the air itself."
---

![Sfumato hero image](/img/instruments/videomancer/sfumato/sfumato_hero_s1.png)
*Sfumato dissolving hard tonal edges into smoky atmospheric gradients, softening shadows more than highlights in the manner of Leonardo da Vinci's vanishing-boundary technique.*

---

## Overview

**Sfumato** is an edge-adaptive atmospheric blur that mimics the Renaissance painting technique of the same name. Its core function is to selectively soften tonal transitions while preserving the gross structure of the image: edges with strong luminance contrast receive the heaviest smoothing, while flat areas pass nearly untouched. A luminance-depth modulation pushes extra blur into the shadows, simulating the way distant objects lose contrast in hazy air. Independent chrominance diffusion dissolves color boundaries beyond what the luminance edges dictate, and an ambient haze lifts the darkest tones while pulling saturation toward neutral.

At subtle settings, Sfumato adds a gentle, painterly softness to video: textures smooth out, skin looks porcelain, highlights retain crispness. At extreme settings, the image melts into bands of atmospheric color, hard edges vanish entirely, and shadows fill with luminous fog. Engaging the varnish warmth tints the result with an amber glow, evoking the golden patina of old oil paintings.

:::tip
***Edge-adaptive blur is the signature effect.*** Unlike a simple Gaussian blur, Sfumato reads the luminance gradient between neighboring pixels and adjusts its smoothing strength on a pixel-by-pixel basis. High gradients trigger heavy blending; flat regions stay crisp. This is what gives the effect its distinctive "painted" quality.
:::

### What's In a Name?

The name ***Sfumato*** comes directly from the Italian verb *sfumare*, meaning "to vanish" or "to evaporate like smoke." Leonardo da Vinci coined the term to describe his technique of layering translucent glazes so that tonal boundaries dissolve without visible brushstrokes: most famously in the *Mona Lisa*, where the corners of the mouth and eyes melt into surrounding shadow with no hard edge at all. In Videomancer, the program applies this idea electronically: an ***IIR*** (infinite impulse response) low-pass filter runs along each scanline, and the filter response is modulated by the local luminance gradient so that strong tonal edges are smoothed away while flat areas remain sharp.

---

## Quick Start

1. Turn **Diffusion** (Knob 1) clockwise to about 50%. The image softens noticeably: tonal edges blur into each other along each scanline, creating a smoky, painterly haze.
2. Increase **Edge Threshold** (Knob 2) from zero. As the threshold rises, notice how the blur becomes selective: only the strongest tonal edges receive heavy smoothing, while gentle gradients remain relatively clean.
3. Raise **Depth** (Knob 3) to about 40%. Darker areas of the image receive extra blur while highlights retain their crispness: shadows melt while bright regions hold their detail. This is the atmospheric perspective effect.
4. Set **Haze** (Knob 5) to about 25%. The deepest shadows lift toward mid-gray and colors desaturate slightly, as though a thin layer of mist sits between you and the subject.

---

## Parameters

![Videomancer front panel with Sfumato loaded](/img/instruments/videomancer/sfumato/sfumato_control_panel.png)
*Videomancer's front panel with Sfumato active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Diffusion

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Diffusion** sets the base strength of the IIR low-pass filter that runs along each scanline. At minimum, the filter is effectively bypassed: pixels pass through unchanged. As you turn the knob clockwise, each pixel blends more heavily with its neighbor, and tonal transitions stretch out into soft, smoky gradients. At maximum, the filter carries nearly all of the previous pixel's value forward, creating long streaky smears of color that trail across the entire line.

Diffusion is the foundation of the entire effect. Every other parameter: edge threshold, depth, chroma diffusion: scales or modulates this base value. If Diffusion is at zero, none of the other blur controls have any visible effect.

---

### Knob 2 — Edge Threshold

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 39.1% |

**Edge Threshold** controls the sensitivity of the edge-adaptive filter. The program computes the luminance gradient: the absolute brightness difference between adjacent pixels: and compares it to this threshold. When the gradient exceeds the threshold, the filter applies full Diffusion strength. When the gradient falls below the threshold, the filter strength scales down proportionally: a pixel in a gradual gradient receives less blur than a pixel at a sharp tonal edge.

At minimum, the threshold is effectively zero and ***all*** pixels receive the full Diffusion amount: the effect becomes a uniform IIR blur. As you increase Edge Threshold, the filter becomes more selective, reserving its heaviest smoothing for the hardest edges. This is the core of Sfumato's intelligence: soft areas stay clean while sharp transitions vanish into smoke.

:::note
Edge Threshold has no effect when Diffusion is at zero, because there is no base blur strength to modulate.
:::

---

### Knob 3 — Depth

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 29.3% |

**Depth** introduces luminance-adaptive blur modulation. The program reads each pixel's brightness and multiplies the effective filter strength by a depth factor derived from it: dark pixels get more blur, bright pixels get less. The result is ***prospettiva aerea***: Leonardo's "aerial perspective": where shadows dissolve into atmospheric haze while highlights remain crisp and detailed.

At minimum, depth modulation is disabled and the filter treats all luminance levels equally. As you increase Depth, the difference in blur strength between shadows and highlights grows more pronounced. At maximum, the darkest regions of the image are smoothed almost completely while the brightest areas pass through virtually untouched.

:::tip
Combine Depth with **Depth Mode** (Switch 8) set to **Quad** for an even steeper shadow-to-highlight contrast. Quadratic depth squares the depth factor, concentrating blur far more aggressively in the deepest shadows.
:::

---

### Knob 4 — Chroma Diffusion

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 58.7% |

**Chroma Diffusion** applies extra blur to the U and V color channels beyond what the luminance channel receives. When **Chroma Lock** (Switch 9) is set to **Indep**, this control adds an independent boost to the chrominance filter alpha, causing color boundaries to dissolve further than luminance boundaries. When Chroma Lock is set to **Lock**, this control has no effect (chrominance uses the same filter strength as luminance.)

At minimum, chrominance receives the same amount of blur as luminance (no extra diffusion). As you increase Chroma Diffusion, colors bleed outward beyond their luminance edges, creating a soft halo of desaturated color around objects. At maximum, chrominance is heavily smeared while luminance structure may still be relatively intact: edges are visible in brightness but their color information has been dissolved away.

---

### Knob 5 — Haze

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 19.6% |

**Haze** simulates atmospheric scattering by lifting shadow luminance toward mid-gray and desaturating colors proportionally. The effect is applied after the IIR filter, so it operates on the already-blurred signal. Haze lifts the Y channel by a fixed offset and pulls the U and V channels toward their neutral midpoints.

At minimum, no atmospheric lift is applied. As you increase Haze, the darkest areas of the image brighten and colors wash out, as though viewing the scene through a layer of mist. At maximum, the image takes on a flat, milky quality with reduced contrast and deeply desaturated color (pure atmospheric haze.)

:::note
Haze is additive to Y, so pushing it to extremes on an already-bright image can clip highlights to white. For the most naturalistic results, pair moderate Haze with moderate **Depth**: shadows get blurred *and* lifted while highlights remain untouched.
:::

---

### Knob 6 — Warmth

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Warmth** controls the color temperature shift applied by the **Varnish** stage (Switch 10). When Varnish is enabled, Warmth shifts the V channel upward and the U channel downward, pushing the overall color balance toward amber and gold (like the aged varnish on an oil painting.)

At minimum, no color shift is applied even when Varnish is enabled. As you increase Warmth, the amber tint strengthens. At maximum, the varnish is deeply golden, reminiscent of the yellowed surface of centuries-old canvas. When Varnish is disabled (Switch 10 set to **Off**), this control has no visible effect.

---

### Switch 7 — Direction

| Property | Value |
|----------|-------|
| Off | Uni |
| On | Bidi |
| Default | Uni |

**Direction** selects between unidirectional and bidirectional IIR filtering. In **Uni** mode, the filter runs left-to-right across each scanline: pixels on the left side of edges blur into the right, creating a directional smear. In **Bidi** mode, the program stores the forward-pass result in a ***line buffer*** and averages it with a reverse-addressed read, producing a symmetric blur that spreads equally in both directions.

:::tip
Unidirectional mode uses zero block RAM and has a subtle directional character: smears trail rightward. Bidirectional mode uses one BRAM tile and produces a more even, painterly softness at the cost of a slightly different visual texture. Try both and decide which suits your image.
:::

---

### Switch 8 — Depth Mode

| Property | Value |
|----------|-------|
| Off | Linear |
| On | Quad |
| Default | Linear |

**Depth Mode** selects the curve applied to the depth modulation factor. In **Linear** mode, the blur reduction from shadows to highlights follows a straight line. In **Quad** mode, the depth factor is squared before it modulates the filter strength, creating a steeper curve that concentrates blur far more aggressively in the deepest shadows while leaving mid-tones and highlights almost unaffected.

Quadratic depth is most dramatic when combined with high **Depth** settings. With low Depth values, the difference between Linear and Quad is subtle.

---

### Switch 9 — Chroma Lock

| Property | Value |
|----------|-------|
| Off | Indep |
| On | Lock |
| Default | Indep |

**Chroma Lock** determines whether the chrominance channels use the same filter alpha as luminance or receive independent, extra diffusion. In **Indep** mode, the **Chroma Diffusion** knob (Knob 4) adds additional blur on top of the base alpha for U and V. In **Lock** mode, chrominance is locked to the luminance alpha and the Chroma Diffusion knob has no effect.

:::note
Lock mode is useful when you want all three channels to blur uniformly: the result looks like a conventional soft-focus filter. Indep mode is the key to the classic sfumato look where color bleeds beyond brightness boundaries.
:::

---

### Switch 10 — Varnish

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Varnish** enables or disables the amber color temperature shift controlled by **Warmth** (Knob 6). When set to **Off**, the blurred and hazed signal passes through without color alteration. When set to **On**, the Warmth control shifts the chrominance balance toward golden amber by pushing V up and U down: simulating the look of an aged oil varnish over the entire image.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Sfumato processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use Bypass for instant A/B comparison between the raw input and the processed result.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (unprocessed) and wet (fully processed) signal using three parallel interpolators: one each for Y, U, and V. At minimum, the output is entirely dry: you see the original input video. At maximum, the output is entirely wet: you see the full Sfumato effect. Intermediate positions blend the two, allowing you to dial in exactly how much softening you want to apply.

:::tip
Mix is a powerful creative tool in its own right. Setting it to around 30–40% applies a gentle "glaze" of the Sfumato effect over a mostly-dry signal: just enough softness to smooth harsh textures without losing sharpness.
:::

---

## Background

### The sfumato technique

***Sfumato*** is one of four canonical painting modes identified by Leonardo da Vinci, alongside ***cangiante*** (shifting hues), ***chiaroscuro*** (strong light and dark contrast), and ***unione*** (harmonious blending). Leonardo described sfumato as "in the manner of smoke, beyond the focus plane": a technique for rendering form without lines or clear boundaries, achieved by building dozens of translucent layers so that tonal transitions vanish imperceptibly.

The most famous application is the *Mona Lisa*, where the corners of the mouth and the edges of the eyes dissolve into surrounding shadow with no discernible border. The technique creates an optical ambiguity that makes the expression seem to shift as the viewer's gaze moves. The Videomancer program captures this idea by making the filter strength proportional to the luminance gradient: hard tonal edges: the places where Leonardo would have layered the most glazes: receive the most smoothing.

### Aerial perspective

***Prospettiva aerea***, or aerial perspective, is Leonardo's observation that distant objects appear lighter, bluer, and less distinct because of atmospheric scattering. The intervening air: dust, moisture, haze: scatters short-wavelength light and reduces contrast. Sfumato models this with its **Depth** parameter: luminance drives the blur strength so that shadows (representing distance or depth in the visual field) dissolve more than highlights. The **Haze** parameter adds the complementary effect: lifting shadow luminance and desaturating color, simulating the actual scattering medium.

### IIR filtering

The core of Sfumato is an ***infinite impulse response*** (IIR) low-pass filter. Unlike a ***finite impulse response*** (FIR) filter: which averages a fixed window of pixels: an IIR filter feeds its own output back into the input. The recurrence relation is:

$$Y_{out}[n] = \alpha \cdot Y_{out}[n-1] + (1 - \alpha) \cdot Y_{in}[n]$$

Here, $\alpha$ is the filter coefficient: higher $\alpha$ means the filter "remembers" more of its previous output, producing heavier smoothing. Because the output depends on all previous inputs (weighted exponentially), a single IIR tap can produce smooth, wide blurs without needing large BRAM-based delay lines. The tradeoff is that IIR filters are inherently causal: they blur in one direction only. Sfumato's bidirectional mode mitigates this by averaging forward and reverse passes stored in a line buffer.


---

## Signal Flow

### Signal Flow Notes

Three key interactions define the character of Sfumato:

1. **Edge-adaptive modulation**: The gradient between adjacent pixels sets the IIR filter coefficient. High gradients push the coefficient toward the full Diffusion value; low gradients reduce it proportionally via the Edge Threshold. The result is a blur that "knows" where edges are: it smooths across hard tonal boundaries while leaving gentle gradients alone.

2. **Depth × edge interaction**: The depth factor modulates the edge-adaptive alpha multiplicatively. A pixel at a hard tonal edge in a shadow region receives the *product* of the edge alpha and the depth factor: compounding two separate blur-boosting effects. This creates a natural hierarchy: bright flat areas are sharpest, dark edges are softest.

3. **Haze as a post-filter stage**: Haze operates on the already-blurred signal, so it lifts shadows that have already been softened by the IIR filter. This sequencing is important: the haze doesn't create new gradients for the filter to smooth, it simply adds a DC offset and desaturation on top of the result.

:::tip
**The IIR resets at every scanline.** The filter state (`s_y_iir_prev`, etc.) is cleared to mid-gray at each `hsync_start`. This means the first few pixels of each line experience a brief *ramp-up* as the filter converges: a subtle visual signature most visible in unidirectional mode with high Diffusion.
:::


---

## Exercises

These exercises explore Sfumato from gentle painterly softening through full atmospheric dissolution. Each builds on the previous exercise, progressively engaging more of the processing chain.
### Exercise 1: Painterly Softness

![Painterly Softness result](/img/instruments/videomancer/sfumato/sfumato_ex1_s1.png)
*Painterly Softness — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A gentle, portrait-like softening that removes harsh textures while preserving the overall structure of the image (similar to a traditional diffusion filter on a camera lens.)

#### Key Concepts

- IIR filtering smooths tonal transitions along each scanline
- Edge-adaptive modulation applies stronger blur to sharp edges
- Bidirectional mode creates symmetric, non-directional softness

#### Video Source

A portrait or close-up with visible skin texture, hair detail, and strong facial features. A well-lit face against a contrasting background works best.

#### Steps

1. **Base blur**: Turn **Diffusion** (Knob 1) to about 50%. The image softens noticeably (tonal transitions stretch out along each scanline.)
2. **Edge select**: Increase **Edge Threshold** (Knob 2) to around 40%. The blur becomes selective: only the strongest tonal edges (skin-to-background, hairline, eye outlines) receive heavy smoothing.
3. **Bidirectional**: Flip **Direction** (Switch 7) to **Bidi**. The directional rightward smear vanishes, replaced by a symmetric softness that feels more like a camera diffusion filter.
4. **Subtle mix**: Pull **Mix** (Fader 12) down to about 60%. The dry signal blends with the soft result, restoring some crispness while retaining the painterly haze.
5. **A/B compare**: Toggle **Bypass** (Switch 11) on and off. The difference is immediately visible in skin texture and hair detail.

#### Settings

| Control | Value |
|---------|-------|
| Diffusion | ~50% |
| Edge Threshold | ~40% |
| Depth | 0% |
| Chroma Diffusion | 0% |
| Haze | 0% |
| Warmth | 0% |
| Direction | Bidi |
| Depth Mode | Linear |
| Chroma Lock | Lock |
| Varnish | Off |
| Bypass | Off |
| Mix | ~60% |

---

### Exercise 2: Atmospheric Perspective

![Atmospheric Perspective result](/img/instruments/videomancer/sfumato/sfumato_ex2_s1.png)
*Atmospheric Perspective — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A scene that looks like it's being viewed through hazy air: distant shadows dissolve and lighten while foreground highlights remain sharp and saturated.

#### Key Concepts

- Depth modulation pushes extra blur into shadows, simulating aerial perspective
- Quadratic depth concentrates the effect in the deepest tones
- Haze lifts shadow luminance and desaturates, simulating scattering atmosphere

#### Video Source

Landscape or cityscape footage with a range of depths: trees, buildings, sky: or any image with strong shadow-to-highlight contrast.

#### Steps

1. **Foundation**: Set **Diffusion** (Knob 1) to ~60% and **Edge Threshold** (Knob 2) to ~30%.
2. **Depth engage**: Raise **Depth** (Knob 3) to about 60%. Shadows begin to dissolve while highlights hold their detail.
3. **Quadratic curve**: Flip **Depth Mode** (Switch 8) to **Quad**. The shadow-blur intensifies dramatically: the deepest tones now receive far more smoothing than mid-tones.
4. **Atmospheric haze**: Raise **Haze** (Knob 5) to about 30%. Shadow areas lift toward mid-gray and colors soften toward neutral.
5. **Chroma bleed**: Set **Chroma Lock** (Switch 9) to **Indep** and raise **Chroma Diffusion** (Knob 4) to ~40%. Color boundaries dissolve beyond their luminance edges, adding to the aerial perspective illusion.
6. **Fine-tune**: Adjust **Mix** (Fader 12) to taste: around 80% provides a strong atmospheric effect while retaining some original detail.

#### Settings

| Control | Value |
|---------|-------|
| Diffusion | ~60% |
| Edge Threshold | ~30% |
| Depth | ~60% |
| Chroma Diffusion | ~40% |
| Haze | ~30% |
| Warmth | 0% |
| Direction | Uni |
| Depth Mode | Quad |
| Chroma Lock | Indep |
| Varnish | Off |
| Bypass | Off |
| Mix | ~80% |

---

### Exercise 3: Venetian Oil Painting

![Venetian Oil Painting result](/img/instruments/videomancer/sfumato/sfumato_ex3_s1.png)
*Venetian Oil Painting — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A richly toned, warm image that evokes the golden glow of a Renaissance oil painting: soft tonal transitions, dissolved color boundaries, atmospheric shadow, and amber varnish.

#### Key Concepts

- Varnish applies an amber color temperature shift to the processed signal
- Combining depth, haze, and varnish recreates the look of aged oil paintings
- Independent chroma diffusion dissolves color boundaries beyond luminance edges

#### Video Source

Still life, portraiture, or any subject with rich color and strong tonal structure. Classical compositions (fruit, drapery, architecture) suit the theme perfectly.

#### Steps

1. **Heavy diffusion**: Set **Diffusion** (Knob 1) to ~60% and **Edge Threshold** (Knob 2) to ~50%. Tonal edges dissolve heavily.
2. **Depth and shadow**: Raise **Depth** (Knob 3) to ~40%. Shadows melt away.
3. **Color dissolution**: Set **Chroma Lock** (Switch 9) to **Indep** and **Chroma Diffusion** (Knob 4) to ~70%. Color bleeds well beyond its luminance boundaries.
4. **Amber varnish**: Enable **Varnish** (Switch 10) and raise **Warmth** (Knob 6) to ~50%. The entire image takes on a golden amber tint.
5. **Bidirectional**: Flip **Direction** (Switch 7) to **Bidi** for an even, non-directional softness.
6. **Atmospheric wash**: Add a touch of **Haze** (Knob 5) at ~15% to lift the deepest shadows slightly.
7. **Full wet**: Leave **Mix** (Fader 12) at 100% for the full painted effect.

#### Settings

| Control | Value |
|---------|-------|
| Diffusion | ~60% |
| Edge Threshold | ~50% |
| Depth | ~40% |
| Chroma Diffusion | ~70% |
| Haze | ~15% |
| Warmth | ~50% |
| Direction | Bidi |
| Depth Mode | Linear |
| Chroma Lock | Indep |
| Varnish | On |
| Bypass | Off |
| Mix | 100% |

---
## Glossary

- **Aerial Perspective**: The visual phenomenon where distant objects appear lighter, less saturated, and less distinct due to atmospheric scattering; also called *prospettiva aerea*.

- **Alpha (Filter Coefficient)**: The feedback strength of an IIR filter, ranging from 0 (no filtering) to 1 (total smoothing); controls how much the previous output influences the current output.

- **Bidirectional Filtering**: Running a filter in both forward and reverse directions and averaging the results, producing symmetric blur without directional bias.

- **Chrominance**: The color-difference components (U and V) of a YUV video signal, representing hue and saturation independently of brightness.

- **Gradient**: The absolute difference in luminance between adjacent pixels; used by Sfumato to detect tonal edges and modulate filter strength.

- **Haze**: An additive luminance lift combined with proportional desaturation, simulating the scattering of light through atmosphere.

- **IIR (Infinite Impulse Response)**: A filter type where the output feeds back into the input, producing smooth, wide-reaching effects from a single tap without large memory buffers.

- **Line Buffer**: A block RAM that stores one scanline of pixel data, used in bidirectional mode to hold the forward-pass result for reverse-pass averaging.

- **Luminance**: The brightness component (Y) of a YUV video signal, representing perceived lightness independent of color.

- **Sfumato**: An Italian painting technique meaning "in the manner of smoke," where tonal boundaries are dissolved through layered transparent glazes, leaving no visible edges.

- **Varnish**: A chrominance color-temperature shift that pushes the image toward amber and gold, simulating the aged surface coating of oil paintings.

---
