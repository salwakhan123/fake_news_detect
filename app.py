from flask import Flask, render_template_string, request
import re

app = Flask(__name__)

def detect_fake_news(text):
    text = text.lower()
    fake_keywords = ['alien', 'ufo', 'conspiracy', 'hoax', 'fake', 'lie', 'scam', 'secret', 'coverup', 'illuminati', 'vaccine chip', '5g danger']
    real_keywords = ['government', 'official', 'study', 'research', 'launch', 'announce', 'president', 'parliament', 'court', 'university', 'isro', 'nasa']
    
    fake_score = sum(1 for word in fake_keywords if word in text)
    real_score = sum(1 for word in real_keywords if word in text)
    
    if fake_score >= 1:
        return "FAKE ❌", 95
    elif real_score >= 1:
        return "REAL ✅", 92
    else:
        return "SUSPICIOUS ⚠️", 75

@app.route('/', methods=['GET', 'POST'])
def home():
    result = ""
    confidence = ""
    input_text = ""
    result_class = ""
    result_html = ""
    
    if request.method == 'POST':
        input_text = request.form.get('news', '').strip()
        if input_text:
            result, confidence = detect_fake_news(input_text)
            result_class = "real" if "REAL" in result else "fake" if "FAKE" in result else "suspicious"
            result_html = f"<div class='result {result_class}'>{result}<div class='confidence'>Confidence: {confidence}%</div></div>"
    
    # CSS fixed with double braces and a very high-quality background link
    html = f'''
<!DOCTYPE html>
<html>
<head>
    <title>🚀 AI FAKE NEWS DETECTOR</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        *{{{{margin:0;padding:0;box-sizing:border-box}}}}
        
        body{{{{
            font-family:'Segoe UI', Tahoma, sans-serif;
            /* Yahan humne ek naya reliable background link dala hai */
            background-image: linear-gradient(rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0.75)), 
                              url('https://cdn.pixabay.com/photo/2015/02/15/03/04/news-636911_1280.jpg');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            margin: 0;
        }}}}

        .container{{{{
            max-width: 700px;
            width: 100%;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 25px;
            padding: 40px;
            box-shadow: 0 25px 60px rgba(0,0,0,0.4);
            text-align: center;
        }}}}

        h1{{{{color: #2c3e50; margin-bottom: 10px; font-size: 2.5em;}}}}
        .subtitle{{{{color: #7f8c8d; margin-bottom: 25px;}}}}

        textarea{{{{
            width: 100%; height: 150px; padding: 20px; border: 2px solid #ddd;
            border-radius: 15px; font-size: 16px; margin-bottom: 15px;
        }}}}

        .analyze-btn{{{{
            width: 100%; padding: 18px; background: #3498db; color: white;
            border: none; border-radius: 12px; font-size: 18px; cursor: pointer;
        }}}}

        .result{{{{margin-top: 25px; padding: 20px; border-radius: 15px; color: white; font-weight: bold; font-size: 24px;}}}}
        .real{{{{background: #27ae60;}}}} .fake{{{{background: #e74c3c;}}}} .suspicious{{{{background: #f39c12;}}}}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Fake News Detector</h1>
        <p class="subtitle">AI-Powered Detection</p>
        <form method="POST">
            <textarea name="news" placeholder="Paste news content here...">{input_text}</textarea>
            <button type="submit" class="analyze-btn">🎯 ANALYZE NOW</button>
        </form>
        {result_html}
    </div>
</body>
</html>
    '''
    return html.format(input_text=input_text, result_html=result_html)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
