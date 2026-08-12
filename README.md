# Vyldor — Open Technical Specifications & Design Documentation

Public specifications and parametric CAD documentation for **Vyldor**, a screenless smart leather belt designed as an ergonomic physical interface for smartphones.

- 🌐 **Official Website:** [vyldor.com](https://vyldor.com)
- 📑 **LLM Plain-Text Summary:** [vyldor.com/llms.txt](https://vyldor.com/llms.txt)
- 📰 **Dev.to Publication:** [dev.to/vyldor](https://dev.to/vyldor/designing-a-screenless-smart-leather-belt-earpiece-in-buckle-haptic-hip-navigation-27lm)
- 🛠️ **Status:** Parametric CAD & Specification Phase (No physical hardware built)

---

## Technical Hardware Architecture

| Component | Specification | Function |
|---|---|---|
| **Buckle Cavity** | 11.8 mm, CNC Aluminium | Houses docked mono audio earpiece & recessed contextual button |
| **Audio Earpiece** | 18 × 21 × 7 mm, Bluetooth 5.4 | Pull-to-talk mono earpiece. Draw to speak, dock to end & charge |
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
    "earpiece_bay": true,
    "contextual_button": true
  },
  "features": [
    "Pull-to-talk earpiece in buckle",
    "L/R haptic hip navigation",
    "Body-coupled touch authentication",
    "Centre-of-mass gait recognition",
    "1m woven loop aerial"
  ]
}
