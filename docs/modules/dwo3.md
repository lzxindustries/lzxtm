---
draft: true
title: "DWO3: Dual Wideband Oscillator"
---

:::warning
This page is a draft under construction. Stay tuned to our newsletter for the official content release.
:::

<!--
import dwo3_frontpanel from '/img/modules/dwo3/dwo3-diagrams/dwo3_frontpanel.png';
-->

import dwo3_line_art_labeled from '/img/modules/dwo3/dwo3-diagrams/dwo3_line_art_labeled_496x1024.png';

# DWO3
<span class="head2_nolink">Dual Wideband Oscillator</span>

{/*
<img src={dwo3_frontpanel} alt="DWO3 front panel" />
*/}

## Overview

- Two discrete analog triangle core VCOs
- Four classic waveforms for video synthesis
  - sine
  - square
  - sawtooth
  - triangle
- Frequencies from several seconds to 2 MHz
- Eight frequency range / video sync modes
  - Locked Horizontal
  - Locked Upper Vertical 
  - Locked Lower Vertical 
  - Seconds
  - Frames
  - Free Lower Vertical
  - Free Upper Vertical
  - Free Horizontal
- Exponential CV input covers a 100:1 tuning ratio for each frequency range
- External clock inputs
  - Phase reset in locked ranges
  - Gated reset in unlocked ranges

---

## Key Specifications

|                   |                                                                                 |
| ----------------- | ------------------------------------------------------------------------------- |
| Mounting Width    | 12 HP                                                                           |
| Power Consumption | 12V @ 230 mA                                                                    |
| Power Connectors  | 16 pin EuroRack ribbon, 2.1mm DC barrel                                         |
| Included          | DC barrel power cable, EuroRack power cable, RCA sync cable                     |
| Video Sync        | Rear RCA in & out                                                               |

---

## System Integration Advice

Oscillators are essential components of any video synthesizer. The exceptionally wide frequency range of DWO3 allows it to function as a frame-locked or chaotic pattern generator and a low frequency animation controller.

<!--

## Controls, Connectors & Indicators

TODO

---

## Operation

TODO

---

## Example Patches

TODO

-->

---

## Installation

<!--
<img src={dwo3_mounting_power_sync} alt="DWO3 installation" />
-->

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

<table>

<tr><th>&nbsp;</th><th>Connectors</th><th>Controls</th></tr>
<tr><td>

<img src={dwo3_line_art_labeled} alt="DWO3: labeled front panel controls" />

</td><td>

| Jack | Function                               |
|------|----------------------------------------|
| J1   | Osc 1 Exponential Frequency CV in      |
| J2   | Osc 2 Exponential Frequency CV in      |
| J3   | Osc 1 Reset in                         |
| J4   | Osc 1 Linear <br />Frequency CV in     |
| J5   | Osc 2 Reset in                         |
| J6   | Osc 2 Linear <br />Frequency CV in     |
| J7   | Osc 1 Sine out                         |
| J8   | Osc 1 Square out                       |
| J9   | Osc 1 Sine out                         |
| J10  | Osc 2 Square out                       |
| J11  | Osc 1 Sawtooth out <br />(rising ramp) |
| J12  | Osc 1 Triangle out                     |
| J13  | Osc 1 Sawtooth out <br />(rising ramp) |
| J14  | Osc 1 Triangle out                     |

</td><td>

| Switch | Function         |
|--------|------------------|
| S1     | Osc 1 Range      |
| S2     | Osc 2 Range      |

| Pot    | Function                             |
|--------|--------------------------------------|
| P1     | Osc 1 Frequency                      |
| P2     | Osc 2 Frequency                      |
| P3     | Osc 1 Exponential Frequency CV Depth |
| P4     | Osc 2 Exponential Frequency CV Depth |

</td></tr></table>

### Technical Data

|                              |                                                                                 |
| ---------------------------- | ------------------------------------------------------------------------------- |
| Manufacturer Part Number     | 950040                                                                          |
| Mounting Width               | 12 HP                                                                           |
| Mounting Depth               | 42 mm                                                                           |
| Mounting Hole Count          | 4                                                                               |
| Power Consumption            | 12V @ 230 mA                                                                    |
| Power Connectors             | 16 pin EuroRack ribbon, 2.1mm DC barrel                                         |
| Input Impedance              | 1M ohms                                                                         |
| Output Impedance             | 75 ohms                                                                         |
| Input Protection Range       | +/-20V                                                                          |
| Input Clipping Range         | +/-2.5V                                                                         |
| Output Range                 | +/-2.5V                                                                         |
| Included                     | DC barrel power cable, EuroRack power cable, RCA sync cable                     |
| EuroRack Power Cable Type    | 16-pin                                                                          |
| EuroRack Power Cable Length  | 25 cm                                                                           |
| DC Barrel Power Cable Length | 25 cm                                                                           |
| RoHS Compliance              | Manufactured with lead-free processes.                                          |
| Video Sync                   | Rear RCA in & out                                                               |

<!--
| Pronunciation                |                                                                                 |
| Propagation Delay            | TODO                                                                            |
| Bandwidth @ -3dB             | TODO                                                                            |
| Module Width                 | TODO mm                                                                         |
| Module Height                | TODO mm                                                                         |
| Module Depth                 | TODO mm                                                                         |
| Product Box Width            | TODO in / TODO mm                                                               |
| Product Box Height           | TODO in / TODO mm                                                               |
| Product Box Depth            | TODO in / TODO mm                                                               |
| Product Weight               | TODO                                                                            |
-->

---

<!--
## Calibration

Calibration is not required for this module.

---
-->

## Maintenance

Keep your module free of dust and debris by performing periodic cleaning. Spots may be cleaned from the frontpanel with a microfiber cloth and isopropyl alcohol or other electronics cleaner.

---

<!-- ## Troubleshooting -->

## Hardware Revisions

The hardware revision code is printed on the circuit board visible from the rear of the module.
