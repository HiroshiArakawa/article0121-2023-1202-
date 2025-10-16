"""
実際の第一条データでNER処理をテスト
"""
import pickle
from ner_extractor import PatentLawNER

def test_article_1():
    """第一条の実際データでテスト"""
    ner = PatentLawNER()
    
    # pickleファイルから第一条を取得
    try:
        with open('334AC0000000121_20230703_505AC0000000051.pickle', 'rb') as f:
            data = pickle.load(f)
        
        # 第一条を探す
        article_1 = None
        if isinstance(data, list):
            for chapter in data:
                if isinstance(chapter, dict) and 'articles' in chapter:
                    for article in chapter['articles']:
                        if '第一条' in article.get('title', '') or '第1条' in article.get('title', ''):
                            article_1 = article
                            break
                    if article_1:
                        break
        
        if article_1:
            print("=== 第一条の実際データテスト ===")
            print(f"タイトル: {article_1.get('title', '')}")
            
            # テキスト取得
            text = ner._get_clean_text(article_1)
            print(f"条文テキスト: {text[:200]}...")
            
            # NER処理
            entities = ner.extract_entities(text)
            law_refs = entities.get('LAW_REFERENCE', [])
            
            print(f"\n抽出された法律参照: {len(law_refs)}個")
            for entity in law_refs:
                original = entity.get('original_text', entity['text'])
                if 'original_text' in entity:
                    print(f"  - 「{original}」 → 「{entity['text']}」 (正規化)")
                else:
                    print(f"  - 「{entity['text']}」")
            
            # その他のカテゴリも表示
            for category, entity_list in entities.items():
                if category != 'LAW_REFERENCE' and entity_list:
                    print(f"\n{category}: {len(entity_list)}個")
                    for entity in entity_list[:3]:  # 最初の3個まで表示
                        print(f"  - 「{entity['text']}」")
                    if len(entity_list) > 3:
                        print(f"  - ...他{len(entity_list)-3}個")
        else:
            print("第一条が見つかりませんでした")
            
    except Exception as e:
        print(f"エラー: {e}")

if __name__ == "__main__":
    test_article_1()
