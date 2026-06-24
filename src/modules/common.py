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

# ==================== 配置 ====================
class Config:
    BASE_DIR = Path("D:/PI_DATABASE")
    DATA_DIR = BASE_DIR / "data"
    CHAR_DIR = BASE_DIR / "data" / "characterization"
    for d in [BASE_DIR, DATA_DIR, CHAR_DIR]:
        d.mkdir(parents=True, exist_ok=True)

    # 图标路径
    ICON1 = Path("D:/icon/1.png")
    ICON2 = Path("D:/icon/2.jpg")


# ==================== 会话状态初始化 ====================
# ==================== 图片辅助 ====================
@st.cache_data
def _img_uri(rel_path: str) -> str:
    """读取图片文件返回 data URI（用于 HTML img src），避免内嵌 base64 撑大源码"""
    import base64 as _b64
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    with open(os.path.join(base_dir, rel_path), "rb") as _f:
        return "data:image/png;base64," + _b64.b64encode(_f.read()).decode()



def init_session_state():
    defaults = {
        "lang": "zh",
                "page_idx": 0,
                "selected_row": None,
                "recipe_data": None,   # 配方表格数据
                "perf_data": None,     # 性能表格数据
                "char_data": None,     # 表征数据
                "r_show_row": False,
                "r_show_col": False,
                "p_show_row": False,
                "p_show_col": False,
            }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ==================== 示例数据 ====================
def get_sample_recipe_data():
    """生成空白配方数据 — 8列"""
    return pd.DataFrame({f"列{i}": [""] * 5 for i in range(1, 9)})

def get_sample_perf_data():
    """生成空白性能数据 — 8列"""
    return pd.DataFrame({f"列{i}": [""] * 5 for i in range(1, 9)})

def get_sample_char_data():
    """生成空白表征数据 — 8列"""
    return pd.DataFrame({f"列{i}": [""] * 5 for i in range(1, 9)})


def apply_styles():
    """应用 Corporate Trust CSS 样式"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        .stApp {
            background: linear-gradient(180deg, #F8FAFC 0%, #F1F5F9 100%);
            font-family: 'Plus Jakarta Sans', 'Segoe UI', 'PingFang SC', sans-serif;
        }

        [data-testid="stSidebar"] {
            background: rgba(255, 255, 255, 0.95);
            border-right: 1px solid rgba(79, 70, 229, 0.1);
            backdrop-filter: blur(20px);
        }

        [data-testid="stSidebar"] .stRadio > div { gap: 4px; }
        [data-testid="stSidebar"] .stRadio label {
            padding: 12px 16px;
            border-radius: 12px;
            transition: all 0.2s ease;
            margin: 2px 0;
        }
        [data-testid="stSidebar"] .stRadio label:hover {
            background: rgba(79, 70, 229, 0.08);
        }
        [data-testid="stSidebar"] .stRadio label:has(input:checked) {
            background: linear-gradient(135deg, rgba(79, 70, 229, 0.10) 0%, rgba(124, 58, 237, 0.08) 50%, rgba(139, 92, 246, 0.06) 100%);
            box-shadow: 0 2px 8px rgba(79, 70, 229, 0.12), inset 0 0 0 1px rgba(79, 70, 229, 0.15);
        }
        [data-testid="stSidebar"] .stRadio label:has(input:checked) > div {
            color: #4F46E5;
            font-weight: 600;
        }
        [data-testid="stSidebar"] .stRadio label input[type="radio"] {
            accent-color: #4F46E5;
        }

        h1 {
            background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #6366F1 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 800 !important;
            font-size: 3rem !important;
            letter-spacing: -0.02em;
            line-height: 1.1 !important;
        }

        h2 { color: #0F172A !important; font-weight: 700 !important; font-size: 1.75rem !important; letter-spacing: -0.01em; }
        h3 { color: #1E293B !important; font-weight: 600 !important; font-size: 1.25rem !important; }

        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-weight: 600;
            font-size: 0.95rem;
            padding: 14px 32px;
            box-shadow: 0 4px 14px rgba(79, 70, 229, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.1) inset;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        .stButton > button[kind="primary"]::before {
            content: '';
            position: absolute;
            top: 0; left: -100%;
            width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }
        .stButton > button[kind="primary"]:hover::before { left: 100%; }
        .stButton > button[kind="primary"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(79, 70, 229, 0.4), 0 0 0 1px rgba(255, 255, 255, 0.1) inset;
        }
        .stButton > button:not([kind="primary"]) {
            background: rgba(255, 255, 255, 0.8);
            color: #4F46E5;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            font-weight: 500;
            transition: all 0.2s;
            backdrop-filter: blur(10px);
        }
        .stButton > button:not([kind="primary"]):hover {
            background: rgba(79, 70, 229, 0.05);
            border-color: #4F46E5;
            color: #4F46E5;
        }

        .card {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 20px;
            padding: 28px;
            box-shadow: 0 4px 20px rgba(79, 70, 229, 0.08), 0 1px 3px rgba(0, 0, 0, 0.05);
            margin: 16px 0;
            border: 1px solid rgba(79, 70, 229, 0.08);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            backdrop-filter: blur(10px);
        }
        .card:hover {
            box-shadow: 0 12px 40px rgba(79, 70, 229, 0.15), 0 4px 12px rgba(0, 0, 0, 0.05);
            transform: translateY(-4px);
            border-color: rgba(79, 70, 229, 0.15);
        }

        .hero-card { perspective: 2000px; margin: 24px 0; }
        .hero-card-content {
            background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.9) 100%);
            border-radius: 24px;
            padding: 40px;
            border: 1px solid rgba(79, 70, 229, 0.1);
            box-shadow: 0 20px 60px rgba(79, 70, 229, 0.15), 0 0 0 1px rgba(255, 255, 255, 0.5) inset;
            transform: rotateX(3deg) rotateY(-8deg);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            backdrop-filter: blur(20px);
            position: relative;
            overflow: hidden;
        }
        .hero-card-content::before {
            content: '';
            position: absolute;
            top: -50%; left: -50%;
            width: 200%; height: 200%;
            background: radial-gradient(circle, rgba(79, 70, 229, 0.03) 0%, transparent 70%);
            pointer-events: none;
        }
        .hero-card:hover .hero-card-content {
            transform: rotateX(1deg) rotateY(-4deg) translateY(-8px);
            box-shadow: 0 30px 80px rgba(79, 70, 229, 0.2);
        }

        .feature-card-left { transform: perspective(1000px) rotateY(3deg); transition: all 0.4s; }
        .feature-card-right { transform: perspective(1000px) rotateY(-3deg); transition: all 0.4s; }
        .feature-card-left:hover, .feature-card-right:hover {
            transform: perspective(1000px) rotateY(0deg) translateY(-6px);
        }

        .icon-container {
                            background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 50%, #DDD6FE 100%);
                            border-radius: 12px; padding: 8px;
                            display: inline-flex; align-items: center; justify-content: center;
                            width: 40px; height: 40px;
                            box-shadow: 0 3px 12px rgba(79, 70, 229, 0.18), 0 0 0 1px rgba(255, 255, 255, 0.5) inset;
                        }

                        .icon-gradient {
                            font-size: 20px;
                            line-height: 1;
                        }

        .stat-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 28px 24px;
            border: 1px solid rgba(79, 70, 229, 0.08);
            text-align: center;
            transition: all 0.3s;
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
        }
        .stat-card::before {
            content: '';
            position: absolute; top: 0; left: 0; right: 0; height: 3px;
            background: linear-gradient(90deg, #4F46E5, #7C3AED, #6366F1);
            opacity: 0; transition: opacity 0.3s;
        }
        .stat-card:hover::before { opacity: 1; }
        .stat-card:hover { transform: translateY(-6px); box-shadow: 0 12px 40px rgba(79, 70, 229, 0.15); }
        .stat-number {
            font-size: 2.8rem; font-weight: 800;
            background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            background-clip: text; line-height: 1; letter-spacing: -0.02em;
        }
        .stat-label { color: #64748B; font-weight: 600; font-size: 0.9rem; margin-top: 12px; text-transform: uppercase; letter-spacing: 0.05em; }

        .badge-glow {
            background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
            color: white; padding: 8px 16px; border-radius: 999px;
            font-weight: 600; font-size: 0.75rem;
            box-shadow: 0 0 20px rgba(79, 70, 229, 0.4), 0 4px 10px rgba(79, 70, 229, 0.2);
            display: inline-block; letter-spacing: 0.02em;
        }

        .stTextInput > div > div > input, .stTextArea > div > div > textarea,
        .stSelectbox > div > div > div {
            background: rgba(255, 255, 255, 0.9) !important;
            border: 1.5px solid #E2E8F0 !important;
            border-radius: 12px !important;
            transition: all 0.2s;
            font-size: 0.95rem;
            outline: none !important;
            box-shadow: none !important;
        }
        .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
            border-color: #4F46E5 !important;
        }
        .stTextInput div, .stTextArea div,
        .stTextInput [data-testid], .stTextArea [data-testid] {
            outline: none !important;
            box-shadow: none !important;
            border: none !important;
        }
        /* 备注输入框 - 紧凑样式 */
        div.st-key-char_note input {
            font-size: 0.8rem !important;
            padding: 2px 6px !important;
            min-height: 26px !important;
        }

        .stDataFrame {
            border-radius: 16px;
            border: 1px solid rgba(79, 70, 229, 0.08);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
            overflow: hidden;
        }
        .stDataFrame th {
            background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
            font-weight: 600; color: #0F172A;
            border-bottom: 2px solid #E2E8F0;
        }

        .stDataEditor {
                    border-radius: 16px;
                    border: 1px solid rgba(79, 70, 229, 0.08);
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
                    overflow: hidden;
                }

                /* 隐藏 data_editor 内部自动生成的 ⋮ 行操作 popover（固定在表头下方的那种），不误伤 toolbar */
                        [data-testid="stDataFrameResizer"] [data-testid="stPopoverButton"],
                        [data-testid="stDataFrame"] [data-testid="stPopoverButton"] { display: none !important; }

                /* 数据区 section 标题栏 */
                .section-header {
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    padding: 12px 0 4px 0;
                }
                .section-header h3 {
                    margin: 0;
                    font-size: 1.15rem !important;
                }
                .section-badge {
                    background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%);
                    color: #4F46E5;
                    font-size: 0.7rem;
                    font-weight: 700;
                    padding: 2px 10px;
                    border-radius: 999px;
                    letter-spacing: 0.04em;
                }
                .section-divider {
                    border: none;
                    height: 1px;
                    background: linear-gradient(90deg, transparent 5%, #E2E8F0 50%, transparent 95%);
                    margin: 32px 0;
                }
                .data-editor-wrap {
                    background: rgba(255, 255, 255, 0.6);
                    border-radius: 16px;
                    padding: 4px 0 0 0;
                    margin: 8px 0;
                }

                .stProgress > div > div > div {
            background: linear-gradient(90deg, #4F46E5, #6366F1, #7C3AED, #4F46E5) !important;
            background-size: 200% 100% !important;
            animation: gradient-shift 2s linear infinite;
            border-radius: 999px;
        }
        @keyframes gradient-shift {
            0% { background-position: 0% 50%; }
            100% { background-position: 200% 50%; }
        }

        hr { border: none; height: 1px; background: linear-gradient(90deg, transparent, #E2E8F0, transparent); margin: 32px 0; }

        .stExpander {
            border: 1px solid rgba(79, 70, 229, 0.08);
            border-radius: 16px;
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
        }

        .stFileUploader > div > div {
            border: 2px dashed #E2E8F0;
            border-radius: 16px;
            background: rgba(255, 255, 255, 0.5);
        }
        .stFileUploader > div > div:hover { border-color: #4F46E5; }

        .bg-decoration {
            position: fixed; width: 600px; height: 600px;
            border-radius: 50%; filter: blur(100px);
            opacity: 0.15; pointer-events: none; z-index: 0;
        }
        .bg-decoration-1 {
            background: linear-gradient(135deg, #4F46E5, #7C3AED);
            top: -200px; right: -100px;
            animation: float 20s ease-in-out infinite;
        }
        .bg-decoration-2 {
            background: linear-gradient(135deg, #7C3AED, #6366F1);
            bottom: -200px; left: -100px;
            animation: float 25s ease-in-out infinite reverse;
        }
        @keyframes float {
            0%, 100% { transform: translate(0, 0) scale(1); }
            33% { transform: translate(30px, -30px) scale(1.1); }
            66% { transform: translate(-20px, 20px) scale(0.9); }
        }

        /* 高亮行样式（数据页联动） */
        .highlight-row {
            background: linear-gradient(135deg, rgba(79, 70, 229, 0.08) 0%, rgba(124, 58, 237, 0.06) 100%) !important;
            box-shadow: inset 3px 0 0 #4F46E5 !important;
        }

        /* 表征预览卡片 */
        .char-card {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 16px;
            padding: 16px;
            border: 1px solid rgba(79, 70, 229, 0.08);
            text-align: center;
            transition: all 0.2s;
        }
        .char-card:hover {
            box-shadow: 0 8px 25px rgba(79, 70, 229, 0.15);
            transform: translateY(-4px);
            border-color: #4F46E5;
        }
        .char-card.active {
            border: 2px solid #4F46E5;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.2);
        }

        /* 右上角控制栏 */
        div[data-testid="element-container"]:has(> div.st-key-top_ctrl) {
            position: fixed;
            top: 6px;
            right: 140px;
            z-index: 999;
        }
        div.st-key-top_ctrl button {
            display: inline-flex !important;
            align-items: center;
            padding: 0 12px !important;
            border-radius: 8px !important;
            min-height: 28px !important;
            border: none !important;
            background: transparent !important;
            color: rgb(49, 51, 63) !important;
            font-size: 14px !important;
            line-height: 28px !important;
            cursor: pointer;
            white-space: nowrap;
        }
        div.st-key-top_ctrl button:hover {
            background: rgba(49, 51, 63, 0.04) !important;
        }
        div.st-key-top_ctrl [data-testid="column"] {
            flex: none !important;
            width: auto !important;
        }

        /* 隐藏 data_editor 每行的"行操作"溢出菜单按钮（⋮）。
           Streamlit 1.58 把行操作菜单渲染成独立的 st-key-<key>_row_menu
           容器（含 stPopoverButton），散落在表格外。这里多选择器确保命中：
           1) 容器级：隐藏整个行操作菜单容器（按钮+弹出层）
           2) 按钮级兜底：全局隐藏 stPopoverButton（本应用仅 data_editor 用到）
           需要行操作时移除此规则 */
        div[class*="row_menu"],
                [data-testid="stPopoverButton"] {
                    display: none !important;
                }

                /* 增删行列工具栏按钮 — 紧凑 pill 风格 */
                .toolbar-btn button {
                    padding: 2px 10px !important;
                    min-height: 28px !important;
                    border-radius: 8px !important;
                    font-size: 0.8rem !important;
                    font-weight: 500 !important;
                    transition: all 0.2s ease !important;
                    border: 1px solid #E2E8F0 !important;
                    background: rgba(255,255,255,0.8) !important;
                    color: #475569 !important;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.03) !important;
                }
                .toolbar-btn button:hover {
                    background: #EEF2FF !important;
                    border-color: #A5B4FC !important;
                    color: #4F46E5 !important;
                    transform: translateY(-1px);
                }
                .toolbar-btn button:active,
                .toolbar-btn button[data-active="true"] {
                    background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%) !important;
                    color: white !important;
                    border-color: transparent !important;
                    box-shadow: 0 2px 8px rgba(79,70,229,0.3) !important;
                }
            </style>
    <div class="bg-decoration bg-decoration-1"></div>
    <div class="bg-decoration bg-decoration-2"></div>
    """, unsafe_allow_html=True)

