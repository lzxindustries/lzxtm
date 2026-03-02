---
draft: false
sidebar_position: 222
slug: /instruments/videomancer/pong
title: "Pong"
image: /img/instruments/videomancer/pong/pong_hero.png
description: "In 1972, Atari released Pong — a table tennis simulation so simple that its entire rule set fits in a single sentence: a ball bounces between two paddles, and if you miss, your opponent scores."
---

import pong_hero from '/img/instruments/videomancer/pong/pong_hero.png';
import pong_animation from '/img/instruments/videomancer/pong/pong_animation.gif';
import pong_control_panel from '/img/instruments/videomancer/pong/pong_control_panel.png';
import pong_exercise1_result from '/img/instruments/videomancer/pong/pong_exercise1_result.gif';
import pong_exercise2_result from '/img/instruments/videomancer/pong/pong_exercise2_result.gif';
import pong_exercise3_result from '/img/instruments/videomancer/pong/pong_exercise3_result.gif';

# Pong

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={pong_hero} alt="Pong hero image"/>
*Pong rendering a classic two-player court with paddles, bouncing ball, dashed center net, and 5x7 dot-matrix score display over processed video.*
<img src={pong_animation} alt="Pong animated output"/>
*Pong output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

In 1972, Atari released Pong — a table tennis simulation so simple that its entire rule set fits in a single sentence: a ball bounces between two paddles, and if you miss, your opponent scores. That simplicity made it the first commercially successful video game and the seed of an entire industry. Pong recreates the complete game on FPGA hardware, rendering every element — paddles, ball, court borders, dashed center net, and bitmap score digits — as a real-time video overlay that mixes with the input signal.

Player 1's paddle is controlled directly by Knob 3, mapping the 10-bit pot value to a vertical screen position. Player 2 can be an AI opponent whose tracking speed is controlled by Knob 4, or a second human player using the fader for manual positioning. The ball's vertical angle changes depending on where it strikes the paddle — center hits return flat, edge hits produce steep angles — reproducing the variable-angle mechanic that gave the original Pong its competitive depth. When a player scores, a brief screen flash fires and the ball re-serves after a half-second pause. Scores count to 9, then the game resets.

At full mix, Pong renders as a clean overlay on black. Reducing the mix fader blends the game court with the input video, creating compositions where the paddles and ball interact visually with the source material — a digital game literally played on top of live video.

---

## Background

### The Birth of Pong

Allan Alcorn built the original Pong as a training exercise assigned by Noel Bushnell at Atari. The entire game was implemented in discrete TTL logic — no CPU, no software, no memory. Horizontal and vertical counters generated the video signal directly, with flip-flops tracking the ball position and score. The paddles were analog potentiometers whose voltage was compared against the vertical counter to determine paddle position. Pong's design is one of the purest examples of hardware-generated video: every game element is a direct function of the raster scan position, computed in real time by combinational and sequential logic. Videomancer's FPGA implementation follows this same philosophy — the ball, paddles, net, and scores are all computed per-pixel from position counters and comparators, with no frame buffer.

### Ball Physics and Angle Control

The original Pong divided each paddle into eight segments. Hitting the ball with the paddle's center returned it horizontally; hitting near the edges sent it at steep angles. This mechanic transformed Pong from a trivial back-and-forth into a game of skill — players could aim their returns by precisely positioning their paddle. Videomancer's implementation uses a seven-zone hit model: the ball's vertical velocity is set to values from -4 to +4 pixels per frame depending on the relative position of the ball center to the paddle center. A center hit produces zero vertical velocity (pure horizontal return), while extreme edge hits produce maximum deflection.

### AI Paddle Tracking

When Player 2 is set to AI mode, the right paddle tracks the ball's vertical position using a simple proportional pursuit algorithm. Each frame, the AI computes the difference between its current position and the ball's Y coordinate, then moves toward the ball at a speed determined by the AI Skill knob (1 to 8 pixels per frame). At low skill settings, the AI paddle drifts slowly and can be beaten by fast angled returns. At high skill settings, the AI tracks nearly perfectly and is almost unbeatable. This tracking model was common in early arcade games because it uses minimal logic — just a comparison and a conditional increment.

### Score Rendering

The original Pong displayed scores using dedicated digit circuits that decoded a BCD counter into segments. Videomancer uses a 5x7 bitmap font stored as constant lookup tables — 10 digits, 7 rows of 5 bits each. During raster scan, the current pixel position is compared against each digit's bounding box, and the font ROM is indexed to determine whether the pixel is on or off. The digits are rendered at 4x scale (20x28 pixels) for visibility at 1080p resolution, positioned above the center net on each player's side.

### The Dashed Net

The center court dividing line in the original Pong was rendered as a dashed vertical stripe — a sequence of short bright segments separated by gaps. This was implemented by ANDing the horizontal center position with a modular vertical counter. Videomancer uses the same technique: a 4-pixel-wide vertical stripe at the horizontal center, with 24-pixel dashes and 16-pixel gaps controlled by a modulo operation on the vertical scan counter.


---

## Signal Flow

```
Synthesis Engine
│
├── Parameter Mapping ──────────────────────────────────────────
│   ├─ registers_in(0)  → Ball Speed (2–8 px/frame)
│   ├─ registers_in(1)  → Paddle Height (40–240 px)
│   ├─ registers_in(2)  → Player 1 Y Position
│   ├─ registers_in(3)  → AI Skill (1–8 px/frame tracking)
│   ├─ registers_in(4)  → Court Hue (chroma offset)
│   ├─ registers_in(5)  → Brightness (foreground Y level)
│   ├─ registers_in(6)  → Toggles (P2 mode, net, score, color, bypass)
│   └─ registers_in(7)  → Mix / P2 Manual Position
│
├── Physics Engine (per vsync) ─────────────────────────────────
│   ├─ 1. Paddle Positioning     (P1 pot-mapped, P2 AI or manual)
│   ├─ 2. Ball Position Update   (velocity accumulation)
│   ├─ 3. Wall Bounce            (top/bottom reflection)
│   ├─ 4. Paddle Collision       (7-zone angle determination)
│   └─ 5. Score Update           (exit detection, serve delay)
│
├── Rasterizer (per pixel) ─────────────────────────────────────
│   ├─ 6. Ball Hit Test          (16×16 square)
│   ├─ 7. Paddle Hit Tests       (left at x=80, right at x=1824)
│   ├─ 8. Net Hit Test           (center dashed line)
│   ├─ 9. Border Hit Test        (4-pixel court border)
│   ├─ 10. Score Digit Lookup    (5×7 font ROM at 4× scale)
│   └─ 11. Color Mux             (priority: objects > net > border > bg)
│
├── Output Stage ───────────────────────────────────────────────
│   └─ 12. Interpolator Mix      (3× interpolator_u wet/dry)
│
├── Sync Pipeline ──────────────────────────────────────────────
│   └─ 6-clock shift register (hsync, vsync, avid, field)
│
└── Bypass ─────────────────────────────────────────────────────
    └─ Select processed or input signal
```

The physics engine and rasterizer operate on different time scales. The physics engine updates once per vertical sync (60 Hz at 1080p30), stepping ball and paddle positions using signed velocity accumulators. The rasterizer runs at pixel rate (74.25 MHz), testing every pixel against the positions computed by the physics engine. This two-rate architecture mirrors the original TTL Pong hardware, where game logic was clocked by the vertical retrace and video rendering was driven by the horizontal and vertical counters. The color mux applies a strict priority: foreground objects (ball, paddles, score digits) at full brightness, the net at half brightness, borders at quarter brightness, and the background at black (with a brief flash effect after a score). Foreground color is either monochrome white or tinted by the Court Hue pot.

---

## Parameter Reference

<img src={pong_control_panel} alt="Videomancer front panel with Pong loaded"/>
*Videomancer's front panel with Pong active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Ball Spd
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Controls the ball speed. The 10-bit register is divided by 128 and offset by 2 to produce a velocity magnitude of 2 to 8 pixels per frame. At low settings the ball drifts slowly across the court, giving both players time to position. At high settings the ball crosses the court in under a second, demanding fast reflexes. The serve velocity uses this same speed value, so higher settings produce faster serves.

---

#### Knob 2 — Pad Size
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the paddle height for both players. The register is divided by 4 and offset by 40 to give a range of 40 to 295 pixels — from a thin sliver covering less than 4% of the screen to a wide bar covering over 27%. Larger paddles make the game easier; smaller paddles demand precision. Both paddles always share the same height, keeping the game fair.

---

#### Knob 3 — P1 Pos
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Controls Player 1's vertical position directly. The pot value is mapped linearly across the full 1080-pixel vertical range, clamped so the paddle stays within the court borders. This is the primary gameplay control for Player 1 — sweep the knob to move the left paddle up and down. The response is immediate (updated every vsync), with no smoothing or inertia.

---

#### Knob 4 — AI Skill
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the AI opponent's tracking speed when Player 2 is in AI mode. The register is divided by 128 and offset by 1 to give a speed of 1 to 8 pixels per frame. At 1 pixel/frame, the AI paddle drifts slowly and misses fast angled returns. At 8 pixels/frame, the AI tracks the ball almost perfectly. This control has no effect when P2 Mode is set to Manual.

---

#### Knob 5 — Court Hue
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Sets the chroma values for foreground elements when Color mode is set to Hue. The pot value is used directly as the U channel, and its complement (1023 minus the pot) as the V channel. Sweeping this control rotates the hue of the ball, paddles, and score digits through the YUV color wheel. In Mono mode this control has no visible effect — all foreground elements render as achromatic white.

---

#### Knob 6 — Bright
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Sets the luminance level of all foreground objects — ball, paddles, score digits, net, and border. The pot value is used directly as the Y channel for foreground elements. At full clockwise, objects render at maximum brightness. Reducing the control dims all game elements uniformly, allowing them to blend more subtly with the input video when the mix is reduced.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — P2 Mode** | AI | Manual |
| **8 — Net** | Off | On |
| **9 — Score** | Off | On |
| **10 — Color** | Mono | Hue |
| **11 — Bypass** | Off | On |

The five toggles control independent game and rendering features. P2 Mode switches between AI and human control of the right paddle. Net and Score independently show or hide the center court divider and the score digits. Color enables chroma tinting of foreground elements. Bypass routes the input signal past all game rendering.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Wet/dry mix crossfade between the unprocessed input video and the game overlay. Three parallel interpolator_u instances blend Y, U, and V channels independently. At 100% the output is pure game overlay on black. At 50% the game elements are semi-transparent over the input video. At 0% the output is pure dry input. Note: when P2 Mode is set to Manual, this fader controls Player 2's paddle position instead of the mix level.

---

## Guided Exercises

These exercises progress from basic Pong gameplay to creative video overlay techniques, exploring the interaction between game rendering and the input video signal.

### Exercise 1: Classic Pong Match

<img src={pong_exercise1_result} alt="Classic Pong Match result"/>
*Classic Pong Match — simulated result across source images.*
**Objective**: Play a round of Pong against the AI with default court rendering.

1. Set Ball Speed to about 40% for a moderate ball pace.
2. Set Paddle Size to about 50% for medium paddles.
3. Turn P1 Position to 50% to center the left paddle.
4. Set AI Skill to about 50% for a fair opponent.
5. Confirm Net and Score are both On.
6. Play by sweeping P1 Position up and down to return the ball.
7. Observe how the ball angle changes depending on where it hits the paddle.
8. Watch the score increment when the ball exits the court.

**Key concepts**: Ball angle is determined by paddle hit position, AI tracking speed affects difficulty, scores reset after reaching 9

---

### Exercise 2: Neon Court Overlay

<img src={pong_exercise2_result} alt="Neon Court Overlay result"/>
*Neon Court Overlay — simulated result across source images.*
**Objective**: Blend the Pong court semi-transparently over live video with colored game elements.

1. Set Mix to about 60% to let the source video show through.
2. Enable Color mode (Hue) for tinted game elements.
3. Sweep Court Hue to find a complementary color for the source material.
4. Set Brightness to about 90% for vivid game elements.
5. Reduce Paddle Size to about 30% for a more challenging game aspect.
6. Increase Ball Speed to about 60% for energetic gameplay.
7. Observe how the ball and paddles appear to float over the source video.

**Key concepts**: Mix fader controls overlay transparency, Color mode tints all foreground elements, brightness and mix interact to control overlay visibility

---

### Exercise 3: Two-Player Head-to-Head

<img src={pong_exercise3_result} alt="Two-Player Head-to-Head result"/>
*Two-Player Head-to-Head — simulated result across source images.*
**Objective**: Play a two-player match using the pot and fader as separate paddle controllers.

1. Switch P2 Mode to Manual — the fader now controls the right paddle.
2. Set Ball Speed to about 35% for a fair match.
3. Set Paddle Size to about 40% for moderately challenging paddles.
4. Player 1 uses Knob 3 (P1 Pos) to control the left paddle.
5. Player 2 uses the Fader to control the right paddle.
6. Note that the fader no longer controls mix — output is full wet.
7. Play to 9 and observe the score reset.

**Key concepts**: Manual mode repurposes the fader for P2 control, both paddle controls can map to external CV for automated play, score resets at 9

---


## Tips

- **Edge hits are the key to winning**: Hit the ball with the top or bottom edge of your paddle to send steep angled returns that the AI (or your opponent) cannot reach.
- **AI Skill is the difficulty knob**: Low skill produces a beatable AI; high skill produces an almost unbeatable opponent. Find the sweet spot for your reflexes.
- **Manual mode for two players**: Switch P2 Mode to Manual and hand the fader to a friend for head-to-head play.
- **Mix for overlay compositing**: Lower the mix fader to blend the Pong court semi-transparently over live video, creating a playable overlay.
- **Color mode for style**: Enable Hue mode and sweep the Court Hue knob for neon-colored game elements that complement your source video.
- **Feedback routing**: Send Pong's output back into the input for recursive game-within-game visual feedback loops.
- **Bypass preserves game state**: Toggling Bypass hides the game overlay but does not pause the simulation — scores and ball position continue updating internally.

---

## Glossary

| Term | Definition |
|------|------------|
| **AI Tracking** | A simple proportional pursuit algorithm where the AI paddle moves toward the ball at a fixed pixel-per-frame speed each vsync. |
| **Bitmap Font** | A typeface stored as a grid of on/off pixel values rather than vector outlines; Pong uses a 5x7 bitmap for each digit. |
| **BT.601** | ITU-R BT.601 color space standard defining the YUV encoding used throughout the Videomancer video pipeline. |
| **FPGA** | Field-Programmable Gate Array; a reconfigurable integrated circuit that executes the video processing pipeline. |
| **Hit Zone** | One of seven vertical segments of the paddle used to determine the ball's return angle after a collision. |
| **Interpolator** | A hardware mixing stage that blends two values by a fractional amount; used for the wet/dry mix fader. |
| **Pipeline** | A series of sequential processing stages where each stage's output feeds the next stage's input on each clock cycle. |
| **Raster Scan** | The process of drawing a video frame line by line from top to bottom, left to right, at a fixed pixel clock rate. |
| **Serve** | The act of launching the ball from the center of the court after a point is scored, directed toward the scoring player's side. |
| **TTL Logic** | Transistor-Transistor Logic; the discrete integrated circuit technology used to build the original Pong hardware without a CPU. |
| **Vsync** | Vertical synchronization pulse marking the start of a new video frame; used as the game physics update clock. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
