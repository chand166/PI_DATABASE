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


# ==================== 数据总览页面（三方联动） ====================
def _render_char_detail(lang: str):
    """表征详情新版面 — 点击表征项后整页跳转到此大图详情视图"""
    idx = st.session_state.char_detail_idx
    row = st.session_state.char_data.iloc[idx]
    # 返回按钮
    if st.button(f"← {t('data_char_back', lang)}", key="back_char_detail"):
        st.session_state.show_char_detail = False
        st.session_state.char_detail_idx = None
        st.rerun()
    st.markdown("---")
    # 详情标题
    st.markdown(
        f"<h2 style='font-size:1.6rem;font-weight:800;margin-bottom:8px;'>"
        f"🖼️ {row.get('样品名称', '')} · {row.get('表征类型', '')}</h2>", unsafe_allow_html=True)
    st.caption(t("data_char_detail_hint", lang))
    # 大图
    img_path = row.get("预览图路径")
    if pd.notna(img_path) and Path(str(img_path)).exists():
        st.image(str(img_path), use_container_width=True)
    else:
        st.info(t("data_char_no_image", lang))
    # 元数据卡片
    note = row.get("备注", "")
    st.markdown(f"""
    <div style="background:#F8FAFC;border-radius:12px;padding:20px;margin-top:16px;">
        <p style="color:#64748B;margin:0;"><strong>{t("data_recipe_col_name", lang)}:</strong> {row.get('样品名称', '')}</p>
        <p style="color:#64748B;margin:8px 0 0 0;"><strong>{t("data_char_col_type", lang)}:</strong> {row.get('表征类型', '')}</p>
        <p style="color:#64748B;margin:8px 0 0 0;"><strong>Path:</strong> {img_path or 'N/A'}</p>
        <p style="color:#64748B;margin:8px 0 0 0;"><strong>{t("data_char_note_label", lang)}:</strong> {note or ''}</p>
    </div>
    """, unsafe_allow_html=True)


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

    # ========== 表征详情新版面（点击表征项后整页跳转至此） ==========
    if st.session_state.get("show_char_detail") and st.session_state.char_detail_idx is not None:
        _render_char_detail(lang)
        return

    # ========== 第一部分：配方表格 ==========
    st.markdown("<div class='section-header'><span class='section-badge'>01</span>"
                f"<h3>{t('data_recipe_title', lang)}</h3></div>", unsafe_allow_html=True)

    # 提示
    st.caption(t("data_recipe_hint", lang))
    st.session_state.selected_row = None

    recipe_df = st.session_state.recipe_data

    # 行操作 + 列操作 — 紧凑工具栏
    st.markdown('<div class="toolbar-btn">', unsafe_allow_html=True)
    tb1, tb2, _ = st.columns([0.1, 0.1, 0.8])
    with tb1:
        active = "true" if st.session_state.get("r_show_row") else "false"
        if st.button("📋 行操作", key="r_row_toggle", use_container_width=True):
            st.session_state.r_show_row = not st.session_state.r_show_row
            st.rerun()
    with tb2:
        active = "true" if st.session_state.get("r_show_col") else "false"
        if st.button("📐 列操作", key="r_col_toggle", use_container_width=True):
            st.session_state.r_show_col = not st.session_state.r_show_col
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.get("r_show_row"):
        with st.container():
            ca1, ca2, ca3 = st.columns(3)
            with ca1:
                if st.button("⬆ 上方插入行", key="r_ins_top2", use_container_width=True):
                    new_row = pd.DataFrame({c: [""] for c in st.session_state.recipe_data.columns})
                    st.session_state.recipe_data = pd.concat([new_row, st.session_state.recipe_data], ignore_index=True)
                    st.rerun()
            with ca2:
                if st.button("⬇ 下方插入行", key="r_ins_bot2", use_container_width=True):
                    new_row = pd.DataFrame({c: [""] for c in st.session_state.recipe_data.columns})
                    st.session_state.recipe_data = pd.concat([st.session_state.recipe_data, new_row], ignore_index=True)
                    st.rerun()
            with ca3:
                del_r = st.number_input("删除行号", min_value=1, max_value=max(len(st.session_state.recipe_data), 1),
                                         value=1, key="r_del_idx2", label_visibility="collapsed")
                if st.button(f"🗑 删除第 {int(del_r)} 行", key="r_del_btn2", use_container_width=True):
                    ridx = int(del_r) - 1
                    if 0 <= ridx < len(st.session_state.recipe_data):
                        st.session_state.recipe_data = st.session_state.recipe_data.drop(ridx).reset_index(drop=True)
                        st.rerun()

    if st.session_state.get("r_show_col"):
        with st.container():
            sel_col = st.selectbox("选择列", st.session_state.recipe_data.columns.tolist(),
                                    key="r_col_sel2", label_visibility="collapsed")
            col_idx = list(st.session_state.recipe_data.columns).index(sel_col) if sel_col in st.session_state.recipe_data.columns else 0
            cb1, cb2, cb3, cb4 = st.columns(4)
            with cb1:
                if st.button("📌 前面插列", key="r_col_b42", use_container_width=True):
                    cols = st.session_state.recipe_data.columns.tolist()
                    st.session_state.recipe_data.insert(col_idx, f"新列_{col_idx}", "")
                    st.rerun()
            with cb2:
                if st.button("📌 后面插列", key="r_col_af2", use_container_width=True):
                    cols = st.session_state.recipe_data.columns.tolist()
                    st.session_state.recipe_data.insert(col_idx + 1, f"新列_{col_idx+1}", "")
                    st.rerun()
            with cb3:
                new_nm = st.text_input("重命名", value=sel_col, key="r_col_rn2", label_visibility="collapsed")
                if st.button("✏ 确定", key="r_col_rnb2", use_container_width=True):
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
    # 确保性能表格行数与配方一致（自动扩展/缩减）
    if len(perf_df) != len(st.session_state.recipe_data):
        diff = len(st.session_state.recipe_data) - len(perf_df)
        if diff > 0:
            new_rows = pd.DataFrame({col: [""] * diff for col in perf_df.columns})
            perf_df = pd.concat([perf_df, new_rows], ignore_index=True)
        elif diff < 0:
            perf_df = perf_df.iloc[:len(st.session_state.recipe_data)].reset_index(drop=True)
        st.session_state.perf_data = perf_df

    # 行操作 + 列操作 — 紧凑工具栏
    st.markdown('<div class="toolbar-btn">', unsafe_allow_html=True)
    tb3, tb4, _ = st.columns([0.1, 0.1, 0.8])
    with tb3:
        active = "true" if st.session_state.get("p_show_row") else "false"
        if st.button("📋 行操作", key="p_row_toggle", use_container_width=True):
            st.session_state.p_show_row = not st.session_state.p_show_row
            st.rerun()
    with tb4:
        active = "true" if st.session_state.get("p_show_col") else "false"
        if st.button("📐 列操作", key="p_col_toggle", use_container_width=True):
            st.session_state.p_show_col = not st.session_state.p_show_col
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.get("p_show_row"):
        with st.container():
            ca1, ca2, ca3 = st.columns(3)
            with ca1:
                if st.button("⬆ 上方插入行", key="p_ins_top2", use_container_width=True):
                    new_row = pd.DataFrame({c: [""] for c in st.session_state.perf_data.columns})
                    st.session_state.perf_data = pd.concat([new_row, st.session_state.perf_data], ignore_index=True)
                    st.rerun()
            with ca2:
                if st.button("⬇ 下方插入行", key="p_ins_bot2", use_container_width=True):
                    new_row = pd.DataFrame({c: [""] for c in st.session_state.perf_data.columns})
                    st.session_state.perf_data = pd.concat([st.session_state.perf_data, new_row], ignore_index=True)
                    st.rerun()
            with ca3:
                del_p = st.number_input("删除行号", min_value=1, max_value=max(len(st.session_state.perf_data), 1),
                                         value=1, key="p_del_idx2", label_visibility="collapsed")
                if st.button(f"🗑 删除第 {int(del_p)} 行", key="p_del_btn2", use_container_width=True):
                    ridx = int(del_p) - 1
                    if 0 <= ridx < len(st.session_state.perf_data):
                        st.session_state.perf_data = st.session_state.perf_data.drop(ridx).reset_index(drop=True)
                        st.rerun()

    if st.session_state.get("p_show_col"):
        with st.container():
            sel_col = st.selectbox("选择列", st.session_state.perf_data.columns.tolist(),
                                    key="p_col_sel2", label_visibility="collapsed")
            col_idx = list(st.session_state.perf_data.columns).index(sel_col) if sel_col in st.session_state.perf_data.columns else 0
            cb1, cb2, cb3, cb4 = st.columns(4)
            with cb1:
                if st.button("📌 前面插列", key="p_col_b42", use_container_width=True):
                    cols = st.session_state.perf_data.columns.tolist()
                    st.session_state.perf_data.insert(col_idx, f"新列_{col_idx}", "")
                    st.rerun()
            with cb2:
                if st.button("📌 后面插列", key="p_col_af2", use_container_width=True):
                    cols = st.session_state.perf_data.columns.tolist()
                    st.session_state.perf_data.insert(col_idx + 1, f"新列_{col_idx+1}", "")
                    st.rerun()
            with cb3:
                new_nm = st.text_input("重命名", value=sel_col, key="p_col_rn2", label_visibility="collapsed")
                if st.button("✏ 确定", key="p_col_rnb2", use_container_width=True):
                    if new_nm.strip() and new_nm.strip() != sel_col:
                        st.session_state.perf_data.rename(columns={sel_col: new_nm.strip()}, inplace=True)
                        st.rerun()
            with cb4:
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
            col: st.column_config.NumberColumn(col) if any(k in col for k in ["Tg", "Td", "介电", "拉伸", "断裂"])
            else st.column_config.TextColumn(col)
            for col in st.session_state.perf_data.columns
        }
    )
    if edited_perf is not None:
        st.session_state.perf_data = edited_perf

    st.markdown("---")

    # ========== 第三部分：表征图表 ==========
    st.markdown("<div class='section-header'><span class='section-badge'>03</span>"
                f"<h3>{t('data_char_title', lang)}</h3></div>", unsafe_allow_html=True)
    st.caption(t("data_char_hint", lang))

    char_df = st.session_state.char_data
    # 确保表征表格行数与配方一致
    if len(char_df) != len(st.session_state.recipe_data):
        diff = len(st.session_state.recipe_data) - len(char_df)
        if diff > 0:
            new_rows = pd.DataFrame({col: [""] * diff for col in char_df.columns})
            char_df = pd.concat([char_df, new_rows], ignore_index=True)
        elif diff < 0:
            char_df = char_df.iloc[:len(st.session_state.recipe_data)].reset_index(drop=True)
        char_df["预览图路径"] = char_df.get("预览图路径", [None] * len(char_df))
        char_df["备注"] = char_df.get("备注", [""] * len(char_df))
        st.session_state.char_data = char_df

    # 显示表征 — 按样品名称分组折叠
    char_df = st.session_state.char_data

    # 联动已删除，所有 expander 默认折叠
    for sample_name in char_df["样品名称"].unique():
        group = char_df[char_df["样品名称"] == sample_name]
        with st.expander(f"📁 {sample_name} ({len(group)} 项表征)", expanded=False):
            for idx, row in group.iterrows():
                c1, c2, c3, c4 = st.columns([1, 0.5, 2.5, 1])
                with c1:
                    st.markdown(f"<div class='char-card' style='padding:12px;'>"
                                f"<strong style='color:#0F172A;'>{row.get('表征类型', '')}</strong></div>",
                                unsafe_allow_html=True)
                with c2:
                    img_path = row.get("预览图路径")
                    if pd.notna(img_path) and Path(str(img_path)).exists():
                        st.image(img_path, width=120)
                    else:
                        st.markdown(f"<div class='char-card' style='padding:16px;'>"
                                    f"<span style='color:#CBD5E1;font-size:0.85rem;'>{t('data_char_no_image', lang)}</span></div>",
                                    unsafe_allow_html=True)
                with c3:
                    # 可编辑备注字段
                    note_key = f"char_note_{idx}"
                    current_note = st.session_state.char_data.at[idx, "备注"] if "备注" in st.session_state.char_data.columns else ""
                    new_note = st.text_input("备注", value=current_note, key=note_key, label_visibility="collapsed",
                                              placeholder="添加备注...")
                    if new_note != current_note:
                        st.session_state.char_data.at[idx, "备注"] = new_note
                with c4:
                    if st.button(f"🔍 详情", key=f"char_detail_{idx}"):
                        st.session_state.show_char_detail = True
                        st.session_state.char_detail_idx = idx
                        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
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
        # 用按钮跳转
        if st.button(t("piass_go", lang), type="primary", use_container_width=True):
            # 直接在同标签页导航到 PI_ASS
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