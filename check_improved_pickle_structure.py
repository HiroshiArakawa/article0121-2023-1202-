"""
改善されたPickleファイルのデータ構造確認
"""

import pickle

# 改善されたPickleファイルを読み込み
with open('334AC0000000121_20230703_505AC0000000051_with_ner_improved.pickle', 'rb') as f:
    data = pickle.load(f)

print(f"=== データ構造確認 ===")
print(f"データ型: {type(data)}")
print(f"データ数: {len(data)}")

# 最初の数個のアイテムを確認
for i, item in enumerate(data[:5]):
    print(f"\n[{i}] データ型: {type(item)}")
    if isinstance(item, dict):
        print(f"    キー: {list(item.keys())}")
        if 'title' in item:
            print(f"    Title: {item['title']}")
        if 'ner_entities' in item:
            total_entities = sum(len(entities) for entities in item['ner_entities'].values())
            print(f"    NER entities: {total_entities}個")
        if 'articles' in item:
            print(f"    子記事数: {len(item['articles'])}")

# 第64条が含まれているか確認
print(f"\n=== 第64条の検索 ===")
found_articles = []

def search_articles(data, search_text="第六十四条"):
    results = []
    for i, item in enumerate(data):
        if isinstance(item, dict):
            # タイトルチェック
            title = item.get('title', '')
            if search_text in title:
                results.append(f"[{i}] Title: {title}")
            
            # 子記事チェック
            if 'articles' in item and isinstance(item['articles'], list):
                for j, article in enumerate(item['articles']):
                    if isinstance(article, dict):
                        article_title = article.get('title', '')
                        if search_text in article_title:
                            results.append(f"[{i}-{j}] Parent: {title} -> Article: {article_title}")
                            # NER entities確認
                            if 'ner_entities' in article:
                                time_entities = article['ner_entities'].get('TIME_PERIOD', [])
                                for entity in time_entities:
                                    if '一年六月' in entity['text']:
                                        results.append(f"    ✅ 「一年六月」発見: '{entity['text']}'")
    return results

results = search_articles(data)
for result in results:
    print(result)

if not results:
    print("第64条が見つかりませんでした")

# データ構造が変わっているか確認
print(f"\n=== フラット構造への変換確認 ===")
print("階層データが平坦化されている可能性があります")

# 条文タイトルでの検索
article_count = 0
for item in data:
    if isinstance(item, dict) and 'title' in item:
        title = item['title']
        if '条' in title:
            article_count += 1
            if article_count <= 5:  # 最初の5つを表示
                print(f"  条文: {title}")

print(f"総条文数（概算）: {article_count}")
