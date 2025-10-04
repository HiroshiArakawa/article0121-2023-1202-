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
                # 他の法律への参照
                r'([^条文]*法)(第[^条]*条|第[^章]*章|第[^節]*節)?',
                r'(特許法|実用新案法|意匠法|商標法|著作権法|民法|刑法|行政手続法|知的財産基本法)',
                r'(政令|省令|規則|告示)',
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
                # 期間表現
                r'([一二三四五六七八九十百千万〇０-９0-9]+)(年|月|日|週間|か月)',
                r'([一二三四五六七八九十百千万〇０-９0-9]+)(年以内|月以内|日以内)',
                r'(直ちに|速やかに|遅滞なく)',
                r'(公告の日|設定の登録の日|出願の日|審決の日)',
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
        
        return entities
    
    def analyze_article_text(self, article_data: Dict) -> Dict:
        """
        条文データの固有表現解析
        
        Args:
            article_data: 条文データ
            
        Returns:
            固有表現解析結果を含む条文データ
        """
        result = article_data.copy()
        
        # 条文テキストの取得
        article_text = article_data.get('text', '')
        title = article_data.get('title', '')
        
        # 全体テキストの構成
        full_text = f"{title}\n{article_text}"
        
        # 固有表現抽出
        entities = self.extract_entities(full_text)
        
        # 結果に追加
        result['ner_entities'] = entities
        result['ner_summary'] = self._create_summary(entities)
        
        return result
    
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
