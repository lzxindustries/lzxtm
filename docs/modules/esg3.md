---
draft: true
title: "ESG3: Encoder & Sync Generator"
---

:::warning
This page is a draft under construction. Stay tuned to our newsletter for the official content release.
:::

<!--
import esg3_frontpanel from '/img/modules/esg3/esg3-diagrams/esg3_frontpanel.png';
-->

import esg3_line_art_labeled from '/img/modules/esg3/esg3-diagrams/esg3_line_art_labeled_496x1024.png';

# ESG3
<span class="head2_nolink">Encoder & Sync Generator</span>

{/*
<img src={esg3_frontpanel} alt="ESG3 front panel" />
*/}

## Overview

Critical to the video mission, ESG3 combines three essential functions into a compact form factor. ESG3 generates sync, outputs SD or HD video, and manipulates color. More than a utility module, ESG3 features integrated processing amplifiers, making it a creative instrument.

To output legal video signals from a modular synthesizer, an encoder is required. ESG3 converts LZX-compatible 1 volt signals to composite, RGB component, or YPbPr component video. It supports a wide range of video standards, from NTSC and PAL up to full high definition.

A modular synthesizer also requires a source of video sync. ESG3 generates sync with or without an external reference. It can be the ultimate source of sync, or genlock to incoming sync or video. Either way, ESG3 ensures that the entire modular system dances to the beat of the same drummer.

Proc amp controls allow aesthetic image manipulation. Each RGB channel features brightness and contrast adjustments. Invert or mute each channel with the flick of a switch. Invert or mute all outputs with another switch, making it easy to cut to black.

---

## Key Specifications

|                   |                                                             |
| ----------------- | ----------------------------------------------------------- |
| Mounting Width    | 12 HP                                                       |
| Power Consumption | 12V @ 300mA                                                 |
| Power Connectors  | 16 pin EuroRack ribbon, 2.1mm DC barrel                     |
| Included          | DC barrel power cable, EuroRack power cable, RCA sync cable |
| Video Sync        | Rear RCA in & out                                           |


### Video Formats

DIP switches on the front panel specify a standard video format for sync and output. Choose the appropriate video timing and component format for your external devices. 

:::warning
ESG3 is not a format converter! The DIP switches must match the format of any incoming external sync. If you need to convert among different video formats, TBC2 is the solution.
:::

ESG3 supports two component formats: **YPbPr** and **RGsB**. YPbPr is appropriate in most situations. RGsB is an option for interfacing with specialized broadcast equipment.

:::note
In RGsB mode, ESG3 outputs composite sync on the green channel. ESG3 does not support the more common RGBHV broadcast standard. It also does not support VESA timings for computer VGA video.
:::

In the table below, the numeral **0** represents the **OFF** state, with the switch in the **DOWN** position. The numeral **1** represents the **ON** state, with the switch in the **UP**** position. The letter **X** indicates a position irrelevant to the listed setting.


| Format         | Setting  |
|----------------|----------|
| NTSC (486i59)  | 0000xxxx |
| PAL (576i50)   | 1000xxxx |
| 480p59         | 0100xxxx |
| 576p50         | 1100xxxx |
| 720p50         | 0101xxxx |
| 720p59         | 0110xxxx |
| 720p60         | 1110xxxx |
| 1080i50        | 0001xxxx |
| 1080i59        | 0010xxxx |
| 1080i60        | 1010xxxx |
| 1080p23        | 1001xxxx |
| 1080p24        | 0011xxxx |
| 1080p25        | 1011xxxx |
| 1080p29        | 1101xxxx |
| 1080p30        | 0111xxxx |
| RsGB           | xxxxxxx1 |
| YPbPr          | xxxxxxx0 |

<!--

---

## System Integration Advice

## Controls, Connectors & Indicators

### Default Control Positions

With nothing patched to the inputs, and all knobs in their center position, the output will be close to black. When the mute/blanking switches are engaged, there should be a minimal brightness shift in the output. If Contrast knobs are fully counter-clockwise, at their zero position, the output will be near 50% gray level.

## Operation


## Example Patches

-->

---

## Installation

<!-- Discuss differences between 10 and 16 pin connectors -->
<!-- Something about making sure all screws have been removed from the intended mounting location. -->

### Requirements

* EuroRack enclosure
* 12V DC or EuroRack power supply
* 2.1mm DC barrel power cable **or** a EuroRack power cable (both options included)
* Four M2.5 x 6mm mounting screws, or screws provided or specified by the enclosure manufacturer
* #1 Phillips head screwdriver, or hand tool provided or specified by the enclosure manufacturer

### Procedure

* Power off and disconnect the EuroRack enclosure's power supply and any attached DC adapters.
* Connect either the EuroRack Power Cable **or** the DC Barrel Power Cable to the module. Do not connect both Eurorack and DC Barrel power.
* Ensure that no mounting screws are in any holes in the area where you wish to mount the module.
* Carefully test fit the module with its attached power cable in the open space in the EuroRack enclosure. If it is obstructed by the enclosure or any internal assemblies, abort this procedure.
* Connect the disconnected end of the power cable to the power supply.
* Connect the sync output to the first module in the sync chain. If the system includes TBC2, it should receive sync directly from ESG3.
* Optionally connect the sync input to an incoming sync or video signal.
* Mount the module to the EuroRack rails using all mounting holes.
* Store the unused cable along with the product box in a safe location. 
* Power on the EuroRack enclosure and start patching.

---

## Full Specifications

<table>

<tr><th>&nbsp;</th><th>Connectors</th><th>Controls</th></tr>
<tr><td>

<img src={esg3_line_art_labeled} alt="DWO3: labeled front panel controls" />

</td><td>

| Jack | Function                               |
|------|----------------------------------------|
| J1   | Red in                                 |
| J2   | RCA Composite video out                |
| J3   | Green in                               |
| J4   | Blue in                                |
| J5   | RCA Y or Green+Sync video out          |
| J6   | RCA Pb or Blue video out               |
| J7   | RCA Pr or Red video out                |

</td><td>

| Switch | Function                             |
|--------|--------------------------------------|
| S1     | All Outputs <br />Invert/Mute        |
| S2     | Red <br />Invert/Mute                |
| S3     | Green <br />Invert/Mute              |
| S4     | Blue <br />Invert/Mute               |
| S5     | Video Standard <br />DIP switches    |

| Pot    | Function                             |
|--------|--------------------------------------|
| P1     | Red Contrast                         |
| P2     | Green Contrast                       |
| P3     | Blue Contrast                        |
| P4     | Red Brightness                       |
| P5     | Green Brightness                     |
| P6     | Blue Brightness                      |

</td></tr></table>

### Technical Data

|                              |                                                                                 |
| ---------------------------- | ------------------------------------------------------------------------------- |
| Mounting Width               | 12 HP                                                                           |
| Mounting Depth               | 42 mm                                                                           |
| Mounting Hole Count          | 4                                                                               |
| Power Consumption            | 12V @ 300 mA                                                                    |
| Power Connectors             | 16 pin EuroRack ribbon, 2.1mm DC barrel                                         |
| Input Impedance              | 100K ohms                                                                       |
| Output Impedance             | 75 ohms                                                                         |
| Input Protection Range       | +/-15V                                                                          |
| Input Clipping Range         | +/-2.5V                                                                         |
| Output Range                 | +/-2.5V                                                                         |
| Module Width                 | 60.96 mm                                                                        |
| Module Height                | 128.5 mm                                                                        |
| Product Box Width            | 4 in / 101.6 mm                                                                 |
| Product Box Height           | 2 in / 50.8 mm                                                                  |
| Product Box Depth            | 6 in / 152.4 mm                                                                 |
| Included                     | DC barrel power cable, EuroRack power cable                                     |
| EuroRack Power Cable Type    | 16-pin to 16-pin                                                                |
| EuroRack Power Cable Length  | 25 cm                                                                           |
| DC Barrel Power Cable Length | 25 cm                                                                           |
| RoHS Compliance              | Manufactured with lead-free processes                                           |
| Video Sync                   | Rear RCA in & out                                                               | 

<!-- 
| Manufacturer Part Number     |                                                                                 |
| Pronunciation                |                                                                                 | 
| Propagation Delay            | TODO                                                                            |
| Bandwidth @ -3dB             | TODO                                                                            |
| Module Depth                 | TODO mm                                                                         |
| Product Weight               | TODO                                                                            |
-->

---

<!--
## Calibration

Explanation of trim pots and calibration procedure

---
-->

## Maintenance

Keep your module free of dust and debris by performing periodic cleaning. Spots may be cleaned from the frontpanel with a microfiber cloth and isopropyl alcohol or other electronics cleaner.

<!-- ## Troubleshooting -->

---

## Hardware Revisions

The hardware revision code is printed on the circuit board visible from the rear of the module.
