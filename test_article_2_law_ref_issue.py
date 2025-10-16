"""
第二条での「行為 二 方法」誤抽出問題の確認テスト
"""

import re
import sys
import os

# プロジェクトのルートディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ner_extractor import PatentLawNER

def test_article_2_law_reference():
    """第二条での法律参照抽出をテスト"""
    
    # 第二条のテキスト（実際の条文）
    article_2_text = """（定義） 第二条 この法律で「発明」とは、自然法則を利用した技術的思想の創作のうち高度のものをいう。 ２ この法律で「特許発明」とは、特許を受けている発明をいう。 ３ この法律で発明について「実施」とは、次に掲げる行為をいう。 一 物（プログラム等を含む。以下同じ。）の発明にあつては、その物の生産、使用、譲渡等（譲渡及び貸渡しをいい、その物がプログラム等である場合には、電気通信回線を通じた提供を含む。以下同じ。）、輸入又は譲渡等の申出（譲渡等のための展示を含む。以下同じ。）をする行為 二 方法の発明にあつては、その方法の使用をする行為 三 物を生産する方法の発明にあつては、前二号に掲げる行為のほか、その方法により生産した物の使用、譲渡等、輸入又は譲渡等の申出をする行為"""
    
    ner = PatentLawNER()
    
    print("=== 第二条でのLAW_REFERENCE抽出結果 ===")
    results = ner.extract_entities(article_2_text)
    
    # LAW_REFERENCEカテゴリの結果を取得
    law_refs = results.get('LAW_REFERENCE', [])
    
    print(f"抽出された法律参照: {len(law_refs)}件")
    for i, entity in enumerate(law_refs, 1):
        print(f"{i}. '{entity['text']}' (位置: {entity['start']}-{entity['end']})")
        
        # 前後の文脈を表示
        start_context = max(0, entity['start'] - 20)
        end_context = min(len(article_2_text), entity['end'] + 20)
        context = article_2_text[start_context:end_context]
        print(f"   文脈: ...{context}...")
        print()
    
    # 問題のある「行為 二 方法」があるかチェック
    problematic_extractions = [
        entity for entity in law_refs 
        if '行為' in entity['text'] and '二' in entity['text'] and '方法' in entity['text']
    ]
    
    if problematic_extractions:
        print("❌ 問題のある抽出を発見:")
        for entity in problematic_extractions:
            print(f"   '{entity['text']}'")
    else:
        print("✅ 「行為 二 方法」の誤抽出は見つかりませんでした")
    
    # 「この法律」が正しく抽出されているかチェック
    correct_extractions = [entity for entity in law_refs if entity['text'] == 'この法律']
    print(f"\n✅ 「この法律」の正しい抽出: {len(correct_extractions)}件")
    
    print("\n=== 他のカテゴリの抽出結果サマリー ===")
    for category, entities in results.items():
        if category != 'LAW_REFERENCE':
            print(f"{category}: {len(entities)}件")

if __name__ == "__main__":
    test_article_2_law_reference()
