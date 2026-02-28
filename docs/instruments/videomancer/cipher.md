---
draft: true
sidebar_position: 49
slug: /instruments/videomancer/cipher
title: "Cipher"
image: /img/instruments/videomancer/cipher/cipher_hero.png
---

import cipher_hero from '/img/instruments/videomancer/cipher/cipher_hero.png';
import cipher_before_after from '/img/instruments/videomancer/cipher/cipher_before_after.png';
import cipher_control_panel from '/img/instruments/videomancer/cipher/cipher_control_panel.png';
import cipher_exercise1_result from '/img/instruments/videomancer/cipher/cipher_exercise1_result.png';
import cipher_exercise2_result from '/img/instruments/videomancer/cipher/cipher_exercise2_result.png';
import cipher_exercise3_result from '/img/instruments/videomancer/cipher/cipher_exercise3_result.png';

# Cipher

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={cipher_hero} alt="Cipher hero image"/>
*Cipher applying LFSR-driven XOR scrambling with position-dependent channel permutation across a multi-source composite.*
<img src={cipher_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Cipher applied.*

---

## Overview

Every pixel in a digital video frame is a number. A brightness value, a pair of color coordinates — nothing more than integers arranged on a grid. Cipher treats those numbers the way a cryptographer treats plaintext: as raw material to be scrambled, permuted, and recombined according to a pseudo-random keystream. The result is video that looks *encrypted* — fragments of the original image shattered into noise, color-swapped mosaics, and bit-rotated abstractions that hover between recognizable content and pure digital chaos.

At the heart of the program is a 16-bit Galois Linear Feedback Shift Register (LFSR), a hardware primitive that generates a deterministic but apparently random sequence of bits from a simple initial seed. This keystream drives four distinct modes of visual scrambling: XOR masking that flips pixel bits against the keystream, channel permutation that swaps luminance and chrominance components based on LFSR state, circular bit rotation that cyclically shifts the binary representation of each pixel value, and selective inversion that complements channels through a compound XOR-and-negate operation. The name *Cipher* references the dual nature of all reversible encryption — the same operation that scrambles can also unscramble, given the right key.

The interplay between the six continuous controls and five mode switches gives Cipher an enormous parameter space. At one extreme, a shallow depth with low scramble produces a subtle veil of noise over the source — barely perceptible digital haze. At the other extreme, full depth with block-mode permutation transforms the image into a mosaic of swapped color tiles, each block sharing a single LFSR state, like a classified document with its pixels individually redacted and rearranged. Between those poles lies a rich territory of glitch aesthetics, cipher-punk textures, and information-theoretic visual art.

---

## Background

### Cryptography and Visual Art

The visual language of encryption has fascinated artists since the earliest substitution ciphers carved into clay tablets. In the twentieth century, the Enigma machine's rotor wheels became an icon of hidden information — the idea that meaning could be present but inaccessible, locked behind a combinatorial barrier. Digital artists in the glitch and data-bending movements adopted the *aesthetics* of encryption: the visual noise of XOR'd bitstreams, the color artifacts of misinterpreted file headers, the mosaic fragmentation of block ciphers. Cipher brings these techniques into the real-time video domain, where the keystream evolves at pixel clock speed and the "plaintext" is a live video signal.

### Linear Feedback Shift Registers

An LFSR is one of the simplest pseudo-random number generators that can be built in digital hardware. It consists of a shift register whose input bit is a linear function (typically XOR) of selected tap positions. Cipher uses a 16-bit maximal-length Galois configuration with the polynomial $x^{16} + x^{15} + x^{13} + x^4 + 1$, which cycles through all $2^{16} - 1 = 65{,}535$ non-zero states before repeating. The sequence is entirely deterministic — given the same seed, the same stream of bits emerges — yet the output passes many statistical tests for randomness. This duality between determinism and apparent chaos is central to Cipher's visual character.

### XOR as Reversible Transformation

The XOR (exclusive-or) operation is the cornerstone of nearly all stream ciphers. It has a remarkable property: applying the same key twice returns the original value. If $P \oplus K = C$, then $C \oplus K = P$. This means that XOR scrambling is perfectly reversible — running the same keystream over the scrambled output recovers the original image exactly. In Cipher's XOR mode, the Depth control determines how many bit positions of each pixel are XOR'd with the keystream. At minimum depth, only the least significant bits are affected, producing subtle noise. At maximum depth, all ten bits are flipped, producing a fully scrambled signal indistinguishable from noise.

### Channel Permutation and Information Scrambling

Permute mode takes a fundamentally different approach to visual disruption. Instead of altering pixel *values*, it rearranges which channel carries which information. Based on LFSR bit 12, the program decides per-pixel whether to swap Y with U or Y with V. The effect is visually dramatic: luminance information appears as chroma and vice versa, creating kaleidoscopic color shifts that depend entirely on the LFSR state at each pixel position. Because the LFSR is deterministic, the permutation pattern is spatially structured — not random noise, but a complex pseudo-random *tiling* of channel swaps across the frame.

### Position-Dependent Processing

Most video effects apply uniformly across every pixel. Cipher breaks this convention by making its processing spatially variable. In stream mode, the LFSR advances every pixel clock, so each pixel gets a unique keystream value — creating fine-grained, pixel-level scrambling. In block mode, the LFSR state is held constant across NxN pixel groups (controlled by the Block Size knob), so clusters of adjacent pixels share the same scramble operation. Block mode produces a mosaic-cipher appearance reminiscent of block ciphers like AES, where the image fragments into uniform tiles of encrypted data. The block size interpolates from single-pixel granularity to large rectangular regions, offering a continuum between noise and mosaic.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Y/U/V Channels ─────────────────────────────────────────────
│   │
│   ├─ 1. Input Register         (latch Y, U, V + parameter snapshot)
│   │
│   ├─ 2. Keystream Generation    (16-bit LFSR → key_y, key_u, key_v)
│   │      ├── Depth Mask         (depth → bit mask: 3–10 bits active)
│   │      └── Scramble Scale     (scramble < 50% → shift key right)
│   │
│   ├─ 3. Mode Select ───────────┬──────────────────────────────
│   │      │                     │
│   │      ├─ Mode 00: XOR       (channels XOR keystream)
│   │      ├─ Mode 01: Permute   (swap Y↔U or Y↔V per LFSR bit 12)
│   │      ├─ Mode 10: Rotate    (circular bit rotation by Shift amt)
│   │      └─ Mode 11: Invert    (complement then XOR keystream)
│   │
│   ├─── Channel Select ─────────┬──────────────────────────────
│   │      │                     │
│   │      ├─ "Y only"           (process Y, pass U/V through)
│   │      ├─ "UV only"          (pass Y through, process U/V)
│   │      ├─ "All"              (process Y, U, V)
│   │      └─ "Swap"             (process Y, swap U↔V)
│   │
│   ├─ 4. Invert Toggle          (optional complement of all channels)
│   │
│   └─ 5. Output Compose         (processed Y, U, V)
│
├── Interpolator (Mix) ─────────────────────────────────────────
│   └─ 4-clock wet/dry blend     (dry=delayed input, wet=processed)
│
├── Sync Signals ───────────────────────────────────────────────
│   └─ Delay pipeline match (hsync, vsync, field: 8+3 clocks)
│
└── Bypass Mux ─────────────────────────────────────────────────
    └─ Select delayed original or mixed signal
```

The pipeline is intentionally shallow — only four processing clocks plus four interpolator clocks — because the core operations (XOR, permutation, rotation, complement) are single-cycle combinational functions masked into a registered pipeline. The LFSR generates a single 16-bit word per clock; the architecture slices this into three overlapping 10-bit windows for the Y, U, and V key streams: `key_y` draws from bits [9:0], `key_u` from bits [15:6], and `key_v` from a wrapped concatenation of bits [7:0] and [15:14]. This overlap means the three channels receive correlated but distinct keystreams from a single LFSR, producing structured rather than independent noise across the color channels.

The depth mask is a critical interaction point. It is built as a contiguous run of ones starting from bit 0, with the number of active bits determined by the Depth knob in eight quantized steps (3 bits through 10 bits). The Scramble knob further attenuates the key by right-shifting when its value is below 50%, creating a two-stage intensity control: Depth selects *which* bits can be affected, Scramble controls *how strongly* they are affected.

---

## Parameter Reference

<img src={cipher_control_panel} alt="Videomancer front panel with Cipher loaded"/>
*Videomancer's front panel with Cipher active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Key
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

The Key knob modifies the LFSR seed, altering the entire pseudo-random keystream that drives all four scramble modes. Different key values produce entirely different spatial patterns of scrambling — think of it as choosing which cipher key to use. Because the LFSR is deterministic, the same Key setting always produces the same pattern when combined with block mode and a fixed frame. Sweeping the Key knob in real time shifts the scramble pattern across the image like a rolling code lock searching for alignment.

---

#### Knob 2 — Depth
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Depth controls how many bit positions of each pixel value are exposed to the keystream. At minimum, only the three least significant bits are affected — a subtle shimmer barely visible in the 10-bit signal. As Depth increases, the mask widens through eight quantized steps until all ten bits participate, producing maximum disruption. In XOR mode, full depth means every bit of every pixel is flipped according to the keystream. In Rotate mode, full depth permits the widest rotation angles. Think of Depth as the "classification level" of the cipher — how much of the signal is considered sensitive enough to encrypt.

---

#### Knob 3 — Scramble
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Scramble is a secondary intensity control that scales the keystream *after* depth masking. When Scramble is below roughly 25%, the masked key is right-shifted by three positions, reducing its effective magnitude by a factor of eight. Between 25% and 50%, a single-position right shift halves the key. Above 50%, the full masked key is applied. This creates a smooth ramp from nearly transparent processing to full-intensity scrambling, allowing fine control over the transition between recognizable source and encrypted noise.

---

#### Knob 4 — Shift
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

The Shift knob controls the circular bit rotation amount used exclusively in Rotate mode (Mode 10). The 10-bit register value is divided by 128 to yield a rotation count from 0 to 7 positions. At zero rotation, pixels pass through unchanged. As the rotation increases, the binary representation of each pixel value is cyclically shifted — the most significant bits wrap around to the least significant positions. This creates a nonlinear value remapping that is neither simple scaling nor inversion, but a deterministic permutation of the binary encoding itself.

---

#### Knob 5 — Block Sz
| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 5 |

Block Size determines the spatial granularity of the scrambling pattern. In stream mode, this control has no effect — each pixel receives its own LFSR state. In block mode, it defines the NxN pixel region that shares a single keystream value. Small blocks (low values) produce fine mosaic textures; large blocks create broad tiles of uniformly scrambled pixels. The stepped control (8 discrete sizes) corresponds to block dimensions that divide evenly into typical scan line lengths, preventing partial-block artifacts at line boundaries.

---

#### Knob 6 — Feedback
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 0% |
| Suffix | % |

Feedback controls a recirculation path that mixes a portion of the scrambled output back into subsequent processing. At 0%, the pipeline operates purely feed-forward. As Feedback increases, the scramble pattern begins to self-reference — the output of one frame's encryption influences the keystream interaction of subsequent pixels, creating evolving textures that drift and mutate over time. High feedback values with block mode produce cellular automaton-like patterns where each tile's state depends on its neighbors' previous states.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Mode** | XOR | Permute |
| **8 — Channels** | Y only | UV only |
| **9 — Pattern** | Stream | Block |
| **10 — Invert** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles divide into three functional groups. Toggles 7 and 8 together define the processing character: Toggle 7 selects among four scramble algorithms (XOR, Permute, Rotate, Invert), while Toggle 8 selects which color channels are affected (Y only, UV only, All, Swap). Toggle 9 chooses between stream processing (pixel-by-pixel LFSR advance) and block processing (held LFSR state across pixel groups). Toggle 10 applies a post-scramble inversion that complements the entire processed signal. Toggle 11 is the bypass mux. The Mode and Channels toggles together create a 4×4 matrix of sixteen distinct scramble configurations, each producing a qualitatively different visual result.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

The Mix fader controls the wet/dry blend between the scrambled (wet) signal and the delayed original (dry) signal via a 4-clock linear interpolator. At 0%, the output is pure source — no scrambling visible. At 100%, the output is fully processed. Intermediate positions produce a translucent overlay effect where the scrambled texture blends with the original image, useful for creating subtle encryption veils or partial-depth glitch effects that retain the readability of the source content.

---

## Guided Exercises

These exercises progress from basic XOR noise through channel permutation to compound scramble effects. Each builds on the previous, introducing one new mode or interaction at a time.

### Exercise 1: XOR Keystream Noise

<img src={cipher_exercise1_result} alt="XOR Keystream Noise result"/>
*XOR Keystream Noise — simulated result across source images.*
**Source**: A live camera feed or recorded footage with clear subject matter and moderate contrast.

**Objective**: Understand how Key, Depth, and Scramble interact to produce XOR-based pseudo-random noise overlays of varying intensity.

1. **Baseline**: Confirm Mode is set to XOR, Channels to All, and Pattern to Stream. Set Depth to 50%. The image should show visible noise — bits of the source flipped by the LFSR keystream.
2. **Depth sweep**: Slowly reduce Depth towards 0%. The noise retreats into the least significant bits, becoming a barely perceptible shimmer. Now sweep Depth up to 100%. The noise engulfs the image as all ten bits participate.
3. **Scramble attenuation**: With Depth at 75%, bring Scramble down from 50% to 0%. The noise intensity drops in two visible steps as the keystream is right-shifted. Return Scramble to 75%.
4. **Key variation**: Slowly sweep the Key knob. The spatial pattern of the noise shifts across the image — different key values produce different LFSR sequences and therefore different pixel patterns.
5. **Invert**: Toggle Invert on. The entire noise texture complements, producing a negative-image version of the scrambled output.

**Key concepts**: XOR is a bitwise operation — each bit is independently flipped or preserved, Depth controls how many bits are exposed to the keystream, Scramble attenuates the key, different Key values produce entirely different pseudo-random sequences

---

### Exercise 2: Channel Permutation Mosaics

<img src={cipher_exercise2_result} alt="Channel Permutation Mosaics result"/>
*Channel Permutation Mosaics — simulated result across source images.*
**Source**: Footage with strong color contrast — the macaw image or similar with distinct saturated regions.

**Objective**: Explore Permute mode with block processing to create mosaic-cipher textures where tiles of the image have their color channels rearranged.

1. **Switch to Permute**: Set Mode to Permute and Pattern to Block. Set Block Size to about position 5 (medium tiles). The image fragments into rectangular tiles, each with its luma and chroma channels swapped according to the LFSR state.
2. **Block size sweep**: Reduce Block Size to minimum — tiles shrink to a fine mosaic. Increase to maximum — large regions share a single channel permutation, creating broad color-shifted zones.
3. **Channel selection**: Switch Channels from All to Y Only. Now only the luminance channel is permuted — the result is monochrome channel-swapped brightness. Switch to UV Only to permute just the color channels, preserving the source brightness.
4. **Key rotation**: Sweep Key slowly. The permutation pattern shifts — different tiles change their channel assignment — like watching a cipher wheel rotate.
5. **Add depth**: Switch back to All channels and increase Depth. In Permute mode, the depth mask modifies which key bits are used for the permutation decision, subtly altering the pattern.

**Key concepts**: Permutation reorders information without destroying it, block mode creates spatial tiling of scramble states, channel selection isolates the permutation to luma or chroma independently

---

### Exercise 3: Compound Rotation and Feedback

<img src={cipher_exercise3_result} alt="Compound Rotation and Feedback result"/>
*Compound Rotation and Feedback — simulated result across source images.*
**Source**: High-contrast footage or graphic patterns — test bars, geometric shapes, or text.

**Objective**: Combine Rotate mode with Feedback and Invert for evolving, self-referencing bit-rotation textures.

1. **Rotate baseline**: Set Mode to Rotate, Channels to All, Pattern to Stream. Set Shift to about 50%. The image's binary representation is cyclically rotated — brightness values remap nonlinearly, producing a distinctive digital texture unlike simple scaling or inversion.
2. **Shift sweep**: Move Shift from 0% to 100%. At zero, no rotation occurs. Each step introduces a new rotation amount, and the visual output changes dramatically at each binary step — the mapping is highly nonlinear.
3. **Enable feedback**: Slowly bring Feedback from 0% to about 40%. The scramble pattern begins to self-reference, creating evolving textures that drift and mutate. Higher values push toward recursive noise.
4. **Block mode mosaic**: Switch Pattern to Block. The rotation is now applied per-tile, creating a mosaic where each block has a different rotation amount. Combined with feedback, the tiles develop individual evolutionary trajectories.
5. **Compound transformation**: Enable Invert. The post-scramble complement interacts with the rotation to create a second layer of remapping. Toggle Invert on and off to see how it transforms the texture.
6. **Mix blend**: Pull Mix down to about 60%. The rotated texture blends with the original, creating a ghostly double-exposure where the source and its encrypted version coexist.

**Key concepts**: Bit rotation is a nonlinear value permutation distinct from scaling or inversion, feedback creates temporal evolution in the scramble pattern, compound operations (rotate + invert) multiply the visual complexity

---


## Tips

- **XOR is reversible**: If you can recreate the same LFSR sequence (same Key, same frame position), XOR'ing the scrambled output a second time recovers the original image exactly. Route the output back through a second Cipher instance with identical settings as a visual proof.
- **Depth before Scramble**: Set Depth first to choose which bits participate, then use Scramble to fine-tune intensity. Depth is the coarse control (eight steps), Scramble is the fine attenuator.
- **Block mode for structure**: Stream mode creates noise; Block mode creates mosaics. When compositing Cipher's output with other programs, Block mode tends to produce more visually coherent results because adjacent pixels share the same transformation.
- **Permute preserves energy**: Unlike XOR, Permute mode doesn't add or remove information — it rearranges it. This makes Permute-mode output excellent for feedback loops, as the signal energy doesn't grow or decay.
- **Invert doubles your palette**: Every Mode × Channels combination produces a different visual texture. Toggling Invert effectively doubles the number of available textures to 32 distinct configurations (4 modes × 4 channel selections × 2 invert states).
- **Feedback drift**: Low feedback (10–30%) creates slow textural evolution. High feedback (>60%) rapidly pushes toward noise saturation. The sweet spot for interesting temporal patterns is usually 20–40%.
- **Mix for encryption veils**: Setting Mix to 30–50% creates a translucent scramble overlay — the source image remains readable but visually "classified," as if viewed through an encryption layer. Useful for title screens and transition effects.
- **Key as performance control**: In live performance, assign the Key knob to a MIDI controller. Sweeping Key in real time shifts the entire scramble pattern across the frame like a rolling cipher, creating dynamic visual motion from a static source.

---

## Glossary

| Term | Definition |
|------|------------|
| **AES** | Advanced Encryption Standard; a widely used block cipher that processes data in fixed-size chunks, referenced here as the visual inspiration for Cipher's block-mode mosaic textures. |
| **Bit rotation** | A circular shift of a binary value where bits shifted off one end wrap to the other end, producing a nonlinear value remapping distinct from simple addition or inversion. |
| **Block cipher** | A cryptographic algorithm that encrypts data in fixed-size groups (blocks) rather than one element at a time; Cipher's block mode emulates this visual pattern. |
| **Complement** | Bitwise NOT; flipping every bit of a value so that 0 becomes 1 and vice versa, producing a luminance and color negative when applied to video data. |
| **Galois LFSR** | A Linear Feedback Shift Register variant where XOR taps are applied during the shift operation itself, producing a maximal-length pseudo-random sequence efficiently in hardware. |
| **Keystream** | A sequence of pseudo-random values generated by the LFSR and used to drive the scramble operations; analogous to the key material in a stream cipher. |
| **LFSR (Linear Feedback Shift Register)** | A shift register whose input bit is computed by XOR of selected tap positions, generating a deterministic pseudo-random bit sequence that cycles through all non-zero states. |
| **LSB (Least Significant Bit)** | The lowest-order bit in a binary value; the first bits affected when Depth is at minimum, producing subtle low-amplitude noise. |
| **MSB (Most Significant Bit)** | The highest-order bit in a binary value; when included in the depth mask, its modification produces the most visually dramatic changes. |
| **Seed** | The initial state loaded into the LFSR before sequence generation begins; different seeds produce different pseudo-random sequences. |
| **Stream cipher** | A cryptographic algorithm that encrypts data one element at a time using a keystream; Cipher's stream mode applies this principle per-pixel. |
| **XOR (Exclusive-OR)** | A bitwise logic operation that outputs 1 when inputs differ and 0 when they match; the fundamental reversible operation underlying all of Cipher's scrambling modes. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V); the native format of Videomancer's 30-bit video pipeline. |

---
