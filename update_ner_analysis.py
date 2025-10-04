"""
修正されたNERエンジンで全体データを再解析
"""

import pickle
from ner_extractor import PatentLawNER
import pandas as pd
from datetime import datetime

# 元のPickleファイルを読み込み
pickle_file = "334AC0000000121_20230703_505AC0000000051.pickle"
print(f"Loading data from {pickle_file}...")

with open(pickle_file, 'rb') as f:
    data = pickle.load(f)

print(f"Loaded {len(data)} articles")

# 修正されたNERエンジンで再解析
ner = PatentLawNER()
print("Re-analyzing with improved NER engine...")

analyzed_data = []
total_entities = 0

for i, article in enumerate(data):
    analyzed_article = ner.analyze_article_text(article)
    analyzed_data.append(analyzed_article)
    
    # 進捗表示
    if 'ner_entities' in analyzed_article:
        article_entity_count = sum(len(entities) for entities in analyzed_article['ner_entities'].values())
        total_entities += article_entity_count
        
    if (i + 1) % 50 == 0:
        print(f"  Processed {i + 1}/{len(data)} articles...")

print(f"Analysis completed! Total entities: {total_entities}")

# 更新されたデータを保存
output_file = "334AC0000000121_20230703_505AC0000000051_with_ner_improved.pickle"
with open(output_file, 'wb') as f:
    pickle.dump(analyzed_data, f)

print(f"Saved improved NER data to {output_file}")

# 時間関連の固有表現を特別にチェック
print("\n=== 時間表現の改善確認 ===")
time_expressions = []

for article in analyzed_data:
    if 'ner_entities' in article and 'TIME_PERIOD' in article['ner_entities']:
        for entity in article['ner_entities']['TIME_PERIOD']:
            time_expressions.append({
                'text': entity['text'],
                'article_number': article.get('article_number', 'unknown'),
                'chapter': article.get('chapter', 'unknown')
            })

# 複合期間表現を抽出
compound_periods = [exp for exp in time_expressions if '年' in exp['text'] and '月' in exp['text']]
print(f"複合期間表現（年月）: {len(compound_periods)}個")

for period in compound_periods[:10]:  # 最初の10個を表示
    print(f"  - '{period['text']}' (第{period['article_number']}条)")

# CSVも更新
print("\nUpdating CSV file...")
csv_file = "patent_law_ner_results_improved.csv"
rows = []

for article in analyzed_data:
    if 'ner_entities' in article:
        for category, entities in article['ner_entities'].items():
            for entity in entities:
                rows.append({
                    'article_number': article.get('article_number', ''),
                    'chapter': article.get('chapter', ''),
                    'category': category,
                    'text': entity['text'],
                    'start': entity['start'],
                    'end': entity['end']
                })

df = pd.DataFrame(rows)
df.to_csv(csv_file, index=False, encoding='utf-8-sig')
print(f"Updated CSV saved to {csv_file} ({len(df)} entities)")

print("\n=== 改善の確認 ===")
print(f"旧CSV: patent_law_ner_results.csv")
print(f"新CSV: {csv_file}")
print("Streamlitアプリでの確認のため、新しいPickleファイルを使用してください。")
