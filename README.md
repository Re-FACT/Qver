# Quality Design Verification Framework (Qver) for eFPGA

[![Regression Tests](https://github.com/Re-FACT/Qver/actions/workflows/test.yml/badge.svg)](https://github.com/Re-FACT/Qver/actions/workflows/test.yml)
[![Code Format](https://github.com/Re-FACT/Qver/actions/workflows/format.yaml/badge.svg)](https://github.com/Re-FACT/Qver/actions/workflows/format.yaml)

Version: see [`VERSION.md`](VERSION.md)

Qver is a python-based framework to run design verification on eFPGA netlists.
Qver is to solve a fundemental problem: Design verification methodology for eFPGAs is different than ASICs.
eFPGA design verification requires not only netlists (RTL-level, gate-level and post-layout), but also

- Bitstreams and the process to download/inject bitstreams to eFPGA configuration memories.
- Testbenches for designs to be mapped on the eFPGA, including testing vectors 

Qver is the one-stop solution to run design verification for a number of designs on eFPGA and report their status.

Qver is based on the [Cocotb](https://www.cocotb.org/), and hence support most of commercial and open-source simulators

- icarus Verilog
- Synopsys VCS
- Siemens Modelsim
- Cadence Xcelium

## Documentation

Full documentatation can be found [here](https://qver.readthedocs-hosted.com/en/latest//)

## Developer Guidelines

Please read the [contributor_guidelines](https://qver.readthedocs-hosted.com/en/latest/developer/contributor_guidelines/) if you would like to contribute to the project.
