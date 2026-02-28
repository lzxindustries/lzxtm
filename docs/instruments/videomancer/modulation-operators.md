---
draft: true
sidebar_position: 2
slug: /instruments/videomancer/modulation-operators
title: "Videomancer: Modulation Operators"
description: "Complete reference guide for Videomancer's 32 modulation operator types across 12 channels, including oscillators, envelope followers, random generators, sequencers, spatial modulators, and physics simulations."
---

# Modulation Operators

## Overview

Every FPGA program on Videomancer exposes up to twelve parameters — six rotary knobs, five toggle switches, and one fader. In normal operation, those parameters sit wherever you leave them. The modulation engine changes that. It writes new values to those parameters automatically, every video field, so the controls move on their own.

Twelve **modulator channels** (P1 through P12) map one-to-one onto the twelve physical controls. Each channel runs an independent **operator** — a small signal-processing algorithm that produces a stream of values between 0 and 1023. That stream replaces (or combines with) the manual knob position, causing the FPGA program's behavior to change over time without you touching anything.

There are 32 operator types. Some are simple oscillators. Some read external voltage or audio signals. Some simulate physics. Some generate algorithmic patterns. The variety exists because different kinds of motion suit different creative contexts — a slow sine wave feels nothing like a bouncing ball, and a cellular automaton produces patterns that no oscillator can.

---

## How Modulation Works

### Signal Path

```
Manual Knob Position (0–1023)
    + MIDI CC Offset
    ───────────────────────┐
                           ▼
                    ┌─────────────┐
                    │  Operator   │ ← Time / Space / Slope parameters
                    │  (1 of 32)  │ ← ADC input (some modes)
                    │             │ ← Transport phase (some modes)
                    │             │ ← Random seed (some modes)
                    └──────┬──────┘
                           │ output (0–1023)
                           ▼
                    ┌─────────────┐
                    │  Gain /     │
                    │  Boolean    │
                    └──────┬──────┘
                           │
                           ▼
                  FPGA Register Write
```

Each modulator updates once per video field (approximately 60 times per second at 59.94 Hz, or 50 times per second at 50 Hz). Some operators also produce **per-line** output — a different value for every scanline within the field — which allows modulation to vary spatially across the frame.

### The Three Parameters

Every operator receives three control values from dedicated knobs on the Videomancer front panel:

| Parameter | Knob | Role |
|-----------|------|------|
| **Time** | M1 | Controls *rate* or *speed* — how fast the operator evolves. For oscillators, this is the period. For followers, it is the slew rate. For physics simulations, it controls a force constant. |
| **Space** | M2 | Controls *amplitude* or *depth* — how much the operator's output affects the target parameter. Often labeled "Gain" or "Depth." |
| **Slope** | M3 | Controls *character* or *shape* — which waveshape, which input channel, how much chaos, which rule. This is the qualitative parameter that changes *what kind* of signal the operator produces. |

The exact meaning of each parameter depends on the active operator. The display labels update automatically when you change modes, so you always see what Time, Space, and Slope do for the current operator.

### Linear vs. Boolean

Modulators operate in one of two output modes:

- **Linear**: Outputs a continuous value from 0 to 1023. Used for knobs and faders.
- **Boolean**: Outputs 0 or 1. Used for toggle switches. The operator's 10-bit output is thresholded — above 512 is "on," at or below 512 is "off."

---

## Operator Reference

### Oscillators

These operators generate periodic waveforms. They are the workhorses of modulation — use them whenever you want a parameter to move back and forth in a repeating pattern.

---

#### 0 — Disabled

| Parameter | Label | Function |
|-----------|-------|----------|
| Time | Time | *(unused)* |
| Space | Space | *(unused)* |
| Slope | Slope | *(unused)* |

**Per-line**: No

Passthrough. The modulator outputs the manual knob position plus any MIDI CC offset, with no modulation applied. This is the default state — select it to return a channel to manual control.

---

#### 1 — Free LFO

| Parameter | Label | Function |
|-----------|-------|----------|
| Time | Rate | Oscillator period. Fully clockwise = 50 ms (fast). Fully counter-clockwise = 20 seconds (slow). The rate follows a logarithmic-squared curve, so most of the knob's travel is in the slow-to-moderate range, with fast rates concentrated at the top end. |
| Space | Depth | Output amplitude. At zero, the oscillator runs but produces no output. At maximum, the full 0–1023 range is used. |
| Slope | Wave | Waveshape select. Eight shapes are available, evenly spaced across the knob: ramp, sawtooth, triangle, square, sine, logarithmic, exponential, and parabola. |

**Per-line**: No

A free-running low-frequency oscillator. This is the most straightforward modulation source — a repeating waveform at a controllable rate. The oscillator runs continuously regardless of transport state and does not lock to any external clock. Phase accumulates indefinitely, so the waveform never resets unless you switch away and back.

The eight waveshapes cover the fundamental periodic functions. Triangle and sine produce smooth, rounded motion. Square produces hard switching between two values (useful for toggling effects on and off rhythmically). Ramp and sawtooth produce asymmetric sweeps — one direction slow, the other instant. Logarithmic and exponential produce curves that spend more time near one extreme than the other. Parabola produces a rounded bounce shape.

---

#### 2 — Sync LFO

| Parameter | Label | Function |
|-----------|-------|----------|
| Time | Division | Musical time division. Ten divisions from 16 bars (very slow) down to 1/8 note (fast): 16/1, 8/1, 4/1, 3/1, 2/1, 1/1, 1/2, 1/3, 1/4, 1/8. |
| Space | Depth | Output amplitude. |
| Slope | Wave | Waveshape select (same eight shapes as Free LFO). |

**Per-line**: No

A tempo-synced LFO whose speed is derived from the current BPM. Unlike Free LFO, this oscillator only advances when the transport is playing — it freezes when playback stops. The oscillator maintains its own phase accumulator but locks its step size to the transport tempo, so the waveform stays in rhythmic relationship to the beat.

The musical divisions are multiplicative: at 1/1 division, the oscillator completes one full cycle per bar. At 1/4, it completes four cycles per bar (quarter-note rate). At 4/1, it takes four bars to complete one cycle.

---

#### 16 — Motion LFO

| Parameter | Label | Function |
|-----------|-------|----------|
| Time | Division | Musical time division (same ten divisions as Sync LFO). |
| Space | Depth | Output amplitude. |
| Slope | Wave | Waveshape select (eight shapes). |

**Per-line**: No

A transport-locked LFO that reads the transport phase directly rather than maintaining its own oscillator. The distinction from Sync LFO matters: Sync LFO *runs at the same speed* as the transport but can drift slightly over time because it maintains an independent accumulator. Motion LFO reads the transport's own phase counter, so it is perfectly phase-locked — zero drift, zero jitter. If you stop and restart the transport, Motion LFO snaps to the exact same position in the waveform every time.

Use Motion LFO when you need modulation that is tightly synchronized to a master clock or sequencer. Use Sync LFO when you want tempo-related motion that is allowed to free-run when the transport stops.

---

#### 23 — Pulse Width

| Parameter | Label | Function |
|-----------|-------|----------|
| Time | Rate | Oscillator period (same logarithmic-squared rate curve as Free LFO, 50 ms–20 s). |
| Space | Depth | Output amplitude (bipolar, centered around half-depth). |
| Slope | Width | Duty cycle. Fully counter-clockwise = 0% (always low). Center = 50% (symmetric square wave). Fully clockwise = 100% (always high). |

**Per-line**: No

A variable-duty-cycle oscillator. Where a standard square wave spends equal time high and low, Pulse Width lets you skew the ratio. At 50% duty, this produces a standard square wave. As you move toward 0% or 100%, the "on" portion shrinks to a brief pulse or stretches to nearly continuous. The output is bipolar around the midpoint of the depth range, so it swings above and below the center value.

Pulse Width is useful for rhythmic gating effects where you want control over how long the "on" portion lasts relative to the cycle — something the square waveshape in Free LFO cannot do.

---

#### 28 — Wavefolder

| Parameter | Label | Function |
|-----------|-------|----------|
| Time | Rate | Oscillator period (logarithmic-squared, 50 ms–20 s). |
| Space | Folds | Fold count. Fully counter-clockwise = no folding (clean sine wave). Fully clockwise = 8 folds. |
| Slope | Symmetry | Fold center offset. Center = symmetric folding. Counter-clockwise or clockwise shifts the fold center, producing asymmetric waveforms. |

**Per-line**: No

An internal sine oscillator whose output is passed through a nonlinear wavefolder. Wavefolding works by amplifying the signal until it exceeds the normal output range, then reflecting ("folding") the excess back inward — like folding a piece of paper. One fold turns a sine wave into a shape with two peaks per cycle. Two folds produce four peaks. Eight folds produce a dense, complex waveform with sixteen zero-crossings per cycle from a single underlying sine.

The Symmetry control shifts where the fold boundary sits. At center, the folding is symmetric around the midpoint and the waveform is balanced. Offsetting the symmetry makes one half of each fold wider than the other, producing asymmetric harmonics.

Wavefolder is the go-to operator when you want complex, harmonically rich modulation from a single oscillator. At low fold counts, the output retains the smooth character of a sine wave with gentle distortion. At high fold counts, it becomes a dense, textured waveform that sits between periodic and chaotic.

---

### External Input

These operators read external signals — CV (control voltage) from analog inputs or audio from the same inputs at higher bandwidth. They turn Videomancer's ADC inputs into modulation sources.

---

#### 3 — CV Input

| Parameter | Label | Function |
|-----------|-------|----------|
| Time | Slew | Smoothing rate. Fully counter-clockwise = instant response (no filtering). Fully clockwise = very slow response (heavy lowpass). |
| Space | Gain | Output amplitude, 4× range. Center (~25%) = unity gain. Maximum = 4× amplification. |
| Slope | Channel | Input channel select. Six options across the knob range: channels 1–4 individually, or mixed pairs (ch1+2, ch3+4). |

**Per-line**: Yes

Reads a control voltage from one of Videomancer's analog inputs. The signal passes through a first-order lowpass slew filter to remove noise or to intentionally smooth fast-moving inputs into slower gestures. The 4× gain range lets you amplify small input signals to fill the full modulation range.

In per-line mode, each scanline reads its own ADC sample, so the modulation varies spatially across the frame — different parts of the image see different modulation values depending on the input signal at that moment in the scan.

---

#### 4 — Audio Input

| Parameter | Label | Function |
|-----------|-------|----------|
| Time | Slew | *(Minimal effect — audio mode bypasses slew filtering)* |
| Space | Gain | Output amplitude, 4× range. |
| Slope | Channel | Input channel select (same six options as CV Input). |

**Per-line**: Yes

Identical to CV Input but with no slew filtering, so the raw ADC signal passes through at full bandwidth. Use this when the input is an audio-rate signal and you want the modulation to follow every cycle of the waveform rather than tracking just the envelope. The per-line variant is particularly useful here — it maps the instantaneous audio waveform onto the vertical dimension of the video frame.

---

#### 21 — Ring Mod

| Parameter | Label | Function |
|-----------|-------|----------|
| Time | Slew | Output smoothing (0 = instant, 1023 = slowest). |
| Space | Gain | Output amplitude. |
| Slope | Channel | Channel pair. Lower half of the knob = ch1 × ch2. Upper half = ch3 × ch4. |

**Per-line**: Yes

Multiplies two ADC input channels together, centered around the midpoint. In signal processing terms, this is **ring modulation** (or balanced modulation) — the output contains the sum and difference frequencies of the two inputs but neither input appears on its own. If both inputs are simple waveforms, the output contains new frequencies not present in either input.

The per-line variant multiplies the two channels at each scanline independently, creating spatially varying modulation patterns driven by the interaction of two external signals.

---

### Envelopes & Followers

These operators track the amplitude or threshold crossings of external signals. They convert dynamic input signals into smooth control signals.

---

#### 6 — Envelope

| Parameter | Label | Function |
|-----------|-------|----------|
| Time | Attack | Attack rate. Fully counter-clockwise = instant (tracks peaks immediately). Fully clockwise = very slow (output rises gradually toward new peaks). |
| Space | Release | Release rate. Fully counter-clockwise = instant (drops immediately when input falls). Fully clockwise = very slow (output holds peaks and decays gradually). |
| Slope | Channel | ADC channel select. |

**Per-line**: No

An envelope follower that tracks the amplitude of an ADC input signal. The input is rectified (absolute value around the midpoint), then processed through a peak detector with independent attack and release rates. When the input exceeds the current output, the output rises at the attack rate. When the input falls below the current output, the output decays at the release rate.

Fast attack and slow release produce a classic "peak hold" envelope that captures transients and releases slowly — ideal for making a parameter respond to the loudness of audio input. Fast attack and fast release produce a signal that closely tracks the input waveform's amplitude.

---

#### 7 — Sample & Hold

| Parameter | Label | Function |
|-----------|-------|----------|
| Time | Rate | Clock period (logarithmic-squared, 50 ms–20 s). |
| Space | Gain | Output amplitude. |
| Slope | Channel | ADC channel select. |

**Per-line**: No

A classic sample-and-hold circuit. An internal clock runs freely at the rate set by Time. On each clock tick, a new sample is captured from the selected ADC input channel, and that value is held constant until the next tick. The result is a staircase waveform — a series of flat plateaus at random-seeming levels determined by whatever the input signal happened to be at each sample moment.

Sample & Hold is one of the fundamental building blocks of analog synthesizer modulation. It turns a continuous signal into discrete steps, creating unpredictable but input-correlated patterns.

---

#### 8 — Trigger Env

| Parameter | Label | Function |
|-----------|-------|----------|
| Time | Attack | Attack rate (0 = instant, 1023 = slowest). |
| Space | Release | Release rate (0 = instant, 1023 = slowest). |
| Slope | Curve | Envelope shape. Three curves across the knob range: linear, exponential, and logarithmic. |

**Per-line**: No

A MIDI-triggered attack/release envelope. When a MIDI note-on message arrives, the output ramps from zero to maximum at the attack rate. When a note-off arrives, it ramps back to zero at the release rate. Three curve shapes control the contour of the ramp: linear (constant rate), exponential (starts fast, decelerates), and logarithmic (starts slow, accelerates).

This is the operator to use when you want a parameter to respond to MIDI keyboard or sequencer events — press a key and the parameter sweeps up, release it and it sweeps back down.

---

#### 10 — FFT Band

| Parameter | Label | Function |
|-----------|-------|----------|
| Time | Slew | Envelope smoothing (0 = instant, 1023 = slowest). |
| Space | Gain | Output amplitude. |
| Slope | Band | Octave band select. Eight bands from sub-bass (~60 Hz) to treble (~8 kHz), evenly spaced across the knob. |

**Per-line**: No

Extracts frequency-band energy from the audio input using a Haar wavelet decomposition. The ADC field buffer (channel 1) is analyzed to isolate the energy in one of eight octave bands. The raw energy value is smoothed by an envelope follower.

This turns Videomancer into an audio-reactive system — different FPGA parameters can respond to different frequency ranges of the input audio. Assign the bass band to one modulator, the treble band to another, and each parameter moves independently in response to the music.

---

#### 18 — Comparator

| Parameter | Label | Function |
|-----------|-------|----------|
| Time | Thresh | Comparison threshold (0–1023). |
| Space | Gain | Output amplitude. |
| Slope | Channel | ADC channel select. |

**Per-line**: Yes

A threshold comparator. The ADC input is compared against the threshold value set by Time. When the input is at or above the threshold, the output is maximum (1023). When below, the output is zero. There is no smoothing, no hysteresis — just a hard binary decision based on voltage level.

In per-line mode, the comparison happens independently at each scanline, so the output creates a spatial pattern: parts of the frame where the input signal exceeds the threshold are "on," and parts where it falls below are "off." This is essentially a real-time luminance key applied to the modulation signal.

---

#### 26 — Slew Limiter

| Parameter | Label | Function |
|-----------|-------|----------|
| Time | Rise | Maximum rise rate. Fully counter-clockwise = frozen (cannot rise). Fully clockwise = instant (follows input upward immediately). |
| Space | Gain | Output amplitude. |
| Slope | Fall | Maximum fall rate. Same scale as Rise but applied to downward movement. |

**Per-line**: No

A rate-limited follower of an ADC input signal. The output tracks the input, but the maximum speed at which it can move upward (rise) and downward (fall) is independently limited. If the input jumps instantly from low to high, the output ramps up at the rise rate. If the input drops, the output ramps down at the fall rate.

Asymmetric slew rates produce distinctive motion profiles. Fast rise and slow fall creates a signal that snaps to peaks and gently decays — useful for making parameters respond quickly to transients but recover slowly. Slow rise and fast fall creates the opposite: sluggish response to increasing input but instant response to decreasing input.

---

#### 24 — Peak Hold

| Parameter | Label | Function |
|-----------|-------|----------|
| Time | Decay | Decay rate. Fully counter-clockwise = instant decay (output tracks input directly). Fully clockwise = infinite hold (peaks are captured and never decay). |
| Space | Gain | Output amplitude. |
| Slope | Channel | ADC channel select. |

**Per-line**: Yes

A peak detector with configurable hold time. New peaks in the ADC input are captured instantly — the output jumps to match. Between peaks, the output decays toward zero at the rate set by Decay. At maximum decay, the output simply follows the input. At minimum decay, peaks are held indefinitely, creating a ratchet effect where the output can only go up.

The per-line variant outputs the *maximum* of the held peak and the current scanline's ADC value, so per-line variation from the input signal is preserved while the held peak provides a floor.

---

#### 25 — Field Accum

| Parameter | Label | Function |
|-----------|-------|----------|
| Time | Rate | Integration rate. Controls how much of the ADC signal is added per field (1/64 at minimum, 1/1 at maximum). |
| Space | Gain | Output amplitude. |
| Slope | Leak | Drain rate. Fully counter-clockwise = no leak (pure integrator, value latches). Fully clockwise = fast drain (accumulator returns to center quickly). |

**Per-line**: No

An integrator — it continuously adds the ADC input (minus the midpoint) to a running accumulator. Over time, the accumulator drifts upward if the input is above center, or downward if below. The Leak parameter applies a constant drain that pulls the accumulator back toward center, preventing it from railing at the extremes.

With no leak and a steady input, Field Accum ramps steadily in one direction until it hits the rail — useful for generating slow ramps locked to an input signal. With moderate leak, it produces a smoothed, sluggishly-responding version of the input. With high leak, the output tracks the input loosely, acting as a weighted running average.

---

#### 31 — Quantizer

| Parameter | Label | Function |
|-----------|-------|----------|
| Time | Levels | Number of quantization levels (2 at minimum, 32 at maximum). |
| Space | Gain | Output amplitude. |
| Slope | Channel | ADC channel select. |

**Per-line**: Yes

Snaps the ADC input to one of N evenly-spaced levels, producing a staircase output. The continuous input range (0–1023) is divided into N equal bins, and every input value within a bin is mapped to that bin's center value.

At 2 levels, the output is binary — effectively a comparator at the midpoint. At 32 levels, the output is a fine staircase that closely tracks the input but with visible quantization steps. The creative sweet spot is often between 4 and 12 levels, where the staircase structure is clearly visible in the modulated parameter.

Quantizer is the only mode in this group with per-line rendering. Each scanline is quantized independently, so the staircase pattern applies spatially — a smooth gradient in the input becomes a series of discrete spatial bands in the output.

---

### Random & Chaos

These operators produce non-repeating or quasi-periodic patterns. They range from smooth noise to mathematical chaos.

---

#### 5 — Random

| Parameter | Label | Function |
|-----------|-------|----------|
| Time | Rise | Rise slew rate (0 = instant, 1023 = slowest). |
| Space | Gain | Output amplitude. |
| Slope | Fall | Fall slew rate (0 = instant, 1023 = slowest). |

**Per-line**: No

Generates a new random 10-bit target value every video field and slews toward it. The slew has independent rise and fall rates — the output moves toward new targets that are above it at the rise rate, and toward targets below it at the fall rate.

With both slew rates at zero (instant), the output jumps to a new random value every field — pure sample-and-hold noise at the field rate. With moderate slew, the output wanders smoothly between random targets. With high slew, the output becomes a slow, lazy random drift.

---

#### 20 — Drift

| Parameter | Label | Function |
|-----------|-------|----------|
| Time | Rate | Step size / volatility. Fully counter-clockwise = static (no movement). Fully clockwise = ±32 per frame. |
| Space | Gain | Output amplitude. |
| Slope | Range | Centering pull. Fully counter-clockwise = free walk (no centering). Fully clockwise = tight centering (output stays near middle). |

**Per-line**: No

Brownian random walk. Each frame, a small random step is added to the current position. A configurable centering force gently pulls the value back toward the midpoint, preventing it from permanently drifting to one extreme.

Drift produces motion that feels organic and aimless — like a leaf blowing in the wind. Unlike Random (which jumps to brand-new targets), Drift moves by small increments from wherever it currently is, so the output is always locally smooth even though its long-term trajectory is unpredictable. The centering force determines whether the walk is bounded (with centering) or truly free-roaming (without).

---

#### 27 — Perlin Noise

| Parameter | Label | Function |
|-----------|-------|----------|
| Time | Speed | Evolution rate. Controls how quickly the noise pattern evolves (16 increments/frame at minimum, 4096 at maximum). |
| Space | Gain | Output amplitude. |
| Slope | Detail | Octave count. Fully counter-clockwise = 1 octave (smooth, gentle undulation). Fully clockwise = 4 octaves (rough, detailed texture). |

**Per-line**: No

Smooth, coherent noise inspired by Perlin noise. Unlike Random (which jumps between uncorrelated values) or Drift (which wanders by small steps), Perlin Noise interpolates smoothly between random lattice points using a smoothstep function ($3t^2 - 2t^3$), producing motion that is continuous and has no visible "steps" or "jumps."

The Detail parameter adds octave layering — additional noise at higher frequencies is summed with the base noise, creating progressively more complex texture. At one octave, the output is a gentle, wide undulation. At four octaves, it has both slow macro-movement and fast micro-variation, much like natural phenomena such as clouds, terrain, or water surfaces.

---

#### 12 — Turing Machine

| Parameter | Label | Function |
|-----------|-------|----------|
| Time | Rate | Clock period (logarithmic-squared, 50 ms–20 s). |
| Space | Gain | Output amplitude. |
| Slope | Mutate | Mutation probability. Fully counter-clockwise = locked (pure LFSR, perfectly repeating cycle). Center = 50% (every other bit is mutated). Fully clockwise = fully random (no pattern memory). |

**Per-line**: No

A shift-register sequencer inspired by the "Turing Machine" module from modular synthesis. An 8-bit register shifts one position per clock tick. The new bit entering the register is either a deterministic XOR feedback (creating a repeating pseudo-random sequence) or a truly random bit — the Mutate parameter controls the probability of mutation.

At zero mutation, the register cycles through a fixed 255-step pattern that repeats identically forever. At full mutation, every bit is random and the output is pure noise. The creative territory is in between: low mutation produces long sequences that occasionally vary. Moderate mutation creates patterns that evolve gradually — recognizable motifs that drift and transform over time.

---

#### 14 — Logistic Map

| Parameter | Label | Function |
|-----------|-------|----------|
| Time | Rate | Iteration clock (logarithmic-squared, 50 ms–20 s). |
| Space | Gain | Output amplitude. |
| Slope | Chaos | Bifurcation parameter *r*. Fully counter-clockwise = 2.8 (stable fixed point). Center ≈ 3.4 (period doubling). Fully clockwise = 4.0 (full chaos). |

**Per-line**: No

Iterates the logistic map equation: $x_{n+1} = r \cdot x_n \cdot (1 - x_n)$. This is one of the simplest mathematical systems that produces genuine chaotic behavior. The Chaos parameter controls the bifurcation parameter *r*, which determines whether the system converges to a fixed point, oscillates between periodic values, or exhibits deterministic chaos.

Sweeping Chaos from low to high takes you through the classic bifurcation diagram: at *r* = 2.8 the output settles to a single stable value. Around *r* = 3.0 it begins alternating between two values (period-2). By *r* = 3.5 it cycles through four values (period-4). Near *r* = 3.57 the period-doubling cascade reaches infinity and the system becomes chaotic — the output never repeats. At *r* = 4.0, full mathematical chaos: the output looks random but is entirely deterministic.

---

#### 22 — Cellular

| Parameter | Label | Function |
|-----------|-------|----------|
| Time | Rate | Generation clock (logarithmic-squared, 50 ms–20 s). |
| Space | Gain | Output amplitude. |
| Slope | Rule | Automaton rule select. Four elementary cellular automaton rules across the knob: Rule 30 (chaotic), Rule 90 (fractal/Sierpinski), Rule 110 (Turing-complete), Rule 150 (symmetric complex). |

**Per-line**: No

A one-dimensional cellular automaton with 33 cells and wrap-around boundaries. Each generation, every cell's next state is determined by its current state and the states of its two neighbors, according to the selected rule. The output is the sum of the center eight cells, scaled to 0–1023.

Stephen Wolfram's elementary cellular automata demonstrate how extremely simple rules can produce complex, structured behavior. Rule 30 produces seemingly random output from ordered initial conditions — it was used as a random number generator in Mathematica. Rule 90 produces self-similar fractal patterns (the Sierpinski triangle). Rule 110 is proven to be Turing-complete, meaning it can compute anything. Rule 150 produces complex symmetric structures.

The automaton re-seeds when you change rules (only the center cell starts active), so switching rules initiates a fresh evolution from a known starting condition.

---

### Sequencing & Rhythm

These operators produce structured, repeating patterns — step sequences, rhythmic gates, and clock-derived signals.

---

#### 9 — Step Seq

| Parameter | Label | Function |
|-----------|-------|----------|
| Time | Rate | Clock period (logarithmic-squared, 50 ms–20 s). |
| Space | Depth | Output amplitude. |
| Slope | Pattern | Pattern select. Eight preset patterns across the knob: pulse, ramp up, ramp down, triangle, alternating, staircase, spike, and random-latch. |

**Per-line**: No

An 8-step sequencer clocked by a free-running accumulator. Each clock tick advances to the next step. Each pattern defines eight fixed output levels that the sequencer cycles through.

The patterns cover common modulation shapes: Pulse produces a single high step followed by seven low steps (a 1/8 duty-cycle gate). Ramp Up and Ramp Down produce ascending and descending staircases. Triangle goes up and back down. Alternating flips between two levels. Staircase has four levels, each held for two steps. Spike is a single-sample impulse. Random-Latch latches a new random value at each step, producing an 8-step random sequence that changes every cycle.

---

#### 15 — Euclidean Rhythm

| Parameter | Label | Function |
|-----------|-------|----------|
| Time | Rate | Clock period (logarithmic-squared, 50 ms–20 s). |
| Space | Gain | Output amplitude. |
| Slope | Density | Pulse count. Fully counter-clockwise = 0 pulses (silent). Fully clockwise = 16 pulses (all steps active). |

**Per-line**: No

Generates Euclidean rhythms — patterns where a given number of pulses are distributed as evenly as possible across 16 steps. The algorithm (equivalent to Bjorklund's) produces the same patterns found in many world music traditions: 3 pulses in 8 steps gives the Cuban tresillo, 5 in 8 gives the "standard" West African rhythm, 7 in 12 approximates a West African bell pattern.

The output is binary per step (high or low), making this operator ideal for boolean modulation of toggle switches. In linear mode, the output alternates between zero and full scale in the Euclidean pattern.

---

#### 29 — Clock Div

| Parameter | Label | Function |
|-----------|-------|----------|
| Time | Division | Division ratio. Fully counter-clockwise = ÷1 (follows transport directly). Fully clockwise = ÷16. |
| Space | Gain | Output amplitude. |
| Slope | Duty | Gate duty cycle. Fully counter-clockwise = shortest possible pulse. Center = 50% (symmetric square). Fully clockwise = nearly 100% (gate stays open almost the entire divided period). |

**Per-line**: No

An integer clock divider that divides the motion transport phase by a ratio from 1 to 16. The output is a square-wave gate at the divided rate, with a controllable duty cycle. At ÷1, the output toggles at the base transport rate. At ÷4, it toggles at one quarter the rate. At ÷16, it produces one gate cycle for every 16 transport cycles.

Clock Div is the rhythmic complement to Motion LFO. Where Motion LFO produces continuously varying waveforms locked to the transport, Clock Div produces clean, hard-edged gates at related tempos. The Duty parameter controls the gate shape — making it useful for creating rhythmic on/off patterns with precise timing relative to the master clock.

---

#### 30 — Prob Gate

| Parameter | Label | Function |
|-----------|-------|----------|
| Time | Rate | Gate period (logarithmic-squared, 50 ms–20 s). |
| Space | Prob | Probability of the gate being "high" on any given period (0% = never, 50% = half the time, 100% = always). |
| Slope | Length | Gate length within the period. Controls what fraction of the period the gate stays open when it fires. |

**Per-line**: No

A probabilistic binary gate. At each period boundary, a random coin flip determines whether the gate will be high or low for the upcoming period. The Prob parameter sets the probability: at 0%, the gate never opens. At 100%, it always opens. At 50%, it opens roughly half the time. The Length parameter controls how long the gate stays open within each period — at full length, the gate fills the entire period; at short length, it produces a brief pulse near the start.

Prob Gate is designed for generative composition — it produces rhythmic on/off patterns that are statistically predictable but not deterministically repeating. Two Prob Gates with different rates and probabilities, assigned to different parameters, create complex polyrhythmic textures that never exactly repeat.

---

### Spatial

These operators produce values that vary across the video frame rather than (or in addition to) varying over time. They are the modulation equivalent of gradients and patterns.

---

#### 11 — H Displace

| Parameter | Label | Function |
|-----------|-------|----------|
| Time | Freq | Spatial frequency. Controls how many waveform cycles appear across the frame height (0.5–16 cycles). |
| Space | Depth | Output amplitude. |
| Slope | Wave | Waveshape select (eight shapes). |

**Per-line**: Yes

Generates a per-line spatial waveform across the frame height with a slow auto-scrolling phase drift (~0.25 Hz). Each scanline gets a different modulation value based on its vertical position in the frame, creating a spatial pattern that slowly drifts over time.

At one cycle per frame, the output is a single waveform period from top to bottom. At higher frequencies, multiple cycles appear, creating horizontal bands of varying modulation intensity. The slow auto-scroll means the pattern constantly shifts position, creating a gentle animation even with a static input.

---

#### 17 — V Gradient

| Parameter | Label | Function |
|-----------|-------|----------|
| Time | Freq | Spatial frequency (0.5–16 cycles per frame). |
| Space | Depth | Output amplitude. |
| Slope | Wave | Waveshape select (eight shapes). |

**Per-line**: Yes

A static vertical gradient — identical to H Displace but without the auto-scrolling phase drift. The waveform is fixed in position, so each scanline always receives the same modulation value. This produces a pure spatial modulation pattern: the parameter varies from the top of the frame to the bottom according to the selected waveshape but does not change from frame to frame.

Use V Gradient when you want a parameter to have a fixed spatial profile — for example, making the bottom of the frame brighter than the top, or applying a different effect intensity at different vertical positions. Use H Displace when you want the same kind of spatial variation but with slow temporal animation.

---

### Physics

These operators simulate physical systems. They produce the kinds of motion that arise from natural forces — gravity, springs, friction, damping.

---

#### 13 — Bouncing Ball

| Parameter | Label | Function |
|-----------|-------|----------|
| Time | Gravity | Gravitational acceleration. Fully counter-clockwise = weak gravity (floaty, slow falls). Fully clockwise = strong gravity (fast, violent bounces). |
| Space | Gain | Output amplitude. |
| Slope | Bounce | Elasticity / restitution coefficient. Fully counter-clockwise = no bounce (ball sticks to floor). Fully clockwise ≈ 100% restitution (ball bounces back to nearly its original height). |

**Per-line**: No

Simulates a ball bouncing on a floor. The ball starts at the top, accelerates downward under gravity, hits the floor, and bounces back up with velocity multiplied by the restitution coefficient. Each bounce is lower than the last (unless restitution is near 100%). When the ball comes to rest, it auto-retriggers after approximately half a second, starting a new drop.

A MIDI note-on resets the ball to the ceiling, triggering a fresh drop. This makes Bouncing Ball useful as a MIDI-triggered decay effect — press a key and the parameter bounces rapidly at first, then settles to a resting value.

---

#### 19 — Pendulum

| Parameter | Label | Function |
|-----------|-------|----------|
| Time | Length | Pendulum period. Fully counter-clockwise = short pendulum (fast swings). Fully clockwise = long pendulum (slow swings). |
| Space | Gain | Output amplitude. |
| Slope | Damp | Damping coefficient. Fully counter-clockwise = undamped (oscillates forever). Fully clockwise = heavy damping (oscillation dies out quickly). |

**Per-line**: No

Simulates a damped pendulum — a weight on a string swinging back and forth. A restoring force proportional to displacement from center pulls the pendulum back when it swings to one side. Damping gradually reduces the swing amplitude. The result is a decaying sinusoidal oscillation that feels natural and organic — the kind of motion you see when you push a swing and let it settle.

A MIDI note-on displaces the pendulum to its maximum angle, triggering a new decay. Without MIDI, the pendulum swings from its initial displacement and either oscillates indefinitely (no damping) or settles to center (with damping).

The difference between Pendulum and a damped Free LFO is physical accuracy: Pendulum's frequency changes slightly with amplitude (a real pendulum swings faster at small angles), and its decay envelope follows the physics of friction rather than an arbitrary exponential curve.

---

## Per-Line Rendering

Eight of the 32 operators produce per-scanline varying output. This means the modulation value changes for every horizontal line of the video frame, not just once per field. Per-line rendering enables spatial modulation effects that would be impossible with field-rate updates alone.

| Mode | Per-line function | What varies per line |
|------|-------------------|---------------------|
| **CV Input** | Reads ADC at each scanline | Input voltage at that moment in the scan |
| **Audio Input** | Reads ADC at each scanline | Audio waveform mapped to vertical position |
| **H Displace** | Evaluates waveform at line position | Spatial wave pattern with slow drift |
| **V Gradient** | Evaluates waveform at line position | Static spatial wave pattern |
| **Comparator** | Compares ADC at each scanline | Binary threshold map across frame |
| **Ring Mod** | Multiplies two ADC channels per line | Product of two input signals, spatially varying |
| **Peak Hold** | max(held peak, per-line ADC) | Spatial floor at the held peak value |
| **Quantizer** | Quantizes ADC at each scanline | Staircase-quantized spatial pattern |

When a per-line operator is active, the FPGA register for that parameter is updated once per scanline during active video, rather than once per field. This means FPGA programs that read the parameter will see it change from line to line — the top of the frame may have a different value than the bottom.

---

## Guided Exercises

These exercises progress from basic oscillator modulation through external input processing to generative composition. Each builds on concepts from the previous exercise.

### Exercise 1: First Movement

**Objective**: Understand what modulation does by watching a single LFO move a single parameter.

1. Load any FPGA program with a clearly visible effect on Knob 1 (Bitcullis's Hori Decimate or Lumarian's Contrast work well).
2. Set a modulator to **Free LFO**. Set Rate to about 40% (a few seconds per cycle). Set Depth to maximum. Set Wave to triangle.
3. Watch the FPGA program's parameter sweep smoothly back and forth. The knob position sets the center of the sweep; depth controls how far it swings.
4. Slowly decrease Depth. The sweep narrows. At zero, the modulation disappears.
5. Change Wave from triangle to square. The parameter now snaps between two values instead of sweeping.
6. Try each waveshape. Notice how each produces a different *feel* of motion from the same rate and depth settings.

**Key concepts**: Rate controls speed, Depth controls swing range, Wave controls the shape of the motion.

---

### Exercise 2: Audio-Reactive Modulation

**Objective**: Use an external audio signal to drive parameter changes.

1. Connect an audio source to Videomancer's CV input 1.
2. Set a modulator to **FFT Band**. Set Band to about 30% (low-mid frequencies — bass drum territory). Set Gain to maximum. Set Slew to about 30% for gentle smoothing.
3. Play music with a strong bass line. Watch the modulated parameter pulse in time with the kick drum.
4. Now set a second modulator to FFT Band on a different parameter. Set Band to 80% (high frequencies — hi-hats and cymbals). The two parameters now respond to different parts of the frequency spectrum independently.
5. Switch the first modulator to **Envelope** mode. Set Attack to about 20% and Release to 60%. Compare how the envelope follower tracks the audio versus the FFT band — the envelope responds to overall loudness, while FFT Band responds to energy in a specific frequency range.

**Key concepts**: FFT Band isolates frequency ranges, Envelope tracks overall amplitude, multiple modulators on different parameters create multi-dimensional audio reactivity.

---

### Exercise 3: Generative Rhythms

**Objective**: Combine pattern generators for evolving, non-repeating modulation.

1. Set the global BPM to 120 (or connect a MIDI clock).
2. Set modulator P1 to **Euclidean Rhythm**. Rate at about 50% (moderate tempo). Density at about 40% (5–6 pulses in 16 steps). This creates a rhythmic gate pattern.
3. Set modulator P2 to **Prob Gate**. Rate at about 60%. Prob at 50%. Length at about 40%. This creates a second rhythmic pattern that is similar in rate but randomly varies from cycle to cycle.
4. Set modulator P3 to **Turing Machine**. Rate matching the others. Gain at maximum. Mutate at about 20%. This adds a quasi-periodic melodic contour that slowly evolves.
5. Let all three run. The Euclidean rhythm provides a steady structural pulse. The Prob Gate adds unpredictable variation. The Turing Machine creates slowly evolving melodic movement. Together, they produce modulation that has rhythmic structure but never exactly repeats.
6. Slowly increase the Turing Machine's Mutate parameter. Watch the melodic pattern dissolve from structured repetition into randomness.

**Key concepts**: Layering different generator types creates complexity, deterministic patterns provide structure, probabilistic elements prevent exact repetition.

---

### Exercise 4: Physics and Chaos

**Objective**: Explore how physics simulations and mathematical chaos differ from traditional oscillators.

1. Set a modulator to **Bouncing Ball**. Gravity at about 50%, Bounce at about 80%.
2. If MIDI is connected, press a key. The ball drops, bounces, and settles. Each key press restarts the drop.
3. Now switch to **Pendulum**. Length at 50%, Damp at about 30%. The parameter swings back and forth, gradually settling to center.
4. Switch to **Logistic Map**. Rate at about 40%. Start with Chaos fully counter-clockwise (stable). Slowly turn Chaos clockwise. Watch the output transition from a steady value, to alternating between two values, to four values, and finally to unpredictable chaos.
5. Switch to **Cellular** (Rule 30). Set Rate to about 30% so you can see individual generations. Watch the apparently random output emerge from a simple three-neighbor rule.
6. Change to Rule 90. Notice the more structured, self-similar pattern.

**Key concepts**: Physics simulations produce natural-feeling decay and oscillation, chaos systems produce deterministic but unpredictable output, the transition from order to chaos is continuous and controllable.

---

## Tips

- **Start with Free LFO**. It is the simplest operator and the best way to learn what a modulator does to any given FPGA parameter. Once you understand the effect, switch to more complex operators.
- **Boolean mode for toggles**. When modulating a toggle switch, the modulator outputs 0 or 1. Any operator that produces values crossing the 512 midpoint will create rhythmic toggling — a triangle LFO becomes an alternating on/off pattern.
- **Layer slow and fast**. Combine a slow modulator (Drift or Perlin Noise at low speed) with a fast one (Free LFO or Euclidean Rhythm). The slow operator creates gradual evolution while the fast one adds rhythmic detail.
- **Motion LFO vs. Sync LFO**. Use Motion LFO when you need perfect phase lock to the transport. Use Sync LFO when you want tempo-related motion that can free-run when the transport is stopped.
- **Depth is your friend**. If a modulated effect is too dramatic, reduce Depth before changing anything else. Most operators produce useful results across their full parameter range — the issue is usually amplitude, not the operator itself.
- **Per-line modes for spatial effects**. Any of the eight per-line operators can create spatial variation across the frame. CV Input with a ramp or triangle wave on the input produces a clean vertical gradient controlled by the external signal.
- **MIDI triggers**. Trigger Env, Bouncing Ball, and Pendulum all respond to MIDI note messages. Connect a keyboard or sequencer to create musically timed one-shot events.
- **Chaos is a spectrum**. Logistic Map's Chaos parameter and Turing Machine's Mutate parameter both control the balance between order and randomness. The most interesting territory is usually in the middle — not fully ordered, not fully random.
- **Combine pattern generators**. Euclidean Rhythm + Prob Gate + Clock Div on three different parameters creates interlocking rhythmic modulation with a mix of deterministic structure and probabilistic variation.
- **Wavefolder for complex LFO shapes**. If the eight basic waveshapes are not enough, Wavefolder produces complex waveforms from a single sine oscillator. Start with one or two folds and sweep Symmetry to find new shapes.
- **Quantizer for stepped spatial effects**. Quantizer with a low level count on a CV input creates visible banding in per-line mode — the frame is divided into discrete horizontal zones.
