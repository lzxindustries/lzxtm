---
draft: false
title: "P: Passive Potentiometer"
---

import pot_front_panel from '/img/modules/pot/pot-diagrams/pot_front-panel.png';
import pot_controls_connectors_indicators from '/img/modules/pot/pot-diagrams/pot_controls-connectors-indicators.png';
import pot_crossfade from '/img/modules/pot/pot-diagrams/pot_crossfade.gif';
import pot_fade_to_black from '/img/modules/pot/pot-diagrams/pot_fade-to-black.gif';
import pot_mounting_power_sync from '/img/modules/pot/pot-diagrams/pot_mounting-power-sync.png';

# P
<span class="head2_nolink">Passive Potentiometer</span>

## Overview

<img src={pot_front_panel} alt="pot_front_panel" />

## Key Specifications

| Parameter         | Value                                                                           |
| ----------------- | ------------------------------------------------------------------------------- |
| Mounting Width    | 2 HP                                                                            |
| Power Consumption | None                                                                            |
| Power Connectors  | None                                                                            |
| Video Sync        | None                                                                            |

<!-- 
## System Integration Advice -->

<!-- - **Utility module** for mixing and level shifting, covering odd cases where the patch needs just one simple operation.
- **Expander module** to add extra inputs or output processing. Extend the functionality any module. Add one next to your favorite oscillators or RGB functions to expand modulation or signal input options.
- **Building block** for patching complex video synthesis functions. As low level analog computing blocks, several PGOs can be patched together to design a wide range of processing functions, including replicating functions from other modules. However, this level of flexibility comes at the expense of greater system size and more complex patches. Using both lower level and higher level modules is a great strategy for getting the most out of a system.
- **Consider multiple PGOs**. Analog computers provide several instances of summing and difference amplifiers. For example, a bidirectional converter or scaler requires two modules. A triple color space function requires three modules. More complex vector functions will require eight or more. -->
<!-- 
## Controls, Connectors & Indicators

<img src={pot_controls_connectors_indicators} alt="pot_controls_connectors_indicators" />

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
<!-- 
## Example Patches -->

<!-- <img src={pot_crossfade} alt="pot_crossfade" />

<img src={pot_fade_to_black} alt="pot_fade_to_black" /> -->

<!-- ### 4 Quadrant Multiplier

### 2 Quadrant Multiplier

### 1 Quadrant Multiplier

### Absolute Value / Full Wave Rectifier

### Half Wave Rectifier

### Sine Wave Shaper

### Square / Exponential Wave Shaper

### Sine Frequency Doubler

### Saw to Triangle / Triangle Frequency Doubler -->

<!-- 
### Buffer

Buffer the input signal with a unity gain of 1.0. Due to the module's propagation delay, it can be used to add slight delays in the video processing path, resulting in the picture shifting slightly to the right.

<img src={PatchBuffer} alt="Buffer"/>

### Amplifier

Amplify the input signal with a gain of 2.

<img src={PatchAmplifier} alt="Amplifier"/>

### Attenuator

Attenuate the input signal with a gain of 0.5.

<img src={PatchAttenuator} alt="Attenuator"/>

### Inverter

Invert the arithmetic sign of the input signal. Positive voltages are converted to negative voltages, or vice versa.

<img src={PatchInverter} alt="Inverter"/>
### Negative

Convert a unipolar signal to negative by subtracting it from 1V. Useful for inverting keys, logic and RGB channels. An input signal ranging from zero to one results in an inverted output ranging from one to zero.

<img src={PatchNegative} alt="Negative"/>

### Subtractor

Subtract one input from another.

<img src={PatchSubtractor} alt="Subtractor"/>

### Adder

Calculate the sum of two input signals.

<img src={PatchAdder} alt="Adder" style={{}} />

### Average

Calculate the average of two input signals.

<img src={PatchAverage} alt="Average" style={{}} />

### Unipolar Modulator

Subtract a modulator from a primary signal, where both are unipolar 0-1V. The primary signal *source a* passes unmodified when the modulating signal *source b* is at its midpoint of 0.5V. As a ramp shifter, *source a* is the input ramp, and *source b* is the positioning control voltage. As a brightness processor, *source a* is a unipolar color channel such as luma, red, green, or blue, and *source b* is the brightness adjustment.

<img src={PatchUnipolarModulator} alt="Unipolar Modulator"/>

### Weighted Mixer

Calculate a 3:1 weighted sum of two inputs, with 3 parts of *source a* for every 1 part of *source b*.

<img src={PatchWeightedMixer} alt="Weighted Mixer"/>

### Compressed Mixer

Calculate the sum of four input signals and attenuate the mix to a value of one half. This is a common scenario to prevent clipping when mixing more than two input signals.

<img src={PatchCompressedMixer} alt="Compressed Mixer"/>

### Bipolar to Unipolar

Convert a +/-1V bipolar signal to the 0-1V unipolar range.

<img src={PatchBipolarToUnipolar} alt="Bipolar To Unipolar"/>

### Unipolar to Bipolar

Convert a 0-1V unipolar signal to the +/-1V bipolar range.

<img src={PatchUnipolarToBipolar} alt="Unipolar To Bipolar"/>

### Differential to Single Ended

Convert a differential input signal to a single-ended output signal. In a differential signal, information is encoded as the difference between a matched pair of separate signals. For example, balanced audio rejects noise on cable runs by sending both a positive and a phase-inverted negative signal on two conductors. Video chroma can be encoded as the difference between two color primaries, such as Pb and Pr, or I and Q. 

<img src={PatchDifferentialToSingleEnded} alt="Differential To Single Ended"/>

### Single Ended to Differential

Convert a single-ended input signal to a differential output signal. One possible application of differential outputs on PGO would be positive and negative versions of the same signal, such as luminance keys. Both signals will have the same amount of propagation delay, allowing precise horizontal alignment of positive and negative masks.

<img src={PatchSingleEndedToDifferential} alt="Single Ended To Differential"/> -->

## Installation

<img src={pot_mounting_power_sync} alt="pot_mounting_power_sync" />

<!-- Discuss differences between 10 and 16 pin connectors -->
<!-- Something about making sure all screws have been removed from the intended mounting location. -->

### Requirements

* EuroRack enclosure.
* Two M2.5 x 6mm mounting screws, or screws provided or specified by the enclosure manufacturer.
* #1 Phillips head screwdriver, or hand tool provided or specified by the enclosure manufacturer.

### Procedure

* Power off and disconnect the EuroRack enclosure's power supply and any attached DC adapters.
* Carefully test fit the module in the open space in the EuroRack enclosure. If it is obstructed by the enclosure or any internal assemblies, abort this procedure.
* Mount the module to the EuroRack rails using all mounting holes.
* Power on the EuroRack enclosure and start patching.
<!-- 
## Full Specifications -->
<!-- 
| Parameter                    | Value                                                                           |
| ---------------------------- | ------------------------------------------------------------------------------- |
| Manufacturer Part Number     | 950065                                                                          |
| Pronunciation                | [piː ɡəʊ](/mp3/modules/pgo/pgo-pronunciation.mp3)                               |
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
| Propagation Delay            | TODO                                                                            |
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
| Video Sync                   | None                                                                            | -->
<!-- 
## Calibration -->

<!-- Calibration is not required for this module. -->

## Maintenance

Keep your module free of dust and debris by performing periodic cleaning. Spots may be cleaned from the frontpanel with a microfiber cloth and isopropyl alcohol or other electronics cleaner.

<!-- ## Troubleshooting -->


## Hardware Revisions

The hardware revision code is printed on the circuit board visible from the rear of the module.

### POT-REVA

Initial production version. February 2025.

[Download POT-REVA Schematic Diagram (PDF)](/pdf/modules/pot/POT-REVA_Schematic_Diagram.pdf)

[Download POT-REVA Interactive Bill of Materials (ZIP)](/zip/modules/pot/POT-REVA_Interactive_Bill_of_Materials.zip)

## DIY 

P is available as a DIY kit that includes the main PCB and the front panel.  The user must source the through-hole components such as jacks and potentiometers.

In the Hardware Revisions section, you will find downloads for the complete schematic and an interactive HTML BOM.

### Bill of Materials

In addition to the PCBs and components included with your DIY kit from LZX, you will need to source the following components from electronics parts vendors.

| Manufacturer                        | Manufacturer Part Number | Description                              | Quantity  | Reference Designators     |
| ----------------------------------- | ------------------------ | ---------------------------------------- | --------- | ------------------------- |
| Wenzhou QingPu Electronics Co., Ltd | WQP-WQP518MA             | 3.5mm Jack Mono Switched                 | 3         | J1, J2, J3                |
| Alps Alpine                         | RS45111A6A08             | 45mm Slide Potentiometer                 | 1         | P1                        |

### Assembly Instructions

This assembly job is recommended for intermediate level DIYers who are comfortable soldering thru hole joints in close proximity to surface mounted parts.

1. Mount and solder front facing jacks and slide potentiometer.
2. Attach the frontpanel and secure it with mounting nuts for the jacks.

