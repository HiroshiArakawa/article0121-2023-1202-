"""
階層構造に対応したNER解析（第64条の「一年六月」を確実に含む）
"""

import pickle
from ner_extractor import PatentLawNER
import pandas as pd

# 元のPickleファイルを読み込み
pickle_file = "334AC0000000121_20230703_505AC0000000051.pickle"
print(f"Loading data from {pickle_file}...")

with open(pickle_file, 'rb') as f:
    data = pickle.load(f)

# 修正されたNERエンジン
ner = PatentLawNER()

def process_articles_recursively(data, processed_articles=None):
    """再帰的に記事を処理"""
    if processed_articles is None:
        processed_articles = []
    
    for item in data:
        if isinstance(item, dict):
            # 直接的な条文（bodyを持つ）の場合
            if 'body' in item or 'text' in item:
                analyzed_article = ner.analyze_article_text(item)
                processed_articles.append(analyzed_article)
            
            # articlesフィールドがある場合は再帰的に処理
            if 'articles' in item and isinstance(item['articles'], list):
                process_articles_recursively(item['articles'], processed_articles)
    
    return processed_articles

print("Re-analyzing with hierarchical structure support...")
analyzed_data = process_articles_recursively(data)

print(f"Total processed articles: {len(analyzed_data)}")

# エンティティの総数を計算
total_entities = 0
for article in analyzed_data:
    if 'ner_entities' in article:
        article_entity_count = sum(len(entities) for entities in article['ner_entities'].values())
        total_entities += article_entity_count

print(f"Total entities: {total_entities}")

# 更新されたデータを保存
output_file = "334AC0000000121_20230703_505AC0000000051_with_ner_hierarchical.pickle"
with open(output_file, 'wb') as f:
    pickle.dump(analyzed_data, f)

print(f"Saved hierarchical NER data to {output_file}")

# 「一年六月」を特別に検索
print("\n=== 「一年六月」の検索 ===")
found_articles = []

for i, article in enumerate(analyzed_data):
    if 'ner_entities' in article and 'TIME_PERIOD' in article['ner_entities']:
        for entity in article['ner_entities']['TIME_PERIOD']:
            if '一年六月' in entity['text']:
                found_articles.append({
                    'index': i,
                    'article': article,
                    'entity': entity
                })

if found_articles:
    print(f"✅ 「一年六月」を含む記事: {len(found_articles)}個")
    for result in found_articles:
        article = result['article']
        entity = result['entity']
        print(f"  - 記事タイトル: {article.get('title', 'N/A')}")
        print(f"    抽出表現: '{entity['text']}'")
        print(f"    位置: {entity['start']}-{entity['end']}")
        if 'clean_text' in article:
            clean_text = article['clean_text']
            if '一年六月' in clean_text:
                index = clean_text.find('一年六月')
                start = max(0, index - 20)
                end = min(len(clean_text), index + 30)
                context = clean_text[start:end]
                print(f"    コンテキスト: ...{context}...")
        print()
else:
    print("❌ 「一年六月」を含む記事が見つかりませんでした")

# CSVファイルも更新
print("Updating CSV file...")
csv_file = "patent_law_ner_results_hierarchical.csv"
rows = []

for article in analyzed_data:
    if 'ner_entities' in article:
        for category, entities in article['ner_entities'].items():
            for entity in entities:
                rows.append({
                    'article_title': article.get('title', ''),
                    'category': category,
                    'text': entity['text'],
                    'start': entity['start'],
                    'end': entity['end']
                })

df = pd.DataFrame(rows)
df.to_csv(csv_file, index=False, encoding='utf-8-sig')
print(f"Updated CSV saved to {csv_file} ({len(df)} entities)")

# 「一年六月」をCSVでも確認
target_in_csv = df[df['text'] == '一年六月']
if len(target_in_csv) > 0:
    print(f"\n✅ CSV内で「一年六月」を確認: {len(target_in_csv)}個")
    for _, row in target_in_csv.iterrows():
        print(f"  - 記事: {row['article_title']}")
        print(f"    カテゴリ: {row['category']}")
        print(f"    位置: {row['start']}-{row['end']}")
else:
    print("\n❌ CSV内に「一年六月」が見つかりませんでした")
