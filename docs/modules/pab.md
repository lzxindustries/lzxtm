---
draft: false
title: "PAB: Programmable Active Buffers"
---

import pab_front_panel from '/img/modules/pab/pab-diagrams/pab_front-panel.png';
import pab_all_front_panels from '/img/modules/pab/pab-diagrams/pab_all-front-panels.png';
import pab_mounting_power_sync from '/img/modules/pab/pab-diagrams/pab_mounting-power-sync.png';
import pab_controls_connectors_indicators from '/img/modules/pab/pab-diagrams/pab_controls-connectors-indicators.png';
import pab_understanding_cascading_input_jacks from '/img/modules/pab/pab-diagrams/pab_understanding-cascading-input-jacks​.png';

# PAB
<span class="head2_nolink">Programmable Active Buffers</span>

## Overview

<img src={pab_front_panel} alt="pab_front_panel" />

## Key Specifications

| Parameter         | Value                                                                           |
| ----------------- | ------------------------------------------------------------------------------- |
| Mounting Width    | 4 HP                                                                            |
| Power Consumption | 12V @ 50mA                                                                      |
| Power Connectors  | 10 pin EuroRack ribbon, 2.1mm DC barrel                                         |
| Video Sync        | None                                                                            |
| Included          | DC barrel power cable, EuroRack power cable, red panel, green panel, blue panel |

## Front Panel Options

PAB ships with a black front panel installed. Red, green and blue panels are also included. All front panels are printed on both sides, allowing a choice of top-to-bottom or bottom-to-top signal flow.

<img src={pab_all_front_panels} alt="pab_all_front_panels" />
<!-- 
## System Integration Advice -->

<!-- - **Utility module** for mixing and level shifting, covering odd cases where the patch needs just one simple operation.
- **Expander module** to add extra inputs or output processing. Extend the functionality any module. Add one next to your favorite oscillators or RGB functions to expand modulation or signal input options.
- **Building block** for patching complex video synthesis functions. As low level analog computing blocks, several PGOs can be patched together to design a wide range of processing functions, including replicating functions from other modules. However, this level of flexibility comes at the expense of greater system size and more complex patches. Using both lower level and higher level modules is a great strategy for getting the most out of a system.
- **Consider multiple PGOs**. Analog computers provide several instances of summing and difference amplifiers. For example, a bidirectional converter or scaler requires two modules. A triple color space function requires three modules. More complex vector functions will require eight or more. -->

## Controls, Connectors & Indicators

<!-- The PAB design was informed by years of studying interfaces common to the building blocks of analog computers and video processing equipment. 

<img src={ControlsConnectorsIndicators} alt="Controls Connectors And Indicators" /> -->

<img src={pab_controls_connectors_indicators} alt="pab_controls_connectors_indicators" />

## Operation

### Understanding Cascading Input Jacks​

<img src={pab_understanding_cascading_input_jacks} alt="pab_understanding_cascading_input_jacks" />

## Installation

<!-- Discuss differences between 10 and 16 pin connectors -->
<!-- Something about making sure all screws have been removed from the intended mounting location. -->

<img src={pab_mounting_power_sync} alt="pab_mounting_power_sync" />

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

## Full Specifications 

| Parameter                    | Value                                                                           |
| ---------------------------- | ------------------------------------------------------------------------------- |
| Manufacturer Part Number     | 950065                                                                          |
| Pronunciation                | pab                                                                             |
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
| Propagation Delay            | 16ns                                                                            |
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

## Calibration -->

<!-- Calibration is not required for this module. -->

## Maintenance

Keep your module free of dust and debris by performing periodic cleaning. Spots may be cleaned from the frontpanel with a microfiber cloth and isopropyl alcohol or other electronics cleaner.

<!-- ## Troubleshooting -->

## Hardware Revisions

The hardware revision code is printed on the circuit board visible from the rear of the module.

### PAB-REVA

Initial prototype. January 2025.

### PAB-REVB

Initial production version. February 2025.

[Download PAB-REVB Schematic Diagram (PDF)](/pdf/modules/pab/PAB-REVB_Schematic_Diagram.pdf)

[Download PAB-REVB Interactive Bill of Materials (ZIP)](/zip/modules/pab/PAB-REVB_Interactive_Bill_of_Materials.zip)

## DIY 

PAB is available as a DIY kit that includes a PCB assembly with pre-assembled SMT components and 4 frontpanel options.  The user must source the through-hole components such as headers and jacks, as well as a suitable power cable for the module.

In the Hardware Revisions section, you will find downloads for the complete schematic and an interactive HTML BOM.

### Bill of Materials

In addition to the PCBs and components included with your DIY kit from LZX, you will need to source the following components from electronics parts vendors.

| Manufacturer                        | Manufacturer Part Number | Description                              | Quantity | Reference Designators                                   |
| ----------------------------------- | ------------------------ | ---------------------------------------- | -------- | ------------------------------------------------------- |
| Wenzhou QingPu Electronics Co., Ltd | WQP-WQP518MA             | 3.5mm Jack Mono Switched                 | 13       | J1, J2, J3, J4, J5, J6, J8, J9, J14, J15, J16, J17, J18 |
|                                     |                          | Pin Header Pitch 0.1in 2X5 Male Shrouded | 1        | J12                                                     |
| Wurth Elektronik                    | 694106402002             | DC Jack Vertical 2.1mm Barrel            | 1        | J13                                                     |
| Recom Technologies                  | R-78K3.3-0.5             | DC/DC Converter Submodule 3.3V           | 1        | U6                                                      | 

### Assembly Instructions

This assembly job is recommended for intermediate level DIYers who are comfortable soldering thru hole joints in close proximity to surface mounted parts.

1. Mount and solder rear facing through hole parts first, in this order: pin header, DC/DC converter, DC barrel jack.
1. Mount and solder front facing jacks next.
2. Attach the frontpanel and secure it with mounting nuts for the jacks.
   
<!-- 
## DIY  -->
<!-- 
PGO is available as a DIY kit that includes a PCB assembly with pre-assembled SMT components and 4 frontpanel options.  The user must source the through-hole components such as headers and jacks, as well as a suitable power cable for the module.

<img src={PCBFrontSMTOnly} alt="PCB Front SMT Only" style={{height: 400}} /> <img src={PCBRearSMTOnly} alt="PCB Rear SMT Only" style={{height: 400}} /> <img src={PCBFront} alt="PCB Front" style={{height: 400}} /> <img src={PCBRear} alt="PCB Rear" style={{height: 400}} />

In the Hardware Revisions section at the end of this document, you will find downloads for the complete schematic and an interactive HTML BOM.

### Bill of Materials

In addition to the PCBs and components included with your DIY kit from LZX, you will need to source the following components from electronics parts vendors.

| Manufacturer                        | Manufacturer Part Number | Description                              | Quantity | Reference Designators                        |
| ----------------------------------- | ------------------------ | ---------------------------------------- | -------- | -------------------------------------------- |
| Wenzhou QingPu Electronics Co., Ltd | WQP-WQP518MA             | 3.5mm Jack Mono Switched                 | 11       | J1, J2, J3, J4, J5, J6, J7, J8, J9, J10, J11 |
|                                     |                          | Pin Header Pitch 0.1in 2X5 Male Shrouded | 1        | J12                                          |
| Wurth Elektronik                    | 694106402002             | DC Jack Vertical 2.1mm Barrel            | 1        | J13                                          |
| Recom Technologies                  | R-78K3.3-0.5             | DC/DC Converter Submodule 3.3V           | 1        | U6                                           |

### Assembly Instructions

This assembly job is recommended for intermediate level DIYers who are comfortable soldering thru hole joints in close proximity to surface mounted parts.

1. Mount and solder rear facing through hole parts first, in this order: pin header, DC/DC converter, DC barrel jack.
1. Mount and solder front facing jacks next.
2. Attach the frontpanel and secure it with mounting nuts for the jacks. -->
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

<!-- 
## Performance Testing

The following tests are designed for verification of hardware revisions and general troubleshooting of performance issues. While intended for use by the LZX Industries design team, we publish the tests here to satisfy the curiosities of advanced users and service technicians.

### Requirements

- Oscilloscope.
- Waveform generator.
- 2x BNC to 3.5mm patch cables.
- Multimeter with probes.
- Power supply capable of providing 12V DC @ 100mA.

### Setup

- Configure your power supply to provide 12 volts to a 2.1mm DC barrel connector.
- Set power supply over current protection to 100mA.
- Connect power to the device.

#### Test +3.3V rail accuracy

- Use your multimeter to measure the voltage present at pin 3 of the U3 DC-DC converter module.
- Verify that the measurement is within the range of 3.0V to 3.6V. -->

<!-- ## Theory Of Operation

### Block Diagram

### Power Supply

### Voltage Reference

### Difference Amplifier -->
