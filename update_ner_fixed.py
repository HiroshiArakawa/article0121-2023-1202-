#!/usr/bin/env python3
"""
修正されたNERで既存データを再処理するスクリプト
"""

import pickle
from ner_extractor import PatentLawNER

def update_ner_data():
    """既存データのNER処理を更新"""
    
    # 元データを読み込み
    try:
        with open('334AC0000000121_20230703_505AC0000000051.pickle', 'rb') as f:
            data = pickle.load(f)
    except FileNotFoundError:
        print("元データファイルが見つかりません")
        return
    
    # NERインスタンスを作成
    ner = PatentLawNER()
    
    print("NER処理を開始...")
    
    processed_count = 0
    
    # データを処理
    for chapter_idx, chapter in enumerate(data):
        if 'articles' in chapter:
            for article_idx, article in enumerate(chapter['articles']):
                # 条文テキストを取得
                text = article.get('text', article.get('body', ''))
                
                if text:
                    # NER処理を実行
                    entities = ner.extract_entities(text)
                    article['ner_entities'] = entities
                    processed_count += 1
                    
                    # 第一条のテスト表示
                    title = article.get('title', article.get('heading', ''))
                    if '第一条' in title:
                        print(f"\n=== {title} ===")
                        law_refs = entities.get('LAW_REFERENCE', [])
                        print(f"LAW_REFERENCE: {len(law_refs)}個")
                        for entity in law_refs:
                            print(f"  - '{entity['text']}'")
    
    print(f"\n処理完了: {processed_count}件の条文を処理")
    
    # 修正されたデータを保存
    output_file = '334AC0000000121_20230703_505AC0000000051_with_ner_fixed.pickle'
    with open(output_file, 'wb') as f:
        pickle.dump(data, f)
    
    print(f"修正されたデータを {output_file} に保存しました")

if __name__ == "__main__":
    update_ner_data()
