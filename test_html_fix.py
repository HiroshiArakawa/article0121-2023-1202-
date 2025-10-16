"""
修正されたハイライト機能のテスト
"""

import sys
import os
import re

# プロジェクトのルートディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def format_article_paragraphs(text):
    """条文テキストを項番号で改行して整形"""
    if not text:
        return text
    
    # 全角数字の項番号パターン（２、３、４...１０、１１...）の前で改行
    # スペース + 全角数字（1桁または2桁） + スペースのパターンを検出
    # ２～９、１０、１１、１２... を対象とする
    formatted_text = re.sub(r'(\s+)([２３４５６７８９]|[１２][０-９])(\s+)', r'\n\n\2 ', text)
    
    # 漢数字の項番号パターン（一、二、三、四、五...）の前で改行
    # スペース + 漢数字 + スペースのパターンを検出
    formatted_text = re.sub(r'(\s+)([一二三四五六七八九十])(\s+)', r'\n\n\2 ', formatted_text)
    
    # 行頭の空白を除去し、段落間の余分な改行を整理
    lines = []
    for line in formatted_text.split('\n'):
        line = line.strip()
        if line:  # 空行でない場合のみ追加
            lines.append(line)
    
    # 項番号で始まる行の前に空行を追加（最初の行は除く）
    result_lines = []
    for i, line in enumerate(lines):
        # 全角数字または漢数字の項番号で始まる行をチェック
        if i > 0 and re.match(r'^([２３４５６７８９]|[１２][０-９]|[一二三四五六七八九十])\s', line):
            result_lines.append('')  # 空行を追加
        result_lines.append(line)
    
    return '\n'.join(result_lines)

def test_html_cleaning_fix():
    """修正されたHTMLクリーニング機能をテスト"""
    
    # 第三条の問題のあるテキスト（HTMLタグが混在）
    problematic_text = """<section class="active Article" id=""><div class="_div_ArticleCaption" style="margin-left: 1em; font-weight: bold;">（期間の計算）</div>
<div class="_div_ArticleTitle" id="" style="margin-left: 1em; text-indent: -1em;">
<span style="font-weight: bold;">第三条</span>　この法律又はこの法律に基く命令の規定による期間の計算は、次の規定による。<div class="_div_ItemSentence" id="" style="margin-left: 1em; text-indent: -1em;">
<span style="font-weight: bold;">一</span>　期間の初日は、算入しない。ただし、その期間が午前零時から始まるときは、この限りでない。</div>
<div class="_div_ItemSentence" id="" style="margin-left: 1em; text-indent: -1em;">
<span style="font-weight: bold;">二</span>　期間の末日が法定の休日（日曜日、土曜日、国民の祝日に関する法律（昭和二十三年法律第百七十八号）に規定する休日及び年末年始の休日（十二月二十九日から翌年の一月三日までの日をいう。）をいう。以下同じ。）に当たるときは、その日の翌日をもつてその期間の末日とする。</div>
</section>"""
    
    print("=== 修正されたHTMLクリーニングテスト ===")
    print("元のテキスト（HTML含む）:")
    print(f"長さ: {len(problematic_text)}")
    print(problematic_text[:200] + "...")
    
    print("\n=== HTMLクリーニング処理 ===")
    
    # ステップ1: HTMLタグ除去
    if '<' in problematic_text and '>' in problematic_text:
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(problematic_text, 'html.parser')
            clean_text = soup.get_text()
            # 連続する空白や改行を整理
            clean_text = re.sub(r'\s+', ' ', clean_text).strip()
            print("BeautifulSoupでクリーニング完了")
        except:
            # BeautifulSoupが使えない場合は正規表現で除去
            clean_text = re.sub(r'<[^>]+>', '', problematic_text)
            clean_text = re.sub(r'\s+', ' ', clean_text).strip()
            print("正規表現でクリーニング完了")
    
    print(f"クリーニング後の長さ: {len(clean_text)}")
    print("クリーニング後のテキスト:")
    print(clean_text[:200] + "...")
    
    # ステップ2: 項番号での改行処理
    formatted_text = format_article_paragraphs(clean_text)
    print("\n=== 項番号改行処理後 ===")
    print(formatted_text)
    
    # ステップ3: サンプルNERハイライト
    print("\n=== NERハイライトシミュレーション ===")
    
    # 「この法律」をハイライト
    highlighted = formatted_text.replace(
        'この法律',
        '<span style="background-color: #FFF2F2; padding: 1px 3px; margin: 0 1px; border-radius: 3px; font-weight: 500; border: 1px solid #FFF2F288;" title="法律参照: この法律">この法律</span>',
        1  # 最初の1回のみ
    )
    
    print("ハイライト後:")
    print(highlighted)
    
    # HTMLタグが適切かチェック
    html_tags = re.findall(r'<[^>]+>', highlighted)
    print(f"\n生成されたHTMLタグ数: {len(html_tags)}")
    for tag in html_tags:
        print(f"  - {tag}")

if __name__ == "__main__":
    test_html_cleaning_fix()
