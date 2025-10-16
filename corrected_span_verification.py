"""
正規表現の検証を修正したデバッグスクリプト
"""

import re

def verify_span_tags(html_text):
    """spanタグの検証を正確に行う"""
    print("=== spanタグ検証（修正版） ===")
    
    # 開始タグと終了タグの数をカウント
    span_open_count = html_text.count('<span')
    span_close_count = html_text.count('</span>')
    print(f"<spanタグ開始数: {span_open_count}")
    print(f"</spanタグ終了数: {span_close_count}")
    
    # 不完全なspanタグをより正確に検出
    # 修正した正規表現: <span で始まって > で終わらないパターン
    incomplete_spans = re.findall(r'<span(?:[^>])*$', html_text, re.MULTILINE)
    print(f"行末で終わる不完全spanタグ: {len(incomplete_spans)}")
    
    # すべてのspanタグを抽出して検証
    all_span_tags = re.findall(r'<span[^>]*>', html_text)
    print(f"検出されたspanタグ数: {len(all_span_tags)}")
    
    if len(all_span_tags) > 0:
        print("最初の3個のspanタグ:")
        for i, tag in enumerate(all_span_tags[:3], 1):
            print(f"  {i}: {tag}")
    
    # 終了タグも確認
    all_close_tags = re.findall(r'</span>', html_text)
    print(f"検出された</span>タグ数: {len(all_close_tags)}")
    
    if span_open_count == span_close_count and span_open_count == len(all_span_tags):
        print("✅ すべてのspanタグが正常に形成されています")
        return True
    else:
        print("⚠️ spanタグに問題があります")
        return False

def test_with_actual_app_code():
    """実際のapp_with_ner.pyと同じコードを使用してテスト"""
    print("\n=== 実際のアプリコードでのテスト ===")
    
    # ユーザーが報告したテキスト
    text = """２ 特許出願、請求その他特許に関する手続（以下単に「手続」という。）についての期間の末日が行政機関の休日に関する法律（昭和六十三年法律第九十一号）第一条第一項各号に掲げる日に当たるときは、その日の翌日をもつてその期間の末日とする。"""
    
    # エンティティを模擬
    entities = {
        'LAW_REFERENCE': [
            {'text': '昭和六十三年法律第九十一号', 'start': 0, 'end': 0}
        ]
    }
    
    # 実際のhighlight_entitiesと同じロジックを使用
    highlighted_text = simulate_highlight_entities(text, entities, selected_category="すべて")
    
    print(f"ハイライト後のテキスト:")
    print(highlighted_text)
    
    # 検証
    is_valid = verify_span_tags(highlighted_text)
    
    return highlighted_text, is_valid

def simulate_highlight_entities(text, entities, selected_category=None):
    """app_with_ner.pyのhighlight_entitiesと同じロジックを模擬"""
    if not entities:
        return text
    
    # エンティティの色分け
    normal_colors = {
        'LAW_REFERENCE': '#FFF2F2',
    }
    
    highlight_colors = {
        'LAW_REFERENCE': '#FFB6C1',
    }
    
    # エンティティを収集
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
        # カテゴリによる色選択
        if selected_category == "すべて" or (selected_category and entity['category'] == selected_category):
            color = highlight_colors.get(entity['category'], '#FFD700')
            border_style = "border: 2px solid #FF6B6B; box-shadow: 0 0 10px rgba(255, 107, 107, 0.5);"
        else:
            color = normal_colors.get(entity['category'], '#F5F5F5')
            border_style = ""
        
        entity_text = entity['text']
        
        # 重複チェック（実際のコードと同じ）
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
            
            # **これが実際のコードと同じ部分**
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

def main():
    # テストを実行
    result_text, is_valid = test_with_actual_app_code()
    
    # 結果をファイルに保存
    with open('corrected_debug_result.html', 'w', encoding='utf-8') as f:
        f.write(f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>修正されたデバッグ結果</title>
</head>
<body>
    <h1>修正されたデバッグ結果</h1>
    <h2>検証結果: {'✅ 正常' if is_valid else '⚠️ 問題あり'}</h2>
    <div style="border: 1px solid #ccc; padding: 10px; margin: 10px;">
        {result_text}
    </div>
</body>
</html>
""")
    
    print(f"\n修正されたデバッグ結果を corrected_debug_result.html に保存しました")
    
    if is_valid:
        print("\n結論: spanタグは正しく生成されています。")
        print("ユーザーが見ている問題は他の原因（Streamlitの表示問題など）と思われます。")
    else:
        print("\n結論: spanタグに問題があります。")

if __name__ == "__main__":
    main()
