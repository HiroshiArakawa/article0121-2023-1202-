"""
NER修正のテストスクリプト
「この法」を「この法律」として抽出するかテスト
"""
from ner_extractor import PatentLawNER

def test_law_reference_normalization():
    """法律参照の正規化をテスト"""
    ner = PatentLawNER()
    
    # テストケース
    test_cases = [
        "この法の目的は、発明の保護及び利用を図ることにより、発明を奨励し、もって産業の発達に寄与することにある。",
        "本法第二条に定める発明とは、自然法則を利用した技術的思想の創作のうち高度のものをいう。",
        "当該法律の規定により、特許権が設定される。",
        "特許法第一条に規定する目的を達成するため、以下の規定を設ける。"
    ]
    
    print("=== 法律参照の正規化テスト ===")
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n【テストケース {i}】")
        print(f"入力: {text}")
        
        entities = ner.extract_entities(text)
        law_refs = entities.get('LAW_REFERENCE', [])
        
        print(f"抽出された法律参照: {len(law_refs)}個")
        for entity in law_refs:
            original = entity.get('original_text', entity['text'])
            if 'original_text' in entity:
                print(f"  - 「{original}」 → 「{entity['text']}」 (正規化)")
            else:
                print(f"  - 「{entity['text']}」")
        
        if not law_refs:
            print("  - なし")

if __name__ == "__main__":
    test_law_reference_normalization()
