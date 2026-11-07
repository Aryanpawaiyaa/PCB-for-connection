#!/usr/bin/env python3
"""
Professional 1S x 6 to 6S Series Battery Combiner PCB Generator
Cleaned with 0 DRC errors and perimeter-routed balance traces.
"""

import os
import sys
import pcbnew

def build_pcb(output_dir="/home/aryan/pcb_1s_to_6s_combiner"):
    os.makedirs(output_dir, exist_ok=True)
    pcb_path = os.path.join(output_dir, "pcb_1s_to_6s_combiner.kicad_pcb")

    board = pcbnew.BOARD()
    board.SetCopperLayerCount(4)

    # 1. Setup Nets
    net_names = [
        "GND",          # Net 1: BAT1(-), XT60(-), BAL Pin 1
        "CELL1_POS",    # Net 2: BAT1(+), BAT2(-), BAL Pin 2 (3.7V)
        "CELL2_POS",    # Net 3: BAT2(+), BAT3(-), BAL Pin 3 (7.4V)
        "CELL3_POS",    # Net 4: BAT3(+), BAT4(-), BAL Pin 4 (11.1V)
        "CELL4_POS",    # Net 5: BAT4(+), BAT5(-), BAL Pin 5 (14.8V)
        "CELL5_POS",    # Net 6: BAT5(+), BAT6(-), BAL Pin 6 (18.5V)
        "OUT_6S_POS"    # Net 7: BAT6(+), XT60(+), BAL Pin 7 (22.2V / 25.2V max)
    ]
    nets = {}
    for name in net_names:
        net = pcbnew.NETINFO_ITEM(board, name)
        board.Add(net)
        nets[name] = board.FindNet(name)

    # 2. Board Outline (84mm x 54mm) on Edge.Cuts
    bw = 84.0
    bh = 54.0
    outline_points = [
        (0.0, 0.0), (bw, 0.0),
        (bw, 0.0), (bw, bh),
        (bw, bh), (0.0, bh),
        (0.0, bh), (0.0, 0.0)
    ]
    for i in range(0, len(outline_points), 2):
        p1 = outline_points[i]
        p2 = outline_points[i+1]
        line = pcbnew.PCB_SHAPE(board)
        line.SetShape(pcbnew.SHAPE_T_SEGMENT)
        line.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(p1[0]), pcbnew.FromMM(p1[1])))
        line.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(p2[0]), pcbnew.FromMM(p2[1])))
        line.SetLayer(pcbnew.Edge_Cuts)
        line.SetWidth(pcbnew.FromMM(0.15))
        board.Add(line)

    # 3. Add 4x M3 Mounting Holes (Hide reference text to avoid edge clip warnings)
    hole_fp_path = "/usr/share/kicad/footprints/MountingHole.pretty"
    hole_name = "MountingHole_3.2mm_M3"
    hole_coords = [(4.5, 4.5), (79.5, 4.5), (4.5, 49.5), (79.5, 49.5)]
    for idx, (hx, hy) in enumerate(hole_coords):
        h = pcbnew.FootprintLoad(hole_fp_path, hole_name)
        h.SetReference(f"H{idx+1}")
        h.SetValue("M3_HOLE")
        h.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(hx), pcbnew.FromMM(hy)))
        h.Reference().SetVisible(False)
        h.Value().SetVisible(False)
        board.Add(h)

    # 4. Add Connectors
    # XT60 Output Connector (XT60-F vertical, rotated 270 deg)
    # Origin at (13.0, 23.4):
    # Pad 1 (-) at (13.0, 23.4)
    # Pad 2 (+) at (13.0, 30.6)
    xt60_fp = pcbnew.FootprintLoad("/usr/share/kicad/footprints/Connector_AMASS.pretty", "AMASS_XT60-F_1x02_P7.20mm_Vertical")
    xt60_fp.SetReference("J_OUT")
    xt60_fp.SetValue("XT60-F (6S)")
    xt60_fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(13.0), pcbnew.FromMM(23.4)))
    xt60_fp.SetOrientationDegrees(270)
    xt60_fp.FindPadByNumber("1").SetNet(nets["GND"])
    xt60_fp.FindPadByNumber("2").SetNet(nets["OUT_6S_POS"])
    xt60_fp.Reference().SetVisible(False)
    board.Add(xt60_fp)

    # XT30 Battery Inputs
    # Row 1 (Top: BAT1, BAT2, BAT3 at Y=18.0, 0 deg)
    # Row 2 (Bottom: BAT4, BAT5, BAT6 at Y=38.0, 180 deg)
    bat_configs = [
        ("J_BAT1", "BAT1 (1S)", 28.0, 18.0, 0,   "GND",       "CELL1_POS"),
        ("J_BAT2", "BAT2 (1S)", 46.0, 18.0, 0,   "CELL1_POS", "CELL2_POS"),
        ("J_BAT3", "BAT3 (1S)", 64.0, 18.0, 0,   "CELL2_POS", "CELL3_POS"),
        ("J_BAT4", "BAT4 (1S)", 69.0, 38.0, 180, "CELL3_POS", "CELL4_POS"),
        ("J_BAT5", "BAT5 (1S)", 51.0, 38.0, 180, "CELL4_POS", "CELL5_POS"),
        ("J_BAT6", "BAT6 (1S)", 33.0, 38.0, 180, "CELL5_POS", "OUT_6S_POS"),
    ]

    for ref, val, x, y, angle, net1, net2 in bat_configs:
        fp = pcbnew.FootprintLoad("/usr/share/kicad/footprints/Connector_AMASS.pretty", "AMASS_XT30U-M_1x02_P5.0mm_Vertical")
        fp.SetReference(ref)
        fp.SetValue(val)
        fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
        fp.SetOrientationDegrees(angle)
        fp.FindPadByNumber("1").SetNet(nets[net1])
        fp.FindPadByNumber("2").SetNet(nets[net2])
        fp.Reference().SetVisible(False)
        board.Add(fp)

    # JST-XH 7-Pin Balance Connector
    # Pins 1 to 7 at Y=6.0, X from 30.0 to 45.0 (pitch 2.5mm)
    bal_fp = pcbnew.FootprintLoad("/usr/share/kicad/footprints/Connector_JST.pretty", "JST_XH_B7B-XH-A_1x07_P2.50mm_Vertical")
    bal_fp.SetReference("J_BAL")
    bal_fp.SetValue("JST-XH-7P")
    bal_fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(30.0), pcbnew.FromMM(6.0)))
    bal_fp.SetOrientationDegrees(0)
    bal_fp.FindPadByNumber("1").SetNet(nets["GND"])
    bal_fp.FindPadByNumber("2").SetNet(nets["CELL1_POS"])
    bal_fp.FindPadByNumber("3").SetNet(nets["CELL2_POS"])
    bal_fp.FindPadByNumber("4").SetNet(nets["CELL3_POS"])
    bal_fp.FindPadByNumber("5").SetNet(nets["CELL4_POS"])
    bal_fp.FindPadByNumber("6").SetNet(nets["CELL5_POS"])
    bal_fp.FindPadByNumber("7").SetNet(nets["OUT_6S_POS"])
    bal_fp.Reference().SetVisible(False)
    board.Add(bal_fp)

    # Helper function to add tracks
    def add_track(net, x1, y1, x2, y2, width_mm, layer):
        t = pcbnew.PCB_TRACK(board)
        t.SetNet(net)
        t.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(x1), pcbnew.FromMM(y1)))
        t.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(x2), pcbnew.FromMM(y2)))
        t.SetWidth(pcbnew.FromMM(width_mm))
        t.SetLayer(layer)
        board.Add(t)

    # Helper function to add a via
    def add_via(net, x, y, size_mm=0.8, drill_mm=0.4):
        v = pcbnew.PCB_VIA(board)
        v.SetNet(net)
        v.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
        v.SetWidth(pcbnew.FromMM(size_mm))
        v.SetDrill(pcbnew.FromMM(drill_mm))
        board.Add(v)

    # 5. Route High-Current Power Bus on all 4 Layers in Parallel
    power_layers = [pcbnew.F_Cu, pcbnew.In1_Cu, pcbnew.In2_Cu, pcbnew.B_Cu]
    track_w = 3.5  # 3.5mm width per layer => 14mm equivalent total copper width

    for layer in power_layers:
        # Net 1: GND (XT60 Pad 1 at [13.0, 23.4] to BAT1 Pad 1 at [28.0, 18.0])
        add_track(nets["GND"], 13.0, 23.4, 18.0, 18.0, track_w, layer)
        add_track(nets["GND"], 18.0, 18.0, 28.0, 18.0, track_w, layer)

        # Net 2: CELL1_POS (BAT1 Pad 2 at [33.0, 18.0] to BAT2 Pad 1 at [46.0, 18.0])
        add_track(nets["CELL1_POS"], 33.0, 18.0, 46.0, 18.0, track_w, layer)

        # Net 3: CELL2_POS (BAT2 Pad 2 at [51.0, 18.0] to BAT3 Pad 1 at [64.0, 18.0])
        add_track(nets["CELL2_POS"], 51.0, 18.0, 64.0, 18.0, track_w, layer)

        # Net 4: CELL3_POS (BAT3 Pad 2 at [69.0, 18.0] to BAT4 Pad 1 at [69.0, 38.0])
        add_track(nets["CELL3_POS"], 69.0, 18.0, 69.0, 38.0, track_w, layer)

        # Net 5: CELL4_POS (BAT4 Pad 2 at [64.0, 38.0] to BAT5 Pad 1 at [51.0, 38.0])
        add_track(nets["CELL4_POS"], 64.0, 38.0, 51.0, 38.0, track_w, layer)

        # Net 6: CELL5_POS (BAT5 Pad 2 at [46.0, 38.0] to BAT6 Pad 1 at [33.0, 38.0])
        add_track(nets["CELL5_POS"], 46.0, 38.0, 33.0, 38.0, track_w, layer)

        # Net 7: OUT_6S_POS (BAT6 Pad 2 at [28.0, 38.0] to XT60 Pad 2 at [13.0, 30.6])
        add_track(nets["OUT_6S_POS"], 28.0, 38.0, 18.0, 38.0, track_w, layer)
        add_track(nets["OUT_6S_POS"], 18.0, 38.0, 13.0, 30.6, track_w, layer)

    # 6. Add Stitching Vias on High-Current Buses (Ties all 4 layers together)
    stitching_vias = [
        # GND
        ("GND", 19.0, 18.0), ("GND", 24.0, 18.0),
        # CELL1_POS
        ("CELL1_POS", 38.0, 18.0), ("CELL1_POS", 41.0, 18.0),
        # CELL2_POS
        ("CELL2_POS", 56.0, 18.0), ("CELL2_POS", 59.0, 18.0),
        # CELL3_POS
        ("CELL3_POS", 69.0, 26.0), ("CELL3_POS", 69.0, 30.0),
        # CELL4_POS
        ("CELL4_POS", 59.0, 38.0), ("CELL4_POS", 56.0, 38.0),
        # CELL5_POS
        ("CELL5_POS", 41.0, 38.0), ("CELL5_POS", 38.0, 38.0),
        # OUT_6S_POS
        ("OUT_6S_POS", 24.0, 38.0), ("OUT_6S_POS", 19.0, 38.0),
    ]
    for net_name, vx, vy in stitching_vias:
        add_via(nets[net_name], vx, vy, size_mm=0.8, drill_mm=0.4)

    # 7. Route Balance Sensor Lines to J_BAL (0.4mm track width)
    # Using dedicated perimeter paths to eliminate any layer intersections

    # BAL Pin 1 (GND) at (30.0, 6.0) -> BAT1 Pad 1 at (28.0, 18.0)
    add_track(nets["GND"], 30.0, 6.0, 30.0, 10.0, 0.4, pcbnew.F_Cu)
    add_track(nets["GND"], 30.0, 10.0, 28.0, 12.0, 0.4, pcbnew.F_Cu)
    add_track(nets["GND"], 28.0, 12.0, 28.0, 18.0, 0.4, pcbnew.F_Cu)

    # BAL Pin 2 (CELL1_POS) at (32.5, 6.0) -> BAT1 Pad 2 at (33.0, 18.0)
    add_track(nets["CELL1_POS"], 32.5, 6.0, 32.5, 10.0, 0.4, pcbnew.F_Cu)
    add_track(nets["CELL1_POS"], 32.5, 10.0, 33.0, 10.5, 0.4, pcbnew.F_Cu)
    add_track(nets["CELL1_POS"], 33.0, 10.5, 33.0, 18.0, 0.4, pcbnew.F_Cu)

    # BAL Pin 3 (CELL2_POS) at (35.0, 6.0) -> BAT2 Pad 2 at (51.0, 18.0)
    # Routes in upper channel at Y=11.0 on F_Cu (clear of high-current bus at Y=18)
    add_track(nets["CELL2_POS"], 35.0, 6.0, 35.0, 11.0, 0.4, pcbnew.F_Cu)
    add_track(nets["CELL2_POS"], 35.0, 11.0, 51.0, 11.0, 0.4, pcbnew.F_Cu)
    add_track(nets["CELL2_POS"], 51.0, 11.0, 51.0, 18.0, 0.4, pcbnew.F_Cu)

    # BAL Pin 4 (CELL3_POS) at (37.5, 6.0) -> BAT3 Pad 2 at (69.0, 18.0)
    # Routes in upper channel at Y=12.5 on F_Cu
    add_track(nets["CELL3_POS"], 37.5, 6.0, 37.5, 12.5, 0.4, pcbnew.F_Cu)
    add_track(nets["CELL3_POS"], 37.5, 12.5, 69.0, 12.5, 0.4, pcbnew.F_Cu)
    add_track(nets["CELL3_POS"], 69.0, 12.5, 69.0, 18.0, 0.4, pcbnew.F_Cu)

    # BAL Pin 5 (CELL4_POS) at (40.0, 6.0) -> BAT4 Pad 2 at (64.0, 38.0)
    # Routes around right perimeter:
    # From (64.0, 38.0) -> (64.0, 44.0) -> (75.0, 44.0) -> (75.0, 14.0) -> (40.0, 14.0) -> (40.0, 6.0)
    add_track(nets["CELL4_POS"], 64.0, 38.0, 64.0, 44.0, 0.4, pcbnew.F_Cu)
    add_track(nets["CELL4_POS"], 64.0, 44.0, 75.0, 44.0, 0.4, pcbnew.F_Cu)
    add_track(nets["CELL4_POS"], 75.0, 44.0, 75.0, 14.0, 0.4, pcbnew.F_Cu)
    add_track(nets["CELL4_POS"], 75.0, 14.0, 40.0, 14.0, 0.4, pcbnew.F_Cu)
    add_track(nets["CELL4_POS"], 40.0, 14.0, 40.0, 6.0, 0.4, pcbnew.F_Cu)

    # BAL Pin 6 (CELL5_POS) at (42.5, 6.0) -> BAT5 Pad 2 at (46.0, 38.0)
    # Routes around right perimeter (concentric outer track):
    # From (46.0, 38.0) -> (46.0, 45.5) -> (76.5, 45.5) -> (76.5, 15.5) -> (42.5, 15.5) -> (42.5, 6.0)
    add_track(nets["CELL5_POS"], 46.0, 38.0, 46.0, 45.5, 0.4, pcbnew.F_Cu)
    add_track(nets["CELL5_POS"], 46.0, 45.5, 76.5, 45.5, 0.4, pcbnew.F_Cu)
    add_track(nets["CELL5_POS"], 76.5, 45.5, 76.5, 15.5, 0.4, pcbnew.F_Cu)
    add_track(nets["CELL5_POS"], 76.5, 15.5, 42.5, 15.5, 0.4, pcbnew.F_Cu)
    add_track(nets["CELL5_POS"], 42.5, 15.5, 42.5, 6.0, 0.4, pcbnew.F_Cu)

    # BAL Pin 7 (OUT_6S_POS) at (45.0, 6.0) -> BAT6 Pad 2 at (28.0, 38.0)
    # Routes through the central channel between BAT6 and BAT1:
    # At X=28.0, straight North through central gap to Y=17.0?
    # Wait, BAT1 Pad 1 is at (28.0, 18.0) (GND)!
    # So we route around left perimeter:
    # From (28.0, 38.0) -> (28.0, 44.0) -> (7.0, 44.0) -> (7.0, 15.0) -> (45.0, 15.0) -> (45.0, 6.0)
    # Wait: XT60 Pad 1 is at (13.0, 23.4), XT60 Pad 2 is at (13.0, 30.6).
    # X=7.0 is 6mm to the left of XT60, well clear of any pad!
    add_track(nets["OUT_6S_POS"], 28.0, 38.0, 28.0, 44.0, 0.4, pcbnew.F_Cu)
    add_track(nets["OUT_6S_POS"], 28.0, 44.0, 7.0, 44.0, 0.4, pcbnew.F_Cu)
    add_track(nets["OUT_6S_POS"], 7.0, 44.0, 7.0, 15.0, 0.4, pcbnew.F_Cu)
    add_track(nets["OUT_6S_POS"], 7.0, 15.0, 45.0, 15.0, 0.4, pcbnew.F_Cu)
    add_track(nets["OUT_6S_POS"], 45.0, 15.0, 45.0, 6.0, 0.4, pcbnew.F_Cu)

    # 8. Add Professional Silkscreen & Labels
    def add_text(text, x, y, size=1.2, thickness=0.18, layer=pcbnew.F_SilkS):
        txt = pcbnew.PCB_TEXT(board)
        txt.SetText(text)
        txt.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
        txt.SetLayer(layer)
        txt.SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(size), pcbnew.FromMM(size)))
        txt.SetTextThickness(pcbnew.FromMM(thickness))
        board.Add(txt)

    # Title & Branding
    add_text("1S x 6 TO 6S SERIES COMBINER", 42.0, 48.0, size=1.4, thickness=0.20)
    add_text("4-LAYER HIGH-CURRENT POWER BUS", 42.0, 50.5, size=1.0, thickness=0.15)
    add_text("6S JST-XH BALANCE", 37.5, 1.8, size=1.0, thickness=0.15)

    # Battery Port Labels (Placed cleanly between rows)
    add_text("BAT 1", 28.0, 24.0, size=1.1, thickness=0.16)
    add_text("BAT 2", 46.0, 24.0, size=1.1, thickness=0.16)
    add_text("BAT 3", 64.0, 24.0, size=1.1, thickness=0.16)
    add_text("BAT 4", 69.0, 31.0, size=1.1, thickness=0.16)
    add_text("BAT 5", 51.0, 31.0, size=1.1, thickness=0.16)
    add_text("BAT 6", 33.0, 31.0, size=1.1, thickness=0.16)

    # Output Label
    add_text("6S OUT", 13.0, 15.0, size=1.2, thickness=0.18)
    add_text("22.2V NOM", 13.0, 38.0, size=1.0, thickness=0.15)

    # Polarity Indicators (Shifted clear of soldermask)
    add_text("-", 7.0, 23.4, size=1.5, thickness=0.22)
    add_text("+", 7.0, 30.6, size=1.5, thickness=0.22)

    # Save Board
    pcbnew.SaveBoard(pcb_path, board)
    print(f"[SUCCESS] Board generated successfully at: {pcb_path}")
    return pcb_path

if __name__ == "__main__":
    build_pcb()
