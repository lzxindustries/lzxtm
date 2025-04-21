---
draft: false
title: "SWITCHER: Dual 4x3 Multiplexer"
---

import switcher_line_art_labeled from '/img/modules/switcher/switcher-diagrams/switcher_line_art_labeled_736x1024.png';

:::warning
This page is a draft under construction. Stay tuned to our newsletter for the official content release.
:::

# SWITCHER

{/*
<img src={switcher_front_panel} alt="Switcher front panel" />
*/}

## Overview
<span class="head2_nolink">Dual 4x3 Multiplexer</span>

Switcher is a dual RGB multiplexer inspired by classic broadcast consoles and video mixers.

---

## Key Specifications

| Parameter         | Value                                                                           |
| ----------------- | ------------------------------------------------------------------------------- |
| Mounting Width    | 18 HP                                                                           |
| Power Consumption | 12V @ 210 mA                                                                    |
| Power Connectors  | 16 pin EuroRack ribbon, 2.1mm DC barrel                                         |
| Included          | DC barrel power cable, EuroRack power cable                                     |
| Video Sync        | Rear RCA                                                                        |

---

<!--
## System Integration Advice

TODO

---
-->

<!--
## Controls, Connectors & Indicators

TODO

---
-->

## Operation

### Route Four Sources to Two Outputs
A control block familiar to anyone who has used broadcast consoles and video mixers. Illuminated pushbuttons allow fast manual selection. Patch the two outputs to FKG3 to complete an A/B switching workflow -- or think outside the box and define the signal path in any way you choose.

### Multi-Pane Masks with Video Rate Control
- Behind Switcher's six control inputs are dedicated hard key generators that slice the input signals at 50% gray level. Use ramps, shapes, and video sources to control the multiplexers and explore a world of multi-panel compositions and texture collages.

### Programmable Routing for Any Signal
- When interpreted in arbitrary ways, Switcher can handle many tasks besides switching RGB signals. Use it to select variations of a modulation bus between oscillators, cycle thru ramp generator angles or wave shapes, or different return paths from a feedback loop.

---

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
* Connect the sync cable to a sync source or the last module in the sync chain.
* Mount the module to the EuroRack rails using all mounting holes.
* Store the unused cable along with the product box in a safe location. 
* Power on the EuroRack enclosure and start patching.

---

## Full Specifications

<table>

<tr><th>Front panel</th><th>Connectors</th><th>Connectors <br />and Controls</th></tr>
<tr><td>

<img src={switcher_line_art_labeled} alt="Switcher: labeled front panel controls" />

</td><td>

| Jack | Function                                     |
|------|----------------------------------------------|
| J1   | Select <br />A0 in                           |
| J2   | Select <br />A1 in                           |
| J3   | Select <br />B0 in                           |
| J4   | Select <br />B1 in                           |
| J5   | Disable <br />A in                           |
| J6   | Disable <br />B in                           |
| J7   | 1 Red in                                     |
| J8   | 2 Red in                                     |
| J9   | 3 Red in                                     |
| J10  | 4 Red in                                     |
| J11  | A Red out                                    |
| J12  | B Red out                                    |
| J13  | 1 Green in                                   |
| J14  | 2 Green in                                   |
| J15  | 3 Green in                                   |
| J16  | 4 Green in                                   |

</td><td>

| Jack | Function                                     |
|------|----------------------------------------------|
| J17  | A Green out                                  |
| J18  | B Green out                                  |
| J19  | 1 Blue in                                    |
| J20  | 2 Blue in                                    |
| J21  | 3 Blue in                                    |
| J22  | 4 Blue in                                    |
| J23  | A Blue out                                   |
| J24  | B Blue out                                   |

| Switch | Function         |
|--------|------------------|
| S1     | A1               |
| S2     | A2               |
| S3     | A3               |
| S4     | A4               |
| S5     | B1               |
| S6     | B2               |
| S7     | B3               |
| S8     | B4               |

</td></tr></table>

### Technical Data

| Parameter                    | Value                                                                           |
| ---------------------------- | ------------------------------------------------------------------------------- |
| Manufacturer Part Number     | 950057                                                                          |
| Mounting Width               | 18 HP                                                                           |
| Mounting Depth               | 32 mm                                                                           |
| Mounting Hole Count          | 4                                                                               |
| Power Consumption            | 12V @ 210 mA                                                                    |
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
| RoHS Compliance              | Manufactured with lead-free processes                                           |
| Video Sync                   | Rear RCA in and out                                                             |

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

---

## Hardware Revisions

The hardware revision code is printed on the circuit board visible from the rear of the module.

