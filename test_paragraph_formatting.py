#!/usr/bin/env python3
"""
第二条の項番号改行テスト
"""

from app_with_ner import format_article_paragraphs

def test_paragraph_formatting():
    """第二条の項番号改行テスト"""
    
    # 第二条のテストケース
    test_text = "（定義） 第二条 この法律で「発明」とは、自然法則を利用した技術的思想の創作のうち高度のものをいう。 ２ この法律で「特許発明」とは、特許を受けている発明をいう。 ３ この法律で発明について「実施」とは、次に掲げる行為をいう。"
    
    print("=== 第二条の項番号改行テスト ===")
    print("元のテキスト:")
    print(f"'{test_text}'")
    print()
    
    # 改行処理を実行
    formatted_text = format_article_paragraphs(test_text)
    
    print("改行処理後:")
    print("---")
    print(formatted_text)
    print("---")
    print()
    
    # 改行が正しく行われているかチェック
    lines = formatted_text.split('\n')
    print(f"行数: {len(lines)}")
    for i, line in enumerate(lines, 1):
        if line.strip():  # 空行でない場合
            print(f"行{i}: '{line}'")
        else:
            print(f"行{i}: (空行)")
    
    # 期待される結果をチェック
    expected_patterns = [
        "この法律で「発明」とは",  # 最初の部分
        "２ この法律で「特許発明」",  # 第2項
        "３ この法律で発明について"   # 第3項
    ]
    
    print("\n=== 検証結果 ===")
    for pattern in expected_patterns:
        found = any(pattern in line for line in lines)
        status = "✅" if found else "❌"
        print(f"{status} '{pattern}' が含まれる行が存在")
    
    # 項番号が行頭に来ているかチェック
    item_lines = [line for line in lines if re.match(r'^[２３４５６７８９]', line.strip())]
    print(f"\n項番号で始まる行: {len(item_lines)}個")
    for line in item_lines:
        print(f"  - '{line.strip()}'")

def test_various_patterns():
    """様々なパターンのテスト"""
    
    test_cases = [
        {
            "name": "基本的な項番号",
            "text": "第一項の内容です。 ２ 第二項の内容です。 ３ 第三項の内容です。"
        },
        {
            "name": "複数の項番号",
            "text": "条文の本文。 ２ 項目２です。 ３ 項目３です。 ４ 項目４です。 ５ 項目５です。"
        },
        {
            "name": "項番号なし",
            "text": "普通の条文で項番号がありません。"
        }
    ]
    
    print("\n=== 様々なパターンのテスト ===")
    
    for case in test_cases:
        print(f"\n【{case['name']}】")
        print(f"元: {case['text']}")
        formatted = format_article_paragraphs(case['text'])
        print("結果:")
        for line in formatted.split('\n'):
            if line.strip():
                print(f"  '{line}'")
            else:
                print("  (空行)")

if __name__ == "__main__":
    import re
    test_paragraph_formatting()
    test_various_patterns()
