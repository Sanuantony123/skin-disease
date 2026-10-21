# -*- coding: utf-8 -*-
"""
XML Helpers for OpenXML WordprocessingML Generation
"""

from xml.sax.saxutils import escape

def p(text="", style="Normal", align="both", bold=False, italic=False, size=24, space_before=0, space_after=120, line_spacing=360):
    text_xml = escape(str(text))
    bold_tag = "<w:b/>" if bold else ""
    italic_tag = "<w:i/>" if italic else ""
    return (
        f'<w:p>'
        f'<w:pPr>'
        f'<w:pStyle w:val="{style}"/>'
        f'<w:jc w:val="{align}"/>'
        f'<w:spacing w:line="{line_spacing}" w:lineRule="auto" w:before="{space_before}" w:after="{space_after}"/>'
        f'<w:rPr>'
        f'<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
        f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
        f'{bold_tag}{italic_tag}'
        f'</w:rPr>'
        f'</w:pPr>'
        f'<w:r>'
        f'<w:rPr>'
        f'<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
        f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
        f'{bold_tag}{italic_tag}'
        f'</w:rPr>'
        f'<w:t xml:space="preserve">{text_xml}</w:t>'
        f'</w:r>'
        f'</w:p>'
    )

def p_multi_runs(runs, align="both", space_before=0, space_after=120, line_spacing=360):
    runs_xml = ""
    for run in runs:
        text = escape(str(run.get("text", "")))
        bold = "<w:b/>" if run.get("bold", False) else ""
        italic = "<w:i/>" if run.get("italic", False) else ""
        size = run.get("size", 24)
        font = run.get("font", "Times New Roman")
        color = f'<w:color w:val="{run.get("color")}"/>' if run.get("color") else ""
        runs_xml += (
            f'<w:r>'
            f'<w:rPr>'
            f'<w:rFonts w:ascii="{font}" w:hAnsi="{font}" w:cs="{font}"/>'
            f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
            f'{bold}{italic}{color}'
            f'</w:rPr>'
            f'<w:t xml:space="preserve">{text}</w:t>'
            f'</w:r>'
        )
    return (
        f'<w:p>'
        f'<w:pPr>'
        f'<w:jc w:val="{align}"/>'
        f'<w:spacing w:line="{line_spacing}" w:lineRule="auto" w:before="{space_before}" w:after="{space_after}"/>'
        f'</w:pPr>'
        f'{runs_xml}'
        f'</w:p>'
    )

def h1(text, align="center"):
    return p(text, style="Heading1", align=align, bold=True, size=32, space_before=240, space_after=120)

def h2(text, align="left"):
    return p(text, style="Heading2", align=align, bold=True, size=28, space_before=180, space_after=90)

def h3(text, align="left"):
    return p(text, style="Heading3", align=align, bold=True, size=24, space_before=140, space_after=60)

def page_break():
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'

def section_break(header_id=None, footer_id=None, start_page_num=None):
    hdr_xml = f'<w:headerReference w:type="default" r:id="{header_id}"/>' if header_id else ""
    ftr_xml = f'<w:footerReference w:type="default" r:id="{footer_id}"/>' if footer_id else ""
    pgnum_xml = f'<w:pgNumType w:start="{start_page_num}"/>' if start_page_num is not None else ""
    return (
        f'<w:p>'
        f'<w:pPr>'
        f'<w:sectPr>'
        f'{hdr_xml}'
        f'{ftr_xml}'
        f'<w:pgSz w:w="11910" w:h="16840"/>'
        f'<w:pgMar w:top="1580" w:right="740" w:bottom="1820" w:left="740" w:header="749" w:footer="1627" w:gutter="0"/>'
        f'{pgnum_xml}'
        f'<w:cols w:space="720"/>'
        f'</w:sectPr>'
        f'</w:pPr>'
        f'</w:p>'
    )

def img_inline(r_id, cx, cy, name="Picture", caption=""):
    img_xml = (
        f'<w:p>'
        f'<w:pPr><w:jc w:val="center"/><w:spacing w:line="240" w:before="120" w:after="60"/></w:pPr>'
        f'<w:r>'
        f'<w:drawing>'
        f'<wp:inline distT="0" distB="0" distL="0" distR="0">'
        f'<wp:extent cx="{cx}" cy="{cy}"/>'
        f'<wp:docPr id="100" name="{name}"/>'
        f'<wp:cNvGraphicFramePr>'
        f'<a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>'
        f'</wp:cNvGraphicFramePr>'
        f'<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        f'<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        f'<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        f'<pic:nvPicPr>'
        f'<pic:cNvPr id="0" name="{name}"/>'
        f'<pic:cNvPicPr><a:picLocks noChangeAspect="1" noChangeArrowheads="1"/></pic:cNvPicPr>'
        f'</pic:nvPicPr>'
        f'<pic:blipFill>'
        f'<a:blip r:embed="{r_id}" cstate="print"/>'
        f'<a:stretch><a:fillRect/></a:stretch>'
        f'</pic:blipFill>'
        f'<pic:spPr>'
        f'<a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
        f'<a:noFill/><a:ln><a:noFill/></a:ln>'
        f'</pic:spPr>'
        f'</pic:pic>'
        f'</a:graphicData>'
        f'</a:graphic>'
        f'</wp:inline>'
        f'</w:drawing>'
        f'</w:r>'
        f'</w:p>'
    )
    if caption:
        img_xml += p(caption, style="Normal", align="center", italic=True, size=20, space_before=40, space_after=120)
    return img_xml

def tbl(headers, rows, col_widths=None):
    total_w = 9500
    if not col_widths:
        w_per_col = int(total_w / len(headers))
        col_widths = [w_per_col] * len(headers)

    tbl_xml = (
        f'<w:tbl>'
        f'<w:tblPr>'
        f'<w:tblW w:w="{total_w}" w:type="dxa"/>'
        f'<w:jc w:val="center"/>'
        f'<w:tblBorders>'
        f'<w:top w:val="single" w:sz="8" w:space="0" w:color="2B5C8F"/>'
        f'<w:left w:val="none"/>'
        f'<w:bottom w:val="single" w:sz="8" w:space="0" w:color="2B5C8F"/>'
        f'<w:right w:val="none"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="D0D7DE"/>'
        f'<w:insideV w:val="none"/>'
        f'</w:tblBorders>'
        f'</w:tblPr>'
    )

    # Header Row
    tbl_xml += '<w:tr><w:trPr><w:tblHeader/></w:trPr>'
    for idx, h_text in enumerate(headers):
        c_w = col_widths[idx]
        tbl_xml += (
            f'<w:tc>'
            f'<w:tcPr>'
            f'<w:tcW w:w="{c_w}" w:type="dxa"/>'
            f'<w:shd w:val="clear" w:color="auto" w:fill="2B5C8F"/>'
            f'<w:tcMar><w:top w:w="120" w:type="dxa"/><w:bottom w:w="120" w:type="dxa"/><w:left w:w="140" w:type="dxa"/><w:right w:w="140" w:type="dxa"/></w:tcMar>'
            f'</w:tcPr>'
            f'<w:p><w:pPr><w:jc w:val="left"/><w:spacing w:line="240" w:before="60" w:after="60"/></w:pPr>'
            f'<w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:color w:val="FFFFFF"/><w:sz w:val="22"/></w:rPr>'
            f'<w:t>{escape(str(h_text))}</w:t></w:r></w:p>'
            f'</w:tc>'
        )
    tbl_xml += '</w:tr>'

    # Body Rows
    for r_idx, row in enumerate(rows):
        bg_fill = "F4F6F9" if r_idx % 2 == 1 else "FFFFFF"
        tbl_xml += '<w:tr>'
        for c_idx, cell_text in enumerate(row):
            c_w = col_widths[c_idx] if c_idx < len(col_widths) else 1500
            tbl_xml += (
                f'<w:tc>'
                f'<w:tcPr>'
                f'<w:tcW w:w="{c_w}" w:type="dxa"/>'
                f'<w:shd w:val="clear" w:color="auto" w:fill="{bg_fill}"/>'
                f'<w:tcMar><w:top w:w="100" w:type="dxa"/><w:bottom w:w="100" w:type="dxa"/><w:left w:w="140" w:type="dxa"/><w:right w:w="140" w:type="dxa"/></w:tcMar>'
                f'</w:tcPr>'
                f'<w:p><w:pPr><w:jc w:val="left"/><w:spacing w:line="260" w:before="40" w:after="40"/></w:pPr>'
                f'<w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="20"/></w:rPr>'
                f'<w:t>{escape(str(cell_text))}</w:t></w:r></w:p>'
                f'</w:tc>'
            )
        tbl_xml += '</w:tr>'
    tbl_xml += '</w:tbl>'
    return tbl_xml

def code_box(code_lines):
    box_xml = ""
    for line in code_lines:
        box_xml += (
            f'<w:p>'
            f'<w:pPr>'
            f'<w:spacing w:line="240" w:before="0" w:after="20"/>'
            f'<w:shd w:val="clear" w:color="auto" w:fill="F8F9FA"/>'
            f'<w:ind w:left="360" w:right="360"/>'
            f'</w:pPr>'
            f'<w:r>'
            f'<w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/><w:sz w:val="18"/><w:szCs w:val="18"/><w:color w:val="24292E"/></w:rPr>'
            f'<w:t xml:space="preserve">{escape(line)}</w:t>'
            f'</w:r>'
            f'</w:p>'
        )
    return box_xml
