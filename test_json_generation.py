#!/usr/bin/env python3
"""
JSON生成のテストスクリプト
health_analysis.pyが正しくJSONを生成できるかテストします
"""

import json
import os
from pathlib import Path
import sys

def test_json_generation():
    """JSONファイル生成をテスト"""
    print("JSON生成テストを開始します...")
    
    # 既存のJSONファイルがあれば削除
    json_path = 'static/analysis_results.json'
    if os.path.exists(json_path):
        os.remove(json_path)
        print("既存のJSONファイルを削除しました")
    
    # health_analysis.pyをインポートして実行
    try:
        from health_analysis import load_and_analyze_health_data
        results = load_and_analyze_health_data()
        print("✅ health_analysis.py の実行が完了しました")
    except Exception as e:
        print(f"❌ health_analysis.py の実行でエラー: {e}")
        return False
    
    # JSONファイルが作成されたか確認
    if not os.path.exists(json_path):
        print(f"❌ JSONファイル {json_path} が作成されませんでした")
        return False
    
    # JSONファイルが正しく読み込めるか確認
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        print("✅ JSONファイルの読み込みが成功しました")
        
        # 基本的な構造をチェック
        required_keys = ['basic_info', 'summary_statistics', 'age_group_statistics', 
                        'bmi_category_statistics', 'correlations']
        for key in required_keys:
            if key not in loaded_data:
                print(f"❌ 必要なキー '{key}' がJSONに含まれていません")
                return False
        
        print("✅ JSONファイルの構造が正しいことを確認しました")
        print(f"ファイルサイズ: {os.path.getsize(json_path)} bytes")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ JSONの解析でエラー: {e}")
        # JSONファイルの内容を確認
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"ファイルの内容 (最初の500文字):")
            print(content[:500])
        except Exception:
            print("ファイルの内容を読み取れませんでした")
        return False
    except Exception as e:
        print(f"❌ ファイル読み込みでエラー: {e}")
        return False

if __name__ == "__main__":
    if test_json_generation():
        print("\n🎉 全てのテストが成功しました！")
        sys.exit(0)
    else:
        print("\n💥 テストが失敗しました")
        sys.exit(1)