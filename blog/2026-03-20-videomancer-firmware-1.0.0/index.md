---
slug: videomancer-firmware-1.0.0
title: "Videomancer Firmware 1.0.0"
authors: [lars]
tags: [videomancer, software]
draft: false
---

It's been a busy couple of weeks — two TBC2 firmware updates, a Devin Greenwood artist feature, and a preview release that gave the adventurous among you a taste of what was cooking. As promised, here's the March 20th Videomancer update. Version 1.0.0 is the first official release of the Videomancer firmware.

<!--truncate-->

## What's New

- **25 embedded programs** — Bitcullis, Colorbars, Corollas, Delirium, Elastica, Faultplane, Fauxtress, Glorious, Howler, Isotherm, Kintsugi, Lumarian, Moire, Mycelium, Passthru, Perlin, Pinwheel, Pong, Sabattier, Scramble, Shadebob, STIC, Stipple, YUV Amplifier, and YUV Phaser. Each ships with 3 factory presets.
- **Developer Mode for in-progress programs** — some programs are still work in progress and are hidden by default. Enable **Developer Mode** to view and test those draft programs.
- **New modulation sources** — mouse, keyboard, gamepad, tablet, triggered envelope, step sequencer, and FFT band modes.
- **MIDI output** — CC output mode for controlling external gear from Videomancer parameters.
- **Performance and stability** — eliminated UI lag, fixed pot response, and resolved crashes during FPGA configuration and program switching.

## Download

- [videomancer_1.0.0.uf2](/firmware/videomancer_1.0.0/videomancer_1.0.0.uf2)

## Installation

Power off your Videomancer. Hold the **BOOT** button while connecting USB-C to your computer. The device will appear as a USB drive. Drag and drop the `.uf2` file onto the drive. The device will reboot automatically when the transfer completes.

See the [Videomancer documentation](/docs/instruments/videomancer) for full details.

## Documentation

Updated program guides and modulation operator documentation are available:

- [Program Guides](/docs/category/programs)
- [Modulation Operators](/docs/instruments/videomancer/modulation-operators)
