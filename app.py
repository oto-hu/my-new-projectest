from flask import Flask, render_template, jsonify
import json
import os
from pathlib import Path
import subprocess
import sys

app = Flask(__name__)

def ensure_analysis_results():
    """解析結果が存在しない場合は解析を実行"""
    if not os.path.exists('static/analysis_results.json'):
        print("解析結果が見つかりません。解析を実行します...")
        try:
            subprocess.run([sys.executable, 'health_analysis.py'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"解析実行エラー: {e}")
            return False
    return True

@app.route('/')
def index():
    """メインページ"""
    if not ensure_analysis_results():
        return "解析の実行に失敗しました。", 500
    
    # 解析結果を読み込み
    try:
        with open('static/analysis_results.json', 'r', encoding='utf-8') as f:
            results = json.load(f)
    except FileNotFoundError:
        return "解析結果が見つかりません。", 404
    
    return render_template('index.html', results=results)

@app.route('/api/analysis')
def api_analysis():
    """解析結果のAPI"""
    if not ensure_analysis_results():
        return jsonify({"error": "解析の実行に失敗しました"}), 500
    
    try:
        with open('static/analysis_results.json', 'r', encoding='utf-8') as f:
            results = json.load(f)
        return jsonify(results)
    except FileNotFoundError:
        return jsonify({"error": "解析結果が見つかりません"}), 404

@app.route('/api/rerun-analysis')
def api_rerun_analysis():
    """解析を再実行するAPI"""
    try:
        subprocess.run([sys.executable, 'health_analysis.py'], check=True)
        return jsonify({"message": "解析が正常に完了しました"})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"解析実行エラー: {e}"}), 500

if __name__ == '__main__':
    # staticディレクトリとimagesディレクトリを作成
    Path('static/images').mkdir(parents=True, exist_ok=True)
    Path('templates').mkdir(parents=True, exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)