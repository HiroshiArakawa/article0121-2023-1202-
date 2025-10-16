"""
実際のStreamlitアプリでの表示をテストするスクリプト
注意: このスクリプトは元のapp_with_ner.pyの一部をシミュレートしています
"""

def test_app_display():
    """アプリでの表示をシミュレートしてテスト"""
    
    # ユーザーが報告したテキスト
    test_text = """２ 特許出願、請求その他特許に関する手続（以下単に「手続」という。）についての期間の末日が行政機関の休日に関する法律（昭和六十三年法律第九十一号）第一条第一項各号に掲げる日に当たるときは、その日の翌日をもつてその期間の末日とする。"""
    
    print("=== 実際のアプリ表示テスト ===")
    print(f"入力テキスト: {test_text}")
    
    # エンティティを模擬
    entities = {
        'LAW_REFERENCE': [
            {'text': '昭和六十三年法律第九十一号', 'start': 0, 'end': 0}
        ]
    }
    
    # 実際のhighlight_entitiesロジックを使用
    from bs4 import BeautifulSoup
    import re
    
    # HTMLタグ除去
    if '<' in test_text and '>' in test_text:
        try:
            soup = BeautifulSoup(test_text, 'html.parser')
            text = soup.get_text()
            text = re.sub(r'\s+', ' ', text).strip()
        except:
            text = re.sub(r'<[^>]+>', '', test_text)
            text = re.sub(r'\s+', ' ', text).strip()
    else:
        text = test_text
    
    # 項番号での改行処理（格納データの全角数字改行機能を模擬）
    # format_article_paragraphs相当の処理
    text = format_article_paragraphs_mock(text)
    
    print(f"前処理後のテキスト: {text}")
    
    # ハイライト処理
    highlighted = simulate_full_highlight_process(text, entities, "すべて")
    
    print(f"\nハイライト結果:")
    print(highlighted)
    
    # Streamlitでの表示で起こりそうな問題をチェック
    print(f"\n=== Streamlit表示での潜在的問題チェック ===")
    
    # 1. HTMLタグの妥当性チェック
    span_open = highlighted.count('<span')
    span_close = highlighted.count('</span>')
    print(f"<span開始タグ数: {span_open}")
    print(f"</span終了タグ数: {span_close}")
    
    if span_open != span_close:
        print("⚠️ タグの不一致が検出されました！")
    else:
        print("✅ タグの数は一致しています")
    
    # 2. 非常に長いスタイル属性による問題の可能性
    long_styles = re.findall(r'style="[^"]{100,}"', highlighted)
    if long_styles:
        print(f"⚠️ 非常に長いstyle属性が見つかりました: {len(long_styles)}個")
        for style in long_styles[:2]:  # 最初の2個だけ表示
            print(f"   {style[:100]}...")
    else:
        print("✅ 過度に長いstyle属性はありません")
    
    # 3. 特殊文字の問題
    special_chars = ['&', '<', '>', '"', "'"]
    for char in special_chars:
        count = highlighted.count(char)
        if count > 0:
            print(f"特殊文字 '{char}': {count}個")
    
    # 4. HTMLエンティティエスケープをテスト
    import html
    escaped = html.escape(highlighted)
    if len(escaped) != len(highlighted):
        print(f"⚠️ HTMLエスケープが必要: 元の長さ{len(highlighted)} → エスケープ後{len(escaped)}")
    else:
        print("✅ HTMLエスケープは不要")
    
    # 5. テストファイルを出力
    with open('streamlit_display_test.html', 'w', encoding='utf-8') as f:
        f.write(f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Streamlit表示テスト</title>
    <style>
        .test-container {{
            padding: 20px;
            border: 1px solid #ccc;
            margin: 10px;
            font-family: "Source Sans Pro", sans-serif;
        }}
    </style>
</head>
<body>
    <h1>Streamlit表示テスト</h1>
    <div class="test-container">
        <h2>入力テキスト:</h2>
        <p>{test_text}</p>
        
        <h2>ハイライト結果:</h2>
        <p>{highlighted}</p>
        
        <h2>診断結果:</h2>
        <ul>
            <li>span開始タグ数: {span_open}</li>
            <li>span終了タグ数: {span_close}</li>
            <li>タグ整合性: {'✅ 正常' if span_open == span_close else '⚠️ 不整合'}</li>
        </ul>
    </div>
</body>
</html>
""")
    
    print("\nテスト結果を streamlit_display_test.html に保存しました")

def format_article_paragraphs_mock(text):
    """format_article_paragraphs関数の模擬実装"""
    if not text:
        return text
    
    # 全角数字パターンの前で改行
    import re
    # ２、３、４...１０、１１...の前で改行
    text = re.sub(r'(\s+)([２-９]|１[０-９])', r'\n\n\2', text)
    
    return text.strip()

def simulate_full_highlight_process(text, entities, selected_category=None):
    """完全なハイライト処理のシミュレーション"""
    if not entities:
        return text
    
    # エンティティの色分け
    normal_colors = {
        'LAW_REFERENCE': '#FFF2F2',
        'ARTICLE_REFERENCE': '#F0F8FF',
        'TIME_PERIOD': '#F0FFF0',
        'MONEY_AMOUNT': '#FFFEF0',
        'ORGANIZATION': '#F8F0FF',
        'PROCEDURE': '#FFF0F8',
        'LEGAL_STATUS': '#F0FFFF',
    }
    
    highlight_colors = {
        'LAW_REFERENCE': '#FFB6C1',
        'ARTICLE_REFERENCE': '#87CEEB',
        'TIME_PERIOD': '#98FB98',
        'MONEY_AMOUNT': '#F0E68C',
        'ORGANIZATION': '#DDA0DD',
        'PROCEDURE': '#FFB6C1',
        'LEGAL_STATUS': '#AFEEEE',
    }
    
    # エンティティを収集し、テキスト長の降順でソート
    all_entities = []
    for category, entity_list in entities.items():
        for entity in entity_list:
            entity_text = entity['text']
            if entity_text in text:
                all_entities.append({
                    'text': entity_text,
                    'category': category
                })
    
    # 重複除去
    unique_entities = []
    seen_texts = set()
    for entity in all_entities:
        if entity['text'] not in seen_texts:
            unique_entities.append(entity)
            seen_texts.add(entity['text'])
    
    # テキスト長の降順でソート
    unique_entities.sort(key=lambda x: len(x['text']), reverse=True)
    
    # ハイライト処理
    highlighted_text = text
    for entity in unique_entities:
        # カテゴリが選択されている場合、または「すべて」が選択されている場合は強調色と赤枠を適用
        if selected_category == "すべて" or (selected_category and entity['category'] == selected_category):
            color = highlight_colors.get(entity['category'], '#FFD700')
            border_style = "border: 2px solid #FF6B6B; box-shadow: 0 0 10px rgba(255, 107, 107, 0.5);"
        else:
            color = normal_colors.get(entity['category'], '#F5F5F5')
            border_style = ""
        
        entity_text = entity['text']
        
        # 既にハイライトされていないかチェック
        if entity_text in highlighted_text and f'>{entity_text}</span>' not in highlighted_text:
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
            
            # 実際のコードと同じ方法でspanタグを構築
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

if __name__ == "__main__":
    test_app_display()
