#!/usr/bin/env python3
"""
「すべてのカテゴリ」選択時の固有表現ボタン赤枠表示修正のテストスクリプト

修正内容:
1. 「すべて」選択時にも各カテゴリボタンが選択状態（赤枠+濃色）で表示される
2. ボタンテキストに「(すべて選択中)」と表示される
3. 右パネルの統計表示にも「(すべて強調中)」と表示される

テスト項目:
- is_selected の条件式が正しく修正されているか
- ボタンテキストの分岐が適切に実装されているか
- 右パネルの表示も修正されているか
- コードの構文エラーがないか
"""

import ast
import sys
from pathlib import Path

def test_syntax_check():
    """構文チェック"""
    print("=== 構文チェック ===")
    try:
        with open("app_with_ner.py", "r", encoding="utf-8") as f:
            code = f.read()
        
        # 構文解析
        ast.parse(code)
        print("✅ 構文エラーなし")
        return True
    except SyntaxError as e:
        print(f"❌ 構文エラー: {e}")
        return False
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def test_is_selected_condition():
    """is_selected条件式の修正確認"""
    print("\n=== is_selected条件式の修正確認 ===")
    
    with open("app_with_ner.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # 修正された条件式のパターンを検索
    patterns = [
        'is_selected = (st.session_state.selected_category == category or',
        'st.session_state.selected_category == "すべて")'
    ]
    
    found_patterns = []
    for pattern in patterns:
        if pattern in content:
            found_patterns.append(pattern)
    
    if len(found_patterns) >= 2:
        print("✅ is_selected条件式が正しく修正されています")
        
        # どこで修正されているかを確認
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if 'is_selected = (st.session_state.selected_category == category or' in line:
                print(f"   - {i}行目: 左パネルの修正を確認")
            elif 'is_selected = (st.session_state.selected_category == category or' in line:
                print(f"   - {i}行目: 右パネルの修正を確認")
        
        return True
    else:
        print("❌ is_selected条件式の修正が不完全です")
        print(f"   見つかったパターン: {found_patterns}")
        return False

def test_button_text_improvement():
    """ボタンテキストの改善確認"""
    print("\n=== ボタンテキストの改善確認 ===")
    
    with open("app_with_ner.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # 「すべて選択中」のテキストが追加されているか
    if 'button_text += " (すべて選択中)"' in content:
        print("✅ ボタンテキストに「すべて選択中」が追加されています")
        
        # 分岐ロジックも確認
        if 'if st.session_state.selected_category == "すべて":' in content:
            print("✅ 「すべて」と個別カテゴリの分岐ロジックが実装されています")
            return True
        else:
            print("❌ 分岐ロジックが見つかりません")
            return False
    else:
        print("❌ ボタンテキストの改善が見つかりません")
        return False

def test_right_panel_improvement():
    """右パネル統計表示の改善確認"""
    print("\n=== 右パネル統計表示の改善確認 ===")
    
    with open("app_with_ner.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # 「すべて強調中」のテキストが追加されているか
    if '(すべて強調中)' in content:
        print("✅ 右パネルに「すべて強調中」が追加されています")
        
        # st.metricでの分岐も確認
        if 'if st.session_state.selected_category == "すべて":' in content and 'st.metric(' in content:
            print("✅ 右パネルの分岐ロジックが実装されています")
            return True
        else:
            print("❌ 右パネルの分岐ロジックが不完全です")
            return False
    else:
        print("❌ 右パネルの改善が見つかりません")
        return False

def test_highlight_function():
    """ハイライト関数の「すべて」対応確認"""
    print("\n=== ハイライト関数の「すべて」対応確認 ===")
    
    with open("app_with_ner.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # highlight_entities関数内の条件式を確認
    highlight_pattern = 'selected_category == "すべて"'
    
    if highlight_pattern in content:
        print("✅ ハイライト関数で「すべて」選択時の処理が追加されています")
        
        # border_styleの赤枠処理も確認
        if 'border: 2px solid #FF6B6B' in content:
            print("✅ 赤枠スタイルが定義されています")
            return True
        else:
            print("❌ 赤枠スタイルが見つかりません")
            return False
    else:
        print("❌ ハイライト関数の「すべて」対応が見つかりません")
        return False
    """CSSスタイリングとボタン色定義の確認"""
    print("\n=== CSSスタイリングとボタン色定義の確認 ===")
    
    with open("app_with_ner.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # ボタン色定義が存在するか
    if 'button_colors = {' in content:
        print("✅ ボタン色定義が存在します")
        
        # カテゴリ別の色が定義されているか
        color_categories = ['LAW_REFERENCE', 'ARTICLE_REFERENCE', 'TIME_PERIOD', 'MONEY_AMOUNT']
        found_categories = [cat for cat in color_categories if cat in content]
        
        print(f"   定義されているカテゴリ: {len(found_categories)}/{len(color_categories)}")
        
        return len(found_categories) >= 3
    else:
        print("❌ ボタン色定義が見つかりません")
def test_css_and_styling():
    """CSSスタイリングとボタン色定義の確認"""
    print("\n=== CSSスタイリングとボタン色定義の確認 ===")
    
    with open("app_with_ner.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # ボタン色定義が存在するか
    if 'button_colors = {' in content:
        print("✅ ボタン色定義が存在します")
        
        # カテゴリ別の色が定義されているか
        color_categories = ['LAW_REFERENCE', 'ARTICLE_REFERENCE', 'TIME_PERIOD', 'MONEY_AMOUNT']
        found_categories = [cat for cat in color_categories if cat in content]
        
        print(f"   定義されているカテゴリ: {len(found_categories)}/{len(color_categories)}")
        
        return len(found_categories) >= 3
    else:
        print("❌ ボタン色定義が見つかりません")
        return False
    """メインテスト実行"""
    print("「すべてのカテゴリ」選択時の固有表現ボタン赤枠表示修正 - テスト開始")
    print("=" * 60)
    
    # 作業ディレクトリの確認
    if not Path("app_with_ner.py").exists():
        print("❌ app_with_ner.py が見つかりません")
        return False
    
    # テスト実行
    tests = [
        test_syntax_check,
        test_is_selected_condition,
        test_button_text_improvement,
        test_right_panel_improvement,
        test_css_and_styling
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
    
    # 結果サマリー
    print("\n" + "=" * 60)
    print("=== テスト結果サマリー ===")
    passed = sum(results)
    total = len(results)
    
    print(f"✅ 成功: {passed}/{total} テスト")
    if passed == total:
        print("🎉 すべてのテストが成功しました！")
        print("\n修正内容:")
        print("- 「すべて」選択時にも各カテゴリボタンが選択状態で表示")
        print("- ボタンテキストに「(すべて選択中)」を表示")
        print("- 右パネル統計に「(すべて強調中)」を表示")
        print("- 既存の色分け・CSS機能は維持")
    else:
        print(f"❌ {total - passed} 個のテストが失敗しました")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
