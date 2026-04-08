from flask import Flask, render_template_string, request
import re

app = Flask(__name__)

# Logic for Fake News Detection
def detect_fake_news(text):
    text = text.lower()
    # Predefined Keywords
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
    
    # CSS braces are doubled {{ }} because we use .format() at the end
    html = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>🚀 AI FAKE NEWS DETECTOR</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        *{{{{margin:0;padding:0;box-sizing:border-box}}}}
        
        body{{{{
            font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            /* Full Background Image with Overlay */
            background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
                        url('https://images.unsplash.com/photo-1585829365234-781fdfc4190b?q=80&w=2070&auto=format&fit=crop');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}}}

        .container{{{{
            max-width: 750px;
            width: 100%;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 30px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
            text-align: center;
            animation: fadeIn 0.8s ease;
        }}}}

        h1{{{{color: #2c3e50; font-size: 2.8em; margin-bottom: 10px;}}}}
        .subtitle{{{{color: #7f8c8d; margin-bottom: 30px; font-size: 1.1em;}}}}

        textarea{{{{
            width: 100%;
            height: 150px;
            padding: 20px;
            border: 2px solid #dfe6e9;
            border-radius: 15px;
            font-size: 16px;
            resize: none;
            transition: 0.3s;
            background: #f9f9f9;
        }}}}

        textarea:focus{{{{outline: none; border-color: #3498db; background: #fff; box-shadow: 0 0 15px rgba(52,152,219,0.2);}}}}

        .analyze-btn{{{{
            width: 100%;
            padding: 18px;
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            border: none;
            border-radius: 15px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 20px;
            transition: 0.3s;
        }}}}

        .analyze-btn:hover{{{{transform: translateY(-2px); box-shadow: 0 10px 20px rgba(52,152,219,0.4);}}}}

        .result{{{{margin-top: 30px; padding: 25px; border-radius: 15px; font-size: 28px; font-weight: bold; color: white; animation: slideUp 0.5s ease;}}}}
        .real{{{{background: linear-gradient(135deg, #2ecc71, #27ae60);}}}}
        .fake{{{{background: linear-gradient(135deg, #e74c3c, #c0392b);}}}}
        .suspicious{{{{background: linear-gradient(135deg, #f39c12, #d35400);}}}}
        
        .confidence{{{{font-size: 18px; margin-top: 5px; opacity: 0.9;}}}}

        .examples{{{{margin-top: 40px; border-top: 1px solid #eee; padding-top: 20px;}}}}
        .ex-btn{{{{
            padding: 10px 20px; margin: 5px; background: #9b59b6; color: white; 
            border: none; border-radius: 20px; cursor: pointer; transition: 0.3s;
        }}}}
        .ex-btn:hover{{{{background: #8e44ad;}}}}

        @keyframes fadeIn {{{{ from {{{{opacity: 0;}}}} to {{{{opacity: 1;}}}} }}}}
        @keyframes slideUp {{{{ from {{{{transform: translateY(20px); opacity: 0;}}}} to {{{{transform: translateY(0); opacity: 1;}}}} }}}}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Fake News Detector</h1>
        <p class="subtitle">Enter a headline to check its authenticity</p>
        
        <form method="POST">
            <textarea name="news" placeholder="Paste news content here...">{input_text}</textarea>
            <button type="submit" class="analyze-btn">🎯 ANALYZE NOW</button>
        </form>

        {result_html}

        <div class="examples">
            <p style="margin-bottom:10px; font-weight:bold;">Quick Tests:</p>
            <button class="ex-btn" onclick="document.querySelector('textarea').value='NASA confirms aliens are living on the Moon secretely!';">🛸 Fake Example</button>
            <button class="ex-btn" style="background:#27ae60" onclick="document.querySelector('textarea').value='ISRO successfully launched the Gaganyaan mission today.';">🚀 Real Example</button>
        </div>
    </div>
</body>
</html>
    '''
    return html.format(input_text=input_text, result_html=result_html)

if __name__ == "__main__":
    # Port 10000 for Render
    app.run(host="0.0.0.0", port=10000)
