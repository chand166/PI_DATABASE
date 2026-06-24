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

from .common import (_img_uri, Config, init_session_state,
    get_sample_recipe_data, get_sample_perf_data, get_sample_char_data, apply_styles)

# ==================== 首页 ====================
def create_home_page():
    lang = st.session_state.get("lang", "zh")

    # Hero Section
    st.markdown(
        '<div class="hero-card"><div class="hero-card-content">'
        '<div style="display:flex;align-items:center;gap:20px;margin-bottom:24px;">'
        '<div class="icon-container"><img src="' + _img_uri('data/logo.png') + '" style="width:24px;height:24px;border-radius:6px;object-fit:cover;"></div>'
        "<div>"
        '<div style="font-size:3rem;margin:0;line-height:1;font-weight:800;'
        'background:linear-gradient(135deg,#4F46E5 0%,#7C3AED 50%,#6366F1 100%);'
        '-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">PI_DATABASE</div>'
        f'<div style="color:#64748B;font-size:1.1rem;margin:8px 0 0 0;font-weight:500;">{t("app_full_name", lang)}</div>'
        "</div></div>"
        f'<div style="margin-bottom:24px;"><span class="badge-glow">✨ {t("powered_by_ai", lang)}</span></div>'
        '<div style="background:linear-gradient(135deg,rgba(79,70,229,0.05) 0%,rgba(124,58,237,0.05) 100%);'
        "border-radius:16px;padding:24px;border:1px solid rgba(79,70,229,0.1);\">"
        f'<div style="color:#0F172A;font-weight:600;margin-bottom:20px;font-size:1rem;">{t("home_core_capabilities", lang)}</div>'
        '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px;">'
        '<div style="text-align:center;padding:16px;background:rgba(255,255,255,0.5);border-radius:12px;">'
        '<div style="font-size:2.2rem;font-weight:800;background:linear-gradient(135deg,#4F46E5 0%,#6366F1 100%);'
        '-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">5+</div>'
        f'<div style="color:#64748B;font-size:0.85rem;font-weight:500;margin-top:4px;">{t("home_db_count", lang)}</div></div>'
        '<div style="text-align:center;padding:16px;background:rgba(255,255,255,0.5);border-radius:12px;">'
        '<div style="font-size:2.2rem;font-weight:800;background:linear-gradient(135deg,#7C3AED 0%,#A855F7 100%);'
        '-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">5+</div>'
        f'<div style="color:#64748B;font-size:0.85rem;font-weight:500;margin-top:4px;">{t("home_perf_count", lang)}</div></div>'
        '<div style="text-align:center;padding:16px;background:rgba(255,255,255,0.5);border-radius:12px;">'
        '<div style="font-size:2.2rem;font-weight:800;background:linear-gradient(135deg,#6366F1 0%,#8B5CF6 100%);'
        '-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">5+</div>'
        f'<div style="color:#64748B;font-size:0.85rem;font-weight:500;margin-top:4px;">{t("home_char_count", lang)}</div></div>'
        "</div></div></div></div>",
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Feature Cards
    st.markdown(f"<h2 style='text-align:center;margin-bottom:8px;'>{t('home_feature_title', lang)}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;color:#64748B;margin-bottom:32px;'>{t('home_feature_subtitle', lang)}</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    features = [
        ("📊", t("home_data_title", lang), t("home_data_desc", lang), "nav_data"),
        ("🧪", t("home_nmr_title", lang), t("home_nmr_desc", lang), "nav_nmr"),
    ]

    for i, (icon, title, desc, nav_key) in enumerate(features):
        with [col1, col2][i]:
            side = "left" if i == 0 else "right"
            st.markdown(f"""
            <div class="feature-card-{side}">
                <div class="card" style="position:relative;overflow:hidden;height:100%;">
                    <div style="position:absolute;top:0;left:0;width:100%;height:100px;
                         background:linear-gradient(135deg,#EEF2FF 0%,#E0E7FF 50%,#DDD6FE 100%);
                         opacity:0.3;"></div>
                    <div style="position:relative;z-index:1;">
                        <div class="icon-container" style="margin-bottom:20px;">
                            <span class="icon-gradient" style="font-size:24px;">{icon}</span>
                        </div>
                        <h3 style="color:#0F172A;margin:0 0 12px 0;font-size:1.2rem;">{title}</h3>
                        <p style="color:#64748B;font-size:0.9rem;line-height:1.6;margin:0;">{desc}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(t("home_enter_module", lang), key=f"home_enter_{i}", use_container_width=True):
                st.session_state.nav_radio = t(nav_key, lang)
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Stats Section
    st.markdown(f"<h2 style='text-align:center;margin-bottom:8px;'>{t('home_project_status', lang)}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;color:#64748B;margin-bottom:32px;'>{t('home_realtime_monitor', lang)}</p>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    rd = get_sample_recipe_data()
    pd_ = get_sample_perf_data()
    cd = get_sample_char_data()
    stats = [
        (len(rd), t("home_db_count", lang), "Records"),
        (len(pd_), t("home_perf_count", lang), "Records"),
        (len(cd), t("home_char_count", lang), "Images"),
        (7, t("home_nmr_tool", lang), "Modules"),
    ]

    for i, (count, label, type_) in enumerate(stats):
        with [col1, col2, col3, col4][i]:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{count}</div>
                <div class="stat-label">{label}</div>
                <div class="stat-type">{type_}</div>
            </div>
            """, unsafe_allow_html=True)


# ==================== 数据总览页面 ====================
def create_data_page():
    lang = st.session_state.get("lang", "zh")

    st.markdown(f"<h1 style='font-size:2rem !important;margin-bottom:0;'>{t('nav_data', lang)}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#64748B;margin-bottom:24px;'>{t('home_data_desc', lang)}</p>", unsafe_allow_html=True)

    # 初始化数据
    if st.session_state.recipe_data is None:
        st.session_state.recipe_data = get_sample_recipe_data()
    if st.session_state.perf_data is None:
        st.session_state.perf_data = get_sample_perf_data()
    if st.session_state.char_data is None:
        st.session_state.char_data = get_sample_char_data()

    # ========== 第一部分：配方表格 ==========
    st.markdown("<div class='section-header'><span class='section-badge'>01</span>"
                f"<h3>{t('data_recipe_title', lang)}</h3></div>", unsafe_allow_html=True)

    st.caption(t("data_recipe_hint", lang))
    st.session_state.selected_row = None

    recipe_df = st.session_state.recipe_data

    # 行/列切换按钮
    st.markdown('<div class="toolbar-btn">', unsafe_allow_html=True)
    tb1, tb2 = st.columns([0.06, 0.06])
    with tb1:
        if st.button("📋 行", key="r_row_toggle", use_container_width=True):
            st.session_state.r_show_row = not st.session_state.r_show_row
            st.rerun()
    with tb2:
        if st.button("📐 列", key="r_col_toggle", use_container_width=True):
            st.session_state.r_show_col = not st.session_state.r_show_col
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # 行操作展开 — 一行内
    if st.session_state.get("r_show_row"):
        with st.container():
            ra1, ra2, ra3, ra4 = st.columns([0.15, 0.15, 0.08, 0.08])
            with ra1:
                if st.button("⬆ 上方插入行", key="r_ins_top2", use_container_width=True):
                    new_row = pd.DataFrame({c: [""] for c in st.session_state.recipe_data.columns})
                    st.session_state.recipe_data = pd.concat([new_row, st.session_state.recipe_data], ignore_index=True)
                    st.rerun()
            with ra2:
                if st.button("⬇ 下方插入行", key="r_ins_bot2", use_container_width=True):
                    new_row = pd.DataFrame({c: [""] for c in st.session_state.recipe_data.columns})
                    st.session_state.recipe_data = pd.concat([st.session_state.recipe_data, new_row], ignore_index=True)
                    st.rerun()
            with ra3:
                del_r = st.number_input("", min_value=1, max_value=max(len(st.session_state.recipe_data), 1),
                                         value=1, key="r_del_idx2", label_visibility="collapsed")
            with ra4:
                if st.button("🗑", key="r_del_btn2", use_container_width=True):
                    ridx = int(del_r) - 1
                    if 0 <= ridx < len(st.session_state.recipe_data):
                        st.session_state.recipe_data = st.session_state.recipe_data.drop(ridx).reset_index(drop=True)
                        st.rerun()

    # 列操作展开 — 一行内
    if st.session_state.get("r_show_col"):
        with st.container():
            cb0, cb1, cb2, cb3, cb4 = st.columns([0.15, 0.13, 0.13, 0.15, 0.08])
            with cb0:
                sel_col = st.selectbox("", st.session_state.recipe_data.columns.tolist(),
                                        key="r_col_sel2", label_visibility="collapsed")
            with cb1:
                if st.button("📌 前面插列", key="r_col_b42", use_container_width=True):
                    col_idx = list(st.session_state.recipe_data.columns).index(sel_col) if sel_col in st.session_state.recipe_data.columns else 0
                    st.session_state.recipe_data.insert(col_idx, f"新列_{col_idx}", "")
                    st.rerun()
            with cb2:
                if st.button("📌 后面插列", key="r_col_af2", use_container_width=True):
                    col_idx = list(st.session_state.recipe_data.columns).index(sel_col) if sel_col in st.session_state.recipe_data.columns else 0
                    st.session_state.recipe_data.insert(col_idx + 1, f"新列_{col_idx+1}", "")
                    st.rerun()
            with cb3:
                new_nm = st.text_input("", value=sel_col, key="r_col_rn2", label_visibility="collapsed")
                if st.button("✏ 重命名", key="r_col_rnb2", use_container_width=True):
                    if new_nm.strip() and new_nm.strip() != sel_col:
                        st.session_state.recipe_data.rename(columns={sel_col: new_nm.strip()}, inplace=True)
                        st.rerun()
            with cb4:
                if len(st.session_state.recipe_data.columns) > 1:
                    if st.button("🗑 删列", key="r_col_del2", use_container_width=True):
                        st.session_state.recipe_data = st.session_state.recipe_data.drop(columns=[sel_col])
                        st.rerun()

    st.caption("📝 双击单元格编辑内容")
    edited_recipe = st.data_editor(
        st.session_state.recipe_data,
        key="recipe_editor",
        use_container_width=True,
        hide_index=False,
        num_rows="fixed",
        column_config={
            col: st.column_config.TextColumn(col) for col in st.session_state.recipe_data.columns
        }
    )
    if edited_recipe is not None:
        st.session_state.recipe_data = edited_recipe

    st.markdown("---")

    # ========== 第二部分：性能表格 ==========
    st.markdown("<div class='section-header'><span class='section-badge'>02</span>"
                f"<h3>{t('data_perf_title', lang)}</h3></div>", unsafe_allow_html=True)
    st.caption(t("data_perf_hint", lang))

    perf_df = st.session_state.perf_data
    if len(perf_df) != len(st.session_state.recipe_data):
        diff = len(st.session_state.recipe_data) - len(perf_df)
        if diff > 0:
            new_rows = pd.DataFrame({col: [""] * diff for col in perf_df.columns})
            perf_df = pd.concat([perf_df, new_rows], ignore_index=True)
        elif diff < 0:
            perf_df = perf_df.iloc[:len(st.session_state.recipe_data)].reset_index(drop=True)
        st.session_state.perf_data = perf_df

    # 行/列切换按钮
    st.markdown('<div class="toolbar-btn">', unsafe_allow_html=True)
    tb3, tb4 = st.columns([0.06, 0.06])
    with tb3:
        if st.button("📋 行", key="p_row_toggle", use_container_width=True):
            st.session_state.p_show_row = not st.session_state.p_show_row
            st.rerun()
    with tb4:
        if st.button("📐 列", key="p_col_toggle", use_container_width=True):
            st.session_state.p_show_col = not st.session_state.p_show_col
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # 行操作展开
    if st.session_state.get("p_show_row"):
        with st.container():
            pa1, pa2, pa3, pa4 = st.columns([0.15, 0.15, 0.08, 0.08])
            with pa1:
                if st.button("⬆ 上方插入行", key="p_ins_top2", use_container_width=True):
                    new_row = pd.DataFrame({c: [""] for c in st.session_state.perf_data.columns})
                    st.session_state.perf_data = pd.concat([new_row, st.session_state.perf_data], ignore_index=True)
                    st.rerun()
            with pa2:
                if st.button("⬇ 下方插入行", key="p_ins_bot2", use_container_width=True):
                    new_row = pd.DataFrame({c: [""] for c in st.session_state.perf_data.columns})
                    st.session_state.perf_data = pd.concat([st.session_state.perf_data, new_row], ignore_index=True)
                    st.rerun()
            with pa3:
                del_p = st.number_input("", min_value=1, max_value=max(len(st.session_state.perf_data), 1),
                                         value=1, key="p_del_idx2", label_visibility="collapsed")
            with pa4:
                if st.button("🗑", key="p_del_btn2", use_container_width=True):
                    ridx = int(del_p) - 1
                    if 0 <= ridx < len(st.session_state.perf_data):
                        st.session_state.perf_data = st.session_state.perf_data.drop(ridx).reset_index(drop=True)
                        st.rerun()

    # 列操作展开
    if st.session_state.get("p_show_col"):
        with st.container():
            pd0, pd1, pd2, pd3, pd4 = st.columns([0.15, 0.13, 0.13, 0.15, 0.08])
            with pd0:
                sel_col = st.selectbox("", st.session_state.perf_data.columns.tolist(),
                                        key="p_col_sel2", label_visibility="collapsed")
            with pd1:
                if st.button("📌 前面插列", key="p_col_b42", use_container_width=True):
                    col_idx = list(st.session_state.perf_data.columns).index(sel_col) if sel_col in st.session_state.perf_data.columns else 0
                    st.session_state.perf_data.insert(col_idx, f"新列_{col_idx}", "")
                    st.rerun()
            with pd2:
                if st.button("📌 后面插列", key="p_col_af2", use_container_width=True):
                    col_idx = list(st.session_state.perf_data.columns).index(sel_col) if sel_col in st.session_state.perf_data.columns else 0
                    st.session_state.perf_data.insert(col_idx + 1, f"新列_{col_idx+1}", "")
                    st.rerun()
            with pd3:
                new_nm = st.text_input("", value=sel_col, key="p_col_rn2", label_visibility="collapsed")
                if st.button("✏ 重命名", key="p_col_rnb2", use_container_width=True):
                    if new_nm.strip() and new_nm.strip() != sel_col:
                        st.session_state.perf_data.rename(columns={sel_col: new_nm.strip()}, inplace=True)
                        st.rerun()
            with pd4:
                if len(st.session_state.perf_data.columns) > 1:
                    if st.button("🗑 删列", key="p_col_del2", use_container_width=True):
                        st.session_state.perf_data = st.session_state.perf_data.drop(columns=[sel_col])
                        st.rerun()

    st.caption("📝 双击单元格编辑内容")
    edited_perf = st.data_editor(
        st.session_state.perf_data,
        key="perf_editor",
        use_container_width=True,
        hide_index=False,
        num_rows="fixed",
        column_config={
            col: st.column_config.TextColumn(col) for col in st.session_state.perf_data.columns
        }
    )
    if edited_perf is not None:
        st.session_state.perf_data = edited_perf

    st.markdown("---")

    # ========== 第三部分：表征表格 ==========
    st.markdown("<div class='section-header'><span class='section-badge'>03</span>"
                f"<h3>{t('data_char_title', lang)}</h3></div>", unsafe_allow_html=True)
    st.caption(t("data_char_hint", lang))

    char_df = st.session_state.char_data
    if len(char_df) != len(st.session_state.recipe_data):
        diff = len(st.session_state.recipe_data) - len(char_df)
        if diff > 0:
            new_rows = pd.DataFrame({col: [""] * diff for col in char_df.columns})
            char_df = pd.concat([char_df, new_rows], ignore_index=True)
        elif diff < 0:
            char_df = char_df.iloc[:len(st.session_state.recipe_data)].reset_index(drop=True)
        st.session_state.char_data = char_df

    st.caption("📝 双击单元格编辑内容")
    edited_char = st.data_editor(
        st.session_state.char_data,
        key="char_editor",
        use_container_width=True,
        hide_index=False,
        num_rows="fixed",
        column_config={
            col: st.column_config.TextColumn(col) for col in st.session_state.char_data.columns
        }
    )
    if edited_char is not None:
        st.session_state.char_data = edited_char

    st.markdown("<br>", unsafe_allow_html=True)


# ==================== NMR 占位 ====================
def create_nmr_page():
    lang = st.session_state.get("lang", "zh")
    st.markdown(f"<h1 style='font-size:2rem !important;'>{t('nmr_title', lang)}</h1>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown(f"""
    <div class="card" style="text-align:center;padding:80px 40px;">
        <div style="font-size:4rem;margin-bottom:20px;">🧪</div>
        <h3 style="color:#64748B;">{t('nmr_placeholder', lang)}</h3>
        <p style="color:#94A3B8;margin-top:12px;">
            NMR 数据处理、峰值标注、谱图可视化等功能即将上线
        </p>
    </div>
    """, unsafe_allow_html=True)


# ==================== 页面4-6 占位 ====================
def create_placeholder_page(page_num: int):
    lang = st.session_state.get("lang", "zh")
    title_key = f"nav_page{page_num}" if page_num <= 6 else "nav_page6"
    st.markdown(f"<h1 style='font-size:2rem !important;'>{t(title_key, lang)}</h1>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown(f"""
    <div class="card" style="text-align:center;padding:80px 40px;">
        <div style="font-size:4rem;margin-bottom:20px;">📋</div>
        <h3 style="color:#64748B;">{t('page_placeholder', lang)}</h3>
        <p style="color:#94A3B8;margin-top:12px;">
            后续功能开发中，敬请期待
        </p>
    </div>
    """, unsafe_allow_html=True)


# ==================== PI_ASS 链接页面 ====================
def create_piass_page():
    lang = st.session_state.get("lang", "zh")
    st.markdown(f"<h1 style='font-size:2rem !important;'>{t('piass_title', lang)}</h1>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown(f"""
    <div class="card" style="text-align:center;padding:60px 40px;">
        <div style="font-size:4rem;margin-bottom:20px;">🔗</div>
        <h3>{t('piass_title', lang)}</h3>
        <p style="color:#64748B;margin:16px 0 32px 0;">{t('piass_desc', lang)}</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(t("piass_go", lang), type="primary", use_container_width=True):
            js = "window.open('http://localhost:8002', '_blank')"
            st.markdown(f"<script>{js}</script>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;color:#94A3B8;font-size:0.9rem;'>"
                    f"{t('piass_new_tab', lang)}: "
                    f"<a href='{t('piass_url', lang)}' target='_blank'>{t('piass_url', lang)}</a></p>",
                    unsafe_allow_html=True)

        st.markdown("""
        <div style="margin-top:40px;background:#F8FAFC;border-radius:16px;padding:24px;
                    border:1px solid #E2E8F0;">
            <h4 style="color:#0F172A;margin-bottom:12px;">PI_ASS — 聚酰亚胺性能预测系统</h4>
            <p style="color:#64748B;font-size:0.9rem;">
                PI_ASS 是聚酰亚胺性能预测与高通量筛选系统，集成了文献评分、数据提取、
                SMILES 转化、描述符计算、模型训练和高通量筛选等功能模块。
                点击上方按钮即可直接跳转使用。
            </p>
        </div>
        """, unsafe_allow_html=True)