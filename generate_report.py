# -*- coding: utf-8 -*-
"""
SkinCare AI - Project Documentation Generator
Creates:
  1. Skin_Disease_Prediction_Documentation.docx
  2. Skin_Disease_Prediction_Documentation.md
Formatted with:
  - Times New Roman font
  - Line spacing 1.5
  - Header: SKIN DISEASE PREDICTION
  - Footer: Department of Computer Applications, MBITS (with page numbers)
  - Layout matching MBITS MCA Mini Project Report format
"""

import os
import shutil
import zipfile
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DOCX = r"C:\Users\admin\.gemini\antigravity\brain\0b726e94-6136-4f3b-ae99-8470a37f274a\.user_uploaded\media_1792145423257_40e0a91d.docx"
ASSETS_DIR = os.path.join(BASE_DIR, "report_assets")
OUTPUT_DOCX = os.path.join(BASE_DIR, "Skin_Disease_Prediction_Documentation.docx")
OUTPUT_MD = os.path.join(BASE_DIR, "Skin_Disease_Prediction_Documentation.md")

print("Initializing Documentation Generator...")
