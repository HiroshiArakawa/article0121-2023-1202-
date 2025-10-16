"""
最新のNER修正でNERデータを再生成し、アプリ用ファイルを更新
"""

import sys
import os
import pickle

# プロジェクトのルートディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ner_extractor import PatentLawNER

def generate_and_update_ner_data():
    """最新の修正でNERデータを生成し、アプリ用ファイルを更新"""
    
    print("=== 最新のNER修正でデータを再生成 ===")
    
    # Pickleファイルから元データを読み込み
    with open('334AC0000000121_20230703_505AC0000000051.pickle', 'rb') as f:
        original_data = pickle.load(f)
    
    print(f"元データを読み込み: {len(original_data)} 章")
    
    # 最新のNER機能で固有表現を抽出
    ner = PatentLawNER()
    updated_data = []
    
    for i, chapter in enumerate(original_data):
        if 'articles' in chapter:
            for article in chapter['articles']:
                # 条文テキストを取得
                article_text = ""
                if 'text' in article:
                    article_text = article['text']
                elif 'body' in article:
                    article_text = article['body']
                
                if article_text:
                    # NER解析を実行
                    entities = ner.extract_entities(article_text)
                    article['ner_entities'] = entities
        
        updated_data.append(chapter)
        
        if (i + 1) % 10 == 0:
            print(f"処理済み: {i + 1}/{len(original_data)} 章")
    
    # アプリが使用するファイルに保存
    output_filename = '334AC0000000121_20230703_505AC0000000051_with_ner_fixed.pickle'
    with open(output_filename, 'wb') as f:
        pickle.dump(updated_data, f)
    
    print(f"✅ 最新のNERデータを {output_filename} に保存しました")
    
    # 第二条のテスト
    test_article_2(updated_data)

def test_article_2(data):
    """第二条での修正結果を確認"""
    print("\n=== 第二条での修正結果確認 ===")
    
    for chapter in data:
        if 'articles' in chapter:
            for article in chapter['articles']:
                if 'title' in article and '第二条' in str(article.get('title', '')):
                    print(f"第二条を発見: {article.get('title', '')}")
                    
                    if 'ner_entities' in article and 'LAW_REFERENCE' in article['ner_entities']:
                        law_refs = article['ner_entities']['LAW_REFERENCE']
                        print(f"LAW_REFERENCE: {len(law_refs)}件")
                        
                        # 問題のある「行為 二 方法」があるかチェック
                        problematic = [
                            entity for entity in law_refs 
                            if '行為' in entity['text'] and '二' in entity['text'] and '方法' in entity['text']
                        ]
                        
                        if problematic:
                            print("❌ まだ「行為 二 方法」の誤抽出があります:")
                            for entity in problematic:
                                print(f"   '{entity['text']}'")
                        else:
                            print("✅ 「行為 二 方法」の誤抽出は解決済み")
                        
                        # 正しい「この法律」の抽出を確認
                        correct_refs = [entity for entity in law_refs if entity['text'] == 'この法律']
                        print(f"✅ 「この法律」の抽出: {len(correct_refs)}件")
                    
                    return

if __name__ == "__main__":
    generate_and_update_ner_data()
