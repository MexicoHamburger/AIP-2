from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>AIP-2 Backend</h1>
    <p>Team2의 백엔드 서버입니다.</p>
    <a href="http://localhost:5173/">NextDev 홈페이지 바로가기</a>
    '''

if __name__ == '__main__':
    app.run(debug=True)