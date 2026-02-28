---
draft: true
sidebar_position: 29
slug: /instruments/videomancer/brushwork
title: "Brushwork"
image: /img/instruments/videomancer/brushwork/brushwork_hero.png
description: "In 1990, NewTek shipped the NewTek — an Amiga-based video effects system that introduced a generation of video producers to real-time digital transitions."
---

import brushwork_hero from '/img/instruments/videomancer/brushwork/brushwork_hero.png';
import brushwork_before_after from '/img/instruments/videomancer/brushwork/brushwork_before_after.png';
import brushwork_control_panel from '/img/instruments/videomancer/brushwork/brushwork_control_panel.png';
import brushwork_exercise1_result from '/img/instruments/videomancer/brushwork/brushwork_exercise1_result.png';
import brushwork_exercise2_result from '/img/instruments/videomancer/brushwork/brushwork_exercise2_result.png';
import brushwork_exercise3_result from '/img/instruments/videomancer/brushwork/brushwork_exercise3_result.png';

# Brushwork

<span class="head2_nolink">Videomancer Program Guide</span>

<img src={brushwork_hero} alt="Brushwork hero image"/>
*Brushwork applying a bristle-textured paint sweep revealing a source image through a warm-toned fill color.*
<img src={brushwork_before_after} alt="Before and after comparison"/>
*Left: unprocessed source. Right: Brushwork applied.*

---

## Overview

In 1990, NewTek shipped the NewTek — an Amiga-based video effects system that introduced a generation of video producers to real-time digital transitions. Among its most celebrated effects were Paint Brush Across and PaintRoller, which simulated a paint tool sweeping across the screen, gradually revealing or concealing video with the organic edge of a physical brush stroke. These transitions transcended the clean geometric wipes that preceded them, bringing textured, hand-made character to broadcast production.

Brushwork recreates and extends this concept in FPGA hardware. A sweep edge advances across the frame (horizontally or vertically), with its contour modulated by one of four BRAM-stored brush texture profiles: bristle brush (clustered peaks with fine gaps), roller (smooth cylindrical pressure undulation), palette knife (smooth blade with sharp paint ridges), and sponge (highly irregular holes and islands). The two Brush A/B toggles select the profile as a 2-bit index. The painted region shows either a solid fill color generated from a 6-sector hue lookup or the input video in transition mode.

The program stores all four profiles in a single 128-entry BRAM tile (4 profiles × 32 entries × 10-bit values). The texture modulates the sweep edge position per-row (or per-column in vertical mode), so each brush profile creates a distinctly shaped edge contour. A softness parameter controls the width of the gradient transition zone at the edge, creating either sharp hard-edged strokes or broad feathered blends.

---

## Background

### The NewTek Legacy

The NewTek NewTek (1990-2005) democratized broadcast-quality video effects on commodity hardware. Its transition library included standard geometric wipes alongside a distinctive set of "physical tool" effects — paint brushes, peeling pages, dripping paint, shatter patterns. These transitions implied the physical presence of a tool acting on the image, creating a sense of craft and materiality. Brushwork's four profiles directly reference this lineage: the bristle brush recalls Paint Brush Across, the roller recalls PaintRoller, and the palette knife and sponge expand the metaphor to additional art-making tools.

### Brush Texture as Edge Modulation

Each brush profile is stored as 32 displacement values spanning the perpendicular axis of the sweep. When the sweep advances horizontally, the 32 entries map across the 720 vertical lines — each entry modulates the sweep edge position for a band of approximately 22 lines. This creates a characteristic edge contour: bristle brush has clustered peaks with gaps between bristle groups, roller has gentle sinusoidal undulation from cylindrical pressure, palette knife has long smooth sections punctuated by sharp paint ridges where excess pigment accumulates, and sponge has an extremely irregular pattern of deep holes and raised islands reflecting the porous structure of the tool.

### Sweep Edge Mechanics

The sweep position maps the Transition knob (0-1023) to the frame width (0-1280 pixels for horizontal, 0-720 for vertical). At the sweep edge, the brush texture displacement is added to create the modulated contour. The Tex Width parameter scales this displacement — at zero, the edge is straight regardless of brush profile; at maximum, the brush texture exerts its full influence, creating deeply contoured edges. Tex Offset allows scrolling through the texture entries, shifting which portion of the brush pattern appears at any given position.

### Alpha Compositing and Fill Color

Behind the sweep edge (the "painted" region), the program composites either a solid fill color or the input video. The fill color is generated from a 6-sector hue lookup — the Fill Hue knob selects the color angle, and Fill Bright controls the luminance. In Video mode (Fill Mode toggle), the roles reverse: the painted region shows the input video while the unpainted region shows the fill color. Combined with the Invert toggle, this provides four compositional variants for maximum flexibility in transition design.

### Soft Edges and Feathering

The Softness parameter controls the width of the transition gradient at the brush edge. At zero softness, the edge is a hard binary cut — pixels are either fully painted or fully transparent. As softness increases, a gradient zone appears where the alpha blends linearly from full opacity to full transparency. This creates feathered, airbrushed edges that soften the mechanical precision of the sweep into something more painterly. Combined with the brush texture, softness allows dramatic variation in edge character — from sharp bristle marks to broad, diffuse color washes.


---

## Signal Flow

```
Input Video (YUV 4:4:4)
│
├── Stage 1: Parameter Decode + Brush Address ──────────────────
│   │
│   ├─ 1. Sweep Position        (transition × 1280 / 1024)
│   ├─ 2. Perpendicular Index   (v_count for horiz, h_count for vert)
│   └─ 3. Brush Address         (brush_sel[1:0] & (tex_index + tex_offset))
│
├── Stage 2: BRAM Read + Edge Calculation ──────────────────────
│   │
│   ├─ 4. Brush Displacement    (BRAM lookup → 10-bit texture value)
│   ├─ 5. Edge Displacement     (brush_disp × tex_width / 1024)
│   └─ 6. Edge-at-Row           (sweep_pos + edge_displacement)
│
├── Stage 3: Matte Alpha Computation ───────────────────────────
│   │
│   ├─ 7. Ahead/Behind Test     (pixel_pos vs edge_at_row ± soft_width)
│   ├─ 8. Gradient Alpha        (linear ramp within soft_width zone)
│   └─ 9. Invert                (optional alpha inversion)
│
├── Stage 4: Alpha Compositor ──────────────────────────────────
│   │
│   ├─ 10. Fill Color           (6-sector hue × brightness → YUV)
│   ├─ 11. Color Mode           (fill × alpha + video × (1-alpha))
│   └─ 12. Video Mode           (video × alpha + fill × (1-alpha))
│
├── Mix ────────────────────────────────────────────────────────
│   └─ 13. Interpolator × 3     (dry/wet crossfade Y, U, V)
│
└── Output
```

The key insight of Brushwork's pipeline is that all edge modulation happens in a single dimension. The brush texture is indexed by the perpendicular axis — vertical position for horizontal sweeps, horizontal position for vertical sweeps — creating a displacement profile that modulates the sweep edge. This means the brush edge is technically a 1D function applied uniformly along the sweep direction, but because the texture profiles contain varied frequency content, the visual impression is of a richly detailed 2D brush stroke. The 32-entry resolution balances BRAM economy against sufficient spatial detail for natural-looking brush edges.

---

## Parameter Reference

<img src={brushwork_control_panel} alt="Videomancer front panel with Brushwork loaded"/>
*Videomancer's front panel with Brushwork active. Knobs 1–6 (top two rows of left cluster), Toggle switches 7–11 (bottom row of left cluster), Fader 12 (right side).*

### Rotary Potentiometers (Knobs 1–6)

#### Knob 1 — Transition
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the position of the sweep edge across the frame, from fully closed (0%) to fully open (100%). This is the primary animation control — sweeping from 0 to 100% executes a complete brush-stroke transition across the frame. The sweep position maps linearly to the frame width: for horizontal mode, 0% is the left edge and 100% is the right edge; for vertical mode, 0% is the top and 100% is the bottom. The brush texture modulates the sweep edge around this center position.

---

#### Knob 2 — Tex Width
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the amplitude of the brush texture displacement. At 0%, the brush texture has no effect and the sweep edge is a straight line. As Tex Width increases, the brush displacement values increasingly modulate the edge position, creating a wider and more pronounced brush-shaped contour. At maximum, the brush profile exerts its full displacement — bristle gaps become deep notches, roller undulations become broad waves, palette knife ridges become prominent shoulders, and sponge holes create irregular channels through the edge.

---

#### Knob 3 — Softness
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 25.0% |
| Suffix | % |

Controls the width of the soft gradient zone at the brush edge. At 0%, the edge is a hard binary cut. As softness increases, the transition zone widens, creating a feathered gradient from fully painted to fully transparent. The gradient is linear within the softness zone. High softness values create broad, airbrushed transitions; low values create crisp, pen-like edges. Softness interacts visually with the brush texture — a soft bristle brush creates diffuse bristle-shaped gradients, while a hard sponge creates sharply defined holes.

---

#### Knob 4 — Fill Hue
| Property | Value |
|----------|-------|
| Range | 0° – 360° |
| Default | 0° |
| Suffix | ° |

Controls the hue of the fill color via a 6-sector color wheel. The VHDL implements a simple YUV color lookup based on the top 3 bits of the hue value, creating 6 distinct color sectors plus two neutral positions. Rotating through the full 360° range cycles through red, yellow, green, cyan, blue, and magenta. The fill color is used in Color fill mode (the default) to paint the brush-stroked region, or in Video reveal mode as the background behind the revealed video.

---

#### Knob 5 — Fill Bright
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 50.0% |
| Suffix | % |

Controls the luminance (brightness) of the fill color. At 0%, the fill is black regardless of the hue setting. At 50%, the fill matches typical broadcast levels. At 100%, the fill is at maximum brightness. This parameter directly sets the Y channel of the fill color — the chrominance is determined by Fill Hue independently. At very low brightness, the painted region becomes a dark wash; at high brightness with saturated hues, it becomes a vivid color field.

---

#### Knob 6 — Tex Offset
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 0.0% |
| Suffix | % |

Controls the offset into the brush texture table, effectively scrolling the texture pattern. At 0%, the texture starts at entry 0 of the selected profile. Increasing the offset shifts which portion of the 32-entry pattern aligns with which screen position. This allows fine-tuning of the brush edge appearance — shifting a bristle brush texture can move a gap to a different vertical position, or align a palette knife ridge with a specific feature in the source video. The offset wraps naturally due to the 5-bit address calculation.

---

### Toggle Switches (Switches 7–11)

| Switch | Off | On |
|--------|-----|-----|
| **7 — Brush A** | Off | On |
| **8 — Brush B** | Off | On |
| **9 — Direction** | Horiz | Vert |
| **10 — Fill Mode** | Color | Video |
| **11 — Invert** | Off | On |

The five toggles configure the brush selection, sweep geometry, and compositing behavior. Brush A and Brush B form a 2-bit selector choosing among the four brush profiles (00=Bristle, 01=Roller, 10=Palette Knife, 11=Sponge). Direction selects horizontal or vertical sweep. Fill Mode chooses between color fill and video reveal compositing. Invert reverses the matte alpha.

---

### Linear Potentiometer (Fader 12)

#### Fader 12 — Mix
| Property | Value |
|----------|-------|
| Range | 0.0% – 100.0% |
| Default | 100.0% |
| Suffix | % |

Controls the dry/wet mix between the original input video and the brush-composited output. At 0% (fully dry), the output is the unprocessed input regardless of all other settings. At 100% (fully wet), the full brush effect is visible. Intermediate values crossfade between the two, allowing the brush effect to be partially blended with the source.

---

## Guided Exercises

These exercises progress from a basic bristle stroke to a complex multi-mode transition, exploring all four brush profiles, sweep directions, fill modes, and soft edge techniques.

### Exercise 1: Classic Bristle Brush Stroke

<img src={brushwork_exercise1_result} alt="Classic Bristle Brush Stroke result"/>
*Classic Bristle Brush Stroke — simulated result across source images.*
**Source**: Feed a high-contrast image (Kodak #4 — the portrait provides clear definition of the brush boundary against facial features).

**Objective**: Create a classic paint-brush-across effect using the bristle profile with moderate softness and a warm fill color.

1. Set Transition to 50% to position the sweep edge at mid-frame.
2. Set Tex Width to 60% for pronounced but not extreme bristle displacement.
3. Set Softness to 25% for slightly feathered edges that suggest brush bristle marks.
4. Set Fill Hue to 30° for a warm orange/red fill color.
5. Set Fill Bright to 60% for a naturally vivid fill.
6. Set Tex Offset to 0%.
7. Set both Brush A and Brush B to Off (Bristle profile, 00).
8. Set Direction to Horiz.
9. Set Fill Mode to Color.
10. Set Invert to Off.
11. Set Mix to 100%.
12. Observe the bristle brush edge at mid-frame — peaks and gaps creating an organic boundary between the warm fill color and the portrait.

**Key concepts**: The Bristle profile has high-frequency variation with clustered peaks separated by deep gaps, creating the distinctive mark of a worn paintbrush with separated bristle groups. The moderate softness adds a slight gradient that softens the bristle marks without eliminating them, producing a natural-looking painted edge.

---

### Exercise 2: Palette Knife Video Reveal

<img src={brushwork_exercise2_result} alt="Palette Knife Video Reveal result"/>
*Palette Knife Video Reveal — simulated result across source images.*
**Source**: Feed a colorful, detailed image (Mandrill — the dense facial texture and vivid colors make the video reveal boundary clearly visible).

**Objective**: Use the palette knife profile with hard edges and video reveal mode to create a sharp-edged transition that reveals the source through a blue fill.

1. Set Transition to 40% for a partially revealed frame.
2. Set Tex Width to 75% for dramatic palette knife ridges.
3. Set Softness to 5% for near-hard edges.
4. Set Fill Hue to 240° for a deep blue fill.
5. Set Fill Bright to 45% for a rich but not overwhelming blue.
6. Set Tex Offset to 30% to shift the knife ridge pattern.
7. Set Brush A to Off, Brush B to On (Palette Knife profile, 10).
8. Set Direction to Horiz.
9. Set Fill Mode to Video — the brush reveals the mandrill through the blue fill.
10. Set Invert to Off.
11. Set Mix to 100%.
12. Observe the sharp palette knife edge with its characteristic long smooth sections punctuated by sudden ridges where paint would accumulate on a real blade.

**Key concepts**: The Palette Knife profile has long smooth sections at moderate displacement, with sudden sharp jumps at entries 7 and 26-27 where paint ridges are modeled. This creates a distinctive edge with mostly clean lines punctuated by dramatic protrusions. Video reveal mode inverts the semantic relationship: the brush "reveals" the video through the fill color field rather than "painting" over it.

---

### Exercise 3: Vertical Sponge Wash with Soft Edges

<img src={brushwork_exercise3_result} alt="Vertical Sponge Wash with Soft Edges result"/>
*Vertical Sponge Wash with Soft Edges — simulated result across source images.*
**Source**: Feed a scene with varied horizontal content (Kodak #23 — the outdoor scene provides horizontal variation that interacts interestingly with vertical sweep).

**Objective**: Create a broad, diffuse vertical wash using the sponge profile with maximum softness and vertical sweep direction.

1. Set Transition to 55% for a sweep slightly past center.
2. Set Tex Width to 85% for maximum sponge texture displacement.
3. Set Softness to 80% for extremely broad, airbrushed edges.
4. Set Fill Hue to 150° for a green fill.
5. Set Fill Bright to 70% for a bright wash.
6. Set Tex Offset to 50% to select a different region of the sponge pattern.
7. Set Brush A to On, Brush B to On (Sponge profile, 11).
8. Set Direction to Vert — sweep advances top-to-bottom.
9. Set Fill Mode to Color.
10. Set Invert to Off.
11. Set Mix to 100%.
12. Observe the extremely irregular sponge edge creating channels and islands of color and video intermixed, softened into a diffuse, watercolor-like wash by the high softness setting.

**Key concepts**: The Sponge profile has the most irregular displacement pattern — alternating between near-zero and near-maximum values with no smooth transitions. Combined with high softness, the hard holes and islands of the sponge texture become broad gradient regions that overlap and interact, creating an effect reminiscent of watercolor bleeding. Vertical direction with horizontal texture indexing means the sponge pattern modulates across the frame width.

---


## Tips

- **Animate the Transition knob**: Brushwork is designed as a transition effect. Slowly sweeping Transition from 0% to 100% executes a complete brush-stroke wipe across the frame.
- **Match brush to content**: Bristle works well for rough, energetic transitions; Roller for smooth, professional wipes; Palette Knife for dramatic reveals; Sponge for organic, textured washes.
- **Softness defines character**: A hard-edged bristle stroke looks like encaustic or oil; a soft-edged one looks like watercolor or airbrush. Adjust softness to match the intended medium.
- **Tex Offset for variety**: Different offset values produce visually different edge contours from the same profile. Use this to avoid repetitive-looking brush transitions.
- **Invert for reverse strokes**: After performing a forward brush stroke (Transition 0→100%), toggle Invert and sweep back (100→0%) to create a complementary reverse stroke.
- **Video reveal for transitions**: In Video mode, use a fill color matching your downstream content's palette, then sweep to reveal the source — this creates production-ready transitions between scenes.
- **Combine with Mix**: At low Mix values (20-40%), the brush effect becomes a subtle color wash over the source rather than a hard transition.

---

## Glossary

| Term | Definition |
|------|------------|
| **Alpha compositing** | A technique for blending two image layers using a per-pixel opacity (alpha) value, where 0 is fully transparent and 1 is fully opaque. |
| **BRAM (Block RAM)** | Dedicated memory blocks within an FPGA used for storing data such as lookup tables or texture profiles; Brushwork uses one BRAM tile for four brush profiles. |
| **Chrominance** | The color-difference components (U and V) of a YUV signal, encoding hue and saturation independently of brightness. |
| **Feathering** | Gradually blending the edge of a selection or transition from fully opaque to fully transparent, producing a soft rather than hard boundary. |
| **Fill color** | A solid color generated from a hue/brightness lookup used to paint the brush-stroked region or as the background in video reveal mode. |
| **Hue** | The attribute of a color that distinguishes it on the color wheel (red, yellow, green, etc.), specified here as an angle in degrees. |
| **Interpolator** | A linear-blending circuit that crossfades between two input values; used in Videomancer for wet/dry mixing. |
| **Matte** | A mask defining which regions of a frame are opaque and which are transparent, used to composite the painted and unpainted areas. |
| **SMPTE** | Society of Motion Picture and Television Engineers, the standards body that defines broadcast video wipe patterns and transition specifications. |
| **Sweep edge** | The primary boundary that advances across the frame during a transition, modulated by the brush texture to create an organic contour. |
| **Texture profile** | A stored one-dimensional displacement pattern (32 entries) that modulates the sweep edge, creating the characteristic shape of each brush type. |
| **YUV** | A color encoding that separates luminance (Y) from chrominance (U, V); the native format of Videomancer's 30-bit video pipeline. |

---
