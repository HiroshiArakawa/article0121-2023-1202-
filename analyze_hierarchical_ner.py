"""
階層構造に完全対応したNER解析スクリプト
"""

import pickle
from ner_extractor import PatentLawNER
import pandas as pd

def analyze_hierarchical_data(data):
    """階層データ構造に対応した再帰的NER解析"""
    ner = PatentLawNER()
    analyzed_data = []
    total_entities = 0
    processed_articles = 0
    
    for i, chapter in enumerate(data):
        print(f"Processing chapter {i+1}: {chapter.get('title', 'Unknown')}")
        
        # 章レベルの解析
        analyzed_chapter = ner.analyze_article_text(chapter)
        
        # 章内の条文を個別に解析
        if 'articles' in chapter and isinstance(chapter['articles'], list):
            analyzed_articles = []
            
            for j, article in enumerate(chapter['articles']):
                if isinstance(article, dict):
                    # 条文レベルの解析
                    analyzed_article = ner.analyze_article_text(article)
                    analyzed_articles.append(analyzed_article)
                    
                    # 統計計算
                    if 'ner_entities' in analyzed_article:
                        article_entities = sum(len(entities) for entities in analyzed_article['ner_entities'].values())
                        total_entities += article_entities
                    
                    processed_articles += 1
                    
                    # 進捗表示
                    if processed_articles % 50 == 0:
                        print(f"  Processed {processed_articles} articles...")
                else:
                    analyzed_articles.append(article)
            
            analyzed_chapter['articles'] = analyzed_articles
        
        analyzed_data.append(analyzed_chapter)
    
    return analyzed_data, total_entities, processed_articles

# 元のPickleファイルを読み込み
print("Loading original data...")
with open('334AC0000000121_20230703_505AC0000000051.pickle', 'rb') as f:
    original_data = pickle.load(f)

print(f"Original data loaded: {len(original_data)} chapters")

# 階層構造に対応した解析実行
print("Starting hierarchical NER analysis...")
analyzed_data, total_entities, processed_articles = analyze_hierarchical_data(original_data)

print(f"Analysis completed!")
print(f"  Total chapters: {len(analyzed_data)}")
print(f"  Total articles processed: {processed_articles}")
print(f"  Total entities extracted: {total_entities}")

# 結果をPickleファイルに保存
output_file = "334AC0000000121_20230703_505AC0000000051_with_ner_hierarchical.pickle"
with open(output_file, 'wb') as f:
    pickle.dump(analyzed_data, f)

print(f"Saved hierarchical NER data to {output_file}")

# 第64条での「一年六月」確認
print("\n=== 第64条での「一年六月」確認 ===")
try:
    chapter_3_2 = analyzed_data[3]  # 第三章の二　出願公開
    article_64 = chapter_3_2['articles'][0]  # 第64条
    
    print(f"Article 64 title: {article_64.get('title', 'N/A')}")
    
    if 'ner_entities' in article_64 and 'TIME_PERIOD' in article_64['ner_entities']:
        time_entities = article_64['ner_entities']['TIME_PERIOD']
        target_found = any('一年六月' in entity['text'] for entity in time_entities)
        
        if target_found:
            print("🎉 成功！第64条で「一年六月」がTIME_PERIODとして抽出されました！")
            for entity in time_entities:
                if '一年六月' in entity['text']:
                    print(f"  - '{entity['text']}' (位置: {entity['start']}-{entity['end']})")
        else:
            print("⚠️ 第64条で「一年六月」がTIME_PERIODとして抽出されませんでした")
            print("抽出された時間表現:")
            for entity in time_entities:
                print(f"  - '{entity['text']}'")
    else:
        print("❌ 第64条にTIME_PERIODエンティティが見つかりませんでした")
        if 'ner_entities' in article_64:
            print(f"利用可能なカテゴリ: {list(article_64['ner_entities'].keys())}")
        else:
            print("NERエンティティが全く存在しません")
            
except Exception as e:
    print(f"エラー: {e}")

# CSVファイルも作成
print("\n=== CSV出力 ===")
csv_file = "patent_law_ner_results_hierarchical.csv"
rows = []

for i, chapter in enumerate(analyzed_data):
    if 'articles' in chapter:
        for j, article in enumerate(chapter['articles']):
            if 'ner_entities' in article:
                for category, entities in article['ner_entities'].items():
                    for entity in entities:
                        rows.append({
                            'chapter_index': i,
                            'chapter_title': chapter.get('title', ''),
                            'article_index': j,
                            'article_title': article.get('title', ''),
                            'category': category,
                            'text': entity['text'],
                            'start': entity['start'],
                            'end': entity['end']
                        })

df = pd.DataFrame(rows)
df.to_csv(csv_file, index=False, encoding='utf-8-sig')
print(f"CSV saved to {csv_file} ({len(df)} entities)")

# 「一年六月」の最終確認
target_rows = df[df['text'] == '一年六月']
if len(target_rows) > 0:
    print(f"\n✅ 「一年六月」がCSVに記録されています: {len(target_rows)}件")
    for _, row in target_rows.iterrows():
        print(f"  - {row['chapter_title']} > {row['article_title']} ({row['category']})")
else:
    print(f"\n❌ 「一年六月」はCSVに記録されていません")
