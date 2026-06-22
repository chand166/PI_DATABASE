import os, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
_SRC = os.path.dirname(_HERE)
_ROOT = os.path.dirname(_SRC)
for _p in (_SRC, _ROOT):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import webbrowser
from PIL import Image as PIL_Image
from i18n import t, get_page_names, get_page_key

from .common import _img_uri

# ==================== 顶部控制栏 ====================
def create_top_right_controls():
    lang = st.session_state.get("lang", "zh")
    lang_btn_text = "English" if lang == "zh" else "中文"

    st.markdown("""
    <style>
    div[data-testid="element-container"]:has(> div.st-key-top_ctrl) {
        position: fixed; top: 6px; right: 140px; z-index: 999;
    }
    div.st-key-top_ctrl button {
        display: inline-flex !important; align-items: center;
        padding: 0 12px !important; border-radius: 8px !important;
        min-height: 28px !important; border: none !important;
        background: transparent !important;
        color: rgb(49, 51, 63) !important;
        font-size: 14px !important; line-height: 28px !important;
        cursor: pointer; white-space: nowrap;
    }
    div.st-key-top_ctrl button:hover { background: rgba(49, 51, 63, 0.04) !important; }
    div.st-key-top_ctrl [data-testid="column"] { flex: none !important; width: auto !important; }
    </style>
    """, unsafe_allow_html=True)

    with st.container(key="top_ctrl"):
        c1, _ = st.columns([0.08, 0.92])
        with c1:
            if st.button(lang_btn_text, key="top_lang_btn"):
                st.session_state.lang = "en" if lang == "zh" else "zh"
                st.rerun()

# ==================== 侧边栏 ====================
def create_sidebar():
    lang = st.session_state.get("lang", "zh")

    # Logo 区域
    st.sidebar.markdown(f"""
    <div style="padding: 20px 0; text-align: center;">
        <div style="
            background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
            width: 60px; height: 60px; border-radius: 16px;
            display: inline-flex; align-items: center; justify-content: center;
            box-shadow: 0 8px 30px rgba(79, 70, 229, 0.3);
            margin-bottom: 12px;">
            <img src="{_img_uri('data/logo.png')}" style="width:32px;height:32px;border-radius:6px;object-fit:cover;">
        </div>
        <h2 style="margin: 0; font-size: 1.5rem; font-weight: 800;
                   background: linear-gradient(135deg, #0F172A 0%, #4F46E5 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   background-clip: text;">
            PI_DATABASE
        </h2>
        <p style="color: #64748B; font-size: 0.8rem; margin-top: 4px;">
            {t('app_subtitle', lang)}
        </p>
    </div>
    <hr style="border: none; height: 1px; background: linear-gradient(90deg, transparent, #E2E8F0, transparent); margin: 16px 0;">
    """, unsafe_allow_html=True)

    # 导航
    pages = get_page_names(lang)
    page = st.sidebar.radio(
        t("sidebar_title", lang), pages,
        key="nav_radio", label_visibility="collapsed"
    )

    # 底部信息
    st.sidebar.markdown("""
    <div style="position: fixed; bottom: 20px; left: 20px; right: 20px;
                background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
                border: 1px solid #E2E8F0; border-radius: 12px;
                padding: 12px 16px; text-align: center;">
        <div style="color: #64748B; font-size: 0.75rem;">PI_DATABASE v1.0</div>
        <div style="color: #94A3B8; font-size: 0.7rem; margin-top: 2px;">Data Management Platform</div>
    </div>
    """, unsafe_allow_html=True)

    return page

