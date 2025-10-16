"""
特許法条文用の固有表現抽出（NER）機能
"""

import re
import pandas as pd
from typing import List, Dict, Tuple, Any, Union
import pickle

class PatentLawNER:
    """特許法条文に特化した固有表現抽出クラス"""
    
    def __init__(self):
        # 法的固有表現のパターン定義
        self.patterns = {
            'LAW_REFERENCE': [
                # 具体的な法律名
                r'(特許法|実用新案法|意匠法|商標法|著作権法|民法|刑法|行政手続法|知的財産基本法|不正競争防止法|独占禁止法|会社法|商標法等の一部を改正する法律)(第[^条]*条|第[^章]*章|第[^節]*節)?',
                r'([不民商工労建独消債公行政][^この本当該同あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん]*法律?)(第[^条]*条|第[^章]*章|第[^節]*節)?',
                # 代名詞的法律参照（「この法律」「その法律」など全体を抽出）
                r'(この法律|その法律|当該法律|本法律)',
                r'(この法|その法|当該法|本法)',
                r'(政令|省令|規則|告示)',
                # 年号付きの法律
                r'(平成|昭和|令和|大正|明治)[一二三四五六七八九十百千万〇０-９0-9]+年法律第[一二三四五六七八九十百千万〇０-９0-9]+号',
                r'(平成|昭和|令和|大正|明治)[一二三四五六七八九十百千万〇０-９0-9]+年.*?法律',
            ],
            'ARTICLE_REFERENCE': [
                # 条文参照
                r'第([一二三四五六七八九十百千万〇０-９0-9]+)条(の[一二三四五六七八九十百千万〇０-９0-9]+)?',
                r'第([一二三四五六七八九十百千万〇０-９0-9]+)項',
                r'第([一二三四五六七八九十百千万〇０-９0-9]+)号',
                r'第([一二三四五六七八九十百千万〇０-９0-9]+)章',
                r'第([一二三四五六七八九十百千万〇０-９0-9]+)節',
                r'附則',
                r'前条|次条|同条|各条',
                r'前項|次項|同項|各項',
                r'前号|次号|同号|各号',
            ],
            'TIME_PERIOD': [
                # 複合期間表現（より具体的なパターンを先に配置）
                r'([一二三四五六七八九十百千万〇０-９0-9]+年[一二三四五六七八九十百千万〇０-９0-9]+月)',
                r'([一二三四五六七八九十百千万〇０-９0-9]+月[一二三四五六七八九十百千万〇０-９0-9]+日)',
                r'([一二三四五六七八九十百千万〇０-９0-9]+年[一二三四五六七八九十百千万〇０-９0-9]+月[一二三四五六七八九十百千万〇０-９0-9]+日)',
                # 基本的な期間表現
                r'([一二三四五六七八九十百千万〇０-９0-9]+)(年|月|日|週間|か月)',
                r'([一二三四五六七八九十百千万〇０-９0-9]+)(年以内|月以内|日以内)',
                # 相対的な期間表現
                r'(直ちに|速やかに|遅滞なく)',
                r'(公告の日|設定の登録の日|出願の日|審決の日)',
                # 期間の起点・終点表現
                r'([一二三四五六七八九十百千万〇０-９0-9]+)(年間|月間|日間)',
                r'(から|まで|以内|以上|未満|を経過)',
            ],
            'MONEY_AMOUNT': [
                # 金額表現
                r'([一二三四五六七八九十百千万億兆〇０-９0-9,，]+)(円|万円|千円)',
                r'(手数料|登録料|年金|審査料|審判料)',
            ],
            'ORGANIZATION': [
                # 組織・機関名
                r'(特許庁|知的財産高等裁判所|最高裁判所|地方裁判所|高等裁判所)',
                r'(審判官|審査官|特許庁長官|経済産業大臣)',
                r'(特許審判|審判廷|審判部)',
            ],
            'PROCEDURE': [
                # 手続き関連
                r'(出願|申請|請求|届出|登録|公告|公示)',
                r'(審査|審判|再審|異議申立て|無効審判)',
                r'(特許権|実用新案権|意匠権|商標権)',
                r'(発明|考案|意匠|商標)',
                r'(明細書|請求項|図面|要約書)',
            ],
            'LEGAL_STATUS': [
                # 法的地位・状態
                r'(権利者|出願人|代理人|利害関係人)',
                r'(無効|取消|拒絶|却下|棄却|認容)',
                r'(効力|権利|義務|責任)',
                r'(違反|侵害|損害)',
            ]
        }
        
        # コンパイル済み正規表現パターン
        self.compiled_patterns = {}
        for category, patterns in self.patterns.items():
            self.compiled_patterns[category] = [
                re.compile(pattern) for pattern in patterns
            ]
    
    def extract_entities(self, text: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        テキストから固有表現を抽出
        
        Args:
            text: 解析対象のテキスト
            
        Returns:
            カテゴリ別の固有表現リスト
        """
        entities = {}
        
        for category, patterns in self.compiled_patterns.items():
            entities[category] = []
            
            for pattern in patterns:
                matches = pattern.finditer(text)
                for match in matches:
                    entity = {
                        'text': match.group(0),
                        'start': match.start(),
                        'end': match.end(),
                        'pattern': pattern.pattern
                    }
                    
                    # 重複除去
                    if not any(e['text'] == entity['text'] and 
                             e['start'] == entity['start'] 
                             for e in entities[category]):
                        entities[category].append(entity)
            
            # 位置順でソート
            entities[category].sort(key=lambda x: x['start'])
        
        # 重複除去とフィルタリング
        entities = self._remove_overlaps(entities)
        
        # 不適切な表現のフィルタリング
        entities = self._filter_inappropriate_entities(entities)
        
        return entities
    
    def _filter_inappropriate_entities(self, entities: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        不適切な固有表現を除外
        
        Args:
            entities: カテゴリ別の固有表現リスト
            
        Returns:
            フィルタリング後の固有表現リスト
        """
        filtered_entities = {}
        
        # LAW_REFERENCEの不適切な表現リスト
        inappropriate_law_refs = {
            '法', 'の法', 'は法', 'に法', 'で法', 'を法', 'が法',
            'の法律', 'は法律', 'に法律', 'で法律', 'を法律', 'が法律',
            'り法', 'り法律', 'し法', 'し法律', 'て法', 'て法律'
        }
        
        for category, items in entities.items():
            filtered_items = []
            
            for item in items:
                text = item['text'].strip()
                
                if category == 'LAW_REFERENCE':
                    # 不適切な表現を除外
                    if text in inappropriate_law_refs:
                        continue
                    # 先頭に空白がある場合は除外（正規表現のキャプチャの問題）
                    if text.startswith(' '):
                        text = text.strip()
                        if text in inappropriate_law_refs:
                            continue
                    # 短すぎる表現や不適切な表現を除外
                    if len(text) < 2:
                        continue
                    # 単独の助詞や接続詞的な表現を除外
                    if text in ['は', 'の', 'が', 'を', 'に', 'で', 'と', 'や', 'から', 'まで']:
                        continue
                    # 「律は、」「法、」などの不完全な表現を除外
                    if text.endswith('、') or text.endswith('は') or text.endswith('が'):
                        continue
                    # 数字や助詞で始まる不適切な表現を除外
                    if text[0] in '0123456789０１２３４５６７８９〇一二三四五六七八九十はがをにで':
                        continue
                
                # テキストを正規化（前後の空白を削除）
                item['text'] = text
                filtered_items.append(item)
            
            filtered_entities[category] = filtered_items
        
        return filtered_entities
    
    def _remove_overlaps(self, entities: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        重複する固有表現を除去（長い表現を優先）
        
        Args:
            entities: カテゴリ別の固有表現リスト
            
        Returns:
            重複除去後の固有表現リスト
        """
        filtered_entities = {}
        
        for category, items in entities.items():
            if not items:
                filtered_entities[category] = []
                continue
            
            # 位置順でソート
            sorted_items = sorted(items, key=lambda x: (x['start'], -len(x['text'])))
            filtered_items = []
            
            for item in sorted_items:
                # 既存のアイテムと重複チェック
                is_overlapping = False
                for existing in filtered_items:
                    # 完全に含まれる場合（既存の方が長い）
                    if (existing['start'] <= item['start'] and 
                        item['end'] <= existing['end']):
                        is_overlapping = True
                        break
                    # 新しいアイテムが既存を含む場合
                    elif (item['start'] <= existing['start'] and 
                          existing['end'] <= item['end']):
                        # 既存のアイテムを削除して新しいアイテムを採用
                        filtered_items.remove(existing)
                        break
                
                if not is_overlapping:
                    filtered_items.append(item)
            
            filtered_entities[category] = filtered_items
        
        return filtered_entities
    
    def analyze_article_text(self, article_data: Dict) -> Dict:
        """
        条文データの固有表現解析
        
        Args:
            article_data: 条文データ
            
        Returns:
            固有表現解析結果を含む条文データ
        """
        result = article_data.copy()
        
        # 条文テキストの取得（HTMLタグ除去）
        article_text = self._get_clean_text(article_data)
        title = article_data.get('title', '')
        
        # 全体テキストの構成
        full_text = f"{title}\n{article_text}"
        
        # 固有表現抽出
        entities = self.extract_entities(full_text)
        
        # 結果に追加
        result['ner_entities'] = entities
        result['ner_summary'] = self._create_summary(entities)
        result['clean_text'] = article_text  # デバッグ用
        
        return result
    
    def _get_clean_text(self, article_data: Dict) -> str:
        """
        条文データからクリーンなテキストを抽出
        
        Args:
            article_data: 条文データ
            
        Returns:
            HTMLタグを除去したクリーンなテキスト
        """
        # 複数のフィールドを確認
        text_fields = ['text', 'body', 'content', 'article_text']
        
        for field in text_fields:
            if field in article_data:
                text = article_data[field]
                if text and isinstance(text, str):
                    # HTMLタグが含まれている場合は除去
                    if '<' in text and '>' in text:
                        try:
                            from bs4 import BeautifulSoup
                            soup = BeautifulSoup(text, 'html.parser')
                            clean_text = soup.get_text()
                            # 連続する空白や改行を整理
                            import re
                            clean_text = re.sub(r'\s+', ' ', clean_text).strip()
                            return clean_text
                        except:
                            # エラーの場合は簡単なタグ除去
                            import re
                            clean_text = re.sub(r'<[^>]+>', '', text)
                            clean_text = re.sub(r'\s+', ' ', clean_text).strip()
                            return clean_text
                    else:
                        return text.strip()
        
        return ""
    
    def _create_summary(self, entities: Dict) -> Dict:
        """固有表現の要約統計を作成"""
        summary = {}
        
        for category, entity_list in entities.items():
            summary[category] = {
                'count': len(entity_list),
                'unique_texts': list(set(e['text'] for e in entity_list))
            }
        
        return summary
    
    def process_all_articles(self, pickle_path: str) -> Union[List, Dict]:
        """
        全条文の固有表現解析
        
        Args:
            pickle_path: Pickleファイルのパス
            
        Returns:
            固有表現解析結果を含む全条文データ
        """
        # Pickleファイル読み込み
        with open(pickle_path, 'rb') as f:
            data = pickle.load(f)
        
        processed_data = []
        
        # データ構造に応じて処理
        if isinstance(data, list):
            # リスト形式の場合（章ごとの構造）
            for i, chapter in enumerate(data):
                if isinstance(chapter, dict) and 'articles' in chapter:
                    # 章内の条文を処理
                    processed_articles = []
                    for article in chapter['articles']:
                        if isinstance(article, dict):
                            processed_article = self.analyze_article_text(article)
                            processed_articles.append(processed_article)
                        else:
                            processed_articles.append(article)
                    
                    # 章構造を保持
                    processed_chapter = chapter.copy()
                    processed_chapter['articles'] = processed_articles
                    processed_data.append(processed_chapter)
                
                elif isinstance(chapter, dict) and 'text' in chapter:
                    # 単一条文の場合
                    processed_article = self.analyze_article_text(chapter)
                    processed_data.append(processed_article)
                else:
                    # その他の場合はそのまま追加
                    processed_data.append(chapter)
                
                # 進捗表示
                if (i + 1) % 10 == 0:
                    print(f"処理済み: {i + 1}/{len(data)} 章")
        
        elif isinstance(data, dict) and 'articles' in data:
            # 辞書形式の場合（従来）
            processed_data = data.copy()
            for i, article in enumerate(data['articles']):
                processed_article = self.analyze_article_text(article)
                processed_data['articles'][i] = processed_article
                
                # 進捗表示
                if (i + 1) % 10 == 0:
                    print(f"処理済み: {i + 1}/{len(data['articles'])} 条文")
        
        return processed_data
    
    def export_ner_results_to_csv(self, processed_data, output_path: str):
        """固有表現解析結果をCSVファイルにエクスポート"""
        rows = []
        
        # データ構造に応じて処理
        articles_to_process = []
        
        if isinstance(processed_data, list):
            # 章構造の場合
            for chapter in processed_data:
                if isinstance(chapter, dict) and 'articles' in chapter:
                    articles_to_process.extend(chapter['articles'])
                elif isinstance(chapter, dict) and 'ner_entities' in chapter:
                    articles_to_process.append(chapter)
        elif isinstance(processed_data, dict) and 'articles' in processed_data:
            articles_to_process = processed_data['articles']
        
        for article in articles_to_process:
            if not isinstance(article, dict):
                continue
                
            article_id = article.get('id', article.get('article_id', ''))
            title = article.get('title', article.get('heading', ''))
            
            if 'ner_entities' in article:
                for category, entities in article['ner_entities'].items():
                    for entity in entities:
                        rows.append({
                            'article_id': article_id,
                            'article_title': title,
                            'category': category,
                            'entity_text': entity['text'],
                            'start_pos': entity['start'],
                            'end_pos': entity['end'],
                            'pattern': entity['pattern']
                        })
        
        # DataFrame作成とCSV出力
        df = pd.DataFrame(rows)
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"固有表現解析結果を {output_path} に保存しました")
        
        return df


def main():
    """メイン実行関数"""
    import os
    
    # NERエクストラクター初期化
    ner = PatentLawNER()
    
    # Pickleファイルのパス
    pickle_file = '334AC0000000121_20230703_505AC0000000051.pickle'
    
    if not os.path.exists(pickle_file):
        print(f"エラー: {pickle_file} が見つかりません")
        return
    
    print("特許法条文の固有表現抽出を開始します...")
    
    # 全条文の解析
    processed_data = ner.process_all_articles(pickle_file)
    
    # 解析結果をPickleファイルに保存
    output_pickle = '334AC0000000121_20230703_505AC0000000051_with_ner.pickle'
    with open(output_pickle, 'wb') as f:
        pickle.dump(processed_data, f)
    print(f"固有表現解析済みデータを {output_pickle} に保存しました")
    
    # CSV出力
    csv_output = 'patent_law_ner_results.csv'
    df = ner.export_ner_results_to_csv(processed_data, csv_output)
    
    # 統計情報表示
    print("\n=== 固有表現抽出統計 ===")
    if len(df) > 0:
        category_counts = df['category'].value_counts()
        for category, count in category_counts.items():
            print(f"{category}: {count}個")
        print(f"\n合計: {len(df)}個の固有表現を抽出しました")
    else:
        print("固有表現が抽出されませんでした。データ構造を確認してください。")


if __name__ == "__main__":
    main()
