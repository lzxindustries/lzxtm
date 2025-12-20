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

## Updating Firmware

### Requirements

- Videomancer device
- Videomancer power supply
- USB-C to USB-A cable
- A Windows, Mac or Linux computer with generic USB Mass Storage Device drivers.

### Procedure

- Download the desired firmware *.uf2 file from [the Videomancer firmware repository on Github](https://github.com/lzxindustries/videomancer-firmware/releases).
- Connect Videomancer's power supply and turn the power switch to the off position
- Connect USB-C to USB-A cable from Videomancer's USB Device port to your computer
- Press and hold down Videomancer's BOOT button
- Turn Videomancer's power switch to the on position
- Release the BOOT button
- Your computer should show a new storage device attached
- Copy the firmware *.uf2 file to the newly detected storage device
- Wait for the transfer to complete
- Videomancer will reboot into the new firmware version

## Input & Output Configurations

### Changing Video Modes

- Press the SYSTEM button.
- Turn the rotary encoder to select the desired setting:
    - VIDEO ROUTE selects input from either the HDMI input mode or the Analog input mode.
    - ANALOG VIDEO IN selects the input connector used for the Analog input mode.
    - ANALOG VIDEO OUT selects the output format on the Analog output connectors.
- Press down the rotary encoder to start editing the selected setting.
- Turn the rotary encoder to select the desired option.
- Press down the rotary encoder again to confirm your selection.

### Input Configurations

#### HDMI Input

- Connect an HDMI source to the HDMI input.
- Set VIDEO ROUTE to HDMI.

#### Composite Video Input

- Connect a composite video signal to the Analog Y/CVBS input.
- Set VIDEO ROUTE to Analog.
- Set ANALOG VIDEO IN to CVBS.

#### S-Video Input

- Using a Mini DIN-4 to dual RCA adapter, connect the Y component to the Analog Pb/B input and the C component to the Analog Pr/R input.
- Connect your S-Video source to the adapter using an S-Video cable.
- Set VIDEO ROUTE to Analog.
- Set ANALOG VIDEO IN to S-Video.

#### YPbPr Component Input

- Connect a YPbPr Component source to the Analog YPbPr inputs.
- Set VIDEO ROUTE to Analog.
- Set ANALOG VIDEO IN to YPbPr.

#### RGB SOG Component Input

- Connect an RGB SOG Component source to the Analog RGB inputs.
- Set VIDEO ROUTE to Analog.
- Set ANALOG VIDEO IN to RGB SOG.

#### 1V RGB + Sync Input

- Connect 1V RGB signals to the 1V RGB inputs. 
- Connect a sync signal to the Analog Y input.  You can use a sync output from the front or rear of any video module in your modular system, or use any video output synchronous with your modular system.
- Set VIDEO ROUTE to Analog.
- Set ANALOG VIDEO IN to RGB 1V.

### Output Configurations

#### HDMI Output

- Connect the HDMI output to your monitor or capture device.

#### Composite Video Output

- Connect the Y/CVBS output to your monitor or capture device.
- Set ANALOG VIDEO OUT to CVBS/S-Video.

#### S-Video Output

- Using a Mini DIN-4 to dual RCA adapter, connect the Y component to the Analog Pb/B output and the C component to the Analog Pr/R output.
- Connect your adapter to your dmonitor or capture device using an S-Video cable.
- Set ANALOG VIDEO OUT to CVBS/S-Video.

#### YPbPr Component Output

- Connect the YPbPr outputs to your monitor or capture device.
- Set ANALOG VIDEO OUT to YUV.

#### RGB SOG Component Output

- Connect the RGB outputs to your monitor or capture device.
- Set ANALOG VIDEO OUT to RGB.

#### 1V RGB Output

- Connect the 1V RGB outputs to your modular system.
- Set ANALOG VIDEO OUT to RGB.
- Note that Videomancer must be synchronous to your modular system.  You can achieve this by either being in 1V RGB input mode as described above, or by sending Videomancer's sync out to the sync input of your modular system.

## Developer Resources

Videomancer is an open-source FPGA-based video synthesis platform. LZX Industries provides comprehensive development tools and community resources for creating custom video processing programs.

### Videomancer SDK

The official SDK provides everything you need to develop VHDL-based video processing programs for Videomancer hardware. It includes build tools, documentation, example programs, and utilities for creating signed `.vmprog` packages.

**Repository:** [github.com/lzxindustries/videomancer-sdk](https://github.com/lzxindustries/videomancer-sdk)

Key features:
- Complete FPGA development toolchain
- Program development and TOML configuration guides
- Example programs (passthrough, YUV amplifier)
- Visual TOML editor and validation tools
- Package signing with Ed25519 cryptography

### Videomancer Community Programs

A community repository for sharing FPGA video processing programs. This collection extends Videomancer's capabilities with effects, processors, and creative tools contributed by the community.

**Repository:** [github.com/lzxindustries/videomancer-community-programs](https://github.com/lzxindustries/videomancer-community-programs)

Key features:
- Community-contributed VHDL programs
- Automated build scripts for compiling programs
- Contributing guidelines for submitting your own programs
- GPL-3.0 licensed open-source contributions

Both repositories are licensed under GPL-3.0 and welcome community contributions.

