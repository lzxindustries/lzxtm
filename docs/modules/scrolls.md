---
draft: false
title: "SCROLLS: Dual Motion Controlled Ramp Generator"
---

import scrolls_frontpanel from '/img/modules/scrolls/scrolls-diagrams/scrolls_frontpanel.png';
import scrolls_corner from '/img/modules/scrolls/scrolls-diagrams/scrolls_corner.gif';
import scrolls_controls_and_connectors from '/img/modules/scrolls/scrolls-diagrams/scrolls_controls-and-connectors.png';
import scrolls_dwo3_reset from '/img/modules/scrolls/scrolls-diagrams/scrolls_dwo3-reset.gif';
import scrolls_hv_blank_three_speeds from '/img/modules/scrolls/scrolls-diagrams/scrolls_hv-blank-three-speeds.gif';
import scrolls_hv_scroll from '/img/modules/scrolls/scrolls-diagrams/scrolls_hv-scroll.gif';
import scrolls_journey_phase_1 from '/img/modules/scrolls/scrolls-diagrams/scrolls_journey-phase1.gif';
import scrolls_journey_phase_2 from '/img/modules/scrolls/scrolls-diagrams/scrolls_journey-phase2.gif';
import scrolls_motion_disabled_blank from '/img/modules/scrolls/scrolls-diagrams/scrolls_motion-disabled-blank.gif';
import scrolls_motion_disabled_mirror from '/img/modules/scrolls/scrolls-diagrams/scrolls_motion-disabled-mirror.gif';
import scrolls_motion_disabled_wrap from '/img/modules/scrolls/scrolls-diagrams/scrolls_motion-disabled-wrap.gif';
import scrolls_mounting_power_sync from '/img/modules/scrolls/scrolls-diagrams/scrolls_mounting-power-sync.png';
import scrolls_orbit from '/img/modules/scrolls/scrolls-diagrams/scrolls_orbit.gif';
import scrolls_ping_pong from '/img/modules/scrolls/scrolls-diagrams/scrolls_ping-pong.gif';
import scrolls_ramp_outputs from '/img/modules/scrolls/scrolls-diagrams/scrolls_ramp-outputs.png';
import scrolls_random_ccw from '/img/modules/scrolls/scrolls-diagrams/scrolls_random-ccw.gif';
import scrolls_random_cw from '/img/modules/scrolls/scrolls-diagrams/scrolls_random-cw.gif';
import scrolls_stairs_oscillator from '/img/modules/scrolls/scrolls-diagrams/scrolls_stairs-oscillator.gif';
import scrolls_synchronous_lfos from '/img/modules/scrolls/scrolls-diagrams/scrolls_synchronous-lfos.gif';
import scrolls_line_art_labeled from '/img/modules/scrolls/scrolls-diagrams/placeholders/scrolls_line_art_labeled_placeholder_345x700.png';

# SCROLLS
<span class="head2_nolink">Dual Motion Controlled Ramp Generator</span>
<!-- 
:::warning
This page is under construction and in a draft state. Stay tuned to our newsletter for the official content release.
::: -->

<img src={scrolls_frontpanel} alt="Scrolls front panel" />

## Overview

Scrolls is a high precision motion controlled dual waveform generator for SD and HD modular video synthesis. It provides full control over two independent sets of video waveforms. Front panel switches provide access to 72 combinations of speed, waveform blanking and mirroring, and advanced motion paths ranging from elliptical orbit to random walk.

Basic generative synthesis patches begin with horizontal and vertical ramps. These define 2D Cartesian coordinates in screen space. With *motion controlled* ramps, the coordinate system itself is shifted, repositioning or animating the entire resulting pattern.

Scrolls also outputs four dedicated low frequency control voltages. These CVs are synchronized to the movement of the video waveforms. Use them to animate the patch in other ways, dancing in time with Scrolls.

<!-- AFR note: throughout, I've changed the name of the low frequency outputs from 'LFO' to 'CV'. I did this because I assume that the Random modes aren't periodic, so not really 'oscillators' in the sense that users are likely to understand the term. Technically, everything is an oscillator, but in this context, users expect 'oscillation' to be synonymous with regular periodicity.-->

Random and Journey modes conjure autonomous entities moving in screen space. Let your figure or pattern wander through the video world, or teleport in strobing patterns of random phases. In any mode, you always set the tempo. Even chaos can to step to the beat.

## Key Specifications

| Parameter         | Value                                                                           |
| ----------------- | ------------------------------------------------------------------------------- |
| Mounting Width    | 12 HP                                                                           |
| Power Consumption | 12V @ 150 mA                                                                    |
| Power Connectors  | 16 pin EuroRack ribbon, 2.1mm DC barrel                                         |
| Video Sync        | Rear RCA                                                                        |
| Included          | DC barrel power cable, EuroRack power cable, RCA sync cable                     |

---

## System Integration Advice

Scrolls is a unique and powerful engine for generative video synthesis. In a pure generative synthesis pipeline, Scrolls is an essential element. It can take your work in many new directions.

At the most fundamental level, Scrolls allows smooth horizontal motion. In analog generative video synthesis, vertical motion is easy. Just tune an oscillator to a frequency in the low audio range. But smooth horizontal motion can be difficult with conventional analog oscillators due to instability at high frequencies. There is a workaround involving an LFO and wavefolding, but that introduces horizontal pattern symmetry whether you like it or not.

Lacking horizontal motion, our creative options are super limited. Scrolls solves this problem with high precision digital waveforms. It's an essential tool for taking generative video beyond the basics. The various modes give you many tools for creating engaging real-time animation, and the synchronized CV outputs expand those possibilities in countless ways.

Scrolls is the cornerstone of a generative video system. It provides the base fabric on which rich tapestries can be woven. Other important modules in such a system might include DSG3, DWO3, Stairs, Keychain, Contour, and Stacker.

---

## Controls, Connectors & Indicators

<img src={scrolls_controls_and_connectors} alt="Scrolls controls and connectors" />

&nbsp;<br />

Scrolls is a rhythm source, almost like the visual version of a drum machine. It packs a great deal of functionality into a small package of 12 HP, with no menu diving.

Two identical submodules, **Ramp 1** and **Ramp 2**, provide independent inputs and outputs. 

The primary global **Mode** of Scrolls is chosen from the eight-position rotary switch in the center of the panel. This selects whether H or V signals are available from the video generator jacks, and how all motion is controlled.

Two three-position toggle switches choose other global options. The top switch selects the **Speed** mode. The switch directly below that selects the **Waveform** mode.

As the primary driver of a generative video patch, Scrolls features numerous outputs. The two bottom rows of jacks are the video waveform generators. Each Ramp submodule provides the following outputs: **Ramp** (rising), **Pulse**, **Sawtooth** (falling), and **Sine**.

Above the video outputs is a row of low frequency control voltage outputs. Each Ramp submodule features two CV outputs, labeled **A** and **B**.

Per each Ramp Submodule, a bipolar **Phase** potentiometer shifts the position of the generator, or controls the motion in some other way. The Phase value can be driven by a control voltage supplied to the **CV** jack. The incoming phase CV is multiplied by the value set with the **Phase CV Depth** attenuverter potentiometer.

---

## Operation

<img src={scrolls_ramp_outputs} alt="Scrolls: video waveforms" />

<img src={scrolls_synchronous_lfos} alt="Scrolls: CV outputs" />

---

### Speed

Choose from three ranges of motion speeds. The toggle switch selects one of three modes, from left to right: **Motion Disabled**, **Slow Range**, and **Fast Range**.

<img src={scrolls_hv_blank_three_speeds} alt="Scrolls: Speed range" />

---

### Waveform

Choose from three waveform modes. The toggle switch selects one of three modes, from left to right: **Wrap**, **Blank**, and **Mirror**. 

#### Wrap

The ramp phase scrolls continuously, repeating across the screen.

<img src={scrolls_motion_disabled_wrap} alt="Scrolls: Wrap waveform" />

#### Blank

The ramp phase can be shifted entirely offscreen.

<img src={scrolls_motion_disabled_blank} alt="Scrolls: Blank waveform" />

#### Mirror

The ramp phase inverts on every other cycle. The result is a scrolling virtual canvas, double the width and double the height of the video image.

<img src={scrolls_motion_disabled_mirror} alt="Scrolls: Mirror waveform" />

&nbsp;<br />

:::note
In HD timing formats, a 20ns black line is visible when the ramp reflects from positive to negative slopes. This is known behavior.
:::

---

### Motion Control Modes

#### HH: Double Horizontal

Both Ramp 1 and Ramp 2 are horizontal, with separate Phase controls.

#### VV: Double Vertical

Both Ramp 1 and Ramp 2 are vertical, with separate Phase controls.

#### HV: Horizontal & Vertical

Ramp 1 is horizontal, Ramp 2 is vertical.

<img src={scrolls_hv_scroll} alt="Scrolls: HV mode" />

#### PP: Ping Pong

Ramp 1 is horizontal, Ramp 2 is vertical. Motion uses triangle waveforms, for the bouncing DVD player logo effect.

<img src={scrolls_ping_pong} alt="Scrolls: Ping-pong mode" />

#### O: Orbital

Ramp 1 is horizontal, Ramp 2 is vertical. Motion uses a quadrature sine wave generator to animate the ramps in an elliptical orbit matching the aspect ratio of the video frame. Phase 1 controls speed, Phase 2 controls depth.

<img src={scrolls_orbit} alt="Scrolls: Orbital mode" />

#### J: Journey

Ramp 1 is horizontal, Ramp 2 is vertical. Motion is similar to HV mode, but speed and direction are based on polar instead of cartesian coordinates. Phase 1 controls angle, Phase 2 controls velocity.

<img src={scrolls_journey_phase_1} alt="Scrolls: Journey mode Phase 1" />

&nbsp;<br />

<img src={scrolls_journey_phase_2} alt="Scrolls: Journey mode Phase 2" />

#### C: Corner

Ramp 1 is horizontal, Ramp 2 is vertical. Motion is similar to Orbital mode, but utilizes trapezoidal rather than sinusoidal waveforms. Phase 1 controls speed, Phase 2 controls depth.

<img src={scrolls_corner} alt="Scrolls: Corner mode" />

#### R?: Random

Ramp 1 is horizontal, Ramp 2 is vertical. Phase 1 controls speed, Phase 2 controls depth. 

One of two random modes is selected by the rotation of Phase 2. Speed and position are random when Phase 2 is turned clockwise, to the right of 12 o'clock. 

<img src={scrolls_random_cw} alt="Scrolls: Random mode, Phase 2 clockwise" />

&nbsp;<br />

Angle of movement is random when Phase 2 is turned counter-clockwise, to the left of 12 o'clock. 

<img src={scrolls_random_ccw} alt="Scrolls: Random mode, Phase 2 counter-clockwise" />

---

## Example Patches

### Reset DWO3
<img src={scrolls_dwo3_reset} alt="Scrolls patch: DWO3 reset" />

---

### Stairs

<img src={scrolls_stairs_oscillator} alt="Scrolls patch: Stairs" />

---

## Installation

<img src={scrolls_mounting_power_sync} alt="Scrolls installation" />

<!-- Something about making sure all screws have been removed from the intended mounting location. -->

### Requirements

* EuroRack enclosure
* 12V DC or EuroRack power supply
* 2.1mm DC barrel power cable **or** a EuroRack power cable (both options included)
* Four M2.5 x 6mm mounting screws, or screws provided or specified by the enclosure manufacturer
* #1 Phillips head screwdriver, or hand tool provided or specified by the enclosure manufacturer

### Procedure

* Power off and disconnect the EuroRack enclosure's power supply and any attached DC adapters.
* Connect either the EuroRack Power Cable **or** the DC Barrel Power Cable to the module. Do not connect both Eurorack and DC Barrel power.
* Ensure that no mounting screws are in any holes in the area where you wish to mount the module.
* Carefully test fit the module with its attached power cable in the open space in the EuroRack enclosure. If it is obstructed by the enclosure or any internal assemblies, abort this procedure.
* Connect the disconnected end of the power cable to the power supply.
* Connect the sync cable to a sync source or the last module in the sync chain.
* Mount the module to the EuroRack rails using all mounting holes.
* Store the unused cable along with the product box in a safe location. 
* Power on the EuroRack enclosure and start patching.

---

## Full Specifications

<!-- AFR note: the following illustration is a screen capture from the product page. It should probably be recreated at full resolution, therefore I've given it the filename 'dsg3_line_art_labeled_placeholder_330x684.png' -->

<!-- AFR note: Markdown doesn't support inline tables, so I was forced to use HTML -->

<table>

<tr><th>&nbsp;</th><th>Connectors</th><th>Controls</th></tr>
<tr><td>

<img src={scrolls_line_art_labeled} alt="Scrolls: labeled front panel controls" />

</td><td>

| Jack | Function         |
|------|------------------|
| J1   | Phase 1 CV in    |
| J2   | Phase 2 CV in    |
| J3   | CV 1A out        |
| J4   | CV 1B out        |
| J5   | CV 2A out        |
| J6   | CV 2B out        |
| J7   | Ramp 1 out       |
| J8   | Pulse 1 out      |
| J9   | Ramp 2 out       |
| J10  | Pulse 2 out      |
| J11  | Saw 1 out        |
| J12  | Tri 1 out        |
| J13  | Saw 2 out        |
| J14  | Tri 2 out        |

</td><td>

| Control | Function         |
|---------|------------------|
| S1      | Speed            |
| S2      | Waveform         |
| S3      | Mode             |
| P1      | Phase 1          |
| P2      | Phase 2          |
| P3      | Phase 1 CV Depth |
| P4      | Phase 2 CV Depth |

</td></tr></table>

<!--

### Technical Data

| Parameter                    | Value                                                                           |
| ---------------------------- | ------------------------------------------------------------------------------- |
| Manufacturer Part Number     | 950001                                                                          |
| Pronunciation                |                                                                                 |
| Mounting Width               | 12 HP                                                                           |
| Mounting Depth               | 42 mm                                                                           |
| Mounting Hole Count          | 4                                                                               |
| Power Consumption            | 12V @ 150 mA                                                                    |
| Power Connectors             | 16 pin EuroRack ribbon, 2.1mm DC barrel                                         |
| Input Impedance              | 1M ohms                                                                         |
| Output Impedance             | 75 ohms                                                                         |
| Input Protection Range       | +/-20V                                                                          |
| Input Clipping Range         | +/-2.5V                                                                         |
| Output Range                 | +/-2.5V                                                                         |
| Propagation Delay            | TODO                                                                            |
| Bandwidth @ -3dB             | TODO                                                                            |
| Module Width                 | TODO mm                                                                         |
| Module Height                | TODO mm                                                                         |
| Module Depth                 | TODO mm                                                                         |
| Product Box Width            | TODO in / TODO mm                                                               |
| Product Box Height           | TODO in / TODO mm                                                               |
| Product Box Depth            | TODO in / TODO mm                                                               |
| Product Weight               | TODO                                                                            |
| Included                     | DC barrel power cable, EuroRack power cable, RCA sync cable                     |
| EuroRack Power Cable Type    | 16-pin                                                                          |
| EuroRack Power Cable Length  | 25 cm                                                                           |
| DC Barrel Power Cable Length | 25 cm                                                                           |
| RoHS Compliance              | Manufactured with lead-free processes.                                          |
| Video Sync                   | Rear RCA                                                                        |

-->

---

## Calibration

Calibration is not required for this module.

---

## Maintenance

Keep your module free of dust and debris by performing periodic cleaning. Spots may be cleaned from the frontpanel with a microfiber cloth and isopropyl alcohol or other electronics cleaner.

<!-- ## Troubleshooting -->

---

## Hardware Revisions

The hardware revision code is printed on the circuit board visible from the rear of the module.

---

## Firmware

Scrolls Firmware 1.0.1 (ZIP)

Should I Update My Firmware?
If your serial number is below #50, you should update your firmware to version 1.0.1, available for download on this page. This will fix compatibility issues with progressive sync timings. Firmware update instructions are included in the download.
