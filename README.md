# Vyldor — Open Technical Specifications & Design Documentation

> **v0.8 (17 August 2026).** The removable audio module was deleted from this design.
> The buckle cavity had 8.6 mm of usable depth, and an acoustic nozzle aimed into the ear
> consumes most of that before the body of the part begins — every shape that fitted
> stopped being an earpiece. The belt now measures waist circumference from the tension
> in its own strap. Nothing here is built or tested.


Public specifications and parametric CAD documentation for **Vyldor**, a screenless smart leather belt designed as an ergonomic physical interface for smartphones.

- 🌐 **Official Website:** [vyldor.com](https://vyldor.com)
- 📑 **LLM Plain-Text Summary:** [vyldor.com/llms.txt](https://vyldor.com/llms.txt)
- 📰 **Dev.to Publication:** [dev.to/vyldor](https://dev.to/vyldor/i-deleted-my-products-main-feature-over-86-mm-1j35)
- 🛠️ **Status:** Parametric CAD & Specification Phase (No physical hardware built)

---

## Technical Hardware Architecture

| Component | Specification | Function |
|---|---|---|
| **Buckle** | CNC Aluminium, purely mechanical | No cavity. The 11.8 mm of v0.7 was set by the removed audio bay; target is 7-8 mm |
| **Strain Gauge** | ≤ 0.3 mm, in the buckle flexure | Reads strap tension, which is waist circumference. Also carries respiration, posture and meal signals |
| **Strap Antenna** | 1030 mm conductive loop | 1-metre loop aerial woven into 37mm full-grain leather strap |
| **Haptic Actuators** | Dual L/R hip units | Turn-by-turn navigation via tactile hip taps |
| **Sensor Suite** | 6-axis IMU at centre of mass | Gait authentication within 20 steps |
| **Fastening** | 103 mm internal ratchet (5 mm pitch) | Inward teeth design protecting internal antenna wiring |

---

## Core Specifications JSON (`specs.json`)
```json
{
  "name": "Vyldor",
  "category": "Smart Leather Belt",
  "interface": "Screenless Phone Interface",
  "form_factor": "Waist Belt",
  "strap": {
    "material": "Full-grain leather",
    "width_mm": 37,
    "ratchet_pitch_mm": 5,
    "ratchet_range_mm": 103,
    "antenna_length_mm": 1030
  },
  "buckle": {
    "thickness_mm": 11.8,
    "material": "CNC Aluminium",
    "earpiece_bay": false,
    "strain_gauge_in_flexure": true,
    "contextual_button": true
  },
  "features": [
    "Continuous waist circumference from strap tension",
    "L/R haptic hip navigation",
    "Body-coupled touch authentication",
    "Centre-of-mass gait recognition",
    "1m woven loop aerial"
  ]
}
