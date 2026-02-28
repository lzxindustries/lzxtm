---
draft: true
sidebar_position: 103
slug: /instruments/videomancer/flurry
title: "Flurry"
image: /img/instruments/videomancer/flurry/flurry_hero.png
---

import flurry_hero from '/img/instruments/videomancer/flurry/flurry_hero.png';
import flurry_animation from '/img/instruments/videomancer/flurry/flurry_animation.gif';
import flurry_control_panel from '/img/instruments/videomancer/flurry/flurry_control_panel.png';
import flurry_exercise1_result from '/img/instruments/videomancer/flurry/flurry_exercise1_result.gif';
import flurry_exercise2_result from '/img/instruments/videomancer/flurry/flurry_exercise2_result.gif';
import flurry_exercise3_result from '/img/instruments/videomancer/flurry/flurry_exercise3_result.gif';

# Flurry

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={flurry_hero} alt="Flurry hero image"/>
*A single luminous particle traces an elliptical orbit through darkness â€” its Manhattan-distance glow diamond sweeping a warm trail across the void.*
<img src={flurry_animation} alt="Flurry animated output"/>
*Flurry output evolving over multiple frames â€” synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Flurry renders a single orbiting luminous particle that traces an elliptical path across the screen, producing a drifting point of light with a diamond-shaped glow field. A 32-entry quarter-wave sine lookup table drives the horizontal and vertical components of the orbit, with the two components offset by 8 entries (a quarter cycle) to produce an ellipse. The particle's position is governed by a 16-bit phase accumulator that advances by the Speed parameter on every vertical sync interval, giving smooth, continuous orbital motion whose rate scales linearly with the knob position.

The name references Apple's macOS Flurry screensaver â€” a mesmerizing cascade of luminous, smoke-like particle trails orbiting around an invisible attractor. While the original Flurry used OpenGL-accelerated additive blending with hundreds of translucent particles, Videomancer's implementation distills the concept to its essence: a single bright particle on an elliptical path, rendered through Manhattan distance glow without any frame buffer or temporal persistence. The result is a minimalist interpretation of orbital particle animation â€” a bright diamond of light sweeping through darkness in perpetual elliptical motion.

Color can be fixed from the Color knob, producing a static chrominance across the entire glow field, or modulated by a frame counter when Color Cycle is enabled, causing the particle's hue to drift slowly through the color space across successive frames. The Mix fader blends the synthesized particle field with any passthrough input video, and the Bypass toggle routes the delayed input directly to the output. Several TOML parameters (Decay, Trails, Multi Orbit, Blur) are defined in the interface but not implemented in the current VHDL â€” they serve as reserved control points for future firmware extensions.

---

## Background

### macOS Flurry Screensaver

The Flurry screensaver, originally written by Calum Robinson in 2002 and later integrated into macOS as a default screen saver, is one of the most recognizable examples of particle-based generative animation. It renders streams of semi-transparent particles orbiting invisible attractors using additive blending and OpenGL acceleration, producing luminous smoke-like tendrils that evoke incense trails or aurora filaments. The visual signature comes from the combination of orbital mechanics, additive glow compositing, and temporal persistence â€” each particle leaves a fading trail that reveals the underlying elliptical path. Videomancer's Flurry distills this concept to a single hardware-friendly particle with no frame buffer, capturing the orbital motion and glow character while sacrificing the multi-particle trail complexity of the original.

### Orbital Mechanics and Parametric Curves

An elliptical orbit in two dimensions can be expressed parametrically as $x(\theta) = a \cdot \cos(\theta)$ and $y(\theta) = b \cdot \sin(\theta)$, where $a$ and $b$ are the semi-major and semi-minor axes and $\theta$ advances with time. In FPGA logic, trigonometric functions are typically approximated through lookup tables. Flurry uses a 32-entry quarter-wave sine table that stores one quarter of a full sine cycle â€” the remaining three quarters are reconstructed through symmetry of the 5-bit phase index. The cosine component is obtained by offsetting the phase index by 8 entries (a quarter of the 32-entry table), producing the 90Â° phase shift that separates sine from cosine. The orbit radius parameter scales both components equally before adding them to the screen center at (640, 360), so the ellipse aspect ratio is fixed by the relationship between the sine and cosine table entries at the 8-entry offset.

### Sine Lookup Table Animation

Hardware-efficient sine generation via quarter-wave lookup tables is a foundational technique in digital signal processing and FPGA design. A full sine wave over $[0, 2\pi]$ has fourfold symmetry: the first quarter (0 to $\pi/2$) can be reflected and negated to reconstruct the remaining three quarters. By storing only 32 samples of the ascending quarter wave (values 0 to 255 in 8-bit unsigned representation), the full 128-entry cycle can be addressed using a 7-bit index with appropriate mirroring logic. Flurry's implementation is simpler: it stores all 32 entries directly (the ascending and descending halves of one half-cycle) and uses the upper 5 bits of the 16-bit phase accumulator as the table index, wrapping naturally at 32. The phase accumulator advances by the Speed register's upper 8 bits each frame, giving fine control over orbital velocity â€” from nearly stationary at low Speed to rapid revolution at maximum.

### Additive Glow Compositing

Additive glow creates the visual impression of a luminous source radiating light into surrounding space. The technique assigns brightness values that decrease with distance from a point source, producing a soft halo effect. Flurry uses Manhattan distance ($|dx| + |dy|$) rather than Euclidean distance ($\sqrt{dx^2 + dy^2}$), which avoids the multiplication and square root operations that are expensive in combinatorial FPGA logic. The resulting iso-brightness contours are diamond-shaped rather than circular, producing a distinctly digital aesthetic that recalls early computer graphics and pixel art. The glow intensity at each pixel is computed as brightness minus distance, clamped to zero when distance exceeds the Size threshold â€” a linear falloff that creates a bright core tapering to darkness at the edges of the diamond.

### Screensaver Art as Generative Practice

The screensaver genre â€” born from the practical necessity of preventing CRT phosphor burn-in â€” has evolved into one of the most widely experienced forms of generative art. From the hypnotic geometry of After Dark's *Starfield* and *Flying Toasters* to the elegant curves of Windows' *Mystify Your Mind* and macOS's *Flurry*, these programs share a common design philosophy: autonomous animation that rewards ambient attention without demanding active engagement. Flurry belongs to this tradition, producing a single orbiting light source whose elliptical path creates satisfying spatial patterns over time. The interplay between orbital velocity, glow size, brightness, and color cycling transforms a simple parametric curve into a contemplative visual instrument â€” a luminous beacon sweeping through darkness with the unhurried regularity of a lighthouse beam.


---

## Signal Flow

```
Synthesis Engine (no input video required)
â”‚
â”œâ”€â”€ Clock 0: Register Decode â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
â”‚   â”œâ”€ orbit_radius = registers_in(0)   [10-bit]
â”‚   â”œâ”€ speed        = registers_in(1)   [10-bit]
â”‚   â”œâ”€ size         = registers_in(2)   [10-bit]
â”‚   â”œâ”€ color        = registers_in(3)   [10-bit]
â”‚   â”œâ”€ brightness   = registers_in(4)   [10-bit]
â”‚   â”œâ”€ decay        = registers_in(5)   [10-bit, unused in VHDL]
â”‚   â”œâ”€ mix_amount   = registers_in(7)   [10-bit]
â”‚   â””â”€ toggles from registers_in(6):
â”‚       â”œâ”€ bit 0: color_cycle (0=off, 1=on)
â”‚       â”œâ”€ bit 1: trails      (0=off, 1=on) [unused in VHDL]
â”‚       â”œâ”€ bit 2: multi_orbit (0=off, 1=on) [unused in VHDL]
â”‚       â”œâ”€ bit 3: blur        (0=off, 1=on) [unused in VHDL]
â”‚       â””â”€ bit 4: bypass
â”‚
â”œâ”€â”€ Quarter-Wave Sine LUT (32 entries, 8-bit unsigned) â”€â”€â”€â”€â”€â”€â”€â”€
â”‚   â””â”€ Values: 0, 25, 50, 74, 98, 120, 142, 162,
â”‚              180, 197, 212, 225, 236, 244, 250, 254,
â”‚              255, 254, 250, 244, 236, 225, 212, 197,
â”‚              180, 162, 142, 120, 98, 74, 50, 25
â”‚
â”œâ”€â”€ Phase Accumulator (16-bit, per-vsync update) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
â”‚   â””â”€ s_phase_acc += speed(9 downto 2)  [upper 8 bits of Speed]
â”‚
â”œâ”€â”€ Orbit Position Computation (per vsync) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
â”‚   â”œâ”€ phase_idx = s_phase_acc(15 downto 11)  [upper 5 bits]
â”‚   â”œâ”€ sin_val = sine_lut(phase_idx)
â”‚   â”œâ”€ cos_val = sine_lut(phase_idx + 8)  [quarter-cycle offset]
â”‚   â”œâ”€ orbit_x = 640 + (sin_val Ã— orbit_radius(9:2)) >> 8
â”‚   â””â”€ orbit_y = 360 + (cos_val Ã— orbit_radius(9:2)) >> 8
â”‚
â”œâ”€â”€ Per-Pixel Manhattan Distance â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
â”‚   â”œâ”€ dx = |x_counter âˆ’ orbit_x|
â”‚   â”œâ”€ dy = |y_counter âˆ’ orbit_y|
â”‚   â””â”€ dist = dx + dy
â”‚
â”œâ”€â”€ Glow Generation â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
â”‚   â””â”€ if dist < size:
â”‚       â””â”€ glow = brightness âˆ’ dist(9 downto 0)
â”‚   else:
â”‚       â””â”€ glow = 0
â”‚
â”œâ”€â”€ Color Assignment â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
â”‚   â”œâ”€ proc_y = glow
â”‚   â”œâ”€ Color Cycle ON:
â”‚   â”‚   â”œâ”€ proc_u = frame_counter(9 downto 2)  [8-bit, expanded to 10]
â”‚   â”‚   â””â”€ proc_v = frame_counter(7 downto 0)  [8-bit, expanded to 10]
â”‚   â””â”€ Color Cycle OFF:
â”‚       â”œâ”€ proc_u = color
â”‚       â””â”€ proc_v = 1023 âˆ’ color
â”‚
â”œâ”€â”€ Interpolator Stage â€” wet/dry mix (4 clocks each) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
â”‚   â”œâ”€ mix_y = lerp(input_y, proc_y, mix_amount)
â”‚   â”œâ”€ mix_u = lerp(input_u, proc_u, mix_amount)
â”‚   â””â”€ mix_v = lerp(input_v, proc_v, mix_amount)
â”‚
â”œâ”€â”€ Sync Pipeline (8-stage delay) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
â”‚   â””â”€ hsync_n, vsync_n, field_n, Y, U, V delayed 8 clocks
â”‚
â””â”€â”€ Bypass Mux â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    â””â”€ bypass ? delayed_input : mixed_output
```

The architecture is driven by two distinct temporal domains. The orbit engine runs exclusively during the vertical blanking interval: each vsync falling edge advances the 16-bit phase accumulator by the upper 8 bits of the Speed register, looks up sine and cosine values from the 32-entry LUT, multiplies each by the scaled orbit radius, and adds the results to the screen center coordinates (640, 360). The cosine component uses a phase index offset of +8 entries within the same sine table â€” equivalent to a 90Â° phase shift â€” which produces the elliptical orbit geometry. The rendering pipeline then operates during active video, computing the Manhattan distance from each output pixel to the single particle position and generating a glow contribution based on the Size and Brightness parameters.

The color cycling mechanism, when enabled, derives chrominance directly from the free-running 16-bit frame counter rather than from the Color knob. The U channel receives bits 9:2 of the counter (a slowly changing 8-bit value expanded to the 10-bit register width) while V receives bits 7:0 â€” a faster-cycling 8-bit value. Because these two bit fields overlap partially (bits 7:2 are shared), U and V evolve at different rates, producing a continuous, asymmetric color drift that cycles through a complex path in the UV chrominance plane. When color cycling is disabled, U is set directly from the Color parameter while V is computed as 1023 âˆ’ Color, producing complementary chrominance that sweeps from one end of the UV axis to the other as the knob is turned.

---

## Parameter Reference

<img src={flurry_control_panel} alt="Videomancer front panel with Flurry loaded"/>
*Videomancer's front panel with Flurry active. Knobs 1â€“6 (top two rows of left cluster), Toggle switches 7â€“11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1â€“6)

#### Knob 1 â€” Orbit Radius
| Property | Value |
|----------|-------|
| Range | 0% â€“ 100% |
| Default | 50% |
| Suffix | % |

Controls the radial extent of the particle's elliptical orbit around the screen center at (640, 360). The upper 8 bits of the 10-bit register value are multiplied by the sine and cosine LUT outputs and right-shifted by 8 to produce pixel offsets from center. At minimum, the orbit collapses to a stationary point at screen center â€” the multiplication product is near zero regardless of the trigonometric values. At maximum, the particle sweeps wide arcs that can approach the screen edges, creating dramatic spatial coverage. Intermediate values produce compact to moderate ellipses whose aspect ratio is fixed by the sine/cosine offset relationship in the LUT.

---

#### Knob 2 â€” Speed
| Property | Value |
|----------|-------|
| Range | 0% â€“ 100% |
| Default | 38% |
| Suffix | % |

Sets the angular velocity of the orbiting particle by controlling how quickly the 16-bit phase accumulator advances. The upper 8 bits of the Speed register are added to the accumulator on every vertical sync interval. At minimum, the particle crawls through its orbit imperceptibly slowly â€” the phase increment is nearly zero, requiring thousands of frames to complete a full revolution. At maximum, the particle races around the ellipse, potentially completing multiple revolutions per second. The visual effect ranges from a near-stationary glow at minimum to a rapidly sweeping beacon at maximum, with moderate settings producing the most contemplative orbital cadence.

---

#### Knob 3 â€” Size
| Property | Value |
|----------|-------|
| Range | 0% â€“ 100% |
| Default | 38% |
| Suffix | % |

Determines the spatial extent of the glow diamond rendered around the particle center. The Size register value serves as the distance threshold: pixels whose Manhattan distance from the particle center is less than this value receive a glow contribution, while pixels beyond the threshold render as black. At minimum, the glow collapses to a tiny point. At maximum, the diamond extends 1023 pixels in Manhattan distance from the particle center, covering a substantial fraction of the screen. Size interacts with Brightness to determine the visible extent â€” the effective visible radius is the minimum of Size and Brightness, since the glow formula (brightness âˆ’ distance) reaches zero when distance equals brightness even if Size allows larger distances.

---

#### Knob 4 â€” Color
| Property | Value |
|----------|-------|
| Range | 0% â€“ 100% |
| Default | 50% |
| Suffix | % |

When Color Cycle is Off, this knob sets the fixed chrominance of the particle. The U channel receives the Color value directly while V receives 1023 âˆ’ Color, creating a complementary relationship. At the center position (512), U and V are both near midpoint, producing a near-neutral white glow. Turning the knob toward minimum shifts the color toward one end of the UV axis (low U, high V â€” warm tones), while turning toward maximum shifts it to the opposite end (high U, low V â€” cool tones). When Color Cycle is On, this parameter has no effect â€” chrominance is derived from the frame counter instead.

---

#### Knob 5 â€” Brightness
| Property | Value |
|----------|-------|
| Range | 0% â€“ 100% |
| Default | 75% |
| Suffix | % |

Controls the peak luminance of the particle's glow field. The Brightness value serves as the ceiling from which Manhattan distance is subtracted: a pixel at distance $d$ from the particle center receives glow equal to brightness âˆ’ $d$, clamped to zero. At maximum (1023), the glow field is intensely bright at center and tapers gradually over a wide area. At minimum, the subtraction drives glow to zero within a few pixels of center, producing a barely perceptible point. Brightness and Size interact to define the visual presence of the particle â€” high brightness with small size creates an intense pinpoint, while moderate brightness with large size creates a broad, diffuse diamond of soft light.

---

#### Knob 6 â€” Decay
| Property | Value |
|----------|-------|
| Range | 0% â€“ 100% |
| Default | 38% |
| Suffix | % |

Labeled as Decay in the TOML interface. Although this parameter is mapped to register 5 and wired to the `s_decay` signal in the VHDL, the current implementation does not use it â€” there is no frame buffer or temporal persistence mechanism. The parameter is reserved for a future firmware revision that might implement exponential decay trails, where previous particle positions would dim gradually over time rather than disappearing instantly. At present, all settings produce identical behavior.

---

### Toggle Switches (Switches 7â€“11)

| Switch | Off | On |
|--------|-----|-----|
| **7 â€” Color Cycle** | Off | On |
| **8 â€” Trails** | Off | On |
| **9 â€” Multi Orbit** | Off | On |
| **10 â€” Blur** | Off | On |
| **11 â€” Bypass** | Off | On |

Toggles 7â€“11 configure five binary aspects of the particle system, though only two toggles have behavioral effects in the current VHDL. Color Cycle (7) switches between fixed knob-derived chrominance and frame-counter-modulated color drift. Bypass (11) routes delayed input directly to the output. The remaining three toggles â€” Trails (8), Multi Orbit (9), and Blur (10) â€” are wired to VHDL signals but have no effect on the rendering pipeline. They serve as reserved interface points for future extensions: Trails would enable temporal persistence, Multi Orbit would render additional particles on offset paths, and Blur would soften the diamond glow edges.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 â€” Mix
| Property | Value |
|----------|-------|
| Range | 0% â€“ 100% |
| Default | 100% |
| Suffix | % |

Controls the wet/dry mix ratio between the delayed input video and the synthesized particle field via the interpolator stage. At maximum (1023), the output is fully wet â€” the particle field at full intensity. At minimum (0), the output is fully dry â€” only the delayed input passes through. In pure synthesis mode (no external input), the "dry" signal is black (Y=0, U=V=512), so reducing Mix fades the particle toward darkness. Intermediate values create translucent particle rendering when overlaid on external video. For standalone screensaver use, keep Mix at maximum for full particle brightness.

---

## Guided Exercises

These exercises explore Flurry's orbital synthesis capabilities, progressing from a basic centered orbit through color cycling dynamics to extreme parameter interactions that reveal the limits of the glow rendering engine.

### Exercise 1: Gentle Orbit

<img src={flurry_exercise1_result} alt="Gentle Orbit result"/>
*Gentle Orbit â€” simulated result across source images.*
**Objective**: Establish a slow, wide elliptical orbit with warm fixed color, observing the relationship between orbit radius, speed, and glow geometry.

1. **Set orbit radius to ~60%**: The particle should trace a moderately wide ellipse around screen center.
2. **Set speed to ~25%**: Slow, contemplative orbital motion â€” the particle takes several seconds to complete a full revolution.
3. **Set moderate size (~40%)**: A clearly visible diamond-shaped glow field extends from the particle center.
4. **Set warm color**: Turn Color to ~25% to place U low and V high, producing a warm amber tone.
5. **Set brightness to ~75%**: Bright enough to see the full extent of the glow diamond, but not clipping.
6. **Disable color cycle**: Color Cycle toggle to Off. The particle should maintain a steady amber hue throughout its orbit.
7. **Observe the orbit shape**: The elliptical path is defined by the sine/cosine offset in the LUT. The horizontal and vertical excursions may differ slightly, creating a true ellipse rather than a circle.
8. **Sweep orbit radius from minimum to maximum**: Watch the orbit collapse to a stationary center point and then expand to fill the screen.

**Key concepts**: Phase accumulator controls orbital velocity, sine LUT offset creates elliptical path, orbit radius scales both axes equally

---

### Exercise 2: Chromatic Sweep

<img src={flurry_exercise2_result} alt="Chromatic Sweep result"/>
*Chromatic Sweep â€” simulated result across source images.*
**Objective**: Enable color cycling and observe the frame-counter-driven chrominance modulation as the particle orbits, noting the asymmetric U and V evolution rates.

1. **Start from Exercise 1 settings** with moderate orbit and brightness.
2. **Enable Color Cycle**: Toggle Color Cycle to On. The particle should begin shifting hue frame by frame.
3. **Set speed to ~15%**: Slow orbit lets you watch the color evolve over time without the particle moving too fast.
4. **Increase brightness to ~85%**: Ensure the color is clearly visible across the full glow diamond.
5. **Observe U vs V cycling rates**: U derives from frame_counter bits 9:2 (slowly changing) while V derives from bits 7:0 (faster changing). The particle's hue should drift through a complex path â€” sometimes warm, sometimes cool, sometimes neutral.
6. **Compare with fixed color**: Toggle Color Cycle Off and set Color to ~50%. The particle locks to a single hue. Toggle back On to resume cycling.
7. **Try maximum orbit radius and speed**: With wide orbit and fast cycling, the particle traces rapid colorful arcs across the screen.

**Key concepts**: Frame counter bits drive asymmetric U/V evolution, color cycling overrides Color knob, complementary UV relationship in fixed mode

---

### Exercise 3: Maximum Glow

<img src={flurry_exercise3_result} alt="Maximum Glow result"/>
*Maximum Glow â€” simulated result across source images.*
**Objective**: Push Size and Brightness to their extremes to explore the glow rendering limits, observing how the Manhattan distance diamond scales and how the single particle can fill a large portion of the screen.

1. **Set orbit radius to ~30%**: Keep the orbit compact near center so the glow field stays on screen.
2. **Set speed to ~10%**: Very slow orbit for steady observation.
3. **Maximize size (~100%)**: The distance threshold extends to 1023, allowing glow contribution across a huge area.
4. **Maximize brightness (~100%)**: The full 1023 ceiling creates intense center brightness with falloff extending across the entire allowed region.
5. **Observe glow extent**: At maximum size and brightness, the diamond should cover a very large area of the screen â€” brightness drops linearly from 1023 at center to 0 at a Manhattan distance of 1023.
6. **Enable color cycle**: The massive glow field drifts through colors, creating a large chromatic wash across the screen.
7. **Reduce size gradually**: Sweep Size from maximum downward. The diamond contracts, concentrating brightness into a smaller, more intense core.
8. **Reduce brightness gradually**: With size still moderate, sweep Brightness down and observe the glow shrinking even within the size threshold â€” the linear falloff reaches zero sooner at lower brightness.

**Key concepts**: Size sets maximum glow distance, brightness sets peak intensity and effective range, effective visible extent is min(size, brightness)

---


## Tips

- **Start with moderate Orbit Radius and slow Speed**: A wide, slow orbit reveals the elliptical path geometry most clearly. Very high speeds cause the particle to jump between positions, obscuring the smooth orbital character.
- **Size and Brightness interact as a minimum**: The visible glow extent is limited by whichever is smaller. For maximum visible area, both must be high. For an intense pinpoint, use high brightness with low size.
- **Color Cycle overrides the Color knob**: When cycling is enabled, adjusting Color has no effect â€” disable cycling first to dial in a specific fixed hue.
- **Manhattan diamonds are a feature**: The diamond-shaped glow is an intentional consequence of the hardware-efficient distance metric. At small sizes it resembles a point source; at large sizes it becomes a distinctive geometric signature.
- **Use Orbit Radius at zero for a stationary light**: Setting orbit radius to minimum parks the particle at screen center, turning Flurry into a static glow field â€” useful for testing brightness, size, and color parameters without the complication of orbital motion.
- **Mix fader doubles as a brightness control**: In pure synthesis mode with no input video, reducing Mix fades the particle toward black. Use this for subtle ambient effects at low mix levels.
- **Reserved parameters are future-ready**: Decay, Trails, Multi Orbit, and Blur exist in the interface but have no current effect. They will activate in future firmware updates without requiring a new program or reconfiguration.
- **Color near midpoint produces white glow**: When Color Cycle is Off and Color is at ~50%, both U and V are near 512 (neutral), producing a pure white particle with no color tint.

---

## Glossary

| Term | Definition |
|------|------------|
| **Additive glow** | A rendering technique where brightness contributions from light sources are summed at each pixel, producing brighter regions where multiple sources overlap. Flurry computes glow as brightness minus distance, producing a linear falloff from the particle center. |
| **Elliptical orbit** | A closed curve traced by a point moving under parametric sine/cosine control with a phase offset between the two components. The 8-entry offset in Flurry's LUT produces the 90Â° separation between horizontal and vertical motion that creates the ellipse. |
| **Manhattan distance** | A distance metric computed as $|dx| + |dy|$ â€” the sum of absolute differences along each axis. Named after Manhattan's grid street layout. Produces diamond-shaped iso-distance contours rather than circles. |
| **Phase accumulator** | A counter that wraps at its maximum value, used to generate a continuously advancing angle for periodic motion. Flurry's 16-bit accumulator wraps at 65536, with the upper 5 bits indexing the 32-entry sine LUT. |
| **Quarter-wave sine LUT** | A lookup table storing one quarter of a sine cycle (0 to peak), from which the full sine wave can be reconstructed through symmetry. Flurry's 32-entry table stores a half-wave (ascending and descending) used directly as both sine and cosine via phase offset. |
| **Screensaver** | A class of autonomous generative animation programs originally designed to prevent CRT phosphor burn-in, now valued as ambient visual art. Flurry belongs to this tradition alongside classics like macOS Flurry and After Dark. |
| **YUV** | A color space separating luminance (Y) from chrominance (U, V), the native pixel format in the Videomancer video pipeline. U and V are centered at 512 in the 10-bit domain; values above and below midpoint represent opposite color directions. |

---
