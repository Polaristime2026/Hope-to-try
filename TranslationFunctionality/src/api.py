from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/translate', methods=['POST'])
def translate():
    if request.content_type != 'application/json':
        return jsonify({'error': 'Unsupported Media Type'}), 415
    
    data = request.json  # 确保解析 JSON
    txt = data.get('text', '')
    
    if not txt:
        return jsonify({'braille': ''})
    
    from ChineseToBraille import se_is_ts
    rtxt = se_is_ts(txt)
    
    return jsonify({'braille': rtxt})
