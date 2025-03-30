---
draft: true
title: "FKG3: Fader & Key Generator"
---

:::warning
This page is a draft under construction. Stay tuned to our newsletter for the official content release.
:::

<!--
import fkg3_frontpanel from '/img/modules/fkg3/fkg3-diagrams/fkg3_frontpanel.png';
-->

import fkg3_panel_labeled from '/img/modules/fkg3/fkg3-diagrams/fkg3_panel_labeled_496x1024.png';

## Overview

FKG3 Keyer serves a wide range of creative image compositing functions.

---

## Key Specifications

|                   |                                                                                 |
| ----------------- | ------------------------------------------------------------------------------- |
| Mounting Width    | 12 HP                                                                           |
| Power Consumption | 12V @ 200 mA                                                                    |
| Power Connectors  | 16 pin EuroRack ribbon, 2.1mm DC barrel                                         |
| Included          | DC barrel power cable, EuroRack power cable, RCA sync cable                     |
| Video Sync        | Rear RCA in & out                                                               |

---

## System Integration Advice

May be expanded by utility modules such as Proc and Matte, becoming the core unit of a color correction and key source processing subsystem.

<!--
---

## Controls, Connectors & Indicators

TODO

-->
---

## Operation

Analog logic based keying modes: Luma Key, Chroma Key Red, Chroma Key Green, and Chroma Key Blue. Softness control sweeps edge response from hard transitions to soft gradients. Patch in monochromatic sources seamlessly via switched RGB input jacks.

<!--
---

## Example Patches

TODO

-->
---

## Installation

<!--
<img src={fkg3_mounting_power_sync} alt="FKG33 installation" />
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

<img src={fkg3_panel_labeled} alt="FKG3: labeled front panel controls" />

</td><td>

| Jack | Function                               |
|------|----------------------------------------|
| J1   | Threshold CV in                        |
| J2   | Softness CV in                         |
| J3   | Red Background in                      |
| J4   | Red Foreground in                      |
| J5   | Red Key in                             |
| J6   | Red out                                |
| J7   | Green Background in                    |
| J8   | Green Foreground in                    |
| J9   | Green Key in                           |
| J10  | Green out                              |
| J11  | Blue Background in                     |
| J12  | Blue Foreground in                     |
| J13  | Blue Key in                            |
| J14  | Blue out                               |

</td><td>

| Switch | Function                             |
|--------|--------------------------------------|
| S1     | Edge mode                            |
| S2     | Source mode                          |
| S3     | Key mode                             |

| Pot    | Function                             |
|--------|--------------------------------------|
| P1     | Threshold                            |
| P2     | Softness                             |
| P3     | Threshold CV Depth                   |
| P4     | Softness CV Depth                    |

</td></tr></table>

|                              |                                                                                 |
| ---------------------------- | ------------------------------------------------------------------------------- |
| Manufacturer Part Number     | 950043                                                                          |
| Mounting Width               | 12 HP                                                                           |
| Mounting Depth               | 42 mm                                                                           |
| Mounting Hole Count          | 4                                                                               |
| Power Consumption            | 12V @ 200 mA                                                                    |
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
| Video Sync                   | Rear RCA                                                                        |

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

Explanation of trim pots and calibration procedure

---
-->

## Maintenance

Keep your module free of dust and debris by performing periodic cleaning. Spots may be cleaned from the frontpanel with a microfiber cloth and isopropyl alcohol or other electronics cleaner.

<!-- ## Troubleshooting -->

---

## Hardware Revisions

The hardware revision code is printed on the circuit board visible from the rear of the module.
