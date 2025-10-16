"""
ユーザーが報告した具体的なケースを再現するデバッグスクリプト
「昭和六十三年法律第九十一号」のハイライト問題を調査
"""

import re

def debug_specific_case():
    """ユーザーが報告した具体的なケースをデバッグ"""
    
    # ユーザーが報告したテキスト
    problem_text = """２ 特許出願、請求その他特許に関する手続（以下単に「手続」という。）についての期間の末日が行政機関の休日に関する法律（昭和六十三年法律第九十一号）第一条第一項各号に掲げる日に当たるときは、その日の翌日をもつてその期間の末日とする。"""
    
    print("=== ユーザー報告ケースのデバッグ ===")
    print(f"問題のテキスト: {problem_text}")
    
    # エンティティを模擬的に作成
    entities = {
        'LAW_REFERENCE': [
            {'text': '昭和六十三年法律第九十一号', 'start': 0, 'end': 0}
        ]
    }
    
    # カラー設定
    highlight_colors = {
        'LAW_REFERENCE': '#FFB6C1',
    }
    
    entity_text = '昭和六十三年法律第九十一号'
    color = highlight_colors['LAW_REFERENCE']
    border_style = "border: 2px solid #FF6B6B; box-shadow: 0 0 10px rgba(255, 107, 107, 0.5);"
    category_jp = '法律参照'
    
    # 実際のhighlight_entitiesコードと同じロジックで生成
    highlighted_part = (
        f'<span style="background-color: {color}; '
        f'padding: 1px 3px; margin: 0 1px; border-radius: 3px; '
        f'font-weight: 500; border: 1px solid {color}88; {border_style}" '
        f'title="{category_jp}: {entity_text}">'
        f'{entity_text}</span>'
    )
    
    print(f"\n生成されたspanタグ:")
    print(highlighted_part)
    
    # spanタグの構造を詳しく分析
    print(f"\n=== spanタグ構造分析 ===")
    print(f"開始タグ部分: <span style=\"...\" title=\"...\">")
    print(f"内容: {entity_text}")
    print(f"終了タグ: </span>")
    
    # 実際の置換処理
    highlighted_text = problem_text.replace(entity_text, highlighted_part, 1)
    
    print(f"\n=== 置換結果 ===")
    print(highlighted_text)
    
    # spanタグの開始と終了をカウント
    span_open_count = highlighted_text.count('<span')
    span_close_count = highlighted_text.count('</span>')
    print(f"\n<spanタグ開始数: {span_open_count}")
    print(f"</spanタグ終了数: {span_close_count}")
    
    # 不完全なspanタグをチェック
    incomplete_spans = re.findall(r'<span[^>]*(?!>)', highlighted_text)
    if incomplete_spans:
        print(f"⚠️ 不完全な<spanタグ: {incomplete_spans}")
    else:
        print("✅ すべてのspanタグが正しく形成されています")
    
    # HTMLファイルとして保存
    with open('debug_specific_case.html', 'w', encoding='utf-8') as f:
        f.write(f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>特定ケースデバッグ</title>
</head>
<body>
    <h1>ユーザー報告ケースのデバッグ結果</h1>
    <h2>元のテキスト:</h2>
    <div style="border: 1px solid #ccc; padding: 10px; margin: 10px;">
        {problem_text}
    </div>
    <h2>ハイライト後:</h2>
    <div style="border: 1px solid #ccc; padding: 10px; margin: 10px;">
        {highlighted_text}
    </div>
</body>
</html>
""")
    
    print("\n結果を debug_specific_case.html に保存しました")
    
    # 追加の検証: Streamlitで使われる可能性のある処理をシミュレート
    print(f"\n=== Streamlit環境での追加検証 ===")
    
    # st.markdownで使われる可能性のあるHTMLエスケープをシミュレート
    import html
    escaped_text = html.escape(highlighted_text)
    print(f"HTMLエスケープ後: {escaped_text[:200]}...")
    
    # 文字エンコーディングの問題をチェック
    try:
        encoded = highlighted_text.encode('utf-8')
        decoded = encoded.decode('utf-8')
        print("✅ UTF-8エンコーディング: 問題なし")
    except Exception as e:
        print(f"⚠️ エンコーディングエラー: {e}")

def analyze_app_code():
    """実際のapp_with_ner.pyのhighlight_entitiesコードを分析"""
    print(f"\n=== app_with_ner.pyのコード分析 ===")
    
    # 実際のコードから問題になりそうな部分を特定
    # f-stringの連結部分に注目
    test_color = '#FFB6C1'
    test_border = "border: 2px solid #FF6B6B; box-shadow: 0 0 10px rgba(255, 107, 107, 0.5);"
    test_entity = '昭和六十三年法律第九十一号'
    test_category = '法律参照'
    
    # 元のコードと同じ方法で構築
    highlighted_part = (
        f'<span style="background-color: {test_color}; '
        f'padding: 1px 3px; margin: 0 1px; border-radius: 3px; '
        f'font-weight: 500; border: 1px solid {test_color}88; {test_border}" '
        f'title="{test_category}: {test_entity}">'
        f'{test_entity}</span>'
    )
    
    print("構築されたspanタグ（詳細分析）:")
    print(highlighted_part)
    
    # 各部分を分解して表示
    parts = [
        f'<span style="background-color: {test_color}; ',
        f'padding: 1px 3px; margin: 0 1px; border-radius: 3px; ',
        f'font-weight: 500; border: 1px solid {test_color}88; {test_border}" ',
        f'title="{test_category}: {test_entity}">',
        f'{test_entity}',
        f'</span>'
    ]
    
    print("\n分解された各部分:")
    for i, part in enumerate(parts, 1):
        print(f"{i}: {part}")
    
    # 全体を結合して最終確認
    full_tag = ''.join(parts)
    print(f"\n結合された最終タグ: {full_tag}")
    
    # 文法チェック
    if full_tag.count('<span') == full_tag.count('</span>'):
        print("✅ タグの開始と終了が一致")
    else:
        print("⚠️ タグの開始と終了が不一致")
    
    # 不完全なタグをチェック
    if re.search(r'<span[^>]*(?!>)', full_tag):
        print("⚠️ 不完全なタグが検出されました")
    else:
        print("✅ タグの構文は正常です")

if __name__ == "__main__":
    debug_specific_case()
    analyze_app_code()
