---
draft: true
sidebar_position: 175
slug: /instruments/videomancer/lith
title: "Lith"
image: /img/instruments/videomancer/lith/lith_hero_s1.png
description: "In the photographic darkroom, lith printing is a process that defies conventional wisdom."
---

![Lith hero image](/img/instruments/videomancer/lith/lith_hero_s1.png)
*Lith rendering a portrait as an extreme-contrast print with warm brown shadows, creamy paper-white highlights, and organic grain in the transition zone (the unmistakable look of infectious development.)*

---

## Overview

Lith recreates the aesthetic of ***lith printing***, a specialized darkroom technique that produces images with extreme contrast, warm shadow tones, and a distinctive organic grain pattern. In the traditional process, photographic paper is vastly overexposed and then developed in highly dilute lith developer. The result is a transfer curve unlike any normal photographic process: shadows lock to deep black or warm brown, highlights become creamy paper white, and the transition between the two is abrupt and nonlinear: controlled by a phenomenon called ***infectious development***.

The lith print look is immediately recognizable: high contrast with no mid-tones in the conventional sense, warm brown shadow areas that feel almost hand-tinted, papery white highlights, and organic grain that clusters in the transition zone between light and dark. Lith brings this entire photochemical process into the video domain, with control over the exposure threshold, infection steepness, shadow warmth, and split-tone temperature.

### What's In a Name?

***Lith*** is short for ***lithographic***, referring to lith developer (originally used for graphic arts and lithographic film) that has been heavily diluted for creative photographic printing. The developer's chemistry with high-contrast silver halide emulsions produces the infectious development that gives lith prints their signature look. The name is both a material reference and a darkroom tradition ("to lith" a print is a verb among fine art photographers.)

---

## Quick Start

1. Feed a video source into Videomancer with Lith loaded. The image snaps to a high-contrast rendering with warm shadows.
2. Adjust **Exposure** (Knob 1) to find the threshold where the image splits between shadow and highlight. Moving the threshold up or down dramatically changes which parts of the image go dark versus light.
3. Turn **Infectn** (Knob 2) to about 70%. The transition between black and white becomes sharper and more abrupt.
4. Increase **Warmth** (Knob 5) to about 60%. The shadow regions take on a rich brown tone, while highlights remain creamy white.

---

## Parameters

![Videomancer front panel with Lith loaded](/img/instruments/videomancer/lith/lith_control_panel.png)
*Videomancer's front panel with Lith active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Exposure

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Exposure** sets the brightness threshold that separates shadow regions from highlight regions. At 50%, the split point sits at mid-gray. Lowering the value pushes the threshold darker, converting more of the image to paper white. Raising it pushes the threshold brighter, converting more of the image to deep shadow. This simulates the overexposure control in traditional lith printing: the amount of light that hits the paper determines where the infectious development boundary falls.

:::note
Unlike a simple brightness control, **Exposure** moves the ***decision point*** that separates the two tonal zones. Everything below the threshold goes toward black (or warm brown); everything above goes toward paper white. The transition steepness is controlled separately by **Infectn**.
:::

---

### Knob 2 — Infectn

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 68% |

**Infectn** (Infection) controls the steepness of the transfer curve at the shadow-to-highlight transition. At low values, the transition is relatively gradual: there's a range of mid-tone gray between black and white. As infection increases, the transition becomes sharper and more abrupt, approaching a hard binary threshold. At maximum, the curve is near-vertical: pixels are either black or white with almost nothing in between. The Developer switch further modifies this behavior, with Strong developer producing a harder step at equivalent infection settings.

---

### Knob 3 — Spread

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Spread** controls the width of the transition zone between full shadow and full highlight. At narrow values (low settings), the transition happens over a very small brightness range, creating a hard edge. At wider values, the transition extends across a broader range of input brightness, allowing more mid-tone information to survive. This is analogous to the "snatch point" timing in real lith printing: how long the developer has to work before the print is snatched from the tray.

---

### Knob 4 — Grain

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 29% |

**Grain** adds LFSR-based noise to the luminance channel, concentrated in the mid-tone transition zone. At 0%, no grain is applied. As the value increases, grain appears in the area between full shadow and full highlight: exactly where real lith prints show their characteristic organic grain. Pure black and pure white areas remain clean, mimicking the way infectious development concentrates grain in the developing boundary.

:::tip
The grain is applied ***only in the transition zone***: pixels flagged as mid-tones between the low and high edges. Shadows and highlights stay clean. This matches the real behavior of lith prints, where grain is concentrated at the "snatch point" between developed and undeveloped areas.
:::

---

### Knob 5 — Warmth

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 59% |

**Warmth** controls the intensity of the warm brown tint applied to shadow regions. At 0%, shadows are neutral. As warmth increases, pixels below the brightness of 400 receive a push toward warm brown in the U (−shift) and V (+shift) chroma channels. This simulates the characteristic warm-tone reaction of lith developer with chlorobromide paper emulsions (the slower the development, the warmer the shadows.)

---

### Knob 6 — Paper

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 88% |

**Paper** controls the brightness level of the highlight regions: the "paper white" ceiling. At 100%, highlights are at full brightness (1023). Reducing this value dims the paper white, as if the paper being printed on is a warm cream rather than bright white. This affects the entire upper portion of the transfer curve, lowering the ceiling that the infectious development pushes highlights toward.

---

### Switch 7 — Developer

| Property | Value |
|----------|-------|
| Off | Dilute |
| On | Strong |
| Default | Dilute |

**Developer** selects between two development strengths. **Dilute** simulates heavily diluted lith developer, which produces a more gradual transition with finer tonal nuance in the mid-tones. **Strong** simulates a more concentrated developer, which produces harder, more binary transitions: shadows go blacker and highlights go whiter with less gradation between them.

---

### Switch 8 — Grain

| Property | Value |
|----------|-------|
| Off | Fine |
| On | Coarse |
| Default | Fine |

**Grain** (Fine/Coarse) controls the visual scale of the film grain, following the same fine/coarse grain system as other Film category programs. **Fine** produces small, dense grain particles. **Coarse** produces larger, more visible grain clumps.

---

### Switch 9 — Split

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Split** enables split-tone processing. When **Off**, highlights remain neutral (achromatic paper white) while shadows receive the warm tone from the Warmth control. When **On**, highlights above a brightness of 600 receive a cool blue-cyan tint (U +20, V −15), creating a ***split-tone*** effect: warm shadows and cool highlights, a classic fine art photographic printing technique.

---

### Switch 10 — Invert

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Invert** flips the processed luminance after all other stages. With Invert **On**, the lith print becomes a negative: warm highlights and paper-dark shadows. This can produce interesting effects when the inverted lith treatment is applied to already high-contrast source material.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Lith processing stages. Use for instant A/B comparison.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**Mix** crossfades between the dry (unprocessed) signal and the wet (Lith-processed) signal. At partial mix values, the extreme contrast of the lith look is softened by blending with the original tonal range, which can produce a stylized high-contrast color effect.

---

## Background

### Lith printing in the darkroom

Lith printing emerged as a creative darkroom technique in the 1990s, popularized by photographers like Tim Rudman, who documented the process extensively. The technique requires using lith developer (typically Kodalith or Fotospeed Lith developer) at extreme dilutions: typically 1:20 to 1:50: with long development times of 5 to 20 minutes. The paper is overexposed by 2 to 5 stops beyond normal, and the development is visually monitored until the image reaches the desired point, at which the print is "snatched" from the developer tray.

### Infectious development

The hallmark of lith printing is ***infectious development***, a self-accelerating chemical reaction. In dilute lith developer, the development process starts slowly and evenly. But once a critical density of silver is reached in any area, the development reaction at that point begins producing its own accelerating chemistry: the byproducts of development catalyze further development in adjacent areas. This creates a positive feedback loop: dark areas develop exponentially faster, while light areas barely develop at all. The result is the characteristic abrupt transition between shadow and highlight, with the speed and steepness of the transition determined by the developer dilution and the snatch timing.

### The transfer curve

The Lith program models this nonlinear transfer curve using threshold-based comparison logic. Input brightness is evaluated against a window defined by the Exposure threshold ± the Spread width. Pixels below the window go to black (or near-black); pixels above go to paper white. Within the window, the Infection parameter controls how the transition happens: from a smooth ramp (low infection) to an abrupt step (high infection). The Developer toggle modifies whether the transition favors a harder (Strong) or softer (Dilute) curve shape, with each producing different intermediate values within the transition zone.


---

## Signal Flow

### Signal Flow Notes

The key design decision is that Lith processes ***only luminance through the transfer curve***: the input U and V channels are discarded entirely. The output chroma comes solely from the toning stage: warm brown for shadows, neutral for highlights, and optionally cool for highlights when split-tone is enabled. This is accurate to real lith printing, which is fundamentally a monochrome process with color coming only from the paper-developer interaction, not from the original image's colors.

The grain placement is tied to the mid-tone flag from the transfer curve stage. Only pixels that fall within the transition zone between low_edge and hi_edge receive grain. This matches the physical behavior of infectiously developed prints, where grain is concentrated at the boundary between fully developed (dark) and undeveloped (light) areas.

:::note
Because the transfer curve is compare-based with no variable multiplications, it evaluates in a single clock cycle. The "Infection" parameter does not create a smooth mathematical curve: it selects among a small number of discrete output levels within the transition zone. This gives a stepped, quantized feel to the mid-tones that actually approximates the abrupt nature of real infectious development quite well.
:::


---

## Exercises

These exercises progress from a basic lith print look to a fully styled split-tone effect.
### Exercise 1: Basic Lith Print

![Basic Lith Print result](/img/instruments/videomancer/lith/lith_ex1_s1.png)
*Basic Lith Print — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A high-contrast, nearly two-tone image with clean paper-white highlights and deep shadows (the basic lith print.)

#### Key Concepts

- Exposure threshold separates the image into shadow and highlight zones
- The transfer curve collapses mid-tones into either black or paper white
- Grain concentrates in the transition zone

#### Video Source

A portrait or scene with a range of brightness values, ideally with some mid-tone detail to see the threshold effect.

#### Steps

1. Set **Exposure** (Knob 1) to ~50%, **Infectn** (Knob 2) to ~50%, **Developer** (Switch 7) to Dilute.
2. Set **Paper** (Knob 6) to ~90% for bright paper white.
3. Set **Warmth** (Knob 5) to 0% to see the effect in pure monochrome first.
4. Slowly sweep **Exposure** up and down. Watch how the threshold moves, converting different tonal zones between black and white.
5. Increase **Infectn** to ~80%. The transition becomes more abrupt (fewer mid-tone grays survive.)

#### Settings

| Control | Value |
|---------|-------|
| Exposure | ~50% |
| Infectn | ~50% (step 2) / ~80% (step 5) |
| Spread | ~50% |
| Grain | ~0% |
| Warmth | ~0% |
| Paper | ~90% |
| Developer | Dilute |
| Grain | Fine |
| Split | Off |
| Invert | Off |
| Bypass | Off |
| Mix | ~100% |

---

### Exercise 2: Warm-Tone Lith with Grain

![Warm-Tone Lith with Grain result](/img/instruments/videomancer/lith/lith_ex2_s1.png)
*Warm-Tone Lith with Grain — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A classic warm-toned lith print with organic grain in the transition zone (the darkroom aesthetic.)

#### Key Concepts

- Warmth adds brown toning to shadow regions only
- Grain appears only in the mid-tone transition zone
- Paper controls the ceiling brightness of highlights

#### Video Source

A portrait or figure study: the warm shadows on skin tones produce an especially evocative result.

#### Steps

1. Set **Exposure** to ~50%, **Infectn** to ~70%, **Spread** to ~50%.
2. Increase **Warmth** (Knob 5) to ~60%. Shadow areas turn warm brown.
3. Add **Grain** (Knob 4) at ~40% with **Grain** (Switch 8) set to Fine. Notice how grain appears only in the transition zone between dark and light.
4. Reduce **Paper** (Knob 6) to ~80%. Highlights become a warmer, creamier white.
5. Try switching **Developer** to Strong. The transition sharpens, and the grain zone narrows.

#### Settings

| Control | Value |
|---------|-------|
| Exposure | ~50% |
| Infectn | ~70% |
| Spread | ~50% |
| Grain | ~40% |
| Warmth | ~60% |
| Paper | ~80% |
| Developer | Dilute (step 1) / Strong (step 5) |
| Grain | Fine |
| Split | Off |
| Invert | Off |
| Bypass | Off |
| Mix | ~100% |

---

### Exercise 3: Split-Tone Masterprint

![Split-Tone Masterprint result](/img/instruments/videomancer/lith/lith_ex3_s1.png)
*Split-Tone Masterprint — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A split-toned lith print with warm brown shadows, cool blue highlights, and visible grain in the razor-thin transition zone.

#### Key Concepts

- Split-tone combines warm shadows with cool highlights
- Strong developer produces the most dramatic shadow-highlight separation
- High infection with narrow spread creates a near-binary result

#### Video Source

High-contrast subject matter: architecture, trees against sky, or strong backlit portraits.

#### Steps

1. Set **Developer** to Strong, **Infectn** to ~80%, **Spread** to ~30%.
2. Set **Warmth** to ~80% for deep brown shadows.
3. Enable **Split** (Switch 9). Bright areas gain a cool blue tint.
4. Add **Grain** at ~50%, Coarse, for visible organic texture in the transition zone.
5. Set **Exposure** to ~60% and **Paper** to ~90%.
6. Reduce **Mix** to ~80% to let a hint of the original image show through.

#### Settings

| Control | Value |
|---------|-------|
| Exposure | ~60% |
| Infectn | ~80% |
| Spread | ~30% |
| Grain | ~50% |
| Warmth | ~80% |
| Paper | ~90% |
| Developer | Strong |
| Grain | Coarse |
| Split | On |
| Invert | Off |
| Bypass | Off |
| Mix | ~80% |

---
## Glossary

- **Chlorobromide Paper**: Photographic paper with a silver emulsion containing both silver chloride and silver bromide, producing warm-tone results in lith development.

- **Infectious Development**: A self-accelerating chemical reaction where the byproducts of silver development catalyze further development in adjacent areas, creating exponentially faster shadow formation.

- **LFSR**: Linear Feedback Shift Register; a deterministic pseudo-random number generator used here for grain simulation.

- **Lith Developer**: A high-contrast graphic arts developer (typically hydroquinone-based) used at extreme dilutions for creative fine art printing.

- **Lith Printing**: A creative darkroom technique using overexposed paper developed in dilute lith developer to produce extreme contrast, warm tones, and organic grain.

- **Snatch Point**: The moment in lith development when the print is removed from the developer tray. Earlier snatching preserves more mid-tones; later snatching increases contrast.

- **Split Tone**: A printing technique where shadow and highlight areas receive different color tints (typically warm shadows and cool highlights.)

- **Transfer Curve**: The mathematical relationship between input brightness and output brightness, which in lith printing is highly nonlinear with an abrupt transition.

---
