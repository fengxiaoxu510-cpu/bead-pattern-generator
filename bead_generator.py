#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
拼豆图纸生成器 (Bead Pattern Generator)
支持多品牌色卡、多尺寸输出、PDF导出
"""

import os
import sys
import argparse
import tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm


# ============================================================
# 品牌色卡数据库
# ============================================================

class BeadPalette:
    # MARD 国产拼豆 - 291色完整色卡
    MARD = {
        "A1": "#FAF4C8", "A2": "#FFFFD5", "A3": "#FEFF8B", "A4": "#FBED56",
        "A5": "#F4D738", "A6": "#FEAC4C", "A7": "#FE8B4C", "A8": "#FFDA45",
        "A9": "#FF995B", "A10": "#F77C31", "A11": "#FFDD99", "A12": "#FE9F72",
        "A13": "#FFC365", "A14": "#FD543D", "A15": "#FFF365", "A16": "#FFFF9F",
        "A17": "#FFE36E", "A18": "#FEBE7D", "A19": "#FD7C72", "A20": "#FFD568",
        "A21": "#FFE395", "A22": "#F4F57D", "A23": "#E6C9B7", "A24": "#F7F8A2",
        "A25": "#FFD67D", "A26": "#FFC830",
        "B1": "#E6EE31", "B2": "#63F347", "B3": "#9EF780", "B4": "#5DE035",
        "B5": "#35E352", "B6": "#65E2A6", "B7": "#3DAF80", "B8": "#1C9C4F",
        "B9": "#27523A", "B10": "#95D3C2", "B11": "#5D722A", "B12": "#166F41",
        "B13": "#CAEB7B", "B14": "#ADE946", "B15": "#2E5132", "B16": "#C5ED9C",
        "B17": "#9BB13A", "B18": "#E6EE49", "B19": "#24B88C", "B20": "#C2F0CC",
        "B21": "#156A6B", "B22": "#0B3C43", "B23": "#303A21", "B24": "#EEFCA5",
        "B25": "#4E846D", "B26": "#8D7A35", "B27": "#CCE1AF", "B28": "#9EE5B9",
        "B29": "#C5E254", "B30": "#E2FCB1", "B31": "#B0E792", "B32": "#9CAB5A",
        "C1": "#E8FFE7", "C2": "#A9F9FC", "C3": "#A0E2FB", "C4": "#41CCFF",
        "C5": "#01ACEB", "C6": "#50AAF0", "C7": "#3677D2", "C8": "#0F54C0",
        "C9": "#324BCA", "C10": "#3EBCE2", "C11": "#28DDDE", "C12": "#1C334D",
        "C13": "#CDE8FF", "C14": "#D5FDFF", "C15": "#22C4C6", "C16": "#1557A8",
        "C17": "#04D1F6", "C18": "#1D3344", "C19": "#1887A2", "C20": "#176DAF",
        "C21": "#BEDDFF", "C22": "#67B4BE", "C23": "#C8E2FF", "C24": "#7CC4FF",
        "C25": "#A9E5E5", "C26": "#3CAED8", "C27": "#D3DFFA", "C28": "#BBCFED",
        "C29": "#34488E",
        "D1": "#AEB4F2", "D2": "#858EDD", "D3": "#2F54AF", "D4": "#182A84",
        "D5": "#B843C5", "D6": "#AC7BDE", "D7": "#8854B3", "D8": "#E2D3FF",
        "D9": "#D5B9F8", "D10": "#361851", "D11": "#B9BAE1", "D12": "#DE9AD4",
        "D13": "#B90095", "D14": "#8B279B", "D15": "#2F1F90", "D16": "#E3E1EE",
        "D17": "#C4D4F6", "D18": "#A45EC7", "D19": "#D8C3D7", "D20": "#9C32B2",
        "D21": "#9A009B", "D22": "#333A95", "D23": "#EBDAFC", "D24": "#7786E5",
        "D25": "#494FC7", "D26": "#DFC2F8",
        "E1": "#FDD3CC", "E2": "#FEC0DF", "E3": "#FFB7E7", "E4": "#E8649E",
        "E5": "#F551A2", "E6": "#F13D74", "E7": "#C63478", "E8": "#FFDBE9",
        "E9": "#E970CC", "E10": "#D33793", "E11": "#FCDDD2", "E12": "#F78FC3",
        "E13": "#B5006D", "E14": "#FFD1BA", "E15": "#F8C7C9", "E16": "#FFF3EB",
        "E17": "#FFE2EA", "E18": "#FFC7DB", "E19": "#FEBAD5", "E20": "#D8C7D1",
        "E21": "#BD9DA1", "E22": "#B785A1", "E23": "#937A8D", "E24": "#E1BCE8",
        "F1": "#FD957B", "F2": "#FC3D46", "F3": "#F74941", "F4": "#FC283C",
        "F5": "#E7002F", "F6": "#943630", "F7": "#971937", "F8": "#BC0028",
        "F9": "#E2677A", "F10": "#8A4526", "F11": "#5A2121", "F12": "#FD4E6A",
        "F13": "#F35744", "F14": "#FFA9AD", "F15": "#D30022", "F16": "#FEC2A6",
        "F17": "#E69C79", "F18": "#D37C46", "F19": "#C1444A", "F20": "#CD9391",
        "F21": "#F7B4C6", "F22": "#FDC0D0", "F23": "#F67E66", "F24": "#E698AA",
        "F25": "#E54B4F",
        "G1": "#FFE2CE", "G2": "#FFC4AA", "G3": "#F4C3A5", "G4": "#E1B383",
        "G5": "#EDB045", "G6": "#E99C17", "G7": "#9D5B3E", "G8": "#753832",
        "G9": "#E6B483", "G10": "#D98C39", "G11": "#E0C593", "G12": "#FFC890",
        "G13": "#B7714A", "G14": "#8D614C", "G15": "#FCF9E0", "G16": "#F2D9BA",
        "G17": "#78524B", "G18": "#FFE4CC", "G19": "#E07935", "G20": "#A94023",
        "G21": "#B88558",
        "H1": "#FDFBFF", "H2": "#FEFFFF", "H3": "#B6B1BA", "H4": "#89858C",
        "H5": "#48464E", "H6": "#2F2B2F", "H7": "#000000", "H8": "#E7D6DB",
        "H9": "#EDEDED", "H10": "#EEE9EA", "H11": "#CECDD5", "H12": "#FFF5ED",
        "H13": "#F5ECD2", "H14": "#CFD7D3", "H15": "#98A6A8", "H16": "#1D1414",
        "H17": "#F1EDED", "H18": "#FFFDF0", "H19": "#F6EFE2", "H20": "#949FA3",
        "H21": "#FFFBE1", "H22": "#CACAD4", "H23": "#9A9D94",
        "M1": "#BCC6B8", "M2": "#8AA386", "M3": "#697D80", "M4": "#E3D2BC",
        "M5": "#D0CCAA", "M6": "#B0A782", "M7": "#B4A497", "M8": "#B38281",
        "M9": "#A58767", "M10": "#C5B2BC", "M11": "#9F7594", "M12": "#644749",
        "M13": "#D19066", "M14": "#C77362", "M15": "#757D78",
        "P1": "#FCF7F8", "P2": "#B0A9AC", "P3": "#AFDCAB", "P4": "#FEA49F",
        "P5": "#EE8C3E", "P6": "#5FD0A7", "P7": "#EB9270", "P8": "#F0D958",
        "P9": "#D9D9D9", "P10": "#D9C7EA", "P11": "#F3ECC9", "P12": "#E6EEF2",
        "P13": "#AACBEF", "P14": "#337680", "P15": "#668575", "P16": "#FEBF45",
        "P17": "#FEA324", "P18": "#FEB89F", "P19": "#FFFEEC", "P20": "#FEBECF",
        "P21": "#ECBEBF", "P22": "#E4A89F", "P23": "#A56268",
        "Q1": "#F2A5E8", "Q2": "#E9EC91", "Q3": "#FFFF00", "Q4": "#FFEBFA",
        "Q5": "#76CEDE",
        "R1": "#D50D21", "R2": "#F92F83", "R3": "#FD8324", "R4": "#F8EC31",
        "R5": "#35C75B", "R6": "#238891", "R7": "#19779D", "R8": "#1A60C3",
        "R9": "#9A56B4", "R10": "#FFDB4C", "R11": "#FFEBFA", "R12": "#D8D5CE",
        "R13": "#55514C", "R14": "#9FE4DF", "R15": "#77CEE9", "R16": "#3ECFCA",
        "R17": "#4A867A", "R18": "#7FCD9D", "R19": "#CDE55D", "R20": "#E8C7B4",
        "R21": "#AD6F3C", "R22": "#6C372F", "R23": "#FEB872", "R24": "#F3C1C0",
        "R25": "#C9675E", "R26": "#D293BE", "R27": "#EA8CB1", "R28": "#9C87D6",
        "T1": "#FFFFFF",
        "Y1": "#FD6FB4", "Y2": "#FEB481", "Y3": "#D7FAA0", "Y4": "#8BDBFA",
        "Y5": "#E987EA",
        "ZG1": "#DAABB3", "ZG2": "#D6AA87", "ZG3": "#C1BD8D", "ZG4": "#96869F",
        "ZG5": "#8490A6", "ZG6": "#94BFE2", "ZG7": "#E2A9D2", "ZG8": "#AB91C0",
    }

    ARTKAL = {
        "S01": "#FFFFFF", "S02": "#000000", "S03": "#FF0000", "S04": "#00FF00",
        "S05": "#0000FF", "S06": "#FFFF00", "S07": "#FF00FF", "S08": "#00FFFF",
        "S09": "#FFA500", "S10": "#800080", "S11": "#FFC0CB", "S12": "#A52A2A",
        "S13": "#808080", "S14": "#C0C0C0", "S15": "#FFD700", "S16": "#4B0082",
        "S17": "#00FF7F", "S18": "#FF4500", "S19": "#1E90FF", "S20": "#FF69B4",
        "S21": "#8B4513", "S22": "#2E8B57", "S23": "#DC143C", "S24": "#4169E1",
        "S25": "#F0E68C", "S26": "#D2691E", "S27": "#5F9EA0", "S28": "#FF6347",
        "S29": "#40E0D0", "S30": "#EE82EE", "S31": "#F5F5DC", "S32": "#696969",
        "S33": "#B22222", "S34": "#228B22", "S35": "#00008B", "S36": "#DAA520",
        "S37": "#D8BFD8", "S38": "#FF1493", "S39": "#7FFF00", "S40": "#9932CC",
    }

    HAMA = {
        "H01": "#FFFFFF", "H02": "#000000", "H03": "#FF0000", "H04": "#00AA00",
        "H05": "#0000CC", "H06": "#FFFF00", "H07": "#FF6600", "H08": "#CC0066",
        "H09": "#00CCCC", "H10": "#FFCC00", "H11": "#666666", "H12": "#CCCCCC",
        "H13": "#990000", "H14": "#006600", "H15": "#000099", "H16": "#FF9966",
        "H17": "#CC99FF", "H18": "#66CCFF", "H19": "#FFCCCC", "H20": "#CCFFCC",
        "H21": "#CCCCFF", "H22": "#FFCC99", "H23": "#99CCFF", "H24": "#CC99CC",
        "H25": "#99FF99", "H26": "#FF99CC", "H27": "#66FFCC", "H28": "#CCFF99",
        "H29": "#FF9999", "H30": "#9999FF", "H31": "#99FFCC", "H32": "#CC9999",
    }

    PERLER = {
        "P001": "#FFFFFF", "P002": "#000000", "P003": "#FF0000", "P004": "#00CC00",
        "P005": "#0000FF", "P006": "#FFFF00", "P007": "#FF6600", "P008": "#FF00FF",
        "P009": "#00FFFF", "P010": "#FFA500", "P011": "#808080", "P012": "#C0C0C0",
        "P013": "#FFD700", "P014": "#800080", "P015": "#FF1493", "P016": "#32CD32",
        "P017": "#1E90FF", "P018": "#FF4500", "P019": "#DA70D6", "P020": "#20B2AA",
        "P021": "#F4A460", "P022": "#778899", "P023": "#B0C4DE", "P024": "#FF6347",
        "P025": "#7CFC00", "P026": "#4169E1", "P027": "#DC143C", "P028": "#48D1CC",
        "P029": "#D2691E", "P030": "#9370DB", "P031": "#FA8072", "P032": "#87CEEB",
    }

    # 从JSON加载多品牌色卡数据库
    import json as _json
    _PALETTE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../references/bead_palettes.json")
    try:
        with open(_PALETTE_PATH) as _f:
            _EXTRA_PALETTES = _json.load(_f)
    except:
        _EXTRA_PALETTES = {}
    
    ARTKAL = _EXTRA_PALETTES.get("Artkal", ARTKAL)
    HAMA = _EXTRA_PALETTES.get("Hama", HAMA)
    PERLER = _EXTRA_PALETTES.get("Perler", PERLER)
    NABBI = _EXTRA_PALETTES.get("Nabbi", {})
    
    BRANDS = {
        "mard": {"name": "MARD 国产", "palette": MARD, "bead_size_mm": 5},
        "artkal": {"name": "Artkal S-5mm", "palette": ARTKAL, "bead_size_mm": 5},
        "hama": {"name": "Hama", "palette": HAMA, "bead_size_mm": 5},
        "perler": {"name": "Perler", "palette": PERLER, "bead_size_mm": 5},
        "nabbi": {"name": "Nabbi", "palette": NABBI, "bead_size_mm": 5},
        "hex": {"name": "通用色号 (HEX)", "palette": {}, "bead_size_mm": 5},
    }

    def __init__(self, brand="mard"):
        self.brand = brand.lower()
        if self.brand not in self.BRANDS:
            raise ValueError(f"不支持的品牌: {brand}。支持: {list(self.BRANDS.keys())}")
        self.config = self.BRANDS[self.brand]
        self.palette = self.config["palette"]
        self.codes = list(self.palette.keys())
        self.rgb_array = np.array([
            tuple(int(self.palette[c].lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
            for c in self.codes
        ])

    def find_closest(self, r, g, b):
        diff = self.rgb_array - np.array([r, g, b])
        dist = np.sum(diff ** 2, axis=1)
        idx = np.argmin(dist)
        return self.codes[idx], self.rgb_array[idx]

    def get_series_name(self, code):
        series_map = {
            "A": "黄橙", "B": "绿色", "C": "青蓝", "D": "紫蓝", "E": "粉色",
            "F": "红色", "G": "棕橙", "H": "黑白灰", "M": "大地", "P": "珍珠",
            "Q": "荧光", "R": "彩虹", "T": "纯白", "Y": "亮彩", "ZG": "复古",
            "S": "标准",
        }
        for prefix, name in series_map.items():
            if code.startswith(prefix):
                return name
        return "其他"


class BeadPatternGenerator:
    def __init__(self, palette, target_width=48):
        self.palette = palette
        self.target_width = target_width
        self.matched_grid = None
        self.matched_rgb = None
        self.bom = {}
        self.target_height = 0

    def process(self, image_path, max_colors=None):
        img = Image.open(image_path).convert("RGB")
        aspect = img.height / img.width
        self.target_height = max(1, int(self.target_width * aspect))
        small = img.resize((self.target_width, self.target_height), Image.Resampling.LANCZOS)
        small_np = np.array(small)

        self.matched_grid = np.zeros((self.target_height, self.target_width), dtype=object)
        self.matched_rgb = np.zeros((self.target_height, self.target_width, 3), dtype=np.uint8)
        self.bom = {}

        for y in range(self.target_height):
            for x in range(self.target_width):
                r, g, b = small_np[y, x]
                code, rgb = self.palette.find_closest(r, g, b)
                self.matched_grid[y, x] = code
                self.matched_rgb[y, x] = rgb
                self.bom[code] = self.bom.get(code, 0) + 1
        
        # 限制颜色数量（取最常用的 N 种）
        if max_colors and len(self.bom) > max_colors:
            top_colors = dict(sorted(self.bom.items(), key=lambda x: -x[1])[:max_colors])
            # 重建：非 top 颜色映射到最近的 top 颜色
            top_rgb = np.array([self.palette.rgb_array[self.palette.codes.index(c)] for c in top_colors])
            for y in range(self.target_height):
                for x in range(self.target_width):
                    code = self.matched_grid[y, x]
                    if code not in top_colors:
                        _, new_rgb = self.palette.find_closest(*self.matched_rgb[y, x])
                        # 找最近 top 色
                        diff = top_rgb - new_rgb
                        dist = np.sum(diff ** 2, axis=1)
                        best_idx = np.argmin(dist)
                        new_code = list(top_colors.keys())[best_idx]
                        self.matched_grid[y, x] = new_code
                        self.matched_rgb[y, x] = top_rgb[best_idx]
            # 重建 BOM
            self.bom = {}
            for y in range(self.target_height):
                for x in range(self.target_width):
                    code = self.matched_grid[y, x]
                    self.bom[code] = self.bom.get(code, 0) + 1
        
        return self

    def generate_pattern_image(self, bead_size=20, show_labels=True, original_img_path=None):
        """生成施工图纸：白底 + 色块 + 蓝色网格线 + 编号 + 原图缩略图 + 标题栏"""
        CELL_SPACING = 1
        w = self.target_width * (bead_size + CELL_SPACING) + CELL_SPACING
        h = self.target_height * (bead_size + CELL_SPACING) + CELL_SPACING
        TITLE_H = 40
        THUMB_MARGIN = 20
        THUMB_W = 160
        LABEL_MARGIN = bead_size + 10
        
        # 计算缩略图高度（保持比例）
        thumb_h = 0
        thumb_img = None
        if original_img_path and os.path.exists(original_img_path):
            thumb_img = Image.open(original_img_path).convert("RGB")
            ratio = THUMB_W / thumb_img.width
            thumb_h = int(thumb_img.height * ratio)
            thumb_img = thumb_img.resize((THUMB_W, thumb_h), Image.Resampling.LANCZOS)
        
        total_w = w + LABEL_MARGIN
        total_h = h + LABEL_MARGIN + TITLE_H + (thumb_h + THUMB_MARGIN * 2 if thumb_img else 0)
        
        img = Image.new("RGB", (total_w, total_h), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        # 字体
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 
                                       max(8, bead_size // 3))
            num_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 
                                           max(7, bead_size // 4))
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
            stat_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
        except:
            font = num_font = title_font = stat_font = ImageFont.load_default()
        
        # ── 标题栏 ──
        CONTENT_TOP = TITLE_H
        draw.rectangle([0, 0, total_w, TITLE_H], fill=(30, 30, 60))
        brand_name = self.palette.config["name"]
        bead_mm = self.palette.config["bead_size_mm"]
        title = f"拼豆施工图纸  |  {self.target_width}x{self.target_height}  |  {self.target_width*self.target_height:,}颗  |  {len(self.bom)}色  |  {brand_name} {bead_mm}mm"
        tw, _ = draw.textbbox((0, 0), title, font=title_font)[2:]
        draw.text(((total_w - tw) // 2, (TITLE_H - 18) // 2), title, fill=(255, 255, 255), font=title_font)
        
        # ── 格子颜色（色块 + 色号标注）──
        for y in range(self.target_height):
            for x in range(self.target_width):
                code = self.matched_grid[y, x]
                fr, fg, fb = self.matched_rgb[y, x]
                x0 = LABEL_MARGIN + x * (bead_size + CELL_SPACING) + CELL_SPACING
                y0 = CONTENT_TOP + LABEL_MARGIN + y * (bead_size + CELL_SPACING) + CELL_SPACING
                # 填色
                draw.rectangle(
                    [x0, y0, x0 + bead_size - 1, y0 + bead_size - 1],
                    fill=(int(fr), int(fg), int(fb))
                )
        
        # ── 网格线（画在色块上面，蓝色）──
        BLUE = (100, 140, 220)
        for x in range(self.target_width + 1):
            lx = LABEL_MARGIN + x * (bead_size + CELL_SPACING)
            draw.line(
                [(lx, CONTENT_TOP + LABEL_MARGIN), (lx, CONTENT_TOP + LABEL_MARGIN + h)],
                fill=BLUE, width=1
            )
        for y in range(self.target_height + 1):
            ly = CONTENT_TOP + LABEL_MARGIN + y * (bead_size + CELL_SPACING)
            draw.line(
                [(LABEL_MARGIN, ly), (LABEL_MARGIN + w, ly)],
                fill=BLUE, width=1
            )
        
        # ── 色号标注（画在网格线上面）──
        if show_labels and bead_size >= 12:
            for y in range(self.target_height):
                for x in range(self.target_width):
                    code = self.matched_grid[y, x]
                    fr, fg, fb = self.matched_rgb[y, x]
                    x0 = LABEL_MARGIN + x * (bead_size + CELL_SPACING) + CELL_SPACING
                    y0 = CONTENT_TOP + LABEL_MARGIN + y * (bead_size + CELL_SPACING) + CELL_SPACING
                    yiq = (int(fr) * 299 + int(fg) * 587 + int(fb) * 114) / 1000
                    tc = (0, 0, 0) if yiq >= 140 else (255, 255, 255)
                    bbox = draw.textbbox((0, 0), code, font=font)
                    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
                    tx = x0 + (bead_size - tw) // 2
                    ty = y0 + (bead_size - th) // 2 - 1
                    draw.text((tx, ty), code, fill=tc, font=font)
        
        # ── 行列编号 ──
        for y in range(self.target_height):
            cy = CONTENT_TOP + LABEL_MARGIN + y * (bead_size + CELL_SPACING) + CELL_SPACING + bead_size // 2
            ns = str(y + 1)
            nb = draw.textbbox((0, 0), ns, font=num_font)
            draw.text(
                (LABEL_MARGIN - 8 - (nb[2] - nb[0]), cy - (nb[3] - nb[1]) // 2),
                ns, fill=(60, 60, 60), font=num_font
            )
        for x in range(self.target_width):
            cx = LABEL_MARGIN + x * (bead_size + CELL_SPACING) + CELL_SPACING + bead_size // 2
            ns = str(x + 1)
            nb = draw.textbbox((0, 0), ns, font=num_font)
            draw.text(
                (cx - (nb[2] - nb[0]) // 2, CONTENT_TOP + LABEL_MARGIN - 8 - (nb[3] - nb[1])),
                ns, fill=(60, 60, 60), font=num_font
            )
        
        # ── 每10格粉色分隔线 ──
        for x in range(0, self.target_width + 1, 10):
            lx = LABEL_MARGIN + x * (bead_size + CELL_SPACING)
            draw.line(
                [(lx, CONTENT_TOP + LABEL_MARGIN), (lx, CONTENT_TOP + LABEL_MARGIN + h)],
                fill=(240, 160, 180), width=2
            )
        for y in range(0, self.target_height + 1, 10):
            ly = CONTENT_TOP + LABEL_MARGIN + y * (bead_size + CELL_SPACING)
            draw.line(
                [(LABEL_MARGIN, ly), (LABEL_MARGIN + w, ly)],
                fill=(240, 160, 180), width=2
            )
        
        # ── 原图缩略图（右下角）──
        if thumb_img:
            thumb_x = total_w - THUMB_W - THUMB_MARGIN
            thumb_y = total_h - thumb_h - THUMB_MARGIN
            # 白色带边框背景
            draw.rectangle(
                [thumb_x - 4, thumb_y - 4, thumb_x + THUMB_W + 4, thumb_y + thumb_h + 4],
                fill=(255, 255, 255), outline=(180, 180, 180), width=2
            )
            img.paste(thumb_img, (thumb_x, thumb_y))
            # 标签
            label = "📷 原图"
            lw, lh = draw.textbbox((0, 0), label, font=stat_font)[2:]
            draw.text((thumb_x + (THUMB_W - lw) // 2, thumb_y - lh - 6), label, fill=(100, 100, 100), font=stat_font)
        
        return img

    def generate_preview_image(self, bead_size=20):
        w, h = self.target_width * bead_size, self.target_height * bead_size
        img = Image.new("RGB", (w, h))
        draw = ImageDraw.Draw(img)
        for y in range(self.target_height):
            for x in range(self.target_width):
                r, g, b = self.matched_rgb[y, x]
                draw.rectangle([x*bead_size, y*bead_size, (x+1)*bead_size-1, (y+1)*bead_size-1], fill=(int(r), int(g), int(b)))
        return img

    def generate_bom_image(self, original_img_path=None):
        bom_sorted = sorted(self.bom.items(), key=lambda x: -x[1])
        total_beads = sum(self.bom.values())
        
        ROW_H = 28
        MARGIN = 30
        # 列宽: 色号 | 色块 | 数量 | 占比
        COL_W = [70, 44, 80, 130]
        TABLE_W = sum(COL_W)
        total_w = MARGIN + TABLE_W + MARGIN
        
        # 标题区 + 表格
        HEADER_H = 60
        table_rows = len(bom_sorted) + 1
        table_h = table_rows * ROW_H
        FOOTER_H = 45
        total_h = HEADER_H + table_h + FOOTER_H
        
        img = Image.new("RGB", (total_w, total_h), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
            header_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)
            cell_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
            mono_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 11)
            small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
        except:
            title_font = header_font = cell_font = mono_font = small_font = ImageFont.load_default()
        
        # ── 标题行：尺寸信息 ──
        brand_name = self.palette.config['name']
        bead_mm = self.palette.config['bead_size_mm']
        size_cm_w = self.target_width * bead_mm / 10
        size_cm_h = self.target_height * bead_mm / 10
        title = f"拼豆色号统计  |  {brand_name} · {bead_mm}mm  |  {self.target_width}×{self.target_height}  |  {total_beads:,}颗  |  {len(self.bom)}色  |  成品约 {size_cm_w:.1f}×{size_cm_h:.1f}cm"
        draw.text((MARGIN, 18), title, fill=(60, 60, 60), font=title_font)
        
        # 表头
        headers = ["色号", "色块", "数量", "占比"]
        col_x = [MARGIN]
        for cw in COL_W[:-1]:
            col_x.append(col_x[-1] + cw)
        
        TABLE_Y = HEADER_H
        draw.rectangle(
            [MARGIN, TABLE_Y, MARGIN + TABLE_W, TABLE_Y + ROW_H],
            fill=(245, 245, 245)
        )
        for i, h in enumerate(headers):
            draw.text((col_x[i], TABLE_Y + 7), h, fill=(100, 100, 100), font=header_font)
        
        # 分隔线
        draw.line(
            [(MARGIN, TABLE_Y + ROW_H), (MARGIN + TABLE_W, TABLE_Y + ROW_H)],
            fill=(220, 220, 220), width=1
        )
        
        # 数据行
        row_y = TABLE_Y + ROW_H
        for idx, (code, count) in enumerate(bom_sorted):
            if idx % 2 == 0:
                draw.rectangle(
                    [MARGIN, row_y, MARGIN + TABLE_W, row_y + ROW_H],
                    fill=(250, 251, 252)
                )
            
            # 色号
            draw.text((col_x[0], row_y + 6), code, fill=(30, 30, 30), font=mono_font)
            
            # 色块
            hex_c = self.palette.palette[code]
            rr, gg, bb = int(hex_c[1:3], 16), int(hex_c[3:5], 16), int(hex_c[5:7], 16)
            bx, by = col_x[1] + 2, row_y + 5
            draw.rectangle([bx, by, bx + 20, by + 18], fill=(rr, gg, bb), outline=(200, 200, 200), width=1)
            
            # 数量
            draw.text((col_x[2], row_y + 6), f"{count:,}", fill=(50, 50, 50), font=cell_font)
            
            # 占比
            pct = count / total_beads * 100
            pct_str = f"{pct:.1f}%"
            bar_x = col_x[3]
            bar_w = int(100 * pct / 100)
            draw.rectangle(
                [bar_x, row_y + 12, bar_x + bar_w, row_y + 19],
                fill=(60, 180, 75)
            )
            draw.text((bar_x + bar_w + 8, row_y + 6), pct_str, fill=(100, 100, 100), font=small_font)
            
            row_y += ROW_H
        
        # ── 底部合计 ──
        footer_y = row_y + 8
        draw.line(
            [(MARGIN, footer_y), (MARGIN + TABLE_W, footer_y)],
            fill=(220, 220, 220), width=1
        )
        draw.text((col_x[0], footer_y + 10), f"合计 {len(bom_sorted)} 色", fill=(30, 30, 30), font=header_font)
        draw.text((col_x[2], footer_y + 10), f"{total_beads:,}", fill=(30, 30, 30), font=header_font)
        draw.text((col_x[3], footer_y + 10), "100%", fill=(30, 30, 30), font=header_font)
        
        return img

    def export_pdf(self, output_path, pattern_img, preview_img, bom_img):
        def add_page(c, pil_img, title, page_width=180*mm):
            w, h = pil_img.size
            scale = page_width / w
            ph = h * scale + 40*mm
            c.setPageSize((page_width, ph))
            c.setFont("Helvetica-Bold", 14)
            c.drawString(10*mm, ph - 15*mm, title)
            tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
            pil_img.save(tmp.name)
            c.drawImage(tmp.name, 0, 10*mm, width=page_width, height=h*scale)
            c.showPage()
            tmp.close()
        c = canvas.Canvas(output_path)
        c.setPageSize((180*mm, 120*mm))
        c.setFont("Helvetica-Bold", 18)
        c.drawString(10*mm, 100*mm, f"{self.palette.config['name']} 拼豆施工图纸")
        c.setFont("Helvetica", 12)
        c.drawString(10*mm, 85*mm, f"图纸: {self.target_width}x{self.target_height} = {self.target_width*self.target_height:,}颗")
        c.drawString(10*mm, 75*mm, f"颜色: {len(self.bom)}种")
        c.drawString(10*mm, 65*mm, f"品牌: {self.palette.config['name']} ({self.palette.config['bead_size_mm']}mm)")
        c.drawString(10*mm, 55*mm, f"成品: 约 {self.target_width*0.5:.1f}x{self.target_height*0.5:.1f} cm")
        c.showPage()
        add_page(c, pattern_img, "1. 施工图纸（带色号标注）")
        add_page(c, preview_img, "2. 纯颜色预览图")
        add_page(c, bom_img, "3. BOM 物料清单")
        c.save()
        return output_path


def main():
    parser = argparse.ArgumentParser(description="拼豆图纸生成器")
    parser.add_argument("--input", "-i", required=True, help="输入图片路径")
    parser.add_argument("--output", "-o", default="./bead_output", help="输出目录")
    parser.add_argument("--brand", "-b", default="mard", choices=["mard", "artkal", "hama", "perler", "nabbi", "hex"])
    parser.add_argument("--width", "-w", type=int, default=48, help="拼豆板宽度格数")
    parser.add_argument("--bead-size", type=int, default=20, help="渲染单格像素大小")
    parser.add_argument("--no-labels", action="store_true", help="不显示色号文字")
    parser.add_argument("--max-colors", type=int, default=30, help="最大颜色数（默认30）")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"错误: 找不到图片 {args.input}")
        sys.exit(1)
    os.makedirs(args.output, exist_ok=True)

    print(f"\n[1/4] 加载 {args.brand.upper()} 色卡...")
    palette = BeadPalette(args.brand)
    print(f"       色卡共 {len(palette.palette)} 色")

    print(f"[2/4] 处理图片 (宽度={args.width}格)...")
    gen = BeadPatternGenerator(palette, target_width=args.width)
    gen.process(args.input, max_colors=args.max_colors)
    print(f"       网格: {gen.target_width}x{gen.target_height}")
    print(f"       总豆子: {gen.target_width*gen.target_height:,}")
    print(f"       使用颜色: {len(gen.bom)}种")

    print(f"[3/4] 生成图纸...")
    pattern = gen.generate_pattern_image(bead_size=args.bead_size, show_labels=not args.no_labels, original_img_path=args.input)
    preview = gen.generate_preview_image(bead_size=args.bead_size)
    bom = gen.generate_bom_image(original_img_path=args.input)
    pattern.save(os.path.join(args.output, f"pattern_{args.brand}_{args.width}.png"))
    preview.save(os.path.join(args.output, f"preview_{args.brand}_{args.width}.png"))
    bom.save(os.path.join(args.output, f"bom_{args.brand}_{args.width}.png"))

    print(f"[4/4] 导出PDF...")
    pdf_path = os.path.join(args.output, f"bead_{args.brand}_{args.width}.pdf")
    gen.export_pdf(pdf_path, pattern, preview, bom)
    print(f"\n✅ 完成! 输出目录: {args.output}")

if __name__ == "__main__":
    main()
