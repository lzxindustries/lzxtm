---
draft: false
---

import proc_frontpanel from '/img/modules/proc/proc-diagrams/proc_frontpanel.png';
import proc_adder from '/img/modules/proc/proc-diagrams/proc_adder.png';
import proc_block_diagram from '/img/modules/proc/proc-diagrams/proc_block-diagram.png';
import proc_brightness from '/img/modules/proc/proc-diagrams/proc_brightness.png';
import proc_buffered_multiple from '/img/modules/proc/proc-diagrams/proc_buffered-multiple.png';
import proc_contrast from '/img/modules/proc/proc-diagrams/proc_contrast.png';
import proc_controls_and_connectors from '/img/modules/proc/proc-diagrams/proc_controls-and-connectors.png';
import proc_dsg3_priority_layering from '/img/modules/proc/proc-diagrams/proc_dsg3-priority-layering.png';
import proc_formula from '/img/modules/proc/proc-diagrams/proc_formula.png';
import proc_gain_bias from '/img/modules/proc/proc-diagrams/proc_gain-bias.gif';
import proc_inverter from '/img/modules/proc/proc-diagrams/proc_inverter.png';
import proc_modulation_mixer from '/img/modules/proc/proc-diagrams/proc_modulation-mixer.png';
import proc_mounting_power_sync from '/img/modules/proc/proc-diagrams/proc_mounting-power-sync.png';
import proc_normalled_connections from '/img/modules/proc/proc-diagrams/proc_normalled-connections.png';
import proc_ramp_shifter from '/img/modules/proc/proc-diagrams/proc_ramp-shifter.gif';
import proc_ramp_shifter_static from '/img/modules/proc/proc-diagrams/proc_ramp-shifter.png';
import proc_rgb_color_picker from '/img/modules/proc/proc-diagrams/proc_rgb-color-picker.gif';
import proc_rgb_color_picker_static from '/img/modules/proc/proc-diagrams/proc_rgb-color-picker.png';
import proc_static_voltage_generator from '/img/modules/proc/proc-diagrams/proc_static-voltage-generator.gif';
import proc_subtractor from '/img/modules/proc/proc-diagrams/proc_subtractor.png';

# PROC - Triple Voltage Processor

:::warning

This page is under construction and in a draft state. Stay tuned to our newsletter for the official content release.

:::

<img src={proc_frontpanel} alt="Frontpanel" />
<img src={proc_adder} alt="Diagram" />
<img src={proc_block_diagram} alt="Diagram" />
<img src={proc_brightness} alt="Diagram" />
<img src={proc_buffered_multiple} alt="Diagram" />
<img src={proc_contrast} alt="Diagram" />
<img src={proc_controls_and_connectors} alt="Diagram" />
<img src={proc_dsg3_priority_layering} alt="Diagram" />
<img src={proc_formula} alt="Diagram" />
<img src={proc_gain_bias} alt="Diagram" />
<img src={proc_inverter} alt="Diagram" />
<img src={proc_modulation_mixer} alt="Diagram" />
<img src={proc_mounting_power_sync} alt="Diagram" />
<img src={proc_normalled_connections} alt="Diagram" />
<img src={proc_ramp_shifter} alt="Diagram" />
<img src={proc_ramp_shifter_static} alt="Diagram" />
<img src={proc_rgb_color_picker} alt="Diagram" />
<img src={proc_rgb_color_picker_static} alt="Diagram" />
<img src={proc_static_voltage_generator} alt="Diagram" />
<img src={proc_subtractor} alt="Diagram" />

## Overview

Proc is a triple voltage processor and summing amplifier. For each channel, it provides continuous control over inversion, attenuation, and DC offset.

## Key Specifications

| Parameter         | Value                                       |
| ----------------- | ------------------------------------------- |
| Mounting Width    | 8 HP                                        |
| Power Consumption | 12V @ 110 mA                                |
| Power Connectors  | 16 pin EuroRack ribbon, 2.1mm DC barrel     |
| Video Sync        | None                                        |
| Included          | DC barrel power cable, EuroRack power cable |

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

| Parameter                    | Value                                       |
| ---------------------------- | ------------------------------------------- |
| Manufacturer Part Number     | 950048                                      |
| Pronunciation                |                                             |
| Mounting Width               | 8 HP                                        |
| Mounting Depth               | 32 mm                                       |
| Mounting Hole Count          | 4                                           |
| Power Consumption            | 12V @ 110 mA                                |
| Power Connectors             | 16 pin EuroRack ribbon, 2.1mm DC barrel     |
| Input Impedance              | 1M ohms                                     |
| Output Impedance             | 75 ohms                                     |
| Input Protection Range       | +/-20V                                      |
| Input Clipping Range         | +/-2.5V                                     |
| Output Range                 | +/-2.5V                                     |
| Propagation Delay            | TODO                                        |
| Bandwidth @ -3dB             | TODO                                        |
| Module Width                 | TODO mm                                     |
| Module Height                | TODO mm                                     |
| Module Depth                 | TODO mm                                     |
| Product Box Width            | TODO in / TODO mm                           |
| Product Box Height           | TODO in / TODO mm                           |
| Product Box Depth            | TODO in / TODO mm                           |
| Product Weight               | TODO                                        |
| Included                     | DC barrel power cable, EuroRack power cable |
| EuroRack Power Cable Type    | 16-pin                                      |
| EuroRack Power Cable Length  | 25 cm                                       |
| DC Barrel Power Cable Length | 25 cm                                       |
| RoHS Compliance              | Manufactured with lead-free processes.      |
| Video Sync                   | None                                        |

## Calibration

Calibration is not required for this module.

## Maintenance

Keep your module free of dust and debris by performing periodic cleaning. Spots may be cleaned from the frontpanel with a microfiber cloth and isopropyl alcohol or other electronics cleaner.

<!-- ## Troubleshooting -->

## Hardware Revisions

The hardware revision code is printed on the circuit board visible from the rear of the module.
