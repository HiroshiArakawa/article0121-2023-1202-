#!/usr/bin/env python3
"""
「この法律」抽出のテスト
"""

from ner_extractor import PatentLawNER

def test_law_reference_extraction():
    """第一条の「この法律」抽出テスト"""
    
    # NERエクストラクター初期化
    ner = PatentLawNER()
    
    # 第一条のテストケース
    test_text = "この法律は、発明の保護及び利用を図ることにより、発明を奨励し、もつて産業の発達に寄与することを目的とする。"
    
    print("=== 第一条のLAW_REFERENCE抽出テスト ===")
    print(f"テストテキスト: {test_text}")
    print()
    
    # 固有表現抽出
    entities = ner.extract_entities(test_text)
    
    # LAW_REFERENCEの結果を表示
    if 'LAW_REFERENCE' in entities and entities['LAW_REFERENCE']:
        print("✅ LAW_REFERENCE抽出結果:")
        for entity in entities['LAW_REFERENCE']:
            print(f"  - '{entity['text']}' (位置: {entity['start']}-{entity['end']})")
            print(f"    パターン: {entity['pattern']}")
        
        # 「この法律」が抽出されているかチェック
        extracted_texts = [e['text'] for e in entities['LAW_REFERENCE']]
        if 'この法律' in extracted_texts:
            print("\n🎉 成功: 「この法律」が正しく抽出されました！")
        else:
            print(f"\n❌ 失敗: 「この法律」が抽出されませんでした。抽出された内容: {extracted_texts}")
    else:
        print("❌ LAW_REFERENCEが抽出されませんでした")
    
    print("\n=== 全カテゴリの抽出結果 ===")
    for category, entity_list in entities.items():
        if entity_list:
            print(f"{category}: {len(entity_list)}個")
            for entity in entity_list:
                print(f"  - '{entity['text']}'")
        else:
            print(f"{category}: なし")

if __name__ == "__main__":
    test_law_reference_extraction()
