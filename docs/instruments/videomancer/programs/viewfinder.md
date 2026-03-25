---
draft: true
sidebar_position: 324
slug: /instruments/videomancer/viewfinder
title: "Viewfinder"
image: /img/instruments/videomancer/viewfinder/viewfinder_hero_s1.png
description: "Every camcorder from the late 1980s through the early 2000s shipped with a tiny electronic viewfinder — a monochrome CRT barely an inch across, pressed against the operator's eye."
---

![Viewfinder hero image](/img/instruments/videomancer/viewfinder/viewfinder_hero_s1.png)
*Viewfinder overlaying zebra stripes, focus peaking highlights, and a blinking REC indicator on a desaturated camcorder-style image.*

---

## Overview

Viewfinder simulates the electronic viewfinder (EVF) found in 1990s prosumer camcorders: the tiny monochrome CRT that operators peered into while shooting with a Sony CCD, Canon UC, or Panasonic NV-series. That small screen didn't just show the image. It overlaid critical shooting aids: diagonal zebra stripes warning of blown highlights, colored edge outlines showing what was in focus, a safe-area rectangle, a center crosshair, and the blinking red REC dot that confirmed tape was rolling. Viewfinder reproduces all of these aids and applies them to any video signal passing through Videomancer.

Beyond its utility as a real exposure and focus monitor, Viewfinder is a powerful aesthetic tool. The desaturation control drains color from the image until it looks like a genuine black-and-white viewfinder CRT. The brightness knob pushes the image into hot, bloomed whites. Focus peaking paints vivid color outlines onto edges, turning any footage into a neon-traced sketch. Stack the overlays together and Viewfinder becomes a living, blinking broadcast-control-room display (part technical instrument, part visual art.)

:::tip
Viewfinder actually works as a real exposure and focus tool. Feed it a camera signal and use **Zebra** and **Peaking** the same way a professional camera operator would: to check exposure levels and confirm focus before recording.
:::

### What's In a Name?

A ***viewfinder*** is the optical or electronic device on a camera that the operator looks through to frame and focus a shot. In film cameras, viewfinders were optical prisms. In video cameras from the 1980s and 1990s, the viewfinder was a tiny ***electronic viewfinder*** (EVF): a miniature monochrome CRT built into the camera body. These EVFs displayed not just the image, but a suite of overlay indicators: zebra stripes, safe-area guides, and the iconic blinking REC dot. The name Viewfinder pays tribute to that small screen and the entire visual language it created.

---

## Quick Start

1. Feed a video source into Videomancer with Viewfinder loaded. Turn **Desat** (Knob 6) fully clockwise to drain all color, producing a monochrome viewfinder look. The image should resemble a black-and-white CRT.
2. Confirm that **Zebra** (Switch 7) is set to **On**. Diagonal stripes should appear on the brightest parts of the image. Adjust **Zebra Level** (Knob 1) to control how much of the image triggers the stripes.
3. Confirm that **Peaking** (Switch 8) is set to **On**. Colored outlines appear along sharp edges. Adjust **Peaking** (Knob 2) to control sensitivity: turn it counterclockwise for thicker, more visible outlines.
4. Turn on **Safe Area** (Switch 9), **Center Mark** (Switch 10), and **REC** (Switch 11). A white rectangle, crosshair, and blinking red dot now overlay the image. You are looking through a fully dressed 1990s camcorder viewfinder.

---

## Parameters

![Videomancer front panel with Viewfinder loaded](/img/instruments/videomancer/viewfinder/viewfinder_control_panel.png)
*Videomancer's front panel with Viewfinder active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Zebra Level

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |

**Zebra Level** sets the luminance threshold above which zebra stripes appear. At 0%, fully counterclockwise, the threshold is at its lowest: almost the entire image is covered in diagonal hatching. As you rotate clockwise, the threshold rises and fewer pixels qualify as "overexposed." At 100%, only the very brightest highlights trigger zebra. This control has no effect when **Zebra** (Switch 7) is set to **Off**.

:::note
In professional video production, zebra stripes at the 70% IRE level indicate properly exposed skin tones, while stripes at 100% IRE warn of clipped highlights. Viewfinder lets you set the threshold anywhere in between.
:::

---

### Knob 2 — Peaking

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 37.5% |

**Peaking** controls the sensitivity of the focus peaking edge detector. At 0%, fully counterclockwise, the edge detection threshold is at its lowest: even the faintest texture triggers a colored highlight. As you turn clockwise, the threshold rises and only the sharpest, highest-contrast edges display peaking color. At 100%, only the most extreme edges are highlighted. This control has no effect when **Peaking** (Switch 8) is set to **Off**.

The edge detector computes a horizontal gradient across a three-pixel window. When the absolute difference between the current pixel and the pixel two positions earlier exceeds the threshold, the pixel is replaced with the selected peak color.

---

### Knob 3 — Peak Color

| Property | Value |
|----------|-------|
| Range | 0 – 1023 |
| Default | 0 |

**Peak Color** selects the color used for focus peaking highlights. The four choices are **Red**, **Green**, **Blue**, and **Yellow**. Red is the default and the most common choice in professional cameras because it stands out against most natural scenes. Green is useful against red or warm-toned footage. Blue works well against skin tones and earth tones. Yellow provides a high-visibility option for dark or blue-heavy scenes.

:::tip
Choose a peaking color that contrasts with your source material. If you're shooting a sunset, switch from Red to **Blue** or **Green** so the peaking outlines don't get lost in the warm tones.
:::

---

### Knob 4 — Brightness

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Brightness** adjusts the overall luminance of the processed image. At 0%, the image is at its darkest. As the knob turns clockwise, brightness increases, scaling luminance values upward. The brightness is applied as a multiplier: it can push bright areas into clipping, producing a bloomed, hot look reminiscent of a viewfinder CRT running at high voltage. At 50%, the image is near its original brightness. Above 50%, the image becomes progressively brighter and can clip to pure white.

---

### Knob 5 — Guide Opac

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Guide Opac** sets the brightness of the overlay guide lines: the safe-area rectangle and center crosshair. At 0%, the guides are invisible (black). At 100%, the guides are at maximum brightness (white). This does not affect the REC indicator, which has its own fixed color.

---

### Knob 6 — Desat

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 75.1% |

**Desat** controls the desaturation of the image. At 0%, fully counterclockwise, the image retains its original color. As you turn clockwise, the color drains away: chroma is blended toward neutral gray. At 100%, the image is fully desaturated, producing pure black-and-white output that mimics the monochrome CRT of a camcorder viewfinder.

The desaturation algorithm blends each chroma channel (U and V) toward the midpoint value of 512. At full desaturation, U and V are both locked at 512, which is neutral gray in YUV color space.

---

### Switch 7 — Zebra

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Zebra** enables or disables the zebra stripe overlay. When set to **On**, diagonal hatching appears on all pixels whose luminance exceeds the **Zebra Level** threshold. The zebra pattern is a 45-degree diagonal stripe generated by XOR-ing the two lowest bits of the horizontal and vertical position counters. In the zebra region, luminance is inverted by ±256 to guarantee visibility against both bright and dark backgrounds. When set to **Off**, no zebra stripes are drawn regardless of the Zebra Level setting.

---

### Switch 8 — Peaking

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Peaking** enables or disables the focus peaking overlay. When set to **On**, pixels where the horizontal edge magnitude exceeds the **Peaking** threshold are replaced with the color selected by **Peak Color**. This produces vivid colored outlines along sharp edges in the image. When set to **Off**, no peaking highlights are drawn.

---

### Switch 9 — Safe Area

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Safe Area** enables or disables the safe-area rectangle overlay. When set to **On**, a thin white rectangle (two pixels wide) is drawn showing the 90% safe area of the frame. This is the broadcast-standard ***action-safe area***: the region of the frame guaranteed to be visible on all displays. Content outside this rectangle may be cropped by consumer televisions. The rectangle is drawn at a brightness determined by **Guide Opac** (Knob 5). When set to **Off**, no rectangle is drawn.

---

### Switch 10 — Center Mark

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Center Mark** enables or disables the center crosshair overlay. When set to **On**, a white crosshair is drawn at the exact center of the frame. The crosshair has 40-pixel arms and is two pixels wide. It uses resolution-adaptive centering, so it remains accurate across different video standards. The crosshair brightness is determined by **Guide Opac** (Knob 5). When set to **Off**, no crosshair is drawn.

---

### Switch 11 — REC

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**REC** enables or disables the blinking REC indicator. When set to **On**, a small red dot (12×12 pixels) appears in the upper-left corner of the frame. The dot blinks at approximately 1.5 Hz: it is visible for about 0.5 seconds, then hidden for about 0.5 seconds, repeating continuously. The REC indicator uses the same red color as the Red peaking option (Y=300, U=350, V=900). When set to **Off**, no recording indicator is displayed.

:::note
The REC dot blinks based on a frame counter. Bit 4 of a 6-bit counter toggles the dot's visibility, producing a blink rate of approximately every 16 frames: roughly once per second at 30 fps, with equal on and off periods.
:::

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry (unprocessed) input and the wet (fully processed) output. At 0%, the output is the original input signal with no Viewfinder processing visible. At 100%, the output is the fully processed result with all active overlays. Intermediate values blend between the two, allowing you to dial in a subtle overlay effect or fade the viewfinder look in and out during a performance.

---

## Background

### Electronic viewfinders

The ***electronic viewfinder*** (EVF) became standard equipment on consumer and prosumer camcorders throughout the 1980s and 1990s. Unlike an optical viewfinder that shows the scene directly through a lens, an EVF displays the camera sensor's output on a miniature screen: originally a tiny monochrome cathode ray tube, typically less than one inch across. Because they were black-and-white, EVFs relied on overlay graphics to communicate critical information: zebra patterns for exposure, edge enhancement for focus confirmation, frame guides for composition, and status indicators like the recording state.

Professional broadcast cameras from Sony, Ikegami, and Panasonic featured sophisticated EVFs with adjustable zebra levels, peaking intensity, and multiple overlay modes. These overlays were generated by dedicated hardware circuits within the camera's viewfinder module. Consumer camcorders offered simpler versions of the same features: a single zebra level, basic peaking, and the iconic blinking REC dot.

### Zebra stripes

***Zebra stripes*** are the primary exposure aid in video production. They overlay a diagonal hatching pattern on any region of the image that exceeds a configurable luminance threshold. The name comes from the resemblance to the stripes on a zebra's hide. Camera operators use zebra at two standard levels: 70 IRE (to monitor skin tone exposure) and 100 IRE (to detect clipped highlights). The pattern must be visually distinct from the underlying image, so it uses a high-contrast design: typically alternating bright and dark diagonal lines. Viewfinder implements this by inverting luminance by ±256 in the striped pixels, ensuring the pattern is visible whether overlaid on bright highlights or mid-tones.

### Focus peaking

***Focus peaking*** highlights in-focus edges by overlaying them with a bright color. The technique originated in Sony's professional camera viewfinders in the late 1980s. The camera's viewfinder circuit detected horizontal edges using a simple high-pass filter and replaced those pixels with a user-selectable color: typically red, green, or white. This gave the operator an immediate visual confirmation of the plane of focus without needing to judge sharpness on a tiny, low-resolution CRT. Viewfinder's edge detector uses a three-pixel horizontal gradient: the absolute difference between the current pixel's luminance and the luminance of the pixel two positions earlier. This simple approach produces clean, responsive edge outlines without requiring line-buffer memory.

### Broadcast safe areas

Television cathode-ray tubes used ***overscan***: the edges of the transmitted image were larger than the visible screen area, and some of the picture was hidden behind the bezel. To ensure critical content remained visible, broadcasters established ***safe areas***: a 90% action-safe zone where all important visual action should occur, and an 80% title-safe zone where all text and graphics should be placed. Although modern flat-panel displays show the full raster, safe-area guides remain standard practice in professional production. Viewfinder draws the 90% action-safe rectangle as a reference guide.


---

## Signal Flow

### Signal Flow Notes

The processing pipeline runs in a single clocked process with several key interactions:

1. **Desaturation before overlays.** Chroma is blended toward neutral *before* any overlay is applied. This means the zebra stripes and focus peaking highlights appear on a desaturated image, just as they would on a real monochrome viewfinder CRT. The overlays are drawn on top of the already-desaturated picture.

2. **Zebra before peaking.** Zebra stripes are applied first. If a pixel is both over-exposed (triggering zebra) and on a sharp edge (triggering peaking), the peaking color wins: it overwrites whatever the zebra stage produced. In practice this is uncommon because zebra regions tend to be large, clipped areas with few internal edges.

3. **Guides override everything.** The safe-area rectangle, center crosshair, and REC indicator are the last processing stage before the mix. A pixel on a guide line shows the guide color regardless of what the underlying image looks like. The guide lines are achromatic white (U=V=512) at a brightness set by Guide Opac, while the REC dot is a fixed red.

:::tip
Because desaturation happens early in the chain, you can use Viewfinder as a monochrome monitor with colored overlays: the image is black-and-white but the peaking highlights and REC dot remain in vivid color. This is exactly how a real camcorder EVF worked.
:::


---

## Exercises

These exercises progress from basic exposure monitoring to building a fully dressed camcorder viewfinder simulation suitable for live performance.
### Exercise 1: Exposure Monitor

![Exposure Monitor result](/img/instruments/videomancer/viewfinder/viewfinder_ex1_s1.png)
*Exposure Monitor — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A functional exposure monitoring display that highlights blown highlights with zebra stripes, just like a real camera operator's viewfinder.

#### Key Concepts

- Zebra stripes mark overexposed regions
- The threshold controls what counts as "overexposed"
- Desaturation simulates a monochrome viewfinder

#### Video Source

A live camera feed or recorded footage with a mix of bright highlights and mid-tone detail: a window in a room, a lamp against a wall, or sunlit objects with shadows.

#### Steps

1. Turn **Desat** (Knob 6) to about 75% to partially desaturate the image, giving it a viewfinder feel.
2. Confirm **Zebra** (Switch 7) is **On**. Lower **Zebra Level** (Knob 1) until diagonal stripes appear on the brightest areas.
3. Slowly raise **Zebra Level** to narrow the stripes to only the most overexposed highlights. Find the sweet spot where the stripes mark only the regions you consider too bright.
4. Adjust **Brightness** (Knob 4) and observe how raising brightness pushes more of the image above the zebra threshold, causing stripes to spread.

#### Settings

| Control | Value |
|---------|-------|
| Zebra Level | ~50% |
| Peaking | 37.5% |
| Peak Color | Red |
| Brightness | 50% |
| Guide Opac | 50% |
| Desat | ~75% |
| Zebra | On |
| Peaking | Off |
| Safe Area | Off |
| Center Mark | Off |
| REC | Off |
| Mix | 100% |

---

### Exercise 2: Focus Peaking Sketch

![Focus Peaking Sketch result](/img/instruments/videomancer/viewfinder/viewfinder_ex2_s1.png)
*Focus Peaking Sketch — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A neon-outlined sketch effect where sharp edges in the image glow in vivid color against a nearly monochrome background.

#### Key Concepts

- Focus peaking highlights in-focus edges with color
- Sensitivity determines how faint an edge must be to trigger peaking
- Different peak colors suit different scenes

#### Video Source

Footage with strong texture and detail: tree bark, fabric, architectural lines, or a face in good lighting. Avoid flat, featureless content.

#### Steps

1. Set **Desat** (Knob 6) to 100% for a fully monochrome background.
2. Turn on **Peaking** (Switch 8). Colored outlines should appear along edges. If not, lower **Peaking** (Knob 2) to increase sensitivity.
3. Sweep **Peaking** (Knob 2) from 0% to 100%. At low values, the image is flooded with color on even the smallest texture. At high values, only the boldest edges light up.
4. Rotate **Peak Color** (Knob 3) through all four settings: **Red**, **Green**, **Blue**, **Yellow**: and choose the color that contrasts best with your source.
5. Turn off **Zebra** (Switch 7) to isolate the peaking effect and appreciate the clean neon-outline look.

#### Settings

| Control | Value |
|---------|-------|
| Zebra Level | 75% |
| Peaking | ~25% |
| Peak Color | Green |
| Brightness | 50% |
| Guide Opac | 50% |
| Desat | 100% |
| Zebra | Off |
| Peaking | On |
| Safe Area | Off |
| Center Mark | Off |
| REC | Off |
| Mix | 100% |

---

### Exercise 3: Full EVF Simulation

![Full EVF Simulation result](/img/instruments/videomancer/viewfinder/viewfinder_ex3_s1.png)
*Full EVF Simulation — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A fully dressed 1990s camcorder viewfinder display with every overlay active: zebra, peaking, safe area, center crosshair, and the blinking REC dot.

#### Key Concepts

- Layered overlays combine into a complete viewfinder display
- Guide opacity balances visibility against distraction
- Mix allows gradual blending of the viewfinder aesthetic

#### Video Source

A live camera feed, handheld for authenticity. Moving subjects add to the camcorder feel.

#### Steps

1. Start from the **Full EVF Sim** preset or dial in similar settings: **Desat** (Knob 6) at 100%, **Brightness** (Knob 4) slightly elevated to about 60%.
2. Turn on all five overlay switches: **Zebra** (Switch 7), **Peaking** (Switch 8), **Safe Area** (Switch 9), **Center Mark** (Switch 10), and **REC** (Switch 11).
3. Set **Zebra Level** (Knob 1) to about 85% so only the hottest highlights trigger stripes.
4. Set **Peaking** (Knob 2) to about 40% for moderate edge detection. Choose **Red** for **Peak Color** (Knob 3).
5. Dial **Guide Opac** (Knob 5) to about 40% so the safe-area rectangle and crosshair are visible but not overwhelming.
6. Lower **Mix** (Fader 12) to about 80% to let a hint of the original color bleed through the monochrome viewfinder image.
7. Watch the blinking REC dot in the upper-left corner. You are now looking through a fully operational 1990s camcorder viewfinder.

#### Settings

| Control | Value |
|---------|-------|
| Zebra Level | ~85% |
| Peaking | ~40% |
| Peak Color | Red |
| Brightness | ~60% |
| Guide Opac | ~40% |
| Desat | 100% |
| Zebra | On |
| Peaking | On |
| Safe Area | On |
| Center Mark | On |
| REC | On |
| Mix | ~80% |

---
## Glossary

- **Desaturation**: The process of reducing the color intensity in an image, blending chroma values toward neutral gray. Full desaturation produces a monochrome (black-and-white) image.

- **Edge Detection**: A signal processing technique that identifies boundaries between regions of different brightness. Viewfinder uses a horizontal gradient method comparing pixels separated by two positions.

- **Electronic Viewfinder (EVF)**: A miniature display built into a video camera that shows the sensor's output to the operator. In 1990s camcorders, this was typically a tiny monochrome CRT less than one inch across.

- **Focus Peaking**: A camera aid that highlights in-focus edges by overlaying them with a bright color, allowing the operator to confirm the focal plane without judging sharpness on a small screen.

- **IRE**: A unit of measurement for video signal amplitude, named after the Institute of Radio Engineers. 0 IRE is black, 100 IRE is peak white.

- **Overscan**: The practice in CRT televisions of displaying an image larger than the visible screen area, hiding the edges behind the bezel. Safe-area guides compensate for this.

- **Safe Area**: The region of a video frame guaranteed to be visible on all displays. The 90% action-safe area ensures critical visual content is not cropped by overscan.

- **YUV**: A color model that separates brightness (Y) from color information (U and V). Viewfinder processes each component independently: desaturation affects only U and V, while brightness adjustment affects only Y.

- **Zebra Stripes**: A diagonal hatching pattern overlaid on regions of a video image that exceed a configurable luminance threshold, used by camera operators to monitor exposure levels.

---
