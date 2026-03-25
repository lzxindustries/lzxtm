---
draft: true
sidebar_position: 55
slug: /instruments/videomancer/cloudgate
title: "Cloudgate"
image: /img/instruments/videomancer/cloudgate/cloudgate_hero_s1.png
description: "In the early 1990s, the NewTek Video Toaster turned commodity hardware into a broadcast studio."
---

![Cloudgate hero image](/img/instruments/videomancer/cloudgate/cloudgate_hero_s1.png)
*Cloudgate layering animated procedural cloud formations over a portrait, with radial tunnel masking revealing the subject through drifting white mist.*

---

## Overview

Cloudgate conjures clouds and smoke from thin air, compositing them over your video input as a semi-transparent overlay. It generates its own animated cloud texture using ***procedural noise***, a mathematical technique that produces organic, naturalistic patterns without any stored imagery. The clouds drift across the frame on their own, swirling and billowing in real time. You control the density, scale, tint, and animation speed of the cloud layer, and a radial tunnel mask lets you reveal or obscure the center of the image through a portal of fog.

At gentle settings, Cloudgate adds an atmospheric haze that softens and mystifies the source material. Crank it up and the clouds take over: thick, opaque banks of mist that swallow the picture entirely. Between those extremes lies a wide range of cinematic fog effects, dreamy dissolves, and volumetric tunnel transitions. The four operation modes offer distinct cloud behaviors, from swirling vortex tunnels to vertically drifting smoke columns to uniform cloud cover.

Cloudgate is inspired by the cloud and smoke transition effects from the NewTek Video Toaster, the legendary Amiga-based video production system of the early 1990s. Those effects were ground-breaking at the time, offering broadcast-quality cloud dissolves from a desktop computer. Cloudgate reimagines them for real-time analog video synthesis with continuous parameter control.

### What's In a Name?

The name ***Cloudgate*** carries a dual meaning. First, it references the program's function: a ***gate*** through which ***clouds*** pass, revealing or concealing the video beneath. The radial tunnel modes literally create a circular gate of clouds. Second, it's a nod to ***Cloud Gate***, the iconic reflective sculpture by Anish Kapoor in Chicago's Millennium Park. Like the sculpture, Cloudgate transforms what it reflects, distorting familiar images through a shimmering, otherworldly lens.

---

## Quick Start

1. Turn **Mix** (Fader 12) fully clockwise and set **Density** (Knob 1) to about 50%. A layer of soft, white clouds appears over your input video, drifting gently across the frame.
2. Increase **Drift Spd** (Knob 4) to speed up the animation. The clouds roll and scroll faster, creating a feeling of motion and depth.
3. Turn up **Tunnel** (Knob 5). A circular aperture opens in the center of the frame, pushing the clouds toward the edges and revealing the original video at the center. You've conjured a portal.
4. Flip **Mode A** (Switch 7) to On. The tunnel inverts: clouds now concentrate at the center and the edges clear. This is the difference between Cloud Tunnel In and Cloud Tunnel Out.

---

## Parameters

![Videomancer front panel with Cloudgate loaded](/img/instruments/videomancer/cloudgate/cloudgate_control_panel.png)
*Videomancer's front panel with Cloudgate active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Density

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Density** controls the opacity threshold of the cloud layer. It determines how much of the generated noise pattern becomes visible as clouds. At 0%, fully counterclockwise, nearly all of the noise field renders as opaque cloud, producing a thick, solid fog that obscures the input. As Density increases, the threshold rises and only the densest peaks of the noise pattern remain visible. At 100%, fully clockwise, very little of the noise exceeds the threshold and the cloud layer is sparse and wispy.

:::tip
Think of Density as a "fog machine" dial. Low values fill the room with fog; high values let most of it dissipate, leaving only faint wisps.
:::

---

### Knob 2 — Scale

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Scale** controls the spatial frequency of the noise pattern, which determines the size of individual cloud formations. At 0%, the noise is sampled at a very coarse scale, producing enormous, slow-moving cloud structures that span the entire frame. As Scale increases, the grid cells shrink and the clouds become smaller, more numerous, and more finely detailed. At 100%, the clouds are at their smallest, creating a dense, granular texture. The Scale parameter selects among six discrete zoom levels internally, so you may notice the cloud pattern jump between sizes as you turn the knob.

---

### Knob 3 — Detail

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Detail** controls the strength of the second noise octave, adding fine-grained texture on top of the base cloud pattern. This is a technique called ***fractional Brownian motion*** (fBM), where multiple layers of noise at different scales are combined to produce a more complex, naturalistic result. At 0%, fully counterclockwise, only the base octave is visible and the clouds have smooth, simple shapes. As Detail increases, the second octave contributes more prominently, adding smaller bumps, ridges, and wisps within each cloud formation. At 100%, the second octave is at full strength and the clouds appear rough and highly textured.

---

### Knob 4 — Drift Spd

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |

**Drift Spd** controls the speed of the cloud animation. Each frame, the noise coordinates shift by an amount determined by this parameter. At 0%, the clouds are frozen in place with no animation. As Drift Spd increases, the clouds move faster. The drift direction depends on the current mode: in **Smoke Up** mode, clouds drift upward; in the tunnel modes, they drift outward; in **Uniform Clouds** mode, they drift diagonally.

---

### Knob 5 — Tunnel

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |

**Tunnel** controls the radius of the radial aperture mask. This parameter only has a visible effect in the two tunnel modes (**Cloud Tunnel In** and **Cloud Tunnel Out**). At 0%, fully counterclockwise, the tunnel aperture is closed and clouds cover the entire frame. As Tunnel increases, the aperture opens wider. At 100%, the aperture reaches the edges of the frame. In **Smoke Up** and **Uniform Clouds** modes, this parameter has no visible effect because those modes use full-frame cloud coverage without any radial masking.

:::note
If you don't see changes when adjusting Tunnel, check that **Mode A** and **Mode B** are set to one of the two tunnel modes (both Off, or A On / B Off).
:::

---

### Knob 6 — Brightness

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |

**Brightness** scales the overall opacity of the cloud layer after the density threshold is applied. At 0%, the clouds are fully transparent regardless of density. At 50%, the default position, the clouds appear at moderate opacity. At 100%, the cloud layer is at maximum strength, producing the densest possible fog. Brightness acts as a master volume control for the entire cloud effect.

---

### Switch 7 — Mode A

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Mode A** is the first bit of the two-bit mode selector. Together with **Mode B** (Switch 8), it selects one of four cloud behavior modes. See the Toggle Group Notes below for the full mode table. Flipping Mode A while Mode B is Off toggles between **Cloud Tunnel In** and **Cloud Tunnel Out**, swapping whether clouds concentrate at the edges or the center.

---

### Switch 8 — Mode B

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Mode B** is the second bit of the two-bit mode selector. Together with **Mode A** (Switch 7), it selects one of four cloud behavior modes. Flipping Mode B while Mode A is Off toggles between **Cloud Tunnel In** and **Smoke Up**, changing the cloud behavior from radial masking to vertical drift.

---

### Switch 9 — Tint A

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Tint A** is the first bit of the two-bit cloud color selector. Together with **Tint B** (Switch 10), it selects one of four cloud tint presets. See the Toggle Group Notes below for the full tint table. Each tint defines a fixed YUV color that the cloud layer is rendered in.

---

### Switch 10 — Tint B

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Tint B** is the second bit of the two-bit cloud color selector. Together with **Tint A** (Switch 9), it selects one of four cloud tint presets. Flipping Tint B while Tint A is Off toggles between **Warm White Mist** and **Cool Gray Mist**.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** routes the unprocessed input signal directly to the output, skipping all cloud generation and compositing stages. The sync delay pipeline still aligns timing, so there is no glitch on transition. Use Bypass for instant A/B comparison between the raw input and the cloud-overlaid result.

---

:::note Toggle Group Notes

**Mode A** and **Mode B** form a two-bit selector that chooses the cloud behavior mode. Each mode changes how clouds are distributed across the frame and the direction of the animated drift.

| Mode A | Mode B | Mode | Description |
|--------|--------|------|-------------|
| Off | Off | Cloud Tunnel In | Clouds dense at edges, clear at center. Drift scrolls outward. The **Tunnel** knob controls the aperture radius |
| On | Off | Cloud Tunnel Out | Clouds dense at center, clear at edges. Drift scrolls outward. The **Tunnel** knob controls the cloud radius |
| Off | On | Smoke Up | Clouds drift upward with slight horizontal turbulence. Full-frame coverage, **Tunnel** knob has no effect |
| On | On | Uniform Clouds | Gentle diagonal drift. Full-frame coverage, **Tunnel** knob has no effect |

:::tip
**Cloud Tunnel In** is a classic transition effect: the subject appears through a circular window framed by billowing clouds. **Cloud Tunnel Out** is the reverse: the subject vanishes behind a growing cloud disc.
:::

**Tint A** and **Tint B** form a second two-bit selector that chooses the color of the cloud layer.

| Tint A | Tint B | Cloud Color |
|--------|--------|-------------|
| Off | Off | Warm White Mist — bright, slightly warm clouds reminiscent of classic Video Toaster effects |
| On | Off | Golden Heavenly Glow — warm golden clouds with amber highlights |
| Off | On | Cool Gray Mist — subdued, cooler fog with subtle blue undertones |
| On | On | Dark Smoke — near-black smoke with neutral color |

:::

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry input signal and the cloud-composited output. At 0%, fully left, the output is the original input with no cloud overlay. At 100%, fully right (the default), the output is the fully processed cloud-composited signal. Intermediate positions blend the two, allowing subtle atmospheric effects without full commitment to the cloud layer.

---

## Background

### Procedural noise

Cloudgate generates its cloud patterns using ***lattice value noise***, one of the simplest forms of procedural noise. The technique divides the screen into a regular grid of cells. At each grid corner, a ***hash function*** (a deterministic number scrambler) produces a pseudorandom value. Between the grid corners, the algorithm uses ***bilinear interpolation*** to smoothly blend the corner values together, producing the soft, rounded contours that read as clouds.

The noise engine in Cloudgate is shared with the Organica program. Both use the same 16-entry permutation table and the same hash function. The difference is in what they do with the noise: Organica uses it for organic textures, while Cloudgate treats it as a volumetric density field and composites it over video.

### Fractional Brownian motion

Natural clouds are not smooth blobs. They have detail at many scales: large billowing masses, medium-sized puffs, and tiny wisps at the edges. Cloudgate achieves this multi-scale structure using ***fractional Brownian motion*** (fBM), a technique that layers multiple ***octaves*** of noise at different spatial frequencies. The base octave provides the large cloud shapes. The second octave, at twice the spatial frequency, adds finer detail within each cloud. The **Detail** knob controls how much the second octave contributes. At zero, you get simple, smooth shapes. At maximum, the clouds gain rough, turbulent edges.

### Alpha compositing

The cloud layer is blended with the input video using ***alpha compositing***, the standard technique for layering transparent imagery. For each pixel, the output is calculated as:

`output = input × (1 − alpha) + cloud_color × alpha`

The ***alpha*** value at each pixel is derived from the noise density field after thresholding and brightness scaling. Where alpha is zero, the input passes through unchanged. Where alpha is one, the cloud color completely replaces the input. Between those extremes, the cloud and input blend together smoothly. This is the same compositing math used in film visual effects and image editing software.

### The radial tunnel mask

The tunnel modes apply a ***radial distance mask*** that varies cloud density based on distance from the center of the frame. The distance is approximated using an ***octagon approximation*** rather than a true circle, which saves significant hardware resources while still producing a visually convincing round aperture. The approximation uses the formula `distance ≈ max(|dx|, |dy|) + 0.5 × min(|dx|, |dy|) − 0.125 × min(|dx|, |dy|)`, where dx and dy are the horizontal and vertical distances from center. The **Tunnel** knob sets the radius threshold: in Cloud Tunnel In mode, pixels inside the radius are cleared; in Cloud Tunnel Out mode, pixels outside the radius are cleared.


---

## Signal Flow

### Signal Flow Notes

The processing chain has two parallel paths that converge at the compositor. The cloud generation engine runs independently, producing an alpha value and a cloud color at each pixel. Meanwhile, the input video is delayed through a 5-stage pipeline so it arrives at the compositor at the same time as the cloud data. The compositor blends the two using the alpha channel and passes the result to three interpolator instances (one per YUV channel) for the final wet/dry mix.

The drift accumulator is updated once per frame at the vsync edge, not once per pixel. This means the entire cloud field shifts uniformly each frame, producing smooth scrolling animation. The direction and magnitude of the shift depend on the current mode: Smoke Up drifts strongly upward with a hint of horizontal turbulence, the tunnel modes drift outward, and Uniform Clouds drifts diagonally.

:::tip
**Scale affects everything.** Because the noise coordinates are scaled before hashing, the Scale parameter changes not only the size of the clouds but also the apparent speed of the drift animation. Larger clouds appear to move more slowly at the same Drift Spd setting because each pixel covers a smaller portion of the noise field.
:::


---

## Exercises

These exercises progress from simple fog overlay to cinematic tunnel transitions. Each builds on the previous one, gradually engaging more of the parameter space.
### Exercise 1: Atmospheric Fog Layer

![Atmospheric Fog Layer result](/img/instruments/videomancer/cloudgate/cloudgate_ex1_s1.png)
*Atmospheric Fog Layer — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A soft, drifting fog layer over live video, like morning mist rolling across a landscape.

#### Key Concepts

- Procedural noise generates naturalistic cloud patterns
- Density and Brightness control how much of the noise field becomes visible
- Drift speed animates the cloud layer

#### Video Source

A live camera feed or recorded footage with a recognizable subject. Faces and landscapes work especially well because the fog interacts visually with familiar forms.

#### Steps

1. Set **Mix** (Fader 12) fully clockwise. Set all toggles to Off.
2. Turn **Density** (Knob 1) to about 40%. A soft haze appears over the video.
3. Adjust **Scale** (Knob 2) to about 50%. The cloud formations take on a medium size, neither too coarse nor too fine.
4. Increase **Detail** (Knob 3) to about 60%. Finer textures appear within the cloud shapes, adding realism.
5. Turn up **Drift Spd** (Knob 4) to about 30%. The clouds begin to scroll gently across the frame.
6. Adjust **Brightness** (Knob 6) to taste. Higher values produce more opaque fog; lower values make it more transparent and atmospheric.

#### Settings

| Control | Value |
|---------|-------|
| Density | 40% |
| Scale | 50% |
| Detail | 60% |
| Drift Spd | 30% |
| Tunnel | 0% |
| Brightness | 50% |
| Mode A | Off |
| Mode B | Off |
| Tint A | Off |
| Tint B | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Cloud Tunnel Portal

![Cloud Tunnel Portal result](/img/instruments/videomancer/cloudgate/cloudgate_ex2_s1.png)
*Cloud Tunnel Portal — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A circular portal through billowing clouds that frames the subject at the center of the image, like peering through a magical rift in a fog bank.

#### Key Concepts

- The tunnel mask creates a radial aperture in the cloud layer
- Mode selection changes whether clouds appear at the edges or the center
- Tint selection colors the clouds for different moods

#### Video Source

A centered subject such as a face, a still life, or graphic content. The tunnel framing works best when there is a clear focal point in the middle of the frame.

#### Steps

1. Start from the Exercise 1 settings. Set **Density** to about 30% and **Brightness** to about 70% for strong, visible clouds.
2. Turn **Tunnel** (Knob 5) to about 50%. A circular clear zone opens in the center of the frame, with clouds framing the edges. The subject is revealed through the portal.
3. Adjust Tunnel to widen or narrow the aperture. Notice how the cloud boundary follows a roughly circular path.
4. Flip **Mode A** (Switch 7) to On. The tunnel inverts: clouds now fill the center and the edges are clear. The subject disappears behind a disc of fog.
5. Set **Tint A** (Switch 9) to On. The clouds change from white to a warm golden color.
6. Set **Tint A** to Off and **Tint B** (Switch 10) to On. The clouds become a cool gray mist.
7. Set both **Tint A** and **Tint B** to On. Dark smoke fills the tunnel.

#### Settings

| Control | Value |
|---------|-------|
| Density | 30% |
| Scale | 50% |
| Detail | 60% |
| Drift Spd | 30% |
| Tunnel | 50% |
| Brightness | 70% |
| Mode A | Off |
| Mode B | Off |
| Tint A | Off |
| Tint B | Off |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 3: Rising Smoke Column

![Rising Smoke Column result](/img/instruments/videomancer/cloudgate/cloudgate_ex3_s1.png)
*Rising Smoke Column — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

Thick, dark smoke rising from the bottom of the frame, partially obscuring the video behind it. Think campfire smoke, volcanic haze, or dramatic stage fog.

#### Key Concepts

- Smoke Up mode creates strong vertical drift animation
- Combining high detail with fast drift produces turbulent smoke
- Tinting dark smoke creates cinematic atmosphere

#### Video Source

Any footage, especially material with a dark lower region or a contrasting subject. Concert footage or moody portraits are ideal.

#### Steps

1. Set **Mode B** (Switch 8) to On and **Mode A** (Switch 7) to Off. This selects **Smoke Up** mode.
2. Set **Density** to about 60% for thick, well-defined smoke.
3. Set **Scale** to about 30% for large, billowing formations.
4. Turn **Detail** (Knob 3) to about 80%. The smoke gains rough, turbulent edges.
5. Increase **Drift Spd** (Knob 4) to about 70%. The smoke rises rapidly with visible horizontal turbulence.
6. Set **Tint A** and **Tint B** both to On. The clouds become dark smoke.
7. Increase **Brightness** to about 80%. The dark smoke becomes dense and opaque.
8. Slowly reduce **Mix** (Fader 12) to about 70% to let some of the background video bleed through the smoke.

#### Settings

| Control | Value |
|---------|-------|
| Density | 60% |
| Scale | 30% |
| Detail | 80% |
| Drift Spd | 70% |
| Tunnel | 0% |
| Brightness | 80% |
| Mode A | Off |
| Mode B | On |
| Tint A | On |
| Tint B | On |
| Bypass | Off |
| Mix | 70% |

---
## Glossary

- **Alpha Compositing**: A blending technique that combines two images using a per-pixel transparency value (alpha), where 0 is fully transparent and 1 is fully opaque.

- **Bilinear Interpolation**: A method of smoothly blending four neighboring grid values based on the fractional position between them, producing soft gradients.

- **Drift**: The per-frame offset applied to the noise coordinates, creating the illusion of cloud movement.

- **fBM (Fractional Brownian Motion)**: A technique that layers multiple octaves of noise at increasing spatial frequencies to produce naturalistic, multi-scale patterns.

- **Hash Function**: A deterministic formula that takes grid coordinates as input and returns a pseudorandom value, ensuring the same coordinates always produce the same noise value.

- **Lattice Value Noise**: A procedural noise technique that assigns pseudorandom values to regular grid points and interpolates between them.

- **Octave**: In procedural noise, a single layer of noise at a specific spatial frequency. Multiple octaves at different frequencies are combined to create complex patterns.

- **Opacity**: The degree to which a pixel blocks the image behind it. Full opacity means the cloud completely replaces the input; zero opacity means the input passes through.

- **Procedural Noise**: A mathematical function that generates apparently random but continuous patterns, used to simulate natural textures like clouds, terrain, and marble.

- **Radial Distance**: The distance of a pixel from the center of the frame, used by the tunnel mask to determine where clouds appear.

---
