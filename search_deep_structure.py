"""
階層データ構造で第64条を探す
"""

import pickle
from ner_extractor import PatentLawNER

# 元のPickleファイルを読み込み
pickle_file = "334AC0000000121_20230703_505AC0000000051.pickle"

with open(pickle_file, 'rb') as f:
    data = pickle.load(f)

print(f"=== 階層データ構造の探索 ===")

def search_articles_recursively(data, target_text="一年六月"):
    """再帰的に記事を検索"""
    found_articles = []
    
    for i, item in enumerate(data):
        if isinstance(item, dict):
            # 直接的な条文チェック
            if any(key in ['body', 'text', 'content'] for key in item.keys()):
                for key in ['body', 'text', 'content']:
                    if key in item and target_text in str(item[key]):
                        found_articles.append({
                            'index': i,
                            'item': item,
                            'found_in': key
                        })
            
            # articlesフィールドがある場合は再帰的に検索
            if 'articles' in item and isinstance(item['articles'], list):
                for j, sub_article in enumerate(item['articles']):
                    if isinstance(sub_article, dict):
                        for key in ['body', 'text', 'content']:
                            if key in sub_article and target_text in str(sub_article[key]):
                                found_articles.append({
                                    'index': f"{i}-{j}",
                                    'item': sub_article,
                                    'found_in': key,
                                    'parent': item.get('title', 'Unknown Chapter')
                                })
    
    return found_articles

# 「一年六月」を検索
results = search_articles_recursively(data, "一年六月")

print(f"「一年六月」を含む記事: {len(results)}個")

for result in results:
    print(f"\n✅ 発見！ (インデックス: {result['index']})")
    article = result['item']
    
    if 'parent' in result:
        print(f"親章: {result['parent']}")
    
    print(f"フィールド: {result['found_in']}")
    print(f"Article Number: {article.get('article_number', 'N/A')}")
    print(f"Title: {article.get('title', 'N/A')}")
    
    # 「一年六月」周辺のテキストを表示
    text_content = article[result['found_in']]
    index = text_content.find("一年六月")
    if index != -1:
        start = max(0, index - 30)
        end = min(len(text_content), index + 50)
        context = text_content[start:end]
        print(f"コンテキスト: ...{context}...")
    
    # NER解析を実行
    print(f"\n=== NER解析結果 ===")
    ner = PatentLawNER()
    entities = ner.analyze_article_text(article)
    
    if 'ner_entities' in entities and 'TIME_PERIOD' in entities['ner_entities']:
        time_entities = entities['ner_entities']['TIME_PERIOD']
        print(f"TIME_PERIOD: {len(time_entities)}個")
        for entity in time_entities:
            print(f"  - '{entity['text']}'")
            if '一年六月' in entity['text']:
                print(f"    ✅ 「一年六月」を含む！")
    
    print("-" * 50)

if not results:
    print("❌ 「一年六月」を含む記事が見つかりませんでした")
    
    # 第3章の2を確認
    print("\n=== 第3章の2「出願公開」の確認 ===")
    for i, item in enumerate(data):
        if isinstance(item, dict) and 'title' in item:
            title = item['title']
            if '出願公開' in title or '第三章の二' in title:
                print(f"章タイトル: {title}")
                if 'articles' in item:
                    print(f"  含まれる条文数: {len(item['articles'])}")
                    for j, article in enumerate(item['articles'][:3]):  # 最初の3つを表示
                        print(f"    [{j}] {article.get('title', 'N/A')}")
                        if 'body' in article:
                            body = article['body'][:100]  # 最初の100文字
                            print(f"        Body preview: {body}...")
                break
