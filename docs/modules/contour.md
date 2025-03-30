---
draft: true
title: "CONTOUR"
---

:::warning
This page is a draft under construction. Stay tuned to our newsletter for the official content release.
:::

<!--
import contour_frontpanel from '/img/modules/contour/contour-diagrams/contour_frontpanel.png';
-->

import contour_line_art_labeled from '/img/modules/contour/contour-diagrams/contour_line_art_labeled_336x1024.png';

# CONTOUR

<!--
<img src={contour_frontpanel} alt="Contour front panel" />
-->

## Overview

Contour is a triple voltage controlled high pass filter for extracting edge transitions from video images and patterns.

:::note
Due to the inherent geometry of the video raster, high frequency analog filters are only effective on transitions in the horizontal dimension. Affecting transitions in the vertical dimension, between adjacent scanlines, would require a digital frame buffer.
:::

## Key Specifications

|                   |                                                                                 |
| ----------------- | ------------------------------------------------------------------------------- |
| Mounting Width    | 8 HP                                                                            |
| Power Consumption | 12V @ 110 mA                                                                    |
| Power Connectors  | 16 pin EuroRack ribbon, 2.1mm DC barrel                                         |
| Included          | DC barrel power cable, EuroRack power cable                                     |
| Video Sync        | None                                                                            |

---

<!--

## System Integration Advice

TODO

---

## Controls, Connectors & Indicators

---

## Operation

TODO

---

## Example Patches

---

-->

## Installation

<!--
<img src={contour_mounting_power_sync} alt="Contour installation" />
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
* Mount the module to the EuroRack rails using all mounting holes.
* Store the unused cable along with the product box in a safe location. 
* Power on the EuroRack enclosure and start patching.

---

## Full Specifications

<!-- AFR note: the following illustration is a screen capture from the product page. It should probably be recreated at full resolution, therefore I've given it the filename 'proc_line_art_labeled_placeholder_250x700.png' -->

<table>

<tr><th>&nbsp;</th><th>Connectors</th><th>Controls</th></tr>
<tr><td>

<img src={contour_line_art_labeled} alt="Contour: labeled front panel controls" />

</td><td>

| Jack | Function                    |
|------|-----------------------------|
| J1   | Filter 1 Cutoff <br />CV in |
| J2   | Filter 1 in                 |
| J3   | Filter 1 out                |
| J4   | Filter 2 Cutoff <br />CV in |
| J5   | Filter 2 in                 |
| J6   | Filter 2 out                |
| J7   | Filter 3 Cutoff <br />CV in |
| J8   | Filter 3 in                 |
| J9   | Filter 3 out                |

</td><td>

| Potentiometer | Function                       |
|---------------|--------------------------------|
| P1            | Filter 1 Cutoff <br />CV Depth |
| P2            | Filter 1 Cutoff                |
| P3            | Filter 2 Cutoff <br />CV Depth |
| P4            | Filter 2 Cutoff                |
| P5            | Filter 3 Cutoff <br />CV Depth |
| P6            | Filter 3 Cutoff                |

</td></tr></table>

### Technical Data

|                              |                                                                                 |
| ---------------------------- | ------------------------------------------------------------------------------- |
| Manufacturer Part Number     | 950037                                                                          |
| Mounting Depth               | 32 mm                                                                           |
| Mounting Hole Count          | 4                                                                               |
| Power Consumption            | 12V @ 110 mA                                                                    |
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

<!-- ## Troubleshooting -->

---

## Hardware Revisions

The hardware revision code is printed on the circuit board visible from the rear of the module.
