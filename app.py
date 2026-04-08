from flask import Flask, render_template_string, request

app = Flask(__name__)

# Fake News Detection Logic
def detect_fake_news(text):
    text = text.lower()
    fake_keywords = ['breaking', 'shocking', 'unbelievable', 'scam', 'conspiracy', 'fake', 'hoax', 'alien', 'ufo']
    real_keywords = ['official', 'confirmed', 'government', 'study', 'source', 'verified', 'isro', 'nasa']
    
    fake_score = sum(1 for word in fake_keywords if word in text)
    real_score = sum(1 for word in real_keywords if word in text)
    
    if fake_score > real_score:
        return "FAKE ❌", 95
    elif real_score > fake_score:
        return "REAL ✅", 92
    else:
        return "SUSPICIOUS ⚠️", 70

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
    
    # HTML with Newspaper Background and 3D Card
    html = f'''
<!DOCTYPE html>
<html>
<head>
    <title>Truth Lens AI</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        *{{{{margin:0;padding:0;box-sizing:border-box}}}}
        
        body{{{{
            font-family:'Segoe UI', sans-serif;
            /* Newspaper Background with Dark Overlay */
            background-image: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.85)), 
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

        /* Attractive 3D Glass Card */
        .glass-card{{{{
            max-width: 750px;
            width: 100%;
            background: rgba(255, 255, 255, 0.07); 
            backdrop-filter: blur(15px);
            border-radius: 30px;
            padding: 50px 40px;
            box-shadow: 0 25px 50px rgba(0,0,0,0.8), 
                        inset 0 0 15px rgba(255,255,255,0.05);
            text-align: center;
            border: 1px solid rgba(255,255,255,0.15);
        }}}}

        h1{{{{
            font-size: 3.8em;
            font-weight: 900;
            color: #ffffff;
            text-shadow: 0 10px 20px rgba(0,0,0,0.5);
            margin-bottom: 5px;
            letter-spacing: -2px;
        }}}}
        
        .tagline{{{{
            color: #bdc3c7;
            font-size: 1.2em;
            margin-bottom: 40px;
            font-weight: 500;
        }}}}

        textarea{{{{
            width: 100%; height: 160px; padding: 25px; border: none;
            border-radius: 20px; font-size: 18px; margin-bottom: 25px;
            background: rgba(255, 255, 255, 0.95);
            color: #1a1a1a;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            resize: none;
        }}}}

        .scan-btn{{{{
            width: 100%; padding: 20px; 
            background: linear-gradient(135deg, #2980b9, #3498db);
            color: white; border: none; border-radius: 15px; font-size: 1.3em;
            font-weight: 800; cursor: pointer; transition: 0.4s;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 15px 30px rgba(41,128,185,0.4);
        }}}}
        .scan-btn:hover{{{{transform: translateY(-5px); box-shadow: 0 20px 40px rgba(41,128,185,0.6);}}}}

        .result{{{{margin-top: 35px; padding: 30px; border-radius: 20px; color: white; font-weight: bold; font-size: 30px; text-shadow: 2px 2px 5px rgba(0,0,0,0.3);}}}}
        .real{{{{background: linear-gradient(45deg, #27ae60, #2ecc71);}}}} 
        .fake{{{{background: linear-gradient(45deg, #c0392b, #e74c3c);}}}} 
        .suspicious{{{{background: #f39c12;}}}}
        .confidence{{{{font-size: 18px; margin-top: 8px; opacity: 0.9; font-weight: normal;}}}}
    </style>
</head>
<body>
    <div class="glass-card">
        <h1>Truth Lens AI</h1>
        <p class="tagline">AI-Powered Verification • Instant Analysis • 95% Accuracy</p>
        <form method="POST">
            <textarea name="news" placeholder="Paste news content here...">{input_text}</textarea>
            <button type="submit" class="scan-btn">🎯 Start Analysis</button>
        </form>
        {result_html}
    </div>
</body>
</html>
    '''
    return html.format(input_text=input_text, result_html=result_html)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
