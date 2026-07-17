# DroneX Battery Carrier PCB

## Project Specification for AI-Assisted Development

---

# Project Overview

**Project Name:** DroneX Battery Carrier PCB

**Project Type:** Professional PCB Design using Atopile with KiCad Generation

**Primary Goal**

Develop a professional-grade Atopile project that automatically generates a complete KiCad PCB project for a compact battery carrier/interface board intended for UAV applications.

The emphasis of this project is on:

* Professional PCB engineering
* Clean project architecture
* Mechanical integration
* Connector placement
* Manufacturing readiness
* Atopile best practices
* KiCad compatibility
* Documentation quality

The project should be written as though it is being developed by an experienced hardware engineer following industry-standard PCB design methodologies.

---

# Design Constraints

## Max PCB Dimensions (keeping the size within the given )

* Width: **50 mm**
* Height: **100 mm**
* Thickness: **1.6 mm**
* Shape: Rectangular
* Corner Radius: **3 mm**

---

# PCB Stackup

Use a **4-layer PCB**.

Layer Structure:

* Layer 1 — Top Copper (2 oz)
* Layer 2 — Continuous Ground Plane
* Layer 3 — Power Plane
* Layer 4 — Bottom Copper (2 oz)

Material:

* FR4
* 1.6 mm thickness

Copper:

* Outer Layers: 2 oz
* Inner Layers: 1 oz

---

# Mounting Requirements

Provide four mounting holes.

Specifications:

* M3
* Hole Diameter: 3.2 mm
* Located 5 mm from every corner

Keep copper clear around mounting holes.

---

# Connector Requirements

Include footprints and placement for:

* 6 × XT30 connectors
* 1 × XT90 connector

The design should prioritize:

* Mechanical robustness
* Symmetry
* Easy cable routing
* Assembly accessibility
* Clear silkscreen identification
* Adequate edge clearance

Connector labels should be human-readable.

---

# Routing Philosophy

The PCB should be designed using professional high-current layout practices.

Prioritize:

* Wide copper regions where appropriate
* Continuous ground reference
* Short routing paths
* Minimal unnecessary vias
* Proper copper pours
* Clean current return paths
* Thermal considerations
* Manufacturability

Include configurable design-rule parameters for:

* Minimum trace width
* Minimum clearance
* Minimum via drill
* Annular ring
* Copper-to-edge clearance
* Thermal relief settings

---

# Silkscreen Requirements

Generate professional silkscreen containing:

* Project name
* Revision placeholder
* Date placeholder
* Connector identifiers
* Pin numbering
* Polarity markings
* Company placeholder
* Version information

Silkscreen should remain legible after assembly.

---

# Mechanical Design

The PCB should include:

* Defined board outline
* Mounting holes
* Courtyard clearances
* Connector alignment
* Edge clearances
* Mechanical stability considerations

---

# Atopile Requirements

Generate a complete Atopile project.

The project should build successfully using:

```bash
ato build
```

No syntax errors should exist.

Use the latest stable Atopile syntax.

Avoid deprecated commands.

---

# Required File Structure

```
DroneX_Battery_Carrier/

├── ato.yaml
├── README.md
│
├── src/
│   ├── main.ato
│   ├── board.ato
│   ├── connectors.ato
│   ├── stackup.ato
│   ├── mounting.ato
│   ├── silkscreen.ato
│   ├── rules.ato
│   └── power.ato
│
├── footprints/
│
├── symbols/
│
├── outputs/
```

Every file should be fully implemented.

No placeholder files.

No omitted sections.

---

# KiCad Generation

The generated project should include:

* Schematic
* PCB
* Netlist
* Footprints
* Symbols
* Design Rules
* Stackup definition

The PCB should open without errors in the current stable version of KiCad.

---

# Manufacturing Outputs

The completed project should support generation of:

* Gerber files
* Drill files
* STEP model
* BOM
* Pick-and-Place files
* IPC-compatible outputs where applicable

---

# Documentation Requirements

The generated README should explain:

* Project overview
* Folder structure
* Build process
* Atopile commands
* KiCad generation
* How to modify board dimensions
* How to update footprints
* How to regenerate outputs
* Version requirements

---

# Coding Standards

The generated Atopile code should be:

* Modular
* Readable
* Well commented
* Professionally formatted
* Reusable
* Consistent
* Organized by functionality

Every module should have a clearly defined responsibility.

---

# Expected Deliverables

The AI should generate:

* Complete Atopile source
* Complete KiCad project
* Complete documentation
* Buildable project
* Production-ready project structure
* Clean directory organization

---

# Quality Expectations

The project should reflect professional engineering practices and be suitable as a reference implementation for learning Atopile and KiCad workflows. The emphasis is on maintainability, documentation, and manufacturable PCB design rather than on implementing battery pack internals or battery management functionality.

The final output should be self-contained, well documented, and ready for further customization by the user.
