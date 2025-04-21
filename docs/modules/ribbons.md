---
draft: false
title: "RIBBONS: Three-Bit Digitizer and Colorizer"
---

:::warning
This page is a draft under construction. Stay tuned to our newsletter for the official content release.
:::

import ribbons_line_art_labeled from '/img/modules/ribbons/ribbons-diagrams/ribbons_line_art_labeled_336x1024.png';

# RIBBONS
<span class="head2_nolink">Three-Bit Digitizer and Colorizer</span>

{/*
<img src={Frontpanel} alt="Frontpanel" />
*/}

## Overview

Ribbons is a three-bit digitizer and colorizer. Slice any video source or other analog waveform into eight discrete bands. The three-bit value scheme invokes the look of primitive digital graphics and posterization effects from the 1970s and '80s.

With nine high-speed analog comparators and CMOS logic, Ribbons digitizes SD or HD video without a pixel clock or quantized timebase. This reveals a surreal and silky quality to the image that is absent from today's conventional digital video.

### Legacy

* 2012: our first three-bit digitizer, **8-Stage Video Quantizer & Sequencer**, loosely inspired by the Sandin IP Amplitude Classifier
* 2018: **Castle 000 ADC** and **Castle 001 DAC**, in the Castle DIY series
* 2019: **Fortress**, first LZX module to integrate ADC and DAC capabilities

The Expedition series module **Topogram** serves some of the same high-level artistic functions as Ribbons. Topogram differentiates a signal into two to six bands, but it's entirely analog, with a completely different design philosophy and patch paradigm. There are several "key" functional differences. Topogram's outputs are all binary, while Ribbons also provides combined grayscale outputs. Topogram's outputs are discrete from one another, but the binary outputs of Ribbons overlap because each is a digit within a three-bit numerical value.

## Key Specifications

| Parameter         | Value                                                                           |
| ----------------- | ------------------------------------------------------------------------------- |
| Mounting Width    | 8 HP                                                                            |
| Power Consumption | 12V @ 125 mA                                                                    |
| Power Connectors  | 16 pin EuroRack ribbon, 2.1mm DC barrel                                         |
| Video Sync        | None                                                                            |
| Included          | DC barrel power cable, EuroRack power cable                                     |

---

<!--
## System Integration Advice

TODO
-->

## Controls & Connectors

* Three-bit DAC output of stepped waveforms such as eight-band grayscale video
* Additional inverted DAC output for more patching options
* Three hard-edge binary outputs, one for each digit of a three-bit number
* Window Key output
* Sampling offset and scale set by voltage-controlled Center and Span parameters
* Enable and Disable inputs extend utility for masking and compositing

---

<!--
## Operation

TODO

---
-->

<!--
## Example Patches

---
-->

## Installation

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
* Mount the module to the EuroRack rails using all mounting holes.
* Store the unused cable along with the product box in a safe location. 
* Power on the EuroRack enclosure and start patching.

---

## Full Specifications

<table>

<tr><th>&nbsp;</th><th>Connectors</th><th>Controls</th></tr>
<tr><td>

<!--
AFR note: this illustration, screen captured from the primary domain, has an error in the Figma or something. J8 and J11 are not labeled.
-->

<img src={ribbons_line_art_labeled} alt="Ribbons: labeled front panel controls" />

</td><td>

| Jack | Function         |
|------|------------------|
| J1   | Center CV in     |
| J2   | Span CV in       |
| J3   | Enable in        |
| J4   | DAC out          |
| J5   | D0 out           |
| J6   | Disable in       |
| J7   | Inverted DAC out |
| J8   | D1 out           |
| J9   | ADC in           |
| J10  | Window Key out   |
| J11  | D2 out           |

</td><td>

| Potentiometer | Function               |
|---------------|------------------------|
| P1            | Center                 |
| P2            | Span                   |
| P3            | Center CV depth        |
| P4            | Pan CV depth           |

</td></tr></table>

### Technical Data

| Parameter                    | Value                                                                           |
| ---------------------------- | ------------------------------------------------------------------------------- |
| Manufacturer Part Number     | 950049                                                                          |
| Mounting Width               | 8 HP                                                                            |
| Mounting Depth               | 32 mm                                                                           |
| Mounting Hole Count          | 4                                                                               |
| Power Consumption            | 12V @ 125 mA                                                                    |
| Power Connectors             | 16 pin EuroRack ribbon, 2.1mm DC barrel                                         |
| Input Impedance              | 1M ohms                                                                         |
| Output Impedance             | 75 ohms                                                                         |
| Input Protection Range       | +/-20V                                                                          |
| Input Clipping Range         | +/-2.5V                                                                         |
| Output Range                 | +/-2.5V                                                                         |
| Included                     | DC barrel power cable, EuroRack power cable                                     |
| EuroRack Power Cable Type    | 16-pin                                                                          |
| EuroRack Power Cable Length  | 25 cm                                                                           |
| DC Barrel Power Cable Length | 25 cm                                                                           |
| RoHS Compliance              | Manufactured with lead-free processes                                           |
| Video Sync                   | None                                                                            |

<!--
| Pronunciation                |                                                                                 |
| Propagation Delay            | TODO                                                                            |
| Bandwidth @ -3dB             | TODO                                                                            |
| Module Width                 | TODO mm                                                                         |
| Module Height                | TODO mm                                                                         |
| Module Depth                 | TODO mm                                                                         |
| Product Box Width            | TODO in / TODO mm                                                               |
| Product Box Height           | TODO in / TODO mm                                                               |
| Product Box Depth            | TODO in / TODO mm                                                               |
| Product Weight               | TODO                                                                            |
-->

---

<!--
## Calibration

Calibration is not required for this module.
---
-->

## Maintenance

Keep the module free of dust and debris by performing periodic cleaning. Spots may be cleaned from the front panel with a microfiber cloth and isopropyl alcohol or other electronics cleaner.

---

<!--
## Troubleshooting

---
-->

## Hardware Revisions

The hardware revision code is printed on the circuit board visible from the rear of the module.
