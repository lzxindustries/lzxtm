---
draft: true
sidebar_position: 204
slug: /instruments/videomancer/plumber
title: "Plumber"
image: /img/instruments/videomancer/plumber/plumber_hero.png
description: "Program guide for Plumber, a Videomancer screen program for the LZX video synthesizer."
---

import plumber_animation from '/img/instruments/videomancer/plumber/plumber_animation.gif';
import plumber_control_panel from '/img/instruments/videomancer/plumber/plumber_control_panel.png';
import plumber_exercise1_result from '/img/instruments/videomancer/plumber/plumber_exercise1_result.gif';
import plumber_exercise2_result from '/img/instruments/videomancer/plumber/plumber_exercise2_result.gif';
import plumber_exercise3_result from '/img/instruments/videomancer/plumber/plumber_exercise3_result.gif';
import plumber_hero from '/img/instruments/videomancer/plumber/plumber_hero.png';

# Plumber

<span class="head2_nolink">Videomancer Program Guide</span>


---


<img src={plumber_hero} alt="Plumber hero image"/>
*A growing pipe network fills a dark grid — copper, teal, and salmon segments extend through intersections and elbows, the growth cursor just visible at the frontier where a new elbow piece connects two runs.*
<img src={plumber_animation} alt="Plumber animated output"/>
*Plumber output evolving over multiple frames — synthesis programs generate imagery without requiring a video input source.*

---

## Overview

Before Windows had wallpaper engines, it had screensavers. Among the most mesmerising was 3D Pipes, which appeared in Windows 95 and NT — a procedural animation that grew a network of connected pipe segments through an invisible three-dimensional grid, turning corners, branching at junctions, and changing colour at random. Plumber recreates that concept in two dimensions on FPGA hardware, rendering a continuously growing pipe network in a 60×34 cell grid at 74.25 MHz using four BRAM tiles and approximately 600 logic cells.

An animated growth cursor starts at the grid centre and extends one cell per tick. At each step, the cursor prefers to continue in its current direction (biased by the Straight control) but will turn randomly if its path is blocked. When the cursor reaches a dead end — surrounded by occupied cells on all four sides — it teleports to a random empty cell and continues in a new colour. The grid stores a 4-bit connection mask (North/South/East/West) and a 3-bit colour index for each cell. The rendering pipeline reads this connection data per pixel and draws thick centre-line segments extending toward each connected edge, with a centre junction box at every occupied cell. When the grid reaches 75% occupancy, the canvas clears and growth restarts from a random position.

At slow growth rates, Plumber produces a deliberate, architectural construction — each new pipe segment visibly extending the network. At maximum speed, the grid fills in seconds, producing a dense, colourful plumbing diagram. The name *Plumber* is a nod to the Windows screensaver and the universal experience of following a pipe to see where it goes.

---

## Background

### The Windows 3D Pipes Screensaver

The 3D Pipes screensaver shipped with Windows NT 3.5 in 1994 and became part of the standard Windows 95/98/NT screensaver collection. It rendered a growing network of pipe segments using OpenGL, with each new segment choosing between straight, elbow, and junction pieces based on what would fit the available space. The result was an ever-expanding labyrinth of glossy metallic pipes that filled the 3D volume before clearing and starting over. It became one of the most recognised graphical screensavers, and its visual language — thick tubes with rounded junctions, cycling through a colour palette — entered the collective memory of a generation of PC users.

### Procedural Growth Algorithms

Plumber's growth cursor implements a biased random walk on a grid graph. At each step, the cursor tries to extend in its current direction. If the target cell is occupied or out of bounds, it tries the remaining directions in random order. If all four are blocked, it teleports. This algorithm produces networks with a characteristic appearance: long straight runs interrupted by turns, with occasional clusters where the cursor was forced to weave through tight spaces. The Straight control biases the random walk toward continuation — high values produce highways of parallel runs, while low values create meandering paths with frequent direction changes.

### Connection Masks and Tile Rendering

Each grid cell stores a 4-bit mask indicating which of the four cardinal directions have pipe connections. This mask implicitly encodes the 16 possible tile types: empty (0000), four end caps (one bit set), four elbows (two adjacent bits), two straights (two opposite bits), four T-junctions (three bits), and the full cross (all four bits). The renderer translates each mask into a pixel pattern by extending arms from the centre of the cell toward each connected edge. The arms are constrained to a configurable width (the pipe radius), and a centre junction box is always drawn for non-empty cells. In Outline mode, the interior of the junction and arms is hollowed, leaving only the pipe walls.

### LFSR-Based Randomness

The cursor's random decisions — turn direction, teleport destination, initial seed — are driven by a 16-bit Linear Feedback Shift Register (LFSR). The LFSR produces a deterministic pseudorandom sequence seeded by the Seed parameter, so the same seed always generates the same pipe network. The LFSR runs continuously (enabled every clock), providing fresh random bits whenever the growth FSM needs to make a decision. Specific bits of the LFSR output select candidate cell coordinates for teleportation and determine the initial cursor direction after a teleport.

### Growth, Colour Cycling, and Canvas Clearing

The growth cursor carries a 3-bit colour counter that increments each time it teleports, cycling through 8 palette entries. This means each contiguous run of pipe segments shares a colour, and colour changes mark the points where the cursor jumped to a new location. The canvas is cleared when the cell count reaches 75% of the total grid (60 × 34 × 0.75 = 1530 cells), triggering a sequential memory wipe that zeroes one cell per clock. After clearing, the cursor resumes from a random position with the accumulated colour counter.


---

## Signal Flow

```
registers_in
│
├─ reg(0) → Growth Rate      (steps_8: frames between growth ticks)
├─ reg(1) → Pipe Thk         (steps_4: pipe radius 2/4/6/8 px)
├─ reg(2) → Straight         (LFSR threshold for straight bias)
├─ reg(3) → Seed             (LFSR initial seed)
├─ reg(4) → Bg Dim           (background video dimming)
├─ reg(5) → Pipe Hue         (DECLARED BUT UNUSED)
├─ reg(6)(0) → Fill Mode     (outline / filled)
├─ reg(6)(1) → Video Fill    (solid colour / video texture)
├─ reg(6)(2) → Glow          (centre brightening)
├─ reg(6)(3) → Grid Lines    (cell boundary overlay)
├─ reg(6)(4) → Bypass
└─ reg(7) → Mix Amount

Video Input (YUV 4:4:4)
│
├─ Timing Generator            (hsync/vsync → h_count, v_count)
│
├─ LFSR (16-bit, free-running)
│   └─ seeded from Seed on init
│       ◄── Seed
│
├─ Growth Tick Generator (per-frame, on vsync_start)
│   └─ tick when frame_count ≥ growth_div − 1
│       ◄── Growth Rate
│
├─ Growth FSM (vblank phase)
│   ├─ GS_IDLE → check occupancy (≥75% → clear canvas)
│   ├─ GS_CHECK_STRAIGHT → test candidate cell
│   │   ├─ free → GS_EXTEND
│   │   └─ occupied or OOB → GS_CHECK_TURN
│   ├─ GS_CHECK_TURN → try next direction (up to 4)
│   │   └─ all blocked → GS_TELEPORT
│   ├─ GS_EXTEND → write new cell (connection + colour)
│   ├─ GS_UPDATE_PREV → add exit bit to previous cell
│   ├─ GS_TELEPORT → increment colour, seek empty cell
│   └─ GS_FIND_EMPTY → LFSR probe (up to 200 attempts)
│       ◄── Straight (bias), LFSR (randomness)
│
├─ Grid BRAM (2048 × 8-bit)
│   └─ cell[addr] = { colour[6:4], conn_mask[3:0] }
│
├─ Rendering Stage 1: Cell Address + Local Coords
│   ├─ cell_x = h_count[10:5],  cell_y = v_count[10:5]
│   └─ local_x = h_count[4:0],  local_y = v_count[4:0]
│
├─ Rendering Stage 2: BRAM Read
│   ├─ read grid[cell_y × 60 + cell_x]
│   └─ delay local_x, local_y by 1 clock
│
├─ Rendering Stage 3: Tile Render + Composite
│   ├─ dx = |local_x − 16|,  dy = |local_y − 16|
│   ├─ pipe_on: junction box + N/S/E/W arms per conn_mask
│   ├─ outline mode: hollow interior where no arm extends
│   ├─ Pipe pixel:
│   │   ├─ Video Fill → output = input video
│   │   └─ Solid Fill:
│   │       ├─ Glow → center pixels = 1023, edges = palette
│   │       └─ Normal → palette[colour_idx] Y/U/V
│   ├─ Grid line pixel:
│   │   └─ Y = input_Y/2 + 64, U/V = input
│   └─ Background pixel:
│       └─ Y = input_Y × (1023 − bg_dim) >> 10
│       ◄── Pipe Thk, Fill Mode, Video Fill, Glow, Grid Lines, Bg Dim
│
├─ Stages 4–7: Interpolator Mix (×3 channels, 4 clk)
│   └─ mix = lerp(delayed_input, rendered, mix_amount)
│       ◄── Mix
│
├─ Sync Delay Pipeline (4-clock shift register)
│
└─ Output Mux
    ├─ Bypass off → mixed Y/U/V + aligned sync
    └─ Bypass on  → input Y/U/V + aligned sync
        ◄── Bypass
```

The growth FSM operates during the vertical blanking interval, reading and writing the BRAM grid while the rendering pipeline is idle. During active video, the rendering pipeline reads the grid in a purely passive manner — one cell lookup per pixel clock, with the cell address derived from the pixel position. This dual-phase access pattern avoids the need for dual-port BRAM: the growth FSM writes during vblank, and the renderer reads during active scan.

The Pipe Hue parameter (register 5) is mapped to a signal (`s_hue_pot`) but is never referenced by the rendering pipeline. Pipe colour is determined entirely by the 3-bit colour counter carried by the growth cursor, which indexes an 8-entry hardcoded YUV palette. The Hue control currently has no visible effect on the output.

---

## Parameter Reference

<img src={plumber_control_panel} alt="Videomancer front panel with Plumber loaded"/>
*Videomancer's front panel with Plumber active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Growth Rate
| Property | Value |
|----------|-------|
| Range | 1c/s – 128c/s |
| Default | 33c/s |
| Suffix | c/s |

Controls the frames between growth ticks using a steps_8 quantization: the pot value maps to dividers of 128, 64, 32, 16, 8, 4, 2, or 1 frames per tick. At the lowest setting (divider 128), the cursor extends one cell approximately every 2 seconds (at 60 fps), producing a deliberate, architectural growth. At the highest setting (divider 1), the cursor extends one cell every frame, filling the grid in approximately 30 seconds. Intermediate settings around step 4 (divider 16) produce a satisfying pace where individual extensions are visible but the network builds steadily.

---

#### Knob 2 — Pipe Thk
| Property | Value |
|----------|-------|
| Range | 2px – 8px |
| Default | 4px |
| Suffix | px |

Sets the pipe thickness using a steps_4 quantization: radius 2, 4, 6, or 8 pixels (at the native 1920×1080 resolution). At radius 2, pipes are thin lines that leave large gaps between runs. At radius 8, pipes are thick tubes that nearly fill the 32-pixel cell, creating a dense, chunky appearance. The radius applies to both the centre junction box and all arm extensions. In Outline mode, the wall thickness is 1 pixel (the difference between the outer radius and the inner hollow), so thicker pipes have proportionally larger open interiors.

---

#### Knob 3 — Straight
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 59% |
| Suffix | % |

Biases the growth cursor toward continuing in its current direction. The register value is compared against the LFSR output: if the LFSR value is below the Straight threshold, the cursor attempts to extend straight ahead. Otherwise, it picks a random perpendicular direction. At 0%, the cursor turns randomly at every step, producing short, meandering paths with frequent elbows. At 100%, the cursor almost always continues straight, producing long parallel runs with turns occurring only when the path is blocked. A moderate setting around 60% creates a natural-looking network with a mix of straight segments and turns.

---

#### Knob 4 — Seed
| Property | Value |
|----------|-------|
| Range | 0 – 1023 |
| Default | 1 |

Seeds the 16-bit LFSR that drives all random decisions in the growth FSM. Each seed value produces a deterministically different pipe network — the same seed always generates the same pattern of turns, teleports, and colour assignments. At 0, the LFSR receives an all-zero seed (which may produce degenerate sequences depending on the LFSR polynomial). Non-zero seeds produce the full pseudorandom sequence. This control is useful for finding and reproducing specific network layouts.

---

#### Knob 5 — Bg Dim
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 68% |
| Suffix | % |

Controls the dimming applied to the background (non-pipe) pixels. The input video's Y channel is multiplied by $(1023 - \text{bg\_dim}) / 1024$. At 0%, the background shows the full input video brightness. At 100%, the background is fully black. When Bg Dim exceeds 900, the background chroma is also neutralised (U = V = 512), preventing colour artefacts in very dark regions. This control effectively sets the contrast between the pipe network and its surroundings — high dim values make the pipes stand out against a dark field.

---

#### Knob 6 — Pipe Hue
| Property | Value |
|----------|-------|
| Range | 0° – 359° |
| Default | 0° |
| Suffix | ° |

This parameter is mapped to register 5 (`s_hue_pot`) but is **not referenced** by the rendering pipeline. The pipe colour for each segment is determined by an internal 8-entry palette indexed by the growth cursor's 3-bit colour counter, which increments on each teleport. The Hue control currently has no visible effect on the output. It is retained in the register map for potential future use or custom VHDL modifications.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Fill Mode** | Outline | Filled |
| **8 — Video Fill** | Solid | Video |
| **9 — Glow** | Off | On |
| **10 — Grid Lines** | Off | On |
| **11 — Bypass** | Off | On |

The five toggles divide into two functional groups plus bypass. Fill Mode (toggle 7) and Video Fill (toggle 8) control the pipe appearance: Fill Mode selects between solid filled pipes and hollow outlined pipes, while Video Fill replaces the solid palette colour with the input video signal within the pipe footprint. Glow (toggle 9) and Grid Lines (toggle 10) add visual overlays: Glow brightens the centre of each pipe to full white, and Grid Lines draws faint lines at cell boundaries. Bypass (toggle 11) overrides everything at the output mux. All operate independently.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0% – 100% |
| Default | 100% |
| Suffix | % |

Crossfades between the delayed input video and the rendered pipe network output. At 0%, the output is pure input — no pipes visible. At 100%, the output is the fully rendered pipe network with dimmed background. Intermediate positions blend the two, allowing the pipe network to appear as a semi-transparent overlay. At 50% with a live video source, the pipe network is ghosted over the video — useful for compositing the procedural pattern as a decorative layer.

---

## Guided Exercises

These exercises build from a slowly growing network through dense fills to video-textured compositions. Because Plumber is a generative synthesis program, each exercise requires time for the growth cursor to build enough of the network to evaluate — allow at least 10 seconds at moderate growth rates before judging the result.

### Exercise 1: Slow Architectural Growth

<img src={plumber_exercise1_result} alt="Slow Architectural Growth result"/>
*Slow Architectural Growth — simulated result across source images.*
**Objective**: Watch the growth FSM build a pipe network one cell at a time, understanding how Straight bias and pipe thickness affect the network structure.

1. **Slow growth**: Set Growth Rate to ~10% (divider 64). Growth ticks occur approximately once per second.
2. **Medium thickness**: Set Pipe Thk to step 2 (~40%). Pipes are visible but not overwhelming.
3. **High straight bias**: Set Straight to ~80%. The cursor strongly prefers continuing in its current direction.
4. **Watch the network**: Observe for 30 seconds. Note how the cursor extends long straight runs with occasional turns.
5. **Reduce straight bias**: Set Straight to ~20%. The cursor now meanders, producing frequent elbows and short segments.
6. **Try different seeds**: Sweep Seed slowly. Each value produces a different network layout from the start.
7. **Enable grid lines**: Flip Grid Lines to On. The 32×32 cell boundaries become visible, showing the grid structure.

**Key concepts**: Growth Rate controls ticks per second, Straight biases the random walk toward continuation, each seed produces a deterministic network, grid lines reveal the cell structure, colour changes mark teleport events

---

### Exercise 2: Dense Outline Network with Glow

<img src={plumber_exercise2_result} alt="Dense Outline Network with Glow result"/>
*Dense Outline Network with Glow — simulated result across source images.*
**Objective**: Fill the grid rapidly and explore outline rendering with centre glow to produce a detailed technical drawing effect.

1. **Fast growth**: Set Growth Rate to ~90% (divider 1–2). The grid fills in seconds.
2. **Thick pipes**: Set Pipe Thk to step 4 (~90%). Maximum thickness shows the most detail in outline mode.
3. **Switch to outline**: Set Fill Mode to Outline. Pipes become hollow rectangular tubes.
4. **Enable glow**: Flip Glow to On. Bright hotspots appear at every junction centre.
5. **Dark background**: Set Bg Dim to ~90%. The pipes stand out sharply against near-black.
6. **Wait for a clear cycle**: Let the grid fill to 75% and watch it clear and restart. The clearing is sequential — cells wipe from the first memory address.
7. **Adjust straight**: Set Straight to ~50%. A balanced network with a mix of straights, elbows, and T-junctions.

**Key concepts**: Outline mode hollows pipe interiors, Glow adds center highlights at junctions, thick pipes show clear wall structure, 75% occupancy triggers canvas clear, rapid growth fills the grid in seconds

---

### Exercise 3: Video-Filled Stained Glass

<img src={plumber_exercise3_result} alt="Video-Filled Stained Glass result"/>
*Video-Filled Stained Glass — simulated result across source images.*
**Objective**: Use the pipe network as a video stencil, filling each pipe segment with the live input signal to create a stained-glass window effect.

1. **Feed video**: Connect a video source with colourful, high-contrast content.
2. **Enable Video Fill**: Set Video Fill to Video. Pipe pixels now show the input video.
3. **Medium growth**: Set Growth Rate to ~50%. The network builds at a visible pace.
4. **Moderate thickness**: Set Pipe Thk to step 3 (~65%). Pipe segments are wide enough to show video detail.
5. **Dark background**: Set Bg Dim to ~85%. Background video is heavily dimmed, making the video-filled pipes the focus.
6. **Set mix**: Push Mix to ~90%. The rendered output dominates with slight input bleed.
7. **Enable grid lines**: Flip Grid Lines to On. Cell boundaries form a leading grid around the video-filled pipes.
8. **Try high Straight**: Set Straight to ~90%. Long video-filled corridors scroll with the growth cursor.

**Key concepts**: Video Fill replaces pipe colour with input video, background dim separates pipe regions from surroundings, grid lines add framing, the pipe footprint acts as a stencil masking the video, high Straight creates corridor-like compositions

---


## Tips

- **Start slow, watch the growth**: Setting Growth Rate below 20% lets you see each individual cell extension, understanding how the cursor navigates the grid.
- **High Straight for highways**: A Straight bias above 80% produces long parallel runs that fill the grid in an orderly, architectural manner — satisfying to watch and producing clean geometric results.
- **Outline + thick for blueprints**: Outline mode with maximum pipe thickness creates a technical drawing aesthetic — hollow rectangular tubes with visible wall structure.
- **Seed for reproducibility**: Each Seed value generates a unique but deterministic network. Bookmark seeds that produce interesting compositions.
- **Darken the background**: Bg Dim at 80%+ makes the pipe network the visual focus. At 100%, pipes float on pure black.
- **Video Fill for stained glass**: Switching to Video Fill mode turns the network into a stencil — each pipe segment shows a window of live video, framed by the dimmed background.
- **Hue pot is currently unused**: The Pipe Hue knob has no effect on the output. Pipe colour cycles automatically through 8 colours as the cursor teleports.
- **Watch the clear cycle**: The 75% occupancy threshold triggers a full canvas wipe. At fast growth rates, you can observe the cycle repeating every 20–30 seconds.

---

## Glossary

| Term | Definition |
|------|------------|
| **BRAM (Block RAM)** | Dedicated memory resources within the FPGA fabric, used here to store the 60×34 grid of cell data (2048 × 8-bit tiles). |
| **Connection mask** | A 4-bit value where each bit represents a pipe connection in one cardinal direction (North, South, East, West), encoding 16 possible tile configurations. |
| **FSM (Finite State Machine)** | A sequential logic circuit with a defined set of states and transitions, used here for the growth cursor's decision-making process. |
| **LFSR (Linear Feedback Shift Register)** | A shift register with feedback taps that produces a deterministic pseudorandom sequence, used here for all random decisions in the growth FSM. |
| **Manhattan distance** | A distance metric defined as the sum of absolute differences along each axis: $d = |x_1 - x_2| + |y_1 - y_2|$. Used for the glow centre brightening test. |
| **Occupancy threshold** | The fraction of grid cells that are non-empty. Plumber clears and restarts when occupancy reaches 75%, preventing the growth FSM from spending excessive time searching for empty cells. |
| **Teleport** | The growth cursor's fallback behaviour when all four cardinal neighbours are occupied or out of bounds. The cursor jumps to a randomly selected empty cell and continues in a new direction with an incremented colour. |
| **YUV** | A colour model that separates luminance (Y) from two chrominance components (U and V), widely used in video signal processing. |
