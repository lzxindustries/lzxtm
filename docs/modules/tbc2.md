---
draft: true
---

# TBC2 - Dual Video Input

<img src={Frontpanel} alt="Frontpanel" />

## Overview

TBC2 is a dual video input module for your LZX modular system. Supported are Composite, Component & S-Video inputs capable of SD/HD video decoding and frame synchronization.

## Key Specifications

| Parameter         | Value                                                                           |
| ----------------- | ------------------------------------------------------------------------------- |
| Mounting Width    | 16 HP                                                                           |
| Power Consumption | 12V @ 600 mA                                                                    |
| Power Connectors  | 16 pin EuroRack ribbon, 2.1mm DC barrel                                         |
| Video Sync        | Front and rear RCA                                                              |
| Included          | DC barrel power cable, EuroRack power cable                                     |

## System Integration Advice

TODO

## Controls, Connectors & Indicators

* SD/HD Video Sync Generator supporting NTSC, PAL, 480p, 576p, 720p50, 720p5994, 720p60, 1080i50, 1080i5994, 1080i60, 1080p2398, 1080p24, 1080p25, 1080p2997, 1080p30 sync formats
* Dual SD/HD Video Decoders supporting NTSC, PAL, 480p, 576p, 720p50, 720p5994, 720p60, 1080i50, 1080i5994, 1080i60, 1080p2398, 1080p24, 1080p25, 1080p2997, 1080p30 input sources
* VESA/VGA input up to 1024x768 with optional 10HP VGA+SCART expander.
* Playback of still images and looping sequences loaded from frontpanel MicroSD card slot
* SD color correction controls for each input: Hue, Saturation, Contrast & Brightness
* Auto upscaling and downscaling modes for both inputs
* MIDI input for remote parameter control

## Submodules

**Decoder**
- TBC2 has two input decoder submodules. Each supports Component (YPbPr/RGsB), Composite (CVBS) and S-Video (YC) inputs. With the addition of the VGA/SCART expander, it supports VGA (RGBHV) and SCART (CVBS/RGsB) inputs.

| Input Standard |
|----------------|
| NTSC           |
| PAL            |
| 480p           |
| 576p           |
| 720p50         |
| 720p5994       |
| 720p60         |
| 1080i50        |
| 1080i5994      |
| 1080i60        |
| 1080p2398      |
| 1080p24        |
| 1080p25        |
| 1080p2997      |
| 1080p30        |
| 640x480p60     |
| 800x600p60     |
| 1024x768p60    |

**Genlock**
- TBC2 has one genlock submodule. This module controls the timing of the output encoders. It is a full featured Sync Generator with front and rear outputs for video sync.

| Output Standard |
|-----------------|
| NTSC            |
| PAL             |
| 480p            |
| 576p            |
| 720p50          |
| 720p5994        |
| 720p60          |
| 1080i50         |
| 1080i5994       |
| 1080i60         |
| 1080p2398       |
| 1080p24         |
| 1080p25         |
| 1080p2997       |
| 1080p30         |

**Encoder**
- TBC2 has two output encoder submodules. Each supports Patchable 1V (YRGB) outputs. The output video standard follows the setting of the Genlock Module.

**Ramp Generator**

TBC2 has one Ramp Generator submodule. The output video standard follows the setting of the Genlock Module. The Ramp Generator is a low speed software renderer designed to generate programmable gradients and other patterns. After any settings change, this module will render a new output frame.

**Media**

TBC2 has one media submodule. This module is capable of loading still images (JPG, PNG, BMP) from the front MicroSD card socket. The output video standard follows the setting of the Genlock Module.

## Operation

To use the media module, copy your images into a subfolder of a compatible MicroSD card. For example:

/media/folder/frame1.JPG

We recommend preparing media in a size matching your system's output video standard in JPG or PNG formats. For example, for NTSC video, prepare media at 720 (W) x 486 (H) dimensions.

Always eject or insert your MicroSD card only when your system is powered off. Keep remote backups of any data on your MicroSD card.

The maximum number of images per media folder is determined by the current output video standard, with a minimum of 24 frames in 1920 (W) x 1080 (H) media sizes.

**MicroSD Card Compatibility**

TBC2 is compatible with some, but not all MicroSD cards. When you acquire a MicroSD card to use with TBC2, we recommend selecting from the specific brands and models we have tested to be hassle free, listed below. Always purchase MicroSD cards from a trusted vendor with name brand packaging to protect yourself against counterfeits. To prepare your MicroSD card for use with TBC2, please format the card as FAT32 with default sector size.

| Brand/Series     |	Size          |
|------------------|---------------|
| SanDisk	         | 8GB, 16GB     |
| SanDisk EDGE	    | 8GB           |

**MIDI Control Change Map**

| CC	  | Module	       | Parameter                   |
|------|---------------|-----------------------------|
| 0	   | Encoder A	    | Crossfade                   |
| 1    |	Decoder A	    | SD Processor Hue            |
| 2    |	Decoder A	    | SD Processor Saturation     |
| 3    |	Decoder A	    | SD Processor Brightness     |
| 4    |	Decoder A     |	SD Processor Contrast       |
| 16   |	Encoder B     |	Crossfade                   |
| 17   |	Decoder B     |	SD Processor Hue            |
| 18   |	Decoder B     |	SD Processor Saturation     |
| 19   |	Decoder B     |	SD Processor Brightness     |
| 20   |	Decoder B     |	SD Processor Contrast       |

**Firmware Update**

1. Download the latest firmware package from the releases section, and unzip the files.
2. Find BOOT.bin and copy it to your MicroSD card.
3. Power down your TBC2 and insert the MicroSD card.
4. Power on your system and wait for TBC2 to finish booting.
5. Activate the Update Firmware button on the System page.
6. Wait for firmware update to complete, until you see the System Restart prompt.
7. Activate the Confirm button to restart your system.
8. Confirm that your TBC2 boots to the correct version by comparing version numbers on the System Page. Power off / power on your system if you see the wrong version initially.

**Factory Reset**

1. To reset your TBC2 firmware to the version shipped from the factory, activate the Reset Firmware button on the System page.
2. Wait for firmware reset to complete, until you see the System Restart prompt.
3. Activate the Confirm button to restart your system.
4. Confirm that your TBC2 boots to the factory installed version by comparing version numbers on the System Page.
5. Power off / power on your system if you see the wrong version initially.

## Troubleshooting

If the module is receiving power, but the screen is blank, complete the following procedure:

1. Format a Micro SD card, sized 16gb or smaller.
2. Copy the current TBC2 firmware (available below) onto the card.
3. With the module powered off, install the card in the slot in the front of the module.
4. There are two buttons on the back edge of the module's circuit board. Hold down the top one (labeled "Boot from SD" on early units) and power up the module.
5. Once the module has powered on, select "update firmware" in the menu and let the module complete that process. Once complete, power cycle the module.
6. If the issue persists, please make a service request at the bottom of this page.


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
| Manufacturer Part Number     | 950046 (MK1) 950058 (MK2)                                                       |
| Pronunciation                | TODO                                                                            |
| Mounting Width               | 16 HP                                                                           |
| Mounting Depth               | 55 mm                                                                           |
| Mounting Hole Count          | 4                                                                               |
| Power Consumption            | 12V @ 600 mA                                                                    |
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
| Video Sync                   | Front and rear RCA                                                              |

## Calibration

Calibration is not required for this module.

## Maintenance

Keep your module free of dust and debris by performing periodic cleaning. Spots may be cleaned from the frontpanel with a microfiber cloth and isopropyl alcohol or other electronics cleaner.

## Firmware Downloads

- [TBC2 Firmware 1.0](https://lzxindustries.net/assets/tbc2-firmware_1.0.zip)
- [TBC2 Firmware 1.0.1](https://lzxindustries.net/assets/tbc2-firmware_1.0.1.zip)
- [TBC2 Firmware 1.0.2-mk1 Orion Panel](https://lzxindustries.net/assets/tbc2-firmware_1.0.2-mk1.zip)
- [TBC2 Firmware 1.0.2-mk2 Gen3 Panel](https://lzxindustries.net/assets/tbc2-firmware_1.0.2-mk2.zip)
- [TBC2 Firmware 1.0.3](https://lzxindustries.net/assets/tbc2-firmware_1.0.3.zip)
