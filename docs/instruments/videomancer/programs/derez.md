---
draft: true
sidebar_position: 82
slug: /instruments/videomancer/derez
title: "Derez"
image: /img/instruments/videomancer/derez/derez_hero_s1.png
description: "Real memory corruption is never random."
---

![Derez hero image](/img/instruments/videomancer/derez/derez_hero_s1.png)
*Derez simulating cascading VRAM corruption: address line faults fold the image into mirrored tiles while stuck data bits carve harsh posterized bands across the frame.*

---

## Overview

Derez is a memory corruption simulator. It recreates the visual artifacts produced by failing RAM chips, stuck address decoders, data bus faults, and dead display lines: the kinds of glitches that haunted vintage arcade boards, early personal computers, and aging CRT monitors. Feed it any video signal, and Derez will systematically break that signal apart as though the hardware reading it were falling to pieces.

The program offers four independent corruption engines that can be combined freely. Address corruption scrambles *where* pixels are read from, creating mirroring, tiling, and spatial folding. Data bus stuck bits force individual bits in the pixel value high or low, producing harsh banding and value clamping. Bit-plane shift separates the binary layers of the luminance channel in space, creating rainbow fringing on edges. Dead line injection replaces entire rows or columns with black, simulating failed scan lines in a display controller.

:::tip
**Start with one engine at a time.** Each corruption mode produces dramatic results on its own. Once you understand how each one distorts the image, combining them creates layered digital decay that feels organic and unpredictable.
:::

### What's In a Name?

***Derez*** is shorthand for ***deresolution***: the process of an object or program losing its structural integrity and dissolving into raw data. The term was popularized by the 1982 film *Tron*, where programs "derezzed" when destroyed, fragmenting into geometric shards. In Videomancer, Derez does the same thing to your video signal: it strips away the orderly structure of digital video, exposing the raw binary scaffolding underneath.

---

## Quick Start

1. Turn **Corrupt Bits** (Knob 1) clockwise to about halfway. The image begins to fold and mirror as address lines are corrupted: chunks of the picture repeat and overlap in geometric patterns.
2. Sweep **Bit Select** (Knob 2) slowly. The corruption pattern shifts as different address bits are targeted. Low values corrupt the fine structure (small tiles); high values corrupt the coarse structure (large folds).
3. Turn **Stuck Mask** (Knob 3) up to introduce data bus faults. Harsh bands of clamped brightness appear as individual data bits are forced high.
4. Raise the **Mix** fader (Fader 12) partway to blend the corrupted signal with the clean original. This lets the source peek through the damage.

---

## Parameters

![Videomancer front panel with Derez loaded](/img/instruments/videomancer/derez/derez_control_panel.png)
*Videomancer's front panel with Derez active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Corrupt Bits

| Property | Value |
|----------|-------|
| Range | 0 – 10 |
| Default | 0 |

**Corrupt Bits** controls how many address bits are affected by corruption. At minimum, fully counterclockwise, no address bits are corrupted and the image passes through with its spatial structure intact. As you turn the knob clockwise, more bits in the horizontal read address are modified: first one, then two, then up to seven. Each additional corrupted bit doubles the spatial disruption: one bit creates a simple mirror fold, two bits create fourfold tiling, and higher counts produce increasingly chaotic interleaving of pixel positions.

The number of bits is quantized to the top 3 bits of the pot value, producing 8 discrete steps (0 through 7). The interaction with **Bit Select** (Knob 2) determines *which* bits are affected.

---

### Knob 2 — Bit Select

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |

**Bit Select** controls the starting position of the corruption window within the 10-bit horizontal address. At minimum, the corruption begins at the least significant address bits and affects the fine spatial structure: pixels swap with their near neighbors, producing tight interleaving patterns and small tiling. As the value increases, the corruption window slides toward the most significant address bits, affecting coarse spatial structure: entire halves or quarters of the image fold, mirror, or repeat.

The offset is quantized to the top 3 bits of the pot value (0 through 7), and the corruption window spans from that offset upward for the number of bits set by **Corrupt Bits**.

:::note
When the window extends beyond the 10th address bit, it wraps around. You may find that certain Bit Select positions produce no visible change if the affected bits lie outside the active width of the line buffer.
:::

---

### Knob 3 — Stuck Mask

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |

**Stuck Mask** controls the data bus stuck-bit pattern. At minimum, no bits are stuck and pixel values pass through unchanged. As you increase the value, the 10-bit binary representation of the pot value is applied as a mask to every pixel, forcing the corresponding data bits to a fixed state. The polarity (high or low) is determined by the **Stuck Pol** toggle (Switch 8).

Low stuck-mask values affect only the least significant bits, producing subtle banding. Higher values engage the more significant bits, creating aggressive posterization and harsh value clamping where entire brightness ranges are collapsed or elevated.

:::tip
With **Animate** (Switch 10) set to **Animate**, the stuck mask rotates by one bit position per video frame instead of deriving directly from the pot. This creates a scanning corruption pattern that cycles through all 10 bit positions automatically.
:::

---

### Knob 4 — Plane Shift

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |

**Plane Shift** controls the spatial displacement between the 10 binary layers of the luminance channel. At minimum, all bit planes are aligned and the Y channel appears normal. As the value increases, lower-order bit planes are progressively delayed relative to higher-order ones. The most significant bit (bit 9) always has zero delay; the least significant bit (bit 0) receives the maximum delay. This separation causes edges to develop rainbow-like fringing: where a sharp brightness transition occurs, the bit planes disagree, and the pixel values along the boundary become a chaotic mix of partially shifted binary weights.

The maximum shift is 64 pixels. The delay for each bit plane is proportional to its distance from the MSB multiplied by the Plane Shift value.

---

### Knob 5 — Dead Lines

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |

**Dead Lines** controls the probability that any given scan line (or column, depending on **Dead Axis**) is replaced with a black value. At minimum, no dead lines appear. As you increase the value, the ***LFSR*** (linear feedback shift register) test threshold rises and more lines fail the test, appearing as black stripes across the image. At maximum, nearly every line is killed.

Dead lines simulate the appearance of a failing VRAM row decoder or a display controller with dead scan lines: a common failure mode in vintage CRT monitors and early flat-panel displays.

---

### Knob 6 — Glitch Seed

| Property | Value |
|----------|-------|
| Range | 0 – 1023 |
| Default | 512 |

**Glitch Seed** sets the initial value of the 16-bit LFSR that drives dead line positioning and animation. Different seed values produce different spatial patterns of dead lines. Because the LFSR is deterministic, the same seed always produces the same pattern, making results repeatable between sessions. The LFSR is re-seeded at the start of every video frame (on vsync), so changing the seed instantly reshuffles the dead line distribution.

---

### Switch 7 — Addr Mode

| Property | Value |
|----------|-------|
| Off | XOR |
| On | Stuck |
| Default | XOR |

**Addr Mode** selects the address corruption algorithm. With the switch set to **XOR**, the corruption mask is XORed with the horizontal read address. XOR flips the targeted bits, causing pixel positions to swap symmetrically: the result is mirroring and folding patterns. With the switch set to **Stuck**, the mask bits are forced to a fixed state (high or low, controlled by **Stuck Pol**). Forcing bits high produces offset and repeat patterns; forcing bits low produces tiling and decimation where multiple source pixels map to the same read address.

---

### Switch 8 — Stuck Pol

| Property | Value |
|----------|-------|
| Off | High |
| On | Low |
| Default | High |

**Stuck Pol** sets the polarity of stuck operations for both address corruption (in Stuck mode) and data bus stuck bits. With the switch set to **High**, affected bits are forced to 1. For address corruption, this shifts the read address upward, causing the image to jump and repeat. For data bits, this forces pixel values toward maximum brightness. With the switch set to **Low**, affected bits are forced to 0. For address corruption, this clears bits, creating tiling patterns. For data bits, this forces values toward black.

---

### Switch 9 — Dead Axis

| Property | Value |
|----------|-------|
| Off | Rows |
| On | Columns |
| Default | Rows |

**Dead Axis** selects whether dead lines are horizontal rows or vertical columns. With the switch set to **Rows**, entire scan lines (horizontal stripes) are replaced with black. With the switch set to **Columns**, individual pixel columns are killed per clock cycle, creating vertical black stripes. Row-mode dead lines are evaluated once per horizontal sync; column-mode lines are evaluated every pixel clock, producing a finer and more chaotic pattern because the LFSR advances much more rapidly.

:::note
In **Columns** mode, the LFSR advances per pixel rather than per line, producing much denser and more textured dead-line patterns compared to **Rows** mode.
:::

---

### Switch 10 — Animate

| Property | Value |
|----------|-------|
| Off | Static |
| On | Animate |
| Default | Static |

**Animate** enables frame-by-frame evolution of the data bus stuck-bit mask. With the switch set to **Static**, the stuck mask is derived directly from the **Stuck Mask** pot value each frame: the corruption pattern is stable and repeatable. With the switch set to **Animate**, the stuck mask rotates by one bit position on every vsync, cycling through all 10 possible single-bit shifts automatically. This produces a scanning interference pattern that sweeps through different bit weights without touching the knobs.

---

### Switch 11 — Channel

| Property | Value |
|----------|-------|
| Off | All |
| On | Y Only |
| Default | All |

**Channel** selects whether data bus stuck bits affect all three video channels or only the luminance channel. With the switch set to **All**, the stuck mask is applied to Y, U, and V equally: both brightness and color are corrupted. With the switch set to **Y Only**, only the luminance channel receives stuck-bit corruption while the chroma channels pass through cleanly. This preserves the color fidelity of the image while still destroying its tonal structure.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**Mix** crossfades between the dry (unprocessed) input signal and the wet (corrupted) output. At 0%, only the original signal is heard. At 100%, fully clockwise, only the corrupted signal passes through. Intermediate values blend the two, letting the clean image ghost through the corruption. This is useful for dialing in subtle glitch textures without fully destroying the source material.

---

## Background

### Memory architecture of vintage hardware

Early video hardware stored frame data in dedicated ***VRAM***: video random access memory. A display controller would read through this memory sequentially, converting stored values into video signals for the monitor. The address bus told the RAM *which* byte to read, and the data bus carried the actual pixel value back. When either bus developed a fault, the results were dramatic and visually distinctive.

A stuck address line meant the display controller couldn't distinguish between certain memory locations. If bit 8 of the address was stuck high, every address in the lower half of memory would be redirected to the upper half, folding the image on itself. If a lower bit was stuck, fine-grained interleaving patterns appeared as adjacent pixels swapped positions. These failure modes are what created the famous "kill screen" glitches in arcade games like *Pac-Man* and *Donkey Kong*.

### Data bus faults and bit-plane separation

When individual data lines on a memory bus fail, the effect is a form of forced quantization. A bit stuck high means that particular weight is always present in the value: a stuck bit 9 (the most significant) clamps every pixel to at least half brightness. A bit stuck low removes that weight entirely. Multiple stuck bits create complex posterization patterns where only certain value ranges are reachable.

***Bit-plane*** separation is a related artifact. In early tile-based graphics hardware, each bit of a pixel's color value was often stored in a separate memory plane. If one plane's timing drifted, its spatial position would shift relative to the others. The eye perceives this as a separation of binary weight layers: edges develop fringing, and flat areas reveal the underlying binary structure of the pixel values.

### Dead lines and display faults

Dead scan lines are a signature failure of aging CRT displays and early LCD panels. A dead line appears when the display controller skips a row or when VRAM cells along an entire row fail and output zero. Horizontal dead lines carve black stripes across the image; vertical dead lines create a picket-fence effect. In Derez, an LFSR pseudo-random sequence determines which lines die, simulating the semi-random nature of real hardware degradation.


---

## Signal Flow

### Signal Flow Notes

The four corruption engines operate in series within a single clocked pipeline. Address corruption comes first because it determines *which* pixel is read from the line buffer: all downstream effects (stuck bits, dead lines) are applied to the already-scrambled data. This means address corruption multiplies the visual impact of every other effect: a stuck data bit applied to address-corrupted data produces different patterns than the same stuck bit on the original data, because the spatial mapping has already been rearranged.

Bit-plane shift is applied only to the Y channel and operates on the data *after* the corrupted read, using independent per-bit shift registers. Because each bit plane is delayed by a different amount, a single sharp edge in the source becomes a cascade of bit-weight transitions spread across up to 64 pixels. The shift amount is proportional to the distance from the MSB, so the most significant bits (which contribute the most visible brightness steps) remain aligned while the least significant bits drift the farthest.

:::tip
**Interaction sweet spot**: Set Corrupt Bits and Bit Select to produce a visible fold or mirror, then slowly introduce Plane Shift. The bit-plane separation follows the mirrored geometry, creating layered fringing patterns that echo the spatial corruption.
:::


---

## Exercises

These exercises progress from simple address-line faults to full multi-engine corruption. Each exercise isolates a different corruption mechanism before combining them.
### Exercise 1: Address Line Fault

![Address Line Fault result](/img/instruments/videomancer/derez/derez_ex1_s1.png)
*Address Line Fault — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A mirrored, folded version of the source video, as though the memory address decoder were failing: the same visual artifact that created the infamous Pac-Man kill screen.

#### Key Concepts

- Address corruption scrambles the read position within a line buffer
- XOR mode produces symmetric mirroring; Stuck mode produces tiling and offset
- The number of corrupted bits controls the spatial scale of the disruption

#### Video Source

A live camera feed or recorded footage with recognizable features: faces, text, or geometric objects make the spatial distortion easy to see.

#### Steps

1. **Single fold**: Set **Corrupt Bits** (Knob 1) to a low value (around 10%). Set **Bit Select** (Knob 2) fully clockwise. A single high-order address bit is corrupted, folding the image at its midpoint.
2. **Sweep the fold**: Slowly turn **Bit Select** counterclockwise. The fold point moves from the coarse structure (large mirror) to the fine structure (tight interleaving).
3. **Increase depth**: Raise **Corrupt Bits** to about 50%. Multiple address bits are now corrupted, creating complex tiling and overlapping folds.
4. **Switch modes**: Toggle **Addr Mode** (Switch 7) from **XOR** to **Stuck**. The symmetric mirroring changes to an offset repeat pattern. Toggle **Stuck Pol** (Switch 8) to compare forcing bits high (offset) versus low (tiling).
5. **Mix back**: Lower the **Mix** fader (Fader 12) to about 60% to let the original image ghost through the corruption.

#### Settings

| Control | Value |
|---------|-------|
| Corrupt Bits | 50% |
| Bit Select | 100% |
| Stuck Mask | 0% |
| Plane Shift | 0% |
| Dead Lines | 0% |
| Glitch Seed | 512 |
| Addr Mode | XOR |
| Stuck Pol | High |
| Dead Axis | Rows |
| Animate | Static |
| Channel | All |
| Mix | 60% |

---

### Exercise 2: Data Bus Decay

![Data Bus Decay result](/img/instruments/videomancer/derez/derez_ex2_s1.png)
*Data Bus Decay — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A decaying data bus effect where individual bits of the pixel value are clamped, combined with spatial separation of the luminance bit planes (the look of VRAM failing bit by bit.)

#### Key Concepts

- Stuck data bits force pixel values to fixed states, creating posterized bands
- Animation rotates the stuck mask automatically, producing scanning patterns
- Bit-plane shift separates binary weight layers in space

#### Video Source

Footage with smooth gradients: sky, skin tones, or color bars. Gradients make stuck-bit banding clearly visible.

#### Steps

1. **Stuck bits**: Turn **Stuck Mask** (Knob 3) slowly clockwise. As the binary value of the pot engages successive bits, corresponding bands of clamped brightness appear. Notice how each new stuck bit creates a hard boundary at a specific brightness threshold.
2. **Polarity**: Toggle **Stuck Pol** (Switch 8) between **High** and **Low**. High pushes values toward white; Low pushes toward black.
3. **Animate**: Toggle **Animate** (Switch 10) to **Animate**. The stuck mask now rotates each frame, creating a scanning corruption pattern that cycles through all bit positions.
4. **Y Only**: Toggle **Channel** (Switch 11) to **Y Only**. Colors now remain clean while brightness is corrupted (the effect becomes more subtle and filmic.)
5. **Plane shift**: Turn **Plane Shift** (Knob 4) clockwise. The 10 bit planes of the Y channel separate horizontally. Edges develop rainbow fringing as different bit weights arrive at different horizontal positions.
6. **Combine**: With both Stuck Mask and Plane Shift active, the stuck-bit bands interact with the plane separation to produce complex layered patterns.

#### Settings

| Control | Value |
|---------|-------|
| Corrupt Bits | 0% |
| Bit Select | 0% |
| Stuck Mask | 50% |
| Plane Shift | 50% |
| Dead Lines | 0% |
| Glitch Seed | 512 |
| Addr Mode | XOR |
| Stuck Pol | High |
| Dead Axis | Rows |
| Animate | Animate |
| Channel | Y Only |
| Mix | 100% |

---

### Exercise 3: Full Memory Failure

![Full Memory Failure result](/img/instruments/videomancer/derez/derez_ex3_s1.png)
*Full Memory Failure — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A comprehensive memory failure simulation combining address faults, stuck data lines, bit-plane drift, and dead scan lines (the complete meltdown of a vintage video system.)

#### Key Concepts

- All four corruption engines combine for layered decay
- Dead lines add structural damage to the already-corrupted image
- The Glitch Seed makes patterns repeatable

#### Video Source

High-contrast footage with both sharp edges and smooth areas: architectural footage, stage lighting, or abstract patterns work well.

#### Steps

1. **Base corruption**: Set **Corrupt Bits** to about 80% and **Bit Select** to about 50%. The image folds and tiles aggressively.
2. **Data damage**: Raise **Stuck Mask** to about 30%. Stuck bits carve harsh bands into the already-scrambled image.
3. **Plane separation**: Turn **Plane Shift** to about 70%. The luminance channel's bit planes separate, adding fringing to the corrupted geometry.
4. **Dead lines**: Raise **Dead Lines** (Knob 5) to about 20%. Black stripes begin cutting through the image.
5. **Dead axis**: Toggle **Dead Axis** (Switch 9) between **Rows** and **Columns** to compare horizontal stripes versus vertical picket-fence patterns.
6. **Seed**: Sweep **Glitch Seed** (Knob 6) to find a pattern that resonates with the source material. Each seed produces a different distribution of dead lines.
7. **Mix**: Use the **Mix** fader to find the balance point where the source is still recognizable through the corruption.

#### Settings

| Control | Value |
|---------|-------|
| Corrupt Bits | 80% |
| Bit Select | 50% |
| Stuck Mask | 30% |
| Plane Shift | 70% |
| Dead Lines | 20% |
| Glitch Seed | 250 |
| Addr Mode | XOR |
| Stuck Pol | High |
| Dead Axis | Rows |
| Animate | Static |
| Channel | All |
| Mix | 60% |

---
## Glossary

- **Address Bus**: The set of signal lines that carry the memory address: the location from which data is to be read. Corruption of address bits causes the wrong data to be read.

- **Bit Plane**: A single binary layer of a multi-bit pixel value. A 10-bit pixel has 10 bit planes, each contributing a different weight to the final brightness.

- **Data Bus**: The set of signal lines that carry the actual pixel data. A stuck data line forces one bit of every value to a fixed state.

- **Dead Line**: A scan line (horizontal) or pixel column (vertical) that outputs black instead of valid image data, simulating a failed row in a display controller.

- **Kill Screen**: A level or state in a vintage arcade game where memory corruption produces unplayable visual garbage (famously occurring at level 256 of *Pac-Man*.)

- **LFSR**: Linear Feedback Shift Register: a hardware pseudo-random number generator that produces deterministic but apparently random sequences from a seed value.

- **Line Buffer**: A single-line memory that stores one horizontal row of pixels, allowing random-access reads from corrupted addresses.

- **Stuck Bit**: A bit in a digital bus that is permanently forced to 0 or 1, regardless of the intended value. A common failure mode in aging RAM and bus drivers.

- **VRAM**: Video Random Access Memory: dedicated memory used to store the image data that a display controller reads to produce the video signal.

- **XOR**: Exclusive OR: a bitwise logic operation that flips a bit when the corresponding mask bit is 1. Used here to create symmetric mirroring in the address space.

---
