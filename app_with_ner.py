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
        # カテゴリが選択されている場合は強調色、そうでなければ通常色を使用
        if selected_category and entity['category'] == selected_category:
            color = highlight_colors.get(entity['category'], '#FFD700')  # ゴールド色
            border_style = "border: 2px solid #FF6B6B; box-shadow: 0 0 10px rgba(255, 107, 107, 0.5);"
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

def display_entity_legend():
    """固有表現の凡例を表示"""
    st.sidebar.markdown("### 🏷️ 固有表現の種類")
    
    legend_items = [
        ('LAW_REFERENCE', '法律参照', '#FFF2F2'),
        ('ARTICLE_REFERENCE', '条文参照', '#F0F8FF'),
        ('TIME_PERIOD', '期間表現', '#F0FFF0'),
        ('MONEY_AMOUNT', '金額表現', '#FFFEF0'),
        ('ORGANIZATION', '組織・機関', '#F8F0FF'),
        ('PROCEDURE', '手続き関連', '#FFF0F8'),
        ('LEGAL_STATUS', '法的地位・状態', '#F0FFFF'),
    ]
    
    for category, description, color in legend_items:
        st.sidebar.markdown(
            f'<div style="background-color: {color}; padding: 6px 10px; margin: 3px 0; '
            f'border-radius: 5px; font-size: 13px; border: 1px solid {color}88;">'
            f'<strong>{description}</strong><br>'
            f'<small style="color: #666;">({category})</small></div>',
            unsafe_allow_html=True
        )

def main():
    st.title("⚖️ 特許法条文閲覧・固有表現抽出システム")
    st.markdown("---")
    
    # データ読み込み
    with st.spinner("データを読み込み中..."):
        data = load_data()
        ner_df = load_ner_csv()
    
    if not data:
        st.error("データの読み込みに失敗しました。")
        return
    
    # サイドバー: 固有表現の凡例
    display_entity_legend()
    
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
            
            selected_article_idx = st.sidebar.selectbox(
                "条文を選択してください:",
                range(len(article_titles)),
                format_func=lambda x: article_titles[x]
            )
            
            if selected_article_idx is not None:
                selected_article = articles[selected_article_idx]
                
                # メインコンテンツ表示
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # 条文表示
                    article_title = selected_article.get('title', selected_article.get('heading', '条文'))
                    st.subheader(f"📄 {article_title}")
                    
                    article_text = get_article_text(selected_article)
                    
                    # 表示モード選択
                    display_mode = st.radio(
                        "表示モード:",
                        ["原文表示", "ハイライト表示"],
                        horizontal=True,
                        help="原文表示：元のテキストをそのまま表示 / ハイライト表示：固有表現をカラーハイライト"
                    )
                    
                    if display_mode == "ハイライト表示" and 'ner_entities' in selected_article:
                        # カテゴリ選択機能を追加
                        st.markdown("#### 🎯 固有表現カテゴリ選択")
                        
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
                        
                        # ラジオボタンでカテゴリ選択
                        selected_category = st.radio(
                            "強調表示するカテゴリを選択:",
                            ["すべて"] + available_categories,
                            format_func=lambda x: "🌈 すべてのカテゴリ" if x == "すべて" else category_names.get(x, x),
                            horizontal=True,
                            help="特定のカテゴリを選択すると、そのカテゴリの固有表現が強調表示されます"
                        )
                        
                        # カテゴリ別クイック選択ボタン
                        st.markdown("**🚀 クイック選択:**")
                        cols = st.columns(4)
                        quick_categories = ['TIME_PERIOD', 'LAW_REFERENCE', 'ARTICLE_REFERENCE', 'ORGANIZATION']
                        
                        for i, cat in enumerate(quick_categories):
                            if cat in available_categories:
                                with cols[i % 4]:
                                    if st.button(
                                        f"{category_names.get(cat, cat)}\n({len(selected_article['ner_entities'][cat])}個)",
                                        key=f"quick_{cat}",
                                        help=f"{category_names.get(cat, cat)}を強調表示"
                                    ):
                                        selected_category = cat
                        
                        # 選択されたカテゴリに応じてハイライト
                        highlight_category = None if selected_category == "すべて" else selected_category
                        highlighted_text = highlight_entities(article_text, selected_article['ner_entities'], highlight_category)
                        
                        st.markdown("#### 🎨 固有表現ハイライト表示")
                        if selected_category != "すべて":
                            st.info(f"💡 {category_names.get(selected_category, selected_category)} が強調表示されています")
                        st.markdown(highlighted_text, unsafe_allow_html=True)
                        
                        # 原文も併記（折りたたみ表示）
                        with st.expander("📝 原文を確認"):
                            st.text_area(
                                "原文テキスト",
                                article_text,
                                height=200,
                                disabled=True,
                                label_visibility="collapsed"
                            )
                    else:
                        # 原文表示（デフォルト）
                        st.markdown("#### 📝 原文")
                        st.text_area(
                            "条文内容",
                            article_text,
                            height=300,
                            disabled=True,
                            label_visibility="collapsed"
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
                
                with col2:
                    # 統計情報表示
                    st.subheader("📊 統計情報")
                    
                    if not ner_df.empty:
                        # 全体統計
                        st.markdown("#### 全体の固有表現統計")
                        category_counts = ner_df['category'].value_counts()
                        
                        for category, count in category_counts.items():
                            st.metric(
                                label=category.replace('_', ' '),
                                value=f"{count}個"
                            )
                        
                        # 選択中条文の統計
                        if 'ner_entities' in selected_article:
                            st.markdown("#### 選択中条文の固有表現")
                            current_entities = selected_article['ner_entities']
                            total_current = sum(len(entities) for entities in current_entities.values())
                            st.metric("合計", f"{total_current}個")
                            
                            # カテゴリ別統計（選択されたカテゴリは強調表示）
                            for category, entities in current_entities.items():
                                if entities:
                                    category_display = category.replace('_', ' ')
                                    # 選択されたカテゴリは強調表示
                                    if 'selected_category' in locals() and category == selected_category:
                                        st.markdown(f"**🎯 {category_display}** (選択中)")
                                        st.metric(
                                            label="",
                                            value=f"{len(entities)}個",
                                            delta=f"強調表示中",
                                            delta_color="normal"
                                        )
                                    else:
                                        st.metric(
                                            label=category_display,
                                            value=f"{len(entities)}個"
                                        )
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
