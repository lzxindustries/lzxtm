---
draft: true
sidebar_position: 37
slug: /instruments/videomancer/carousel
title: "Carousel"
image: /img/instruments/videomancer/carousel/carousel_hero_s1.png
description: "In the early 1980s, the Ampex ADO 100 introduced real-time digital video manipulation to broadcast television."
---

import BeforeAfterSlider from '@site/src/components/BeforeAfterSlider';
import carousel_control_panel from '/img/instruments/videomancer/carousel/carousel_control_panel.png';
import carousel_source1_runner from '/img/instruments/videomancer/carousel/carousel_source1_runner.png';
import carousel_source2_parrot from '/img/instruments/videomancer/carousel/carousel_source2_parrot.png';
import carousel_source3_elephant from '/img/instruments/videomancer/carousel/carousel_source3_elephant.png';
import carousel_source4_pattern from '/img/instruments/videomancer/carousel/carousel_source4_pattern.png';
import carousel_source5_woman from '/img/instruments/videomancer/carousel/carousel_source5_woman.png';
import carousel_source6_paint from '/img/instruments/videomancer/carousel/carousel_source6_paint.png';
import carousel_hero_s1 from '/img/instruments/videomancer/carousel/carousel_hero_s1.png';
import carousel_hero_s2 from '/img/instruments/videomancer/carousel/carousel_hero_s2.png';
import carousel_hero_s3 from '/img/instruments/videomancer/carousel/carousel_hero_s3.png';
import carousel_hero_s4 from '/img/instruments/videomancer/carousel/carousel_hero_s4.png';
import carousel_hero_s5 from '/img/instruments/videomancer/carousel/carousel_hero_s5.png';
import carousel_hero_s6 from '/img/instruments/videomancer/carousel/carousel_hero_s6.png';
import carousel_ex1_s1 from '/img/instruments/videomancer/carousel/carousel_ex1_s1.png';
import carousel_ex1_s2 from '/img/instruments/videomancer/carousel/carousel_ex1_s2.png';
import carousel_ex1_s3 from '/img/instruments/videomancer/carousel/carousel_ex1_s3.png';
import carousel_ex1_s4 from '/img/instruments/videomancer/carousel/carousel_ex1_s4.png';
import carousel_ex1_s5 from '/img/instruments/videomancer/carousel/carousel_ex1_s5.png';
import carousel_ex1_s6 from '/img/instruments/videomancer/carousel/carousel_ex1_s6.png';
import carousel_ex2_s1 from '/img/instruments/videomancer/carousel/carousel_ex2_s1.png';
import carousel_ex2_s2 from '/img/instruments/videomancer/carousel/carousel_ex2_s2.png';
import carousel_ex2_s3 from '/img/instruments/videomancer/carousel/carousel_ex2_s3.png';
import carousel_ex2_s4 from '/img/instruments/videomancer/carousel/carousel_ex2_s4.png';
import carousel_ex2_s5 from '/img/instruments/videomancer/carousel/carousel_ex2_s5.png';
import carousel_ex2_s6 from '/img/instruments/videomancer/carousel/carousel_ex2_s6.png';
import carousel_ex3_s1 from '/img/instruments/videomancer/carousel/carousel_ex3_s1.png';
import carousel_ex3_s2 from '/img/instruments/videomancer/carousel/carousel_ex3_s2.png';
import carousel_ex3_s3 from '/img/instruments/videomancer/carousel/carousel_ex3_s3.png';
import carousel_ex3_s4 from '/img/instruments/videomancer/carousel/carousel_ex3_s4.png';
import carousel_ex3_s5 from '/img/instruments/videomancer/carousel/carousel_ex3_s5.png';
import carousel_ex3_s6 from '/img/instruments/videomancer/carousel/carousel_ex3_s6.png';

# Carousel

<span class="head2_nolink">Videomancer Program Guide</span>

<BeforeAfterSlider
  sources={[
    { label: "Runner", before: carousel_source1_runner, after: carousel_hero_s1 },
    { label: "Parrot", before: carousel_source2_parrot, after: carousel_hero_s2 },
    { label: "Elephant", before: carousel_source3_elephant, after: carousel_hero_s3 },
    { label: "Pattern", before: carousel_source4_pattern, after: carousel_hero_s4 },
    { label: "Woman", before: carousel_source5_woman, after: carousel_hero_s5 },
    { label: "Paint", before: carousel_source6_paint, after: carousel_hero_s6 },
  ]}
/>
*Carousel mapping live video onto a rotating cube face with per-scanline perspective foreshortening and directional shading.*

---

## Overview

In the early 1980s, the Ampex ADO 100 introduced real-time digital video manipulation to broadcast television. Its signature effect — the Auto Cube — became the visual shorthand for "digital video effects" for an entire decade. A single channel of video mapped onto the face of a spinning cube, foreshortened as the face turned away from the viewer, darkened by simulated directional lighting, and revealing a colored background as it rotated past the edge. It appeared in network idents, news opens, commercial bumpers, and any production that wanted to say *the future is here*.

Carousel recreates that single-face rotation. The name comes from the revolving motion of the mapped face — a carousel platform spinning its rider through a full circle. The program computes per-scanline geometry from a cosine lookup table, maps source pixels through a DDA (Digital Differential Analyzer) accumulator, applies luminance shading proportional to the face angle, and composites the result over a solid-color background. The effect is entirely horizontal in default configuration — each scanline is independently compressed and repositioned — but the rotation axis can be switched to horizontal for a top-over-bottom tumble.

At a fixed angle the program produces a static oblique projection — a picture-in-picture with perspective compression. With auto-rotation enabled and speed turned up, the face spins continuously, cycling through front-face video, edge collapse, back-face display (mirrored or solid), and return. The shading, background hue, and mix controls allow the effect to range from a subtle off-axis tilt to a full theatrical cube spin complete with lighting and chromatic background.

---

## Background

### What Is DVE?

DVE — Digital Video Effects — is the broadcast industry term for real-time spatial manipulation of a video image. The first DVE systems appeared in the late 1970s: the Quantel DPE 5000, NEC DVE, and Ampex ADO (Ampex Digital Optics). These machines could squeeze, stretch, rotate, tumble, and page-turn a full frame of video in real time, an astonishing capability when all prior effects required optical or mechanical processes. The ADO 100's rotating cube was perhaps the most recognized DVE effect ever created — a single video source mapped onto one face of a three-dimensional cube that spun on command. Carousel distills this effect to its essential geometry: one face, one axis, real-time rotation.

### What Is Perspective Foreshortening?

When a flat rectangle rotates away from the viewer, it appears to narrow along the axis of rotation. A face turned 45° appears approximately 70% of its original width (cos 45° ≈ 0.707). At 90° — edge-on — it vanishes entirely (cos 90° = 0). This geometric narrowing is called **foreshortening**, and it is the primary visual cue for three-dimensional rotation on a two-dimensional display. Carousel computes the visible width of the face as the absolute value of the cosine of the rotation angle, scaled to the active video width. The result is a scanline-by-scanline compression that narrows symmetrically around the face center.

### What Is DDA Mapping?

A Digital Differential Analyzer is an algorithm for stepping through a source signal at a rate different from the output rate. To compress 1280 pixels of source video into, say, 900 pixels of visible face, Carousel sets up a fixed-point accumulator that advances by a step larger than one source pixel per output pixel. Each output pixel reads from the source address pointed to by the integer part of the accumulator. The result is a spatially compressed version of the source — every pixel is accounted for, with no gaps or overlaps, and the compression ratio is continuously variable based on the rotation angle.

### What Is Directional Shading?

Real objects under fixed lighting appear brighter when facing the light and darker when turned away. Carousel approximates this with a **shade factor** derived from the cosine of the rotation angle. When the face is square to the viewer (cos θ = 1), shading is at maximum brightness. As the face rotates away, the shade factor decreases, darkening the mapped video. The Shade Depth control sets the floor — how dark the face gets at its most oblique angle before disappearing. This single-parameter lighting model is crude by 3D-rendering standards but perfectly matches the look of original 1980s DVE hardware, which used similar approximations.

### What Is Front/Back Face Switching?

A rotating plane has two sides. The front face is the side the viewer sees when the rotation angle is between −90° and +90° — the side showing the source video. Beyond 90°, the plane has rotated past edge-on and the viewer is looking at the back. Carousel detects this transition using the sign of the cosine: positive cosine means front face, negative means back. In **Mirror** mode, the back face shows the source video horizontally flipped — as if the plane were transparent. In **Solid** mode, the back face shows a uniform medium gray, mimicking an opaque card.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── 1. Input Register         (latch Y/U/V + sync)
│
├── 2. Rotation Phase         (DDS accumulator: auto speed or manual angle)
│       │
│       ├─ theta_index = phase(15:8)
│       ├─ cos_val = C_COS_LUT(theta_index)
│       ├─ sin_val = C_COS_LUT((theta_index + 192) mod 256)
│       └─ front_face = (theta_index < 64) or (theta_index >= 192)
│
├── 3. Per-Line Geometry      (computed once per scanline at h_active start)
│       ├─ abs_cos = |cos_val − 512|
│       ├─ line_width = ACTIVE_W × abs_cos / 512
│       ├─ face_center = HALF_W + sin_signed × HALF_W / 512
│       ├─ face_left = face_center − line_width / 2
│       └─ face_right = face_center + line_width / 2
│
├── 4. Region Classify + DDA  (per pixel)
│       ├─ Inside face → DDA accumulator → read_addr
│       │   └─ Back face + Mirror → read_addr = W − 1 − raw_addr
│       └─ Outside face → background region
│
├── 5. Line Buffer Read       (2-clock latency)
│       └─ 3× video_line_buffer (Y, U, V) random-access read
│
├── 6. Shade + Composite      (per pixel)
│       ├─ shade_factor = abs_cos × (1023 − shade_depth) / 512 + shade_depth
│       ├─ Face pixels: shaded_y = lb_y × shade_factor >> 10
│       ├─ Back face solid: Y=256, U/V=512
│       └─ Background: Y=bkg_lum, U/V from 64-entry hue LUT
│
├── 7. Interpolator Mix       (4-clock latency)
│       └─ 3× interpolator_u: crossfade dry ↔ wet
│
├── Sync Signals ─────────────────────────────────────────
│   └─ Pass-through (hsync, vsync, field, avid) with pipeline delay
│
└── Bypass ────────────────────────────────────────────────
    └─ Select original or processed signal
```

The critical geometry is computed once per scanline at the start of horizontal active video, then held constant across the line. This means the face boundaries and DDA step size are uniform within each line — a correct approximation for rotation about a vertical axis (where every scanline sees the same width), and an intentional simplification for horizontal axis rotation (where a true 3D projection would vary width per scanline). The two-clock read latency from the line buffers is absorbed into the pipeline; the shade and composite stage operates on data from the previous line's write, creating a one-line delay that is visually imperceptible at video rates.

---

## Parameter Reference

<img src={carousel_control_panel} alt="Videomancer front panel with Carousel loaded"/>
*Videomancer's front panel with Carousel active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Angle
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Sets the manual rotation angle when Auto Rotate is off. The face width and position update smoothly as you turn the knob, compressing to a thin sliver near the quarter-turn points and expanding back to full width at center and at the half-turn. In auto mode this control is ignored — the DDS phase accumulator overrides it. Start with manual mode to understand how the geometry responds to angle before switching to continuous rotation.

---

#### Knob 2 — BKG Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 180° |
| Suffix | ° |

Sets the hue of the background color visible in the regions outside the mapped face. The background uses a 64-entry lookup table that maps hue angle to U/V chroma values at the luminance set by BKG Lum. Full sweep produces a complete color wheel — reds, yellows, greens, cyans, blues, magentas. A chromatic background is essential for the classic broadcast cube aesthetic, where the spinning face floated over a solid color field.

---

#### Knob 3 — Speed
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the auto-rotation speed when Auto Rotate is enabled. At minimum the face is stationary. As speed increases, the DDS phase accumulator advances more per frame, producing faster continuous rotation. Very high speeds create a rapid strobing effect as the face whips through front/back/edge transitions on every few frames. For smooth cinematic rotation, keep speed in the lower quarter of its range.

---

#### Knob 4 — Perspective
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Labeled Perspective in the TOML configuration. In the current VHDL implementation this register is declared but not connected to any processing logic — it is reserved for a future per-scanline trapezoid modulation that would vary face width from top to bottom, simulating true perspective convergence. Turning this knob has no visible effect on the output. It is included in the control layout for forward compatibility.

---

#### Knob 5 — Shade Depth
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the minimum brightness of the face shading. At maximum, the face is unshaded — full brightness at all angles. At minimum, the face darkens dramatically as it rotates away from center, reaching near-black at edge-on. The shade factor is derived from the cosine of the rotation angle scaled between this minimum floor and full brightness. A mid-range setting produces the most naturalistic lighting — noticeable darkening at oblique angles without total blackout.

---

#### Knob 6 — BKG Lum
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Sets the luminance of the background independently of its hue. At minimum, the background is black regardless of the BKG Hue setting. At maximum, the background reaches peak white, with the hue LUT providing only the U/V chrominance. For the classic broadcast look — a deep saturated color field — keep luminance in the 20–40% range. Higher values produce pastels; lower values produce rich, dark backgrounds.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Back Face** | Mirror | Solid |
| **8 — Rot Axis** | Vertical | Horiz |
| **9 — Direction** | CW | CCW |
| **10 — Auto Rotate** | Manual | Auto |
| **11 — Bypass** | Off | On |

The five toggles configure the rotation behavior and appearance mode. Back Face and Rot Axis affect the geometric mapping itself. Direction and Auto Rotate control the motion system. Bypass overrides everything. They can be changed at any time — even mid-rotation — without glitching, because the geometry pipeline recomputes every scanline.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Crossfades between the original (dry) video and the rotated/composited (wet) output. At 100% the full cube-face effect is visible. At 0% the original video passes through unmodified. Intermediate positions blend the two — useful for ghostly superimposition effects where the rotating face is semi-transparent over the source. The interpolator operates on all three YUV channels simultaneously.

---

## Guided Exercises

These exercises progress from static angle positioning through continuous rotation to full broadcast-style cube animation. Each introduces additional controls while building on the geometry concepts from the previous exercise.

### Exercise 1: Static Oblique Projection

<BeforeAfterSlider
  sources={[
    { label: "Runner", before: carousel_source1_runner, after: carousel_ex1_s1 },
    { label: "Parrot", before: carousel_source2_parrot, after: carousel_ex1_s2 },
    { label: "Elephant", before: carousel_source3_elephant, after: carousel_ex1_s3 },
    { label: "Pattern", before: carousel_source4_pattern, after: carousel_ex1_s4 },
    { label: "Woman", before: carousel_source5_woman, after: carousel_ex1_s5 },
    { label: "Paint", before: carousel_source6_paint, after: carousel_ex1_s6 },
  ]}
/>
*Static Oblique Projection — simulated result across source images.*
**Source**: A live camera feed or recorded footage with recognizable subjects.

**Objective**: Understand the relationship between rotation angle, face width, and shading by positioning the face manually.

1. **Center position**: With Angle at 0°, confirm the face fills the entire screen — the image appears unmodified except for the background visible at mix transitions.
2. **Quarter turn**: Slowly rotate the Angle knob toward 90°. Watch the face narrow symmetrically, revealing background on both sides.
3. **Shading**: With the face at about 45°, increase Shade Depth from maximum to minimum. Observe the face darkening as shading deepens.
4. **Background color**: Sweep BKG Hue through a full rotation while keeping the face at 45°. The color field behind the face cycles through the spectrum.
5. **Edge-on**: Push the angle to exactly 90°. The face collapses to near-zero width — edge-on. Rotate past 90° to see the back face appear.
6. **Back face modes**: Toggle Back Face between Mirror and Solid. In Mirror mode the video is flipped; in Solid mode it shows gray.

**Key concepts**: Face width is proportional to |cos(angle)|, shading darkens as the face turns away, background is visible outside the face boundaries, front/back switching occurs at the 90° boundary

---

### Exercise 2: Continuous Cube Spin

<BeforeAfterSlider
  sources={[
    { label: "Runner", before: carousel_source1_runner, after: carousel_ex2_s1 },
    { label: "Parrot", before: carousel_source2_parrot, after: carousel_ex2_s2 },
    { label: "Elephant", before: carousel_source3_elephant, after: carousel_ex2_s3 },
    { label: "Pattern", before: carousel_source4_pattern, after: carousel_ex2_s4 },
    { label: "Woman", before: carousel_source5_woman, after: carousel_ex2_s5 },
    { label: "Paint", before: carousel_source6_paint, after: carousel_ex2_s6 },
  ]}
/>
*Continuous Cube Spin — simulated result across source images.*
**Source**: Bold, high-contrast footage — animated graphics, text overlays, or a face.

**Objective**: Configure continuous auto-rotation and explore speed, direction, and axis behavior.

1. **Enable auto**: Switch Auto Rotate to Auto. The Angle knob is now overridden.
2. **Slow rotation**: Set Speed to about 10%. Watch the face smoothly rotate — narrowing, disappearing at edge, returning as the back face, then reappearing front-on.
3. **Direction**: While rotating slowly, toggle Direction from CW to CCW. The face reverses smoothly.
4. **Axis change**: Toggle Rot Axis to Horizontal. The compression switches from horizontal squeeze to vertical squeeze — a top-over-bottom tumble.
5. **Speed sweep**: Slowly increase Speed. At high speeds the face becomes a rapid strobe as it whips through angles. Find a comfortable cinematic speed in the lower quarter.
6. **Back face solid**: With the face spinning, switch Back Face to Solid. The back side now shows gray instead of flipped video — notice how it changes the character of the spin.

**Key concepts**: DDS phase accumulator creates smooth continuous rotation, direction reversal is instantaneous, axis change reorients the entire geometry, high speeds create stroboscopic effects

---

### Exercise 3: Broadcast Cube Ident

<BeforeAfterSlider
  sources={[
    { label: "Runner", before: carousel_source1_runner, after: carousel_ex3_s1 },
    { label: "Parrot", before: carousel_source2_parrot, after: carousel_ex3_s2 },
    { label: "Elephant", before: carousel_source3_elephant, after: carousel_ex3_s3 },
    { label: "Pattern", before: carousel_source4_pattern, after: carousel_ex3_s4 },
    { label: "Woman", before: carousel_source5_woman, after: carousel_ex3_s5 },
    { label: "Paint", before: carousel_source6_paint, after: carousel_ex3_s6 },
  ]}
/>
*Broadcast Cube Ident — simulated result across source images.*
**Source**: A logo, station ident graphic, or bold text on a contrasting background.

**Objective**: Recreate the classic 1980s broadcast cube spin — a logo rotating over a saturated color field with dramatic shading and smooth motion.

1. **Color field**: Set BKG Hue to a deep blue (~240°) and BKG Lum to about 20%. This creates the saturated background typical of 1980s network idents.
2. **Shading**: Set Shade Depth to about 40% for dramatic face darkening as it rotates away.
3. **Slow spin**: Enable Auto Rotate, set Speed to about 8% for a stately rotation.
4. **Mirror back**: Set Back Face to Mirror so the logo is legible from both sides.
5. **Full wet**: Ensure Mix is at 100%. The entire frame should be the cube effect.
6. **Record a cycle**: Let the face complete 2–3 full rotations while recording. This is the classic ADO cube spin.
7. **Tumble variant**: Switch Rot Axis to Horizontal for a top-over-bottom tumble. Change BKG Hue to magenta (~300°) for variation.

**Key concepts**: The combination of saturated background, moderate shading, and slow rotation recreates the iconic broadcast DVE aesthetic, mirror back face preserves logo legibility, axis switching creates variety in sequential idents

---


## Tips

- **Manual first, auto second**: Start in Manual mode to understand how the face geometry responds to angle before enabling continuous rotation. Once you see the geometry, auto mode makes sense.
- **Shade Depth is the lighting knob**: The most convincing 3D illusion comes from moderate shading — around 40–60%. Too little looks flat; too much makes the face vanish into darkness at oblique angles.
- **Background luminance matters**: A dark, saturated background (BKG Lum ~20–30%, strong hue) reads as a professional broadcast color field. Bright backgrounds wash out the effect.
- **Perspective does nothing (yet)**: The Perspective knob is reserved for a future update. Don't spend time troubleshooting why it has no effect — it is intentionally unconnected.
- **Mirror makes it legible**: If your source contains text or logos, use Mirror mode for the back face so the content remains readable from both sides of the rotation.
- **Feedback loops amplify the spin**: Routing the output back to the input creates recursive cube faces — a face within a face within a face, each at a different rotation angle.
- **Low speed for broadcast feel**: The classic ADO cube spin was stately and slow. Keep Speed below 15% for that authentic 1980s network ident pacing.
- **Combine with other DVE programs**: Use Carousel's output as input to programs that add further spatial effects for complex multi-layer broadcast compositions.

---

## Glossary

| Term | Definition |
|------|------------|
| **ADO** | Ampex Digital Optics; an early broadcast DVE system (1981) whose Auto Cube effect is the direct inspiration for Carousel. |
| **Compositing** | The process of combining multiple image layers into a single output, here merging the rotated face with a colored background. |
| **Cosine** | A trigonometric function that, for a rotation angle θ, gives the ratio of the visible face width to its full width; stored here as a 256-entry lookup table. |
| **DDA** | Digital Differential Analyzer; an algorithm that steps through source pixels at a non-integer rate to produce spatial compression or expansion. |
| **DDS** | Direct Digital Synthesis; a technique using a phase accumulator incremented each frame to generate a continuously advancing rotation angle. |
| **DVE** | Digital Video Effects; the broadcast industry term for real-time spatial manipulation of video images such as squeeze, rotate, tumble, and page-turn. |
| **Foreshortening** | The apparent narrowing of a surface as it rotates away from the viewer, proportional to the cosine of the rotation angle. |
| **LUT** | Lookup Table; a pre-computed array of values indexed by an input parameter, used here for cosine and background hue-to-chroma conversions. |
| **Phase accumulator** | A counter that wraps around at a fixed modulus, producing a continuously cycling value used to drive the rotation angle in auto mode. |
| **Scanline** | A single horizontal row of pixels in a video frame; Carousel computes face geometry independently for each scanline. |
| **YUV** | A color encoding system separating luminance (Y) from two chrominance components (U, V), the native format for video processing. |

---
