#!/usr/bin/env python3
"""
色付きボタンエラー修正のテストスクリプト

修正内容:
1. label_visibility パラメータの削除
2. HTMLボタンとStreamlitボタンの組み合わせ方式の改良
3. CSS動的生成による色適用の改善
"""

import sys
import subprocess
import os

def test_streamlit_syntax():
    """Streamlitコードの構文チェック"""
    print("🧪 Streamlitアプリの構文チェック開始")
    
    try:
        # 構文チェック用のPython import テスト
        result = subprocess.run([
            'python', '-c', 
            'import app_with_ner; print("✅ 構文チェック成功")'
        ], capture_output=True, text=True, cwd='.')
        
        if result.returncode == 0:
            print("✅ app_with_ner.py の構文は正常です")
            return True
        else:
            print("❌ 構文エラーが検出されました:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ テスト実行エラー: {e}")
        return False

def test_button_parameters():
    """ボタンパラメータの検証"""
    print("\n🧪 ボタンパラメータ検証開始")
    
    # app_with_ner.py の内容を読み込み
    try:
        with open('app_with_ner.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # label_visibility パラメータが残っていないかチェック
        if 'label_visibility' in content:
            print("❌ label_visibility パラメータが残っています")
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                if 'label_visibility' in line:
                    print(f"  行 {i}: {line.strip()}")
            return False
        else:
            print("✅ label_visibility パラメータは正しく削除されています")
        
        # buttonの使用パターンをチェック
        button_calls = []
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if 'st.sidebar.button(' in line or 'st.button(' in line:
                button_calls.append((i, line.strip()))
        
        print(f"✅ ボタン呼び出し箇所: {len(button_calls)}個")
        for line_num, line in button_calls[:3]:  # 最初の3個を表示
            print(f"  行 {line_num}: {line[:60]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ ファイル読み込みエラー: {e}")
        return False

def test_color_definitions():
    """色定義の確認"""
    print("\n🧪 色定義確認開始")
    
    try:
        with open('app_with_ner.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # button_colors の定義をチェック
        if 'button_colors = {' in content:
            print("✅ button_colors の定義が見つかりました")
            
            # 各カテゴリの色定義をチェック
            categories = [
                'LAW_REFERENCE', 'ARTICLE_REFERENCE', 'TIME_PERIOD',
                'MONEY_AMOUNT', 'ORGANIZATION', 'PROCEDURE', 'LEGAL_STATUS'
            ]
            
            found_categories = []
            for category in categories:
                if f"'{category}'" in content:
                    found_categories.append(category)
            
            print(f"✅ 色定義されたカテゴリ: {len(found_categories)}/7")
            for cat in found_categories:
                print(f"  - {cat}")
            
            return len(found_categories) == 7
        else:
            print("❌ button_colors の定義が見つかりません")
            return False
            
    except Exception as e:
        print(f"❌ 色定義確認エラー: {e}")
        return False

def test_css_generation():
    """CSS生成部分の確認"""
    print("\n🧪 CSS生成確認開始")
    
    try:
        with open('app_with_ner.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # CSS生成コードの存在確認
        css_patterns = [
            'button_style_css = f"""',
            'background:',
            'color:',
            'border:',
            'transition:'
        ]
        
        found_patterns = []
        for pattern in css_patterns:
            if pattern in content:
                found_patterns.append(pattern)
        
        print(f"✅ CSS生成パターン: {len(found_patterns)}/{len(css_patterns)}")
        for pattern in found_patterns:
            print(f"  - {pattern}")
        
        return len(found_patterns) >= 4
        
    except Exception as e:
        print(f"❌ CSS生成確認エラー: {e}")
        return False

def main():
    """メインテスト関数"""
    print("🔧 色付きボタンエラー修正テスト")
    print("=" * 50)
    
    tests = [
        ("構文チェック", test_streamlit_syntax),
        ("ボタンパラメータ検証", test_button_parameters),
        ("色定義確認", test_color_definitions),
        ("CSS生成確認", test_css_generation)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("🏁 テスト結果サマリー")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\n📊 成功率: {passed}/{len(tests)} ({passed/len(tests)*100:.1f}%)")
    
    if passed == len(tests):
        print("🎉 すべてのテストが成功しました！")
        print("💡 修正内容:")
        print("  - label_visibility パラメータを削除")
        print("  - 動的CSS生成による色適用")
        print("  - エラーハンドリングの改善")
    else:
        print("⚠️ 一部のテストで問題が検出されました。")
    
    print(f"\n🌐 テスト完了後の確認:")
    print(f"  アプリURL: http://localhost:8514")
    print(f"  左パネルのカテゴリボタンが色分けされているか確認してください")

if __name__ == "__main__":
    main()
