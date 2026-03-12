---
draft: true
sidebar_position: 12
slug: /instruments/videomancer/aurora
title: "Aurora"
image: /img/instruments/videomancer/aurora/aurora_hero.png
description: "In the early 1990s, the Amiga demoscene invented an effect called \"shadebobs\" — small sprites drawn additively into a framebuffer without ever clearing the screen."
---

import aurora_hero from '/img/instruments/videomancer/aurora/aurora_hero.png';
import aurora_animation from '/img/instruments/videomancer/aurora/aurora_animation.gif';
import aurora_control_panel from '/img/instruments/videomancer/aurora/aurora_control_panel.png';
import aurora_exercise1_result from '/img/instruments/videomancer/aurora/aurora_exercise1_result.gif';
import aurora_exercise2_result from '/img/instruments/videomancer/aurora/aurora_exercise2_result.gif';
import aurora_exercise3_result from '/img/instruments/videomancer/aurora/aurora_exercise3_result.gif';

# Aurora

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={aurora_hero} alt="Aurora hero image"/>
*Aurora painting luminous Lissajous trails in rainbow mode — overlapping orbits create prismatic interference patterns on a persistent framebuffer.*
<img src={aurora_animation} alt="Aurora animated output"/>
*Aurora output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

In the early 1990s, the Amiga demoscene invented an effect called "shadebobs" — small sprites drawn additively into a framebuffer without ever clearing the screen. As each bob traced its path, it left behind a trail of accumulated brightness, painting luminous interference patterns in a kind of long-exposure drawing with light. Aurora recreates this technique in real-time FPGA hardware.

The program maintains a persistent 40×32 pixel framebuffer stored in BRAM (stride 64, fitting in 4 BRAM tiles at 2,048 bytes). Two or four "bobs" — single-pixel stamps — move in Lissajous orbits across this canvas. Each frame, the bobs are additively stamped into the framebuffer (brightness values are added, saturating at maximum). A global fade gradually dims the entire canvas, creating a dynamic equilibrium where new strokes glow brightly while old ones decay to darkness. The framebuffer is read out during active video, upscaled to full resolution via nearest-neighbor (each framebuffer pixel covers a 32×32 block of output pixels), and colorized through one of four palette modes before mixing with the input video.

The name *Aurora* refers to the aurora borealis — curtains of light that shimmer and shift across the polar sky. With the heat map or rainbow colorizer and a trefoil Lissajous pattern, the resemblance is unmistakable: luminous arcs of green and pink light glowing against darkness.

---

## Quick Start

1. **Aurora is a painting program**: Unlike most Videomancer programs that transform each frame independently, Aurora accumulates over time. Be patient — allow 30–60 seconds after each control change to see the full effect evolve.
2. **Fade Rate is the memory control**: Zero fade = permanent long-exposure painting. Maximum fade = short comets. The middle range creates the most visually interesting dynamic equilibrium.
3. **Pattern + Speed + Orbit Size define the drawing**: These three controls determine *what* is drawn. Intensity and Fade Rate determine *how* it looks. Color mode determines *what color* it is. Separate these mental models.

---

## Background

### What Are Shadebobs?

**Shadebobs** were an iconic effect invented on the Amiga home computer, popularized by demoscene groups like Sanity, Andromeda, and Scoopex in the early 1990s. The technique exploited the Amiga's planar graphics hardware, which could efficiently perform bitwise addition to a framebuffer. A small sprite (the "bob") is drawn at successive positions without clearing the screen. Each draw additively increases the brightness of the pixels it touches. As the bob traces complex mathematical curves, it paints elaborate luminous interference patterns that glow with accumulated light.

The visual result is ethereal: overlapping dots of light create webs, spirals, and curtain-like formations. The longer the effect runs, the richer and more complex the pattern becomes. The characteristic "smeared light" quality — where the bob builds up brightness at intersection points — is unlike any other visual effect.

### What Are Lissajous Curves?

**Lissajous curves** (also called Bowditch curves) are the trajectories produced when two sinusoidal oscillations are combined along perpendicular axes:

$x(t) = A \sin(f_x t + \varphi_x)$

$y(t) = B \sin(f_y t + \varphi_y)$

The shape of the curve depends on the frequency ratio $f_x : f_y$ and the phase relationship. At 1:1, the path is an ellipse (or circle with 90° phase offset). At 1:2, it traces a figure-8. At 2:3, a trefoil. Higher ratios produce increasingly complex rosettes. Aurora provides eight preset frequency ratios, each producing a distinct orbital pattern.

### What Is a Persistent Framebuffer?

Unlike most video effects programs on Videomancer — which process each frame independently — Aurora maintains **persistent state** between frames. The 40×32 framebuffer (8-bit luminance per pixel, power-of-2 stride of 64) stores the accumulated painting from all previous frames. New bob stamps are added. A fade pass subtracts a small amount from every pixel each frame. This creates a memory effect: the canvas remembers, and the bobs draw a continuous record of their motion.

The fade rate controls how long that memory lasts. At zero fade, the canvas accumulates indefinitely until saturated — a permanent record. At maximum fade, trails vanish almost immediately, and only the bobs themselves are visible — bright heads with no tails. Between these extremes, you get trails of varying length, from long luminescent ribbons to short comet tails.

### What Is Additive Compositing?

When a bob stamps into the framebuffer, its brightness value is **added** to the existing pixel value (clamped to 255). This is fundamentally different from painting *over* pixels — it means overlapping bob paths create brighter intersections. Where two paths cross, the brightness is the sum of both contributions. This additive accumulation creates the luminous node structure characteristic of shadebobs: a web of bright intersection points connected by dimmer trail segments.


---

## Signal Flow

```
┌──────────────────────────────────────────────────────────────────┐
│  Phase Increment (independent process, triggered at vsync)       │
│     ├─ For each bob: phase_x += speed × preset.fx (or fixed)    │
│     │                 phase_y += speed × preset.fy (or fixed)    │
│     └─ 16-bit phase accumulators, wrapping                       │
│           ◄── Speed (pot 1), Pattern (pot 2)                     │
│                                                                  │
│  Frame Update FSM (during vertical blanking)                     │
│                                                                  │
│  1. Bob Position Compute (BOB_COMPUTE → BOB_MULT → BOB_CLAMP)   │
│     ├─ For each active bob:                                      │
│     │   sine_x = quarter_wave_LUT(phase_x[bob](15:8))           │
│     │   sine_y = quarter_wave_LUT(phase_y[bob](15:8))           │
│     │   pos = FB_center + shift_right(sine(9:4) × amp(9:4), 2)  │
│     └─ Clamp to 1..W−2 / 1..H−2                                │
│           ◄── Orbit Size (pot 6), Bob Count (toggle 8)           │
│                                                                  │
│  2. Global Fade (FADE_RD / FADE_WR, 2-cycle read-modify-write)  │
│     ├─ For each pixel in 40×32 FB (2048 addresses):              │
│     │   fb[addr] = max(0, fb[addr] − fade_subtract)             │
│     └─ fade_subtract = fade_rate(9:6) → 0..15 per frame         │
│           ◄── Fade Rate (pot 3)                                  │
│                                                                  │
│  3. Bob Stamp (STAMP_RD / STAMP_WR, 1×1 additive)               │
│     ├─ For each bob:                                             │
│     │   brightness = intensity(9:2) → 8-bit                     │
│     │   fb[addr] = min(255, fb[addr] + brightness)               │
│     └─ Saturating 9-bit addition                                 │
│           ◄── Intensity (pot 4), Bob Count (toggle 8)            │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  Readout Pipeline (during active video)                          │
│                                                                  │
│  Stage 1: Address generation                                     │
│     └─ fb_x = hcount(11:5), fb_y = vcount(10:5)  (÷32)         │
│        clamped to FB_W−1 and FB_H−1                              │
│        addr = fb_y × 64 + fb_x  (shift_left + OR)               │
│                                                                  │
│  Stage 2: BRAM read (1 clk latency)                              │
│     └─ 8-bit luminance value                                     │
│                                                                  │
│  Stage 3a: Scale + pre-register                                  │
│     └─ luma_10 = fb_byte & "00"  (8-bit → 10-bit, ×4)           │
│                                                                  │
│  Stage 3b: Colorize (from registered fb_byte and luma)           │
│     ├─ Mono:    Y = luma, UV = pre-computed hue tint             │
│     ├─ Heat:    Y = luma, UV = 4-band map via fb_byte(7:6)       │
│     ├─ Rainbow: Y = luma, UV = 4-quadrant hue via                │
│     │           fb_byte(7:6) + hue(9:8) → 2-bit index            │
│     └─ Duo:     Y = luma, UV = 2-color split on fb_byte(7)      │
│           ◄── Color Mode (toggle 7), Hue (pot 5)                 │
│                                                                  │
│  Stage 4: Brightness scaling (6×6 multiply)                      │
│     └─ Y = (color_Y(9:4) × orbit_size(9:4)) >> 2                │
│           ◄── Orbit Size (pot 6)                                 │
│                                                                  │
│  Stage 5: Output register                                        │
│                                                                  │
│  Stages 6–9: Interpolator (4 clk, per Y/U/V)                    │
│     └─ Mix = lerp(input_delayed, processed, mix_amount)          │
│           ◄── Mix (fader 12)                                     │
└──────────────────────────────────────────────────────────────────┘

 Output = bypass ? input_delayed : mix_result
           ◄── Bypass (toggle 11)
```

Aurora is fundamentally different from Videomancer's signal-processing programs. Instead of transforming the input video frame-by-frame, it maintains an internal canvas (framebuffer) with persistent state across frames. The input video is only used in two ways: (1) Video Seed mode paints input luminance into the framebuffer, and (2) the Mix fader crossfades between the generated image and the delayed input. The frame update FSM (bob position compute → fade → stamp) runs during vertical blanking using 2-cycle read-modify-write through BRAM ports; the readout pipeline runs during active video, sharing the same BRAM read port via an address mux. Phase increments run in a separate process triggered at vsync, decoupled from the FSM to avoid adding carry chains to the critical path. The Orbit Size pot serves double duty: it controls the Lissajous amplitude during bob position computation and also scales the readout luminance in the brightness scaling stage.

---

## Parameter Reference

<img src={aurora_control_panel} alt="Videomancer front panel with Aurora loaded"/>
*Videomancer's front panel with Aurora active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

At 0%, the bobs are frozen in place — they stamp the same position every frame, burning a bright static dot into the framebuffer. As you increase speed, the bobs trace their Lissajous paths faster. Very high speeds make the bobs race around their orbits so quickly that the trails blur together into continuous luminous bands. The speed pot scales phase increment per frame, so the relationship between Speed and visual velocity depends on the Pattern preset — complex presets with high frequency ratios produce faster apparent motion for the same Speed setting. Internally, controls the orbital velocity of the bobs.

---

#### Knob 2 — Pattern
| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 2 |

Selects one of eight Lissajous frequency ratio presets that determine the orbital pattern shape. This is a **stepped** control with 8 discrete positions:

| Step | Ratio (fx:fy) | Pattern |
|------|---------------|---------|
| 1 | 1:1 | Circle / ellipse |
| 2 | 1:2 | Figure-8 |
| 3 | 2:3 | Trefoil |
| 4 | 3:4 | Complex rosette |
| 5 | 3:5 | Five-petaled flower |
| 6 | 1:3 | Lemniscate variant |
| 7 | 5:7 | Complex, slow-repeat |
| 8 | 2:5 | Asymmetric loop |

Each preset produces a fundamentally different painting pattern. Simple ratios (1:1, 1:2) produce clean, symmetric curves. Complex ratios (5:7, 2:5) produce intricate, dense patterns that fill more of the canvas before repeating.

---

#### Knob 3 — Fade Rate
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |
| Suffix | % |

At 0%, no fade occurs and the canvas accumulates indefinitely until every pixel saturates at maximum brightness. This produces a permanent luminous record of every orbit the bobs have traced. At maximum, the fade is so aggressive that trails disappear almost immediately, leaving only the bright bob positions visible as moving dots. Internally, controls the global fade rate — how quickly the framebuffer dims between frames.

The artistic sweet spot is in the middle range, where trails persist long enough to show the Lissajous curve structure but fade before the canvas saturates. The fade rate interacts strongly with Speed: fast bobs with slow fade create long flowing trails; slow bobs with fast fade create short bright arcs.

---

#### Knob 4 — Intensity
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Controls the brightness of each 1×1 bob stamp — how much luminance is added per pixel per frame. The 10-bit register is scaled to 8-bit via `intensity(9:2)`, giving a brightness range of 0–255 per stamp. At low intensity, bobs produce faint traces that build up slowly through repeated passes. At high intensity, each stamp burns a bright mark into the framebuffer, creating vivid trails that saturate quickly.

The interaction with Fade Rate is important: high intensity with high fade produces bright but short trails (comets). High intensity with low fade produces trails that saturate quickly, filling the canvas with maximum brightness. Low intensity with low fade produces subtle, slowly accumulating patterns that take minutes to develop.

---

#### Knob 5 — Hue
| Property | Value |
|----------|-------|
| Range | 0deg – 360deg |
| Default | 0deg |
| Suffix | deg |

Controls the color tint applied to the framebuffer output. The hue value is pre-computed into UV offsets at vsync only (not per-pixel), keeping it off the readout pipeline critical path. The effect depends on the active Color Mode (Toggle 7):

- **Mono mode**: The Hue pot sets the UV offset from neutral via a 4-quadrant computation, tinting the monochrome output. Sweep through warm amber, cool blue, green, magenta.
- **Heat mode**: Hue has no direct effect — the 4-band thermal palette is fixed.
- **Rainbow mode**: The upper 2 bits of the Hue pot (`hue(9:8)`) are added to the upper 2 bits of the framebuffer luminance (`fb_byte(7:6)`) to index a 4-entry computed color map. Different Hue positions shift which quadrant of colors appear at each luminance level.
- **Duo mode**: Hue has no direct effect — the two-color pair is fixed (complementary cyan/warm tones split on `fb_byte(7)`).

---

#### Knob 6 — Orbit Size
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |
| Suffix | % |

Serves a dual role: it controls both the amplitude of the Lissajous orbits and the brightness of the readout image. For orbit amplitude, the upper 6 bits of the register (`orbit_size(9:4)`) are used as a 7-bit unsigned multiplier against the sine lookup result during bob position computation. At 0%, all bobs converge on the center of the 40×32 framebuffer. As you increase Orbit Size, the bobs sweep wider paths, clamped to a 1-pixel border. In the readout pipeline, Orbit Size is also the multiplier in the brightness scaling stage (`color_Y(9:4) × orbit_size(9:4)`), so turning it down dims both the orbit amplitude and the output image simultaneously.

Small orbit sizes create tight, dim patterns concentrated in the center of the screen. Large orbit sizes create sweeping, bright curves that fill the entire display.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Color** | Mono | Duo |
| **8 — Bobs** | 2 Bobs | 4 Bobs |
| **9 — Clear** | Off | On |
| **10 — Video Seed** | Off | On |
| **11 — Bypass** | Off | On |

The five toggle switches control four independent binary options plus a combined 2-bit color mode selector. Toggle 7 is a 4-position selector (using 2 bits from `registers_in(6)(1:0)`) that dramatically changes the visual character. Toggles 8–11 are independent binary controls mapped to individual bits of register 6.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry crossfade between the input video (delayed to match pipeline latency) and the Aurora output. At 0% (fully down), the output is pure input video — Aurora is inaudible. At 100% (fully up), the output is pure Aurora. Intermediate positions blend the two, allowing the aurora pattern to be superimposed over live video at any opacity. This is the primary creative control for compositing the generative pattern with external footage.


#### Switch 11 — Bypass
| Property | Value |
|----------|-------|
| Off | Processing active |
| On | Bypass engaged |

Routes the unprocessed input signal directly to the output, bypassing all Aurora processing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use for instant A/B comparison between the raw input and the processed result.---
## Guided Exercises

These exercises progress from basic trail painting to complex multi-bob compositions with colorization. Because Aurora is a generative program with persistent state, each exercise unfolds over time — allow 30–60 seconds after each parameter change to observe the full effect.

### Exercise 1: Classic Shadebob Trails

<img src={aurora_exercise1_result} alt="Classic Shadebob Trails result"/>
*Classic Shadebob Trails — simulated result across source images.*
**What You'll Create**: Learn how speed, fade, and intensity interact to control trail character.

1. **Start clean**: Toggle Clear (Switch 9) to reset the framebuffer.
2. **Set the orbit**: Choose Pattern preset 4 (rosette). Set Orbit Size to ~80%.
3. **Fast speed**: Set Speed to ~80%. Watch two bobs race around the complex rosette path, painting bright trails across the canvas.
4. **Minimal fade**: Set Fade Rate to ~6%. With almost no fade, trails accumulate permanently — the canvas fills with a luminous long-exposure record of every orbit pass.
5. **Maximum intensity**: Set Intensity to 100%. Each 1×1 stamp burns a bright mark into the framebuffer, and intersection points where both bobs cross saturate to full brightness.
6. **Warm tint**: Set Hue to ~15%. The mono trails pick up a subtle warm tone. Sweep Hue to shift the tint across the spectrum.

**Key concepts**: Persistent framebuffer accumulates over time, fade rate controls trail length, intensity controls brightness per stamp, near-zero fade creates permanent long-exposure painting, rosette creates dense self-intersecting patterns

---

### Exercise 2: Rainbow Aurora

<img src={aurora_exercise2_result} alt="Rainbow Aurora result"/>
*Rainbow Aurora — simulated result across source images.*
**What You'll Create**: Explore colorization modes and the interaction between pattern complexity and color mixing.

1. **Clear and prepare**: Toggle Clear. Set Pattern to 5 (five-petal flower), Orbit Size to ~80%, Speed to ~60%.
2. **Enable Rainbow**: Switch Color (Toggle 7) to Rainbow. The trails immediately display colored bands — the 4-quadrant colorizer maps luminance regions to distinct hues.
3. **Four bobs**: Switch Bobs (Toggle 8) to 4 Bobs. The five-petal pattern with 4 bobs creates dense, overlapping floral structures.
4. **Minimal fade**: Set Fade Rate to ~6% and Intensity to 100%. With near-permanent trails and maximum brightness, the canvas fills with vivid color bands.
5. **Watch intersections**: Where trails overlap, the additive luminance pushes pixels across quadrant boundaries, shifting their color assignment.
6. **Rotate the quadrants**: Sweep Hue (Knob 5). The 4-quadrant color assignment rotates — the same luminance bands map to different color regions.
7. **Clear and observe**: Toggle Clear to restart. Watch the rainbow pattern build up from scratch.

**Key concepts**: Rainbow mode maps luminance quadrants to distinct hues, overlapping trails shift quadrant boundaries through additive brightness, Hue rotates the 4-quadrant color assignment, 4 bobs and low fade create dense saturated patterns

---

### Exercise 3: Video Seed Composition

<img src={aurora_exercise3_result} alt="Video Seed Composition result"/>
*Video Seed Composition — simulated result across source images.*
**What You'll Create**: Combine live video seeding with generative bob painting.

1. **Setup**: Set Mix to ~70% to blend Aurora over the input.
2. **Enable Video Seed**: Switch Video Seed (Toggle 10) to On. The input video luminance now feeds into the framebuffer.
3. **Add bobs**: Set moderate Speed (~35%), Pattern 2 (figure-8), Orbit Size ~60%.
4. **Adjust fade**: Set Fade Rate to ~40%. The video image persists while bobs paint luminous figure-8 trails over it.
5. **Rainbow on video**: Switch to Rainbow mode. The video-seeded luminance maps through the 4-quadrant colorizer, creating a false-color image with luminous bob trails woven through it.
6. **Increase intensity**: Raise Intensity. The bobs burn through the video image, leaving bright paths that overpower the seeded content.
7. **Clear and rebuild**: Toggle Clear to erase, then watch the video image re-seed while the bobs paint over it.

**Key concepts**: Video Seed feeds input luminance into the persistent framebuffer, creating hybrid generative/live compositions.  Mix fader controls the blend ratio, colorizer applies to both seeded video and bob trails

---


## Tips

- **Clear is your eraser**: When you change Pattern or Orbit Size, toggle Clear to start fresh. Old trails from the previous pattern will otherwise persist until they fade naturally.
- **Rainbow intersections create unique colors**: In Rainbow mode, overlapping trails shift luminance upward, which shifts the 2-bit quadrant index. Intersection points that cross luminance band boundaries display different color quadrants than surrounding trail segments.
- **Video Seed creates hybrid compositions**: Enable Video Seed and set moderate Mix to superimpose luminous trails over live footage. The video image becomes a canvas that the bobs paint over.
- **Feedback loops create aurora evolution**: Routing output back to input creates recursive accumulation. The aurora trails feed back into the framebuffer through Video Seed, creating self-reinforcing patterns that evolve unpredictably.
- **Bypass for A/B comparison**: Switch 11 instantly shows the unprocessed input for comparison.

---

## Glossary

| Term | Definition |
|------|------------|
| **Additive compositing** | A blending mode where pixel brightness values are summed rather than overwritten, causing overlapping elements to appear brighter at intersection points. |
| **Demo** | A computer art subculture focused on producing real-time audio-visual programs (demos) that showcase creative programming within hardware constraints. |
| **Framebuffer** | A block of memory storing a complete image; Aurora's framebuffer persists across frames, accumulating luminance from bob stamps over time. |
| **FSM** | Finite State Machine; the sequential control logic that coordinates bob position computation, global fade, and stamp operations during vertical blanking. |
| **Lissajous curve** | A parametric curve traced by combining two perpendicular sinusoidal oscillations at different frequencies, defining each bob's orbital path. |
| **Nearest-neighbour upscaling** | An image scaling method that assigns each output pixel the value of its closest source pixel, producing the blocky enlargement visible in Aurora's low-resolution framebuffer. |
| **Phase accumulator** | A digital counter that increments by a fixed step each frame and wraps at overflow, controlling each bob's position along its Lissajous orbit. |
| **Quarter-wave LUT** | A lookup table storing one quarter of a sine cycle; the full waveform is reconstructed through symmetry, saving FPGA memory. |
| **Saturation** | The condition where a pixel value reaches its maximum (255 for 8-bit) and cannot increase further despite additional additive stamps. |
| **Shadebobs** | An Amiga demoscene effect where small sprites are additively stamped into a persistent framebuffer without clearing, painting luminous trail patterns. |
| **Vsync** | Vertical synchronisation; the timing pulse marking the start of each video frame, during which Aurora executes its frame update FSM. |

---
