---
sidebar_position: 1
---

# Glossary

### Absolute Value

An absolute value function inverts all values below zero and forces the output to be positive.

### Chroma Key Generator

processes the chroma components (PbPr) of a component video signal, allowing key extraction based on Hue and Saturation of the video source

### Clipping Amplifier

Also known as a soft key generator or wide range contrast processor. The output is created by amplifying the video source to create a high contrast mask with variable edge width.

### Comparator

Also known as a hard key generator or 1-bit ADC (Analog-to-Digital converter) function. When the positive input voltage is greater than the negative input voltage, the output is 1 volt (White Level). Otherwise, the output is 0 volts (Black Level).

### Component Key Generator

acts on one color channel at a time, but still includes the entire colorspace in its output function

### Doubler

Also known as a saw-to-triangle waveshaper, the doubler is a combination of an absolute value function and clipping amplifier function.

### Encoder

A video encoder takes 1 volt scale unipolar signals for Red, Green & Blue color channels, and performs all operations required to convert them into a video signal for display or recording.

### Exponential Amplifier

An exponential amplifier changes a linear input voltage into an output with exponential scale.

### Fader

a module which performs a transition between two video sources. typically it has a direct key input, without much local control over the key itself.

### Frame Synchronizer

A frame synchronizer takes an external video feed and synchronizes it with the system's internal timing. A frame synchronizer is usually required to input multiple external video sources into your system like cameras and media players.

### Hard Key

a boolean logic signal which switches between two signals.

### Hard Key Generator

typically implemented as a differential analog comparator.

### Key

any video signal used to control a transition between two or more other video signals

### Key Generator

a module designed to condition an input for the purpose of keying operations

### Keyer

a module which has both a key generator and a fader or switcher

### Linear Colorizer

combines multiple faders with a multi level key generator function to produce a transition across more than two inputs

### Logarithmic Amplifier

An logarithmic amplifier changes a linear input voltage into an output with logarithmic scale.

### Luma Key Generator

processes the luma component (Y) of a component video signal, allowing key extraction based on the overall brightness of the video source

### Maximum Value

A maximum value function compares two or more inputs, and passes the input with the most voltage to the output.

### Minimum Value

A minimum value function compares two or more inputs, and passes the input with the least voltage to the output.

### Multi Level Key Generator

produces multiple key signals from a single source, and are often used as the frontend for colorizers and sequencers

### Negative

Also known as a voltage mirror. The output is equal to the input voltage is subtracted from 1 volt (White Level).

### Ramp Generator

A ramp generator is a waveform generator which produces analog waveforms synchronous to the horizontal or vertical dimensions of the video screen. It is a common component of analog graphics modules, such as shape and pattern generators.

### Soft Key

an analog voltage representing the mix ratio between two video signals

### Soft Key Generator

typically implemented as a high gain differential amplifier with black and white level clipping

### Summing Amplifier

Also known as a Mixer. A summing amplifier adds two or more voltages to each other. The voltages may be unipolar or bipolar scale.

### Voltage Controlled Oscillator (VCO)

A voltage controlled oscillator is similar to a ramp generator, only its frequency may be changed or modulated. A voltage controlled oscillator may be free running, or reset in time with the video sync to synthesize a stable pattern.

### Window Key Generator

has dual threshold controls, either Upper/Lower or Span/Center
