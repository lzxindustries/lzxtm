---
draft: true
sidebar_position: 31
slug: /instruments/videomancer/breakout
title: "Breakout"
image: /img/instruments/videomancer/breakout/breakout_hero.png
description: "Breakout is a fully playable brick-breaker arcade game implemented entirely in FPGA fabric."
---

![Breakout hero image](/img/instruments/videomancer/breakout/breakout_hero_s1.png)
*A glowing ball ricochets off a row of colorful bricks as a wide paddle slides into position at the bottom of the court*

---

## Overview

**Breakout** is a fully playable brick-breaker arcade game running inside the FPGA. A ball bounces around a rectangular court, destroying bricks arranged in a grid near the top of the screen while you slide a paddle along the bottom to keep it in play. The paddle's position and width are controlled by knobs, and a serve toggle launches the ball. Smash every brick and the grid resets for a new level; miss the ball and it reappears on the paddle after a brief pause.

The game runs in pure register logic with zero block RAM: all thirty-two bricks (eight columns by four rows), the ball, the paddle, and the court border are rendered as simple geometric hit tests against the current pixel coordinate. Ball physics use a five-zone angle model: hitting the paddle dead center sends the ball straight up, while hitting the edges launches it at progressively steeper horizontal angles. A brief background flash fires whenever a brick is destroyed, giving satisfying visual feedback.

### What's In a Name?

The name pays tribute to Atari's 1976 *Breakout*, designed by Nolan Bushnell and Steve Bristow and famously prototyped by Steve Wozniak and Steve Jobs. By recreating the brick-and-paddle mechanic inside a video synthesizer, Videomancer turns the classic reflex game into a real-time visual instrument: overlay it on any video source using the **Mix** fader for playable composited graphics.

---

## Quick Start

1. Set **Bypass** to Off and push the **Mix** fader fully clockwise to see the game.
2. Flip **Serve** from Ready to Launch (the ball fires upward from the paddle.)
3. Turn **Pad Pos** to slide the paddle and intercept the ball as it bounces back down.
4. Watch the bricks shatter row by row. When all active bricks are gone, the grid resets.

---

## Parameters

![Videomancer front panel with Breakout loaded](/img/instruments/videomancer/breakout/breakout_control_panel.png)
*Videomancer's front panel with Breakout active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Ball Spd

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |

**Ball Spd** sets how many pixels the ball travels per frame. At the minimum the ball crawls at roughly two pixels per frame: plenty of time to react. Turning clockwise increases the speed up to about nine pixels per frame, creating a frantic volley that demands quick reflexes. Because the ball moves in a straight line with fixed horizontal and vertical components, faster speeds make trajectories harder to predict off the paddle's edge zones.

---

### Knob 2 — Pad Size

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Pad Size** adjusts the paddle's width from about eighty pixels (a narrow bar that demands precise positioning) up to around three hundred and thirty-five pixels (nearly a fifth of the screen width in HD). Wider paddles are more forgiving but reduce the angular range you can impart to the ball, since the five-zone deflection model divides whatever width you've chosen into equal regions.

---

### Knob 3 — Pad Pos

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Pad Pos** slides the paddle horizontally along the bottom of the court. At minimum the paddle hugs the left wall; at maximum it rests against the right wall. The paddle is clamped so it never overlaps the four-pixel court border. This is your primary gameplay control (sweep it in real time to intercept the ball.)

---

### Knob 4 — Rows

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Rows** selects how many rows of bricks are active, from one to four. At the lowest setting only the top row of eight bricks appears, making for a quick round. Turning clockwise adds rows beneath, up to the full four-row, thirty-two-brick grid. More rows mean more targets and a longer game, but also more surface area to deflect the ball off of.

---

### Knob 5 — Court Hue

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Court Hue** sets the base color for game elements when the **Color** switch is in Hue mode. In Mono mode this knob has no visible effect. In Hue mode it tints the paddle and ball with the base hue, while each row of bricks shifts the hue further: top rows brighter and more saturated, bottom rows dimmer: creating a layered color gradient across the field.

---

### Knob 6 — Bright

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |

**Bright** controls the overall brightness of every game element. Bricks use a row-based brightness gradient: the top row receives full intensity, the second row about three-quarters, the third row half, and the bottom row one-quarter. This shading creates a natural depth cue even in Mono mode. The paddle and ball render at full pot brightness, and the border at one-quarter.

---

### Switch 7 — Serve

| Property | Value |
|----------|-------|
| Off | Ready |
| On | Launch |
| Default | Ready |

**Serve** launches the ball. When set to Ready, the ball sits on the paddle surface, tracking its horizontal position. Flip to Launch and the ball fires upward with a slight horizontal bias that alternates direction with each serve, so consecutive launches angle left and right.

:::note
After the ball exits the bottom of the screen, it reappears on the paddle after a brief half-second delay. You must return **Serve** to Ready and flip it again to re-launch.
:::

---

### Switch 8 — Walls

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Walls** toggles between side-wall bouncing and horizontal wrapping. When On, the ball bounces off the left and right borders of the court like a traditional Breakout game. When Off, the ball wraps around horizontally: exiting the right edge and re-entering from the left: creating a cylindrical playing field that adds unpredictability to the ball's trajectory.

---

### Switch 9 — Score

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Score** is mapped in the parameter configuration but has no visible effect in the current FPGA implementation. The control is reserved for a future update.

---

### Switch 10 — Color

| Property | Value |
|----------|-------|
| Off | Mono |
| On | Hue |
| Default | Mono |

**Color** selects between Mono and Hue rendering. In Mono mode, all game elements are white against a black background. In Hue mode, the paddle and ball take on a color derived from the **Court Hue** knob, bricks receive a row-dependent hue shift, and the border remains neutral. The row-based shading from the **Bright** knob still applies in Hue mode, adding a luminance gradient to the color gradient.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** switches the output between the processed game video and the unmodified input. When On, the input signal passes through unchanged regardless of the Mix position.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry input signal and the game overlay. At minimum you see only the input; at maximum you see only the game. Intermediate positions blend the two, letting you superimpose the paddle-and-ball action over live camera footage or pattern generators.

---

## Background

### The Five-Zone Paddle

Unlike simple Breakout implementations where the ball always bounces at the same angle, Invaders: sorry, Breakout: uses a five-zone deflection model. The paddle is divided into five equal horizontal regions. Hitting the far-left zone sends the ball sharply to the left (horizontal velocity −4); the inner-left zone gives a moderate leftward angle (−2); the center zone sends the ball straight up (0); and the right zones mirror the left. This model rewards precise paddle positioning and makes the game feel dynamic even though the ball only has a handful of possible trajectories.

### Shift-Based Geometry

Because the iCE40 FPGA lacks a hardware multiplier, all position calculations use bit shifts and additions. Paddle positioning multiplies the knob value by the screen width using a shift-and-subtract approximation: `pot × 1920 ≈ (pot << 11) − (pot << 7)`. Brick column and row indices use power-of-two pitches (128 pixels and 32 pixels, respectively) so that division reduces to right-shifts and modulo reduces to bit masking. This keeps the entire game within the FPGA's budget of about six hundred logic cells and zero block RAM.

### Hit Flash

When the ball destroys a brick, a four-frame ***hit flash*** brightens the entire background. The flash counter starts at four and decrements once per frame, producing a brief pulse of light that decays over roughly one-fifteenth of a second. This subtle feedback confirms the hit even when you're focused on chasing the ball, and it adds a satisfying strobe punctuation to the visual rhythm of the game.


---

## Signal Flow

### Signal Flow Notes

All game logic: paddle positioning, ball physics, brick collision, and level resets: executes once per frame at the vertical sync pulse. The ball's position updates in a single process that checks wall boundaries, paddle overlap, and brick grid membership in sequence. Brick indices are computed from the ball's position using right-shifts (division by the power-of-two pitch), and the alive state of BCD that brick is read via a constant-index for-loop to avoid variable-width array indexing, which GHDL's synthesis path does not support.

The rendering pipeline runs at the full pixel clock, testing every screen coordinate against the ball, paddle, bricks, and border. A priority chain ensures the ball and paddle always render on top of bricks, bricks on top of the border, and the hit flash lights up the background behind everything. The interpolator at the end crossfades between the delayed input and the rendered game, enabling real-time compositing.


---

## Exercises

Below are three exercises exploring Breakout as a visual performance tool.
### Exercise 1: Brick Smasher

![Brick Smasher result](/img/instruments/videomancer/breakout/breakout_ex1_s1.png)
*Brick Smasher — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A classic monochrome Breakout session (white paddle and ball against black, full grid, walls on.)

#### Key Concepts

Basic gameplay, paddle control, brick destruction

#### Steps

1. Load the settings below. Four rows of eight bricks fill the upper portion of the court.
2. Flip **Serve** to Launch. The ball fires upward and bounces off the top wall.
3. Sweep **Pad Pos** to intercept the ball. Try hitting the paddle's edge zones to steer the ball toward dense clusters of bricks.
4. Watch the hit flash pulse with each brick you destroy. Clear all thirty-two bricks and the grid respawns.
5. Experiment with **Pad Size**: a narrower paddle is harder to play but gives you sharper deflection angles.

#### Settings

| Control | Value |
|---------|-------|
| Ball Spd | 40% |
| Pad Size | 50% |
| Pad Pos | 50% |
| Rows | 100% |
| Court Hue | 50% |
| Bright | 80% |
| Serve | Launch |
| Walls | On |
| Score | Off |
| Color | Mono |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Video Overlay

![Video Overlay result](/img/instruments/videomancer/breakout/breakout_ex2_s1.png)
*Video Overlay — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

The Breakout game floating semi-transparently over a live video source (a playable overlay composited in real time.)

#### Key Concepts

Compositing, transparent game layer, performance integration

#### Steps

1. Patch a camera feed or pattern generator into the Videomancer input.
2. Set **Mix** to about 60%. The game graphics blend with the underlying video.
3. Play a round: the paddle and ball ghost over the input image, creating a layered composite.
4. Try adjusting **Bright** to balance the game elements against the video. Lower brightness lets the input dominate; higher makes the game punch through.
5. Turn **Walls** Off. Now the ball wraps horizontally, appearing to phase through the edges of the composite.

#### Settings

| Control | Value |
|---------|-------|
| Ball Spd | 35% |
| Pad Size | 50% |
| Pad Pos | 50% |
| Rows | 75% |
| Court Hue | 50% |
| Bright | 70% |
| Serve | Launch |
| Walls | Off |
| Score | Off |
| Color | Mono |
| Bypass | Off |
| Mix | 60% |

---

### Exercise 3: Speed Challenge

![Speed Challenge result](/img/instruments/videomancer/breakout/breakout_ex3_s1.png)
*Speed Challenge — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A frantic, colorful speed run where the ball moves fast, the paddle is narrow, and horizontal wrapping makes trajectories unpredictable.

#### Key Concepts

Fast gameplay, narrow paddle, no walls, hue-mode visuals

#### Steps

1. Dial in the settings below. The ball moves near maximum speed and the paddle is quite narrow.
2. Set **Color** to Hue. Notice how each row of bricks gets a different color (the top row is brightest, fading to dim at the bottom.)
3. Serve the ball and try to keep up. With **Walls** Off, the ball wraps horizontally, making it harder to predict where it will reappear.
4. Sweep **Court Hue** while playing. The entire color palette rotates, creating an evolving rainbow of destruction.
5. Try reducing **Rows** to 2 for a quicker but still visually striking session.

#### Settings

| Control | Value |
|---------|-------|
| Ball Spd | 90% |
| Pad Size | 20% |
| Pad Pos | 50% |
| Rows | 60% |
| Court Hue | 25% |
| Bright | 100% |
| Serve | Launch |
| Walls | Off |
| Score | Off |
| Color | Hue |
| Bypass | Off |
| Mix | 100% |

---
## Glossary

- **AABB**: Axis-aligned bounding box: the rectangular collision region used to test whether the ball overlaps a brick, the paddle, or a wall.

- **Deflection model**: The rule set that determines the ball's outgoing angle after hitting the paddle, here a five-zone system based on the horizontal hit position.

- **Hit flash**: A brief full-background brightness pulse triggered when a brick is destroyed, lasting four frames.

- **Horizontal wrap**: When walls are off, the ball exits one side of the screen and re-enters from the other, as if the court were wrapped into a cylinder.

- **Level reset**: When all active bricks are destroyed, the full grid of bricks respawns for a new round.

- **Pitch (brick)**: The spacing between brick columns (128 pixels) and rows (32 pixels), chosen as powers of two for shift-based arithmetic.

- **Priority mux**: The color multiplexer that decides which game element to display when multiple elements overlap at a pixel: ball and paddle take priority over bricks, bricks over the border.

- **Serve timer**: A thirty-frame countdown after the ball exits the bottom of the screen, during which the ball is hidden before reappearing on the paddle.

---
