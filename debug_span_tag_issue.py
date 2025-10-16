"""
<span>タグが正しく閉じられない問題をデバッグするスクリプト
"""

import pickle
import re
from bs4 import BeautifulSoup

def format_article_paragraphs(text):
    """条文テキストを項番号で改行して整形"""
    if not text:
        return text
    
    # 全角数字の項番号パターン（２、３、４...１０、１１...）の前で改行
    text = re.sub(r'(?<=\S)(?=[\s]*[２３４５６７８９１０１１１２１３１４１５１６１７１８１９２０])', '\n', text)
    
    # 漢数字の項番号パターン（一、二、三...）の前で改行
    text = re.sub(r'(?<=\S)(?=[\s]*[一二三四五六七八九十])', '\n', text)
    
    # 連続する改行を整理
    text = re.sub(r'\n+', '\n', text)
    
    return text

def highlight_entities(text, entities, selected_category=None):
    """テキスト中の固有表現をハイライト（デバッグ版）"""
    if not entities:
        return text
    
    print(f"DEBUG: 入力テキスト: {text[:100]}...")
    print(f"DEBUG: selected_category: {selected_category}")
    
    # 入力テキストのHTMLタグを完全に除去（安全のため）
    if '<' in text and '>' in text:
        try:
            soup = BeautifulSoup(text, 'html.parser')
            text = soup.get_text()
            # 連続する空白や改行を整理
            text = re.sub(r'\s+', ' ', text).strip()
        except:
            # BeautifulSoupが使えない場合は正規表現で除去
            text = re.sub(r'<[^>]+>', '', text)
            text = re.sub(r'\s+', ' ', text).strip()
    
    # 項番号での改行処理を適用
    text = format_article_paragraphs(text)
    
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
    
    print(f"DEBUG: 見つかったエンティティ数: {len(all_entities)}")
    
    # 重複除去（同じテキストは1回のみ）
    unique_entities = []
    seen_texts = set()
    for entity in all_entities:
        if entity['text'] not in seen_texts:
            unique_entities.append(entity)
            seen_texts.add(entity['text'])
    
    # テキスト長の降順でソート（長い表現を先に処理）
    unique_entities.sort(key=lambda x: len(x['text']), reverse=True)
    
    print(f"DEBUG: 重複除去後のエンティティ数: {len(unique_entities)}")
    
    # ハイライト処理
    highlighted_text = text
    for i, entity in enumerate(unique_entities):
        # カテゴリが選択されている場合、または「すべて」が選択されている場合は強調色と赤枠を適用
        if selected_category == "すべて" or (selected_category and entity['category'] == selected_category):
            color = highlight_colors.get(entity['category'], '#FFD700')  # ゴールド色
            border_style = "border: 2px solid #FF6B6B; box-shadow: 0 0 10px rgba(255, 107, 107, 0.5);"
            print(f"DEBUG: 強調表示適用 -> {entity['text']} (category: {entity['category']})")
        else:
            color = normal_colors.get(entity['category'], '#F5F5F5')
            border_style = ""
        
        entity_text = entity['text']
        
        # 既にハイライトされていないかチェック（より正確な条件）
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
            
            highlighted_part = (
                f'<span style="background-color: {color}; '
                f'padding: 1px 3px; margin: 0 1px; border-radius: 3px; '
                f'font-weight: 500; border: 1px solid {color}88; {border_style}" '
                f'title="{category_jp}: {entity_text}">'
                f'{entity_text}</span>'
            )
            
            print(f"DEBUG: エンティティ {i+1}: '{entity_text}'")
            print(f"DEBUG: 生成されたスパンタグ: {highlighted_part}")
            
            # 最初の出現箇所のみ置換
            old_text = highlighted_text
            highlighted_text = highlighted_text.replace(entity_text, highlighted_part, 1)
            
            if old_text != highlighted_text:
                print(f"DEBUG: 置換成功")
            else:
                print(f"DEBUG: 置換失敗 - テキストが見つからない")
        else:
            print(f"DEBUG: スキップ - '{entity_text}' (既にハイライト済みまたはテキストに存在しない)")
    
    print(f"DEBUG: 最終結果の長さ: {len(highlighted_text)}")
    print(f"DEBUG: 最終結果（最初の200文字）: {highlighted_text[:200]}")
    
    return highlighted_text

def main():
    # pickleファイルを読み込み
    pickle_file = "334AC0000000121_20230703_505AC0000000051_with_ner_fixed.pickle"
    
    try:
        with open(pickle_file, 'rb') as f:
            data = pickle.load(f)
        print(f"pickleファイル読み込み成功: {len(data)}件")
    except FileNotFoundError:
        print(f"エラー: {pickle_file} が見つかりません")
        return
    
    # 第64条を検索
    article_64 = None
    for item in data:
        if isinstance(item, dict) and 'article_number' in item:
            if item['article_number'] == '第六十四条':
                article_64 = item
                break
    
    if not article_64:
        print("第64条が見つかりません")
        return
    
    print(f"第64条を発見: {article_64.get('title', 'タイトルなし')}")
    
    # テキストを取得
    text = article_64.get('text', '')
    if not text:
        text = article_64.get('body', '')
    if not text:
        text = article_64.get('content', '')
    
    print(f"元のテキスト: {text[:200]}...")
    
    # NERエンティティを取得
    entities = article_64.get('ner_entities', {})
    print(f"エンティティカテゴリ数: {len(entities)}")
    for category, entity_list in entities.items():
        print(f"  {category}: {len(entity_list)}個")
    
    # ハイライト処理をテスト（すべてのカテゴリ）
    print("\n=== すべてのカテゴリでハイライトテスト ===")
    highlighted = highlight_entities(text, entities, selected_category="すべて")
    
    # 結果を分析
    print(f"\n=== 結果分析 ===")
    print(f"ハイライト後の長さ: {len(highlighted)}")
    
    # <spanタグの数をカウント
    span_open_count = highlighted.count('<span')
    span_close_count = highlighted.count('</span>')
    print(f"<spanタグ開始数: {span_open_count}")
    print(f"</spanタグ終了数: {span_close_count}")
    
    if span_open_count != span_close_count:
        print("⚠️ <spanタグの開始と終了の数が一致しません！")
    else:
        print("✅ <spanタグの開始と終了の数が一致しています")
    
    # 不完全なspanタグを検索
    import re
    incomplete_spans = re.findall(r'<span[^>]*(?!>)', highlighted)
    if incomplete_spans:
        print(f"⚠️ 不完全な<spanタグが見つかりました: {len(incomplete_spans)}個")
        for i, span in enumerate(incomplete_spans[:3]):  # 最初の3個だけ表示
            print(f"  {i+1}: {span}")
    else:
        print("✅ 不完全な<spanタグは見つかりませんでした")
    
    # 結果をファイルに保存
    with open('debug_highlight_result.html', 'w', encoding='utf-8') as f:
        f.write(f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>ハイライト結果デバッグ</title>
</head>
<body>
    <h1>ハイライト結果</h1>
    <div style="border: 1px solid #ccc; padding: 10px; margin: 10px;">
        {highlighted}
    </div>
</body>
</html>
""")
    
    print("\n結果を debug_highlight_result.html に保存しました")

if __name__ == "__main__":
    main()
