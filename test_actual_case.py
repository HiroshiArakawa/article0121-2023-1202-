"""
実際の問題ケースのテスト
"""

def test_actual_problem_case():
    """ユーザーが報告した実際の問題をテスト"""
    
    print("=== 実際の問題ケーステスト ===")
    
    # ユーザーが報告したテキスト（ただし閉じタグを追加して完全版を作成）
    original_problematic = """２ 特許出願、請求その他特許に関する手続（以下単に「手続」という。）についての期間の末日が行政機関の休日に関する法律（<span style="background-color: #FFB6C1; padding: 1px 3px; margin: 0 1px; border-radius: 3px; font-weight: 500; border: 1px solid #FFB6C188; border: 2px solid #FF6B6B; box-shadow: 0 0 10px rgba(255, 107, 107, 0.5);" title="法律参照: 昭和六十三年法律第九十一号">昭和六十三年法律第九十一号）第一条第一項各号に掲げる日に当たるときは、その日の翌日をもつてその期間の末日とする。"""
    
    # 問題のエンティティ
    entity_text = "昭和六十三年法律第九十一号"
    
    print(f"問題のエンティティ: '{entity_text}'")
    print(f"元テキスト長: {len(original_problematic)}")
    
    # HTMLタグの状態を確認
    import re
    opening_tags = re.findall(r'<span[^>]*>', original_problematic)
    closing_tags = re.findall(r'</span>', original_problematic)
    
    print(f"\n=== HTMLタグ状態 ===")
    print(f"開始タグ: {len(opening_tags)}個")
    print(f"閉じタグ: {len(closing_tags)}個")
    
    if len(opening_tags) > len(closing_tags):
        print("❌ 閉じタグが不足しています")
        
        # 閉じタグを修正
        # エンティティテキストの直後に閉じタグを挿入
        if entity_text in original_problematic:
            # エンティティテキストの位置を特定
            entity_pos = original_problematic.find(entity_text)
            entity_end = entity_pos + len(entity_text)
            
            # エンティティの前後を確認
            before = original_problematic[max(0, entity_pos-50):entity_pos]
            after = original_problematic[entity_end:entity_end+20]
            
            print(f"\nエンティティ前文脈: ...{before}")
            print(f"エンティティ: {entity_text}")
            print(f"エンティティ後文脈: {after}...")
            
            # 修正: エンティティの直後に閉じタグを挿入
            fixed_text = (
                original_problematic[:entity_end] + 
                '</span>' + 
                original_problematic[entity_end:]
            )
            
            print(f"\n=== 修正後 ===")
            print(f"修正後テキスト長: {len(fixed_text)}")
            
            # 修正後のタグ状態を確認
            fixed_opening = re.findall(r'<span[^>]*>', fixed_text)
            fixed_closing = re.findall(r'</span>', fixed_text)
            print(f"修正後 開始タグ: {len(fixed_opening)}個")
            print(f"修正後 閉じタグ: {len(fixed_closing)}個")
            
            if len(fixed_opening) == len(fixed_closing):
                print("✅ タグバランスが修正されました")
            
            # 修正された部分を表示
            fixed_entity_pos = fixed_text.find(entity_text)
            fixed_entity_end = fixed_entity_pos + len(entity_text)
            context = fixed_text[fixed_entity_pos-20:fixed_entity_end+20]
            print(f"修正された部分: ...{context}...")
            
            return fixed_text
    else:
        print("✅ タグバランスは正常です")
        
    return original_problematic

if __name__ == "__main__":
    result = test_actual_problem_case()
    
    # 結果をファイルに保存
    with open('fixed_problematic_text.html', 'w', encoding='utf-8') as f:
        f.write(result)
    print(f"\n修正結果を fixed_problematic_text.html に保存しました")
