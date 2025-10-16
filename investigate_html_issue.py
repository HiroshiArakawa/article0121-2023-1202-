"""
第三条でのHTML表示問題の調査
"""

import sys
import os
import pickle

# プロジェクトのルートディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ner_extractor import PatentLawNER

def investigate_article_3_issue():
    """第三条でのHTML表示問題を調査"""
    
    print("=== 第三条のHTML表示問題調査 ===")
    
    # Pickleファイルから最新データを読み込み
    try:
        with open('334AC0000000121_20230703_505AC0000000051_with_ner_fixed.pickle', 'rb') as f:
            data = pickle.load(f)
    except FileNotFoundError:
        with open('334AC0000000121_20230703_505AC0000000051_with_ner.pickle', 'rb') as f:
            data = pickle.load(f)
    
    # 第三条を検索
    for chapter in data:
        if 'articles' in chapter:
            for article in chapter['articles']:
                if 'title' in article and '第三条' in str(article.get('title', '')):
                    print(f"第三条を発見: {article.get('title', '')}")
                    
                    # 元のテキストを確認
                    article_text = ""
                    if 'text' in article:
                        article_text = article['text']
                    elif 'body' in article:
                        article_text = article['body']
                    
                    print(f"\n=== 元のテキスト ===")
                    print(f"長さ: {len(article_text)}")
                    print(f"内容: {article_text[:500]}...")
                    
                    # HTMLタグが含まれているかチェック
                    if '<' in article_text and '>' in article_text:
                        print("\n❌ HTMLタグが含まれています")
                        
                        # 問題のあるHTMLを特定
                        import re
                        html_tags = re.findall(r'<[^>]+>', article_text)
                        print(f"発見されたHTMLタグ: {len(html_tags)}個")
                        for i, tag in enumerate(html_tags[:5]):  # 最初の5個を表示
                            print(f"  {i+1}. {tag}")
                        
                        # 問題の部分を特定
                        if 'span style' in article_text:
                            span_matches = re.findall(r'<span[^>]*>.*?</span>', article_text)
                            print(f"\nspan要素: {len(span_matches)}個")
                            for i, span in enumerate(span_matches[:3]):
                                print(f"  {i+1}. {span}")
                    else:
                        print("\n✅ HTMLタグは含まれていません")
                    
                    # NER結果を確認
                    if 'ner_entities' in article:
                        entities = article['ner_entities']
                        print(f"\n=== NER結果 ===")
                        for category, ents in entities.items():
                            if ents:
                                print(f"{category}: {len(ents)}個")
                                # 最初のいくつかを表示
                                for ent in ents[:3]:
                                    print(f"  - '{ent['text']}' (位置: {ent['start']}-{ent['end']})")
                    
                    return

def test_html_cleaning():
    """HTMLクリーニング機能をテスト"""
    print("\n=== HTMLクリーニングテスト ===")
    
    # 問題のあるテキストをシミュレート
    problematic_text = """２ 特許出願、請求その他特許に関する手続（以下単に「手続」という。）についての期間の末日が行政機関の休日に関する法律（<span style="background-color: #FFF2F2; padding: 1px 3px; margin: 0 1px; border-radius: 3px; font-weight: 500; border: 1px solid #FFF2F288; " title="法律参照: 昭和六十三年法律第九十一号">昭和六十三年法律第九十一号）第一条第一項各号に掲げる日に当たるときは、その日の翌日をもつてその期間の末日とする。"""
    
    print("元のテキスト:")
    print(problematic_text)
    
    # BeautifulSoupでクリーニング
    from bs4 import BeautifulSoup
    import re
    
    print("\n=== BeautifulSoupでクリーニング ===")
    try:
        soup = BeautifulSoup(problematic_text, 'html.parser')
        clean_text = soup.get_text()
        print("クリーニング後:")
        print(clean_text)
    except Exception as e:
        print(f"BeautifulSoupエラー: {e}")
    
    print("\n=== 正規表現でクリーニング ===")
    regex_clean = re.sub(r'<[^>]+>', '', problematic_text)
    print("クリーニング後:")
    print(regex_clean)

if __name__ == "__main__":
    investigate_article_3_issue()
    test_html_cleaning()
