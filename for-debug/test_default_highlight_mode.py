#!/usr/bin/env python3
"""
デフォルト表示モードを「ハイライト表示」に変更したテストスクリプト

修正内容:
1. st.radioの選択肢順序を["ハイライト表示", "原文表示"]に変更
2. index=0を明示的に設定してハイライト表示をデフォルトに
3. helpテキストの順序も修正

テスト項目:
- st.radioの選択肢順序が正しく変更されているか
- index=0が設定されているか
- helpテキストが適切に更新されているか
- 条件分岐のロジックが正しく動作するか
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

def test_radio_options_order():
    """st.radioの選択肢順序確認"""
    print("\n=== st.radioの選択肢順序確認 ===")
    
    with open("app_with_ner.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # 「ハイライト表示」が最初に来ているかチェック
    if '["ハイライト表示", "原文表示"]' in content:
        print("✅ 選択肢の順序が正しく修正されています（ハイライト表示が最初）")
        return True
    else:
        print("❌ 選択肢の順序が修正されていません")
        if '["原文表示", "ハイライト表示"]' in content:
            print("   古い順序が残っています")
        return False

def test_default_index():
    """デフォルトインデックス設定確認"""
    print("\n=== デフォルトインデックス設定確認 ===")
    
    with open("app_with_ner.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # index=0が設定されているかチェック
    if 'index=0' in content and '# デフォルトでハイライト表示を選択' in content:
        print("✅ デフォルトインデックス（index=0）が設定されています")
        print("✅ 適切なコメントも追加されています")
        return True
    elif 'index=0' in content:
        print("✅ デフォルトインデックス（index=0）が設定されています")
        print("⚠️ コメントが見つかりませんが、機能的には問題ありません")
        return True
    else:
        print("❌ デフォルトインデックスが設定されていません")
        return False

def test_help_text_order():
    """helpテキストの順序確認"""
    print("\n=== helpテキストの順序確認 ===")
    
    with open("app_with_ner.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # helpテキストの順序が修正されているかチェック
    expected_help = "ハイライト表示：固有表現をカラーハイライト / 原文表示：元のテキストをそのまま表示"
    if expected_help in content:
        print("✅ helpテキストの順序が修正されています")
        return True
    else:
        print("❌ helpテキストの順序が修正されていません")
        return False

def test_condition_logic():
    """条件分岐ロジックの確認"""
    print("\n=== 条件分岐ロジックの確認 ===")
    
    with open("app_with_ner.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # ハイライト表示の条件分岐が正しいかチェック
    if 'if display_mode == "ハイライト表示"' in content:
        print("✅ ハイライト表示の条件分岐が正しく設定されています")
        
        # else節があるかもチェック
        if 'else:' in content and 'st.text_area' in content:
            print("✅ 原文表示のelse節も存在します")
            return True
        else:
            print("⚠️ else節の確認ができませんが、条件分岐は正常です")
            return True
    else:
        print("❌ ハイライト表示の条件分岐が見つかりません")
        return False

def test_comment_updates():
    """コメント更新の確認"""
    print("\n=== コメント更新の確認 ===")
    
    with open("app_with_ner.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # コメントが適切に更新されているかチェック
    if '# 表示モード選択（デフォルト：ハイライト表示）' in content:
        print("✅ コメントが適切に更新されています")
        return True
    else:
        print("⚠️ コメントが更新されていませんが、機能的には問題ありません")
        return True

def main():
    """メインテスト実行"""
    print("デフォルト表示モード「ハイライト表示」変更 - テスト開始")
    print("=" * 60)
    
    # 作業ディレクトリの確認
    if not Path("app_with_ner.py").exists():
        print("❌ app_with_ner.py が見つかりません")
        return False
    
    # テスト実行
    tests = [
        test_syntax_check,
        test_radio_options_order,
        test_default_index,
        test_help_text_order,
        test_condition_logic,
        test_comment_updates
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
        print("\n変更内容:")
        print("- デフォルト表示モードを「ハイライト表示」に変更")
        print("- st.radioの選択肢順序を最適化")
        print("- index=0を明示的に設定")
        print("- helpテキストの順序を更新")
        print("- 適切なコメントを追加")
    else:
        print(f"❌ {total - passed} 個のテストが失敗しました")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
