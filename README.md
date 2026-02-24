# Mock-Processor-Concurrency-Simulator

A Python simulator of a mock processor pipeline that models concurrent stage behavior in a single-threaded, tick-based execution flow.

## Project Overview

This project simulates how instruction-processing stages can operate with concurrency-like behavior without using multithreading. It advances instruction tokens across pipeline stages each cycle, enforcing timing and readiness rules to mimic coordinated processor execution.

## Technical Highlights

- Implemented a multi-stage mock processor pipeline using place/transition modeling
- Simulated concurrency in a single thread through ordered, tick-based stage execution
- Added token timing control (`arrival_tick`) to enforce safe cross-stage synchronization
- Implemented decode/read, issue routing, ALU, address generation, load, and write-back transitions
- Modeled arithmetic/logic flow and load-address flow as separate coordinated paths
- Added deterministic simulation-state snapshots written to `simulation.txt`

## Pipeline Model

### Places

- `INM`: instruction memory queue
- `INB`: decoded instruction buffer
- `AIB`: arithmetic instruction buffer
- `LIB`: load instruction buffer
- `ADB`: address buffer
- `REB`: result buffer
- `RGF`: register file
- `DAM`: data memory

### Supported Instruction Behavior

- Arithmetic/logic path: `ADD`, `SUB`, `AND`, `OR`
- Load path: `LD` with effective address calculation and memory read
- Write-back path updates register state through `REB -> RGF`

### Transition Flow

- `DECODE`: pulls instruction from `INM`, resolves source register values, and pushes to `INB`
- `ISSUE1` / `ISSUE2`: routes instruction from `INB` to arithmetic or load path
- `ALU`: computes arithmetic/logic results into `REB`
- `ADDR`: computes load addresses into `ADB`
- `LOAD`: reads memory using computed address and emits load result into `REB`
- `WRITE`: commits result tokens from `REB` into `RGF`

## Output Artifacts

- `simulation.txt`: per-cycle snapshots of all pipeline components
- Console debug report: transition execution and executability trace details

## Core Files

- `Psim.py`: simulation driver, cycle loop, component printing, and termination logic
- `places.py`: token model, place abstractions, memory/register storage behavior, and execution gating
- `transitions.py`: transition operations for decode/issue/execute/load/write flow
- `instructions.txt`: instruction stream input
- `registers.txt`: initial register state input
- `datamemory.txt`: initial data memory input

## Lessons Learned

- **Single-thread concurrency modeling:** representing concurrent behavior through cycle-coordinated stage progression
- **Synchronization by timing:** using token arrival ticks to prevent invalid same-cycle execution dependencies
- **Pipeline decomposition:** separating decode, route, execute, load, and write-back into maintainable stage logic
- **Stateful simulation design:** managing evolving register/memory/token state across deterministic cycles
- **Dataflow debugging:** validating complex stage interactions through structured logs and step-by-step snapshots
