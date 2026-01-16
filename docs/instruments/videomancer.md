---
draft: false
sidebar_position: 1
slug: /instruments/videomancer
---

import videomancer_connectors_and_controls from '/img/instruments/videomancer/videomancer-connectors-and-controls.png';

import videomancer_frontpanel from '/img/instruments/videomancer/videomancer_frontpanel.png';

import videomancer_rearpanel from '/img/instruments/videomancer/videomancer_rearpanel.png';

# Videomancer

:::warning
This documentation site is a work in progress, and all content is subject to change before the official launch.
:::

<img src={videomancer_frontpanel} alt="Videomancer front panel"/>

<img src={videomancer_rearpanel} alt="Videomancer rear connections"/>

## Overview

Videomancer is a standalone instrument and development platform for video synthesis. Its open source hybrid digital/analog architecture leverages the best of both domains. With a full complement of inputs and outputs for every signal type, it integrates seamlessly with any studio or performance rig. Videomancer supports a wide range of standard and high definition video formats.

**Inputs and outputs:**

* HDMI digital video/audio in and out
* RCA Multi-format Analog video in and out, configurable as:
    - CVBS composite
    - S-Video (Y/C) component
    - YPbPr component
    - RGB component with sync on green (RGsB / SoG)
* RCA analog Video Sync out
* TS mini-jack 1v modular RGB video in and out
* 2x TRS stereo mini-jack inputs, configurable as control voltages or line level audio signals
* TRS mini-jack Type A MIDI in and MIDI through
* USB-C USB Device and USB Host ports
* microSD card slot

Due to its extraordinary versatility, Videomancer can perform many functions, including but not limited to:

* Process HDMI or analog video
* Convert conventional analog video to HDMI
* Convert HDMI to conventional analog video
* Decode conventional analog video to 1v modular RGB
* Decode HDMI to 1v modular RGB
* Encode 1v modular RGB to conventional analog video
* Encode 1v modular RGB to HDMI
* Modulate video with audio
* Modulate video with low frequency control voltages
* Modulate video with MIDI
* Synchronize modulation with MIDI
* Define modulation frequencies with BPM or tap tempo

Each of Videomancer's 12 parameters can be driven by any modulation input, or by a unique low frequency oscillator per each parameter. Incoming control voltages are automatically sampled and held for each frame or field of video, preventing frame tearing. This behavior can be disabled by simply switching the input mode to Audio instead of CV.

### Architecture

Under the hood, Videomancer is an *embedded system*, a special-purpose computer driven by a Field-Programmable Gate Array (FPGA). This is a type of processor that can be configured &ldquo;in the field&rdquo; to implement different circuits via firmware. That means Videomancer can perform many different functions with a level of efficiency that would otherwise require custom-designed hardware for each function. Instead of a different physical circuit, the FPGA simply loads a different firmware program. This approach diverges radically from conventional digital graphics that rely on parallel processing on a GPU to emulate particular circuits. All of this results in Videomancer being extraordinarily versatile and powerful, while remaining affordable, portable, and power-efficient.

Another benefit of Videomancer's FPGA architecture is ultra low latency, in the range of 0.0001 to 0.0007 millisecond. All conventional digital video devices insert at least one frame of delay, which is 33 milliseconds at 30 frames per second. Videomancer's delay is absolutely imperceptible, giving immediate feedback in applications such as audio reactivity.

LZX is committed to making video synthesis affordable to working artists, not just big studios. To keep costs down, Videomancer's design has very little volatile memory. It can only hold a few lines of video in memory at a time. That's enough for certain effects that are impossible in the analog domain, such as vertical blurring. But it's not enough to store an entire frame, so Videomancer isn't a frame store. It can't convert resolutions or frame rates, or sync one video signal to another. For those capabilites, we offer the [TBC2 Dual Video Input](/docs/modules/tbc2) module.

### Legacy

Videomancer is the second standalone instrument released by LZX, the first being the popular **Vidiot**. Videomancer shares almost zero DNA with Vidiot beyond support for the LZX 1V modular standard. Vidiot was envisioned as an entry-level semi-modular instrument with fixed functionality. In contrast, Videomancer is a development platform whose capabilities will continue to expand over time. 15 years of continuous design and manufacturing expertise have culminated in an instrument highly optimized for creativity, portability, expandability, and efficiency. The firmware of Videomancer is part of a shared code base that also finds expression within instruments currently under development, such as Chromagnon, and instruments planned for the future, such as Memory Palace Mk II. The open source Software Developer's Kit opens the door for third party community developers to contribute programs to Videomancer, enriching the creative possibilities for all artists who use the device.

---

## Connectors & Controls

<img src={videomancer_connectors_and_controls} alt="Videomancer connectors and controls" />

---

## Signal Paths

### Video Routing and Color Formats

To choose from the available video inputs and outputs, follow this procedure:

- Press the **SYSTEM** button
- Turn the rotary encoder to select the desired setting:
    - **VIDEO ROUTE** selects input from either **HDMI** or **Multi-format Analog** RCA jacks
    - **ANALOG VIDEO IN** selects the active **Multi-format Analog** RCA input jacks and the color format
    - **ANALOG VIDEO OUT** selects the active **Multi-format Analog** RCA output jacks and the color format
- Press the rotary encoder once to edit the selected setting
- Turn the rotary encoder to select an option
- Press the rotary encoder again to confirm the option

---

### Input Configurations

#### HDMI in

* Connect a source to the **HDMI** input
* Set **VIDEO ROUTE** to **HDMI**

#### Composite (CVBS) video in

* Connect a composite video signal to the **Analog Y/CVBS** input
* Set **VIDEO ROUTE** to **Analog**
* Set **ANALOG VIDEO IN** to **CVBS**

#### S-Video in

* Using a Mini DIN-4 to dual RCA adapter, connect the **Y** (luminance) component to the **Analog Pb/B** input and the **C** (chroma) component to the **Analog Pr/R** input
* Connect an S-Video source to the adapter with an S-Video cable
* Set **VIDEO ROUTE** to **Analog**
* Set **ANALOG VIDEO IN** to **S-Video**

#### YPbPr component in

* Connect a YPbPr Component source to the **Multi-format Analog** inputs
* Set **VIDEO ROUTE** to **Analog**
* Set **ANALOG VIDEO IN** to **YPbPr**

#### RGB Sync on Green (SoG) component in

* Connect an RGB SoG component source to the **Multi-format Analog** inputs
* Set **VIDEO ROUTE** to **Analog**
* Set **ANALOG VIDEO IN** to **RGB SoG**

#### 1V RGB + Sync in

* Connect 1V RGB signals to the **1V RGB** inputs
* Connect a sync signal to the **Analog Y** input
    - Take a sync output from the front or rear of any module
    - Or take any video output that includes embedded sync, and is in sync with the modular system. For example, the following RCA jacks of ESG3 all include sync:
        - **CVBS**
        - The **Y** output in **YPbPr** mode
        - The **Green** output in **RGB / SoG** mode
* Set **VIDEO ROUTE** to **Analog**
* Set **ANALOG VIDEO IN** to **RGB 1V**

:::note
Videomancer needs to receive a sync reference. That can come from sync embedded in the HDMI or conventional analog video source. 1V modular RGB does not carry sync, so sync must be supplied separately. Sync can come directly from the modular system, or from some other video device that is in sync with the modular system.
:::

---

### Output Configurations

#### HDMI out

- Connect the **HDMI** output to a monitor or capture device

#### Composite video out

* Connect the **Y/G/CVBS** output to a monitor or capture device
* Set **ANALOG VIDEO OUT** to **CVBS/S-Video**

#### S-Video out

* Using a Mini DIN-4 to dual RCA adapter, connect the **Y** component to the **Analog Pb/B** output and the **C** component to the **Analog Pr/R** output
* Connect the adapter to a monitor or capture device using an S-Video cable
* Set **ANALOG VIDEO OUT** to **CVBS/S-Video**

#### YPbPr component out

* Connect the **YPbPr** outputs to a monitor or capture device
* Set **ANALOG VIDEO OUT** to **YUV**

#### RGB Sync on Green (SoG) component out

* Connect the **RGB** outputs to a monitor or capture device
* Set **ANALOG VIDEO OUT** to **RGB**

#### 1V RGB + Sync out

* Connect the **1V RGB** outputs to the modular system
* Connect the **SYNC** output to the sync input of the modular system
* Set **ANALOG VIDEO OUT** to **RGB**

:::note
Videomancer automatically syncs to any conventional video signal patched to the HDMI or RCA inputs. However, it is not a frame store like TBC2. To use Videomancer as a decoder to convert to 1v modular video, patch the Videomancer Sync output to the sync input of the modular system.
:::

:::warning
Videomancer is an ultra low latency digital signal processing device, but it can never be as fast as a dedicated analog circuit. Any video going through Videomancer is delayed slightly. If Videomancer is patched into the *middle* of a modular system, between the modular decoder and the modular encoder, Videomancer's output will be shifted to the right relative to the rest of the modular system. The amount of horizontal shift depends on video resolution, frame rate, and the particular program loaded into Videomancer.

Therefore, inserting Videomancer between a modular decoder and encoder is not a recommended configuration. Using Videomancer as an &ldquo;effects send&rdquo; may be possible in exotic scenarios where the modular decoder, encoder, and/or sync generator are not sharing the same sync reference, but that would be a non-standard, advanced, experimental configuration.
:::

---

## Operation

### Supported Formats and Standards

Videomancer can convert between various color spaces and color encoding formats. Choose the input and output options via the **SYSTEM** menu, as described in the [Video Routing and Color Formats](/docs/instruments/videomancer#video-routing-and-color-formats) section.

| Color formats                         |
|---------------------------------------|
| HDMI YCbCr (YUV)                      |
| YPbBr component (YUV)                 |
| RGsB component (Sync On Green)        |
| Composite (CVBS)                      |
| S-Video (Y/C)                         |

---

Videomancer genlocks to incoming video, assuming the timing, resolution, and frame rate of the source. It can't convert raster formats, so there's no function to choose resolutions or frame rates.

| Resolution and frame rate standards           |
|-----------------------------------------------|
| 240p29                                        |
| NTSC 486i59                                   |
| PAL 576i50                                    |
| 480p29                                        |
| 576p25                                        |
| 720p50                                        |
| 720p59                                        |
| 720p60                                        |
| 1080i50                                       |
| 1080i59                                       |
| 1080i60                                       |
| 1080p23                                       |
| 1080p24                                       |
| 1080p25                                       |
| 1080p29                                       |
| 1080p30                                       |

---

## Firmware Update

Keeping Videomancer updated with the latest firmware ensures access to the latest programs, features, and bug fixes. The process is very simple and only takes a few minutes.

### Requirements

- Videomancer and power supply
- Windows, Mac or Linux computer
- USB-A to USB-C cable

### Procedure

- Download the desired firmware `.UF2` file from the Videomancer [firmware repository](https://github.com/lzxindustries/videomancer-firmware/releases)  on GitHub
- Connect Videomancer to power supply and switch power to the **OFF** position
- Connect the computer's USB-A port to Videomancer's USB-C **Device** port (not the Host port)
- Hold down Videomancer **BOOT** button
- Switch Videomancer power to the **ON** position
- Release the **BOOT** button
- A new USB storage device is listed in the computer's filesystem. It shows up as a Raspberry Pi, because that's the control system for Videomancer's USB ports.
- Copy the firmware `.UF2` file to the newly detected storage device. Wait a few minutes for the transfer to complete.
- Videomancer automatically reboots into the new firmware and displays the currently installed version

---

## Developer Resources

Videomancer is an open-source FPGA-based video synthesis platform. LZX Industries provides comprehensive development tools and community resources for creating custom video processing programs.

### Videomancer SDK

The official Software Developer's Kit provides everything needed to develop programs for Videomancer with the VHDL hardware description language. The SDK includes build tools, documentation, example programs, and utilities for creating signed `.VMPROG` packages.

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

