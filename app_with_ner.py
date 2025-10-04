"""
固有表現表示機能付きStreamlitアプリ
"""

import streamlit as st
import pickle
import pandas as pd
from ner_extractor import PatentLawNER
import re
from bs4 import BeautifulSoup

def get_article_text(article):
    """条文から表示用テキストを取得"""
    # 複数のフィールドを確認
    text_fields = ['text', 'body', 'content', 'article_text']
    
    for field in text_fields:
        if field in article:
            text = article[field]
            if text:
                # HTMLタグが含まれている場合は除去
                if '<' in text and '>' in text:
                    try:
                        soup = BeautifulSoup(text, 'html.parser')
                        clean_text = soup.get_text()
                        # 連続する空白や改行を整理
                        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
                        return clean_text
                    except:
                        # エラーの場合は簡単なタグ除去
                        clean_text = re.sub(r'<[^>]+>', '', text)
                        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
                        return clean_text
                else:
                    return text
    
    return "テキストが見つかりません"

# ページ設定
st.set_page_config(
    page_title="特許法条文閲覧・NER表示システム",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS: 左パネル（サイドバー）のフォントサイズを小さくして見やすくする
st.markdown("""
<style>
/* サイドバー全体のフォントサイズを小さく（複数バージョン対応） */
.css-1d391kg, .css-1aumxhk, .st-emotion-cache-1aumxhk, section[data-testid="stSidebar"] {
    font-size: 0.8rem;
}

/* サイドバーの見出し（h3）のフォントサイズ */
.css-1d391kg h3, .css-1aumxhk h3, .st-emotion-cache-1aumxhk h3, section[data-testid="stSidebar"] h3 {
    font-size: 1.0rem;
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;
}

/* サイドバーのselect boxのフォントサイズ */
.css-1d391kg .stSelectbox, .css-1aumxhk .stSelectbox, section[data-testid="stSidebar"] .stSelectbox {
    font-size: 0.8rem;
}

/* サイドバーのselect boxの選択肢フォントサイズ */
.css-1d391kg .stSelectbox > div > div, section[data-testid="stSidebar"] .stSelectbox > div > div {
    font-size: 0.8rem;
}

/* サイドバーのボタンのフォントサイズ */
.css-1d391kg .stButton, .css-1aumxhk .stButton, section[data-testid="stSidebar"] .stButton {
    font-size: 0.8rem;
}

/* サイドバーのボタンテキスト */
.css-1d391kg button, .css-1aumxhk button, section[data-testid="stSidebar"] button {
    font-size: 0.8rem !important;
    padding: 0.25rem 0.5rem !important;
    line-height: 1.2 !important;
    margin: 0.1rem 0 !important;
}

/* サイドバーのメトリック表示 */
.css-1d391kg .metric-container, .css-1aumxhk .metric-container, section[data-testid="stSidebar"] [data-testid="metric-container"] {
    font-size: 0.8rem;
}

/* サイドバーの区切り線の間隔を狭く */
.css-1d391kg hr, .css-1aumxhk hr, section[data-testid="stSidebar"] hr {
    margin: 0.5rem 0;
}

/* サイドバーの段落の行間を狭く */
.css-1d391kg p, .css-1aumxhk p, section[data-testid="stSidebar"] p {
    margin-bottom: 0.5rem;
    line-height: 1.3;
}

/* 固有表現凡例のカラーバッジを小さく */
.css-1d391kg .stMarkdown div, .css-1aumxhk .stMarkdown div, section[data-testid="stSidebar"] .stMarkdown div {
    font-size: 0.7rem;
    padding: 2px 6px;
    margin: 1px 0;
}

/* selectboxのラベルテキストも小さく */
section[data-testid="stSidebar"] label {
    font-size: 0.8rem !important;
}

/* サイドバー内のマークダウンテキスト */
section[data-testid="stSidebar"] .stMarkdown {
    font-size: 0.8rem;
}

/* コンパクトなボタンスタイル */
section[data-testid="stSidebar"] button[kind="secondary"], 
section[data-testid="stSidebar"] button[kind="primary"] {
    min-height: 2rem !important;
    padding: 0.2rem 0.5rem !important;
}

/* 固有表現カテゴリボタンの色分け（テキストベース選択） */
/* Streamlitボタンのテキスト内容で識別 */

/* 一般的なサイドバーボタンのスタイル改善 */
section[data-testid="stSidebar"] button {
    transition: all 0.2s ease !important;
    border-radius: 4px !important;
}

/* ホバー効果 */
section[data-testid="stSidebar"] button:hover {
    opacity: 0.8 !important;
    transform: scale(1.02) !important;
}

/* 選択中ボタンの特別なスタイル */
section[data-testid="stSidebar"] button[kind="primary"] {
    font-weight: bold !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
}

/* 右ペイン第２カラムのフォントサイズを小さく */
[data-testid="column"]:last-child {
    font-size: 0.6rem;
}

/* より具体的なカラム選択（複数の方法でターゲット） */
.main .block-container [data-testid="column"]:nth-child(2),
.stApp [data-testid="column"]:nth-child(2),
div[data-testid="stHorizontalBlock"] > div:nth-child(2) {
    font-size: 0.6rem !important;
}

/* 右ペイン第２カラムの見出し（複数セレクタで確実に適用） */
[data-testid="column"]:last-child h1,
[data-testid="column"]:last-child h2,
[data-testid="column"]:last-child h3,
[data-testid="column"]:last-child h4,
[data-testid="column"]:last-child .stMarkdown h1,
[data-testid="column"]:last-child .stMarkdown h2,
[data-testid="column"]:last-child .stMarkdown h3,
[data-testid="column"]:last-child .stMarkdown h4,
.main .block-container [data-testid="column"]:nth-child(2) h1,
.main .block-container [data-testid="column"]:nth-child(2) h2,
.main .block-container [data-testid="column"]:nth-child(2) h3,
.main .block-container [data-testid="column"]:nth-child(2) h4,
div[data-testid="stHorizontalBlock"] > div:nth-child(2) h1,
div[data-testid="stHorizontalBlock"] > div:nth-child(2) h2,
div[data-testid="stHorizontalBlock"] > div:nth-child(2) h3,
div[data-testid="stHorizontalBlock"] > div:nth-child(2) h4 {
    font-size: 0.65rem !important;
    margin-bottom: 0.3rem !important;
    margin-top: 0.3rem !important;
    line-height: 1.2 !important;
}

/* Streamlitの見出しコンポーネント */
[data-testid="column"]:last-child [data-testid="stHeader"],
[data-testid="column"]:last-child [data-testid="stSubheader"],
div[data-testid="stHorizontalBlock"] > div:nth-child(2) [data-testid="stHeader"],
div[data-testid="stHorizontalBlock"] > div:nth-child(2) [data-testid="stSubheader"] {
    font-size: 0.65rem !important;
}

/* 右ペイン第２カラムのメトリック表示 */
[data-testid="column"]:last-child [data-testid="metric-container"],
div[data-testid="stHorizontalBlock"] > div:nth-child(2) [data-testid="metric-container"] {
    font-size: 0.5rem !important;
    padding: 0.2rem !important;
}

/* 右ペイン第２カラムのメトリックラベル */
[data-testid="column"]:last-child [data-testid="metric-container"] label,
div[data-testid="stHorizontalBlock"] > div:nth-child(2) [data-testid="metric-container"] label {
    font-size: 0.5rem !important;
}

/* 右ペイン第２カラムのメトリック値 */
[data-testid="column"]:last-child [data-testid="metric-container"] [data-testid="metric-value"],
div[data-testid="stHorizontalBlock"] > div:nth-child(2) [data-testid="metric-container"] [data-testid="metric-value"] {
    font-size: 0.55rem !important;
}

/* 右ペイン第２カラムの一般的なテキスト */
[data-testid="column"]:last-child p,
[data-testid="column"]:last-child div,
div[data-testid="stHorizontalBlock"] > div:nth-child(2) p,
div[data-testid="stHorizontalBlock"] > div:nth-child(2) div {
    font-size: 0.6rem !important;
    line-height: 1.2 !important;
    margin-bottom: 0.2rem !important;
}

/* 右ペイン第２カラムのマークダウン */
[data-testid="column"]:last-child .stMarkdown,
div[data-testid="stHorizontalBlock"] > div:nth-child(2) .stMarkdown {
    font-size: 0.6rem !important;
}

/* 右ペイン第２カラムの情報ボックス */
[data-testid="column"]:last-child .stAlert,
div[data-testid="stHorizontalBlock"] > div:nth-child(2) .stAlert {
    font-size: 0.5rem !important;
    padding: 0.3rem !important;
    margin: 0.2rem 0 !important;
}

/* 右ペイン第２カラムのコンパクト表示 */
[data-testid="column"]:last-child *,
div[data-testid="stHorizontalBlock"] > div:nth-child(2) * {
    margin-top: 0.1rem !important;
    margin-bottom: 0.1rem !important;
}

/* より強力なセレクタで見出しを確実に小さくする */
[data-testid="column"]:last-child *,
div[data-testid="stHorizontalBlock"] > div:nth-child(2) * {
    font-size: inherit !important;
}

/* 最終的な強制適用 */
[data-testid="column"]:last-child h1,
[data-testid="column"]:last-child h2,
[data-testid="column"]:last-child h3,
div[data-testid="stHorizontalBlock"] > div:nth-child(2) h1,
div[data-testid="stHorizontalBlock"] > div:nth-child(2) h2,
div[data-testid="stHorizontalBlock"] > div:nth-child(2) h3 {
    font-size: 0.65rem !important;
    font-weight: bold !important;
}

/* 特別な対策：統計情報の見出しを確実に変更 */
h2:contains("📊 統計情報"),
h3:contains("📊 統計情報"),
h4:contains("📊 統計情報") {
    font-size: 0.65rem !important;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """データ読み込み（キャッシュ付き）"""
    try:
        # 階層構造対応の改善されたNERデータを優先読み込み
        with open('334AC0000000121_20230703_505AC0000000051_with_ner_hierarchical.pickle', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        try:
            # 従来のNER解析済みデータを読み込み
            with open('334AC0000000121_20230703_505AC0000000051_with_ner.pickle', 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            # NER解析済みデータがない場合は元データを読み込み
            with open('334AC0000000121_20230703_505AC0000000051.pickle', 'rb') as f:
                return pickle.load(f)

@st.cache_data
def load_ner_csv():
    """NER結果CSVを読み込み"""
    try:
        # 階層構造対応の改善されたCSVを優先読み込み
        return pd.read_csv('patent_law_ner_results_hierarchical.csv', encoding='utf-8-sig')
    except FileNotFoundError:
        try:
            return pd.read_csv('patent_law_ner_results_improved.csv', encoding='utf-8-sig')
        except FileNotFoundError:
            try:
                return pd.read_csv('patent_law_ner_results.csv')
            except FileNotFoundError:
                return pd.DataFrame()

def highlight_entities(text, entities, selected_category=None):
    """テキスト中の固有表現をハイライト（カテゴリ選択対応版）"""
    if not entities:
        return text
    
    # デバッグ出力（一時的）
    # print(f"DEBUG: highlight_entities called with selected_category='{selected_category}'")
    
    # エンティティの色分け（通常とハイライト用）
    normal_colors = {
        'LAW_REFERENCE': '#FFF2F2',      # 非常に薄い赤
        'ARTICLE_REFERENCE': '#F0F8FF',  # 非常に薄い青
        'TIME_PERIOD': '#F0FFF0',        # 非常に薄い緑
        'MONEY_AMOUNT': '#FFFEF0',       # 非常に薄い黄
        'ORGANIZATION': '#F8F0FF',       # 非常に薄い紫
        'PROCEDURE': '#FFF0F8',          # 非常に薄いピンク
        'LEGAL_STATUS': '#F0FFFF',       # 非常に薄いシアン
    }
    
    # 選択されたカテゴリ用の強調色
    highlight_colors = {
        'LAW_REFERENCE': '#FFB6C1',      # 濃いピンク
        'ARTICLE_REFERENCE': '#87CEEB',  # 濃い空色
        'TIME_PERIOD': '#98FB98',        # 濃い薄緑
        'MONEY_AMOUNT': '#F0E68C',       # 濃い黄色
        'ORGANIZATION': '#DDA0DD',       # 濃い薄紫
        'PROCEDURE': '#FFB6C1',          # 濃いピンク
        'LEGAL_STATUS': '#AFEEEE',       # 濃いシアン
    }
    
    # エンティティを収集し、テキスト長の降順でソート
    all_entities = []
    for category, entity_list in entities.items():
        for entity in entity_list:
            entity_text = entity['text']
            if entity_text in text:  # テキスト内に存在する場合のみ
                all_entities.append({
                    'text': entity_text,
                    'category': category
                })
    
    # 重複除去（同じテキストは1回のみ）
    unique_entities = []
    seen_texts = set()
    for entity in all_entities:
        if entity['text'] not in seen_texts:
            unique_entities.append(entity)
            seen_texts.add(entity['text'])
    
    # テキスト長の降順でソート（長い表現を先に処理）
    unique_entities.sort(key=lambda x: len(x['text']), reverse=True)
    
    # ハイライト処理
    highlighted_text = text
    for entity in unique_entities:
        # カテゴリが選択されている場合、または「すべて」が選択されている場合は強調色と赤枠を適用
        if selected_category == "すべて" or (selected_category and entity['category'] == selected_category):
            color = highlight_colors.get(entity['category'], '#FFD700')  # ゴールド色
            border_style = "border: 2px solid #FF6B6B; box-shadow: 0 0 10px rgba(255, 107, 107, 0.5);"
            # デバッグ出力（一時的）
            # print(f"DEBUG: Applying highlight to {entity['text']} (category: {entity['category']})")
        else:
            color = normal_colors.get(entity['category'], '#F5F5F5')
            border_style = ""
        entity_text = entity['text']
        
        # 既にハイライトされていないかチェック
        if entity_text in highlighted_text and highlighted_text.count(f'>{entity_text}<') == 0:
            # カテゴリ名を日本語で表示
            category_jp = {
                'LAW_REFERENCE': '法律参照',
                'ARTICLE_REFERENCE': '条文参照', 
                'TIME_PERIOD': '期間表現',
                'MONEY_AMOUNT': '金額表現',
                'ORGANIZATION': '組織・機関',
                'PROCEDURE': '手続き関連',
                'LEGAL_STATUS': '法的地位'
            }.get(entity['category'], entity['category'])
            
            highlighted_part = (
                f'<span style="background-color: {color}; '
                f'padding: 1px 3px; margin: 0 1px; border-radius: 3px; '
                f'font-weight: 500; border: 1px solid {color}88; {border_style}" '
                f'title="{category_jp}: {entity_text}">'
                f'{entity_text}</span>'
            )
            
            # 最初の出現箇所のみ置換
            highlighted_text = highlighted_text.replace(entity_text, highlighted_part, 1)
    
    return highlighted_text

def display_entity_legend(selected_article=None):
    """クリック可能な固有表現凡例を表示（色付きボタン対応版）"""
    st.sidebar.markdown("### 🏷️ 固有表現の種類 (クリックで選択)")
    
    # セッション状態から条文データを取得
    if selected_article is None and 'current_article' in st.session_state:
        selected_article = st.session_state.current_article
    
    # カテゴリ別の色定義（ボタン用）
    button_colors = {
        'LAW_REFERENCE': {'bg': '#FFE4E6', 'border': '#FFB6C1', 'text': '#8B4B8B'},
        'ARTICLE_REFERENCE': {'bg': '#E6F3FF', 'border': '#87CEEB', 'text': '#1E3A8A'},
        'TIME_PERIOD': {'bg': '#E6FFE6', 'border': '#98FB98', 'text': '#2F5233'},
        'MONEY_AMOUNT': {'bg': '#FFFAE6', 'border': '#F0E68C', 'text': '#8B7355'},
        'ORGANIZATION': {'bg': '#F3E6FF', 'border': '#DDA0DD', 'text': '#663399'},
        'PROCEDURE': {'bg': '#FFE6F0', 'border': '#FFB6C1', 'text': '#8B5A7C'},
        'LEGAL_STATUS': {'bg': '#E6FFFF', 'border': '#AFEEEE', 'text': '#2F4F4F'},
    }
    
    legend_items = [
        ('LAW_REFERENCE', '📚 法律参照', '#FFF2F2'),
        ('ARTICLE_REFERENCE', '📋 条文参照', '#F0F8FF'),
        ('TIME_PERIOD', '⏰ 期間表現', '#F0FFF0'),
        ('MONEY_AMOUNT', '💰 金額表現', '#FFFEF0'),
        ('ORGANIZATION', '🏢 組織・機関', '#F8F0FF'),
        ('PROCEDURE', '⚙️ 手続き関連', '#FFF0F8'),
        ('LEGAL_STATUS', '⚖️ 法的地位・状態', '#F0FFFF'),
    ]
    
    # 「すべて」ボタン
    is_all_selected = (st.session_state.selected_category == "すべて")
    all_button_style = "primary" if is_all_selected else "secondary"
    all_button_text = "🌈 すべてのカテゴリ" + (" (選択中)" if is_all_selected else "")
    
    if st.sidebar.button(
        all_button_text,
        key="legend_all_categories",
        help="すべてのカテゴリを表示",
        type=all_button_style,
        use_container_width=True
    ):
        st.session_state.selected_category = "すべて"
        st.session_state.category_selection_source = "legend"
    
    st.sidebar.markdown("---")
    
    # 各カテゴリの凡例とボタン
    for category, description, color in legend_items:
        # 選択中の条文にこのカテゴリが存在するかチェック
        has_entities = False
        entity_count = 0
        if selected_article and 'ner_entities' in selected_article:
            if category in selected_article['ner_entities'] and selected_article['ner_entities'][category]:
                has_entities = True
                entity_count = len(selected_article['ner_entities'][category])
        
        # 選択状態の確認（「すべて」が選択されている場合も選択状態として扱う）
        is_selected = (st.session_state.selected_category == category or 
                      st.session_state.selected_category == "すべて")
        
        # ボタンのスタイルとテキスト
        if has_entities:
            button_text = f"{description}"
            if is_selected:
                if st.session_state.selected_category == "すべて":
                    button_text += " (すべて選択中)"
                else:
                    button_text += " (選択中)"
            button_text += f" ({entity_count}個)"
            
            # カテゴリの色を取得
            colors = button_colors.get(category, {'bg': '#F5F5F5', 'border': '#DDD', 'text': '#333'})
            
            # カラーバッジと説明をHTMLで表示（コンパクト版、ボタンと同じ色で統一）
            badge_html = (
                f'<div style="background-color: {colors["bg"]}; padding: 2px 6px; margin: 1px 0; '
                f'border-radius: 2px; font-size: 10px; border: 1px solid {colors["border"]}; '
                f'color: {colors["text"]}; display: inline-block; width: 100%; text-align: center;">'
                f'<small>({category})</small></div>'
            )
            st.sidebar.markdown(badge_html, unsafe_allow_html=True)
            
            # 色付きボタンのスタイルをCSSで適用（動的に生成）
            button_style_css = f"""
            <style>
            /* {category}ボタンの色設定 */
            button[key="legend_{category}"] {{
                background: {colors["border"] if is_selected else colors["bg"]} !important;
                color: {"#FFFFFF" if is_selected else colors["text"]} !important;
                border: 1px solid {colors["border"]} !important;
                font-weight: {"bold" if is_selected else "normal"} !important;
                transition: all 0.2s ease !important;
            }}
            
            button[key="legend_{category}"]:hover {{
                opacity: 0.8 !important;
                transform: scale(1.02) !important;
            }}
            </style>
            """
            st.sidebar.markdown(button_style_css, unsafe_allow_html=True)
            
            # Streamlitボタン（CSSで色が適用される）
            if st.sidebar.button(
                button_text,
                key=f"legend_{category}",
                help=f"{description}を強調表示",
                type="primary" if is_selected else "secondary",
                use_container_width=True
            ):
                st.session_state.selected_category = category
                st.session_state.category_selection_source = "legend"
        else:
            # エンティティがない場合は無効なボタン（グレーアウト、コンパクト版）
            badge_html = (
                f'<div style="background-color: #f0f0f0; padding: 2px 6px; margin: 1px 0; '
                f'border-radius: 2px; font-size: 10px; border: 1px solid #ddd; '
                f'color: #999; display: inline-block; width: 100%; text-align: center;">'
                f'<small>({category})</small></div>'
            )
            st.sidebar.markdown(badge_html, unsafe_allow_html=True)
            
            # 無効なボタン
            st.sidebar.button(
                f"{description} (0個)",
                key=f"legend_{category}_disabled",
                help="この条文にはこのカテゴリの固有表現がありません",
                disabled=True,
                use_container_width=True
            )
        
        # スペース追加（小さく）
        st.sidebar.markdown('<div style="margin: 2px 0;"></div>', unsafe_allow_html=True)

def main():
    st.title("⚖️ 特許法条文閲覧・固有表現抽出システム")
    st.markdown("---")
    
    # セッション状態の初期化
    if 'selected_category' not in st.session_state:
        st.session_state.selected_category = "すべて"
    if 'category_selection_source' not in st.session_state:
        st.session_state.category_selection_source = "radio"  # "radio" or "sidebar"
    if 'selected_article_idx' not in st.session_state:
        st.session_state.selected_article_idx = 0  # デフォルトは0番目（1条）
    
    # 章ごとの条文選択インデックスを管理するための初期化
    # この方式により、章を切り替えても各章の最後に選択した条文を覚えている
    # そして左パネルのカテゴリボタンをクリックしても条文選択が変わらない
    
    # データ読み込み
    with st.spinner("データを読み込み中..."):
        data = load_data()
        ner_df = load_ner_csv()
    
    if not data:
        st.error("データの読み込みに失敗しました。")
        return
    
    # サイドバー: 章選択
    st.sidebar.markdown("### 📖 章選択")
    chapter_titles = [f"{i+1}. {chapter.get('title', f'章{i+1}')}" for i, chapter in enumerate(data)]
    selected_chapter_idx = st.sidebar.selectbox(
        "章を選択してください:",
        range(len(chapter_titles)),
        format_func=lambda x: chapter_titles[x]
    )
    
    if selected_chapter_idx is not None:
        selected_chapter = data[selected_chapter_idx]
        
        # 条文選択
        if 'articles' in selected_chapter:
            articles = selected_chapter['articles']
            
            st.sidebar.markdown("### 📄 条文選択")
            article_titles = []
            for i, article in enumerate(articles):
                title = article.get('title', article.get('heading', f'条文{i+1}'))
                article_titles.append(f"{i+1}. {title}")
            
            # セッション状態のキーでインデックスを管理
            if f'chapter_{selected_chapter_idx}_article_idx' not in st.session_state:
                st.session_state[f'chapter_{selected_chapter_idx}_article_idx'] = 0
            
            current_article_idx = st.session_state[f'chapter_{selected_chapter_idx}_article_idx']
            
            # インデックスの範囲チェック
            if current_article_idx >= len(article_titles):
                current_article_idx = 0
                st.session_state[f'chapter_{selected_chapter_idx}_article_idx'] = 0
            
            selected_article_idx = st.sidebar.selectbox(
                "条文を選択してください:",
                range(len(article_titles)),
                format_func=lambda x: article_titles[x],
                index=current_article_idx,
                key=f"article_selector_chapter_{selected_chapter_idx}"
            )
            
            # 選択が変更された場合はセッション状態を更新
            if selected_article_idx != current_article_idx:
                st.session_state[f'chapter_{selected_chapter_idx}_article_idx'] = selected_article_idx
                st.session_state.selected_article_idx = selected_article_idx  # 互換性のため保持
            else:
                st.session_state.selected_article_idx = current_article_idx
            
            if selected_article_idx is not None:
                selected_article = articles[selected_article_idx]
                
                # 選択中の条文をセッション状態に保存
                st.session_state.current_article = selected_article
                
                # サイドバー: 固有表現の凡例（条文選択後に表示）
                display_entity_legend(selected_article)
                
                # メインコンテンツ表示
                col1, col2 = st.columns([3, 0.864])
                
                with col1:
                    # 条文表示
                    article_title = selected_article.get('title', selected_article.get('heading', '条文'))
                    st.subheader(f"📄 {article_title}")
                    
                    article_text = get_article_text(selected_article)
                    
                    # デフォルトでハイライト表示を設定
                    if 'display_mode' not in st.session_state:
                        st.session_state.display_mode = "ハイライト表示"
                    
                    display_mode = st.session_state.display_mode
                    
                    if display_mode == "ハイライト表示" and 'ner_entities' in selected_article:
                        # まず固有表現ハイライト表示
                        available_categories = list(selected_article['ner_entities'].keys())
                        category_names = {
                            'LAW_REFERENCE': '📚 法律参照',
                            'ARTICLE_REFERENCE': '📋 条文参照', 
                            'TIME_PERIOD': '⏰ 期間表現',
                            'MONEY_AMOUNT': '💰 金額表現',
                            'ORGANIZATION': '🏢 組織・機関',
                            'PROCEDURE': '⚙️ 手続き関連',
                            'LEGAL_STATUS': '⚖️ 法的地位'
                        }
                        
                        selected_category = st.session_state.selected_category
                        
                        # 選択されたカテゴリに応じてハイライト（「すべて」の場合はそのまま渡す）
                        highlight_category = selected_category
                        highlighted_text = highlight_entities(article_text, selected_article['ner_entities'], highlight_category)
                        
                        st.markdown("#### 🎨 固有表現ハイライト表示")
                        
                        # 現在の選択状態を表示
                        if selected_category != "すべて":
                            source_icons = {
                                "radio": "⚙️ カテゴリ選択",
                                "quick_button": "🚀 クイック選択", 
                                "quick_button_right": "🚀 右パネルクイック選択", 
                                "sidebar": "📊 右パネル統計",
                                "legend": "🏷️ 左パネル凡例"
                            }
                            source_text = source_icons.get(st.session_state.category_selection_source, "🔧 システム")
                            st.info(f"💡 {category_names.get(selected_category, selected_category)} が強調表示中 (選択元: {source_text})")
                        else:
                            st.info("🌈 すべてのカテゴリが表示されています")
                        
                        st.markdown(highlighted_text, unsafe_allow_html=True)
                        
                        # 原文も併記（折りたたみ表示）
                        with st.expander("📝 原文を確認"):
                            st.text_area(
                                "原文テキスト",
                                article_text,
                                height=200,
                                disabled=True
                            )
                        
                        # カテゴリ選択機能を下に移動
                        st.markdown("#### 🎯 固有表現カテゴリ選択")
                        
                        # ラジオボタンでカテゴリ選択（セッション状態と連動）
                        current_selection = st.radio(
                            "強調表示するカテゴリを選択:",
                            ["すべて"] + available_categories,
                            index=(["すべて"] + available_categories).index(st.session_state.selected_category) if st.session_state.selected_category in (["すべて"] + available_categories) else 0,
                            format_func=lambda x: "🌈 すべてのカテゴリ" if x == "すべて" else category_names.get(x, x),
                            horizontal=True,
                            help="特定のカテゴリを選択すると、そのカテゴリの固有表現が強調表示されます"
                        )
                        
                        # ラジオボタンで選択された場合、セッション状態を更新
                        if current_selection != st.session_state.selected_category:
                            st.session_state.selected_category = current_selection
                            st.session_state.category_selection_source = "radio"
                    else:
                        # 原文表示（デフォルト）
                        st.markdown("#### 📝 原文")
                        st.text_area(
                            "条文内容",
                            article_text,
                            height=300,
                            disabled=True
                        )
                        
                        if 'ner_entities' in selected_article:
                            st.info("💡 「ハイライト表示」を選択すると、固有表現が色分けされます。")
                    
                    # 固有表現の詳細表示
                    if 'ner_entities' in selected_article:
                        st.markdown("#### 🏷️ 抽出された固有表現")
                        
                        # タブで整理
                        entity_tabs = st.tabs(["📊 概要", "📋 詳細リスト", "🔍 検索"])
                        
                        with entity_tabs[0]:
                            # 概要表示
                            total_entities = sum(len(entities) for entities in selected_article['ner_entities'].values())
                            st.metric("合計固有表現数", total_entities)
                            
                            for category, entities in selected_article['ner_entities'].items():
                                if entities:
                                    category_display = category.replace('_', ' ').title()
                                    st.metric(f"{category_display}", f"{len(entities)}個")
                        
                        with entity_tabs[1]:
                            # 詳細リスト
                            for category, entities in selected_article['ner_entities'].items():
                                if entities:
                                    st.markdown(f"**{category.replace('_', ' ').title()}** ({len(entities)}個)")
                                    
                                    # テーブル形式で表示
                                    entity_data = []
                                    for i, entity in enumerate(entities, 1):
                                        entity_data.append({
                                            "No.": i,
                                            "表現": entity['text'],
                                            "位置": f"{entity['start']}-{entity['end']}"
                                        })
                                    
                                    if entity_data:
                                        df_entities = pd.DataFrame(entity_data)
                                        st.dataframe(df_entities, width="stretch", hide_index=True)
                        
                        with entity_tabs[2]:
                            # 検索機能
                            search_term = st.text_input("固有表現を検索:", placeholder="例: 特許庁, 第一条, 出願")
                            
                            if search_term:
                                found_entities = []
                                for category, entities in selected_article['ner_entities'].items():
                                    for entity in entities:
                                        if search_term.lower() in entity['text'].lower():
                                            found_entities.append({
                                                "カテゴリ": category,
                                                "表現": entity['text'],
                                                "位置": f"{entity['start']}-{entity['end']}"
                                            })
                                
                                if found_entities:
                                    st.success(f"「{search_term}」に関連する固有表現が{len(found_entities)}個見つかりました")
                                    df_found = pd.DataFrame(found_entities)
                                    st.dataframe(df_found, width="stretch", hide_index=True)
                                else:
                                    st.info(f"「{search_term}」に関連する固有表現は見つかりませんでした")
                    else:
                        st.info("この条文には固有表現解析データがありません。")
                    
                    # 表示モード選択を一番下に移動
                    st.markdown("---")
                    st.markdown("#### ⚙️ 表示設定")
                    display_mode = st.radio(
                        "表示モード:",
                        ["ハイライト表示", "原文表示"],
                        index=0 if st.session_state.display_mode == "ハイライト表示" else 1,
                        horizontal=True,
                        help="ハイライト表示：固有表現をカラーハイライト / 原文表示：元のテキストをそのまま表示",
                        key="display_mode_selector"
                    )
                    
                    # 表示モードが変更された場合はセッション状態を更新して再実行
                    if display_mode != st.session_state.display_mode:
                        st.session_state.display_mode = display_mode
                        st.rerun()
                
                with col2:
                    # 右ペインのコンパクトスタイルを直接適用（強力な優先度で上書き）
                    st.markdown("""
                    <style>
                    /* 右ペイン第２カラムのサイズを強制的に2倍に設定 */
                    .stApp [data-testid="column"]:nth-child(2),
                    [data-testid="column"]:last-child,
                    div[data-testid="stHorizontalBlock"] > div:nth-child(2) {
                        font-size: 1.2rem !important;
                    }
                    
                    .stApp [data-testid="column"]:nth-child(2) h1,
                    .stApp [data-testid="column"]:nth-child(2) h2,
                    .stApp [data-testid="column"]:nth-child(2) h3,
                    .stApp [data-testid="column"]:nth-child(2) h4,
                    [data-testid="column"]:last-child h1,
                    [data-testid="column"]:last-child h2,
                    [data-testid="column"]:last-child h3,
                    [data-testid="column"]:last-child h4,
                    div[data-testid="stHorizontalBlock"] > div:nth-child(2) h1,
                    div[data-testid="stHorizontalBlock"] > div:nth-child(2) h2,
                    div[data-testid="stHorizontalBlock"] > div:nth-child(2) h3,
                    div[data-testid="stHorizontalBlock"] > div:nth-child(2) h4 {
                        font-size: 1.3rem !important;
                        margin: 0.6rem 0 !important;
                    }
                    
                    .stApp [data-testid="column"]:nth-child(2) [data-testid="metric-container"],
                    [data-testid="column"]:last-child [data-testid="metric-container"],
                    div[data-testid="stHorizontalBlock"] > div:nth-child(2) [data-testid="metric-container"] {
                        font-size: 1.0rem !important;
                        padding: 0.4rem !important;
                    }
                    
                    .stApp [data-testid="column"]:nth-child(2) [data-testid="metric-container"] label,
                    [data-testid="column"]:last-child [data-testid="metric-container"] label,
                    div[data-testid="stHorizontalBlock"] > div:nth-child(2) [data-testid="metric-container"] label {
                        font-size: 1.0rem !important;
                    }
                    
                    .stApp [data-testid="column"]:nth-child(2) [data-testid="metric-container"] [data-testid="metric-value"],
                    [data-testid="column"]:last-child [data-testid="metric-container"] [data-testid="metric-value"],
                    div[data-testid="stHorizontalBlock"] > div:nth-child(2) [data-testid="metric-container"] [data-testid="metric-value"] {
                        font-size: 1.1rem !important;
                    }
                    
                    .stApp [data-testid="column"]:nth-child(2) .stAlert,
                    [data-testid="column"]:last-child .stAlert,
                    div[data-testid="stHorizontalBlock"] > div:nth-child(2) .stAlert {
                        font-size: 1.0rem !important;
                        padding: 0.6rem !important;
                    }
                    
                    .stApp [data-testid="column"]:nth-child(2) p,
                    .stApp [data-testid="column"]:nth-child(2) div,
                    [data-testid="column"]:last-child p,
                    [data-testid="column"]:last-child div,
                    div[data-testid="stHorizontalBlock"] > div:nth-child(2) p,
                    div[data-testid="stHorizontalBlock"] > div:nth-child(2) div {
                        font-size: 1.2rem !important;
                        line-height: 1.4 !important;
                    }
                    </style>
                    """, unsafe_allow_html=True)
                    
                    # 統計情報表示（スタイル直接適用、さらに大きく）
                    
                    # クイック選択ボタンを右ペインの上部に配置
                    if 'ner_entities' in selected_article:
                        st.markdown('<div style="font-size: 1.2rem !important; font-weight: bold; margin: 0.4rem 0; color: #ff6b35;">🚀 クイック選択</div>', unsafe_allow_html=True)
                        
                        available_categories = list(selected_article['ner_entities'].keys())
                        category_names = {
                            'LAW_REFERENCE': '📚 法律参照',
                            'ARTICLE_REFERENCE': '📋 条文参照', 
                            'TIME_PERIOD': '⏰ 期間表現',
                            'MONEY_AMOUNT': '💰 金額表現',
                            'ORGANIZATION': '🏢 組織・機関',
                            'PROCEDURE': '⚙️ 手続き関連',
                            'LEGAL_STATUS': '⚖️ 法的地位'
                        }
                        
                        quick_categories = ['TIME_PERIOD', 'LAW_REFERENCE', 'ARTICLE_REFERENCE', 'ORGANIZATION']
                        
                        for cat in quick_categories:
                            if cat in available_categories:
                                if st.button(
                                    f"{category_names.get(cat, cat)} ({len(selected_article['ner_entities'][cat])}個)",
                                    key=f"quick_right_{cat}",
                                    help=f"{category_names.get(cat, cat)}を強調表示",
                                    use_container_width=True
                                ):
                                    st.session_state.selected_category = cat
                                    st.session_state.category_selection_source = "quick_button_right"
                                    st.rerun()
                        
                        # 区切り線
                        st.markdown("---")
                    
                    st.markdown('<div style="font-size: 1.3rem !important; font-weight: bold; margin: 0.6rem 0; color: #1f77b4;">📊 統計情報</div>', unsafe_allow_html=True)
                    
                    if not ner_df.empty:
                        # 全体統計
                        st.markdown('<div style="font-size: 1.2rem !important; font-weight: bold; margin: 0.4rem 0; color: #2e7d32;">📈 全体の固有表現統計</div>', unsafe_allow_html=True)
                        category_counts = ner_df['category'].value_counts()
                        
                        for category, count in category_counts.items():
                            st.metric(
                                label=category.replace('_', ' '),
                                value=f"{count}個"
                            )
                        
                        # 選択中条文の統計情報（読み取り専用）
                        if 'ner_entities' in selected_article:
                            st.markdown('<div style="font-size: 1.2rem !important; font-weight: bold; margin: 0.4rem 0; color: #d32f2f;">📊 現在の条文の固有表現</div>', unsafe_allow_html=True)
                            current_entities = selected_article['ner_entities']
                            total_current = sum(len(entities) for entities in current_entities.values())
                            
                            st.metric("合計", f"{total_current}個")
                            
                            # カテゴリ名の日本語表示
                            category_names = {
                                'LAW_REFERENCE': '📚 法律参照',
                                'ARTICLE_REFERENCE': '📋 条文参照', 
                                'TIME_PERIOD': '⏰ 期間表現',
                                'MONEY_AMOUNT': '💰 金額表現',
                                'ORGANIZATION': '🏢 組織・機関',
                                'PROCEDURE': '⚙️ 手続き関連',
                                'LEGAL_STATUS': '⚖️ 法的地位'
                            }
                            
                            # カテゴリ別表示（メトリック形式、クリック不可）
                            for category, entities in current_entities.items():
                                if entities:
                                    category_display = category_names.get(category, category.replace('_', ' '))
                                    is_selected = (st.session_state.selected_category == category or 
                                                  st.session_state.selected_category == "すべて")
                                    
                                    # 選択中の場合は特別な表示
                                    if is_selected:
                                        if st.session_state.selected_category == "すべて":
                                            st.metric(
                                                f"🎯 {category_display} (すべて強調中)",
                                                f"{len(entities)}個"
                                            )
                                        else:
                                            st.metric(
                                                f"🎯 {category_display} (強調中)",
                                                f"{len(entities)}個"
                                            )
                                    else:
                                        st.metric(
                                            category_display,
                                            f"{len(entities)}個"
                                        )
                            
                            # カテゴリ選択のヒント
                            st.info("💡 カテゴリを選択するには左パネルまたは上記のクイック選択ボタンをご利用ください")
                    else:
                        st.info("固有表現データが見つかりません。")
                
                # 関連条文表示（参照がある場合）
                if 'ner_entities' in selected_article and 'ARTICLE_REFERENCE' in selected_article['ner_entities']:
                    article_refs = selected_article['ner_entities']['ARTICLE_REFERENCE']
                    if article_refs:
                        st.markdown("#### 🔗 条文参照")
                        ref_texts = [ref['text'] for ref in article_refs]
                        st.markdown("この条文は以下の条文を参照しています: " + ", ".join(set(ref_texts)))

    # フッター
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
        特許法条文閲覧・固有表現抽出システム | 
        Powered by Streamlit & spaCy | 
        Built with ❤️ by GitHub Copilot
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
