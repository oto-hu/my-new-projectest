import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import json

def load_and_analyze_health_data():
    """
    健康診断データの解析を実行し、結果をJSONと画像で保存する
    """
    
    # TASK-01: データ読み込みと基本情報確認
    print("TASK-01: データ読み込みと基本情報確認")
    print("=" * 50)
    
    df = pd.read_csv('health_check_sample.csv')
    
    basic_info = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'columns': list(df.columns),
        'data_types': df.dtypes.astype(str).to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'memory_usage': df.memory_usage(deep=True).sum()
    }
    
    print(f"総行数: {basic_info['total_rows']}")
    print(f"総列数: {basic_info['total_columns']}")
    print(f"列名: {basic_info['columns']}")
    print("\nデータ型:")
    for col, dtype in basic_info['data_types'].items():
        print(f"  {col}: {dtype}")
    
    print("\n欠損値:")
    for col, missing in basic_info['missing_values'].items():
        print(f"  {col}: {missing}")
    
    # TASK-02: 要約統計量の算出
    print("\n\nTASK-02: 要約統計量の算出")
    print("=" * 50)
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    summary_stats = df[numeric_cols].describe().to_dict()
    
    print("数値列の要約統計量:")
    print(df[numeric_cols].describe())
    
    # TASK-03: 主要指標の算出と分析（健康データに合わせて調整）
    print("\n\nTASK-03: 主要指標の算出と分析")
    print("=" * 50)
    
    # BMI計算
    df['BMI'] = df['Weight_kg'] / (df['Height_cm'] / 100) ** 2
    
    # BMIカテゴリ
    def categorize_bmi(bmi):
        if bmi < 18.5:
            return '低体重'
        elif bmi < 25:
            return '標準体重'
        elif bmi < 30:
            return '肥満1度'
        else:
            return '肥満2度以上'
    
    df['BMI_Category'] = df['BMI'].apply(categorize_bmi)
    
    # 年代別分析
    df['Age_Group'] = pd.cut(df['Age'], bins=[0, 30, 40, 50, 60, 100], 
                            labels=['20代', '30代', '40代', '50代', '60代以上'])
    
    # 年代別平均値
    age_group_stats = df.groupby('Age_Group').agg({
        'BMI': 'mean',
        'Systolic_BP': 'mean',
        'Diastolic_BP': 'mean',
        'Cholesterol': 'mean',
        'Exercise_Days_Per_Week': 'mean'
    }).round(2)
    
    print("年代別平均値:")
    print(age_group_stats)
    
    # BMIカテゴリ別統計
    bmi_category_stats = df['BMI_Category'].value_counts()
    print("\nBMIカテゴリ別人数:")
    print(bmi_category_stats)
    
    # TASK-04: データ可視化
    print("\n\nTASK-04: データ可視化")
    print("=" * 50)
    
    # 可視化用のディレクトリを作成
    Path('static/images').mkdir(parents=True, exist_ok=True)
    
    # 1. BMIカテゴリ別人数の棒グラフ
    plt.figure(figsize=(10, 6))
    bmi_category_stats.plot(kind='bar', color='skyblue')
    plt.title('BMIカテゴリ別人数分布')
    plt.xlabel('BMIカテゴリ')
    plt.ylabel('人数')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/images/bmi_category_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. 年代別平均BMI推移
    plt.figure(figsize=(10, 6))
    age_group_stats['BMI'].plot(kind='line', marker='o', color='red')
    plt.title('年代別平均BMI推移')
    plt.xlabel('年代')
    plt.ylabel('平均BMI')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('static/images/age_group_bmi_trend.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. 運動日数と健康指標の相関散布図
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # BMIと運動日数
    axes[0, 0].scatter(df['Exercise_Days_Per_Week'], df['BMI'], alpha=0.6, color='blue')
    axes[0, 0].set_xlabel('週間運動日数')
    axes[0, 0].set_ylabel('BMI')
    axes[0, 0].set_title('運動日数 vs BMI')
    
    # 収縮期血圧と運動日数
    axes[0, 1].scatter(df['Exercise_Days_Per_Week'], df['Systolic_BP'], alpha=0.6, color='red')
    axes[0, 1].set_xlabel('週間運動日数')
    axes[0, 1].set_ylabel('収縮期血圧')
    axes[0, 1].set_title('運動日数 vs 収縮期血圧')
    
    # コレステロールと運動日数
    axes[1, 0].scatter(df['Exercise_Days_Per_Week'], df['Cholesterol'], alpha=0.6, color='green')
    axes[1, 0].set_xlabel('週間運動日数')
    axes[1, 0].set_ylabel('コレステロール値')
    axes[1, 0].set_title('運動日数 vs コレステロール値')
    
    # 空腹時血糖値と運動日数
    axes[1, 1].scatter(df['Exercise_Days_Per_Week'], df['Fasting_Blood_Sugar'], alpha=0.6, color='orange')
    axes[1, 1].set_xlabel('週間運動日数')
    axes[1, 1].set_ylabel('空腹時血糖値')
    axes[1, 1].set_title('運動日数 vs 空腹時血糖値')
    
    plt.tight_layout()
    plt.savefig('static/images/exercise_correlation_scatter.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 4. 健康指標の分布ヒストグラム
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    
    df['BMI'].hist(bins=20, ax=axes[0, 0], color='lightblue', edgecolor='black')
    axes[0, 0].set_title('BMI分布')
    axes[0, 0].set_xlabel('BMI')
    
    df['Systolic_BP'].hist(bins=20, ax=axes[0, 1], color='lightcoral', edgecolor='black')
    axes[0, 1].set_title('収縮期血圧分布')
    axes[0, 1].set_xlabel('収縮期血圧')
    
    df['Diastolic_BP'].hist(bins=20, ax=axes[0, 2], color='lightgreen', edgecolor='black')
    axes[0, 2].set_title('拡張期血圧分布')
    axes[0, 2].set_xlabel('拡張期血圧')
    
    df['Cholesterol'].hist(bins=20, ax=axes[1, 0], color='gold', edgecolor='black')
    axes[1, 0].set_title('コレステロール値分布')
    axes[1, 0].set_xlabel('コレステロール値')
    
    df['Fasting_Blood_Sugar'].hist(bins=20, ax=axes[1, 1], color='plum', edgecolor='black')
    axes[1, 1].set_title('空腹時血糖値分布')
    axes[1, 1].set_xlabel('空腹時血糖値')
    
    df['Exercise_Days_Per_Week'].hist(bins=8, ax=axes[1, 2], color='lightsteelblue', edgecolor='black')
    axes[1, 2].set_title('週間運動日数分布')
    axes[1, 2].set_xlabel('週間運動日数')
    
    plt.tight_layout()
    plt.savefig('static/images/health_indicators_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 結果をJSONで保存
    try:
        # JSONに変換できない値（NaN等）を処理
        correlations = {}
        for key, corr_data in [
            ('exercise_bmi', df[['Exercise_Days_Per_Week', 'BMI']]),
            ('exercise_systolic_bp', df[['Exercise_Days_Per_Week', 'Systolic_BP']]),
            ('exercise_cholesterol', df[['Exercise_Days_Per_Week', 'Cholesterol']]),
            ('exercise_blood_sugar', df[['Exercise_Days_Per_Week', 'Fasting_Blood_Sugar']])
        ]:
            corr_value = corr_data.corr().iloc[0, 1]
            correlations[key] = float(corr_value) if not np.isnan(corr_value) else 0.0
        
        analysis_results = {
            'basic_info': basic_info,
            'summary_statistics': summary_stats,
            'age_group_statistics': age_group_stats.to_dict(),
            'bmi_category_statistics': bmi_category_stats.to_dict(),
            'correlations': correlations
        }
        
        # staticディレクトリを確実に作成
        Path('static').mkdir(exist_ok=True)
        
        # 一時ファイルに書き込んでからrenameで原子的に更新
        temp_file = 'static/analysis_results.json.tmp'
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_results, f, ensure_ascii=False, indent=2)
        
        # ファイルを原子的に置き換え
        import os
        os.rename(temp_file, 'static/analysis_results.json')
        
    except Exception as e:
        print(f"JSON保存エラー: {e}")
        # エラーの場合でも部分的な結果を保存
        Path('static').mkdir(exist_ok=True)
        error_result = {
            'error': f"解析中にエラーが発生しました: {e}",
            'basic_info': basic_info if 'basic_info' in locals() else {},
            'summary_statistics': summary_stats if 'summary_stats' in locals() else {}
        }
        with open('static/analysis_results.json', 'w', encoding='utf-8') as f:
            json.dump(error_result, f, ensure_ascii=False, indent=2)
        raise
    
    print("解析完了！結果は以下に保存されました：")
    print("- static/analysis_results.json: 解析結果データ")
    print("- static/images/bmi_category_distribution.png: BMIカテゴリ分布")
    print("- static/images/age_group_bmi_trend.png: 年代別BMI推移")
    print("- static/images/exercise_correlation_scatter.png: 運動と健康指標の相関")
    print("- static/images/health_indicators_distribution.png: 各健康指標の分布")
    
    return analysis_results

if __name__ == "__main__":
    results = load_and_analyze_health_data()