---
draft: false
---

import stacker_frontpanel from '/img/modules/stacker/stacker-diagrams/stacker_frontpanel.png';
import stacker_block_diagram from '/img/modules/stacker/stacker-diagrams/stacker_block-diagram.png';
import stacker_controls_and_connectors from '/img/modules/stacker/stacker-diagrams/stacker_controls-and-connectors.png';
import stacker_dsg3_proc from '/img/modules/stacker/stacker-diagrams/stacker_dsg3-proc.gif';
import stacker_mounting_power_sync from '/img/modules/stacker/stacker-diagrams/stacker_mounting-power-sync.png';
import stacker_normalled_connections from '/img/modules/stacker/stacker-diagrams/stacker_normalled-connections.png';
import stacker_priority_layering_combo from '/img/modules/stacker/stacker-diagrams/stacker_priority-layering-combo.png';
import stacker_priority_layering_formulas from '/img/modules/stacker/stacker-diagrams/stacker_priority-layering-formulas.png';
import stacker_priority_layering_no_mult from '/img/modules/stacker/stacker-diagrams/stacker_priority-layering-no-mult.png';
import stacker_priority_layering from '/img/modules/stacker/stacker-diagrams/stacker_priority-layering.png';
import stacker_size_ratio_under_the_hood from '/img/modules/stacker/stacker-diagrams/stacker_size-ratio-under-the-hood.gif';
import stacker_size_ratio from '/img/modules/stacker/stacker-diagrams/stacker_size-ratio.gif';

# STACKER - Triple Quadrilateral Key Generator

:::warning

This page is under construction and in a draft state. Stay tuned to our newsletter for the official content release.

:::

<img src={stacker_frontpanel} alt="Frontpanel" />
<img src={stacker_block_diagram} alt="Diagram" />
<img src={stacker_controls_and_connectors} alt="Diagram" />
<img src={stacker_dsg3_proc} alt="Diagram" />
<img src={stacker_mounting_power_sync} alt="Diagram" />
<img src={stacker_normalled_connections} alt="Diagram" />
<img src={stacker_priority_layering_combo} alt="Diagram" />
<img src={stacker_priority_layering_formulas} alt="Diagram" />
<img src={stacker_priority_layering_no_mult} alt="Diagram" />
<img src={stacker_priority_layering} alt="Diagram" />
<img src={stacker_size_ratio_under_the_hood} alt="Diagram" />
<img src={stacker_size_ratio} alt="Diagram" />

## Overview

Stacker is a triple quadrilateral key generator and layer-priority encoder for your modular video synthesizer. Feed Stacker horizontal and vertical waveforms from DWO3, DSG3 or Angles to produce three stacked quadrilateral shapes on the outputs.

## Key Specifications

| Parameter         | Value                                                                           |
| ----------------- | ------------------------------------------------------------------------------- |
| Mounting Width    | 8 HP                                                                            |
| Power Consumption | 12V @ 95 mA                                                                     |
| Power Connectors  | 16 pin EuroRack ribbon, 2.1mm DC barrel                                         |
| Video Sync        | None                                                                            |
| Included          | DC barrel power cable, EuroRack power cable                                     |

## System Integration Advice

TODO

## Controls, Connectors & Indicators

## Operation

**Generate Squares, Rectangles & Rhombi**
- A quadrilateral key generator has 2 inputs (for horizontal and vertical reference waveforms and 4 thresholds (for the top, right, bottom, left borders.) Ratio & Size controls quickly define the 4 thresholds as a group.

**Compose Priority Layered Sprites & Glyphs**
- Each key output is subtracted from the lower layers. This nesting doll effect allows programming of simple letterforms and icons.

**Extract Foreground Fragments From Complex Sources**
- When fed horizontal and vertical references from wave shapers, video cameras, and other complex sources, Stacker serves as a tool for extracting foreground details, tiles and mosaics.


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
| Manufacturer Part Number     | 950051                                                                          |
| Pronunciation                |                                                                                 |
| Mounting Width               | 8 HP                                                                            |
| Mounting Depth               | 32 mm                                                                           |
| Mounting Hole Count          | 4                                                                               |
| Power Consumption            | 12V @ 95 mA                                                                     |
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
