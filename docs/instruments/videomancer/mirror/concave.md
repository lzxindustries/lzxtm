---
draft: true
sidebar_position: 53
slug: /instruments/videomancer/concave
title: "Concave"
image: /img/instruments/videomancer/concave/concave_hero.png
---

import concave_hero from '/img/instruments/videomancer/concave/concave_hero.png';
import concave_before_after from '/img/instruments/videomancer/concave/concave_before_after.png';
import concave_control_panel from '/img/instruments/videomancer/concave/concave_control_panel.png';
import concave_exercise1_result from '/img/instruments/videomancer/concave/concave_exercise1_result.png';
import concave_exercise2_result from '/img/instruments/videomancer/concave/concave_exercise2_result.png';
import concave_exercise3_result from '/img/instruments/videomancer/concave/concave_exercise3_result.png';

# Concave

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={concave_hero} alt="Concave hero image"/>
*Concave applying distance-based brightness modulation to simulate the warped reflections of a curved mirror surface.*
<img src={concave_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Concave applied.*

---

## Overview

A concave mirror curves inward, gathering light toward a focal point. A convex mirror curves outward, spreading light away. Both produce images that are brighter or darker depending on how far each point sits from the optical center — regions near the center concentrate or disperse light differently than regions at the edges. Concave brings this optical behavior into the video domain.

The program computes the vertical distance of each scanline from a user-defined center point, squares that distance to produce a parabolic falloff, and uses the result to modulate the brightness of the Y channel. In concave mode, pixels near the center remain bright while those farther away darken — simulating a concave mirror that focuses light inward. In convex mode, the relationship reverses: edges brighten relative to the center, simulating a convex mirror that spreads light outward. The name refers directly to the optical geometry — the inward curve of a concave reflector.

The Distortion control sets the threshold at which the distance effect saturates, controlling how far the brightness gradient extends from the center. At conservative settings, the effect is a gentle vertical vignette. At extreme settings, only a narrow band around the center retains any brightness, collapsing the image into a luminous stripe floating in darkness.

---

## Background

### Concave and Convex Optics

In classical optics, a concave mirror has a reflective surface that curves inward like the inside of a bowl. Parallel rays of light striking the mirror converge at the focal point, producing a real image that is brighter near the center of curvature and dimmer toward the edges. A convex mirror curves outward like the back of a spoon — parallel rays diverge after reflection, producing a virtual image that appears to originate behind the mirror. Both mirror types produce characteristic radial brightness gradients that depend on the distance from the optical axis.

### Anamorphic Distortion in Video Art

Video synthesizers have a long history of simulating optical distortions. Analog video processors achieved barrel and pincushion effects by modulating the deflection voltages of CRT displays. Digital systems can reproduce these transformations by remapping pixel coordinates. Concave takes a simplified approach: rather than performing full geometric remapping, it modulates brightness based on vertical position. The visual result suggests the warped reflections seen in curved mirrors — a luminance gradient that follows the geometry of a curved surface.

### Fun-House Mirrors and Perceptual Distortion

The fun-house mirror is a cultural fixture — a deliberately warped reflective surface that stretches, compresses, and distorts the viewer's reflection. The psychological effect comes from the violation of expected self-image. In video synthesis, similar perceptual disruption arises when brightness gradients are imposed on a recognizable image. Concave's vertical brightness modulation can make a face appear to recede into shadow at the top and bottom while remaining bright at eye level — a digital echo of the concave mirror's focusing effect.

### Distance-Squared Falloff

The brightness modulation in Concave follows an inverse-square relationship. The vertical distance from the center scanline is squared before being used as a modulation factor. This produces a parabolic falloff — the brightness changes slowly near the center and accelerates toward the edges. The squared distance matches the physics of real optical systems, where light intensity follows an inverse-square law. The Distortion parameter acts as a clamp on this squared distance, limiting how far the effect extends before saturating.

### Brightness Modulation as Depth Cue

In film and photography, vignetting — the darkening of image corners relative to the center — is a natural optical artifact that has become a deliberate creative tool. It directs the viewer's attention toward the center of the frame. Concave's brightness modulation works on the same principle but along the vertical axis only, creating a horizontal band of focus. This vertical vignette is particularly effective with video content where the subject occupies the center of the frame.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Sync Detection ─────────────────────────────────────────────
│   ├─ hsync/vsync fall edge detection
│   └─ X counter (per line), Y counter (per field)
│
├── Y Channel ──────────────────────────────────────────────────
│   │
│   ├─ 1. Distance Calc     (v_dist_y = y_counter − center_y)
│   ├─ 2. Distance Squared  (v_dist_sq = v_dist_y × v_dist_y)
│   ├─ 3. Squeeze Factor    (concave: 1023 − dist_sq, clamped at 512)
│   │                       (convex: dist_sq + 512, clamped at 1023)
│   ├─ 4. Brightness Mod    (v_y_out = Y_in × squeeze, bits 19:10)
│   └─ 5. Mix               (interpolator_u: dry ↔ wet via Mix)
│
├── U/V Channels ───────────────────────────────────────────────
│   │
│   ├─ 1. Pass-through      (proc_u = U_in, proc_v = V_in)
│   └─ 2. Mix               (interpolator_u: dry ↔ wet via Mix)
│
├── Sync/Data Delay ────────────────────────────────────────────
│   └─ 8-clock shift register (hsync, vsync, field, Y, U, V)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select original (delayed) or mixed signal
```

The core of Concave is a single multiplication: the input Y value is scaled by a squeeze factor derived from the squared vertical distance to the center scanline. This squeeze factor ranges from 512 (half brightness, at the distance clamp) to 1023 (full brightness, at the center) in concave mode, or from 512 (at center) to 1023 (at clamp) in convex mode. The 10-bit multiplication produces a 20-bit result; the upper 10 bits are taken as the output, effectively dividing by 1024 and preserving the original brightness scale.

The U and V channels pass through unmodified to the mix stage, preserving the original color information while only the luminance is shaped. The three interpolator_u instances blend the processed YUV with the delayed original YUV according to the Mix fader, providing smooth wet/dry crossfading.

---

## Parameter Reference

<img src={concave_control_panel} alt="Videomancer front panel with Concave loaded"/>
*Videomancer's front panel with Concave active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Distortion
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the distance threshold at which the brightness modulation saturates. At low values, even scanlines close to the center experience significant darkening (concave) or brightening (convex), producing a tight band of effect. At high values, the modulation extends across more of the frame before clamping, creating a gentle gradient that covers a wider vertical range. This control defines how pronounced the mirror curvature appears — low values simulate a deeply curved mirror, high values simulate a shallow curve.

---

#### Knob 2 — Center X
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Reserved for horizontal center offset. The register is mapped but does not currently affect the processing pipeline. In future revisions, this parameter may shift the focal point horizontally across the frame, allowing the brightness gradient to be centered on specific image features rather than the frame midpoint.

---

#### Knob 3 — Center Y
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the vertical center of the brightness gradient. The Y counter value is compared against this parameter to compute the signed distance for each scanline. At 50%, the gradient is centered vertically in the frame. Lower values shift the bright region toward the top of the image; higher values shift it toward the bottom. This is the primary compositional control — it determines which scanlines receive full brightness and which fall into the modulated region.

---

#### Knob 4 — Radius
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Reserved for radius control. The register is mapped but does not currently modify the processing pipeline. In future revisions, this parameter may define the radius of a circular or elliptical region within which the brightness modulation is applied, limiting the effect to a defined area rather than spanning the full frame height.

---

#### Knob 5 — Zoom
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Reserved for zoom control. The register is mapped but does not currently affect processing. In future revisions, this parameter may scale the distance function, stretching or compressing the brightness gradient independently of the Distortion threshold.

---

#### Knob 6 — Tint
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Reserved for tint control. The register is mapped but does not currently modify the chroma channels. In future revisions, this parameter may tint the darkened or brightened regions with a color shift, adding chromatic depth to the distance-based modulation.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Convex** | Off | On |
| **8 — Circular** | Off | On |
| **9 — Edge Wrap** | Off | On |
| **10 — Color** | Off | On |
| **11 — Bypass** | Off | On |

Toggle 7 selects between concave and convex mirror modes, fundamentally changing the brightness gradient direction. Toggle 11 provides instant bypass for A/B comparison. Toggles 8, 9, and 10 are registered for future functionality — Circular (limiting the effect to a round region), Edge Wrap (wrapping the distance calculation at frame boundaries), and Color (applying modulation to chroma channels as well as luma). Currently only the Convex and Bypass toggles modify the output signal.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Controls the wet/dry mix between the processed and original signal via three interpolator_u instances. At 0%, the output is entirely the original (delayed) signal — no brightness modulation is visible. At 100%, the output is entirely the processed signal with full distance-based modulation. Intermediate values blend the two, allowing subtle brightness shaping to be layered over the source without completely replacing it.

---

## Guided Exercises

These exercises explore Concave's brightness modulation from gentle vignettes to dramatic carved-light effects. Each exercise adds complexity, building from simple center placement to full concave/convex comparison.

### Exercise 1: Vertical Vignette

<img src={concave_exercise1_result} alt="Vertical Vignette result"/>
*Vertical Vignette — simulated result across source images.*
**Source**: A live camera feed or recorded footage with a centered subject — a face, a still life, or a graphic pattern.

**Objective**: Learn how Center Y and Distortion interact to create a controlled vertical brightness gradient.

1. **Center the gradient**: Set Center Y to 50% so the bright region sits at the vertical midpoint of the frame.
2. **Apply distortion**: Slowly decrease Distortion from 100% toward 0%. Watch as the edges of the frame darken, creating a vertical vignette that narrows around the center.
3. **Shift the center**: Move Center Y below 50% to push the bright band toward the top of the frame. Move it above 50% to push it downward.
4. **Full mix**: Confirm Mix is at 100% to see the full effect. Then reduce Mix to 50% to blend the vignette with the original — a subtle shading overlay.
5. **Bypass**: Toggle Bypass to compare the vignetted image against the original.

**Key concepts**: Vertical distance from center controls brightness, the squared distance creates a parabolic falloff, Distortion sets the saturation threshold

---

### Exercise 2: Convex Inversion

<img src={concave_exercise2_result} alt="Convex Inversion result"/>
*Convex Inversion — simulated result across source images.*
**Source**: High-contrast footage — strong geometric shapes, text overlays, or architectural subjects.

**Objective**: Explore how convex mode inverts the brightness gradient and changes the visual character.

1. **Start concave**: Set Distortion to ~40%, Center Y to 50%, Mix to 100%. Observe the darkened edges and bright center strip.
2. **Switch to convex**: Enable the Convex toggle. The gradient inverts — the center darkens while edges brighten. The image appears to glow from the periphery.
3. **Narrow the effect**: Decrease Distortion. The bright edge region extends further inward in convex mode, eventually overwhelming the center.
4. **Creative offset**: Shift Center Y to ~25%. The bright/dark transition line moves upward, creating an asymmetric split where the top of the frame is treated differently from the bottom.
5. **Partial mix**: Set Mix to ~60% to blend the convex modulation with the original, creating a soft edge glow.

**Key concepts**: Convex reverses the concave brightness relationship, asymmetric center placement creates split-screen brightness effects, partial mix blends the effect non-destructively

---

### Exercise 3: Carved Light Band

<img src={concave_exercise3_result} alt="Carved Light Band result"/>
*Carved Light Band — simulated result across source images.*
**Source**: Any active video — motion footage works particularly well as the moving content passes through the brightness band.

**Objective**: Use extreme settings to isolate a narrow horizontal stripe of brightness from a dark surround.

1. **Extreme distortion**: Set Distortion to ~10% — this creates a very tight brightness band.
2. **Center placement**: Set Center Y to 50% to place the band at the vertical midpoint.
3. **Observe the band**: Only scanlines very close to the center Y retain brightness. Everything else falls to half-brightness or below.
4. **Sweep the band**: Slowly move Center Y from 0% to 100%. The bright stripe scans vertically through the image, revealing different horizontal slices of the source.
5. **Convex stripe**: Enable Convex to invert — now a narrow dark stripe sits at center with bright edges. The visual character completely changes.
6. **Layer with mix**: Set Mix to ~40% so the carved band is layered over the original rather than replacing it.

**Key concepts**: Low Distortion values create narrow brightness bands, sweeping Center Y scans the band through the image like a slit-scan, convex inversion turns a bright band into a dark stripe

---


## Tips

- **Center Y is compositional**: Think of it as placing a spotlight — wherever the center is, that horizontal band receives the most (concave) or least (convex) brightness.
- **Low Distortion = tight band**: The Distortion parameter is a distance threshold. Lower values mean the squared-distance clamp kicks in sooner, creating a narrower region of full brightness.
- **Convex for edge glow**: Switch to convex mode when you want the frame edges to brighten rather than darken — useful for creating a halo or border glow effect.
- **Mix for subtlety**: Use partial Mix values (30–60%) to add gentle brightness shaping without overpowering the source. Full mix at extreme Distortion settings can crush most of the image to half-brightness.
- **Feedback loops**: Routing the output back to the input compounds the brightness modulation — each pass darkens the edges further (concave) or brightens them further (convex), creating self-reinforcing gradients.
- **Pair with color programs**: Since Concave only modulates luminance (U/V pass through), chain it with a chroma-processing program to independently shape brightness and color.
- **Animate Center Y**: Slowly sweeping Center Y with an LFO or modulation source creates a scanning spotlight effect — a bright horizontal band that moves through the frame over time.

---

## Glossary

| Term | Definition |
|------|------------|
| **Brightness Modulation** | Scaling the luminance value of each pixel by a position-dependent factor, making some regions brighter or darker than others. |
| **Concave Mirror** | A mirror with an inward-curving reflective surface that converges light toward a focal point, producing brighter center and darker edges. |
| **Convex Mirror** | A mirror with an outward-curving reflective surface that diverges light, producing darker center and brighter edges. |
| **Distance-Squared Falloff** | A parabolic brightness profile where modulation increases with the square of the distance from center, matching natural optical behavior. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Interpolator** | A circuit that blends between two input values based on a mix coefficient, used here for wet/dry crossfading. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Squeeze Factor** | The multiplicative scaling value applied to each pixel's luminance, derived from the squared vertical distance to the center scanline. |
| **Vignette** | Darkening of image edges relative to the center, here applied along the vertical axis to simulate curved-mirror optics. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
