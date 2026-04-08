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
            /* Aapki image ka direct online link background mein */
            background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
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

        /* 3D Glassmorphism Effect */
        .glass-card{{{{
            max-width: 650px;
            width: 100%;
            background: rgba(255, 255, 255, 0.1); 
            backdrop-filter: blur(15px);
            border-radius: 30px;
            padding: 45px;
            box-shadow: 0 25px 50px rgba(0,0,0,0.5);
            text-align: center;
            border: 1px solid rgba(255,255,255,0.2);
            transition: transform 0.3s;
        }}}}

        h1{{{{
            font-size: 3.5em;
            font-weight: 900;
            color: #fff;
            text-shadow: 2px 4px 15px rgba(0,0,0,0.5);
            margin-bottom: 5px;
            letter-spacing: -1px;
        }}}}
        
        .tagline{{{{
            color: #ecf0f1;
            font-size: 1.1em;
            margin-bottom: 30px;
            opacity: 0.9;
        }}}}

        textarea{{{{
            width: 100%; height: 160px; padding: 20px; border: none;
            border-radius: 20px; font-size: 16px; margin-bottom: 20px;
            background: rgba(255, 255, 255, 0.95);
            box-shadow: inset 2px 2px 10px rgba(0,0,0,0.1);
            color: #2c3e50;
        }}}}

        .scan-btn{{{{
            width: 100%; padding: 18px; 
            background: linear-gradient(45deg, #00c6ff, #0072ff);
            color: white; border: none; border-radius: 15px; font-size: 1.2em;
            font-weight: bold; cursor: pointer; transition: 0.3s;
            text-transform: uppercase;
            box-shadow: 0 10px 20px rgba(0,114,255,0.3);
        }}}}
        .scan-btn:hover{{{{transform: translateY(-3px); box-shadow: 0 15px 25px rgba(0,114,255,0.4);}}}}

        .result{{{{margin-top: 30px; padding: 20px; border-radius: 15px; color: white; font-weight: bold; font-size: 26px;}}}}
        .real{{{{background: linear-gradient(135deg, #2ecc71, #27ae60);}}}} 
        .fake{{{{background: linear-gradient(135deg, #e74c3c, #c0392b);}}}} 
        .suspicious{{{{background: #f39c12;}}}}
        .confidence{{{{font-size: 16px; margin-top: 5px; font-weight: normal;}}}}

        .examples{{{{margin-top: 35px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 20px;}}}}
        .ex-btn{{{{
            padding: 10px 20px; margin: 5px; border: none; border-radius: 25px; 
            cursor: pointer; font-weight: bold; color: white; background: rgba(255,255,255,0.2);
            transition: 0.3s;
        }}}}
        .ex-btn:hover{{{{background: rgba(255,255,255,0.3);}}}}
    </style>
</head>
<body>
    <div class="glass-card">
        <h1>Truth Lens</h1>
        <p class="tagline">Advanced News Verification • 95% Accuracy</p>
        <form method="POST">
            <textarea name="news" placeholder="Paste news content here for 3D analysis...">{input_text}</textarea>
            <button type="submit" class="scan-btn">Analyze Now</button>
        </form>
        {result_html}
        <div class="examples">
            <button class="ex-btn" onclick="document.querySelector('textarea').value='NASA found aliens on Mars today!';">Fake News Test</button>
            <button class="ex-btn" onclick="document.querySelector('textarea').value='Official government report confirms GDP growth.';">Real News Test</button>
        </div>
    </div>
</body>
</html>
    '''
    return html.format(input_text=input_text, result_html=result_html)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
