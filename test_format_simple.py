#!/usr/bin/env python3
"""
第二条の項番号改行テスト - 簡易版
"""

import re

def format_article_paragraphs(text):
    """条文テキストを項番号で改行して整形"""
    if not text:
        return text
    
    # 全角数字の項番号パターン（２、３、４...１０、１１...）の前で改行
    # スペース + 全角数字（1桁または2桁） + スペースのパターンを検出
    # ２～９、１０、１１、１２... を対象とする
    formatted_text = re.sub(r'(\s+)([２３４５６７８９]|[１２][０-９])(\s+)', r'\n\n\2 ', text)
    
    # 行頭の空白を除去し、段落間の余分な改行を整理
    lines = []
    for line in formatted_text.split('\n'):
        line = line.strip()
        if line:  # 空行でない場合のみ追加
            lines.append(line)
    
    # 項番号で始まる行の前に空行を追加（最初の行は除く）
    result_lines = []
    for i, line in enumerate(lines):
        # 全角数字の項番号で始まる行をチェック
        if i > 0 and re.match(r'^([２３４５６７８９]|[１２][０-９])\s', line):
            result_lines.append('')  # 空行を追加
        result_lines.append(line)
    
    return '\n'.join(result_lines)

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
    for i, line in enumerate(lines):
        print(f"行{i+1}: '{line}'")

if __name__ == "__main__":
    test_paragraph_formatting()
