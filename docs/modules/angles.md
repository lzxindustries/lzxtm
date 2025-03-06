---
draft: true
---

import angles_frontpanel from '/img/modules/angles/angles-diagrams/angles_frontpanel.png';
import angles_15_135_255_300 from '/img/modules/angles/angles-diagrams/angles_15-135-255-300.png';
import angles_45_degree_tilt from '/img/modules/angles/angles-diagrams/angles_45-degree-tilt.png';
import angles_controls_and_connectors from '/img/modules/angles/angles-diagrams/angles_controls-and-connectors.png';
import angles_dwo3_cv from '/img/modules/angles/angles-diagrams/angles_dwo3-cv.png';
import angles_fixed_ratio_mixer from '/img/modules/angles/angles-diagrams/angles_fixed-ratio-mixer.png';
import angles_fixed_ratio_outputs from '/img/modules/angles/angles-diagrams/angles_fixed-ratio-outputs.png';
import angles_mounting_power_sync from '/img/modules/angles/angles-diagrams/angles_mounting-power-sync.png';
import angles_normalled_connections from '/img/modules/angles/angles-diagrams/angles_normalled-connections.png';
import angles_quadrilateral from '/img/modules/angles/angles-diagrams/angles_quadrilateral.png';
import angles_ramp_generator_outputs from '/img/modules/angles/angles-diagrams/angles_ramp-generator-outputs.png';
import angles_rgb_gradient from '/img/modules/angles/angles-diagrams/angles_rgb-gradient.png';
import angles_triangle from '/img/modules/angles/angles-diagrams/angles_triangle.png';

# ANGLES - Fixed Ratio Mixer & Dual Ramp Generator

:::warning

This page is under construction and in a draft state. Stay tuned to our newsletter for the official content release.

:::

<img src={angles_frontpanel} alt="Frontpanel" />
<img src={angles_15_135_255_300} alt="Diagram" />
<img src={angles_45_degree_tilt} alt="Diagram" />
<img src={angles_controls_and_connectors} alt="Diagram" />
<img src={angles_dwo3_cv} alt="Diagram" />
<img src={angles_fixed_ratio_mixer} alt="Diagram" />
<img src={angles_fixed_ratio_outputs} alt="Diagram" />
<img src={angles_mounting_power_sync} alt="Diagram" />
<img src={angles_normalled_connections} alt="Diagram" />
<img src={angles_quadrilateral} alt="Diagram" />
<img src={angles_ramp_generator_outputs} alt="Diagram" />
<img src={angles_rgb_gradient} alt="Diagram" />
<img src={angles_triangle} alt="Diagram" />

## Overview

Angles is a dual SD/HD ramp waveform generator and 24 output fixed ratio mixer.

## Key Specifications

| Parameter         | Value                                                                           |
| ----------------- | ------------------------------------------------------------------------------- |
| Mounting Width    | 12 HP                                                                           |
| Power Consumption | 12V @ 175 mA                                                                    |
| Power Connectors  | 10 pin EuroRack ribbon, 2.1mm DC barrel                                         |
| Video Sync        | Rear RCA input and output                                                       |
| Included          | DC barrel power cable, EuroRack power cable, RCA sync cable                     |

## System Integration Advice

In order to synthesize visual elements with complex geometries, such as vanishing point illusions or polygons, one needs parallel access to separate angles at fixed ratios on independent outputs. For this purpose, a single crossfader or mixer does not go very far, and Angles becomes very powerful. Angles is a great support module to add after your system includes one or more of the following modules: Dual Shape Generator, Dual Wideband Oscillator, Stairs, Keychain. It really shines in 4+ module systems where its outputs can be distributed throughout the patch to multiple destinations.

## Controls, Connectors & Indicators

## Operation

Horizontal and vertical waveform generators are an essential ingredient in most generative patches. Due to this, many patches may feel constrained within a box, with the dimensions of shapes and patterns either oriented at 0 or 90 degrees. Angles offers ratio mixes from 0 to 345 degrees in 15 degree increments across 24 ouputs – that’s over 500 different alternatives to HV. Instead of patching HV, you can now pick any 2 angles.

## Example Patches

## Waveshape Expander

Patch your Dual Oscillator outputs or Dual Shape Generator outputs into Angles’ inputs to expand the number of available waveforms.

## Spatial Reference

Patch any 2 outputs from Angles into your Dual Shape Generator to completely change the orientation of its generated patterns.

## Oscillator Protractor

Patch outputs from Angles into your Dual Oscillator CV inputs to modulate its’ waveforms at different angles.

## Complex Color Field

Patch any 3 outputs from Angles into RGB to create a complex color gradient for use as a background or modulation source.

## Quadrature Expander

Patch the +/-Sin/Cos outputs from a quadrature oscillator into Angles’ four inputs to create a full spread of 24 different output phases.

## Hierarchichal Spatial Reference

Patch any 4 outputs from one Angles to the 4 input on a second Angles module to get a completely different set of 24 perspectives.

## Installation

<!-- Discuss differences between 10 and 16 pin connectors -->
<!-- Discuss sync connection -->
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
| Manufacturer Part Number     | 950036                                                                          |
| Pronunciation                |                                                                                 |
| Mounting Width               | 12 HP                                                                           |
| Mounting Depth               | TODO mm                                                                         |
| Mounting Hole Count          | 4                                                                               |
| Power Consumption            | 12V @ 175 mA                                                                    |
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
| Video Sync                   | Required                                                                        |

## Calibration

Calibration is not required for this module.

## Maintenance

Keep your module free of dust and debris by performing periodic cleaning. Spots may be cleaned from the frontpanel with a microfiber cloth and isopropyl alcohol or other electronics cleaner.

<!-- ## Troubleshooting -->

## Hardware Revisions

The hardware revision code is printed on the circuit board visible from the rear of the module.
