"""
ハイライト処理のデバッグテスト
"""

import re

def debug_highlight_process():
    """ハイライト処理をステップバイステップでデバッグ"""
    
    # 第三条のクリーンテキスト（HTMLタグ除去後）
    clean_text = """（期間の計算） 第三条 この法律又はこの法律に基く命令の規定による期間の計算は、次の規定による。 一 期間の初日は、算入しない。ただし、その期間が午前零時から始まるときは、この限りでない。 二 期間の末日が法定の休日（日曜日、土曜日、国民の祝日に関する法律（昭和二十三年法律第百七十八号）に規定する休日及び年末年始の休日（十二月二十九日から翌年の一月三日までの日をいう。）をいう。以下同じ。）に当たるときは、その日の翌日をもつてその期間の末日とする。"""
    
    print("=== ハイライト処理デバッグ ===")
    print(f"元テキスト長: {len(clean_text)}")
    print(f"元テキスト: {clean_text[:100]}...")
    
    # エンティティデータをシミュレート
    entity_text = "昭和二十三年法律第百七十八号"
    color = "#FFB6C1"
    border_style = "border: 2px solid #FF6B6B; box-shadow: 0 0 10px rgba(255, 107, 107, 0.5);"
    category_jp = "法律参照"
    
    print(f"\n=== エンティティ情報 ===")
    print(f"対象エンティティ: '{entity_text}'")
    print(f"色: {color}")
    print(f"ボーダースタイル: {border_style}")
    
    # エンティティが存在するかチェック
    if entity_text in clean_text:
        print(f"✅ エンティティがテキスト内に存在")
        positions = []
        start = 0
        while True:
            pos = clean_text.find(entity_text, start)
            if pos == -1:
                break
            positions.append(pos)
            start = pos + 1
        print(f"出現位置: {positions}")
    else:
        print(f"❌ エンティティがテキスト内に存在しません")
        return
    
    # ハイライト処理をシミュレート
    print(f"\n=== ハイライト処理シミュレーション ===")
    
    # ステップ1: ハイライト部分を作成
    highlighted_part = (
        f'<span style="background-color: {color}; '
        f'padding: 1px 3px; margin: 0 1px; border-radius: 3px; '
        f'font-weight: 500; border: 1px solid {color}88; {border_style}" '
        f'title="{category_jp}: {entity_text}">'
        f'{entity_text}</span>'
    )
    
    print(f"生成されたハイライト部分:")
    print(f"長さ: {len(highlighted_part)}")
    print(f"内容: {highlighted_part}")
    
    # ステップ2: 置換処理
    highlighted_text = clean_text.replace(entity_text, highlighted_part, 1)
    
    print(f"\n=== 置換結果 ===")
    print(f"置換後の長さ: {len(highlighted_text)}")
    
    # 置換された部分を確認
    entity_pos = highlighted_text.find('<span')
    if entity_pos != -1:
        before = highlighted_text[max(0, entity_pos-30):entity_pos]
        span_part = highlighted_text[entity_pos:entity_pos+200]
        print(f"置換された部分:")
        print(f"前文脈: ...{before}")
        print(f"span部分: {span_part}...")
        
        # 閉じタグがあるかチェック
        if '</span>' in span_part:
            print("✅ 閉じタグが含まれています")
        else:
            print("❌ 閉じタグが含まれていません")
    
    # HTMLタグのバランスをチェック
    opening_tags = len(re.findall(r'<span[^>]*>', highlighted_text))
    closing_tags = len(re.findall(r'</span>', highlighted_text))
    
    print(f"\n=== HTMLタグバランス ===")
    print(f"開始タグ: {opening_tags}個")
    print(f"閉じタグ: {closing_tags}個")
    
    if opening_tags == closing_tags:
        print("✅ タグバランス正常")
    else:
        print("❌ タグバランス異常")
    
    return highlighted_text

if __name__ == "__main__":
    result = debug_highlight_process()
    
    # 結果をファイルに保存して詳細確認
    with open('highlight_debug_result.txt', 'w', encoding='utf-8') as f:
        f.write(result)
    print(f"\n結果を highlight_debug_result.txt に保存しました")
