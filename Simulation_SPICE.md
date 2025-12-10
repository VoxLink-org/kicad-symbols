# Library: Simulation_SPICE

## 0
Definition:
```json
{
  "symbol": "0",
  "library": "Simulation_SPICE",
  "ref_prefix": "#GND",
  "description": "0V reference potential for simulation",
  "keywords": "simulation",
  "datasheet": "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#subsec_Circuit_elements__device"
}
```

## BSOURCE
Definition:
```json
{
  "symbol": "BSOURCE",
  "library": "Simulation_SPICE",
  "ref_prefix": "B",
  "description": "Arbitrary behavioral voltage or current source for simulation only",
  "keywords": "simulation dependent",
  "datasheet": "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#sec_Non_linear_Dependent_Sources"
}
```

## D
Definition:
```json
{
  "symbol": "D",
  "library": "Simulation_SPICE",
  "ref_prefix": "D",
  "description": "Diode for simulation or PCB",
  "keywords": "simulation",
  "datasheet": "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#cha_DIODEs"
}
```

## ESOURCE
Definition:
```json
{
  "symbol": "ESOURCE",
  "library": "Simulation_SPICE",
  "ref_prefix": "E",
  "description": "Voltage-controlled voltage source symbol for simulation only",
  "keywords": "simulation vcvs dependent",
  "datasheet": "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#subsec_Exxxx__Linear_Voltage_Controlled"
}
```

## GSOURCE
Definition:
```json
{
  "symbol": "GSOURCE",
  "library": "Simulation_SPICE",
  "ref_prefix": "G",
  "description": "Voltage-controlled current source symbol for simulation only",
  "keywords": "simulation vccs dependent",
  "datasheet": "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#subsec_Gxxxx__Linear_Voltage_Controlled"
}
```

## IAM
Definition:
```json
{
  "symbol": "IAM",
  "library": "Simulation_SPICE",
  "ref_prefix": "I",
  "description": "Current source, AM",
  "keywords": "simulation amplitude modulated",
  "datasheet": "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#sec_Independent_Sources_for"
}
```

## IBIS_DEVICE
Definition:
```json
{
  "symbol": "IBIS_DEVICE",
  "library": "Simulation_SPICE",
  "ref_prefix": "U?",
  "description": "Device model for IBIS files. Pin 3 can be used to monitor the die potential",
  "keywords": "Simulation IBIS",
  "datasheet": "https://ibis.org"
}
```

## IBIS_DEVICE_DIFF
Definition:
```json
{
  "symbol": "IBIS_DEVICE_DIFF",
  "library": "Simulation_SPICE",
  "ref_prefix": "U?",
  "description": "Device model for IBIS files. Pin 3 can be used to monitor the die potential",
  "keywords": "Simulation IBIS",
  "datasheet": "https://ibis.org"
}
```

## IBIS_DRIVER
Definition:
```json
{
  "symbol": "IBIS_DRIVER",
  "library": "Simulation_SPICE",
  "ref_prefix": "U?",
  "description": "Driver model for IBIS files.",
  "keywords": "Simulation IBIS",
  "datasheet": "https://ibis.org"
}
```

## IBIS_DRIVER_DIFF
Definition:
```json
{
  "symbol": "IBIS_DRIVER_DIFF",
  "library": "Simulation_SPICE",
  "ref_prefix": "U?",
  "description": "Driver model for IBIS files. Pin 3 can be used to monitor the die potential.",
  "keywords": "Simulation IBIS",
  "datasheet": "https://ibis.org"
}
```

## IDC
Definition:
```json
{
  "symbol": "IDC",
  "library": "Simulation_SPICE",
  "ref_prefix": "I",
  "description": "Current source, DC",
  "keywords": "simulation",
  "datasheet": "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#sec_Independent_Sources_for"
}
```

## IEXP
Definition:
```json
{
  "symbol": "IEXP",
  "library": "Simulation_SPICE",
  "ref_prefix": "I",
  "description": "Current source, exponential",
  "keywords": "simulation",
  "datasheet": "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#sec_Independent_Sources_for"
}
```

## IPULSE
Definition:
```json
{
  "symbol": "IPULSE",
  "library": "Simulation_SPICE",
  "ref_prefix": "I",
  "description": "Current source, pulse",
  "keywords": "simulation",
  "datasheet": "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#sec_Independent_Sources_for"
}
```

## IPWL
Definition:
```json
{
  "symbol": "IPWL",
  "library": "Simulation_SPICE",
  "ref_prefix": "I",
  "description": "Current source, piece-wise linear",
  "keywords": "simulation",
  "datasheet": "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#sec_Independent_Sources_for"
}
```

## ISFFM
Definition:
```json
{
  "symbol": "ISFFM",
  "library": "Simulation_SPICE",
  "ref_prefix": "I",
  "description": "Current source, single-frequency FM",
  "keywords": "simulation frequency modulated",
  "datasheet": "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#sec_Independent_Sources_for"
}
```

## ISIN
Definition:
```json
{
  "symbol": "ISIN",
  "library": "Simulation_SPICE",
  "ref_prefix": "I",
  "description": "Current source, sinusoidal",
  "keywords": "simulation",
  "datasheet": "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#sec_Independent_Sources_for"
}
```

## ITRNOISE
Definition:
```json
{
  "symbol": "ITRNOISE",
  "library": "Simulation_SPICE",
  "ref_prefix": "I",
  "description": "Current source, transient noise",
  "keywords": "simulation",
  "datasheet": "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#subsec_Transient_noise_source"
}
```

## ITRRANDOM
Definition:
```json
{
  "symbol": "ITRRANDOM",
  "library": "Simulation_SPICE",
  "ref_prefix": "I",
  "description": "Current source, random noise",
  "keywords": "simulation",
  "datasheet": "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#subsec_Random_voltage_source"
}
```

## NJFET
Definition:
```json
{
  "symbol": "NJFET",
  "library": "Simulation_SPICE",
  "ref_prefix": "Q",
  "description": "N-JFET transistor, for simulation only",
  "keywords": "transistor NJFET N-JFET",
  "datasheet": "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#cha_JFETs"
}
```

## NMOS
Definition:
```json
{
  "symbol": "NMOS",
  "library": "Simulation_SPICE",
  "ref_prefix": "Q",
  "description": "N-MOSFET transistor, drain/source/gate",
  "keywords": "transistor NMOS N-MOS N-MOSFET simulation",
  "datasheet": "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#cha_MOSFETs"
}
```

## NMOS_Substrate
Definition:
```json
{
  "symbol": "NMOS_Substrate",
  "library": "Simulation_SPICE",
  "ref_prefix": "Q",
  "description": "N-channel MOSFET symbol with substrate (bulk) pin",
  "keywords": "mosfet nmos simulation",
  "datasheet": "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#cha_MOSFETs"
}
```

## NPN
Definition:
```json
{
  "symbol": "NPN",
  "library": "Simulation_SPICE",
  "ref_prefix": "Q",
  "description": "Bipolar transistor symbol for simulation only, substrate tied to the emitter",
  "keywords": "simulation",
  "datasheet": "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#cha_BJTs"
}
```

## NPN_Substrate
Definition:
```json
{
  "symbol": "NPN_Substrate",
  "library": "Simulation_SPICE",
  "ref_prefix": "Q",
  "description": "Bipolar transistor symbol for simulation only, with substrate pin",
  "keywords": "simulation",
  "datasheet": "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#cha_BJTs"
}
```

## OPAMP
Definition:
```json
{
  "symbol": "OPAMP",
  "library": "Simulation_SPICE",
  "ref_prefix": "U",
  "description": "Operational amplifier, single",
  "keywords": "simulation",
  "datasheet": "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#sec__SUBCKT_Subcircuits"
}
```

## PJFET
Definition:
```json
{
  "symbol": "PJFET",
  "library": "Simulation_SPICE",
  "ref_prefix": "Q",
  "description": "P-JFET transistor, for simulation only",
  "keywords": "transistor PJFET P-JFET",
  "datasheet": "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#cha_JFETs"
}
```

## PMOS
Definition:
```json
{
  "symbol": "PMOS",
  "library": "Simulation_SPICE",
  "ref_prefix": "Q",
  "description": "P-MOSFET transistor, drain/source/gate",
  "keywords": "transistor PMOS P-MOS P-MOSFET simulation",
  "datasheet": "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#cha_MOSFETs"
}
```

## PMOS_Substrate
Definition:
```json
{
  "symbol": "PMOS_Substrate",
  "library": "Simulation_SPICE",
  "ref_prefix": "Q",
  "description": "P-channel MOSFET symbol with substrate (bulk) pin",
  "keywords": "mosfet pmos simulation",
  "datasheet": "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#cha_MOSFETs"
}
```

## PNP
Definition:
```json
{
  "symbol": "PNP",
  "library": "Simulation_SPICE",
  "ref_prefix": "Q",
  "description": "Bipolar transistor symbol for simulation only, substrate tied to the emitter",
  "keywords": "simulation",
  "datasheet": "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#cha_BJTs"
}
```

## PNP_Substrate
Definition:
```json
{
  "symbol": "PNP_Substrate",
  "library": "Simulation_SPICE",
  "ref_prefix": "Q",
  "description": "Bipolar transistor symbol for simulation only, with substrate pin",
  "keywords": "simulation",
  "datasheet": "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#cha_BJTs"
}
```

## SWITCH
Definition:
```json
{
  "symbol": "SWITCH",
  "library": "Simulation_SPICE",
  "ref_prefix": "S",
  "description": "Voltage controlled switch symbol for simulation only",
  "keywords": "simulation",
  "datasheet": "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#subsec_Switches"
}
```

## TLINE
Definition:
```json
{
  "symbol": "TLINE",
  "library": "Simulation_SPICE",
  "ref_prefix": "T",
  "description": "Lossless transmission line, for simulation only",
  "keywords": "lossless transmission line characteristic impedance",
  "datasheet": "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#sec_Lossless_Transmission_Lines"
}
```

## VAM
Definition:
```json
{
  "symbol": "VAM",
  "library": "Simulation_SPICE",
  "ref_prefix": "V",
  "description": "Voltage source, AM",
  "keywords": "simulation amplitude modulated",
  "datasheet": "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#sec_Independent_Sources_for"
}
```

## VDC
Definition:
```json
{
  "symbol": "VDC",
  "library": "Simulation_SPICE",
  "ref_prefix": "V",
  "description": "Voltage source, DC",
  "keywords": "simulation",
  "datasheet": "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#sec_Independent_Sources_for"
}
```

## VEXP
Definition:
```json
{
  "symbol": "VEXP",
  "library": "Simulation_SPICE",
  "ref_prefix": "V",
  "description": "Voltage source, exponential",
  "keywords": "simulation",
  "datasheet": "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#sec_Independent_Sources_for"
}
```

## VOLTMETER_DIFF
Definition:
```json
{
  "symbol": "VOLTMETER_DIFF",
  "library": "Simulation_SPICE",
  "ref_prefix": "MES?",
  "description": "Differential voltmeter for simulation. The sensed differential voltage can be measured on the third terminal as a single-ended voltage",
  "keywords": "voltmeter differential vdiff",
  "datasheet": "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#sec__SUBCKT_Subcircuits"
}
```

## VPULSE
Definition:
```json
{
  "symbol": "VPULSE",
  "library": "Simulation_SPICE",
  "ref_prefix": "V",
  "description": "Voltage source, pulse",
  "keywords": "simulation",
  "datasheet": "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#sec_Independent_Sources_for"
}
```

## VPWL
Definition:
```json
{
  "symbol": "VPWL",
  "library": "Simulation_SPICE",
  "ref_prefix": "V",
  "description": "Voltage source, piece-wise linear",
  "keywords": "simulation",
  "datasheet": "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#sec_Independent_Sources_for"
}
```

## VSFFM
Definition:
```json
{
  "symbol": "VSFFM",
  "library": "Simulation_SPICE",
  "ref_prefix": "V",
  "description": "Voltage source, single-frequency FM",
  "keywords": "simulation frequency modulated",
  "datasheet": "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#sec_Independent_Sources_for"
}
```

## VSIN
Definition:
```json
{
  "symbol": "VSIN",
  "library": "Simulation_SPICE",
  "ref_prefix": "V",
  "description": "Voltage source, sinusoidal",
  "keywords": "simulation ac vac",
  "datasheet": "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#sec_Independent_Sources_for"
}
```

## VTRNOISE
Definition:
```json
{
  "symbol": "VTRNOISE",
  "library": "Simulation_SPICE",
  "ref_prefix": "V",
  "description": "Voltage source, transient noise",
  "keywords": "simulation",
  "datasheet": "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#subsec_Transient_noise_source"
}
```

## VTRRANDOM
Definition:
```json
{
  "symbol": "VTRRANDOM",
  "library": "Simulation_SPICE",
  "ref_prefix": "V",
  "description": "Voltage source, random noise",
  "keywords": "simulation",
  "datasheet": "https://ngspice.sourceforge.io/docs/ngspice-html-manual/manual.xhtml#subsec_Random_voltage_source"
}
```
