#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PI_DATABASE 聚酰亚胺数据管理平台 - 入口
基于 Streamlit + Corporate Trust 设计风格
板块: 首页 | 数据总览(配方/性能/表征三方联动) | NMR | 页面4-6 | PI_ASS链接
"""
import streamlit as st
from PIL import Image as PIL_Image
import os, sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))
sys.path.insert(0, str(_ROOT / "src"))

st.set_page_config(
    page_title="PI_DATABASE | 聚酰亚胺数据库",
    page_icon=PIL_Image.open("D:/icon/1.png"),
    layout="wide",
    initial_sidebar_state="expanded"
)

from modules.common import init_session_state, apply_styles
from modules.components import create_sidebar, create_top_right_controls
from modules.pages import (create_home_page, create_data_page, create_nmr_page,
                           create_placeholder_page, create_piass_page)
from i18n import get_page_key


def main():
    apply_styles()
    init_session_state()
    page = create_sidebar()
    lang = st.session_state.get("lang", "zh")
    st.session_state.page = page
    create_top_right_controls()
    page_key = get_page_key(page, lang)
    if page_key == "nav_home":
        create_home_page()
    elif page_key == "nav_data":
        create_data_page()
    elif page_key == "nav_nmr":
        create_nmr_page()
    elif page_key == "nav_page4":
        create_placeholder_page(4)
    elif page_key == "nav_page5":
        create_placeholder_page(5)
    elif page_key == "nav_page6":
        create_placeholder_page(6)
    elif page_key == "nav_piass":
        create_piass_page()


if __name__ == "__main__":
    main()
