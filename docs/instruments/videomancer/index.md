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
This documentation is a work in progress, and all content is subject to change before the official documentation launch.
:::

<img src={videomancer_frontpanel} alt="Videomancer front panel"/>

<img src={videomancer_rearpanel} alt="Videomancer rear connections"/>

## Overview

Videomancer is a standalone instrument and development platform for video synthesis. Its open source hybrid digital/analog architecture leverages the best of both domains. With a full complement of inputs and outputs for every signal type, it integrates seamlessly with any studio or performance rig. Videomancer supports a wide range of standard and high definition video formats.

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

Each of Videomancer's 12 Parameters can be driven by any modulation input, or by a unique low frequency oscillator per each Parameter.

### Architecture

Under the hood, Videomancer is an *embedded system*, a special-purpose computer driven by a Field-Programmable Gate Array (FPGA). This is a type of processor that can be configured &ldquo;in the field&rdquo; to implement different circuits via firmware. That means Videomancer can perform many different functions with a level of efficiency that would otherwise require custom-designed hardware for each function. Instead of a different physical circuit, the FPGA simply loads a different firmware program. This approach diverges radically from conventional digital graphics that rely on parallel processing on a GPU. Videomancer's architecture imparts extraordinary versatility and power, while remaining affordable, portable, and power-efficient.

Another benefit of Videomancer's FPGA architecture is ultra-low latency, in the range of 0.0001 to 0.0007 millisecond. Conventional digital video devices insert at least one frame of delay, which is 33 milliseconds at 30 frames per second. Videomancer is orders of magnitude faster. Latency is absolutely imperceptible, giving immediate feedback in applications such as audio reactivity.

LZX is committed to making video synthesis affordable to working artists, not just big studios. To keep costs down, Videomancer's design requires very little volatile memory. It can only hold a few lines of video in memory at a time. That's enough for certain effects that are impossible in the analog domain, such as vertical blurring. But it's not enough to store an entire frame, so Videomancer isn't a frame store. It can't convert resolutions or frame rates, or sync one video signal to another. For those capabilites, we offer the [TBC2 Dual Video Input](/docs/modules/tbc2) Eurorack module.

### Legacy

Videomancer is the second standalone instrument released by LZX, the first being the popular **Vidiot**. Videomancer shares very little DNA with Vidiot beyond support for the LZX 1V modular standard. Vidiot was envisioned as an entry-level semi-modular instrument with fixed functionality. In contrast, Videomancer is a development platform whose capabilities will continue to expand over time. 15 years of continuous design and manufacturing expertise have culminated in an instrument highly optimized for creativity, portability, expandability, and efficiency. The firmware of Videomancer is part of a shared code base that also finds expression within instruments currently under development, such as Chromagnon, and instruments planned for the future, such as Memory Palace Mk II. The open source Software Developer's Kit opens the door for third party community developers to contribute programs to Videomancer, enriching the creative possibilities for all artists who use the instrument.

---

## Key Specifications

| Parameter         | Value                                                                           |
| ----------------- | ------------------------------------------------------------------------------- |
| Dimensions (mm)   | 234.2 width / 178.1 depth / 75.44 height                                        |
| Dimensions (inch) | 9.22 width / 7.01 depth / 2.97 height                                           |
| Power Consumption | 12V @ 1000 mA                                                                   |
| Power Connectors  | 2.1mm DC barrel                                                                 |
| Included          | International power supply                                                      |
| Video Sync        | Rear RCA Sync out, rear RCA Multi-format Analog in                              |

---

## Connectors, Controls, and Indicators

<img src={videomancer_connectors_and_controls} alt="Videomancer connectors and controls" />

---

### Connectors

* **HDMI** digital video/audio in and out
    - Full-size HDMI jacks
    - Supporting a wide range of digital video [formats](/docs/instruments/videomancer#supported-formats-and-standards)
* **Multi-format Analog** video in and out
    - Triple RCA jacks configurable as:
        - CVBS composite
        - S-Video (Y/C) component
        - YPbPr component
        - RGB component with sync on green (RGsB / SoG)
* **Video Sync** out
    - RCA jack
    - For genlocking a modular system or other video devices to Videomancer
* **1v RGB** video in and out
    - Triple TS mini-jacks
    - DC-coupled [LZX modular standard](/docs/guides/standards)
* **Audio/CV** inputs
    - Four signal inputs on two TRS stereo mini-jacks
    - Configurable as control voltages or line level audio signals
* **MIDI** in and out
    - TRS mini-jacks
    - MIDI standard Type A
    - Input signal passed through to output
* **USB** ports
    - USB-C jacks
    - **Device** port for connection to PC
    - **Host** port for future functionality
* **microSD** card slot
    - For future functionality
* **DC Power**
    - Barrel jack
        - 2.1 mm diameter center conductor
    - Power supply requirements:
        - 12 Volts
        - Minimum 1000 mA
        - Center positive

---

### Controls

**Front Panel Controls**

* **Rotary Encoder**
    - Incremental digital data entry
    - Turn to choose an option, push to execute
    - Define global System settings
    - Choose Motion mode per Parameter
    - Load and save State user presets
* **Navigation** buttons
    - Press to access a function on the LCD display
    - White buttons: **SYSTEM**, **MOTION**, and **STATE** functions
    - Black buttons labeled **1** through **&ast;** : switch *focus* to Parameter 1 through 12
* **Motion** control knobs
    - Adjust modulation for the currently *focused* Parameter
* **Parameter** control knobs
    - Manually adjust continuous Parameters 1 through 6
* **Toggle** control switches
    - Manually enable / disable binary Parameters 7 though 11
* **Slider** Parameter control
    - Manually adjust continuous Parameter 12
* **Transport** buttons
    - **Start** and **Stop** modulation in Sync mode
    - **Tap** to set tempo in beats per minute

**Rear Chassis Controls**

* **Power** switch
* **Boot** button
    - For [firmware update](/docs/instruments/videomancer#firmware-update)

---

### Indicators

**Front Panel Indicators**

* LCD screen
    - User feedback for System settings and functions, States, Motion modes, and Parameter values
* Front panel LED lights
    - Parameter knob, switch, and fader LEDs indicate the currently focused Parameter: 1 through 12
    - **Motion** knob LEDs indicate the active Motion control: **Time**, **Space**, **Slope**
    - **Start** and **Stop** LEDs indicate transport playback status
    - **Tap** LED flashes during transport playback to indicate tempo

**Rear Chassis Indicators**

* **Power** LED light
* **HDMI** input and output LED lights
    - Illuminate when HDMI status is active and locked


---

## Signal Paths


### Supported Formats and Standards

Videomancer genlocks to incoming video, assuming the timing, resolution, and frame rate of the source. It can't convert raster formats, so there's no function to choose resolutions or frame rates.

| Resolution and frame rate standards           |
|-----------------------------------------------|
| 240p29 (planned)                              |
| 288p25 (planned)                              |
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

Videomancer can convert between various color spaces and color encoding formats. Choose the input and output options via the System menu, as described in [Video Routing](/docs/instruments/videomancer#video-routing) below.

| Color formats                         |
|---------------------------------------|
| HDMI YCbCr (YUV)                      |
| YPbBr component (YUV)                 |
| RGsB component (Sync On Green)        |
| Composite (CVBS)                      |
| S-Video (Y/C)                         |

---

### Video Routing

To choose from the available video inputs and outputs, follow this procedure:

- Press the **SYSTEM** button
- Turn the rotary encoder to select the desired setting:
    - **VIDEO ROUTE** selects input from either **HDMI** or **Multi-format Analog** RCA jacks
    - **ANALOG VIDEO IN** selects the active **Multi-format Analog** RCA input jacks and the color format
    - **ANALOG VIDEO OUT** selects the active **Multi-format Analog** RCA output jacks and the color format
- Press the Rotary Encoder once to edit the selected setting
- Turn the Rotary Encoder to select an option
- Press the Rotary Encoder again to confirm the option

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
Videomancer is an ultra-low latency digital signal processing device, but it can never be as fast as a dedicated analog circuit. Any video going through Videomancer is delayed slightly. If Videomancer is patched into the *middle* of a modular system, between the modular decoder and the modular encoder, Videomancer's output will be shifted to the right relative to the rest of the modular system. The amount of horizontal shift depends on video resolution, frame rate, and the particular program loaded into Videomancer.

Therefore, inserting Videomancer between a modular decoder and encoder is not a recommended configuration. Using Videomancer as an &ldquo;effects send&rdquo; may be possible in exotic scenarios where the modular decoder, encoder, and/or sync generator are not sharing the same sync reference, but that would be a non-standard, advanced, experimental configuration.
:::

---

## Operation

### System

Pressing the **SYSTEM** button activates the System menu. By default, the current System status, input, and format are displayed. Turn the Rotary Encoder to cycle through the System submenus:

* **PROGRAM**
* **VIDEO ROUTE**
* **ANALOG IN**
* **ANALOG OUT**
* **MIDI CHANNEL**

To make changes to System settings:

* Turn the Rotary Encoder to choose a System submenu
* Press the Rotary Encoder to move the cursor to the bottom row
* Turn the Rotary Encoder to change the setting
* Press the Rotary Encoder to confirm the setting

---

### States

A State is a user-defined preset including all information on the current conditions of Videomancer. All System, Motion, and Parameter values are stored within the State. States are stored in non-volatile internal flash memory. Internal storage provides 128 State registers, numbered 0 to 127. Future firmware plans include storing States on microSD card.

To save a State:

* Press the **STATE** button
* Turn the Rotary Encoder to select a State register number
* Long-press and hold the Rotary Encoder for at least two seconds
* Press the Rotary Encoder again to confirm the Save operation

To load a State:

* Press the **STATE** button
* Turn the Rotary Encoder to select a State register number
* Press the Rotary Encoder
* Press the Rotary Encoder again to confirm the Load operation

---

### Programs

Videomancer includes numerous Programs, which are firmware applications that can be loaded on the fly. To load a program:

* Press the **SYSTEM** button
* Turn the Rotary Encoder to select the **PROGRAM** submenu
* Press the Rotary Encoder to move the cursor to the bottom row, where the name of the current Program is displayed
* Turn the Rotary Encoder to select a Program
* Press the Rotary Encoder to load the Program

:::warning
When Videomancer loads a Program, all outputs will be disabled for a few seconds. During Program load, no video or sync signal is present at the outputs. Any downstream video device does not receive a signal, so it may display black, a blue screen, or an error message such as "no signal detected". If this is an issue, such as during a live performance, send Videomancer through a device such as a mixer that always outputs a valid video signal.
:::

:::note
Some Programs may default to a black output. Typically, the **&ast; Slider** for Parameter 12 performs the function of fading to black, or luminance keying to black. After loading a Program, it may be necessary to move the Slider to its furthest extents in order to see an image.
:::

Programs include:

* **[Bitcullis](/docs/instruments/videomancer/bitcullis)**
    - Bit-crushing / culling / decimation in horizontal and vertical dimensions
    - **Posterize**, **Bit Swap**, **Dither**
* **[Faultplane](/docs/instruments/videomancer/faultplane)**
    - **Delay** (horizontal shift), **Displace** (skew), **Flip** (horizontal mirror)
    - Two independent sets of interleaved transforms, **Top** and **Bottom**
* **[Lumarian](/docs/instruments/videomancer/lumarian)**
    - Proc amp controls: **Brightness**, **Contrast**, **Saturation**, **Gamma**
    - Horizontal edge detection, **Gain**, **Cutoff**, **Rectify**
* **Passthru**
    - Test Program, no effects
    - Invert Y, U, and V on Switches 7 through 9
* **[Pinwheel](/docs/instruments/videomancer/pinwheel)**
    - Hue and saturation processing
    - Map luminance to hue and saturation
* **YUV Amplifier**
    - **Gain** (amplitude) and **Offset** (bias) of individual YUV color components
* **YUV Phaser**
    - **Phase** and **Displace** (horizontal shift) of individual YUV color components

---

### Parameters

Any Parameter 1 through 12 can be adjusted manually at any time via the Parameter Knobs, Switches, or Fader. If Videomancer is in Parameter display mode, then the Parameter number, name, and values of the *focused* Parameter are shown onscreen.

If Videomancer is in **SYSTEM**, **MOTION**, or **STATE** mode, then the LCD display shows the menus for that mode. In this case, the properties of the focused Parameter are not displayed. However, all Parameter controls are still active, and the Motion controls for the focused Parameter are also active.

To enter Parameter display mode, press any of the Parameter buttons labeled **1** through **&ast;** (Parameters 1 through 12). The selected Parameter is given focus and its properties are displayed.

If Parameter display mode is active, simply moving a Parameter control brings that Parameter into focus and displays the Parameter's **Manual** value onscreen. Moving a **Time**, **Space**, or **Slope** control knob displays the associated Motion property and its value.

All Parameter controls employ a soft takeover method for updating the value. The physical control must be moved beyond the current parameter value in order to take effect. When the Parameter value doesn't match the physical control position, an **exclamation point** is displayed on the left side of the value.

---

### Motion

Each Parameter can be separately modulated by its own individual **MOTION** source. Modulation is summed with the **Manual** value set by the Parameter knob, switch, or fader control. The Manual control acts as a bias or offset to the modulation.

To choose a Motion mode:

* Press the button or adjust the control of the desired Parameter to give it focus
* Press the Rotary Encoder or turn it by one increment to display the current Motion mode
* Turn the Rotary Encoder to cycle through the available Motion modes

Selection of a Motion mode takes place immediately.

When the Motion mode menu is displayed, pressing the Rotary Encoder sets the Motion mode to **Off**, disabling all modulation.

:::tip
To quickly disable modulation for the focused Parameter, press the Rotary Encoder twice.
:::

**MOTION** modes include:
* **Off**
    - Modulation disabled
* **Free LFO**
    - Internal free-running low frequency oscillator
    - Not synchronized to anything
* **Sync LFO**
    - Internal low frequency oscillator
    - Synchronized to the internal clock or external MIDI
* **CV**
    - External low frequency control voltage
    - From one or two channels of the **AUDIO/CV** inputs
    - Voltage range before clipping: +6.6V to -6.6V
    - Sampled at video frame or field rate, preventing frame tearing
* **Audio**
    - External line level audio or mid-frequency control voltage
    - From one or two channels of the **AUDIO/CV** inputs
    - Sampled at video line rate
* **Random**
    - Internal low frequency random noise source

---

#### MOTION Control Knobs

Motion properties are adjusted with the **Time**, **Space**, and **Slope** knobs.

**Space** always controls the **Gain** or amplitude of modulation. The range of the Gain property depends on the current Motion mode. For example, **LFO** modes have a maximum Gain of 100%. **CV** and **Audio** modes have a maximum Gain of 400% to accommodate sources with different voltage ranges.

**Time** and **Slope** knobs perform different functions depending on the active **MOTION** mode.

**Free LFO** and **Sync LFO**:
* **Slope** = waveform **Shape**
    - **Ramp** (rising)
    - **Sawtooth** (falling)
    - **Triangle**
    - **Square**
    - **Sine**
    - **Logarithmic** (fast out)
    - **Exponential** (slow out)
    - **Parabola**

**Free LFO**:
* **Time** = **Frequency**
    - Oscillation period, in seconds

**Sync LFO**:
* **Time** = **Division**
    - Oscillation period expressed as the ratio of beats divided by oscillator cycles
    - Beats ÷ oscillations
    - E.g. 1/4 = one beat per four oscillations, 4/1 = four beats per oscillation

**CV** and **Audio**:
* **Time** = **Slew** rate
    - Similar to a lowpass filter, removes high frequency components of the control signal
* **Slope** = **Input** channel selector
    - If a channel pair is selected, then the modulation is the sum of the two channel values

**Random**:
* **Time** = **Rise**
* **Slope** = **Fall**
    - **Rise** and **Fall** constrain the random values, not the frequency of the noise
    - Setting **Rise** and **Fall** to zero freezes the noise at a constant value
    - Setting **Rise** and **Fall** to 100% gives the full range within the **LFN Gain** property set by the **Space** knob

Within a Motion property page, the current mode is indicated by the following abbreviations:

* **Free LFO** = **LFO**, Low Frequency Oscillator
* **Sync LFO** = **LFSO**, Low Frequency Synchronized Oscillator
* **CV** = **LFCV**, Low Frequency Control Voltage
* **Audio** = **HFCV**, High Frequency Control Voltage
* **Random** = **LFN**, Low Frequency Noise

---

### Tempo

**Sync LFO** Motion mode locks the period of the internal oscillator to a clock frequency. The clock source can be Videomancer's internal timecode, or an external MIDI source.

Press the **MOTION** button to display the current values of Timecode (**TC**) and Beats Per Minute (**BPM**).

Sync LFO mode is deterministic based on the value of Videomancer's timecode, whether that is internally generated, or externally provided via MIDI. All Sync LFO oscillators begin with a phase of zero at timecode value `00:00:00:00`. If the Time properties of Sync LFOs are constant, then the exact same phase relationships are preserved on each playback.

#### Internal Synchronization

Press the **START** button to globally activate playback of internal timecode.

Press the **STOP** button to globally deactivate playback of internal timecode and reset the time index to `00:00:00:00`.

:::note
Videomancer does not have a manual pause button. Stopping playback sends the timecode value to zero, resetting the phase of all oscillators. Use [MIDI Timecode](/docs/instruments/videomancer#midi-synchronization) if you wish to pause and resume playback.
:::

#### Internal BPM Tempo

To change the **BPM** value numerically:
    - Press the **MOTION** button
    - Turn the Rotary Encoder

To change the **BPM** value rhythmically while playback is stopped:
    - Press the **MOTION** button
    - Press the **TAP** button once to begin sampling the tempo
    - Press the **TAP** button again to finish sampling the tempo

To change the **BPM** value rhythmically during playback:
    - Press the **TAP** button once to begin sampling the tempo
    - Press the **TAP** button again to finish sampling the tempo

The new tempo takes effect immediately.

---

### MIDI Synchronization

A MIDI signal supplied to Videomancer automatically overrides the internal timecode.

By default, Videomancer receives MIDI on all channels (Omni). To change the MIDI channel:

* Press the **SYSTEM** button
* Turn the Rotary Encoder to the **MIDI CHANNEL** menu
* Press the Rotary Encoder to move the cursor to the bottom row
* Turn the Rotary Encoder to select a MIDI channel
* Press the Rotary Encoder to confirm MIDI channel selection

**BPM** setting is determined by incoming MIDI Clock or MIDI Timecode (MTC). Videomancer adopts the current incoming MIDI BPM tempo, even when the MIDI source is stopped. Any manual changes to BPM are overridden by incoming MIDI on the next beat.

Transport functions are also overridden by incoming MIDI Clock or MIDI Timecode. When the MIDI source starts or stops, Videomancer transport also starts or stops. However, if the MIDI source is stopped, Videomancer transport controls still function. We can press the **START** or **STOP** buttons to control playback while the MIDI source is not playing. However, we can't change the BPM as long as the MIDI source is transmitting MIDI Clock or MIDI Timecode.

MIDI Clock Start and Stop signals perform the same functions as the **START** and **STOP** buttons. MIDI Clock Stop resets the Videomancer timecode to `00:00:00:00`, regardless of the timecode value of the MIDI source. MIDI Clock Continue and Song Pointer signals are ignored. Therefore, MIDI Clock is a relative time index, not an absolute one.

MIDI Timecode is an absolute time reference. Videomancer timecode follows the current MIDI Timecode value, but only during playback. Stopping or pausing the MIDI source causes Videomancer timecode to stop, but does not reset to zero. Starting the MIDI source causes Videomancer timecode to update to the incoming MIDI Timecode value, so we can pause and resume playback without resetting oscillator phase. Any other transport controls on the MIDI source, such as rewind, fast forward, or skipping to a different timecode value, have no effect on Videomancer's timecode. Videomancer only responds when MIDI Timecode plays or stops.

If the MIDI source transmits both MIDI Clock and MIDI Timecode, Videomancer gives priority to MIDI Clock. Videomancer timecode is reset to zero when the MIDI source stops.

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

