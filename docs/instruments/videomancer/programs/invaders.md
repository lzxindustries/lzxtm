---
draft: true
sidebar_position: 146
slug: /instruments/videomancer/invaders
title: "Invaders"
image: /img/instruments/videomancer/invaders/invaders_hero.png
description: "Space Invaders, released by Taito in 1978, is arguably the most important arcade game ever made."
---

![Invaders hero image](/img/instruments/videomancer/invaders/invaders_hero_s1.png)
*A formation of alien invaders descends through the darkness as a lone triangular cannon fires upward from behind a row of protective bunkers*

---

## Overview

**Invaders** is a fully playable Space Invaders arcade game running entirely inside the FPGA. A formation of fifty-five aliens: arranged in an eleven-column, five-row grid: marches back and forth across the screen, stepping downward each time the block reaches a wall. You control a triangular cannon at the bottom of the frame, sliding it left and right with a knob and firing upward with a toggle switch. Destroy every alien in the wave and they respawn for another round; let them reach your firing line and the game resets.

The entire game: movement logic, collision detection, score tracking, and font rendering: runs in pure combinational and register logic with zero block RAM. A 5×7 bitmap font ROM embedded in the VHDL draws a three-digit score counter in the upper-left corner, scaled four times for visibility. Four protective shield bunkers can absorb incoming alien fire, though each shield is destroyed after a single hit. The aliens choose their attack column at random using a sixteen-bit LFSR, keeping every round unpredictable.

### What's In a Name?

The name is a direct homage to Taito's 1978 *Space Invaders*, one of the most influential arcade games ever made. By recreating its core mechanics inside a video synthesizer, Videomancer turns the classic defend-the-earth scenario into a live-performance visual instrument: you can overlay the game on any video source using the **Mix** fader, compositing retro arcade graphics onto your signal chain in real time.

---

## Quick Start

1. Set **Bypass** to Off and push the **Mix** fader fully clockwise so the game fills the screen.
2. Turn **Ship Pos** to slide your cannon left and right (find a column of aliens and line up your shot.)
3. Flip the **Fire** toggle from Ready to Launch. A small white bullet streaks upward; if it hits an alien, that invader disappears and your score increments.
4. Watch the upper-left corner: the three-digit score counter tracks your kills. Keep firing and dodging the aliens' return fire until the formation is wiped out.

---

## Parameters

![Videomancer front panel with Invaders loaded](/img/instruments/videomancer/invaders/invaders_control_panel.png)
*Videomancer's front panel with Invaders active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Knob 1 — Ship Pos

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Ship Pos** slides your cannon horizontally across the bottom of the screen. At the minimum position the ship hugs the left wall; at maximum it sits against the right wall. The cannon is a sixty-four-pixel-wide triangle whose apex points upward: the classic defender silhouette. Because aiming is entirely positional (bullets always fly straight up), precise knob control is essential for threading shots into tight columns of surviving aliens.

---

### Knob 2 — Alien Spd

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 38% |

**Alien Spd** sets how frequently the alien formation takes a step. At the lowest setting the block drifts lazily, with nearly a full second between moves. Turning clockwise tightens the interval until the aliens march rapidly across the screen. Each step covers eight pixels horizontally; when the formation reaches the edge of the court it reverses direction and drops one row closer to your ship. Faster aliens give you less time to aim but create a more frantic, satisfying rhythm.

:::tip
Start with **Alien Spd** near the low end while you learn the controls. Once you're comfortable threading shots into the grid, crank it up for a real challenge.
:::

---

### Knob 3 — Fire Rate

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Fire Rate** controls how often the aliens shoot back. At the lowest setting the aliens lob a bullet downward roughly every ninety frames: about one and a half seconds. Turning clockwise shortens the interval, making the aliens increasingly aggressive. Only one alien bullet can exist on screen at a time, so higher fire rates mainly reduce the pause between volleys rather than flooding the screen.

---

### Knob 4 — Shields

| Property | Value |
|----------|-------|
| Range | 0 – 4 |
| Default | 3 |

**Shields** selects how many protective bunkers appear between you and the alien formation. At the lowest notch, no shields appear and you're fully exposed. Stepping through the positions adds up to three shield bunkers spaced evenly across the court. Each shield is eighty pixels wide and forty pixels tall: large enough to absorb a single alien bullet, after which it vanishes entirely. Shields are restored whenever you clear a full wave of aliens.

---

### Knob 5 — Court Hue

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 50% |

**Court Hue** sets the base color for game elements when the **Color** switch is set to Hue mode. In Mono mode this knob has no visible effect. In Hue mode it controls the starting hue applied to the top row of aliens; each row below shifts the color further, creating a rainbow gradient across the formation. The ship, alien bullets, and shields all receive their own fixed hue offsets relative to this base.

---

### Knob 6 — Bright

| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 75% |

**Bright** sets the overall brightness of every game element: ship, aliens, bullets, shields, score, and border. At minimum everything fades to black; at maximum each element reaches full intensity. Shields render at half brightness and the border at one-eighth brightness relative to this knob, maintaining a natural visual hierarchy even as you raise or lower the overall level.

---

### Switch 7 — Fire

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Fire** is your trigger. Flipping from Ready to Launch fires one bullet straight up from the center of your ship. You can only have one bullet on screen at a time: if you miss, you must wait for it to leave the top of the frame before firing again. Each shot travels eight pixels per frame, reaching the top row of aliens in roughly a quarter-second at HD rates.

:::note
The fire toggle is ***edge-detected***: the bullet launches on the transition from Ready to Launch, not while the toggle is held. Flip it back to Ready to rearm.
:::

---

### Switch 8 — Border

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Border** toggles a thin four-pixel frame around the edges of the court. When On, a dim white border outlines the play area, helping define the edges of the game field against a black background. When Off the border disappears, letting the action bleed to the very edges of the frame (useful when overlaying the game onto video.)

---

### Switch 9 — Score

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | On |

**Score** toggles the three-digit score counter in the upper-left corner. When On, each alien you destroy increments the counter, rendered in a scaled 5×7 bitmap font. When Off the score display disappears, giving you a cleaner visual if you're using the game purely as a graphic source. The score still tracks internally and resets when the game restarts.

---

### Switch 10 — Color

| Property | Value |
|----------|-------|
| Off | Mono |
| On | Hue |
| Default | Mono |

**Color** selects between Mono and Hue rendering. In Mono mode, every game element is white against a black background: a faithful recreation of the original arcade's monochrome display. In Hue mode, each row of aliens gets a different color derived from the **Court Hue** knob. The player ship glows warm, alien bullets glow cool, and shields take on a muted midtone, giving the game a vivid rainbow-arcade look.

---

### Switch 11 — Bypass

| Property | Value |
|----------|-------|
| Off | Off |
| On | On |
| Default | Off |

**Bypass** switches the output between the processed game video and the unmodified input. When On, the input signal passes through unchanged regardless of the Mix fader position.

---

### Fader 12 — Mix

| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |

**Mix** crossfades between the dry input signal and the game overlay. At minimum you see only the input; at maximum you see only the game. Intermediate positions blend the two, letting you superimpose the alien formation and bullets over live camera footage, pattern generators, or any other source in your signal chain.

:::tip
Try the "Arcade Overlay" preset: it sets Mix to about 60% so the game graphics float transparently over your input video, creating a playable heads-up display.
:::

---

## Background

### The Original Invaders

Taito's *Space Invaders* (1978) was among the first video games to feature destructible enemies, an escalating difficulty curve, and a persistent high score. Its simple mechanics: move, shoot, dodge: proved endlessly compelling. The hardware used a bitmapped framebuffer (a luxury at the time) to render rows of alien sprites that advanced toward the player. Invaders recreates this formula inside a Videomancer FPGA program, replacing the framebuffer with pure register-based rendering.

### Shift-Based Game Arithmetic

Because the iCE40 FPGA has no hardware multiplier or divider, all game math uses bit shifts and additions. Ship positioning multiplies the knob value by the screen width using a shift-and-subtract approximation of `× 1856`. Alien speed converts the pot into a frame-count interval via a right-shift. Score rendering uses a hardcoded 5×7 font ROM: ten characters × eight rows × five columns: with integer division by the scale factor to select the correct pixel. Even the LFSR that picks the alien firing column avoids multiplication, using a four-tap XOR polynomial (`x^16 + x^14 + x^13 + x^11 + 1`) to generate pseudorandom selection.

### Resolution Awareness

Invaders uses the Videomancer ABI's resolution package to adapt its geometry to whatever video standard is active. The ship's vertical position, court boundaries, and alien start coordinates all derive from runtime resolution lookups, so the game plays correctly in both SD and HD modes. The HD clock divisor is set to 2, slowing the pixel clock by half in HD mode to keep the game logic running at a manageable rate.


---

## Signal Flow

### Signal Flow Notes

The game logic updates once per frame at the vertical sync pulse, making all movement, collision detection, and scoring run at the video field rate. The rendering pipeline then paints every pixel at full pixel-clock speed by testing each screen coordinate against the current positions of the ship, aliens, bullets, shields, border, and score glyphs. A priority chain in the color mux ensures that the score always renders on top, followed by the ship, aliens, and bullets in descending order (this avoids visual artifacts when game elements overlap.)

The interpolator stage at the end crossfades between the delayed input video and the rendered game output based on the Mix fader, letting the game serve as either a standalone video source or a transparent overlay on existing footage.


---

## Exercises

Below are three exercises exploring Invaders as a video performance tool. Each exercise specifies all twelve controls to reproduce the starting configuration.
### Exercise 1: Solo Defense

![Solo Defense result](/img/instruments/videomancer/invaders/invaders_ex1_s1.png)
*Solo Defense — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A classic monochrome arcade session (white aliens against black, shields up, score ticking.)

#### Key Concepts

Basic gameplay, shield placement, score tracking

#### Steps

1. Load the default preset or dial in the settings below.
2. Turn **Ship Pos** to center your cannon under the alien formation.
3. Flip the **Fire** toggle to Launch and take your first shot. Watch the score increment when you hit an alien.
4. Move **Ship Pos** to dodge the alien bullet (it falls from a random column) while lining up your next shot.
5. Try to clear the entire wave. When the last alien dies, the grid respawns at the top and your shields are restored.

#### Settings

| Control | Value |
|---------|-------|
| Ship Pos | 50% |
| Alien Spd | 20% |
| Fire Rate | 30% |
| Shields | 75% |
| Court Hue | 50% |
| Bright | 80% |
| Fire | Launch |
| Border | On |
| Score | On |
| Color | Mono |
| Bypass | Off |
| Mix | 100% |

---

### Exercise 2: Arcade Overlay

![Arcade Overlay result](/img/instruments/videomancer/invaders/invaders_ex2_s1.png)
*Arcade Overlay — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

The alien formation floating semi-transparently over a live video source (a playable heads-up display composited in real time.)

#### Key Concepts

Video compositing, transparent game overlay, performance integration

#### Steps

1. Patch a camera feed or pattern generator into the Videomancer input.
2. Set **Mix** to about 60% so the game graphics blend with the input.
3. Turn **Border** Off to remove the frame lines (they'll interfere with the underlying image.)
4. Play a round with the aliens ghosting over the video. Notice how brighter game elements (ship, bullets) punch through while darker areas let the input show.
5. Experiment with **Bright** to adjust how much the game elements dominate the composite.

#### Settings

| Control | Value |
|---------|-------|
| Ship Pos | 50% |
| Alien Spd | 25% |
| Fire Rate | 30% |
| Shields | 75% |
| Court Hue | 50% |
| Bright | 70% |
| Fire | Launch |
| Border | Off |
| Score | Off |
| Color | Mono |
| Bypass | Off |
| Mix | 60% |

---

### Exercise 3: Rainbow Armada

![Rainbow Armada result](/img/instruments/videomancer/invaders/invaders_ex3_s1.png)
*Rainbow Armada — simulated result across source images.*
#### Exercise Illustration

***A description of the exercise illustration.***

#### Learning Outcomes

A vivid color arcade field where each row of aliens glows in a different hue, creating a rainbow gradient that shifts as you change the base color.

#### Key Concepts

Hue mode, row-based alien coloring, visual composition

#### Steps

1. Set **Color** to Hue and turn **Court Hue** to about 25%: the top row of aliens takes the base hue and each successive row shifts further through the color wheel.
2. Turn **Bright** to maximum. Notice how the ship glows warm, alien bullets glow cool, and shields sit at a muted midtone.
3. Slowly sweep **Court Hue** clockwise while playing. The entire color palette rotates: reds become blues become greens, cycling the formation through rainbow after rainbow.
4. Try raising **Alien Spd** to about 50% for a faster, more visually dynamic game where the colored formation sweeps rapidly back and forth.

#### Settings

| Control | Value |
|---------|-------|
| Ship Pos | 50% |
| Alien Spd | 50% |
| Fire Rate | 40% |
| Shields | 50% |
| Court Hue | 25% |
| Bright | 100% |
| Fire | Launch |
| Border | On |
| Score | On |
| Color | Hue |
| Bypass | Off |
| Mix | 100% |

---
## Glossary

- **AABB**: Axis-aligned bounding box: the rectangular hit-detection region used for collision checks between bullets and sprites.

- **BCD**: Binary-coded decimal: a way of storing each decimal digit (0–9) in four bits, used here for the three-digit score counter.

- **DDS**: Direct digital synthesis: a technique for generating periodic waveforms from a phase accumulator, used in other Videomancer programs but not in Invaders itself.

- **Edge detection**: Detecting the instant a signal transitions from low to high (or vice versa), used here to fire the player bullet on the toggle-switch transition rather than while it's held.

- **Font ROM**: A read-only lookup table storing the pixel pattern for each character, here a 5×7 bitmap for digits 0–9.

- **Formation**: The rectangular grid of aliens that moves as a single block, reversing direction and stepping down when any member reaches a wall.

- **LFSR**: Linear-feedback shift register: a simple pseudorandom number generator that picks which alien column fires next.

- **Priority mux**: A multiplexer chain that selects which game element's color to display when multiple sprites overlap at the same pixel.

- **Sprite**: A small graphical element positioned independently on screen (here the ship, aliens, bullets, and shields.)

- **Wave**: One complete set of fifty-five aliens; clearing a wave respawns the grid and restores shields.

---
