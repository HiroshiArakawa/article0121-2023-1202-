#!/usr/bin/env python3
"""
ハイライト表示の問題をデバッグするためのスクリプト

「すべてのカテゴリ」選択時に右パネルで固有表現が赤枠表示されない問題を調査
"""

import re

def test_highlight_logic():
    """ハイライト関数の論理をテスト"""
    print("=== ハイライト関数の論理テスト ===")
    
    # テストケース
    test_cases = [
        {"selected_category": "すべて", "entity_category": "TIME_PERIOD", "expected": "強調"},
        {"selected_category": "TIME_PERIOD", "entity_category": "TIME_PERIOD", "expected": "強調"},
        {"selected_category": "TIME_PERIOD", "entity_category": "LAW_REFERENCE", "expected": "通常"},
        {"selected_category": None, "entity_category": "TIME_PERIOD", "expected": "通常"},
        {"selected_category": "", "entity_category": "TIME_PERIOD", "expected": "通常"},
    ]
    
    for i, case in enumerate(test_cases, 1):
        selected_category = case["selected_category"]
        entity_category = case["entity_category"]
        expected = case["expected"]
        
        # 現在のロジックをテスト
        if selected_category and (entity_category == selected_category or selected_category == "すべて"):
            result = "強調"
        else:
            result = "通常"
        
        status = "✅" if result == expected else "❌"
        print(f"{status} テスト{i}: selected='{selected_category}', entity='{entity_category}' -> {result} (期待: {expected})")
        
        if result != expected:
            print(f"   問題: 論理条件が期待通りに動作していません")

def check_current_code():
    """現在のコードの問題を確認"""
    print("\n=== 現在のコードの問題確認 ===")
    
    try:
        with open("app_with_ner.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        # ハイライト関数の呼び出し部分を確認
        highlight_call_pattern = r'highlight_entities\([^)]+\)'
        matches = re.findall(highlight_call_pattern, content)
        
        print("ハイライト関数の呼び出し:")
        for match in matches:
            print(f"  {match}")
        
        # 「すべて」の処理箇所を確認
        lines = content.split('\n')
        all_related_lines = []
        for i, line in enumerate(lines, 1):
            if 'すべて' in line or 'selected_category' in line:
                all_related_lines.append((i, line.strip()))
        
        print(f"\n「すべて」または「selected_category」関連の行 (最初の10行):")
        for i, (line_num, line_content) in enumerate(all_related_lines[:10]):
            print(f"  {line_num}: {line_content}")
        
    except Exception as e:
        print(f"❌ ファイル読み込みエラー: {e}")

def suggest_fix():
    """修正案を提示"""
    print("\n=== 修正案 ===")
    print("1. highlight_entities関数の条件を以下に修正:")
    print("   修正前: if selected_category and (entity['category'] == selected_category or selected_category == \"すべて\"):")
    print("   修正後: if selected_category == \"すべて\" or (selected_category and entity['category'] == selected_category):")
    print("")
    print("2. または、呼び出し側で「すべて」の場合の処理を明示的に指定:")
    print("   highlight_category = selected_category  # Noneにしない")
    print("")
    print("3. デバッグ用のprint文を一時的に追加して動作確認")

if __name__ == "__main__":
    test_highlight_logic()
    check_current_code()
    suggest_fix()
