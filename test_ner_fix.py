#!/usr/bin/env python3
"""
NER修正のテストスクリプト
"""

from ner_extractor import PatentLawNER

def test_ner_fix():
    """「この法」問題の修正をテスト"""
    
    # NERインスタンスを作成
    ner = PatentLawNER()
    
    # テストケース
    test_cases = [
        "この法律は、特許法の規定により適用される。",
        "この法の施行に関し必要な事項は政令で定める。", 
        "特許法第一条の規定は適用しない。",
        "実用新案法及び意匠法の規定を準用する。",
        "本法は昭和34年法律第121号である。"
    ]
    
    print("=== NER修正テスト ===")
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n【テストケース {i}】")
        print(f"テキスト: {text}")
        
        entities = ner.extract_entities(text)
        law_refs = entities.get('LAW_REFERENCE', [])
        
        print(f"LAW_REFERENCE抽出結果: {len(law_refs)}個")
        for entity in law_refs:
            print(f"  - '{entity['text']}' (位置: {entity['start']}-{entity['end']})")
        
        # 「この法」が除外されているかチェック
        inappropriate_found = any(
            entity['text'].strip() in ['この法', 'この法律', '本法'] 
            for entity in law_refs
        )
        
        if inappropriate_found:
            print("  ❌ 不適切な表現が残っています")
        else:
            print("  ✅ 不適切な表現は除外されています")

if __name__ == "__main__":
    test_ner_fix()
