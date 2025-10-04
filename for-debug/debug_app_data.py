"""
アプリのデータ構造デバッグ用スクリプト
"""

import pickle

def debug_article_structure():
    """条文データの詳細構造を確認"""
    try:
        with open('334AC0000000121_20230703_505AC0000000051_with_ner.pickle', 'rb') as f:
            data = pickle.load(f)
    except FileNotFoundError:
        with open('334AC0000000121_20230703_505AC0000000051.pickle', 'rb') as f:
            data = pickle.load(f)
    
    print("=== 条文データ構造の詳細調査 ===")
    print(f"全体データ型: {type(data)}")
    print(f"章数: {len(data)}")
    
    if isinstance(data, list) and len(data) > 0:
        # 最初の章を詳しく調査
        first_chapter = data[0]
        print(f"\n=== 第1章の構造 ===")
        print(f"キー: {list(first_chapter.keys())}")
        print(f"タイトル: {first_chapter.get('title', 'なし')}")
        
        if 'articles' in first_chapter:
            articles = first_chapter['articles']
            print(f"条文数: {len(articles)}")
            
            if len(articles) > 0:
                first_article = articles[0]
                print(f"\n=== 第1条文の構造 ===")
                print(f"型: {type(first_article)}")
                
                if isinstance(first_article, dict):
                    print(f"キー: {list(first_article.keys())}")
                    
                    for key, value in first_article.items():
                        if isinstance(value, str):
                            preview = value[:100] + "..." if len(value) > 100 else value
                            print(f"{key}: '{preview}' ({len(value)} 文字)")
                        else:
                            print(f"{key}: {type(value)}")
                    
                    # テキストフィールドの特定
                    text_fields = ['text', 'content', 'body', 'article_text', 'description']
                    for field in text_fields:
                        if field in first_article:
                            print(f"\n✅ テキストフィールド '{field}' が見つかりました")
                            text_content = first_article[field]
                            print(f"内容プレビュー: {text_content[:200]}...")
                else:
                    print(f"条文データが辞書型ではありません: {type(first_article)}")
        
        # 数章分をチェック
        print(f"\n=== 複数章のサンプル ===")
        for i in range(min(3, len(data))):
            chapter = data[i]
            title = chapter.get('title', f'章{i+1}')
            article_count = len(chapter.get('articles', []))
            print(f"章{i+1}: {title} (条文数: {article_count})")

if __name__ == "__main__":
    debug_article_structure()
