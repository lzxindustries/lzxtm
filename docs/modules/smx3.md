---
draft: false
title: "SMX3: 3x3 Matrix Mixer"
---

:::warning
This page is a draft under construction. Stay tuned to our newsletter for the official content release.
:::

import smx3_line_art_labeled from '/img/modules/smx3/smx3-diagrams/smx3_line_art_labeled_496x1024.png';

# SMX3
<span class="head2_nolink">3x3 Matrix Mixer</span>

{/*
<img src={Frontpanel} alt="Frontpanel" />
*/}

## Overview

SMX3 Matrix Mixer is a flexible mixing and routing module with nine inputs and three outputs. Each input can amplify, attenuate, or invert a signal in a range from -2x to +2x.

The inputs form a matrix of three rows and three columns. They're internally normalled, allowing signals to cascade down from one patch point to another. This is the key to many creative operations such as outputting multiple distinct mixes of input signals. For example, send three color components to the top row of inputs, and mix them in any way imaginable for a startling array of colorization options.

SMX3 also excels at adjusting and combining low frequency control signals.

Core functions of SMX3 include:

* Add
* Subtract
* Attenuate
* Amplify
* Invert
* Colorize

---

## Key Specifications

| Parameter         | Value                                                                           |
| ----------------- | ------------------------------------------------------------------------------- |
| Mounting Width    | 12 HP                                                                           |
| Power Consumption | 12V @ 175 mA                                                                    |
| Power Connectors  | 16 pin EuroRack ribbon, 2.1mm DC barrel                                         |
| Included          | DC barrel power cable, EuroRack power cable                                     |
| Video Sync        | None                                                                            |

---

## System Integration Advice

SMX3 is a core element of any complete modular video synthesizer. It's essential for controlling color, either in RGB or YIQ component space.

SMX3 doesn't internally generate any voltages, so it can't bias a signal. It pairs well with modules that provide static voltages, such as Proc, PGO, and Matte. These pairings enable greater creative flexibility. For example, SMX3 + Proc makes it possible to freely mix unipolar and bipolar signals such as YIQ color components from Swatch.

:::note
SMX3 can accept or output both positive and negative voltages. However, many modules such as encoders can't accept any voltage outside the range of zero to +1 volts. 
:::

---


<!--
## Controls & Connectors

---
-->

<!--
## Operation

TODO

---
-->

<!--
## Example Patches

---
-->

## Installation

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
* Mount the module to the EuroRack rails using all mounting holes.
* Store the unused cable along with the product box in a safe location. 
* Power on the EuroRack enclosure and start patching.

---

## Full Specifications

<table>

<tr><th>&nbsp;</th><th>Connectors</th><th>Controls</th></tr>
<tr><td>

<img src={smx3_line_art_labeled} alt="SMX3: labeled front panel controls" />

</td><td>

| Jack | Function                    |
|------|-----------------------------|
| J1   | A1 in                       |
| J2   | B1 in                       |
| J3   | C1 in                       |
| J4   | Mixer 1 out                 |
| J5   | A2 in                       |
| J6   | B2 in                       |
| J7   | C2 in                       |
| J8   | Mixer 2 out                 |
| J9   | A3 in                       |
| J10  | B3 in                       |
| J11  | C3 in                       |
| J12  | Mixer 3 out                |

</td><td>

| Potentiometer | Function                       |
|---------------|--------------------------------|
| P1            | A1 gain                        |
| P2            | B1 gain                        |
| P3            | C1 gain                        |
| P4            | A2 gain                        |
| P5            | B2 gain                        |
| P6            | C2 gain                        |
| P7            | A3 gain                        |
| P8            | B3 gain                        |
| P9            | C3 gain                        |

</td></tr></table>

### Technical Data

| Parameter                    | Value                                                                           |
| ---------------------------- | ------------------------------------------------------------------------------- |
| Manufacturer Part Number     | 950050                                                                          |
| Mounting Width               | 12 HP                                                                           |
| Mounting Depth               | 42 mm                                                                           |
| Mounting Hole Count          | 4                                                                               |
| Power Consumption            | 12V @ 174 mA                                                                    |
| Power Connectors             | 16 pin EuroRack ribbon, 2.1mm DC barrel                                         |
| Input Impedance              | 1M ohms                                                                         |
| Output Impedance             | 75 ohms                                                                         |
| Input Protection Range       | +/-20V                                                                          |
| Input Clipping Range         | +/-2.5V                                                                         |
| Output Range                 | +/-2.5V                                                                         |
| Included                     | DC barrel power cable, EuroRack power cable                                     |
| EuroRack Power Cable Type    | 16-pin                                                                          |
| EuroRack Power Cable Length  | 25 cm                                                                           |
| DC Barrel Power Cable Length | 25 cm                                                                           |
| RoHS Compliance              | Manufactured with lead-free processes.                                          |
| Video Sync                   | None                                                                            |

---

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

<!--
## Calibration

Calibration is not required for this module.

---
-->

## Maintenance

Keep the module free of dust and debris by performing periodic cleaning. Spots may be cleaned from the front panel with a microfiber cloth and isopropyl alcohol or other electronics cleaner.

<!-- 
## Troubleshooting

---
-->

---

## Hardware Revisions

The hardware revision code is printed on the circuit board visible from the rear of the module.
