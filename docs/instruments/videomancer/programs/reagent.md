---
draft: true
sidebar_position: 242
slug: /instruments/videomancer/reagent
title: "Reagent"
image: /img/instruments/videomancer/reagent/reagent_hero.png
description: "Chemistry has a beautiful color language."
---

![Reagent hero image](/img/instruments/videomancer/reagent/reagent_hero_s1.png)
*Reagent applying SNES-inspired dual-screen color math to live video, producing ghostly motion trails and time-shifted arithmetic blending.*

---

## Overview

Reagent is a dual-screen arithmetic blending engine inspired by the Super Nintendo's S-PPU Color Math hardware. It splits your video into two paths: a "Main Screen" showing the current frame and a "Sub Screen" holding a time-delayed copy: then combines them per-component using one of four arithmetic modes: addition, subtraction, half-addition, or wrap-addition. The result is a family of effects ranging from ghostly translucent overlays to hard-edged shadow silhouettes to psychedelic modular color wrapping.

The Sub Screen is stored as a downsampled luminance thumbnail in a 4-frame ring buffer, then upsampled back to full resolution with nearest-neighbor interpolation. This produces the characteristic chunky, low-resolution artifacts of a retro console's secondary display layer. Chroma for the Sub Screen is borrowed from the current input with an optional hue rotation, so the delayed image can take on entirely new color character. A vertical Color Window can restrict blending to a band of the screen, leaving the rest untouched: just as the SNES PPU used window masking to create localized transparency for torchlight circles and spotlight effects.

:::tip
***Color Math is a per-component operation.*** Unlike simple crossfading, Reagent's arithmetic modes treat each color channel independently. Addition saturates to white, subtraction clamps to black, half-addition averages, and wrap-addition overflows modularly (each creating a distinct visual vocabulary.)
:::

### What's In a Name?

The name ***Reagent*** borrows from chemistry: a reagent is a substance added to a mixture to cause a reaction. Here, the Sub Screen is the reagent: a time-shifted ingredient introduced into the main signal to trigger a visual transformation. The arithmetic modes are the reactions: addition brightens, subtraction darkens, half-addition dilutes, and wrap-addition catalyzes unpredictable color overflow. The name also nods to the SNES RPG tradition, where reagents and potions fuel the magic systems that Color Math was originally designed to visualize.

---

## Quick Start

1. Set **Mix** (Fader 12) fully clockwise to hear the full wet signal. Turn **Delay** (Knob 2) clockwise to select a 1- or 2-frame delay. Move something in front of the camera: you should see a blocky, pixelated ghost trailing behind the live image.
2. Sweep **Sub Hue** (Knob 1) slowly. The ghost's color shifts through the spectrum as the Sub Screen's chroma rotates independently of the main image.
3. Toggle **Math A** (Switch 7) to **Sub**. The ghost becomes a dark silhouette: subtraction removes brightness where the delayed image overlaps the current frame.
4. Toggle **Math B** (Switch 8) to **Half**. The image softens into a dreamy half-addition average, like a double exposure.

---

## Parameters

![Videomancer front panel with Reagent loaded](/img/instruments/videomancer/reagent/reagent_control_panel.png)
*Videomancer's front panel with Reagent active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Sub Hue

| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |

**Sub Hue** rotates the hue of the Sub Screen's chroma channels. The Sub Screen borrows its color from the current input's U and V values, then applies a rotation through the full 360° color wheel. At 0°, fully counterclockwise, the Sub Screen's color matches the live input. As you turn the knob clockwise, colors shift through the spectrum: reds become greens, blues become oranges, and so on. At 360° (fully clockwise, which wraps back to 0°), the color has completed a full revolution and returns to its original hue.

:::tip
Because the Sub Screen's luminance comes from the delay buffer but its chroma comes from the *current* frame (with rotation applied), **Sub Hue** creates a split between brightness and color that can produce striking complementary-color ghost effects.
:::

---

### Knob 2 — Delay

| Property | Value |
|----------|-------|
| Range | 0frm – 3frm |
| Default | 1frm |

**Delay** selects how many frames old the Sub Screen image is, in four discrete steps: 0, 1, 2, or 3 frames. At 0 frames (fully counterclockwise), the Sub Screen is a downsampled copy of the current frame: no temporal offset, but the blocky thumbnail resolution is still visible. At 1 frame, you get a single-frame echo that accentuates motion blur. At 2 and 3 frames, the ghost falls further behind, creating a longer trail. Because the buffer stores only luminance at 32×24 resolution, the delay has a distinctly retro, low-resolution quality.

---

### Knob 3 — Main Brt

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Main Brt** controls the brightness gain applied to the Main Screen before it enters the Color Math engine. At 50% (the default midpoint), brightness passes through at unity. Turning counterclockwise toward 0% dims the main image to black. Turning clockwise toward 100% boosts the main image to full white. This gain directly affects the arithmetic: a brighter Main Screen produces brighter addition results and stronger subtraction from the Sub Screen.

---

### Knob 4 — Sub Brt

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Sub Brt** controls the brightness gain applied to the Sub Screen's luminance after it is read from the delay buffer and before it enters the Color Math engine. At 50% (the default midpoint), Sub Screen brightness is at unity. Turning counterclockwise dims the ghost toward invisibility. Turning clockwise overdrives the ghost, making it dominate the arithmetic blend. In subtract mode, a bright Sub Screen carves deeper shadows. In add mode, it pushes the result harder toward saturation.

---

### Knob 5 — Win Size

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Win Size** sets the vertical extent of the Color Window. At 100% (the default, fully clockwise), the window spans the entire screen height, so Color Math applies everywhere. As you turn counterclockwise, the window shrinks vertically, restricting the blended region to a narrower horizontal band. At 0%, the window is at its smallest. Areas outside the window show only the brightness-adjusted Main Screen, bypassing the Color Math engine entirely.

:::note
The Color Window is purely vertical: it creates horizontal bands across the screen. There is no horizontal window control. This mirrors the SNES PPU's window system, which defined rectangular screen regions for masking effects.
:::

---

### Knob 6 — Win Pos

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Win Pos** sets the vertical center of the Color Window. At 50% (the default midpoint), the window is centered on the screen. Turning counterclockwise moves the window toward the top of the frame. Turning clockwise moves it toward the bottom. Combined with **Win Size**, you can position a band of Color Math blending anywhere on the screen while the rest remains unaffected.

---

### Switch 7 — Math A

| Property | Value |
|----------|-------|
| Off | Add |
| On | Sub |
| Default | Add |

**Math A** selects between addition and subtraction for the Color Math engine. With the switch set to **Add**, the Main Screen and Sub Screen values are summed per-component, saturating at maximum brightness (1023). With the switch set to **Sub**, the Sub Screen values are subtracted from the Main Screen, clamping at zero (black). Addition creates luminous, translucent overlays. Subtraction creates dark voids and shadow silhouettes where the two screens overlap.

---

### Switch 8 — Math B

| Property | Value |
|----------|-------|
| Off | Full |
| On | Half |
| Default | Full |

**Math B** selects between full-strength and half-strength arithmetic. With the switch set to **Full**, the arithmetic from **Math A** is applied at full scale. With the switch set to **Half**, the operation changes: in combination with **Add**, it becomes ***half-addition***: `(Main + Sub) / 2`: producing a true 50% transparency blend. In combination with **Sub**, it becomes ***wrap-addition***: modular overflow where the sum wraps around past 1023, creating psychedelic color banding and unpredictable hue shifts.

---

### Switch 9 — Sub Inv

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Sub Inv** inverts the Sub Screen's luminance and chroma before it enters the Color Math engine. With the switch set to **Off**, the Sub Screen passes through normally. With the switch set to **On**, all three channels (Y, U, V) are complemented: bright areas become dark, and colors shift to their complements. This effectively turns addition into a form of inverted subtraction and vice versa, letting you explore negative-image blending without changing the arithmetic mode.

---

### Switch 10 — Window

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Window** enables or disables the Color Window masking system. With the switch set to **Off** (the default), Color Math applies uniformly to the entire frame. With the switch set to **On**, the Color Math result is confined to the vertical band defined by **Win Size** and **Win Pos**; the region outside the window shows only the brightness-adjusted Main Screen. Use the window to localize the blending effect: spotlight circles, horizon-line splits, or moving bands of transparency.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Reagent processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use Bypass for instant A/B comparison between the raw input and the processed result.

---

:::note Toggle Group Notes

**Math A** and **Math B** form a combined 2-bit mode selector that chooses between four distinct arithmetic operations:

| Math A | Math B | Mode | Behavior |
|--------|--------|------|----------|
| Add | Full | Addition | `Main + Sub`, saturate at 1023 |
| Sub | Full | Subtraction | `Main − Sub`, clamp at 0 |
| Add | Half | Half-Addition | `(Main + Sub) / 2` |
| Sub | Half | Wrap-Addition | `Main + Sub`, modular overflow (wraps past 1023) |

Addition and subtraction are the classic SNES Color Math modes. Half-addition was the standard technique for translucent overlays in games like ***Chrono Trigger*** and ***EarthBound***. Wrap-addition has no SNES equivalent: it is a Videomancer extension that exploits modular arithmetic for abstract color effects.

:::

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (unprocessed) signal and the wet (Color Math blended) signal. At 0%, fully down, only the original input is heard. At 100% (the default, fully up), only the blended result passes through. Intermediate values blend the two proportionally using linear interpolation. Use Mix for subtle ghost overlays at low wet values, or commit to the full effect at 100%.

---

## Background

### SNES Color Math

The Super Nintendo's ***Picture Processing Unit*** (S-PPU) contained a hardware subsystem called ***Color Math*** that was unique among consoles of its era. The PPU maintained two independent rendering pipelines: the ***Main Screen*** and the ***Sub Screen***: each capable of displaying different combinations of background layers and sprites. After both screens were rendered, Color Math combined them per-pixel using simple arithmetic: addition, subtraction, or half-addition.

This architecture was the engine behind some of the most memorable visual effects in 16-bit gaming. Translucent water surfaces in ***Donkey Kong Country***, the dream sequences in ***Chrono Trigger***, the psychedelic PSI attacks in ***EarthBound***, and the ghostly encounters in ***Final Fantasy VI*** all relied on Color Math. The ***Color Window*** system further refined these effects by restricting transparency to specific screen regions: torchlight circles in mine shafts, spotlight beams in boss battles, and fog banks that faded at their edges.

### Temporal Delay as Sub Screen

In Reagent, the Sub Screen is not a separate rendering layer but a ***temporally delayed copy*** of the input signal. The delay buffer stores luminance-only thumbnails at 32×24 resolution: roughly matching the SNES's 256×224 output scaled down to fit within the iCE40's limited block RAM. When the delayed image is read back and upsampled to full resolution using ***nearest-neighbor interpolation***, the blocky pixel grid evokes the chunky aesthetic of a 16-bit console.

The chroma channels for the Sub Screen are borrowed from the current frame's U and V values rather than being stored in the buffer. This is a practical concession to BRAM limitations, but it creates an interesting creative property: the Sub Screen always carries the *current* frame's color, recolored by the hue rotation control, while its luminance structure shows the *delayed* frame's spatial content.

### Arithmetic Modes

The four arithmetic modes each produce a distinct visual character:

- **Addition** (saturate): brightens everything the two screens share. Overlapping bright areas clip to white, creating luminous halos and flare effects.
- **Subtraction** (clamp): darkens where the Sub Screen has brightness. Moving objects leave dark shadow trails. Static areas cancel out.
- **Half-addition** (average): a true 50/50 blend producing soft double-exposure effects. The gentlest mode.
- **Wrap-addition** (modular): the sum wraps around past 1023, producing unpredictable hue and brightness shifts wherever the combined values overflow. This is Reagent's most abstract mode and has no SNES equivalent.


---

## Signal Flow

### Signal Flow Notes

Two key architectural details shape Reagent's behavior:

1. **Chroma sourcing**: The Sub Screen's luminance comes from the delay buffer (time-shifted) but its chroma comes from the *current* frame with optional hue rotation. This means the ghostly shapes carry delayed spatial structure but present-tense color: a split that becomes most visible when **Sub Hue** is offset from 0°.

2. **Window bypass path**: When the Color Window is enabled, regions outside the window show the brightness-adjusted Main Screen, *not* the raw input. The Main Brt control still affects the entire frame. Only the Color Math blending is confined to the window region.

:::note
The sync delay pipeline runs in parallel with the processing chain. The dry signal for the Mix stage comes from the *delayed* raw input, ensuring proper temporal alignment between the dry and wet paths regardless of processing latency.
:::


---

## Exercises

These exercises explore Reagent's modes progressively: from simple motion trails to localized window effects to abstract modular color wrapping.
### Exercise 1: Motion Ghost Trails

![Motion Ghost Trails result](/img/instruments/videomancer/reagent/reagent_ex1_s1.png)
*Motion Ghost Trails — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A luminous motion trail that follows moving objects, producing a ghostly double-exposure effect.

#### Key Concepts

- Temporal delay creates motion echoes
- Addition mode brightens overlapping regions
- The Sub Screen's low resolution creates characteristic blockiness

#### Steps

1. Set **Delay** (Knob 2) to 1 frame. Move your hand or an object in front of the camera (a blocky, pixelated echo should trail behind.)
2. Increase **Sub Brt** (Knob 4) to about 75%. The ghost brightens and becomes more visible.
3. Sweep **Sub Hue** (Knob 1) to roughly 180°. The ghost takes on a complementary color to your input, creating a cyan-against-orange or magenta-against-green pairing.
4. Set **Delay** to 3 frames. The echo falls further behind, stretching the trail.
5. Toggle **Bypass** (Switch 11) on and off to compare the raw input against the ghostly version.

#### Settings

| Control | Value |
|---------|-------|
| Sub Hue | 180° |
| Delay | 3 frm |
| Main Brt | 50.0% |
| Sub Brt | 75.0% |
| Win Size | 100.0% |
| Win Pos | 50.0% |
| Math A | Add |
| Math B | Full |
| Sub Inv | Off |
| Window | Off |
| Bypass | Off |
| Mix | 100.0% |

---

### Exercise 2: Shadow Silhouettes with Color Window

![Shadow Silhouettes with Color Window result](/img/instruments/videomancer/reagent/reagent_ex2_s1.png)
*Shadow Silhouettes with Color Window — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A moving band of shadow-trail effect sweeping across the screen, with the rest of the frame showing the clean main image.

#### Key Concepts

- Subtraction mode creates dark voids where the two screens overlap
- The Color Window restricts blending to a vertical band
- Win Pos and Win Size position the blending zone

#### Steps

1. Set **Math A** (Switch 7) to **Sub** and **Math B** (Switch 8) to **Full** for subtraction mode.
2. Set **Delay** (Knob 2) to 2 frames and **Sub Brt** (Knob 4) to about 60%.
3. Enable **Window** (Switch 10). The subtraction effect vanishes from most of the screen.
4. Set **Win Size** (Knob 5) to about 40%. A horizontal band of shadow-trail appears.
5. Slowly sweep **Win Pos** (Knob 6) from top to bottom. The shadow band slides across the frame like a scanner bar, revealing the subtraction effect only within the window.
6. Enable **Sub Inv** (Switch 9). The shadow silhouette inverts: dark regions become bright and vice versa within the window.

#### Settings

| Control | Value |
|---------|-------|
| Sub Hue | 0° |
| Delay | 2 frm |
| Main Brt | 50.0% |
| Sub Brt | 60.0% |
| Win Size | 40.0% |
| Win Pos | 50.0% |
| Math A | Sub |
| Math B | Full |
| Sub Inv | Off |
| Window | On |
| Bypass | Off |
| Mix | 100.0% |

---

### Exercise 3: Wrap-Addition Color Alchemy

![Wrap-Addition Color Alchemy result](/img/instruments/videomancer/reagent/reagent_ex3_s1.png)
*Wrap-Addition Color Alchemy — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Abstract, psychedelic color patterns where arithmetic overflow creates unpredictable hue shifts and banding.

#### Key Concepts

- Wrap-addition produces modular overflow (values past 1023 wrap back to 0)
- Hue rotation on the Sub Screen creates complementary color interactions
- Sub Inv combined with wrap mode produces chaotic color chemistry

#### Steps

1. Set **Math A** (Switch 7) to **Sub** and **Math B** (Switch 8) to **Half** for wrap-addition mode.
2. Set **Main Brt** (Knob 3) and **Sub Brt** (Knob 4) both to about 75% to push combined values past the overflow threshold.
3. Observe the output: bright areas in the source produce unexpected color shifts as channel values wrap around past 1023.
4. Sweep **Sub Hue** (Knob 1) slowly through 360°. The wrap boundaries shift through the spectrum, creating constantly changing banding patterns.
5. Enable **Sub Inv** (Switch 9). The inversion flips the Sub Screen's contribution, moving the overflow boundaries to different tonal regions of the image.
6. Adjust **Mix** (Fader 12) to about 60% to blend the abstract wrap result with the clean input, softening the extremity.

#### Settings

| Control | Value |
|---------|-------|
| Sub Hue | 120° |
| Delay | 1 frm |
| Main Brt | 75.0% |
| Sub Brt | 75.0% |
| Win Size | 100.0% |
| Win Pos | 50.0% |
| Math A | Sub |
| Math B | Half |
| Sub Inv | On |
| Window | Off |
| Bypass | Off |
| Mix | 60.0% |

---
## Glossary

- **Block RAM (BRAM)**: Dedicated memory blocks inside the FPGA used for buffering video data; Reagent uses six tiles for its 4-frame delay buffer.

- **Clamp**: Limiting a value to a minimum or maximum boundary; subtraction mode clamps results at zero (black) to prevent underflow.

- **Color Math**: The SNES S-PPU's per-pixel arithmetic blending system that combines Main Screen and Sub Screen images using addition, subtraction, or averaging.

- **Color Window**: A screen region mask that restricts Color Math to a defined area; in Reagent, a vertical band controlled by Win Size and Win Pos.

- **Half-Addition**: An arithmetic mode that averages Main and Sub Screen values: `(Main + Sub) / 2`: producing 50% transparency blending.

- **Hue Rotation**: Rotating the U and V chroma channels through the color wheel by a specified angle, changing the perceived color without altering brightness.

- **Main Screen**: The current-frame video path in Reagent's dual-screen architecture, analogous to the SNES PPU's primary rendering pipeline.

- **Nearest-Neighbor Interpolation**: An upsampling method that repeats pixel values rather than blending between them, producing sharp, blocky enlargements.

- **Saturate**: Limiting a value at the maximum (1023) when addition would exceed it, preventing wraparound artifacts in standard add mode.

- **Sub Screen**: The time-delayed secondary video path, stored as a low-resolution luminance thumbnail and combined with the Main Screen via Color Math.

- **Wrap-Addition**: Modular arithmetic where values exceeding 1023 overflow back to 0, creating unpredictable color shifts at overflow boundaries.

---
