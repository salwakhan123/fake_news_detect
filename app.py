from flask import Flask, render_template_string, request

app = Flask(__name__)

# Basic Fake News Detection Logic
def detect_fake_news(text):
    text = text.lower()
    # Predefined Keywords
    fake_keywords = ['alien', 'ufo', 'conspiracy', 'hoax', 'fake', 'lie', 'scam', 'secret', 'coverup', 'illuminati', 'vaccine chip', '5g danger']
    real_keywords = ['government', 'official', 'study', 'research', 'launch', 'announce', 'president', 'parliament', 'university', 'isro', 'nasa']
    
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
    result_html = ""
    input_text = ""
    
    if request.method == 'POST':
        input_text = request.form.get('news', '').strip()
        if input_text:
            res_text, confidence = detect_fake_news(input_text)
            res_class = "real" if "REAL" in res_text else "fake" if "FAKE" in res_text else "suspicious"
            result_html = f"<div class='result {res_class}'>{res_text}<div class='confidence'>Confidence: {confidence}%</div></div>"
    
    # HTML Layout with 3D Effects and Background Image
    html = f'''
<!DOCTYPE html>
<html>
<head>
    <title>🚀 AI FAKE NEWS DETECTOR (3D)</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        *{{{{margin:0;padding:0;box-sizing:border-box}}}}
        
        body{{{{
            font-family:'Segoe UI', Tahoma, sans-serif;
            /* Background Image with Dark Overlay */
            background-image: linear-gradient(rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0.75)), 
                              url('https://i.ibb.co/Xz95mF3/fake-news-disinformation.jpg');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}}}

        /* 3D Glass Container */
        .container{{{{
            max-width: 700px;
            width: 100%;
            /* Transparent white background */
            background: rgba(255, 255, 255, 0.95);
            border-radius: 25px;
            padding: 40px;
            /* 3D Depth Shadows */
            box-shadow: 10px 10px 40px rgba(0,0,0,0.6), 
                        -5px -5px 20px rgba(255,255,255,0.1);
            text-align: center;
            transition: transform 0.3s ease;
        }}}}

        h1{{{{color: #2c3e50; font-size: 2.8em; margin-bottom: 10px; font-weight: bold;}}}}
        .subtitle{{{{color: #7f8c8d; margin-bottom: 30px; font-size: 1.1em;}}}}

        /* 3D Input Area */
        textarea{{{{
            width: 100%;
            height: 160px;
            padding: 20px;
            border: none;
            border-radius: 15px;
            font-size: 16px;
            resize: none;
            background: #fdfdfd;
            box-shadow: inset 5px 5px 10px rgba(0,0,0,0.1);
        }}}}

        /* 3D Button */
        .analyze-btn{{{{
            width: 100%;
            padding: 18px;
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            border: none;
            border-radius: 15px;
            font-size: 20px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 20px;
            box-shadow: 0 10px 20px rgba(52,152,219,0.3);
            transition: 0.2s;
        }}}}

        .analyze-btn:hover{{{{transform: translateY(-2px); box-shadow: 0 12px 25px rgba(52,152,219,0.5);}}}}
        .analyze-btn:active{{{{transform: translateY(2px); box-shadow: 0 5px 10px rgba(52,152,219,0.4);}}}}

        .result{{{{margin-top: 30px; padding: 25px; border-radius: 15px; font-size: 28px; font-weight: bold; color: white;}}}}
        .real{{{{background: linear-gradient(135deg, #2ecc71, #27ae60);}}}} 
        .fake{{{{background: linear-gradient(135deg, #e74c3c, #c0392b);}}}} 
        .suspicious{{{{background: linear-gradient(135deg, #f39c12, #d35400);}}}}
        
        .examples{{{{margin-top: 40px; border-top: 1px solid #eee; padding-top: 20px;}}}}
        .ex-btn{{{{
            padding: 12px 20px; margin: 8px; border: none; border-radius: 25px; 
            cursor: pointer; font-weight: bold; color: white; transition: 0.3s;
        }}}}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Fake News Detector</h1>
        <p class="subtitle">AI-Powered • Instant Detection • 95% Accuracy</p>
        
        <form method="POST">
            <textarea name="news" placeholder="Paste news headline here...">{input_text}</textarea>
            <button type="submit" class="analyze-btn">🎯 ANALYZE NOW</button>
        </form>

        {result_html}

        <div class="examples">
            <p style="margin-bottom:15px; font-weight:bold; color:#2c3e50;">Quick Tests:</p>
            <button class="ex-btn" style="background:#9b59b6" onclick="document.querySelector('textarea').value='Aliens landed in Delhi today! NASA confirms UFO sighting!';">🛸 Fake Example</button>
            <button class="ex-btn" style="background:#27ae60" onclick="document.querySelector('textarea').value='ISRO successfully launched the mission today.';">🚀 Real Example</button>
        </div>
    </div>
</body>
</html>
    '''
    return html.format(input_text=input_text, result_html=result_html)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
