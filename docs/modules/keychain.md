---
draft: true
---


import keychain_frontpanel from '/img/modules/keychain/keychain-diagrams/keychain_frontpanel.png';
import keychain_block_diagram from '/img/modules/keychain/keychain-diagrams/keychain_block-diagram.png';
import keychain_controls_and_connectors from '/img/modules/keychain/keychain-diagrams/keychain_controls-and-connectors.png';
import keychain_cv_mult from '/img/modules/keychain/keychain-diagrams/keychain_cv-mult.png';
import keychain_input_mult from '/img/modules/keychain/keychain-diagrams/keychain_input-mult.png';
import keychain_lfo_threshold from '/img/modules/keychain/keychain-diagrams/keychain_lfo-threshold.gif';
import keychain_linear_wipe from '/img/modules/keychain/keychain-diagrams/keychain_linear-wipe.gif';
import keychain_mounting_power_sync from '/img/modules/keychain/keychain-diagrams/keychain_mounting-power-sync.png';
import keychain_normalled_connections from '/img/modules/keychain/keychain-diagrams/keychain_normalled-connections.png';
import keychain_threshold_concept from '/img/modules/keychain/keychain-diagrams/keychain_threshold-concept.png';

# KEYCHAIN - Triple Hard Key Generator

:::warning

This page is under construction and in a draft state. Stay tuned to our newsletter for the official content release.

:::

<img src={keychain_frontpanel} alt="Frontpanel" /> 
<img src={keychain_block_diagram} alt="Diagram" /> 
<img src={keychain_controls_and_connectors} alt="Diagram" /> 
<img src={keychain_cv_mult} alt="Diagram" /> 
<img src={keychain_input_mult} alt="Diagram" /> 
<img src={keychain_lfo_threshold} alt="Diagram" /> 
<img src={keychain_linear_wipe} alt="Diagram" /> 
<img src={keychain_mounting_power_sync} alt="Diagram" /> 
<img src={keychain_normalled_connections} alt="Diagram" /> 
<img src={keychain_threshold_concept} alt="Diagram" /> 

## Overview

Keychain is a triple hard key generator. Using voltage comparators with a 7ns response time, this module can generate sharp edged stencil shapes from any video or pattern generator source.

## Key Specifications

| Parameter         | Value                                                                           |
| ----------------- | ------------------------------------------------------------------------------- |
| Mounting Width    | 8 HP                                                                            |
| Power Consumption | 12V @ 110 mA                                                                    |
| Power Connectors  | 16 pin EuroRack ribbon, 2.1mm DC barrel                                         |
| Video Sync        | None                                                                            |
| Included          | DC barrel power cable, EuroRack power cable                                     |

## System Integration Advice

TODO

## Controls, Connectors & Indicators

## Operation

TODO

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
| Manufacturer Part Number     | 950056                                                                          |
| Pronunciation                |                                                                                 |
| Mounting Width               | 8 HP                                                                            |
| Mounting Depth               | 32 mm                                                                           |
| Mounting Hole Count          | 4                                                                               |
| Power Consumption            | 12V @ 110 mA                                                                    |
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
| Included                     | DC barrel power cable, EuroRack power cable                                     |
| EuroRack Power Cable Type    | 16-pin                                                                          |
| EuroRack Power Cable Length  | 25 cm                                                                           |
| DC Barrel Power Cable Length | 25 cm                                                                           |
| RoHS Compliance              | Manufactured with lead-free processes.                                          |
| Video Sync                   | None                                                                            |

## Calibration

Calibration is not required for this module.

## Maintenance

Keep your module free of dust and debris by performing periodic cleaning. Spots may be cleaned from the frontpanel with a microfiber cloth and isopropyl alcohol or other electronics cleaner.

<!-- ## Troubleshooting -->

## Hardware Revisions

The hardware revision code is printed on the circuit board visible from the rear of the module.
