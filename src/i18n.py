# -*- coding: utf-8 -*-
"""
PI_DATABASE 国际化模块 (i18n)
支持中英文切换
"""

TRANSLATIONS = {
    # === 通用 ===
    "app_title": {
        "zh": "PI_DATABASE | 聚酰亚胺数据库",
        "en": "PI_DATABASE | Polyimide Database"
    },
    "app_subtitle": {
        "zh": "聚酰亚胺数据综合管理平台",
        "en": "Polyimide Data Management Platform"
    },
    "app_full_name": {
        "zh": "聚酰亚胺数据管理平台",
        "en": "Polyimide Data Management Platform"
    },
    "powered_by_ai": {
        "zh": "数据驱动的 PI 研究",
        "en": "Data-Driven PI Research"
    },

    # === 侧边栏 ===
    "sidebar_title": {
        "zh": "📋 导航板块",
        "en": "📋 Modules"
    },
    "quick_links": {
        "zh": "💡 快捷操作",
        "en": "💡 Quick Links"
    },
    "rdkit_ready": {
        "zh": "RDKit 已就绪",
        "en": "RDKit Ready"
    },

    # === 导航菜单（7个页面） ===
    "nav_home":       {"zh": "🏠 首页",       "en": "🏠 Home"},
    "nav_data":       {"zh": "📊 数据总览",   "en": "📊 Data Overview"},
    "nav_nmr":        {"zh": "🧪 NMR 分析",   "en": "🧪 NMR Analysis"},
    "nav_page4":      {"zh": "📋 页面 4",     "en": "📋 Page 4"},
    "nav_page5":      {"zh": "📋 页面 5",     "en": "📋 Page 5"},
    "nav_page6":      {"zh": "📋 页面 6",     "en": "📋 Page 6"},
    "nav_piass":      {"zh": "🔗 PI_ASS",     "en": "🔗 PI_ASS"},

    # === 首页 ===
    "home_core_capabilities": {
        "zh": "平台核心能力",
        "en": "Core Capabilities"
    },
    "home_db_count": {
        "zh": "配方数据",
        "en": "Recipe Data"
    },
    "home_perf_count": {
        "zh": "性能数据",
        "en": "Performance Data"
    },
    "home_char_count": {
        "zh": "表征记录",
        "en": "Characterization"
    },
    "home_nmr_tool": {
        "zh": "NMR 分析工具",
        "en": "NMR Analysis Tool"
    },
    "home_feature_title": {
        "zh": "功能板块",
        "en": "Feature Modules"
    },
    "home_feature_subtitle": {
        "zh": "一站式管理聚酰亚胺配方、性能与表征数据",
        "en": "One-stop management of PI formulation, performance & characterization data"
    },
    "home_data_title": {"zh": "数据总览", "en": "Data Overview"},
    "home_data_desc": {
        "zh": "配方表格、性能表格、表征图三方联动，点击高亮",
        "en": "Linked recipe/performance/characterization with click highlighting"
    },
    "home_nmr_title": {"zh": "NMR 分析", "en": "NMR Analysis"},
    "home_nmr_desc": {
        "zh": "核磁共振数据处理与可视化",
        "en": "NMR data processing & visualization"
    },
    "home_enter_module": {"zh": "进入板块 →", "en": "Enter Module →"},
    "home_project_status": {
        "zh": "数据概览",
        "en": "Data Overview"
    },
    "home_realtime_monitor": {
        "zh": "实时数据统计",
        "en": "Real-time Statistics"
    },

    # === 数据页面 ===
    "data_recipe_title": {
        "zh": "📋 配方表格",
        "en": "📋 Recipe Table"
    },
    "data_recipe_hint": {
        "zh": "双击单元格编辑，右键可增删行列",
        "en": "Double-click to edit, right-click to add/delete rows"
    },
    "data_perf_title": {
        "zh": "📈 性能表格",
        "en": "📈 Performance Table"
    },
    "data_perf_hint": {
        "zh": "双击单元格编辑，与配方表格联动高亮",
        "en": "Double-click to edit, linked with recipe table"
    },
    "data_char_title": {
        "zh": "🖼️ 表征图表",
        "en": "🖼️ Characterization"
    },
    "data_char_hint": {
        "zh": "点击预览图可查看大图详情",
        "en": "Click preview image to view details"
    },
    "data_char_no_image": {
        "zh": "暂无预览图",
        "en": "No preview image"
    },
    "data_char_view_detail": {
        "zh": "🔍 查看详情",
        "en": "🔍 View Details"
    },
    "data_highlighted": {
        "zh": "已高亮",
        "en": "Highlighted"
    },
    "data_recipe_col_name":     {"zh": "样品名称", "en": "Sample Name"},
    "data_recipe_col_dianhy":   {"zh": "二酐单体", "en": "Dianhydride"},
    "data_recipe_col_diamine":  {"zh": "二胺单体", "en": "Diamine"},
    "data_recipe_col_solvent":  {"zh": "溶剂",     "en": "Solvent"},
    "data_recipe_col_method":   {"zh": "合成方法", "en": "Synthesis Method"},
    "data_perf_col_name":       {"zh": "样品名称",  "en": "Sample Name"},
    "data_perf_col_tg":         {"zh": "Tg (°C)",  "en": "Tg (°C)"},
    "data_perf_col_td":         {"zh": "Td (°C)",  "en": "Td (°C)"},
    "data_perf_col_dielectric": {"zh": "介电常数",  "en": "Dielectric Const."},
    "data_perf_col_tensile":    {"zh": "拉伸强度(MPa)", "en": "Tensile (MPa)"},
    "data_perf_col_elongation": {"zh": "断裂伸长率(%)",  "en": "Elongation (%)"},
    "data_char_col_name":       {"zh": "样品名称", "en": "Sample Name"},
    "data_char_col_type":       {"zh": "表征类型", "en": "Type"},
    "data_char_col_preview":    {"zh": "预览图",   "en": "Preview"},

    # === NMR ===
    "nmr_title": {
        "zh": "🧪 NMR 分析面板",
        "en": "🧪 NMR Analysis Panel"
    },
    "nmr_placeholder": {
        "zh": "功能开发中，敬请期待...",
        "en": "Feature under development..."
    },

    # === Page 4-6 ===
    "page4_title": {"zh": "📋 页面 4", "en": "📋 Page 4"},
    "page5_title": {"zh": "📋 页面 5", "en": "📋 Page 5"},
    "page6_title": {"zh": "📋 页面 6", "en": "📋 Page 6"},
    "page_placeholder": {
        "zh": "功能开发中，敬请期待...",
        "en": "Feature under development..."
    },

    # === PI_ASS 链接 ===
    "piass_title": {
        "zh": "🔗 PI_ASS 项目",
        "en": "🔗 PI_ASS Project"
    },
    "piass_desc": {
        "zh": "点击下方按钮跳转到 PI_ASS 聚酰亚胺性能预测系统",
        "en": "Click the button below to go to PI_ASS Polyimide Performance Prediction System"
    },
    "piass_go": {
        "zh": "🚀 打开 PI_ASS",
        "en": "🚀 Open PI_ASS"
    },
    "piass_new_tab": {
        "zh": "或在新标签页打开",
        "en": "Or open in a new tab"
    },
    "piass_url": {
        "zh": "http://localhost:8002",
        "en": "http://localhost:8002"
    },
}


def t(key: str, lang: str = "zh") -> str:
    """获取翻译文本"""
    entry = TRANSLATIONS.get(key)
    if entry is None:
        return key
    return entry.get(lang, entry.get("zh", key))


def get_page_names(lang: str) -> list:
    """获取导航页面名称列表（7个页面）"""
    keys = [
        "nav_home", "nav_data", "nav_nmr",
        "nav_page4", "nav_page5", "nav_page6",
        "nav_piass"
    ]
    return [t(k, lang) for k in keys]


def get_page_key(page_name: str, lang: str) -> str:
    """根据页面显示名称返回内部 key"""
    keys = [
        "nav_home", "nav_data", "nav_nmr",
        "nav_page4", "nav_page5", "nav_page6",
        "nav_piass"
    ]
    for k in keys:
        if t(k, lang) == page_name:
            return k
    return "nav_home"