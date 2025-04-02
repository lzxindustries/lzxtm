---
draft: false
title: "MLT: Passive Multiples"
---

import mlt_frontpanel from '/img/modules/mlt/mlt-diagrams/mlt_front-panel.png';
import mlt_controls_connectors_indicators from '/img/modules/mlt/mlt-diagrams/mlt_controls-connectors-indicators.png';
import mlt_mounting_power_sync from '/img/modules/mlt/mlt-diagrams/mlt_mounting-power-sync.png';
import mlt_mults from '/img/modules/mlt/mlt-diagrams/mlt_mults.png';
import mlt_understanding_cascading_input_jacks from '/img/modules/mlt/mlt-diagrams/mlt_understanding-cascading-input-jacks​.png';

# MLT
<span class="head2_nolink">Passive Multiples</span>

<img src={mlt_frontpanel} alt="mlt_frontpanel"/>

<!-- ## Overview -->

## Key Specifications

|                   |                                                                                 |
| ----------------- | ------------------------------------------------------------------------------- |
| Mounting Width    | 4 HP                                                                            |
| Power Consumption | None                                                                            |
| Power Connectors  | None                                                                            |
| Video Sync        | None                                                                            |

---

## Controls, Connectors & Indicators

<img src={mlt_controls_connectors_indicators} alt="mlt_controls_connectors_indicators"/>

---

## Operation

### Understanding Cascading Input Jacks​

MLT uses switched, or normalled, connections between some of its input jacks. With no cable inserted, a signal flows down from one input jack to another. This connection is overridden when a cable is inserted. Normalled inputs are indicated on the front panel with arrows.

<img src={mlt_understanding_cascading_input_jacks} alt="mlt_understanding_cascading_input_jacks"/>

---

## Example Patches

<img src={mlt_mults} alt="mlt_mults"/>

---

## Installation

<img src={mlt_mounting_power_sync} alt="mlt_mounting_power_sync"/>

### Requirements

* EuroRack enclosure.
* Two M2.5 x 6mm mounting screws, or screws provided or specified by the enclosure manufacturer.
* #1 Phillips head screwdriver, or hand tool provided or specified by the enclosure manufacturer.

### Procedure

* Power off and disconnect the EuroRack enclosure's power supply and any attached DC adapters.
* Ensure that no mounting screws are in any holes in the area where you wish to mount the module.
* Carefully test fit the module in the open space in the EuroRack enclosure. If it is obstructed by the enclosure or any internal assemblies, abort this procedure.
* Mount the module to the EuroRack rails using all mounting holes.
* Power on the EuroRack enclosure and start patching.

---

## Full Specifications

|                              |                                                                                 |
| ---------------------------- | ------------------------------------------------------------------------------- |
| Mounting Width               | 4 HP                                                                            |
| Mounting Hole Count          | 2                                                                               |
| Power Consumption            | n/a                                                                             |
| Module Width                 | 20.32 mm                                                                        |
| Module Height                | 128.5 mm                                                                        |
| Product Box Width            | 4 in / 101.6 mm                                                                 |
| Product Box Height           | 2 in / 50.8 mm                                                                  |
| Product Box Depth            | 6 in / 152.4 mm                                                                 |
| RoHS Compliance              | Manufactured with lead-free processes.                                          |
| Video Sync                   | None                                                                            |

<!--
| Manufacturer Part Number     |                                                                                 |
| Mounting Depth               | TODO mm                                                                         |
| Module Depth                 | TODO mm                                                                         |
| Product Weight               | TODO                                                                            |
| Included                     | DC barrel power cable, EuroRack power cable, red panel, green panel, blue panel |
-->

<!-- 
## Calibration -->

<!-- Calibration is not required for this module. -->

## Maintenance

Keep your module free of dust and debris by performing periodic cleaning. Spots may be cleaned from the frontpanel with a microfiber cloth and isopropyl alcohol or other electronics cleaner.

<!-- ## Troubleshooting -->

---

## Hardware Revisions

The hardware revision code is printed on the circuit board visible from the rear of the module.

### MLT-RevA

Initial production version, February 2025

[Download MLT-REVA Schematic Diagram (PDF)](/pdf/modules/mlt/MLT-REVA_Schematic_Diagram.pdf)

[Download MLT-REVA Interactive Bill of Materials (ZIP)](/zip/modules/mlt/MLT-REVA_Interactive_Bill_of_Materials.zip)

---

## DIY 

MLT is available as a DIY kit that includes the main PCB and the front panel.  The user must source the through-hole components such as jacks and potentiometers.

In the Hardware Revisions section, you will find downloads for the complete schematic and an interactive HTML BOM.

### Bill of Materials

In addition to the PCBs and components included with your DIY kit from LZX, you will need to source the following components from electronics parts vendors.

| Manufacturer                        | Manufacturer Part Number | Description                | Quantity | Reference Designators    |
| ----------------------------------- | ------------------------ | -------------------------- | -------- | -------------------------|
| Wenzhou QingPu Electronics Co., Ltd | WQP-WQP518MA             | 3.5mm Jack Mono Switched   | 32       | J1, J2, J3, J4, J5, J6, J7, J8, J9, J10, J11, J12, J13, J14, J15, J16, J17, J18, J19, J20, J21, J22, J23, J24, J25, J26, J27, J28, J29, J30, J31, J32 |

### Assembly Instructions

This assembly job is recommended for intermediate level DIYers who are comfortable soldering thru hole joints in close proximity to surface mounted parts.

1. Mount and solder front facing jacks.
2. Attach the front panel and secure it with mounting nuts for the jacks.