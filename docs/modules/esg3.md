---
draft: true
title: "ESG3: Encoder & Sync Generator"
---

# ESG3
<span class="head2_nolink">Encoder & Sync Generator</span>

## Overview

ESG3 Encoder is our third generation of video synthesis core modules, offering everything you need to convert voltages from your EuroRack synthesizer into HD/SD Component and SD Composite video signals. Programmable output and sync reference format: NTSC, PAL, 486p5994, 576p50, 720p50, 720p5994, 720p60, 1080i50, 1080i5994, 1080i60, 1080p2398, 1080p24, 1080p25, 1080p2997, 1080p30. HD/SD component and composite video encoding with a fully analogue signal path. RGB proc amp with brightness, contrast, inversion and mute per channel.

## Key Specifications

| Parameter         | Value                                    |
| ----------------- | ---------------------------------------- |
| Mounting Width    | 12 HP                                    |
| Power Consumption | 12V @ 300mA                              |
| Power Connectors  | 16 pin EuroRack ribbon, 2.1mm DC barrel  |
| Video Sync        | Input and output via rear RCA connectors |
| Included          | EuroRack power cable                     |


## Video Formats

ESG3's format selection switch determines the module's video output format and video sync standard. Additionally, the user may select between YPbPr and RGB colorspace modes for the Component output encoder. In most cases, the user should select the YPbPr component output mode. Optionally, RGB component output mode may be used with some displays and capture devices if supported.

0 represents the switch's OFF state. 1 represents the switch's ON state. x indicates a position irrelevant to the listed setting.

| Format	      | Setting     |
|--------------|-------------|
| NTSC	        | 0000xxxx    |
| PAL	         | 1000xxxx    |
| 480p5994	    | 0100xxxx    |
| 576p50	      | 1100xxxx    |
| 1080i5994    |	0010xxxx    |
| 1080i60	     | 1010xxxx    |
| 720p5994     |	0110xxxx    |
| 720p60	      | 1110xxxx    |
| 1080i50	     | 0001xxxx    |
| 1080p2398    |	1001xxxx    |
| 720p50	      | 0101xxxx    |
| 1080p2997	   | 1101xxxx    |
| 1080p24	     | 0011xxxx    |
| 1080p25	     | 1011xxxx    |
| 1080p30	     | 0111xxxx    |
| RGB Out	     | xxxxxxx1    |
| YPbPr Out	   | xxxxxxx0    |

## System Integration Advice

## Controls, Connectors & Indicators

### Default Control Positions

With nothing patched to the inputs, and all knobs in their center position, the output will be close to black. When the mute/blanking switches are engaged, there should be a minimal brightness shift in the output. If Contrast knobs are fully counter-clockwise, at their zero position, the output will be near 50% gray level.

## Operation


## Example Patches


## Installation

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

## Full Specifications

| Parameter                    | Value                                                                           |
| ---------------------------- | ------------------------------------------------------------------------------- |
<!-- | Manufacturer Part Number     | 950065                                                                          | -->
<!-- | Pronunciation                | [piː ɡəʊ](/mp3/modules/pgo/pgo-pronunciation.mp3)                               | -->
| Mounting Width               | 12 HP                                                                            |
| Mounting Depth               | 42 mm                                                                         |
| Mounting Hole Count          | 4                                                                               |
| Power Consumption            | 12V @ 300 mA                                                                     |
| Power Connectors             | 16 pin EuroRack ribbon, 2.1mm DC barrel                                         |
| Input Impedance              | 100K ohms                                                                         |
| Output Impedance             | 75 ohms                                                                         |
| Input Protection Range       | +/-15V                                                                          |
| Input Clipping Range         | +/-2.5V                                                                         |
<!-- | Output Range                 | +/-2.5V                                                                         | -->
<!-- | Propagation Delay            | TODO                                                                            | -->
<!-- | Bandwidth @ -3dB             | TODO                                                                            | -->
| Module Width                 | 60.96 mm                                                                        |
| Module Height                | 128.5 mm                                                                        |
| Module Depth                 | TODO mm                                                                         |
| Product Box Width            | 4 in / 101.6 mm                                                                 |
| Product Box Height           | 2 in / 50.8 mm                                                                  |
| Product Box Depth            | 6 in / 152.4 mm                                                                 |
| Product Weight               | TODO                                                                            |
| Included                     | DC barrel power cable, EuroRack power cable, red panel, green panel, blue panel |
| EuroRack Power Cable Type    | 16-pin to 16-pin                                                                |
| EuroRack Power Cable Length  | 25 cm                                                                           |
<!-- | DC Barrel Power Cable Length | 25 cm                                                                           | -->
| RoHS Compliance              | Manufactured with lead-free processes.                                          |
| Video Sync                   | Input and output via rear RCA connectors                                                                            | 

## Calibration

<!-- Explanation of trim pots and calibration procedure -->

## Maintenance

Keep your module free of dust and debris by performing periodic cleaning. Spots may be cleaned from the frontpanel with a microfiber cloth and isopropyl alcohol or other electronics cleaner.

<!-- ## Troubleshooting -->

## Hardware Revisions

<!-- The hardware revision code is printed on the circuit board visible from the rear of the module. -->
