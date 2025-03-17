---
draft: true
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

# SCROLLS
<span class="head2_nolink">Dual Motion Controlled Ramp Generator</span>

:::warning

This page is under construction and in a draft state. Stay tuned to our newsletter for the official content release.

:::

<img src={scrolls_frontpanel} alt="Frontpanel" />
<img src={scrolls_corner} alt="Diagram" />
<img src={scrolls_controls_and_connectors} alt="Diagram" />
<img src={scrolls_dwo3_reset} alt="Diagram" />
<img src={scrolls_hv_blank_three_speeds} alt="Diagram" />
<img src={scrolls_hv_scroll} alt="Diagram" />
<img src={scrolls_journey_phase_1} alt="Diagram" />
<img src={scrolls_journey_phase_2} alt="Diagram" />
<img src={scrolls_motion_disabled_blank} alt="Diagram" />
<img src={scrolls_motion_disabled_mirror} alt="Diagram" />
<img src={scrolls_motion_disabled_wrap} alt="Diagram" />
<img src={scrolls_mounting_power_sync} alt="Diagram" />
<img src={scrolls_orbit} alt="Diagram" />
<img src={scrolls_ping_pong} alt="Diagram" />
<img src={scrolls_ramp_outputs} alt="Diagram" />
<img src={scrolls_random_ccw} alt="Diagram" />
<img src={scrolls_random_cw} alt="Diagram" />
<img src={scrolls_stairs_oscillator} alt="Diagram" />
<img src={scrolls_synchronous_lfos} alt="Diagram" />

## Overview

Scrolls is a motion controlled dual ramp generator module for EuroRack video synthesizers. It provides the synthesist with full control over the screen positioning of its high precision HD/SD dual video waveform generators. Front panel switches provide access to 72 combinatorial states addressing movement speed, waveform blanking and mirroring, and advanced motion paths from elliptical orbit to random exploration.

Most analog video synthesis patches begin with horizontal and vertical ramp waveforms. These generators provide the synthesist with a method of identifying 2D coordinates on the screen. With motion controlled ramps, these 2D coordinates can be repositioned and animated at their source – causing the entire resulting video art pattern to animate.

In addition to motion control over the internal video waveforms, Scrolls presents four dedicated low frequency waveform generators. These signals are synchronous with the movement of the internal ramps, and provide ways to animate other parts of your patch in tempo with the video pattern.

Random and Journey modes provide methods for generating the illusion of autonomous entities within the space of your video composition. Watch your video pattern slowly explore around the screen at random directions, or teleport in strobing patterns of random phases. In all of these modes, the synthesist has control over a basic clock speed, which allows even chaos to step to the beat.

## Key Specifications

| Parameter         | Value                                                                           |
| ----------------- | ------------------------------------------------------------------------------- |
| Mounting Width    | 12 HP                                                                           |
| Power Consumption | 12V @ 150 mA                                                                    |
| Power Connectors  | 16 pin EuroRack ribbon, 2.1mm DC barrel                                         |
| Video Sync        | Rear RCA                                                                        |
| Included          | DC barrel power cable, EuroRack power cable, RCA sync cable                     |

## System Integration Advice

TODO

## Controls, Connectors & Indicators

## HH. Double Horizontal Mode
Both waveform generators are horizontal ramps with separate phase controls.

## VV. Double Vertical Mode
Both waveform generators are vertical ramps with separate phase controls.

## HV. Horizontal & Vertical Mode
The first ramp generator is horizontal and the second ramp generator is vertical.

## PP. Ping Pong Mode
The first ramp generator is horizontal and the second ramp generator is vertical. The motion control algorithm uses triangle waveforms, for the bouncing DVD player logo effect.

## O. Orbital Mode
The first ramp generator is horizontal and the second ramp generator is vertical. The motion control algorithm uses a quadrature sine wave generator to animate the ramps in an elliptical orbit. Phase1 controls motion speed and Phase2 controls motion depth.

## J. Journey Mode
The first ramp generator is horizontal and the second ramp generator is vertical. The motion control algorithm is similar to HV mode, but the manner in which the speed and direction of movement is based on polar instead of cartesian coordinates. Phase1 controls motion angle and Phase2 controls motion velocity.

## C. Corner Mode
The first ramp generator is horizontal and the second ramp generator is vertical. The motion control algorithm is similar to O mode, but utilizes trapezoidal rather than sinusoidal waveforms. Phase1 controls motion speed and Phase2 controls motion depth.

## R?. Random Mode
The first ramp generator is horizontal and the second ramp generator is vertical. The motion control algorithm is different depending on whether Phase2 is counter-clockwise or clockwise from it's midpoint. The clockwise position is random position and speed and the counter-clockwise position is random angle of movement. Phase1 controls motion speed and Phase2 controls motion depth.

## Speed Mode
There are three motion speed modes. From toggle switch positions, left to right: Motion Disabled, Slow Range, Fast Range.

## Waveform Mode
There are three waveform modes. From toggle switch positions, left to right: Wrap, Blank, and Mirror. In Wrap mode, the ramp phase scrolls continuously, repeating across the screen. In Blank mode, the ramp phase may be moved entirely off screen. In Mirror mode, the ramp phase inverts on even numbered cycles, creating an oversized quadrilateral space that is 2x2 screens in size. When used in HD timing formats, there will be a 20ns black line present when the ramp reflects from positive to negative slopes. This is expected behavior.

## Operation

## Example Patches

## Installation

<!-- Something about making sure all screws have been removed from the intended mounting location. -->

### Requirements

* EuroRack enclosure.
* 12V DC or EuroRack power supply.
* 2.1mm DC barrel power cable **or** a EuroRack power cable (both options included).
* Four M2.5 x 6mm mounting screws, or screws provided or specified by the enclosure manufacturer.
* #1 Phillips head screwdriver, or hand tool provided or specified by the enclosure manufacturer.

### Procedure

* Power off and disconnect the EuroRack enclosure's power supply and any attached DC adapters.
* Connect only one of, the EuroRack Power Cable or the DC Barrel Power Cable to the module. 
* Carefully test fit the module with its attached power cable in the open space in the EuroRack enclosure. If it is obstructed by the enclosure or any internal assemblies, abort this procedure.
* Connect the disconnected end of the power cable to the power supply.
* Connect the sync cable to your sync source or the last module in your sync chain
* Mount the module to the EuroRack rails using all mounting holes.
* Store the unused cable along with the product box in a safe location. 
* Power on the EuroRack enclosure and start patching.

## Full Specifications

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

## Calibration

Calibration is not required for this module.

## Maintenance

Keep your module free of dust and debris by performing periodic cleaning. Spots may be cleaned from the frontpanel with a microfiber cloth and isopropyl alcohol or other electronics cleaner.

<!-- ## Troubleshooting -->

## Hardware Revisions

The hardware revision code is printed on the circuit board visible from the rear of the module.

## Firmware

Scrolls Firmware 1.0.1 (ZIP)

Should I Update My Firmware?
If your serial number is below #50, you should update your firmware to version 1.0.1, available for download on this page. This will fix compatibility issues with progressive sync timings. Firmware update instructions are included in the download.
