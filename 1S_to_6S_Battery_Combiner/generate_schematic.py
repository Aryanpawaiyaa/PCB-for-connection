#!/usr/bin/env python3
"""
Generate a 100% on-grid KiCad 9 schematic (.kicad_sch)
Aligned to standard 50-mil (1.27mm) grid.
"""

import os
import uuid

def generate_schematic(project_dir="/home/aryan/pcb_1s_to_6s_combiner"):
    sch_path = os.path.join(project_dir, "pcb_1s_to_6s_combiner.kicad_sch")

    def uid():
        return str(uuid.uuid4())

    sch_text = f"""(kicad_sch
	(version 20250114)
	(generator "eeschema")
	(generator_version "9.0")
	(uuid "{uid()}")
	(paper "A4")
	(title_block
		(title "1S x 6 to 6S Series Battery Combiner")
		(date "2026-11-07")
		(rev "1.0")
		(company "Antigravity Hardware")
		(comment 1 "Connects 6x 1S LiPo/Li-ion batteries in series to 6S output")
		(comment 2 "Inputs: 6x XT30-M | Output: 1x XT60-F | Balance: 1x JST-XH 7P")
	)
	(lib_symbols
		(symbol "Connector_Generic:Conn_01x02"
			(pin_names (offset 1.016) (hide yes))
			(exclude_from_sim no) (in_bom yes) (on_board yes)
			(property "Reference" "J" (at 0 2.54 0) (effects (font (size 1.27 1.27))))
			(property "Value" "Conn_01x02" (at 0 -5.08 0) (effects (font (size 1.27 1.27))))
			(symbol "Conn_01x02_1_1"
				(rectangle (start -1.27 1.27) (end 1.27 -3.81) (stroke (width 0.254) (type default)) (fill (type background)))
				(pin passive line (at -5.08 0 0) (length 3.81) (name "Pin_1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -5.08 -2.54 0) (length 3.81) (name "Pin_2" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "Connector_Generic:Conn_01x07"
			(pin_names (offset 1.016) (hide yes))
			(exclude_from_sim no) (in_bom yes) (on_board yes)
			(property "Reference" "J" (at 0 2.54 0) (effects (font (size 1.27 1.27))))
			(property "Value" "Conn_01x07" (at 0 -17.78 0) (effects (font (size 1.27 1.27))))
			(symbol "Conn_01x07_1_1"
				(rectangle (start -1.27 1.27) (end 1.27 -16.51) (stroke (width 0.254) (type default)) (fill (type background)))
				(pin passive line (at -5.08 0 0) (length 3.81) (name "Pin_1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -5.08 -2.54 0) (length 3.81) (name "Pin_2" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -5.08 -5.08 0) (length 3.81) (name "Pin_3" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -5.08 -7.62 0) (length 3.81) (name "Pin_4" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -5.08 -10.16 0) (length 3.81) (name "Pin_5" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -5.08 -12.7 0) (length 3.81) (name "Pin_6" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -5.08 -15.24 0) (length 3.81) (name "Pin_7" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
			)
		)
	)
"""

    # Grid aligned positions (multiples of 1.27mm):
    # J_BAT1..6: X = 50.8 + (i-1)*25.4, Y = 50.8
    # Pin 1 at (bx - 5.08, 50.8)
    # Pin 2 at (bx - 5.08, 53.34)
    labels = []
    net_names = ["GND", "CELL1_POS", "CELL2_POS", "CELL3_POS", "CELL4_POS", "CELL5_POS", "OUT_6S_POS"]

    for i in range(1, 7):
        bx = 50.8 + (i - 1) * 25.4
        sch_text += f"""
	(symbol
		(lib_id "Connector_Generic:Conn_01x02")
		(at {bx:.2f} 50.8 0)
		(unit 1)
		(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)
		(uuid "{uid()}")
		(property "Reference" "J_BAT{i}" (at {bx:.2f} 45.72 0) (effects (font (size 1.27 1.27))))
		(property "Value" "XT30-M (1S)" (at {bx:.2f} 55.88 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "Connector_AMASS:AMASS_XT30U-M_1x02_P5.0mm_Vertical" (at {bx:.2f} 50.8 0) (effects (font (size 1.27 1.27)) (hide yes)))
		(pin "1" (uuid "{uid()}"))
		(pin "2" (uuid "{uid()}"))
	)
"""
        labels.append((net_names[i-1], bx - 5.08, 50.8))
        labels.append((net_names[i], bx - 5.08, 53.34))

    # J_OUT (XT60) at X = 203.2, Y = 50.8
    out_x = 203.2
    sch_text += f"""
	(symbol
		(lib_id "Connector_Generic:Conn_01x02")
		(at {out_x:.2f} 50.8 0)
		(unit 1)
		(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)
		(uuid "{uid()}")
		(property "Reference" "J_OUT" (at {out_x:.2f} 45.72 0) (effects (font (size 1.27 1.27))))
		(property "Value" "XT60-F (6S)" (at {out_x:.2f} 55.88 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "Connector_AMASS:AMASS_XT60-F_1x02_P7.20mm_Vertical" (at {out_x:.2f} 50.8 0) (effects (font (size 1.27 1.27)) (hide yes)))
		(pin "1" (uuid "{uid()}"))
		(pin "2" (uuid "{uid()}"))
	)
"""
    labels.append(("GND", out_x - 5.08, 50.8))
    labels.append(("OUT_6S_POS", out_x - 5.08, 53.34))

    # J_BAL at X = 114.3, Y = 101.6
    bal_x = 114.3
    bal_y = 101.6
    sch_text += f"""
	(symbol
		(lib_id "Connector_Generic:Conn_01x07")
		(at {bal_x:.2f} {bal_y:.2f} 0)
		(unit 1)
		(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)
		(uuid "{uid()}")
		(property "Reference" "J_BAL" (at {bal_x:.2f} {bal_y - 3.81:.2f} 0) (effects (font (size 1.27 1.27))))
		(property "Value" "JST-XH-7P (6S)" (at {bal_x:.2f} {bal_y + 19.05:.2f} 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "Connector_JST:JST_XH_B7B-XH-A_1x07_P2.50mm_Vertical" (at {bal_x:.2f} {bal_y:.2f} 0) (effects (font (size 1.27 1.27)) (hide yes)))
		(pin "1" (uuid "{uid()}"))
		(pin "2" (uuid "{uid()}"))
		(pin "3" (uuid "{uid()}"))
		(pin "4" (uuid "{uid()}"))
		(pin "5" (uuid "{uid()}"))
		(pin "6" (uuid "{uid()}"))
		(pin "7" (uuid "{uid()}"))
	)
"""
    for p in range(7):
        labels.append((net_names[p], bal_x - 5.08, bal_y + p * 2.54))

    # Add Net Labels
    for text, lx, ly in labels:
        sch_text += f"""
	(label "{text}"
		(at {lx:.2f} {ly:.2f} 180)
		(fields_autoplaced yes)
		(uuid "{uid()}")
		(effects (font (size 1.27 1.27)) (justify right))
	)
"""

    sch_text += ")\n"

    with open(sch_path, "w") as f:
        f.write(sch_text)

    print(f"[SUCCESS] On-grid schematic written to: {sch_path}")

if __name__ == "__main__":
    generate_schematic()
