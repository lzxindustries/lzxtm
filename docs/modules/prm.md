---
draft: false
title: "PRM: Programmable Rectifier & Multiplier"
---

import prm_front_panel from '/img/modules/prm/prm-diagrams/prm_front-panel.png';
import prm_all_front_panels from '/img/modules/prm/prm-diagrams/prm_all-front-panels.png';
import prm_controls_connectors_indicators from '/img/modules/prm/prm-diagrams/prm_controls-connectors-indicators.png';
import prm_mounting_power_sync from '/img/modules/prm/prm-diagrams/prm_mounting-power-sync.png';
import prm_exponential_amplifier from '/img/modules/prm/prm-diagrams/prm_exponential-amplifier.png';
import prm_four_quadrant_multiplier from '/img/modules/prm/prm-diagrams/prm_four-quadrant-multiplier.png';
import prm_two_quadrant_multiplier from '/img/modules/prm/prm-diagrams/prm_two-quadrant-multiplier.png';
import prm_one_quadrant_multiplier from '/img/modules/prm/prm-diagrams/prm_one-quadrant-multiplier.png';
import prm_half_wave_rectifier from '/img/modules/prm/prm-diagrams/prm_half-wave-rectifier.png';
import prm_full_wave_rectifier from '/img/modules/prm/prm-diagrams/prm_full-wave-rectifier.png';
import prm_half_wave_inverter from '/img/modules/prm/prm-diagrams/prm_half-wave-inverter.png';

# PRM
<span class="head2_nolink">Programmable Rectifier & Multiplier</span>

## Overview

<img src={prm_front_panel} alt="prm_front_panel" />

## Key Specifications

| Parameter         | Value                                                                           |
| ----------------- | ------------------------------------------------------------------------------- |
| Mounting Width    | 4 HP                                                                            |
| Power Consumption | 12V @ 75mA                                                                      |
| Power Connectors  | 10 pin EuroRack ribbon, 2.1mm DC barrel                                         |
| Video Sync        | None                                                                            |
| Included          | DC barrel power cable, EuroRack power cable, red panel, green panel, blue panel |

## Front Panel Options

PRM ships with a black front panel installed. Red, green and blue panels are also included. All front panels are printed on both sides, allowing a choice of top-to-bottom or bottom-to-top signal flow.

<img src={prm_all_front_panels} alt="prm_all_front_panels" />

<!-- 
## System Integration Advice -->

<!-- - **Utility module** for mixing and level shifting, covering odd cases where the patch needs just one simple operation.
- **Expander module** to add extra inputs or output processing. Extend the functionality any module. Add one next to your favorite oscillators or RGB functions to expand modulation or signal input options.
- **Building block** for patching complex video synthesis functions. As low level analog computing blocks, several PGOs can be patched together to design a wide range of processing functions, including replicating functions from other modules. However, this level of flexibility comes at the expense of greater system size and more complex patches. Using both lower level and higher level modules is a great strategy for getting the most out of a system.
- **Consider multiple PGOs**. Analog computers provide several instances of summing and difference amplifiers. For example, a bidirectional converter or scaler requires two modules. A triple color space function requires three modules. More complex vector functions will require eight or more. -->

## Controls, Connectors & Indicators

The PRM design was informed by years of studying interfaces common to the building blocks of analog computers and video processing equipment. 

<img src={prm_controls_connectors_indicators} alt="prm_controls_connectors_indicators" />

<!-- 
## Operation -->

<!-- PGO sits at a lower level of abstraction than more complex modules like video shape generators and video keyers. The synthesist is granted full access to the signal path, and the freedom to program a function in discrete steps.

PGO is a *patch-programmable* operator. Its overall function is determined by patch connections rather than switch positions or variable voltages. Connections to specific input and output jacks define operations at different mixing ratios and amounts of gain.

### Understanding Cascading Input Jacks​

PGO uses switched, or normalled, connections between some of its input jacks. With no cable inserted, a signal flows from one input jack to another input jack. This connection is overridden when a cable is inserted. Normalled inputs are indicated on the front panel with arrows.

<img src={NormalledConnections} alt="Normalled Connections"/>

### Difference Amplifier​

A difference amplifier subtracts one voltage from another. It is similar to a differential amplifier, but is specifically optimized to subtract one voltage from another with accuracy.  PGO's amplifier is fully differential, meaning that it has both positive and negative outputs.  

In PGO's implementation, the positive input and negative input of the difference amplifier are each preceded by a four input summing amplifier stage. This configuration allows the user to both add multiple input signals and subtract multiple input signals. Due to the cascaded input switches, the gain of each side of the difference amplifier may be programmed by which jacks are patched and which jacks are left open.

<img src={ProgrammingGain} alt="Programming Gain"/>

### Voltage Reference​

PGO provides a static voltage reference of 1V at its output jack. This level corresponds to a luminance value of white, or to the 100% brightness level of an RGB channel. This reference voltage may be patched anywhere in your system, or back to one of the inputs on PGO.

<img src={ProgrammingOffset} alt="Programming Offset"/> -->

## Example Patches

### Half Wave Rectifier

<img src={prm_half_wave_rectifier} alt="prm_half_wave_rectifier" />

### Half Wave Inverter

<img src={prm_half_wave_inverter} alt="prm_half_wave_inverter" />

### Full Wave Rectifier

<img src={prm_full_wave_rectifier} alt="prm_full_wave_rectifier" />

### Four Quadrant Multiplier

<img src={prm_four_quadrant_multiplier} alt="prm_four_quadrant_multiplier" />

### Two Quadrant Multiplier

<img src={prm_two_quadrant_multiplier} alt="prm_two_quadrant_multiplier" />

### One Quadrant Multiplier

<img src={prm_one_quadrant_multiplier} alt="prm_one_quadrant_multiplier" />

### Exponential Amplifier

<img src={prm_exponential_amplifier} alt="prm_exponential_amplifier" />

## Installation

<img src={prm_mounting_power_sync} alt="prm_mounting_power_sync" />

<!-- Discuss differences between 10 and 16 pin connectors -->
<!-- Something about making sure all screws have been removed from the intended mounting location. -->

### Requirements

* EuroRack enclosure.
* 12V DC or EuroRack power supply.
* 2.1mm DC barrel power cable **or** a EuroRack power cable (both options included).
* Two M2.5 x 6mm mounting screws, or screws provided or specified by the enclosure manufacturer.
* #1 Phillips head screwdriver, or hand tool provided or specified by the enclosure manufacturer.

### Procedure

* Power off and disconnect the EuroRack enclosure's power supply and any attached DC adapters.
* Connect only one of, the EuroRack Power Cable or the DC Barrel Power Cable to the module. 
* Carefully test fit the module with its attached power cable in the open space in the EuroRack enclosure. If it is obstructed by the enclosure or any internal assemblies, abort this procedure.
* Connect the disconnected end of the power cable to the power supply.
* Mount the module to the EuroRack rails using all mounting holes.
* Store the unused cable along with the product box in a safe location. 
* Power on the EuroRack enclosure and start patching.

### Full Specifications 

| Parameter                    | Value                                                                           |
| ---------------------------- | ------------------------------------------------------------------------------- |
| Manufacturer Part Number     | 950066                                                                          |
| Pronunciation                | piː-rɒm                                                                         |
| Mounting Width               | 4 HP                                                                            |
| Mounting Depth               | TODO mm                                                                         |
| Mounting Hole Count          | 2                                                                               |
| Power Consumption            | 12V @ 50 mA                                                                     |
| Power Connectors             | 10 pin EuroRack ribbon, 2.1mm DC barrel                                         |
| Input Impedance              | 1M ohms                                                                         |
| Output Impedance             | 75 ohms                                                                         |
| Input Protection Range       | +/-20V                                                                          |
| Input Clipping Range         | +/-2.5V                                                                         |
| Output Range                 | +/-2.5V                                                                         |
| Propagation Delay            | 32ns                                                                            |
| Bandwidth @ -3dB             | TODO                                                                            |
| Module Width                 | 20.32 mm                                                                        |
| Module Height                | 128.5 mm                                                                        |
| Module Depth                 | TODO mm                                                                         |
| Product Box Width            | 4 in / 101.6 mm                                                                 |
| Product Box Height           | 2 in / 50.8 mm                                                                  |
| Product Box Depth            | 6 in / 152.4 mm                                                                 |
| Product Weight               | TODO                                                                            |
| Included                     | DC barrel power cable, EuroRack power cable, red panel, green panel, blue panel |
| EuroRack Power Cable Type    | 10-pin to 16-pin                                                                |
| EuroRack Power Cable Length  | 25 cm                                                                           |
| DC Barrel Power Cable Length | 25 cm                                                                           |
| RoHS Compliance              | Manufactured with lead-free processes.                                          |
| Video Sync                   | None                                                                            | 

<!-- 
## Calibration -->

<!-- Calibration is not required for this module. -->

## Maintenance

Keep your module free of dust and debris by performing periodic cleaning. Spots may be cleaned from the frontpanel with a microfiber cloth and isopropyl alcohol or other electronics cleaner.

<!-- ## Troubleshooting -->

## Hardware Revisions

The hardware revision code is printed on the circuit board visible from the rear of the module.

### PRM-REVA

Initial prototype. September 2024.

### PRM-REVB

Second prototype. December 2024.

### PRM-REVC

Third prototype. January 2025.

### PRM-REVD

Initial production version. February 2025.

[Download PRM-REVD Schematic Diagram (PDF)](/pdf/modules/prm/PRM-REVD_Schematic_Diagram.pdf)

[Download PRM-REVD Interactive Bill of Materials (ZIP)](/zip/modules/prm/PRM-REVD_Interactive_Bill_of_Materials.zip)

## DIY 

PRM is available as a DIY kit that includes a PCB assembly with pre-assembled SMT components and 4 frontpanel options.  The user must source the through-hole components such as headers and jacks, as well as a suitable power cable for the module.

In the Hardware Revisions section, you will find downloads for the complete schematic and an interactive HTML BOM.

### Bill of Materials

In addition to the PCBs and components included with your DIY kit from LZX, you will need to source the following components from electronics parts vendors.

| Manufacturer                        | Manufacturer Part Number | Description                              | Quantity | Reference Designators                        |
| ----------------------------------- | ------------------------ | ---------------------------------------- | -------- | -------------------------------------------- |
| Wenzhou QingPu Electronics Co., Ltd | WQP-WQP518MA             | 3.5mm Jack Mono Switched                 | 9        | J4, J5, J6, J7, J8, J9, J10, J11, J12        |
|                                     |                          | Pin Header Pitch 0.1in 2X5 Male Shrouded | 1        | J2                                           |
| Wurth Elektronik                    | 694106402002             | DC Jack Vertical 2.1mm Barrel            | 1        | J3                                           |
| Recom Technologies                  | R-78K5.0-0.5             | DC/DC Converter Submodule 5.0V           | 1        | U5                                           | 

### Assembly Instructions

This assembly job is recommended for intermediate level DIYers who are comfortable soldering thru hole joints in close proximity to surface mounted parts.

1. Mount and solder rear facing through hole parts first, in this order: pin header, DC/DC converter, DC barrel jack.
1. Mount and solder front facing jacks next.
2. Attach the frontpanel and secure it with mounting nuts for the jacks.
   
<!-- 
## Functional Testing -->
<!-- 
The following tests are designed to verify the module is functioning as expected after assembly. If you are concerned your module is not operating properly, these tests may be used for self verification before a repair is initiated.  It is also best practice to perform a functional test when selling or purchasing a module on the secondhand market.

### Requirements

- A voltmeter, multimeter or oscilloscope
- 12V power supply or EuroRack power supply
- Patch cables

### Setup

- Connect the module to power and turn on your case
- Prepare to probe the disconnected end of a patch cable -- in these tests, the positive probe should make contact with the tip of the plug, and the negative probe or grounding clip should make contact with the sleeve of the plug

### T1. Test voltage reference

- Verify that the Voltage Reference Out is within +/-2% of 1.00V.

### T2. Test difference amplifier positive inputs

- Connect a cable from the voltage reference output to Difference Amplifier In1+
- Verify that Difference Amplifier Out+ is within +/-2% of +2V.
- Verify that Difference Amplifier Out- is within +/-2% of -2V.

### T3. Test difference amplifier negative inputs

- Connect a cable from the voltage reference output to Difference Amplifier In1-
- Verify that Difference Amplifier Out+ is within +/-2% of -2V.
- Verify that Difference Amplifier Out- is within +/-2% of +2V.

This concludes functional testing. If all steps starting with *Verify...* passed their conditions, your PGO is operating within expected parameters. -->
