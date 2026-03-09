import json
import os
from datetime import datetime

def generate_html_dashboard():
    # Looking for the latest processed news file
    data_dir = "data/"
    if not os.path.exists(data_dir):
        # Fallback for different working directory scenarios
        data_dir = "social-intelligence-mvp/data/"
    
    processed_files = [f for f in os.listdir(data_dir) if f.startswith("processed_news_")]
    if not processed_files:
        # Fallback to any raw news if no processed exists
        processed_files = [f for f in os.listdir(data_dir) if f.startswith("raw_")]
        if not processed_files:
            return "No data files found."
    
    latest_file = os.path.join(data_dir, sorted(processed_files)[-1])
    
    with open(latest_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Sentiment distribution calculation
    stats = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for item in data:
        sentiment = item.get('sentiment', 'Neutral').capitalize()
        if sentiment in stats:
            stats[sentiment] += 1
        else:
            stats["Neutral"] += 1

    # Dark mode / Cyberpunk UI Template
    html_content = f"""
    <!DOCTYPE html>
    <html lang="zh-CN" class="dark">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Social Intelligence MVP - Brand Insight</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script>
            tailwind.config = {{
                darkMode: 'class',
                theme: {{
                    extend: {{
                        colors: {{
                            cyber: {{
                                black: '#0a0a0c',
                                card: '#16161a',
                                primary: '#3b82f6',
                                accent: '#00f2ff',
                                danger: '#ff0055',
                                success: '#00ffaa'
                            }}
                        }}
                    }}
                }}
            }}
        </script>
        <style>
            body {{ background-color: #0a0a0c; color: #e2e8f0; }}
            .cyber-card {{ 
                background-color: #16161a; 
                border: 1px solid #2d2d35;
                transition: transform 0.2s, border-color 0.2s;
            }}
            .cyber-card:hover {{ 
                transform: translateY(-2px);
                border-color: #3b82f6;
            }}
            .sentiment-positive {{ border-left: 4px solid #00ffaa; }}
            .sentiment-negative {{ border-left: 4px solid #ff0055; }}
            .sentiment-neutral {{ border-left: 4px solid #3b82f6; }}
            .chart-container {{ position: relative; height: 250px; width: 100%; }}
        </style>
    </head>
    <body class="font-sans leading-normal tracking-normal p-6">
        <div class="container mx-auto">
            <header class="mb-10 flex flex-col md:flex-row justify-between items-center">
                <div>
                    <h1 class="text-3xl font-black text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-400 uppercase tracking-wider">
                        Social Intelligence MVP
                    </h1>
                    <p class="text-gray-500 mt-1">AI-Powered Brand Sentiment Analysis | Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
                <div class="mt-4 md:mt-0 px-4 py-2 rounded-lg bg-cyber-card border border-gray-800">
                    <span class="text-xs text-gray-500 block uppercase">Analyzing Keywords</span>
                    <span class="text-sm font-bold text-blue-400">君乐宝, 飞鹤, 雪花啤酒, 临工重机</span>
                </div>
            </header>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
                <!-- Stats Section -->
                <div class="cyber-card p-6 rounded-xl flex flex-col justify-center">
                    <h3 class="text-gray-400 text-sm uppercase font-bold mb-4">Sentiment Distribution</h3>
                    <div class="chart-container">
                        <canvas id="sentimentChart"></canvas>
                    </div>
                </div>

                <!-- Feed Section -->
                <div class="lg:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-4 overflow-y-auto max-h-[600px] pr-2">
    """

    for item in data:
        sentiment = item.get('sentiment', 'Neutral')
        sentiment_class = f"sentiment-{sentiment.lower()}"
        
        # Risk indicator
        risk_icon = ""
        if sentiment.lower() == 'negative':
            risk_icon = '<span class="text-cyber-danger text-xs flex items-center mt-1"><svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path></svg> HIGH RISK ALERT</span>'

        html_content += f"""
                    <div class="cyber-card p-5 rounded-lg {sentiment_class}">
                        <div class="flex justify-between items-start mb-2">
                            <span class="px-2 py-0.5 text-[10px] font-bold tracking-widest text-cyber-primary border border-cyber-primary rounded uppercase">
                                {item.get('keyword', 'GENERAL')}
                            </span>
                            <span class="text-[10px] text-gray-600 font-mono italic">{item.get('source', 'Web')}</span>
                        </div>
                        <h2 class="text-md font-bold text-gray-200 leading-snug mb-2">
                            <a href="{item.get('url', item.get('link', '#'))}" target="_blank" class="hover:text-cyber-accent transition-colors">
                                {item.get('title', 'No Title')}
                            </a>
                        </h2>
                        <p class="text-xs text-gray-400 line-clamp-3 mb-3">
                            {item.get('summary', item.get('content', '')[:100])}
                        </p>
                        <div class="flex justify-between items-end border-t border-gray-800 pt-3 mt-2">
                            <span class="text-[10px] text-gray-600 uppercase">Analysis: <span class="text-gray-400">{sentiment}</span></span>
                            {risk_icon}
                        </div>
                    </div>
        """

    html_content += f"""
                </div>
            </div>
            
            <footer class="mt-12 text-center border-t border-gray-900 pt-8 pb-4">
                <p class="text-gray-600 text-[10px] uppercase tracking-[0.2em]">Generated by Eric Agent @ OpenClaw | Strategic Social Intelligence MVP</p>
            </footer>
        </div>

        <script>
            const ctx = document.getElementById('sentimentChart').getContext('2d');
            new Chart(ctx, {{
                type: 'doughnut',
                data: {{
                    labels: ['Positive', 'Negative', 'Neutral'],
                    datasets: [{{
                        data: [{stats['Positive']}, {stats['Negative']}, {stats['Neutral']}],
                        backgroundColor: ['#00ffaa', '#ff0055', '#3b82f6'],
                        borderColor: '#16161a',
                        borderWidth: 2,
                        hoverOffset: 10
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            position: 'bottom',
                            labels: {{
                                color: '#94a3b8',
                                usePointStyle: true,
                                padding: 20,
                                font: {{ size: 11, family: 'monospace' }}
                            }}
                        }}
                    }},
                    cutout: '70%'
                }}
            }});
        </script>
    </body>
    </html>
    """
    
    # We write to social-intelligence-mvp/index.html but we check current dir
    output_path = "index.html"
    if "social-intelligence-mvp" not in os.getcwd():
        output_path = "social-intelligence-mvp/index.html"
        
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    return output_path

if __name__ == "__main__":
    path = generate_html_dashboard()
    print(f"Dashboard generated at: {path}")
