---
draft: true
sidebar_position: 155
slug: /instruments/videomancer/kaleid
title: "Kaleid"
image: /img/instruments/videomancer/kaleid/kaleid_hero.png
description: "In 1992, a shareware program called DAZZLE50 mesmerized DOS users with kaleidoscopic color patterns that required nothing more than a VGA card and a 386."
---

![Kaleid hero image](/img/instruments/videomancer/kaleid/kaleid_hero_s1.png)
*Kaleid generating smoothly cycling rainbow diamonds with octagonal symmetry folding and triangle-wave color bands.*

---

## Overview

**Kaleid** is a kaleidoscopic pattern generator inspired by classic VGA-era screen savers and color image generators like DAZZLE50 (1992). It creates evolving geometric patterns by applying coordinate-based algorithms to the pixel grid itself, then painting the results with smoothly cycling rainbow or monochrome color bands. No input video is required: Kaleid synthesizes imagery from scratch.

Four pattern algorithms are available: an XOR fractal, concentric diamonds, concentric square rings, and a moiré interference pattern. Each algorithm maps the screen's pixel coordinates through a symmetry fold: either four-fold or eight-fold: before computing a pattern value. That value feeds into a ***triangle-wave*** color engine that produces smoothly animated hues cycling across the screen. The result is a continuously evolving, mathematically precise light show.

With the **Overlay** switch engaged, Kaleid can also multiply its luminance pattern onto an incoming video signal, turning the synthesizer into a processing effect that imprints geometric texture onto live footage.

:::tip
Kaleid uses ***zero block RAM***: its entire pipeline is combinational logic and registers. This makes it one of the lightest programs in the library.
:::

### What's In a Name?

The name ***Kaleid*** is a truncation of ***kaleidoscope***, from the Greek *kalos* (beautiful), *eidos* (form), and *skopein* (to look at). A kaleidoscope creates beautiful forms by reflecting a scene through angled mirrors. Kaleid does the same thing mathematically: it folds the screen's coordinate space around its center point, then reflects and repeats the pattern across two or four axes of symmetry.

---

## Quick Start

1. You should see an animated rainbow pattern filling the screen by default. Turn **Pattern** (Knob 1) slowly through its four steps and watch the shape of the geometry change: from fractal webs to diamonds to square rings to shimmering moiré interference.
2. Sweep **Zoom** (Knob 2) from left to right. At the left extreme, you see broad, sweeping shapes. As you turn clockwise, the features become finer and more numerous, like looking deeper into a crystal.
3. Adjust **Speed** (Knob 3) to control the color cycling animation. At the far left the pattern is frozen; turning clockwise makes the colors flow faster.
4. Toggle **Fold** (Switch 8) from **Quad** to **Octagonal**. The pattern gains four additional axes of symmetry, doubling its mirror complexity and creating star-like shapes.

---

## Parameters

![Videomancer front panel with Kaleid loaded](/img/instruments/videomancer/kaleid/kaleid_control_panel.png)
*Videomancer's front panel with Kaleid active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Pattern

| Property | Value |
|----------|-------|
| Range | 1 – 4 |
| Default | 2 |

**Pattern** selects between four geometric algorithms. Each mode computes a different mathematical function of the folded screen coordinates:

In the first position, the XOR mode produces ***Sierpinski-like*** fractal structures: nested triangular and rectangular self-similar patterns that emerge from the bitwise exclusive-or of the horizontal and vertical coordinates. In the second position, Diamond mode sums the coordinates to create concentric diamond shapes radiating from the center (this is the ***Manhattan distance***, the distance you'd walk along a city grid). The third position, Rings, takes the maximum of the two coordinates to produce concentric square rings (the ***Chebyshev distance***). The fourth position, Moiré, combines the sum and XOR operations to create dense interference fringes that shimmer and beat against each other.

:::note
Because Pattern uses a stepped control mode, you'll feel four distinct detents as you turn the knob. Each detent selects one algorithm cleanly.
:::

---

### Knob 2 — Zoom

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |

**Zoom** controls the spatial scale of the pattern by multiplying the folded coordinates. At the lowest settings, features are large: broad bands and thick shapes that fill the screen. As Zoom increases, the coordinate space is multiplied by larger factors (×1, ×2, ×4), producing finer detail: thinner bands, tighter rings, and denser fractal structures.

The zoom operates in discrete steps selected by the top two bits of the control value: this means you'll notice the scale shift in jumps rather than as a smooth sweep. Between each step, the lower bits have no effect, so the knob has four "zones" of roughly equal width.

---

### Knob 3 — Speed

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 13% |

**Speed** controls how fast the color animation cycles. Kaleid uses a ***direct digital synthesis*** (DDS) phase accumulator that advances once per video frame. The Speed knob sets how much the phase advances each frame: at zero, the pattern is frozen in place; at maximum, colors race across the geometry at full speed.

Because the accumulator is 16 bits wide and only the top 12 bits feed the color engine, the animation wraps smoothly: there's no visible glitch or jump when the phase counter rolls over.

---

### Knob 4 — Hue

| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |

**Hue** offsets the base color of the entire pattern. Think of it as rotating the color wheel: at zero, the pattern starts at its natural hue; sweeping Hue clockwise shifts all colors uniformly around the spectrum. Because the offset is added directly into the 12-bit phase register, it shifts the starting point of the triangle-wave color engine without affecting the animation speed or the pattern geometry.

:::tip
Try setting Speed to zero and sweeping Hue manually. You'll step through the color spectrum by hand, choosing exactly the palette you want for a still pattern.
:::

---

### Knob 5 — Saturation

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |

**Saturation** controls the intensity of the chroma (color) channels. At zero, the U and V channels are scaled to nothing and the pattern becomes monochrome gray. As Saturation increases, the triangle-wave outputs for U and V are multiplied by progressively larger values, producing richer, more vivid colors. At maximum, the full range of the triangle wave is used, yielding bold, saturated rainbow bands.

Saturation only takes effect in **Rainbow** mode (Switch 7). In Mono mode, the U and V channels are forced to neutral regardless of this knob's position.

---

### Knob 6 — Brightness

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |

**Brightness** controls the amplitude of the luminance channel. It works by scaling the Y triangle-wave output: at zero, the luminance is flat at the midpoint (gray), and as Brightness increases, the peaks and valleys of the wave stretch further apart, producing greater contrast between the light and dark bands of the pattern. At maximum, the full dynamic range of the display is used.

---

### Switch 7 — Color

| Property | Value |
|----------|-------|
| Off | Mono |
| On | Rainbow |
| Default | Rainbow |

**Color** selects between two color modes. In **Mono** mode, the U and V channels are held at neutral (512), producing a grayscale pattern whose brightness follows the triangle wave. In **Rainbow** mode, three triangle waves offset by 120° each drive the Y, U, and V channels independently, creating a smooth, continuously cycling spectrum of colors. Rainbow is the default.

---

### Switch 8 — Fold

| Property | Value |
|----------|-------|
| Off | Quad |
| On | Octagonal |
| Default | Quad |

**Fold** selects between two symmetry modes. **Quad** applies four-fold mirror symmetry by reflecting the screen around both the horizontal and vertical center lines: every quadrant of the screen is identical. **Octagonal** adds a diagonal fold on top of the four-fold mirror, swapping the horizontal and vertical coordinates when x > y. This creates eight-fold symmetry, producing star-shaped and pinwheel patterns.

:::tip
Octagonal fold dramatically changes the XOR pattern. The Sierpinski fractal becomes a star-shaped web of nested triangles (a shape you can't achieve with Quad alone.)
:::

---

### Switch 9 — Overlay

| Property | Value |
|----------|-------|
| Off | Replace |
| On | Overlay |
| Default | Replace |

**Overlay** switches between two composition modes. In **Replace** mode (the default), Kaleid's generated pattern completely replaces the input video: the output is pure synthesis. In **Overlay** mode, the pattern's luminance is multiplied with the input video's luminance, and the input's original chroma is preserved. This imprints the geometric pattern onto the incoming image as a luminance texture, creating an effect similar to projecting a kaleidoscope onto live footage.

:::note
In Overlay mode, the Saturation knob has no effect: chroma comes entirely from the input signal. Brightness still controls the pattern's luminance scaling before the multiplication.
:::

---

### Switch 10 — Invert

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Invert** flips the luminance of the generated pattern. The Y channel is complemented (1023 − Y) after brightness scaling but before the overlay multiplication. This reverses which parts of the pattern are bright and which are dark, turning positive shapes into negative ones. In Overlay mode, inversion flips which areas of the input video are brightened versus darkened.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, skipping all pattern generation and mixing. The sync delay pipeline still aligns timing, so there is no glitch when switching. Use Bypass for instant A/B comparison between the raw input and the synthesized pattern.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |

**Mix** crossfades between the delayed input signal (dry) and the generated pattern (wet) using three interpolator instances. At 0%, only the original input is visible; at 100%, only the Kaleid pattern is visible. Intermediate values blend the two together. This provides a smooth way to introduce or fade out the effect without switching Bypass.

---

## Background

### Coordinate-based pattern generation

Classic VGA-era screen savers and demo scene productions often generated mesmerizing visuals using nothing more than the pixel's own screen coordinates as input to simple mathematical functions. Programs like DAZZLE50 (1992) computed bitwise operations on x and y positions, then mapped the results to color palettes. The technique requires no frame buffer, no stored images, and no complex rendering: just a function evaluated at every pixel, every frame. Kaleid follows this tradition directly, implementing four such functions in pure FPGA logic.

### Symmetry folding

A physical kaleidoscope creates complex patterns from simple elements by placing mirrors at angles. Kaleid does this mathematically by "folding" the coordinate space: replacing each coordinate with its absolute distance from the screen center. This ***four-fold*** symmetry means that a pattern computed for positive (x, y) is mirrored identically into all four quadrants. Adding the ***diagonal fold*** (swapping x and y when x > y) doubles the symmetry to eight-fold, as if placing mirrors at 45° angles inside the kaleidoscope tube.

### Triangle-wave color cycling

To paint the patterns with color, Kaleid evaluates a ***triangle wave*** function: a periodic signal that ramps linearly up, then linearly back down, repeating forever. Three instances of this function run simultaneously, offset by 120° from each other, driving the Y, U, and V channels of the video output. As the animation phase advances frame by frame, all three waves shift in lockstep, creating the characteristic smooth rainbow cycling where colors flow continuously through the spectrum. The triangle wave is a zero-resource approximation of a cosine: it uses no BRAMs, no multipliers, and no lookup tables: just a quadrant selector and a bit fold.


---

## Signal Flow

### Signal Flow Notes

The pipeline is purely feedforward with no feedback or frame storage. Two important interactions define Kaleid's behavior:

1. **Phase composition**: The 12-bit color phase is the sum of three components: the spatial pattern value (from the coordinate algorithm), the animation phase (advancing per frame), and the hue offset (from the Hue knob). Changing any one of these shifts the color mapping across the entire screen simultaneously. The pattern provides the spatial variation, the animation provides temporal motion, and the hue knob provides manual offset.

2. **Overlay modulation**: When Overlay is active, the Y channel undergoes an additional multiplication stage. The pattern's brightness is multiplied with the input video's luminance: `output_Y = input_Y × pattern_Y / 1024`. This is a ***modulation*** operation, not a blend: areas where the pattern is dark will darken the input, and areas where the pattern is bright will preserve the input. The input's chroma (U, V) passes through unchanged, so the original colors of the video are retained with the pattern imprinted as a luminance texture.

:::tip
**Overlay plus Invert**: toggling Invert with Overlay active flips which regions of the input are darkened. This is a quick way to swap between "pattern as shadow" and "pattern as spotlight."
:::


---

## Exercises

These exercises walk through Kaleid's pattern generation from simple geometry to complex animated compositions. Each exercise is self-contained (no input video is needed.)
### Exercise 1: Fractal Kaleidoscope

![Fractal Kaleidoscope result](/img/instruments/videomancer/kaleid/kaleid_ex1_s1.png)
*Fractal Kaleidoscope — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A frozen, eight-fold Sierpinski-style fractal web in monochrome, exploring how the XOR algorithm and diagonal fold interact.

#### Key Concepts

- XOR creates self-similar fractal structures
- Symmetry folding multiplies the complexity
- Zoom controls the level of fractal detail

#### Steps

1. Set **Pattern** (Knob 1) to the first detent (XOR mode). You should see a complex web of nested rectangles and triangles.
2. Set **Speed** (Knob 3) to 0% to freeze the animation. The pattern is now static.
3. Switch **Color** (Switch 7) to **Mono**. The pattern becomes a grayscale fractal.
4. Toggle **Fold** (Switch 8) to **Octagonal**. The rectangular web transforms into an eight-pointed star structure.
5. Sweep **Zoom** (Knob 2) from left to right. At low zoom, you see the broad outer shape; at high zoom, the self-similar fractal detail becomes visible, with patterns repeating at finer and finer scales.
6. Increase **Brightness** (Knob 6) to stretch the contrast between light and dark bands.

#### Settings

| Control | Value |
|---------|-------|
| Pattern | 1 (XOR) |
| Zoom | 50% |
| Speed | 0% |
| Hue | 0° |
| Saturation | 75% |
| Brightness | 75% |
| Color | Mono |
| Fold | Octagonal |
| Overlay | Replace |
| Invert | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Rainbow Diamond Animation

![Rainbow Diamond Animation result](/img/instruments/videomancer/kaleid/kaleid_ex2_s1.png)
*Rainbow Diamond Animation — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A pulsating diamond pattern painted in full-spectrum rainbow colors, cycling smoothly through the color wheel.

#### Key Concepts

- Diamond mode creates concentric Manhattan-distance shapes
- Triangle-wave color cycling produces smooth rainbow bands
- Hue and Speed control the color engine independently

#### Steps

1. Set **Pattern** (Knob 1) to the second detent (Diamond mode). Concentric diamond shapes radiate from the center.
2. Switch **Color** (Switch 7) to **Rainbow** and increase **Saturation** (Knob 5) to about 75%. The diamonds fill with vivid color bands.
3. Set **Speed** (Knob 3) to about 30%. The colors begin flowing outward through the diamond shapes.
4. Sweep **Hue** (Knob 4) slowly. The entire color palette rotates: reds become greens, blues become oranges: without changing the pattern geometry or animation speed.
5. Increase **Zoom** (Knob 2) to pack more diamond rings onto the screen. The color bands become thinner and more numerous.
6. Toggle **Fold** between Quad and Octagonal. In Quad mode, the diamonds have four-fold symmetry; in Octagonal mode, additional diagonal folds create a more complex star pattern.

#### Settings

| Control | Value |
|---------|-------|
| Pattern | 2 (Diamond) |
| Zoom | 70% |
| Speed | 30% |
| Hue | 0° |
| Saturation | 75% |
| Brightness | 75% |
| Color | Rainbow |
| Fold | Quad |
| Overlay | Replace |
| Invert | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Moiré Video Texture

![Moiré Video Texture result](/img/instruments/videomancer/kaleid/kaleid_ex3_s1.png)
*Moiré Video Texture — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A shimmering moiré interference texture overlaid on live video, creating a projection-like kaleidoscopic effect on the incoming footage.

#### Key Concepts

- Moiré mode creates dense interference fringes
- Overlay multiplies the pattern onto an input video signal
- Mix crossfades between dry and wet for subtle textures

#### Steps

1. Connect a video source to Videomancer's input. Set **Pattern** (Knob 1) to the fourth detent (Moiré mode).
2. Switch **Overlay** (Switch 9) to **Overlay**. The pattern is now multiplied onto the input video's luminance.
3. Set **Zoom** (Knob 2) to about 50%. The moiré fringes are medium-density.
4. Set **Speed** (Knob 3) to about 20%. The interference pattern slowly shifts and pulses.
5. Adjust **Brightness** (Knob 6) to control how strongly the pattern modulates the image. Higher brightness lets more of the input through; lower brightness deepens the dark areas of the pattern.
6. Toggle **Invert** (Switch 10). The bright and dark regions of the pattern swap (areas that were transparent become opaque and vice versa.)
7. Pull **Mix** (Fader 12) to about 60% to blend the textured result with the clean input for a subtler effect.

#### Settings

| Control | Value |
|---------|-------|
| Pattern | 4 (Moiré) |
| Zoom | 50% |
| Speed | 20% |
| Hue | 0° |
| Saturation | 50% |
| Brightness | 60% |
| Color | Rainbow |
| Fold | Quad |
| Overlay | Overlay |
| Invert | Off |
| Bypass | Off |
| Mix | 60% |

---
## Glossary

- **Chebyshev Distance**: The maximum of the absolute differences along each axis; produces concentric square contours.

- **DDS (Direct Digital Synthesis)**: A technique for generating periodic waveforms by incrementing a phase accumulator at a fixed rate; used here for the color cycling animation.

- **Manhattan Distance**: The sum of the absolute differences along each axis; produces concentric diamond contours. Named after the grid layout of city blocks.

- **Moiré Pattern**: An interference pattern created when two repetitive structures overlap at slightly different scales or angles, producing visible beat frequencies.

- **Sierpinski Triangle**: A fractal pattern created by recursively subdividing a triangle; the XOR of two coordinates produces a discrete approximation of this structure.

- **Symmetry Fold**: A mathematical operation that mirrors coordinates around an axis, causing the same pattern to appear identically in multiple regions of the screen.

- **Triangle Wave**: A periodic waveform that ramps linearly up and down, used here as a zero-resource approximation of a cosine for color generation.

- **XOR (Exclusive Or)**: A bitwise operation that outputs 1 when its inputs differ. Applied to pixel coordinates, it produces self-similar fractal patterns.

---
