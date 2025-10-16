"""
修正された重複チェック機能のテスト
"""

def test_duplicate_check_fix():
    """修正された重複チェックをテスト"""
    
    print("=== 修正された重複チェックテスト ===")
    
    # シミュレーション: 既にハイライトされたテキスト
    highlighted_text = """（期間の計算） 第三条 この法律又はこの法律に基く命令の規定による期間の計算は、次の規定による。 一 期間の初日は、算入しない。ただし、その期間が午前零時から始まるときは、この限りでない。 二 期間の末日が法定の休日（日曜日、土曜日、国民の祝日に関する法律（<span style="background-color: #FFB6C1; padding: 1px 3px; margin: 0 1px; border-radius: 3px; font-weight: 500; border: 1px solid #FFB6C188; border: 2px solid #FF6B6B; box-shadow: 0 0 10px rgba(255, 107, 107, 0.5);" title="法律参照: 昭和二十三年法律第百七十八号">昭和二十三年法律第百七十八号</span>）に規定する休日及び年末年始の休日（十二月二十九日から翌年の一月三日までの日をいう。）をいう。以下同じ。）に当たるときは、その日の翌日をもつてその期間の末日とする。"""
    
    entity_text = "昭和二十三年法律第百七十八号"
    
    print(f"テストエンティティ: '{entity_text}'")
    
    # 旧式のチェック
    old_check = entity_text in highlighted_text and highlighted_text.count(f'>{entity_text}<') == 0
    print(f"旧式チェック: {old_check}")
    print(f"  - エンティティ存在: {entity_text in highlighted_text}")
    print(f"  - パターン '>{entity_text}<' カウント: {highlighted_text.count(f'>{entity_text}<')}")
    
    # 新式のチェック
    new_check = entity_text in highlighted_text and f'>{entity_text}</span>' not in highlighted_text
    print(f"新式チェック: {new_check}")
    print(f"  - エンティティ存在: {entity_text in highlighted_text}")
    print(f"  - パターン '>{entity_text}</span>' 存在: {f'>{entity_text}</span>' in highlighted_text}")
    
    # 実際のハイライト済み部分を確認
    span_start = highlighted_text.find('<span')
    span_end = highlighted_text.find('</span>') + 7
    if span_start != -1 and span_end != -1:
        span_content = highlighted_text[span_start:span_end]
        print(f"\n実際のspan内容:")
        print(f"{span_content}")
    
    print(f"\n=== 結論 ===")
    if old_check and not new_check:
        print("✅ 修正により重複を正しく検出できるようになりました")
    elif not old_check and new_check:
        print("⚠️ 修正により新たな問題が発生した可能性があります") 
    else:
        print("ℹ️ 両方のチェックで同じ結果です")

if __name__ == "__main__":
    test_duplicate_check_fix()
