"""
入れ子spanタグ問題を修正したhighlight_entities関数をテストするスクリプト
"""

import re
from bs4 import BeautifulSoup

def format_article_paragraphs(text):
    """条文テキストを項番号で改行して整形"""
    if not text:
        return text
    
    # 全角数字の項番号パターン（２、３、４...１０、１１...）の前で改行
    text = re.sub(r'(\s+)([２-９]|１[０-９])', r'\n\n\2', text)
    
    return text.strip()

def highlight_entities_nested_fix(text, entities, selected_category=None):
    """入れ子spanタグ問題を修正したハイライト関数"""
    if not entities:
        return text
    
    print(f"DEBUG: 入力テキスト長: {len(text)}")
    
    # 入力テキストのHTMLタグを完全に除去（安全のため）
    if '<' in text and '>' in text:
        try:
            soup = BeautifulSoup(text, 'html.parser')
            text = soup.get_text()
            text = re.sub(r'\s+', ' ', text).strip()
        except:
            text = re.sub(r'<[^>]+>', '', text)
            text = re.sub(r'\s+', ' ', text).strip()
    
    # 項番号での改行処理を適用
    text = format_article_paragraphs(text)
    
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
    
    # 重複除去（同じテキストは1回のみ）
    unique_entities = []
    seen_texts = set()
    for entity in all_entities:
        if entity['text'] not in seen_texts:
            unique_entities.append(entity)
            seen_texts.add(entity['text'])
    
    # テキスト長の降順でソート（長い表現を先に処理）
    unique_entities.sort(key=lambda x: len(x['text']), reverse=True)
    
    print(f"DEBUG: 重複除去後のエンティティ: {[e['text'] for e in unique_entities]}")
    
    # ★ 入れ子防止: 重複するエンティティを除去
    # 長いエンティティを優先し、短いエンティティがその一部の場合は除去
    filtered_entities = []
    for i, entity in enumerate(unique_entities):
        is_subset = False
        for j, other_entity in enumerate(unique_entities):
            if i != j and len(other_entity['text']) > len(entity['text']):
                # 他のエンティティがより長く、現在のエンティティがその一部の場合
                if entity['text'] in other_entity['text']:
                    is_subset = True
                    print(f"DEBUG: Skipping '{entity['text']}' (subset of '{other_entity['text']}')")
                    break
        
        if not is_subset:
            filtered_entities.append(entity)
    
    print(f"DEBUG: Original entities: {len(unique_entities)}, Filtered: {len(filtered_entities)}")
    print(f"DEBUG: 処理対象エンティティ: {[e['text'] for e in filtered_entities]}")
    unique_entities = filtered_entities
    
    # ハイライト処理
    highlighted_text = text
    for i, entity in enumerate(unique_entities, 1):
        # カテゴリによる色選択
        if selected_category == "すべて" or (selected_category and entity['category'] == selected_category):
            color = highlight_colors.get(entity['category'], '#FFD700')
            border_style = "border: 2px solid #FF6B6B; box-shadow: 0 0 10px rgba(255, 107, 107, 0.5);"
        else:
            color = normal_colors.get(entity['category'], '#F5F5F5')
            border_style = ""
        
        entity_text = entity['text']
        
        # ★ 入れ子を防ぐための厳密なチェック
        if (entity_text in highlighted_text and 
            f'>{entity_text}</span>' not in highlighted_text):
            
            # さらに詳細なチェック: エンティティの前後にspanタグがないか確認
            entity_start = highlighted_text.find(entity_text)
            if entity_start != -1:
                # エンティティの前後50文字をチェック
                before_text = highlighted_text[max(0, entity_start-50):entity_start]
                after_text = highlighted_text[entity_start+len(entity_text):entity_start+len(entity_text)+50]
                
                # spanタグの内部でないかチェック
                open_spans_before = before_text.count('<span') - before_text.count('</span>')
                if open_spans_before > 0:
                    print(f"DEBUG: Skipping '{entity_text}' - inside existing span tag")
                    continue
                
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
                
                # HTMLタグを一行で確実に構築
                style_attrs = f"background-color: {color}; padding: 1px 3px; margin: 0 1px; border-radius: 3px; font-weight: 500; border: 1px solid {color}88; {border_style}"
                highlighted_part = f'<span style="{style_attrs}" title="{category_jp}: {entity_text}">{entity_text}</span>'
                
                print(f"DEBUG: エンティティ {i}: '{entity_text}' -> 処理中")
                
                # 置換処理
                old_highlighted_text = highlighted_text
                highlighted_text = highlighted_text.replace(entity_text, highlighted_part, 1)
                
                # 置換が実際に行われたかチェック
                if old_highlighted_text == highlighted_text:
                    print(f"WARNING: 置換されませんでした '{entity_text}'")
                else:
                    print(f"SUCCESS: 置換成功 '{entity_text}'")
                
                # spanタグの整合性をチェック
                span_open_count = highlighted_text.count('<span')
                span_close_count = highlighted_text.count('</span>')
                if span_open_count != span_close_count:
                    print(f"ERROR: spanタグ不整合 '{entity_text}' - 開始: {span_open_count}, 終了: {span_close_count}")
                    highlighted_text = old_highlighted_text
                    print(f"RECOVERY: 前の状態に復元 '{entity_text}'")
        else:
            print(f"SKIP: スキップ '{entity_text}' (既にハイライト済みまたは見つからない)")
    
    # 最終的なspanタグ整合性チェック
    final_span_open = highlighted_text.count('<span')
    final_span_close = highlighted_text.count('</span>')
    print(f"DEBUG: 最終spanタグ数 - 開始: {final_span_open}, 終了: {final_span_close}")
    
    if final_span_open != final_span_close:
        print(f"CRITICAL ERROR: 最終spanタグ不整合 - 開始: {final_span_open}, 終了: {final_span_close}")
        highlighted_text = re.sub(r'<span[^>]*>', '', highlighted_text)
        highlighted_text = highlighted_text.replace('</span>', '')
        print("EMERGENCY RECOVERY: すべてのspanタグを除去、プレーンテキストで返却")
    else:
        print("SUCCESS: 最終的なspanタグ整合性OK")
    
    return highlighted_text

def test_nested_span_fix():
    """入れ子spanタグ問題の修正をテスト"""
    
    # 入れ子問題を再現するテストケース
    test_text = """２ 特許出願、請求その他特許に関する手続（以下単に「手続」という。）についての期間の末日が行政機関の休日に関する法律（昭和六十三年法律第九十一号）第一条第一項各号に掲げる日に当たるときは、その日の翌日をもつてその期間の末日とする。"""
    
    # 意図的に重複・入れ子を作るエンティティセット
    entities = {
        'LAW_REFERENCE': [
            {'text': '昭和六十三年法律第九十一号', 'start': 0, 'end': 0},  # 長いエンティティ
            {'text': '法律', 'start': 0, 'end': 0},  # 短いエンティティ（重複）
        ],
        'ARTICLE_REFERENCE': [
            {'text': '第一条第一項各号', 'start': 0, 'end': 0},  # 長いエンティティ
            {'text': '第一条', 'start': 0, 'end': 0},  # 短いエンティティ（重複）
            {'text': '第一項', 'start': 0, 'end': 0},  # 短いエンティティ（重複）
        ],
        'PROCEDURE': [
            {'text': '手続', 'start': 0, 'end': 0},
            {'text': '出願', 'start': 0, 'end': 0}
        ]
    }
    
    print("=== 入れ子spanタグ問題修正のテスト ===")
    print(f"入力テキスト: {test_text}")
    print(f"潜在的な問題エンティティ:")
    for category, entity_list in entities.items():
        print(f"  {category}: {[e['text'] for e in entity_list]}")
    
    # 修正されたハイライト処理を実行
    result = highlight_entities_nested_fix(test_text, entities, selected_category="すべて")
    
    print(f"\n=== 結果 ===")
    print(f"出力長: {len(result)}")
    print(f"結果: {result}")
    
    # 最終検証
    span_open = result.count('<span')
    span_close = result.count('</span>')
    print(f"\n=== 最終検証 ===")
    print(f"<spanタグ開始数: {span_open}")
    print(f"</spanタグ終了数: {span_close}")
    
    # 入れ子チェック
    nested_spans = 0
    current_pos = 0
    while True:
        span_start = result.find('<span', current_pos)
        if span_start == -1:
            break
        span_end = result.find('</span>', span_start)
        if span_end == -1:
            break
        
        # この範囲内に別のspanタグがあるかチェック
        inner_span = result.find('<span', span_start + 1)
        if inner_span != -1 and inner_span < span_end:
            nested_spans += 1
            print(f"NESTED SPAN DETECTED: {result[span_start:span_end+7]}")
        
        current_pos = span_end + 7
    
    print(f"入れ子spanタグ数: {nested_spans}")
    
    if span_open == span_close and nested_spans == 0:
        print("✅ 修正成功: spanタグの整合性OK、入れ子なし")
    else:
        print("⚠️ 問題が残存しています")
    
    # HTMLファイルとして保存
    with open('test_nested_span_fix.html', 'w', encoding='utf-8') as f:
        f.write(f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>入れ子spanタグ修正テスト</title>
</head>
<body>
    <h1>入れ子spanタグ修正テスト</h1>
    <h2>入力:</h2>
    <div style="border: 1px solid #ccc; padding: 10px; margin: 10px;">
        {test_text}
    </div>
    <h2>出力:</h2>
    <div style="border: 1px solid #ccc; padding: 10px; margin: 10px;">
        {result}
    </div>
    <h2>検証結果:</h2>
    <ul>
        <li>spanタグ開始数: {span_open}</li>
        <li>spanタグ終了数: {span_close}</li>
        <li>入れ子spanタグ数: {nested_spans}</li>
        <li>整合性: {'✅ OK' if span_open == span_close and nested_spans == 0 else '⚠️ NG'}</li>
    </ul>
</body>
</html>
""")
    
    print("\nテスト結果を test_nested_span_fix.html に保存しました")

if __name__ == "__main__":
    test_nested_span_fix()
