---
draft: true
sidebar_position: 31
slug: /instruments/videomancer/breakout
title: "Breakout"
image: /img/instruments/videomancer/breakout/breakout_hero.png
description: "Breakout is a fully playable brick-breaker arcade game implemented entirely in FPGA fabric."
---

import breakout_hero from '/img/instruments/videomancer/breakout/breakout_hero.png';
import breakout_animation from '/img/instruments/videomancer/breakout/breakout_animation.gif';
import breakout_control_panel from '/img/instruments/videomancer/breakout/breakout_control_panel.png';
import breakout_exercise1_result from '/img/instruments/videomancer/breakout/breakout_exercise1_result.gif';
import breakout_exercise2_result from '/img/instruments/videomancer/breakout/breakout_exercise2_result.gif';
import breakout_exercise3_result from '/img/instruments/videomancer/breakout/breakout_exercise3_result.gif';

# Breakout

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={breakout_hero} alt="Breakout hero image"/>
*Breakout in mid-game — a 12×12 ball ricochets off a wide paddle while rows of color-banded bricks crumble from the top down, three BCD score digits glowing above the court.*
<img src={breakout_animation} alt="Breakout animated output"/>
*Breakout output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Breakout is a fully playable brick-breaker arcade game implemented entirely in FPGA fabric. A ball bounces around a bordered court, destroying bricks arranged in a 14-column by 8-row grid. The paddle is positioned by a potentiometer — hardware analog control standing in for the original game's spinner knob. When all active bricks are cleared, the grid resets for a new level while the score continues to climb. When the ball falls past the paddle, it re-serves automatically after a brief delay.

The name and gameplay are drawn directly from the 1976 Atari coin-op designed by Nolan Bushnell and Steve Bristow, famously prototyped by Steve Wozniak and Steve Jobs shortly before they founded Apple Computer. The original arcade cabinet used discrete TTL logic — no CPU, no RAM — to generate its video output. This FPGA implementation follows the same spirit: zero BRAM, approximately 800 LUTs, and a 6-clock rendering pipeline that produces a full 1080p court from pure register logic. Every frame, the physics engine updates ball position and velocity, tests for collisions against the paddle, walls, and all 112 potential brick cells, increments a BCD score counter, and checks for level completion — all within a single vertical blanking interval.

Six knobs control the gameplay variables — ball speed, paddle size, paddle position, number of active brick rows, aesthetic hue, and overall brightness — while five toggles manage serving, wall behavior, score display, color mode, and bypass. The fader provides a wet/dry mix against the input video, allowing the game to be composited over a live source. The result is a playable video synthesizer module: part instrument, part game, entirely real-time.

---

## Quick Start

1. **Start slow, speed up gradually**: Begin with Ball Spd at ~30% to learn the paddle angle zones and court geometry. Increase speed only once you are comfortable guiding the ball into brick clusters.
2. **Wide paddle for compositing, narrow for gameplay**: When using Breakout as a visual overlay in a performance context, a wide paddle keeps the game running passively with minimal intervention. For a genuine challenge, narrow the paddle and focus on precision.
3. **Use the wrap for trick shots**: With Walls Off, the ball can wrap from one side to the other, hitting bricks from unexpected angles. This is harder to control but clears edge columns more efficiently than wall bounces.

---

## Background

### The Atari Breakout Legacy

Breakout occupies a singular position in the history of both video games and personal computing. Atari's 1976 arcade cabinet was the direct successor to Pong, replacing the opposing paddle with a wall of destructible bricks and transforming a two-player competitive game into a single-player puzzle of angles and timing. The original hardware was built from approximately 44 discrete TTL integrated circuits — no microprocessor, no software. Video generation, ball physics, collision detection, and score display were all implemented as combinatorial and sequential logic gates. This Videomancer program returns to that hardware-first philosophy, implementing the entire game in FPGA fabric with no CPU in the loop, continuing the tradition of video games as pure digital circuit design.

### Paddle Collision and Angle Reflection

The heart of any Breakout implementation is the paddle collision model. The original Atari game divided the paddle into zones, each producing a different reflection angle for the ball. This FPGA version uses a 5-zone model: the extreme left edge launches the ball at a steep leftward angle, the left-center at a moderate leftward angle, the center returns a pure vertical bounce, the right-center at a moderate rightward angle, and the extreme right edge at a steep rightward angle. The zone boundaries are computed relative to the paddle center, giving the player direct analog control over ball trajectory. Combined with the continuously variable paddle width from Pot 2, this creates a rich control space — a wide paddle offers a forgiving catch area but coarser angle selection, while a narrow paddle demands precision but rewards it with tighter directional control.

### BCD Scorekeeping in Hardware

The 3-digit score display uses Binary-Coded Decimal (BCD) arithmetic — each decimal digit is stored as a 4-bit value (0–9) rather than converting between binary and decimal at display time. When the ball destroys a brick, the ones digit increments; if it reaches 10, it resets to 0 and carries into the tens digit, which in turn can carry into the hundreds digit. This cascading carry chain is the same approach used in TTL-era coin-op machines and early pinball score reels. The digits are rendered through a 5×7 dot-matrix font ROM scaled to 20×28 pixels, positioned at the top center of the court.

### Brick Grid Geometry and Alive Registers

The brick field is a 14-column by 8-row grid, yielding 112 individual brick cells tracked by a single 112-bit register vector. Each bit represents the alive/dead state of one brick. The grid uses power-of-two pitches (128 pixels horizontal, 32 pixels vertical) so that column and row indices can be computed from pixel coordinates using shifts and masks rather than division — critical for fitting the logic into the iCE40's LUT budget. Each visible brick is 124×28 pixels with 4-pixel gaps, creating a clean grid appearance. When the ball center enters a live brick cell, that bit is cleared, the score increments, and the ball's vertical velocity reverses. When all bits in the active rows read zero, the entire vector resets to all-ones for a new level.

### Court Rendering and Color Mapping

The rendering pipeline evaluates five hit-test conditions for every pixel: ball, paddle, brick, border, and score digit. Each test is a pair of signed comparisons against rectangle boundaries. Hit tests are registered for one clock cycle, then a priority color mux assigns pixel color in the next cycle. Ball and paddle share the brightest foreground color. Bricks receive a row-dependent shade — top rows are brightest, bottom rows dimmest — creating a gradient that evokes the rainbow rows of the original Atari cabinet. In Hue mode, chroma is added using the Court Hue pot to shift the U and V channels, with row index further offsetting V to produce per-row color variation. A score flash counter briefly brightens the background on each brick hit, providing momentary visual feedback.


---

## Signal Flow

Register Decode → Derived Parameters → Video Timing Generator → ... → Interpolator Mix → Output

```
Registers (10-bit pots, toggle bits, fader)
│
├── Register Decode ──────────────────────────────────────────
│   ├─ s_speed_pot     = registers_in(0)          Ball speed
│   ├─ s_padsize_pot   = registers_in(1)          Paddle width
│   ├─ s_pad_pos_pot   = registers_in(2)          Paddle H position
│   ├─ s_rows_pot      = registers_in(3)          Active brick rows
│   ├─ s_hue_pot       = registers_in(4)          Court hue offset
│   ├─ s_bright_pot    = registers_in(5)          Brightness
│   ├─ s_serve_toggle  = registers_in(6)(0)       Serve launch
│   ├─ s_walls_en      = registers_in(6)(1)       Side wall enable
│   ├─ s_score_en      = registers_in(6)(2)       Score display enable
│   ├─ s_color_mode    = registers_in(6)(3)       Mono/Hue
│   ├─ s_bypass        = registers_in(6)(4)       Bypass
│   └─ s_mix_amount    = registers_in(7)          Wet/dry mix
│
├── Derived Parameters ───────────────────────────────────────
│   ├─ s_ball_speed  = 2 + speed_pot/128          [2..9 px/frame]
│   ├─ s_paddle_w    = 80 + padsize_pot/4         [80..335 px]
│   └─ s_active_rows = clamp(2 + rows_pot/128, 8) [2..8 rows]
│
├── Video Timing Generator ───────────────────────────────────
│   └─ hsync/vsync edges → s_timing flags
│
├── Position Counters (per clk) ──────────────────────────────
│   ├─ s_h_count: 12-bit horizontal pixel counter
│   └─ s_v_count: 12-bit vertical line counter
│
├── Paddle Update (per vblank) ───────────────────────────────
│   └─ s_pad_x = pot × 1920/1024, clamped to court bounds
│
├── Ball Physics (per vblank) ────────────────────────────────
│   ├─ If inactive + serve_timer > 0: hide off-screen (delay)
│   ├─ If inactive + serve_timer = 0: sit on paddle
│   ├─ Serve trigger: ball_vy = -speed, ball_vx = ±2
│   ├─ Position update: x += vx, y += vy
│   ├─ Top wall bounce: reverse vy
│   ├─ Side walls (if enabled): reverse vx at borders
│   ├─ Side wrap (if disabled): horizontal wrap-around
│   ├─ Paddle collision: 5-zone angle model → new vx, vy
│   ├─ Brick collision: clear alive bit, reverse vy, BCD ++
│   ├─ Bottom exit: deactivate, start serve_timer
│   └─ Level complete: reset all alive bits to 1
│
├── Rendering Pipeline (per pixel) ───────────────────────────
│   ├─ Hit tests: ball, paddle, brick, border, score digit
│   ├─ Brick shade: row-based brightness gradient (top=max)
│   └─ Color mux (priority order):
│       ├─ Ball/Paddle  → bright_pot Y, optional hue UV
│       ├─ Score digit   → bright_pot Y, neutral UV
│       ├─ Brick         → row shade Y, optional row-hue UV
│       ├─ Border        → bright_pot/4 Y, neutral UV
│       └─ Background    → 0 Y (flash on hit), neutral UV
│
├── Sync & Data Delay (6-clk pipeline) ──────────────────────
│   ├─ s_sync_pipe[0..5]: 4-bit sync shift register
│   └─ s_y/u/v_delay[0..5]: pass-through video delay
│
├── Interpolator Mix (wet/dry) ──────────────────────────────
│   ├─ mix_y = lerp(delayed_input_y, game_y, mix_amount)
│   ├─ mix_u = lerp(delayed_input_u, game_u, mix_amount)
│   └─ mix_v = lerp(delayed_input_v, game_v, mix_amount)
│
└── Output ───────────────────────────────────────────────────
    ├─ Bypass off: mix result + delayed sync
    └─ Bypass on:  pass-through input
```

The physics engine and rendering pipeline are decoupled by time domain. Ball position, velocity, paddle position, brick state, and score are all updated once per frame during the vertical blanking interval. The rendering pipeline then reads this state combinatorially as it scans every pixel during the active video region. This separation means the game state is perfectly consistent across each frame — no tearing, no partial updates. The 5-zone paddle angle model is the core gameplay mechanic: the player controls trajectory not by aiming, but by choosing where on the paddle to intercept the ball, a design principle inherited directly from the original Atari cabinet.

---

## Parameter Reference

<img src={breakout_control_panel} alt="Videomancer front panel with Breakout loaded"/>
*Videomancer's front panel with Breakout active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Ball Spd
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

At low settings, the ball drifts lazily across the court, giving the player ample time to position the paddle but making each round slow. At high settings, the ball crosses the court in just a few frames, demanding fast reflexes and precise paddle placement. The speed value also determines the magnitude of the upward velocity component on serve, so faster speeds produce a more aggressive initial launch angle. Finding the right speed is a balance between challenge and playability — the sweet spot depends on how rapidly the player can manipulate the Pad Pos knob. Internally, controls the base speed at which the ball travels per frame.

---

#### Knob 2 — Pad Size
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Determines the horizontal width of the paddle in pixels. A wide paddle catches the ball easily but reduces directional control because the 5-zone angle model has wider dead zones in the center. A narrow paddle sharpens angle selection but increases the likelihood of missing the ball entirely. The paddle width is computed as a fixed base plus a fraction of the pot value, and is clamped so the paddle never extends beyond the court borders. In combination with Ball Spd, paddle size defines the fundamental difficulty curve of the game.

---

#### Knob 3 — Pad Pos
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Directly positions the paddle's horizontal center on the court. This is the player's primary gameplay control — sweeping the knob left and right moves the paddle across the full width of the 1920-pixel court. The pot value is linearly mapped to the screen width, and the resulting position is clamped so the paddle edges never overlap the court border. Because the knob is analog and continuously variable, paddle movement is perfectly smooth with no stepping or dead zones, offering a tactile control experience closer to the original arcade spinner than a digital input could provide.

---

#### Knob 4 — Rows
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the number of active brick rows in the grid, determining how many rows of 14 bricks are alive at the start of each level. Fewer rows create a shorter game with less visual density and faster level completion. More rows fill the upper portion of the court with a dense wall of targets, requiring more hits (and more time) to clear. The row count is derived from the pot value and clamped to a valid range, ensuring the brick field always displays at least a minimal wall. Increasing rows mid-game does not resurrect previously destroyed bricks — only a level reset (clearing all remaining bricks) repopulates the full grid.

---

#### Knob 5 — Court Hue
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Shifts the chrominance of all court elements when Color mode is set to Hue. The pot value directly maps to the U channel, with V derived as its complement. In Hue mode, this produces a global color wash that tints the ball, paddle, and bricks. Bricks receive an additional per-row V offset based on their row index, so the hue pot establishes the base color while each row shifts progressively away from it, creating a rainbow-banded effect reminiscent of the original Atari Breakout's colored rows. In Mono mode, this control has no visible effect — all elements render as neutral grayscale.

---

#### Knob 6 — Bright
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Controls the overall foreground brightness of the ball, paddle, score digits, and brick field. The pot value is used directly as the Y (luma) level for the ball and paddle, and as the basis for the row-dependent brick shading gradient. Top-row bricks receive the full brightness value; each subsequent row receives a diminishing fraction. The court border renders at one-quarter brightness regardless of this setting, maintaining a subtle frame around the play area. Low brightness settings create a moody, dimly lit court; high settings produce a vivid, high-contrast display.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Serve** | Ready | Launch |
| **8 — Walls** | Off | On |
| **9 — Score** | Off | On |
| **10 — Color** | Mono | Hue |
| **11 — Bypass** | Off | On |

The five toggles divide into gameplay and aesthetic functions. Serve is the primary game-control toggle — it launches the ball when flipped to Launch and can be returned to Ready after serving. Walls changes the lateral boundary behavior, fundamentally altering ball trajectories and difficulty. Score and Color are display toggles that affect visual presentation without altering gameplay mechanics. Bypass routes the input video directly to the output, disabling the game entirely.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the wet/dry mix between the synthesized game output and the delayed input video. At full wet, only the game graphics are visible — bricks, ball, paddle, and score on a black background. At full dry, the input video passes through unmodified. Intermediate positions composite the game over the source using linear interpolation, allowing the brick-breaker to be overlaid on live video footage. The mix operates independently on Y, U, and V channels through three parallel interpolator instances. This control is essential for live performance contexts where the game should appear as a translucent overlay rather than a full-screen replacement.





---

## Guided Exercises

These three exercises explore Breakout's gameplay mechanics and visual presentation. Each one highlights a different balance between difficulty, aesthetics, and compositing.

### Exercise 1: Classic Arcade Setup

<img src={breakout_exercise1_result} alt="Classic Arcade Setup result"/>
*Classic Arcade Setup — simulated result across source images.*
**What You'll Create**: Configure a faithful recreation of the original Breakout arcade experience — moderate speed, full brick rows, colored bands, walls on, and score visible.

1. **Set moderate ball speed**: Turn Ball Spd to roughly 40% for a manageable but engaging pace.
2. **Medium paddle width**: Set Pad Size to around 50% — not too forgiving, not punishing.
3. **Center the paddle**: Set Pad Pos to ~50% to start mid-court.
4. **Full brick rows**: Turn Rows to ~100% for a full 8-row wall.
5. **Enable color**: Toggle Color to Hue, then set Court Hue to ~25% for a warm red-orange base that gradients into cooler hues at lower rows.
6. **Full brightness**: Set Bright to ~75% for vivid court graphics.
7. **Enable score and walls**: Toggle Score to On and Walls to On.
8. **Launch the ball**: Flip Serve to Launch. Use Pad Pos to play through a level.

**Key concepts**: 5-zone paddle angle control, row-based brightness gradient, BCD score increments, level reset on clearing all active bricks

---

### Exercise 2: Speed Challenge with Narrow Paddle

<img src={breakout_exercise2_result} alt="Speed Challenge with Narrow Paddle result"/>
*Speed Challenge with Narrow Paddle — simulated result across source images.*
**What You'll Create**: Create a high-difficulty configuration with fast ball movement, a narrow paddle, and no side walls — testing reflexes and pot-turning precision.

1. **Maximum ball speed**: Turn Ball Spd to ~90% for rapid traversal.
2. **Narrow paddle**: Set Pad Size to ~10% — a slim target that demands accuracy.
3. **Disable side walls**: Toggle Walls to Off. The ball wraps horizontally, adding spatial confusion.
4. **Moderate rows**: Set Rows to ~60% for 5–6 active rows — enough challenge without overwhelming density.
5. **Monochrome**: Toggle Color to Mono for a stark, high-contrast display that emphasizes ball tracking.
6. **Full brightness**: Bright to ~100% for maximum visibility of the small ball.
7. **Serve and play**: Flip Serve to Launch. Survive as long as possible. Note how the wrap-around changes your paddle strategy.

**Key concepts**: Horizontal wrap versus wall bounce, narrow paddle sharpens angle zones, high speed reduces reaction time, monochrome emphasizes spatial awareness

---

### Exercise 3: Game as Video Overlay

<img src={breakout_exercise3_result} alt="Game as Video Overlay result"/>
*Game as Video Overlay — simulated result across source images.*
**What You'll Create**: Composite the Breakout game over a live video input, using the mix fader to create a translucent game overlay suitable for live performance or broadcast.

1. **Feed a video source**: Connect a camera or video player to the input. The source will show through behind the game.
2. **Set mix to ~60%**: Pull the Mix fader to roughly 60% so the game graphics are prominent but the source video remains visible.
3. **Moderate settings**: Ball Spd ~35%, Pad Size ~50%, Rows ~75%, Bright ~80%.
4. **Enable hue mode**: Toggle Color to Hue, set Court Hue to ~70% for a cool blue tint that contrasts well with typical video content.
5. **Serve and play**: Launch the ball. Observe how the brick grid, paddle, and ball composite over the source material.
6. **Adjust mix live**: Sweep the Mix fader during gameplay — notice how lowering the mix makes the game ghostly and the source dominant, while raising it makes the game solid.
7. **Try score off**: Toggle Score to Off for a cleaner overlay with fewer hard-edged elements competing with the source.

**Key concepts**: Wet/dry interpolation composites synthesis over input, hue tinting separates game layer from source, mix fader as live performance control

---


## Tips

- **Court Hue at ~25% mimics the original**: A warm red-orange base hue with the row gradient produces the closest match to the classic Atari Breakout color scheme of red, orange, yellow, and green rows.
- **Score Off for cleaner overlays**: When compositing over video, the score digits can be visually distracting. Turn Score Off for a purely geometric game layer — the score remains tracked internally and reappears when toggled back On.
- **Mix at ~40% creates ghost bricks**: A low mix setting renders the brick field as a faint grid pattern over the input video, creating an interesting lattice effect even when the game is not actively being played.
- **Serve timing matters**: The ball launches from wherever the paddle is when you flip Serve to Launch. Position the paddle first, then serve, to aim the initial trajectory toward a specific section of the brick wall.
- **Fewer rows for faster levels**: Setting Rows low (2–3 rows) creates quick levels of 28–42 bricks each. The rapid level reset creates a satisfying rhythm of destruction and renewal, especially at higher speeds.

---

## Glossary

| Term | Definition |
|------|------------|
| **Alive register** | A 112-bit std_logic_vector where each bit represents the alive (1) or destroyed (0) state of one brick in the 14×8 grid. |
| **Angle zone** | One of five regions across the paddle width that determines the horizontal velocity assigned to the ball on a paddle collision. Zones progress from steep-left to vertical to steep-right. |
| **BCD (Binary-Coded Decimal)** | A numeric encoding where each decimal digit (0–9) is stored as a separate 4-bit value, simplifying digit-by-digit display without binary-to-decimal conversion. |
| **Brick pitch** | The center-to-center spacing of bricks in the grid: 128 pixels horizontal, 32 pixels vertical. Power-of-two values enable efficient coordinate-to-index conversion via bit shifting. |
| **Chebyshev distance** | A distance metric using the maximum of absolute coordinate differences: max(|dx|, |dy|). Not used in Breakout's rectangular hit tests, which use independent axis-aligned range checks. |
| **Dot-matrix font** | A character representation where each glyph is defined as a grid of on/off pixels. Breakout uses a 5×7 font ROM for the digits 0–9, scaled 4× to 20×28 pixels. |
| **Hit test** | A per-pixel comparison that determines whether the current scan position falls within a game object's bounding rectangle (ball, paddle, brick, border, or score digit). |
| **Level reset** | The event triggered when all alive bits in the active rows are cleared. All 112 bits are set back to 1, repopulating the entire brick grid for a new level while the score continues. |
| **Score flash** | A 4-frame brightness pulse applied to the background color immediately after a brick is destroyed, providing visual feedback for successful hits. |
| **Serve timer** | A 6-bit countdown (30 frames at 60 fps = 0.5 seconds) that delays the ball's return to the paddle after it exits the bottom of the court, preventing instantaneous re-serve. |
| **Sync pipeline** | A 6-stage shift register that delays the hsync, vsync, avid, and field signals to match the rendering pipeline latency, ensuring the output video timing is correctly aligned. |
| **Vblank** | The vertical blanking interval: the period between the last visible scan line of one frame and the first visible scan line of the next. All physics and game state updates occur during vblank. |
| **Wrap mode** | The horizontal boundary behavior when Walls is Off. The ball's X position wraps modulo 1920, teleporting from one side of the court to the other without velocity change. |

---
