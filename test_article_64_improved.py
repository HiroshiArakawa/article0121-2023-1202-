"""
第64条で修正されたNERエンジンをテスト
"""

from ner_extractor import PatentLawNER
import pickle

# 元のPickleファイルを読み込み
pickle_file = "334AC0000000121_20230703_505AC0000000051.pickle"

with open(pickle_file, 'rb') as f:
    data = pickle.load(f)

# 第64条を探す（前のスクリプトの結果から、インデックス3-0であることがわかっている）
chapter_3_2 = data[3]  # 第三章の二　出願公開
article_64 = chapter_3_2['articles'][0]  # 第64条

print("=== 第64条の詳細 ===")
print(f"Title: {article_64.get('title', 'N/A')}")
print(f"Keys: {list(article_64.keys())}")

if 'body' in article_64:
    print(f"Body preview: {article_64['body'][:200]}...")

# 修正されたNERエンジンでテスト
print("\n=== 修正後NERエンジンでの解析 ===")
ner = PatentLawNER()

# HTMLタグ除去テスト
clean_text = ner._get_clean_text(article_64)
print(f"Clean text: {clean_text}")

# 「一年六月」が含まれているかチェック
if '一年六月' in clean_text:
    print("✅ クリーンテキストに「一年六月」が含まれています")
else:
    print("❌ クリーンテキストに「一年六月」が含まれていません")

# NER解析実行
entities = ner.analyze_article_text(article_64)

print("\n=== NER解析結果 ===")
if 'ner_entities' in entities:
    for category, items in entities['ner_entities'].items():
        if items:
            print(f"\n【{category}】({len(items)}個)")
            for item in items:
                print(f"  - '{item['text']}' (位置: {item['start']}-{item['end']})")
                if '一年六月' in item['text']:
                    print(f"    🎯 「一年六月」を含む表現！")

# 特に時間表現をチェック
if 'ner_entities' in entities and 'TIME_PERIOD' in entities['ner_entities']:
    time_entities = entities['ner_entities']['TIME_PERIOD']
    target_found = any('一年六月' in entity['text'] for entity in time_entities)
    
    if target_found:
        print("\n🎉 成功！「一年六月」がTIME_PERIODとして抽出されました！")
    else:
        print("\n⚠️  「一年六月」がTIME_PERIODとして抽出されませんでした")
        print("抽出された時間表現:")
        for entity in time_entities:
            print(f"  - '{entity['text']}'")
else:
    print("\n❌ TIME_PERIODカテゴリが見つかりませんでした")
