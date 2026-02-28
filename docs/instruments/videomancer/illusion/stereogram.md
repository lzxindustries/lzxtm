---
draft: true
sidebar_position: 245
slug: /instruments/videomancer/stereogram
title: "Stereogram"
image: /img/instruments/videomancer/stereogram/stereogram_hero.png
description: "Stereogram generates a Single Image Random Dot Stereogram (SIRDS) from the input video's luminance channel."
---

import stereogram_before_after from '/img/instruments/videomancer/stereogram/stereogram_before_after.png';
import stereogram_control_panel from '/img/instruments/videomancer/stereogram/stereogram_control_panel.png';
import stereogram_exercise1_result from '/img/instruments/videomancer/stereogram/stereogram_exercise1_result.png';
import stereogram_exercise2_result from '/img/instruments/videomancer/stereogram/stereogram_exercise2_result.png';
import stereogram_exercise3_result from '/img/instruments/videomancer/stereogram/stereogram_exercise3_result.png';
import stereogram_hero from '/img/instruments/videomancer/stereogram/stereogram_hero.png';
import stereogram_source1_kodim01 from '/img/instruments/videomancer/stereogram/stereogram_source1_kodim01.png';
import stereogram_source2_kodim02 from '/img/instruments/videomancer/stereogram/stereogram_source2_kodim02.png';
import stereogram_source3_kodim01_bw from '/img/instruments/videomancer/stereogram/stereogram_source3_kodim01_bw.png';

# Stereogram

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={stereogram_hero} alt="Stereogram hero image"/>
*Hidden depths emerge from random-dot fields as the classic autostereogram algorithm transforms video luminance into cross-eyed 3D illusions.*
<img src={stereogram_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Stereogram applied.*

---

## Overview

Stereogram generates a Single Image Random Dot Stereogram (SIRDS) from the input video's luminance channel. The input brightness is interpreted as a depth map — brighter pixels appear closer, darker pixels recede — and the stereogram algorithm encodes this depth information into a repeating pattern of random dots that, when viewed with converged or diverged eyes, produces the illusion of three-dimensional surfaces floating in space. This is the same technique that made Magic Eye posters a worldwide phenomenon in the 1990s.

The algorithm works by horizontally shifting the repeat boundary of the dot pattern according to the local depth value derived from the input luminance. Where the source video is bright, the repeat period shortens, pulling that region visually closer to the viewer. Where the video is dark, the repeat period lengthens, pushing the region further away. The result is a flat image of apparently random dots that conceals a volumetric scene visible only through binocular disparity.

The name directly references the stereogram — any flat image that encodes three-dimensional depth information perceivable through binocular vision. The random-dot variant, pioneered by Béla Julesz in 1960, eliminated pictorial depth cues and proved that human stereoscopic perception operates on pure disparity, not on recognizable shapes. Stereogram brings this perceptual experiment to real-time video, turning any camera feed or video source into a depth-encoded illusion.

---

## Background

### Random-Dot Stereograms

Béla Julesz created the first computer-generated random-dot stereogram (RDS) at Bell Labs in 1960 to study binocular depth perception. By presenting each eye with a slightly offset pattern of random dots — with no monocular shape cues — Julesz demonstrated that the human visual system extracts depth purely from retinal disparity. The SIRDS (Single Image Random Dot Stereogram) extends this by encoding both eye views into a single image through periodic horizontal repetition, allowing a single printed image to produce a 3D effect when viewed with the correct vergence.

### The SIRDS Algorithm

The core algorithm works line by line. A random dot pattern is generated for the leftmost repeat-width columns. Then, for each subsequent column, the pixel value is copied from the column one repeat-width to the left — but shifted by a depth-dependent offset. This offset is derived from the luminance of the source image at that pixel position. Where the luminance is high (bright), the offset reduces the effective repeat width, creating a disparity that the brain interprets as a surface closer to the viewer. Where luminance is low (dark), the offset increases the repeat width, pushing the surface away.

### Depth from Luminance

In Stereogram's implementation, the input Y channel is directly mapped to depth displacement. The Depth parameter scales this mapping — at low Depth, even bright/dark extremes produce only subtle depth variation; at high Depth, the full luminance range creates dramatic depth excursions. This luminance-to-depth mapping is the same principle used in displacement mapping for 3D rendering, where a grayscale heightmap drives surface deformation.

### LFSR Pattern Generation

The random dot pattern is generated by a 16-bit Linear Feedback Shift Register (LFSR), which produces a deterministic pseudo-random sequence. The LFSR cycles through 65535 states before repeating, providing sufficient randomness for the dot field. The Dot Density parameter controls a threshold comparison against the LFSR output, determining what fraction of pixels become visible dots versus background. Higher density creates a denser dot field with finer spatial resolution for depth encoding.

### Magic Eye and Popular Culture

The commercial Magic Eye books, first published in 1993 by N.E. Thing Enterprises, brought SIRDS to mass culture. The technique was extended to include colored patterns and hidden pictorial messages, but the fundamental algorithm remained the same: periodic horizontal repetition with depth-modulated offsets. Stereogram recreates this technique in real-time video, allowing any input signal to be transformed into a continuously-updating depth illusion.


---

## Signal Flow

```
                              ┌────────────────────┐
data_in ─────────────────────►│ Stage 0: Y → Depth │
                              │ (scale by depth pot)│
                              └──────┬─────────────┘
                                     │
                                     ▼
                              ┌────────────────────┐
                              │ Stage 1: LFSR      │
                              │ random pattern gen  │
                              └──────┬─────────────┘
                                     │
                                     ▼
                              ┌────────────────────┐
                              │ Stage 2: Horiz.    │
                              │ repeat + depth     │
                              │ offset shift       │
                              └──────┬─────────────┘
                                     │
                                     ▼
                              ┌────────────────────┐
                              │ Stage 3: Dot dens. │
                              │ LFSR threshold     │
                              └──────┬─────────────┘
                                     │
                                     ▼
                              ┌────────────────────┐
                              │ Stage 4: Dot shape │
                              │ (Manhattan round)  │
                              └──────┬─────────────┘
                                     │
                                     ▼
                              ┌────────────────────┐
                              │ Stage 5: Guide dots│
                              │ (top of frame)     │
                              └──────┬─────────────┘
                                     │
                                     ▼
                              ┌────────────────────┐
                              │ Stage 6: Proc Amp  │
                              │ contrast/bright    │
                              └──────┬─────────────┘
                                     │
                                     ▼
                              ┌────────────────────┐
                              │ Stage 7: Inv + Mix │
                              └──────┬─────────────┘
                                     │
data_in ──► [sync delay] ──► dry ──► Interpolator ◄── wet
                                       (4 clk)
                                          │
                                          ▼
                                      data_out
```

The pipeline has a critical horizontal dependency: each pixel's value in Stage 2 depends on a pixel one repeat-width to the left, creating a left-to-right data dependency that cannot be parallelised within a scanline. The LFSR in Stage 1 provides the seed randomness only for the first repeat-width columns; all subsequent columns derive their values from the horizontal repeat with depth-dependent offset. This means the depth illusion quality depends heavily on the Repeat Width parameter — too narrow and the depth resolution is poor, too wide and the viewer's eyes must diverge uncomfortably far to lock on.

The Dot Density and Dot Shape stages (3–4) are post-filtering operations that modify the appearance of the already-depth-encoded pattern. Reducing dot density creates sparse constellations of dots with more background space; round dot shape softens the square-pixel grid into circular elements. Neither stage affects the underlying depth encoding — they are purely cosmetic modifiers.

---

## Parameter Reference

<img src={stereogram_control_panel} alt="Videomancer front panel with Stereogram loaded"/>
*Videomancer's front panel with Stereogram active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Dot Dens
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls the density of the random dot pattern. Higher values produce more visible dots per unit area, creating a denser field with finer spatial resolution for depth perception. At low values, the dot field becomes sparse — individual dots are clearly separated, making the stereogram harder to "lock on" to but producing a more ethereal, star-field appearance. At high values, the field approaches a continuous texture where nearly every pixel is active, encoding depth with maximum fidelity but creating a visually busier pattern.

---

#### Knob 2 — Depth Rng
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Scales the depth displacement amount — how much the input luminance shifts the horizontal repeat boundary. At low values, depth variation is subtle and the stereogram appears nearly flat, requiring careful viewing to detect any 3D effect. At high values, the depth excursion is dramatic, creating strongly-layered surfaces that pop out or recede significantly. Excessive depth can cause the pattern to break down, as the horizontal shift exceeds the brain's ability to fuse the binocular disparity.

---

#### Knob 3 — Repeat W
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the base repeat width of the dot pattern — the horizontal distance between identical pattern repetitions. Narrower widths are easier to view (the eyes diverge less) but provide less spatial resolution for the depth encoding. Wider widths create finer depth detail but require the viewer to diverge their eyes further, which is more difficult and fatiguing. The optimal width depends on the viewing distance and the viewer's eye separation.

---

#### Knob 4 — Dot Size
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Injects additional pseudo-random noise into the dot pattern, breaking up the regularity of the LFSR sequence. At zero, the dot pattern is purely deterministic from the LFSR. As Noise increases, additional random perturbation is added, creating a more organic, less regular dot field. This can help disguise the repeating structure of the stereogram at the cost of slightly degrading the depth encoding precision.

---

#### Knob 5 — Noise
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Applies contrast scaling to the output signal. The Y channel is centred at 512, scaled by the contrast factor, then re-centred. At the initial midpoint, contrast is unity. Below midpoint, the dots become more gray, reducing the contrast between dot and background. Above midpoint, dots become crisper with deeper blacks and brighter whites. High contrast makes the stereogram easier to see as individual dots but does not affect the depth encoding.

---

#### Knob 6 — Contrast
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Shifts the output brightness after contrast scaling. At the midpoint, no offset is applied. Below midpoint, the overall image darkens; above, it brightens. This is purely a cosmetic adjustment that shifts the tonal centre of the dot pattern without affecting the depth information encoded in the horizontal repetition structure.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Pattern** | Dots | Chars |
| **8 — Depth** | Source | Invert |
| **9 — Color** | Mono | Color |
| **10 — Animate** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles control the visual character and accessibility of the stereogram. Color switches between monochrome and color dot fields. Dot Shape softens the pixel grid. Guide adds convergence guide dots to help the viewer lock on. Invert flips the tonal polarity. Bypass disables all processing. Color and Guide are the most viewer-impactful: color dots are more visually interesting but can interfere with depth perception, while Guide dots are essential for viewers unfamiliar with the free-viewing technique.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfades between the dry (original) and wet (stereogram) signal using interpolators. At 0% the output is the unmodified input; at 100% the output is the full stereogram. Intermediate values overlay the dot pattern onto the original image, creating a ghosted effect where the source video shows through the stereogram texture — useful for confirming the depth map correspondence.

---

## Guided Exercises

These exercises progress from basic stereogram generation through depth control to creating viewable 3D depth illusions from live video.

### Exercise 1: First Stereogram

<img src={stereogram_exercise1_result} alt="First Stereogram result"/>
*First Stereogram — simulated result across source images.*
**Source**: Simple high-contrast geometric shapes — a white circle on a black background, or bold text.

**Objective**: Generate a basic random-dot stereogram and learn to perceive the hidden depth.

1. **Default settings**: Start with all controls at their initial values.
2. **Enable guides**: Toggle Guide On. Two reference dots appear at the top of the frame.
3. **View the stereogram**: Relax your eyes and look "through" the screen until the guide dots split into three. The hidden shape should emerge as a floating surface.
4. **Adjust depth**: Increase Depth to about 60%. The shape pops out more dramatically.
5. **Reduce depth**: Set Depth to about 20%. The shape is still visible but subtler.
6. **Compare**: Use Bypass to see the original source and correlate bright regions with the perceived depth.

**Key concepts**: Bright regions in the source appear closer in the stereogram, the guide dots help establish the correct vergence angle, depth pot controls the strength of the 3D illusion

---

### Exercise 2: Depth Control with Video

<img src={stereogram_exercise2_result} alt="Depth Control with Video result"/>
*Depth Control with Video — simulated result across source images.*
**Source**: A slowly-moving face or hand — something with natural depth variation and luminance contrast.

**Objective**: Explore how real-world luminance maps to perceived stereogram depth in real time.

1. **Set repeat width**: Start with Repeat Width at about 40% for comfortable viewing.
2. **Moderate depth**: Set Depth to about 50%.
3. **Observe motion**: As the face/hand moves, the stereogram depth map updates in real time. Bright highlights (forehead, nose tip) project forward; shadows recede.
4. **Increase repeat width**: Move to about 65%. The depth resolution improves but viewing becomes harder.
5. **Add noise**: Set Noise to about 30%. The pattern becomes more organic, less regular.
6. **Round dots**: Toggle Dot Shape to Round. The individual dots become softer.

**Key concepts**: Real-time luminance changes create dynamic depth surfaces, repeat width trades viewing comfort against depth resolution, noise breaks up pattern regularity

---

### Exercise 3: Color Stereogram with Full Processing

<img src={stereogram_exercise3_result} alt="Color Stereogram with Full Processing result"/>
*Color Stereogram with Full Processing — simulated result across source images.*
**Source**: Any colorful, dynamic footage — music visuals, abstract patterns, or natural scenes.

**Objective**: Create a richly textured color stereogram with optimised contrast and dot density.

1. **Enable color**: Toggle Color to Color. The dots gain random hues.
2. **High density**: Set Dot Density to about 75%. The field becomes a dense color mosaic.
3. **Moderate depth**: Depth at about 45%.
4. **Increase contrast**: Set Contrast to about 65%. Dots become crisper.
5. **Slight brightness lift**: Set Brightness to about 55%. The background lightens slightly.
6. **Round dots**: Toggle Dot Shape to Round for softer dot appearance.
7. **Try invert**: Toggle Invert On. The color dots now sit in a bright field — a different aesthetic.
8. **Mix to overlay**: Reduce Mix to about 60%. The original video ghosting shows through.

**Key concepts**: Color dots add visual interest but may slightly impede depth perception, high contrast and density improve dot visibility, mix blending creates overlay effects, invert changes the figure/ground relationship

---


## Tips

- **Start with guides**: Always enable Guide dots when first learning to view stereograms. They provide the vergence reference needed to "lock on" to the 3D image.
- **Narrow repeat width for beginners**: A repeat width of 30–40% is easiest to fuse. Widen only after you can comfortably perceive the depth.
- **High-contrast sources encode best**: Stereograms need clear luminance variation to create perceivable depth. Feed high-contrast, slowly-moving sources for the most dramatic 3D effect.
- **Mono for depth, Color for show**: Monochrome dot fields are easier to perceive in 3D. Switch to color for visual interest once you've confirmed the depth structure.
- **Moderate depth prevents breakdown**: Depth values above 70% can cause pattern tearing where the horizontal shift exceeds the repeat width. Stay at 40–60% for reliable fusion.
- **Round dots + high density = organic texture**: Round dots at 70%+ density create a rich, stippled look reminiscent of pointillist painting.
- **Mix for depth overlay**: At 50–60% Mix, the original video ghosts through the stereogram, creating a hybrid visualization where the source and its depth encoding coexist.
- **Try divergent and convergent**: Some viewers find it easier to diverge (look through the screen) while others converge (cross eyes). Both produce depth, but with inverted polarity.

---

## Glossary

| Term | Definition |
|------|------------|
| **Binocular disparity** | The slight difference in horizontal position between the images seen by the left and right eyes, which the brain uses to compute depth. |
| **BT.601** | The ITU-R standard defining the color matrix used to convert between RGB and YUV in video systems. |
| **Convergence** | The inward rotation of the eyes to fixate on a near object. In stereogram viewing, convergent viewing crosses the eyes to fuse the pattern. |
| **Depth map** | A grayscale image where pixel brightness represents distance from the viewer, used here to drive the stereogram displacement. |
| **Divergence** | The outward rotation of the eyes beyond parallel (looking "through" the image). The standard technique for viewing Magic Eye stereograms. |
| **Free-viewing** | Perceiving stereoscopic depth without optical aids, using either divergent or convergent eye techniques. |
| **Interpolator** | A linear-blending circuit that crossfades between two input values; used in Videomancer for wet/dry mixing. |
| **LFSR** | Linear-Feedback Shift Register; a shift register whose input bit is a function of its previous state, producing pseudo-random sequences. |
| **Manhattan distance** | The sum of absolute horizontal and vertical differences from a point, used here to approximate circular dot shapes from square pixels. |
| **Proc amp** | Processing amplifier; a gain-and-offset stage that applies contrast (multiplication) and brightness (addition) to a signal. |
| **SIRDS** | Single Image Random Dot Stereogram; a flat image encoding binocular depth information through periodic horizontal repetition of random-dot patterns. |
| **Vergence** | The simultaneous movement of both eyes to obtain or maintain binocular vision. The angle between the eyes' lines of sight. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V); the native format of Videomancer's 30-bit video pipeline. |
