# DroneX Battery Carrier PCB

This project is a code-first hardware design of a high-current battery carrier PCB for UAVs. It is written in the **Atopile** hardware description language and compiles directly into a native **KiCad** project.

The board interfaces **six external battery modules** (via AMASS XT30 connectors) in a parallel power distribution configuration, delivering power to a single high-power output (via an AMASS XT90 connector). The power network is designed to work with modules constructed from **Molicel P50B** high-drain lithium-ion cells.

---

## Technical Specifications

| Parameter | Specification |
| --- | --- |
| **Max Dimensions** | 50 mm (Width) × 100 mm (Length) × 1.6 mm (Thickness) |
| **Stackup** | 4-layer FR4 (2 oz copper outer, 1 oz inner layers) |
| **Mechanical Mounts** | 4 × M3 mounting holes, 3.2 mm diameter, 5 mm offset from corners |
| **Voltage Range** | 18.0V (Min/Cut-off) — 21.6V (Nominal) — 25.2V (Max/Charge) [6S Li-ion] |
| **Current Handling** | 30A max per XT30 input branch, 90A nominal/max for the main XT90 bus |
| **DRC Constraints** | Min Trace: 0.15 mm, Min Clearance: 0.15 mm, Min Via: 0.3 mm drill / 0.6 mm outer |

---

## Directory Structure

```
DroneX_Battery_Carrier/
├── ato.yaml             # Atopile project and compiler target configuration
├── README.md            # Project and workflow documentation (this file)
├── src/                 # Atopile design source files
│   ├── main.ato         # Entry point instantiating all modules and power links
│   ├── board.ato        # Mechanical board geometry outline variables
│   ├── connectors.ato   # Component models for XT30 & XT90 with AMASS footprints
│   ├── stackup.ato      # 4-layer stackup parameter assignments
│   ├── mounting.ato     # M3 mounting hole models and placement variables
│   ├── silkscreen.ato   # Metadata, project identification, and safety polarity silk variables
│   ├── rules.ato        # DRC rules, trace widths, and thermal reliefs configuration
│   └── power.ato        # Power nets, interfaces, and electrical limit settings
├── footprints/          # Directory placeholder for local footprint files (.pretty)
├── symbols/             # Directory placeholder for local schematic symbol libraries (.kicad_sym)
└── outputs/             # Build output directory (netlists, schematics, PCB, fabrication data)
```

---

## Atopile Compilation Instructions

The Atopile compiler transforms your `.ato` hardware code into standard KiCad schematics and netlists.

### 1. Prerequisites
Ensure you have the `atopile` compiler installed:
```bash
pip install atopile
# Or verify version compatibility
ato --version
```

### 2. Build the Project
Run the compiler from the project root directory:
```bash
ato build
```
The compiler will:
- Validate syntax and enforce electrical rules/constraints.
- Generate netlists, KiCad schematic files (`.kicad_sch`), and layout updates for the board (`.kicad_pcb`).
- Store output artifacts in the `build/` or `outputs/` folder.

---

## KiCad Layout and Routing Workflow

Since Atopile handles structural netlist configuration, the physical placement and trace layout are completed in **KiCad**:

1. Open the generated project folder in **KiCad**.
2. Open the **PCB Editor** (`.kicad_pcb`).
3. Press `F8` (Update PCB from Schematic) to pull in all XT30/XT90 components and mounting holes.
4. **Placement Guidelines:**
   - Arrange the XT30 connectors symmetrically. Place **2 connectors on the left edge**, **2 on the right edge**, and **2 on the bottom edge**.
   - Place the output **XT90 connector on the top edge** for clean cable routing to the ESCs.
   - Position the 4 mounting holes at exactly `x=5mm, y=5mm` offsets from each corner.
5. **Power Routing / Copper Pours:**
   - Define a solid copper zone pour on Layer 2 (Inner GND Plane) assigned to the `GND` net.
   - Define wide copper plane pours on Layer 3 (Inner Power Plane) and Layer 4 (Bottom) assigned to the `V_BAT` net.
   - Connect the XT30 and XT90 terminals to their respective planes with thermal reliefs configured in `rules.ato` to ensure robust soldering.

---

## Generating Manufacturing Outputs

Once the layout is routed in KiCad, generate production files:

### 1. Gerber and Drill Files
1. Open the PCB Editor in KiCad.
2. Go to **File -> Plot...**.
3. Select layers: `F.Cu`, `B.Cu`, `In1.Cu`, `In2.Cu`, `F.SilkS`, `B.SilkS`, `F.Mask`, `B.Mask`, and `Edge.Cuts`.
4. Click **Plot** to generate Gerber files.
5. Click **Generate Drill Files...**, select your output directory, and click **Generate Drill File**.

### 2. STEP 3D Model
1. Open the PCB Editor.
2. Go to **File -> Export -> STEP...**.
3. Select the output directory, configure resolution settings, and click **Export** to create a 3D CAD assembly.

### 3. BOM & Pick-and-Place (CPL)
1. Go to **Tools -> Fabrication Outputs -> Component Placement...** to export Pick and Place coordinates (`.pos`).
2. Go to **Tools -> Fabrication Outputs -> BOM...** to export the Bill of Materials.
3. For Interactive BOMs, install the **Interactive Html BOM** plugin in KiCad, and select its icon to generate an interactive HTML placement review page.

---

## Maintenance and Modifications

### Modifying Footprints
To assign a different footprint to a connector (e.g. switching to horizontal XT30 connectors):
1. Open `src/connectors.ato`.
2. Locate `component XT30` and change the `footprint` value to your target library entry:
   ```ato
   footprint = "Connector_AMASS:AMASS_XT30U-F_1x02_P5.00mm_Horizontal"
   ```
3. Save and re-run `ato build`.

### Changing Board Dimensions
To resize the PCB (e.g. changing the width to 60 mm):
1. Open `src/board.ato`.
2. Modify the width parameter:
   ```ato
   width = 60mm
   ```
3. Update `src/mounting.ato` coordinate documentation to reflect the new dimensions, and redraw the boundary on the `Edge.Cuts` layer in KiCad.
