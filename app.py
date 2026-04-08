from flask import Flask, render_template_string, request

app = Flask(__name__)

# Basic ML-style logic (Keywords based)
def detect_fake_news(text):
    text = text.lower()
    # In keywords ko aap badha sakte hain
    fake_keywords = ['breaking', 'shocking', 'unbelievable', 'secret', 'hidden', 'scam', 'conspiracy', 'fake', 'hoax']
    real_keywords = ['official', 'report', 'confirmed', 'government', 'study', 'source', 'authorized', 'verified']
    
    fake_score = sum(1 for word in fake_keywords if word in text)
    real_score = sum(1 for word in real_keywords if word in text)
    
    if fake_score > real_score:
        return "FAKE ❌", 85 + (fake_score * 2)
    elif real_score > fake_score:
        return "REAL ✅", 80 + (real_score * 2)
    else:
        return "SUSPICIOUS ⚠️", 65

@app.route('/', methods=['GET', 'POST'])
def home():
    result_html = ""
    input_text = ""
    
    if request.method == 'POST':
        input_text = request.form.get('news', '').strip()
        if input_text:
            res_text, confidence = detect_fake_news(input_text)
            res_class = "real" if "REAL" in res_text else "fake" if "FAKE" in res_text else "suspicious"
            # Result block with styling
            result_html = f"<div class='result {res_class}'>{res_text}<div class='confidence'>Confidence Score: {min(confidence, 99)}%</div></div>"
    
    # Full Layout with Background Image
    html = f'''
<!DOCTYPE html>
<html>
<head>
    <title>AI Fake News Detector</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        *{{{{margin:0; padding:0; box-sizing:border-box;}}}}
        
        body{{{{
            font-family: 'Segoe UI', sans-serif;
            /* Background Image from your request */
            background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                        url('https://i.ibb.co/Xz95mF3/fake-news-disinformation.jpg');
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
            max-width: 650px;
            width: 100%;
            background: rgba(255, 255, 255, 0.98);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.5);
            text-align: center;
        }}}}

        h1{{{{color: #2c3e50; margin-bottom: 10px; font-size: 2.4em;}}}}
        .subtitle{{{{color: #7f8c8d; margin-bottom: 25px;}}}}

        textarea{{{{
            width: 100%; height: 140px; padding: 15px; border: 2px solid #ddd;
            border-radius: 12px; font-size: 16px; margin-bottom: 20px; resize: none;
        }}}}

        .analyze-btn{{{{
            width: 100%; padding: 15px; background: #3498db; color: white;
            border: none; border-radius: 10px; font-size: 18px; font-weight: bold;
            cursor: pointer; transition: 0.3s;
        }}}}
        .analyze-btn:hover{{{{background: #2980b9;}}}}

        .result{{{{margin-top: 25px; padding: 20px; border-radius: 10px; color: white; font-weight: bold; font-size: 22px;}}}}
        .real{{{{background: #27ae60;}}}} .fake{{{{background: #e74c3c;}}}} .suspicious{{{{background: #f39c12;}}}}
        .confidence{{{{font-size: 16px; margin-top: 5px; opacity: 0.9; font-weight: normal;}}}}

        .examples{{{{margin-top: 30px; border-top: 1px solid #eee; padding-top: 20px;}}}}
        .ex-btn{{{{padding: 8px 15px; margin: 5px; border: none; border-radius: 20px; cursor: pointer; color: white; background: #9b59b6;}}}}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Fake News Detector</h1>
        <p class="subtitle">Enter text to check for misinformation</p>
        <form method="POST">
            <textarea name="news" placeholder="Paste your news content here...">{input_text}</textarea>
            <button type="submit" class="analyze-btn">CHECK AUTHENTICITY</button>
        </form>
        {result_html}
        <div class="examples">
            <p style="font-size:14px; margin-bottom:10px;">Try these examples:</p>
            <button class="ex-btn" onclick="document.querySelector('textarea').value='NASA found a hidden secret city on Mars!';">Fake News</button>
            <button class="ex-btn" style="background:#2ecc71" onclick="document.querySelector('textarea').value='Official report shows GDP growth in the last quarter.';">Real News</button>
        </div>
    </div>
</body>
</html>
    '''
    return html.format(input_text=input_text, result_html=result_html)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
