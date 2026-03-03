---
draft: true
sidebar_position: 147
slug: /instruments/videomancer/invaders
title: "Invaders"
image: /img/instruments/videomancer/invaders/invaders_hero.png
description: "Space Invaders, released by Taito in 1978, is arguably the most important arcade game ever made."
---

import invaders_hero from '/img/instruments/videomancer/invaders/invaders_hero.png';
import invaders_animation from '/img/instruments/videomancer/invaders/invaders_animation.gif';
import invaders_control_panel from '/img/instruments/videomancer/invaders/invaders_control_panel.png';
import invaders_exercise1_result from '/img/instruments/videomancer/invaders/invaders_exercise1_result.gif';
import invaders_exercise2_result from '/img/instruments/videomancer/invaders/invaders_exercise2_result.gif';
import invaders_exercise3_result from '/img/instruments/videomancer/invaders/invaders_exercise3_result.gif';

# Invaders

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={invaders_hero} alt="Invaders hero image"/>
*Invaders rendering a 5x11 alien grid descending toward a player ship with shields and score display, evoking classic arcade video synthesis.*
<img src={invaders_animation} alt="Invaders animated output"/>
*Invaders output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Space Invaders, released by Taito in 1978, is arguably the most important arcade game ever made. Its core mechanic — a grid of aliens marching horizontally and descending toward a lone defender — created the template for the shoot-em-up genre and single-handedly launched the golden age of arcade games. Videomancer's Invaders program implements this iconic gameplay entirely in FPGA logic: a 5x11 grid of 55 aliens, a player-controlled ship, upward-firing bullets, downward-firing alien projectiles, four destructible shields, and a three-digit BCD score — all rendered without a frame buffer or CPU.

The player ship position is controlled by Knob 1, providing smooth analog positioning across the bottom of the screen. Toggle 7 (Fire) triggers a bullet launch on its rising edge. Aliens march horizontally as a block, stepping down one row each time the formation reaches a screen edge. The alien speed (Knob 2) controls the march pace, and the fire rate (Knob 3) determines how frequently aliens shoot downward. Knob 4 selects the number of shield blocks (0-3), providing a discrete difficulty setting.

Each destroyed alien increments the score and clears its bit in a 55-bit alive register. When all aliens are destroyed, the game pauses briefly and resets with a fresh wave. If any alien reaches the ship's vertical position, the game also resets. At full mix, the Invaders display renders against black. Reducing the mix fader blends the game with input video, creating an arcade overlay on live footage.

---

## Background

### The 1978 Revolution

Tomohiro Nishikado designed Space Invaders during 1977-1978, implementing the game on custom hardware based on the Intel 8080 processor. The game was so phenomenally popular in Japan that it allegedly caused a nationwide shortage of 100-yen coins. Its impact on Western culture was equally profound — it was the first game to track and display a high score, the first to use a continuous background soundtrack (the iconic four-note descending march), and the first to demonstrate that video games could be a mass-market entertainment medium.

### Block Movement and Descending Threat

The original Space Invaders used a clever trick: aliens moved one at a time in sequence, creating the illusion of synchronized block movement while requiring only a single sprite update per frame. Videomancer's FPGA implementation takes the opposite approach — all aliens share a common block offset that advances each tick, so the entire formation moves simultaneously. The march direction reverses and the formation drops one row when any live alien reaches the screen boundary. This descent mechanic creates increasing tension as the aliens approach the ship's position.

### Sprite-Based Rendering

Unlike grid-based games, Invaders uses sprite rendering: each alien is an 8x8 pixel bitmap, and the player ship is a 16x8 pixel bitmap. The rasterizer checks each pixel against all potentially visible sprites — the alien grid, the player ship, active bullets, and shield blocks. Priority ordering determines which sprite wins when they overlap. This per-pixel sprite test is computationally straightforward on FPGA hardware, where all comparisons execute in parallel within a single clock cycle.

### Shield Destruction

The original Space Invaders featured four shield bunkers that could absorb both player and alien bullets, gradually eroding with each hit. Videomancer implements simplified shields as rectangular blocks that disappear entirely when hit by any bullet. The Shields knob (steps_4 mode) selects 0-3 shields, providing a discrete difficulty control: 3 shields offers maximum protection, 0 shields leaves the player fully exposed.

### LFSR Alien Fire

Aliens fire downward at pseudo-random intervals determined by a 16-bit LFSR and the Fire Rate knob. Each frame, the LFSR advances, and if the least significant bits fall below the fire rate threshold, the lowest alive alien in a randomly selected column fires a bullet downward. This creates an organic, unpredictable barrage that increases in danger as more aliens are active — a challenging inversion of the original game's increasing speed mechanic.


---

## Signal Flow

```
Synthesis Engine
|
+-- Parameter Mapping ------------------------------------------------
|   +- registers_in(0)  -> Ship Position (horizontal)
|   +- registers_in(1)  -> Alien Speed (march interval)
|   +- registers_in(2)  -> Fire Rate (alien bullet frequency)
|   +- registers_in(3)  -> Shields (0-3 shield blocks)
|   +- registers_in(4)  -> Court Hue (chroma offset)
|   +- registers_in(5)  -> Brightness (foreground Y level)
|   +- registers_in(6)  -> Toggles (fire, border, score, color, bypass)
|   +- registers_in(7)  -> Mix
|
+-- Game Logic (per vsync) -------------------------------------------
|   +- 1. Ship Position   (pot → pixel X coordinate)
|   +- 2. Fire Edge       (rising edge on toggle 7 → spawn bullet)
|   +- 3. Bullet Update   (advance player bullet upward by step size)
|   +- 4. Alien March     (move block offset, reverse + descend at edges)
|   +- 5. Alien Fire      (LFSR-driven downward bullet spawn)
|   +- 6. Collision Detect (bullet vs alien grid → clear alive bit + score)
|   +- 7. Shield Collision (bullet vs shield → destroy shield)
|   +- 8. Ship Collision   (alien bullet vs ship → game reset)
|   +- 9. Wave Reset       (all aliens dead → reset alive register)
|
+-- Rasterizer (per pixel) -------------------------------------------
|   +- 10. Alien Sprite    (8x8 bitmap per grid cell, alive check)
|   +- 11. Ship Sprite     (16x8 bitmap at ship X, bottom of screen)
|   +- 12. Bullet Render   (2x6 pixel rectangles for player + alien bullets)
|   +- 13. Shield Render   (rectangular blocks, 4 positions)
|   +- 14. Border Render   (optional screen-edge border)
|   +- 15. Score Digits    (5x7 font at 4x scale, 3-digit BCD)
|   +- 16. Color Mux       (priority: bullet > ship > alien > shield > border > score > bg)
|
+-- Output Stage ----------------------------------------------------
|   +- 17. Interpolator Mix  (3x interpolator_u wet/dry)
|
+-- Sync Pipeline ---------------------------------------------------
|   +- 6-clock shift register (hsync, vsync, avid, field)
|
+-- Bypass ----------------------------------------------------------
    +- Select processed or input signal
```

The game logic pipeline processes all collision detection during vsync blanking. Player bullet position is stored as a (X, Y) coordinate pair; alien bullet position is similarly tracked. The alien grid uses a 55-bit alive register where each bit corresponds to one alien in the 5x11 grid. When a player bullet overlaps an alien's bounding box and that alien's bit is set, the bit is cleared and the score increments. When all 55 bits are clear, a new wave resets the alive register to all ones and repositions the formation at the top.

The rasterizer evaluates each pixel against all sprite types in priority order. Alien sprites use a static 8x8 bitmap ROM — the classic two-frame animation of the original game is simplified to a single sprite pattern. The player ship uses a 16x8 bitmap positioned at the X coordinate from Knob 1. Bullets are simple 2x6 pixel rectangles that move vertically each frame.

---

## Parameter Reference

<img src={invaders_control_panel} alt="Videomancer front panel with Invaders loaded"/>
*Videomancer's front panel with Invaders active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Ship Pos
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Ship Pos controls the horizontal position of the player ship at the bottom of the screen. The full pot range maps to the playable screen width, with clamping to prevent the ship from exiting the visible area. This provides smooth, proportional ship control similar to the original arcade game's analog paddle. The ship position updates every frame, so sweeping the knob produces fluid lateral movement.

---

#### Knob 2 — Alien Spd
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |
| Suffix | % |

Alien Spd controls the march speed of the alien formation. At low values, aliens move very slowly, giving the player ample time to aim and fire. At high values, the formation races across the screen, descending rapidly and leaving little time to react. The speed pot maps inversely to the frame count between march steps — higher pot values produce shorter intervals and faster alien movement.

---

#### Knob 3 — Fire Rate
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Fire Rate controls how frequently aliens fire downward bullets. At low values, alien fire is rare and the player faces minimal return fire. At high values, aliens shoot frequently, creating a dense barrage of descending projectiles. The fire rate interacts with the number of alive aliens — more active columns mean more potential shooters per LFSR trigger, creating organic difficulty scaling.

---

#### Knob 4 — Shields
| Property | Value |
|----------|-------|
| Range | 0 – 4 |
| Default | 3 |

Shields selects the number of shield blocks present on the field (0-3), using the steps_4 control mode for discrete selection. Zero shields leaves the player fully exposed to alien fire. Each additional shield provides a destructible barrier that absorbs one hit from either a player bullet or an alien bullet (player bullets should avoid hitting shields). Shields are positioned evenly across the screen above the ship's patrol zone.

---

#### Knob 5 — Court Hue
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |
| Suffix | % |

Court Hue shifts the chroma values applied to all game elements when Color mode is active. Sweeping this knob rotates through the YUV color wheel, changing aliens, ship, bullets, and shields collectively. Different hue values evoke different arcade aesthetics — green for classic monochrome CRT, blue for ice-themed variants, orange for warm retro tones. In Mono mode, this knob has no visible effect.

---

#### Knob 6 — Bright
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |
| Suffix | % |

Bright controls the luminance (Y channel) of all foreground game elements. Aliens, ship, bullets, shields, score digits, and border all reference this brightness value at various fractions. Higher brightness produces vivid, high-contrast sprites against the dark background. Lower brightness creates a dim, atmospheric display that blends more subtly when mixed with input video.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Fire** | Off | On |
| **8 — Border** | Off | On |
| **9 — Score** | Off | On |
| **10 — Color** | Mono | Hue |
| **11 — Bypass** | Off | On |

The five toggles partition into gameplay action (Fire), display options (Border, Score, Color), and signal routing (Bypass). Fire is a momentary action toggle — the game detects its rising edge to fire a bullet. Border, Score, and Color are persistent display modes. Bypass routes the input signal past the game overlay while the simulation continues running internally.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Mix controls the wet/dry blend between the game overlay and the input video. At full mix, only the Invaders game is visible against black. Reducing mix fades in the input video behind the game elements, creating an arcade overlay on live footage. At zero mix, the game is invisible and only the input signal passes through. The mix engages three interpolator_u instances for Y, U, and V channels independently.

---

## Guided Exercises

These exercises explore the core shoot-em-up mechanics, the interaction between fire rate, alien speed, and shield configuration, and the use of the game as a retro-styled video overlay.

### Exercise 1: First Defence

<img src={invaders_exercise1_result} alt="First Defence result"/>
*First Defence — simulated result across source images.*
**Objective**: Destroy a complete wave of 55 aliens using the ship position knob and fire toggle.

1. Set Ship Pos to center (~50%).
2. Set Alien Spd to about 20% for slow alien march.
3. Set Fire Rate to about 15% for minimal return fire.
4. Set Shields to 3 for full protection.
5. Enable Score to track kills.
6. Toggle Fire (Off→On) to launch a bullet upward.
7. Aim by adjusting Ship Pos before each shot.
8. Wait for the bullet to resolve (hit or miss) before firing again.
9. Clear all 55 aliens to see the wave reset.

**Key concepts**: Single-bullet-at-a-time, ship positioning, alien alive register, wave reset, score tracking

---

### Exercise 2: Speed Run

<img src={invaders_exercise2_result} alt="Speed Run result"/>
*Speed Run — simulated result across source images.*
**Objective**: Survive a fast alien formation with high return fire and no shields.

1. Set Alien Spd to about 65% for an aggressive march speed.
2. Set Fire Rate to about 60% for frequent alien bullets.
3. Set Shields to 0 for maximum danger.
4. Position the ship using Knob 1 and fire rapidly, toggling Fire after each bullet resolves.
5. Watch for descending alien bullets — move the ship to dodge.
6. The formation descends faster and reaches the ship sooner at high speed.
7. Try to clear as many aliens as possible before the wave reaches you.

**Key concepts**: High-speed march, alien bullet dodging, no-shield exposure, descent pressure, rapid fire discipline

---

### Exercise 3: Arcade Overlay

<img src={invaders_exercise3_result} alt="Arcade Overlay result"/>
*Arcade Overlay — simulated result across source images.*
**Objective**: Blend the Invaders game over input video at partial mix for a retro arcade overlay composition.

1. Set Mix to about 55% to blend game and input video.
2. Switch Color to Hue and sweep Court Hue to find a retro-styled color (try greenish ~30% for classic CRT look).
3. Set Bright to about 90% for vivid sprites visible through the mix.
4. Set Alien Spd to about 30% for smooth visual march.
5. Set Fire Rate to about 25% for occasional alien bullets adding visual interest.
6. Enable Score for a persistent score counter overlay.
7. Let the game play as a visual element, firing occasionally to add bullet animation.

**Key concepts**: Partial mix compositing, retro CRT color, overlay transparency, game as visual element

---


## Tips

- **Lead your shots**: Since only one bullet can be active at a time, position the ship under target aliens before firing. Missed shots waste time while the bullet travels off-screen.
- **Work the edges**: Destroy aliens on the formation edges first to slow the descent rate — fewer edge aliens means more horizontal travel before reversal and descent.
- **Shield strategy**: Shields protect from alien bullets but block your own shots too. Position your ship offset from shields to maintain a clear firing lane while keeping shields between you and alien fire.
- **Speed is the threat**: Alien speed determines how quickly the formation descends. At high speeds, you have very few rounds to thin the formation before it reaches you.
- **Fire rate awareness**: High alien fire rate creates a dense curtain of descending bullets. Keep the ship moving laterally to dodge between alien shots.
- **Mix for retro aesthetics**: Reduce Mix to blend the game over CRT-scanned video input for an authentic retro arcade-on-TV look.
- **Color for classic feel**: Set Color to Hue with Court Hue at ~30% (greenish) to evoke the classic green-phosphor CRT aesthetic of early arcade monitors.
- **Bypass for dramatic reveals**: Hide the game with Bypass during a video performance, then reveal the active game state at a dramatic moment.

---

## Glossary

| Term | Definition |
|------|------------|
| **Alive Register** | A 55-bit register where each bit represents one alien in the 5x11 grid. A set bit means the alien is alive and rendered; cleared means destroyed. |
| **BCD** | Binary-Coded Decimal; each decimal digit is stored in 4 bits, used for the three-digit score display. |
| **Formation** | The 5x11 alien grid that moves as a unified block, sharing horizontal and vertical offsets. |
| **LFSR** | Linear Feedback Shift Register; generates pseudo-random values used to determine which alien fires and when. |
| **March** | The horizontal movement of the alien formation. The formation reverses direction and descends one row at each screen edge. |
| **Rising Edge** | The transition from Off to On on the Fire toggle, used as the trigger to launch a player bullet. |
| **Shield** | A destructible rectangular barrier that absorbs one bullet (player or alien), providing temporary protection. |
| **Sprite** | A small bitmap image (8x8 for aliens, 16x8 for the ship) rendered at a specific screen position by pixel comparison. |
| **Vsync** | Vertical synchronization pulse marking the start of a new video frame, used as the game tick clock. |
| **Wave** | A complete set of 55 aliens. When all are destroyed, a new wave spawns at the top of the screen. |
| **YUV** | A color encoding separating luminance (Y) from chrominance (U, V), used throughout the Videomancer video pipeline. |

---
