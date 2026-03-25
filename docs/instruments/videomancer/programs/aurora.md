---
draft: true
sidebar_position: 12
slug: /instruments/videomancer/aurora
title: "Aurora"
image: /img/instruments/videomancer/aurora/aurora_hero.png
description: "In the early 1990s, the Amiga demoscene invented an effect called \"shadebobs\" — small sprites drawn additively into a framebuffer without ever clearing the screen."
---

![Aurora hero image](/img/instruments/videomancer/aurora/aurora_hero_s1.png)
*Aurora painting luminous Lissajous trails into a persistent framebuffer, with additive bob stamps fading into glowing orbital patterns.*

---

## Overview

Aurora is a video synthesizer inspired by the iconic ***shadebob*** effect from the Amiga demoscene of the early 1990s. It draws soft, glowing shapes: called ***bobs***: that trace complex mathematical curves across a persistent canvas. Each bob stamps its gradient footprint additively into a framebuffer, building up brightness wherever its path overlaps. A slow, global fade dims the entire canvas between frames, so fresh strokes glow brightly while old ones dissolve into darkness. The result is an ever-evolving tapestry of luminous trails: aurora-like curtains, spirograph rosettes, and glowing orbital webs.

Because Aurora is a ***synthesis*** program, it generates imagery from scratch rather than processing an incoming video signal. The input video is still available for mixing via the **Mix** fader and for seeding the framebuffer when **Video Seed** is enabled. Four color modes: Monochrome, Heat, Rainbow, and Duo-tone: transform the raw luminance trails into vivid, full-color compositions. The interplay between speed, pattern, fade rate, and color mode gives Aurora a vast palette of visual moods, from meditative, slow-burning nebulae to frantic, electric neon webs.

:::tip
Aurora is a ***generative*** program. It creates its own imagery: you don't need an input signal to see results. Just load the program and watch the trails appear.
:::

### What's In a Name?

The name ***Aurora*** evokes the aurora borealis: shimmering curtains of light that ripple across the polar sky. Just as the northern lights are painted by charged particles tracing magnetic field lines, Aurora's bobs trace mathematical curves and paint luminous trails across the screen. The name also nods to the ancient Roman goddess of dawn, whose light gradually fills the sky: much like the way Aurora's framebuffer slowly fills with accumulated radiance.

---

## Quick Start

1. Load **Aurora**. Two glowing dots immediately begin tracing smooth curves across a black canvas, leaving bright trails that slowly fade behind them. You're watching the default Lissajous pattern at moderate speed.
2. Turn **Speed** (Knob 1) clockwise. The bobs accelerate, painting trails faster and filling the canvas more quickly. Turn it counterclockwise to slow them to a crawl.
3. Turn **Fade Rate** (Knob 3) counterclockwise toward zero. The trails persist much longer, building up a dense, luminous web. Turn it clockwise for a faster fade that leaves only the most recent strokes visible.

---

## Parameters

![Videomancer front panel with Aurora loaded](/img/instruments/videomancer/aurora/aurora_control_panel.png)
*Videomancer's front panel with Aurora active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Speed

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |

**Speed** controls how fast the bobs travel along their orbital paths. At 0%, the bobs are nearly stationary, producing an almost frozen glow at their current positions. As Speed increases, the bobs trace their Lissajous curves more rapidly, sweeping across the canvas and painting trails at a faster rate. At 100%, the bobs move quickly enough that the trails become dense, continuous ribbons of light.

Speed interacts closely with **Fade Rate** (Knob 3). Fast speed with slow fade produces a thick, saturated web of overlapping trails. Fast speed with fast fade creates crisp, animated streamers that chase across the screen.

---

### Knob 2 — Pattern

| Property | Value |
|----------|-------|
| Range | 1 – 8 |
| Default | 2 |

**Pattern** selects one of eight ***Lissajous*** frequency-ratio presets that define the shape of the orbital path. Each preset pairs a horizontal frequency with a vertical frequency to produce a distinct curve:

1. Circle or ellipse (1:1)
2. Figure eight (1:2)
3. Trefoil (2:3)
4. Complex rosette (3:4)
5. Five-petaled flower (3:5)
6. Lemniscate variant (1:3)
7. Complex, slow-repeating weave (5:7)
8. Asymmetric loop (2:5)

Lower presets produce simple, symmetrical curves. Higher presets produce increasingly intricate patterns with longer repeat cycles. The visual density of the trails grows with pattern complexity because the bob revisits different regions of the canvas before returning to its starting point.

:::note
The Pattern knob is quantized to 8 discrete steps. You'll feel it "click" between presets as you turn it.
:::

---

### Knob 3 — Fade Rate

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |

**Fade Rate** controls how quickly the global fade dims the persistent framebuffer. At 0%, the fade is at its slowest: trails linger for a very long time, and the canvas gradually saturates to full brightness. As the value increases, each frame subtracts more luminance from every pixel, so trails disappear more quickly. At 100%, the fade is aggressive: only the very latest bob positions remain visible, producing a tight, comet-like streamer rather than a lingering web.

The interplay between Fade Rate and **Speed** (Knob 1) determines the visual density of Aurora's output. Low fade rate with low speed creates a slowly building, meditative glow. High fade rate with high speed produces energetic, animated trails.

:::tip
A fade rate of zero does not freeze the image: the bobs continue stamping brightness. The canvas will eventually saturate to full white if the fade is too low relative to the speed and intensity.
:::

---

### Knob 4 — Intensity

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |

**Intensity** sets the brightness of each bob stamp. At 0%, the bobs deposit almost no light, and the canvas remains dark. As Intensity increases, each stamp adds more luminance to the framebuffer, causing trails to build up faster and glow more brightly. At 100%, even a single stamp can push pixels close to full brightness, creating bold, high-contrast trails.

Intensity interacts with **Fade Rate** (Knob 3) to set the equilibrium brightness of the canvas. High intensity and low fade rate will saturate the framebuffer quickly; low intensity and high fade rate will keep the image dim and delicate.

---

### Knob 5 — Hue

| Property | Value |
|----------|-------|
| Range | 0deg – 360deg |
| Default | 0deg |

**Hue** shifts the color tint applied to Aurora's luminance trails. The effect of this knob depends on the active color mode selected by the **Color Lo** and **Color Hi** toggles:

- In **Mono** mode, Hue rotates the tint applied to the monochrome trails, sweeping through warm oranges, cool blues, magentas, and greens as you turn the knob from 0 to 360 degrees.
- In **Rainbow** mode, Hue offsets the starting position of the rainbow palette, rotating which colors correspond to which brightness levels.
- In **Heat** and **Duo-tone** modes, Hue has no visible effect (those palettes use fixed color mappings.)

---

### Knob 6 — Orbit Size

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |

**Orbit Size** controls the amplitude of the Lissajous curves: how far the bobs swing from the center of the canvas. At 0%, the bobs barely move from the center, painting a tight, concentrated glow. As the value increases, the bobs swing wider, covering more of the screen. At 100%, the bobs reach the edges of the framebuffer, painting trails that span the full canvas.

:::note
Because the framebuffer operates at 1/16 resolution (120×68 pixels), the bob positions are clamped to stay within bounds. Very large orbit sizes may cause the bobs to cluster near the edges.
:::

---

### Switch 7 — Color Lo

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Color Lo** is the low bit of the two-bit color mode selector. Together with **Color Hi** (Switch 8), it selects one of four color palettes. See the Toggle Group Notes below for the full mode table.

---

### Switch 8 — Color Hi

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Color Hi** is the high bit of the two-bit color mode selector. Together with **Color Lo** (Switch 7), it selects one of four color palettes. See the Toggle Group Notes below for the full mode table.

---

### Switch 9 — Bobs

| Property | Value |
|----------|-------|
| Off | 2 Bobs |
| On | 4 Bobs |
| Default | 2 Bobs |

**Bobs** selects the number of active shadebobs. Set to **2 Bobs**, two bobs trace the Lissajous curve with a 90-degree phase offset between them. Set to **4 Bobs**, four bobs are active, with phase offsets at 0°, 90°, 180°, and 270°. More bobs produce denser, more symmetrical patterns because the curve is traced from multiple starting positions simultaneously.

---

### Switch 10 — Video Seed

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Video Seed** controls whether the incoming video signal is used to seed the framebuffer. When set to **Off**, Aurora generates a purely synthetic image: the canvas starts black and is painted only by the bobs. When set to **On**, the input video contributes to the framebuffer content, allowing external imagery to blend with and influence the luminous trails.

:::tip
With **Video Seed** on, try feeding Aurora a slowly moving camera signal. The video content becomes a ghostly substrate that the bobs paint over, creating a layered composite of real-world imagery and synthetic geometry.
:::

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, bypassing all Aurora synthesis. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use Bypass for instant A/B comparison between the raw input and Aurora's output.

---

:::note Toggle Group Notes

**Color Lo** (Switch 7) and **Color Hi** (Switch 8) form a two-bit binary selector that chooses Aurora's color palette. The four modes are:

| Color Hi | Color Lo | Mode | Description |
|----------|----------|------|-------------|
| Off | Off | **Mono** | White trails tinted by the **Hue** knob. Clean, classic look. |
| Off | On | **Heat** | Cool blue for dim pixels, green for mid-tones, warm red-orange for bright areas, and white at full intensity. Thermal camera aesthetic. |
| On | Off | **Rainbow** | Luminance maps to a 16-color rainbow palette. The **Hue** knob rotates the palette offset. Psychedelic and colorful. |
| On | On | **Duo-tone** | Pixels below half brightness get one color, pixels above get the complementary color. Bold, graphic two-color look. |

:::tip
Try switching color modes while the trails are already built up. The existing framebuffer data is instantly re-colorized: you don't need to wait for new trails to see the difference.
:::

:::

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the delayed input video (dry) and Aurora's synthesized output (wet). At 0%, only the input video is visible. At 100%, only Aurora's synthesis is visible. Intermediate values blend the two, allowing the Lissajous trails to overlay the source material at any opacity.

:::tip
**Mix** is powerful for live performance. Keep it at 50% to see both the camera feed and Aurora's trails simultaneously, creating a layered composite in real time.
:::

---

## Background

### Shadebobs and the Amiga demoscene

The ***shadebob*** effect was born on the Commodore Amiga in the early 1990s, pioneered by demoscene groups like Sanity, Andromeda, and Scoopex. The Amiga's planar graphics hardware could efficiently perform bitwise addition to a framebuffer: an operation that was expensive on other platforms. A small, soft-edged sprite (the "bob") was drawn at successive positions without ever clearing the screen. Each draw ***additively*** increased the brightness of the pixels it touched.

As the bob traced complex curves, it painted elaborate interference patterns that glowed with accumulated light. The visual effect was unlike anything else in the demoscene: ethereal curtains of luminance, spider-web geometries, and pulsing aurora-like ribbons. Aurora recreates this technique in hardware, using Videomancer's FPGA to maintain a persistent framebuffer and paint into it at video rate.

### Lissajous figures

***Lissajous figures*** are the curves produced when two sinusoidal motions are combined at right angles. If the horizontal position follows $x = A \sin(f_x t)$ and the vertical position follows $y = B \sin(f_y t + \phi)$, the resulting path depends on the frequency ratio $f_x : f_y$. A 1:1 ratio produces circles or ellipses; 1:2 produces a figure eight; higher ratios produce increasingly complex rosettes and knots.

Aurora's eight pattern presets correspond to eight frequency-ratio pairs. Each preset produces a distinct curve shape. Because the bobs trace these curves continuously and the framebuffer retains their history, the Lissajous figure gradually reveals itself as a luminous drawing (the mathematical beauty of harmonic motion made visible.)

### Framebuffer persistence

Unlike most Videomancer programs, which process each pixel independently and statelessly, Aurora maintains a ***persistent framebuffer*** stored in the FPGA's block RAM. The framebuffer is a 120×68-pixel canvas (1/16 of the full video resolution) that is never cleared. Each frame, two operations happen in sequence: a global fade pass subtracts a small amount of brightness from every pixel, and then the bob stamps add brightness at the bob positions. This creates a dynamic equilibrium: trails fade at the rate set by **Fade Rate** while new strokes replenish brightness at the rate set by **Speed** and **Intensity**.

The low resolution of the framebuffer is deliberate: it fits within two 4-Kbit BRAM tiles, keeping resource usage modest. The chunky, low-resolution aesthetic also contributes to Aurora's retro character, evoking the look of early home computers and arcade machines.


---

## Signal Flow

### Signal Flow Notes

Aurora's pipeline is divided into two time domains. The **frame-update domain** runs during the vertical blanking interval: the fade pass sweeps through all 8,160 framebuffer pixels, subtracting the fade amount, and then the stamp pass writes the bob kernel at each bob position. This happens once per frame. The **readout domain** runs during active video: pixel counters map each output pixel to a framebuffer address (dividing by 8 in each axis), the BRAM delivers the 8-bit luminance, the colorizer maps it to YUV based on the selected palette, and the interpolator mixes the result with the delayed input.

The two domains share the dual-port BRAM: port A handles the fade and stamp FSM, while port B handles active-video readout. This time-multiplexing is safe because the fade and stamp operations complete during blanking, before readout begins.

:::note
Because the framebuffer resolution is 120×68, each "pixel" on screen is a block of roughly 16×16 output pixels. This gives Aurora its characteristic chunky, retro look.
:::


---

## Exercises

These exercises explore Aurora's orbital painting from simple trails to complex layered compositions. Each exercise builds on the previous one, gradually engaging more controls.
### Exercise 1: Luminous Trails

![Luminous Trails result](/img/instruments/videomancer/aurora/aurora_ex1_s1.png)
*Luminous Trails — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A glowing web of Lissajous trails that slowly builds on a black canvas, demonstrating the interplay between speed, fade, and intensity.

#### Key Concepts

- Additive painting into a persistent framebuffer
- Speed and fade rate create a dynamic equilibrium
- Lissajous patterns produce complex curves from simple ratios

#### Steps

1. Load **Aurora** with default settings. Two bobs trace a simple curve, leaving fading trails.
2. Turn **Fade Rate** (Knob 3) fully counterclockwise. The trails now persist almost indefinitely, and the canvas begins to fill with accumulated light.
3. Slowly increase **Speed** (Knob 1) to about 75%. The bobs move faster, painting more of the curve per second.
4. Turn **Pattern** (Knob 2) clockwise to preset 5 (five-petaled flower). Watch the trail pattern change from a simple loop to an intricate rosette.
5. Adjust **Intensity** (Knob 4) to find the sweet spot where trails are bright but the canvas doesn't saturate to pure white.

#### Settings

| Control | Value |
|---------|-------|
| Speed | ~75% |
| Pattern | 5 |
| Fade Rate | 0% |
| Intensity | ~60% |
| Hue | 0 deg |
| Orbit Size | ~75% |
| Color Lo | Off |
| Color Hi | Off |
| Bobs | 2 Bobs |
| Video Seed | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Color Palettes

![Color Palettes result](/img/instruments/videomancer/aurora/aurora_ex2_s1.png)
*Color Palettes — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Compare all four color modes on a fully developed trail pattern, then use Hue to shift the palette.

#### Key Concepts

- Four color modes re-map luminance to different palettes
- Hue rotation shifts tint in Mono and Rainbow modes
- Existing framebuffer data is re-colorized instantly

#### Steps

1. From Exercise 1, let the canvas build up a rich trail pattern at moderate fade and speed.
2. Set **Color Lo** (Switch 7) to **On**, leaving **Color Hi** (Switch 8) at **Off**. The trails shift to a thermal heat-map palette: cool blue for dim areas, warm orange and red for bright areas.
3. Now set **Color Hi** to **On** and **Color Lo** to **Off**. The trails become a rainbow spectrum, with luminance mapped to hue.
4. While in Rainbow mode, slowly sweep **Hue** (Knob 5) from 0 to 360 degrees. The entire rainbow palette rotates, shifting which colors correspond to which brightness levels.
5. Set both **Color Lo** and **Color Hi** to **On** for Duo-tone mode. The trails snap to a bold two-color graphic: dim areas in one color, bright areas in the complementary color.
6. Return to **Mono** mode (both switches Off). Sweep **Hue** to tint the monochrome trails with warm or cool hues.

#### Settings

| Control | Value |
|---------|-------|
| Speed | ~50% |
| Pattern | 3 |
| Fade Rate | ~25% |
| Intensity | ~75% |
| Hue | 180 deg |
| Orbit Size | ~75% |
| Color Lo | On |
| Color Hi | Off |
| Bobs | 2 Bobs |
| Video Seed | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Four-Bob Symmetry and Video Seed

![Four-Bob Symmetry and Video Seed result](/img/instruments/videomancer/aurora/aurora_ex3_s1.png)
*Four-Bob Symmetry and Video Seed — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A four-bob symmetrical aurora overlaid on a live camera feed, with the input video seeding the framebuffer.

#### Key Concepts

- Four bobs create symmetrical patterns from phase-offset orbits
- Video Seed blends external imagery into the persistent framebuffer
- Mix fader composites synthesis over the camera feed

#### Video Source

A live camera feed or recorded footage with slow, organic motion (clouds, water, or a lava lamp.)

#### Steps

1. Set **Bobs** (Switch 9) to **4 Bobs**. The pattern immediately becomes denser and more symmetrical, with four bobs tracing the same curve at 90-degree offsets.
2. Set **Pattern** (Knob 2) to preset 7 (complex weave, 5:7 ratio). The four bobs now trace an intricate, slowly repeating pattern.
3. Enable **Video Seed** (Switch 10). The camera feed now contributes to the framebuffer content: you'll see ghostly impressions of the input video beneath the Lissajous trails.
4. Lower **Mix** (Fader 12) to about 50%. The output blends Aurora's synthesis with the delayed input video, creating a layered composite.
5. Set the color mode to **Rainbow** (Color Hi On, Color Lo Off) and sweep **Hue** (Knob 5) slowly. The synthetic trails and the seeded video content are both colorized through the same rainbow palette.

#### Settings

| Control | Value |
|---------|-------|
| Speed | ~60% |
| Pattern | 7 |
| Fade Rate | ~25% |
| Intensity | ~60% |
| Hue | 90 deg |
| Orbit Size | ~60% |
| Color Lo | Off |
| Color Hi | On |
| Bobs | 4 Bobs |
| Video Seed | On |
| Bypass | Off |
| Mix | 50% |

---
## Glossary

- **Additive blending**: A compositing method where pixel brightness values are summed, causing overlapping regions to glow brighter. Aurora's bobs use additive blending to paint into the framebuffer.

- **Bob**: A soft-edged graphic stamp: in Aurora, a 3×3 gradient kernel that is painted into the framebuffer at the bob's current position.

- **BRAM**: Block RAM; dedicated memory blocks inside the FPGA used to store the persistent framebuffer.

- **DDS**: Direct Digital Synthesis; a technique for generating waveforms by incrementing a phase accumulator. Aurora uses DDS to produce the sinusoidal bob motions.

- **Fade**: The per-frame subtraction applied to every pixel in the framebuffer, causing old trails to gradually dim toward black.

- **Framebuffer**: A region of memory that stores a complete image. Aurora's framebuffer persists across frames, retaining the accumulated trail history.

- **Lissajous figure**: A curve produced by combining two sinusoidal motions at right angles. The shape depends on the frequency ratio and phase offset.

- **Orbit**: The path traced by a bob across the canvas, defined by Lissajous frequency ratios and amplitude.

- **Shadebob**: A demoscene effect originating on the Amiga, where soft gradient sprites are additively composited into a persistent framebuffer to create luminous trail patterns.

- **Synthesis program**: A Videomancer program that generates imagery from scratch, rather than processing an incoming video signal.

---
