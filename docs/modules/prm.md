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
import prm_sine_shaper from '/img/modules/prm/prm-diagrams/prm_sine-shaper.png';
import prm_parabolic_frequency_doubler from '/img/modules/prm/prm-diagrams/prm_parabolic-frequency-doubler.png';
import prm_linear_frequency_doubler from '/img/modules/prm/prm-diagrams/prm_linear-frequency-doubler.png';
import prm_2d_rotator from '/img/modules/prm/prm-diagrams/prm_2d-rotator.png';
import prm_divider from '/img/modules/prm/prm-diagrams/prm_divider.png';
import prm_minimum_value from '/img/modules/prm/prm-diagrams/prm_minimum-value.png';
import prm_maximum_value from '/img/modules/prm/prm-diagrams/prm_maximum-value.png';
import prm_analog_logic_xor from '/img/modules/prm/prm-diagrams/prm_analog-logic-xor.png';
import prm_voltage_limiter from '/img/modules/prm/prm-diagrams/prm_voltage-limiter.png';

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

### Front Panel Options

PRM ships with a black front panel installed. Red, green and blue panels are also included.

<img src={prm_all_front_panels} alt="prm_all_front_panels" />

All front panels are printed on both sides, allowing a choice of top-to-bottom or bottom-to-top signal flow. This gives great flexibility in designing modular systems.

---

<!--
AFR note: recommend adding an illustration of the reverse sides of the four panels.
-->

<!-- 
## System Integration Advice -->

<!-- - **Utility module** for mixing and level shifting, covering odd cases where the patch needs just one simple operation.
- **Expander module** to add extra inputs or output processing. Extend the functionality any module. Add one next to your favorite oscillators or RGB functions to expand modulation or signal input options.
- **Building block** for patching complex video synthesis functions. As low level analog computing blocks, several PGOs can be patched together to design a wide range of processing functions, including replicating functions from other modules. However, this level of flexibility comes at the expense of greater system size and more complex patches. Using both lower level and higher level modules is a great strategy for getting the most out of a system.
- **Consider multiple PGOs**. Analog computers provide several instances of summing and difference amplifiers. For example, a bidirectional converter or scaler requires two modules. A triple color space function requires three modules. More complex vector functions will require eight or more. -->

## Connectors

The PRM design was informed by years of studying interfaces common to the building blocks of analog computers and video processing equipment. 

<img src={prm_controls_connectors_indicators} alt="prm_controls_connectors_indicators" />

---

<!-- 
## Operation 

---

-->

## Example Patches

### Half-wave Rectify

<!-- Describe function -->

<img src={prm_half_wave_rectifier} alt="prm_half_wave_rectifier" />

---

### Half-wave Invert

<!-- Describe function -->

<img src={prm_half_wave_inverter} alt="prm_half_wave_inverter" />

---

### Full-wave Rectify

<!-- Describe function -->

<img src={prm_full_wave_rectifier} alt="prm_full_wave_rectifier" />

---

### Four-quadrant Multiply

<!-- Describe function -->

<img src={prm_four_quadrant_multiplier} alt="prm_four_quadrant_multiplier" />

---

### Two-quadrant Multiply

<!-- Describe function -->

<img src={prm_two_quadrant_multiplier} alt="prm_two_quadrant_multiplier" />

---

### One-quadrant Multiply

<!-- Describe function -->

<img src={prm_one_quadrant_multiplier} alt="prm_one_quadrant_multiplier" />

---

### Sine

<!-- Describe function -->

<img src={prm_sine_shaper} alt="prm_sine_shaper" />

---

### Exponential / Antisine

<!-- Describe function -->

<img src={prm_exponential_amplifier} alt="prm_exponential_amplifier" />

---

### Double Frequency / Parabolic

<!-- Describe function -->

<img src={prm_parabolic_frequency_doubler} alt="prm_parabolic_frequency_doubler" />

<!--
AFR note: Source should be labeled "source a".
-->

---

### Double Frequency / Ramp to Triangle 

<!-- Describe function -->

<img src={prm_linear_frequency_doubler} alt="prm_linear_frequency_doubler" />

<!--
AFR note: illustration does not show ramp to triangle conversion, it shows triangle frequency doubling only. Suggest adding an additional illustration with a ramp as the source. Also, source should be labeled "source a".
-->

---

### 2D Rotation

<!-- Describe function -->

<img src={prm_2d_rotator} alt="prm_2d_rotator" />

---

### Divide

<!-- Describe function -->

<img src={prm_divider} alt="prm_divider" />

---

### Minimum / Logical AND

<!-- Describe function -->

<img src={prm_minimum_value} alt="prm_minimum_value" />

---

### Maximum / Logical OR

<!-- Describe function -->

<img src={prm_maximum_value} alt="prm_maximum_value" />

---

### Difference / Logical XOR

<!-- Describe function -->

<img src={prm_analog_logic_xor} alt="prm_analog_logic_xor" />

---

### Limit Voltage

<!-- Describe function -->

<img src={prm_voltage_limiter} alt="prm_voltage_limiter" />

---

## Installation

<img src={prm_mounting_power_sync} alt="prm_mounting_power_sync" />

### Requirements

* EuroRack enclosure
* 12V DC or EuroRack power supply
* 2.1 mm DC barrel power cable **or** EuroRack power cable (both options included)
* Eurorack power for PRM requires a 16-pin to 10-pin ribbon cable
* Two M2.5 x 6mm mounting screws, or screws provided or specified by the enclosure manufacturer
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

<!--
### Technical Data
-->

| Parameter                    | Value                                                                           |
| ---------------------------- | ------------------------------------------------------------------------------- |
| Manufacturer Part Number     | 950066                                                                          |
| Pronunciation                | piː-rɒm                                                                         |
| Mounting Width               | 4 HP                                                                            |
| Mounting Hole Count          | 2                                                                               |
| Power Consumption            | 12V @ 75 mA                                                                     |
| Power Connectors             | 10 pin EuroRack ribbon, 2.1mm DC barrel                                         |
| Input Impedance              | 1M ohms                                                                         |
| Output Impedance             | 75 ohms                                                                         |
| Input Protection Range       | +/-20V                                                                          |
| Input Clipping Range         | +/-2.5V                                                                         |
| Output Range                 | +/-2.5V                                                                         |
| Propagation Delay            | 32ns                                                                            |
| Module Width                 | 20.32 mm                                                                        |
| Module Height                | 128.5 mm                                                                        |
| Product Box Width            | 4 in / 101.6 mm                                                                 |
| Product Box Height           | 2 in / 50.8 mm                                                                  |
| Product Box Depth            | 6 in / 152.4 mm                                                                 |
| Included                     | DC barrel power cable, EuroRack power cable, red panel, green panel, blue panel |
| EuroRack Power Cable Type    | 10-pin to 16-pin                                                                |
| EuroRack Power Cable Length  | 25 cm                                                                           |
| DC Barrel Power Cable Length | 25 cm                                                                           |
| RoHS Compliance              | Manufactured with lead-free processes.                                          |
| Video Sync                   | None                                                                            |

<!-- 
| Mounting Depth               | TODO mm                                                                         |
| Bandwidth @ -3dB             | TODO                                                                            |
| Module Depth                 | TODO mm                                                                         |
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

### PRM-RevA

Initial prototype. September 2024.

### PRM-RevB

Second prototype. December 2024.

### PRM-RevC

Third prototype. January 2025.

### PRM-RevD

Initial production version. February 2025.

PRM-RevD Schematic Diagram
&nbsp;<br />
[Download PDF](/pdf/modules/prm/PRM-REVD_Schematic_Diagram.pdf)

PRM-RevD Interactive Bill of Materials
&nbsp;<br />
[Download ZIP](/zip/modules/prm/PRM-REVD_Interactive_Bill_of_Materials.zip)

---

## DIY 

PRM is available as an assembled module, a full DIY kit, or a partial DIY kit.

Downloads for the complete schematic and an interactive HTML Bill of Materials are found in the [Hardware Revisions](/docs/modules/prm#hardware-revisions) section above.

### Partial DIY Components

The partial DIY kit from LZX includes the printed circuit board and front panel. The following components must be purchased separately from electronics parts vendors.

| Manufacturer                        | Manufacturer Part Number | Description                              | Quantity | Reference Designators                        |
| ----------------------------------- | ------------------------ | ---------------------------------------- | -------- | -------------------------------------------- |
| Wenzhou QingPu Electronics Co., Ltd | WQP-WQP518MA             | 3.5mm Jack Mono Switched                 | 9        | J4, J5, J6, J7, J8, J9, J10, J11, J12        |
|                                     |                          | Pin Header Pitch 0.1in 2X5 Male Shrouded | 1        | J2                                           |
| Wurth Elektronik                    | 694106402002             | DC Jack Vertical 2.1mm Barrel            | 1        | J3                                           |
| Recom Technologies                  | R-78K5.0-0.5             | DC/DC Converter Submodule 5.0V           | 1        | U5                                           | 

### Assembly Instructions

This assembly job is recommended for intermediate level DIYers who are comfortable soldering thru hole joints in close proximity to surface mounted parts.

1. Mount and solder rear-facing through hole parts first, in this order: pin header, DC/DC converter, DC barrel jack.
2. Mount and solder front-facing jacks.
3. Attach the front panel and secure it with mounting nuts for the jacks.
   
<!-- 
## Functional Testing
-->

