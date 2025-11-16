---
draft: false
sidebar_position: 1
slug: /instruments/videomancer
---

import videomancer_connectors_and_controls from '/img/instruments/videomancer/videomancer-connectors-and-controls.png';

# Videomancer

:::warning
This documentation site is a work in progress, and all content is subject to change before the official launch.
:::

## Connectors & Controls

<img src={videomancer_connectors_and_controls} alt="Videomancer connectors and controls" />
**Connectors and controls**

## How To Update Firmware

### Requirements

- Videomancer device
- Videomancer power supply
- USB-C to USB-A cable
- A Windows, Mac or Linux computer with generic USB Mass Storage Device drivers.

### Procedure

- Download the desired firmware *.uf2 file from [the Videomancer firmware repository on Github](https://github.com/lzxindustries/videomancer-firmware/releases).
- Connect Videomancer's power supply and turn the power switch to the off position
- Connect USB-C to USB-A cable from Videomancer's USB port to your computer
- Press and hold down Videomancer's BOOT button
- Turn Videomancer's power switch to the on position
- Release the BOOT button
- Your computer should show a new storage device attached
- Copy the firmware *.uf2 file to the newly detected storage device
- Wait for the transfer to complete
- Videomancer will reboot into the new firmware version