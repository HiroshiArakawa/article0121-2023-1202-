"""
第三条での閉じタグ問題のデバッグ
"""

import sys
import os
import re

# プロジェクトのルートディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def debug_span_tag_issue():
    """閉じタグ問題をデバッグ"""
    
    # 問題のあるテキスト（ユーザーが報告したもの）
    problematic_text = """２ 特許出願、請求その他特許に関する手続（以下単に「手続」という。）についての期間の末日が行政機関の休日に関する法律（<span style="background-color: #FFB6C1; padding: 1px 3px; margin: 0 1px; border-radius: 3px; font-weight: 500; border: 1px solid #FFB6C188; border: 2px solid #FF6B6B; box-shadow: 0 0 10px rgba(255, 107, 107, 0.5);" title="法律参照: 昭和六十三年法律第九十一号">昭和六十三年法律第九十一号）第一条第一項各号に掲げる日に当たるときは、その日の翌日をもつてその期間の末日とする。"""
    
    print("=== 閉じタグ問題のデバッグ ===")
    print(f"問題のテキスト長: {len(problematic_text)}")
    print(f"テキスト: {problematic_text}")
    
    # HTMLタグを分析
    print("\n=== HTMLタグ分析 ===")
    
    # 開始タグを検索
    opening_tags = re.findall(r'<span[^>]*>', problematic_text)
    print(f"開始 <span> タグ: {len(opening_tags)}個")
    for i, tag in enumerate(opening_tags):
        print(f"  {i+1}. {tag}")
    
    # 閉じタグを検索
    closing_tags = re.findall(r'</span>', problematic_text)
    print(f"閉じ </span> タグ: {len(closing_tags)}個")
    for i, tag in enumerate(closing_tags):
        print(f"  {i+1}. {tag}")
    
    # タグバランスの確認
    if len(opening_tags) != len(closing_tags):
        print(f"\n❌ タグバランス問題: 開始タグ{len(opening_tags)}個 vs 閉じタグ{len(closing_tags)}個")
    else:
        print(f"\n✅ タグバランス正常: {len(opening_tags)}個ずつ")
    
    # 対象のエンティティテキストを確認
    print("\n=== エンティティ分析 ===")
    entity_text = "昭和六十三年法律第九十一号"
    print(f"対象エンティティ: '{entity_text}'")
    
    # エンティティテキストの前後を確認
    entity_pos = problematic_text.find(entity_text)
    if entity_pos != -1:
        before = problematic_text[max(0, entity_pos-50):entity_pos]
        after = problematic_text[entity_pos+len(entity_text):entity_pos+len(entity_text)+50]
        print(f"前文脈: ...{before}")
        print(f"対象: {entity_text}")
        print(f"後文脈: {after}...")
        
        # 閉じタグが直後にあるかチェック
        immediate_after = problematic_text[entity_pos+len(entity_text):entity_pos+len(entity_text)+10]
        print(f"直後の文字: '{immediate_after}'")
        
        if immediate_after.startswith('</span>'):
            print("✅ 閉じタグが直後にあります")
        else:
            print("❌ 閉じタグが直後にありません")
    
    # 修正シミュレーション
    print("\n=== 修正シミュレーション ===")
    
    # パターン1: 正規表現で修正
    if entity_text in problematic_text and not problematic_text.count(f'{entity_text}</span>'):
        print("パターン1: 閉じタグが欠けている可能性")
        # 欠けた閉じタグを追加
        fixed_text = problematic_text.replace(
            f'{entity_text}）',
            f'{entity_text}</span>）'
        )
        print(f"修正後の該当部分: ...{fixed_text[entity_pos-10:entity_pos+len(entity_text)+20]}...")
    
    # パターン2: HTMLエスケープ問題
    print("\nパターン2: HTMLエスケープ問題のチェック")
    if '&lt;' in problematic_text or '&gt;' in problematic_text:
        print("❌ HTMLエスケープが含まれています")
    else:
        print("✅ HTMLエスケープ問題なし")

if __name__ == "__main__":
    debug_span_tag_issue()
