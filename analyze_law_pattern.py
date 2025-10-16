"""
LAW_REFERENCEパターンの詳細分析
"""

import re

def analyze_law_reference_pattern():
    """LAW_REFERENCEパターンが「行為 二 方法」を抽出するか確認"""
    
    # 修正後のパターン（スペースを除外文字に追加）
    pattern = r'([不民商工労建独消債公行政][^\s この本当該同あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん]*法律?)'
    
    test_texts = [
        "行為 二 方法",
        "行為二方法", 
        "をする行為 二 方法の発明",
        "方法の発明",
        "民法",
        "商法",
        "行政法"
    ]
    
    print("=== LAW_REFERENCEパターン分析 ===")
    print(f"パターン: {pattern}")
    print()
    
    for text in test_texts:
        matches = re.findall(pattern, text)
        if matches:
            print(f"✅ '{text}' → 抽出: {matches}")
        else:
            print(f"❌ '{text}' → 抽出なし")
    
    print("\n=== パターンの問題分析 ===")
    
    # 「行為 二 方法」がマッチする理由を分析
    test_string = "行為 二 方法"
    
    # 1. [不民商工労建独消債公行政] - 「行」が含まれるかチェック
    first_char_pattern = r'[不民商工労建独消債公行政]'
    if re.match(first_char_pattern, test_string[0]):
        print(f"問題1: 最初の文字 '{test_string[0]}' が [不民商工労建独消債公行政] にマッチ")
    
    # 2. [^この本当該同...] - 除外文字パターンをチェック
    exclusion_chars = "この本当該同あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん"
    remaining_text = test_string[1:]  # 「為 二 方法」
    
    print(f"問題2: 残りのテキスト '{remaining_text}' が除外文字に該当するかチェック")
    for i, char in enumerate(remaining_text):
        if char in exclusion_chars:
            print(f"  位置{i}: '{char}' は除外対象")
        else:
            print(f"  位置{i}: '{char}' は除外対象外 → マッチ対象")

if __name__ == "__main__":
    analyze_law_reference_pattern()
