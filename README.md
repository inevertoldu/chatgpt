# ChatGPT 및 LLM을 교육 및 연구에 활용하기
ChatGPT 및 여러 LLM을 API를 이용해 활용하는 방법을 안내하는 예제로 구성되어 있습니다.

nlp.yaml: 실습용 가상환경을 그대로 제공하였습니다. (MacOS)<br>
gptai.yaml: 실습용 가상환경을 그대로 제공하였습니다. (Linux)

가상환경을 그대로 동일하게 설치하려면 가상환경 파일을 다운로드한 후, command 화면에서 <b>conda env create -f nlp.yaml</b>라고 명령어를 치면 가능합니다.<br>
(만약 이미 가상환경이 동일한 이름으로 설치되어 있을 경우, 에러가 발생할 수 있으므로 해당 이름의 가상환경을 먼저 삭제 또는 변경한 뒤에 실행하기 바랍니다.)

pdf: 강의용 교안이 올라와 있는 폴더<br>
personal: langchain을 이용한 ChatGPT 검색 폴더<br>
wos_gifted_db: 실습용 Vector DB로, Web of Science에서 검색해 추출한 영재교육 관련 논문 상세서지정보 분석 데이터베이스
<p></p>

<H1>Flask를 이용한 나만의 ChatGPT 기반 서비스 만들기</H1> 

Flask를 이용하기 위해서는 몇 개의 라이브러리를 설치해야 합니다.
가상환경을 활성화한 뒤 다음의 명령어를 실행해야 합니다.

pip install Flask==2.2.3<br>
pip install Flask-WTF<br>
pip install Flask-Moment<br>
pip install flask-cors<br>
pip install python-dotenv<br>

<H1>Flask의 구조</H1>

플라스크는 python을 이용해 웹 서비스를 할 수 있도록 개발된 패키지입니다.<br>
서버 역할을 수행하는 파일(app.py)과 실제 사용자에게 나타날 여러 파일들의 구조를 띠고 있습니다.
<p></p>
<b>[Project Folder]</b><br>
\- app.py<br>
\- .env<br>
\- <b>[templates]</b><br>
\- <b>[static]</b><br>
<p>templates 폴더는 HTML이 위치하고 있고, static에는 각종 이미지나 스타일, 자바스크립트 등의 정보를 갖고 있습니다.</p>

본 레포지토리에는 .env 파일이 없습니다. 메모장이나 텍스트 편집기를 이용해 .env 파일을 만들고 아래의 내용을 추가하도록 합니다.

FLASK_APP=app.py<br>
FLASK_ENV=development<br>
OPENAI_API_KEY=your_api_key
<p></p>
export FLASK_APP=app.py<br>
export FLASK_DEBUG=true
<p></p>
app.py을 만들고 나면, 명령어 창에서 flask run이라고 입력하면 수행할 수 있습니다.

<H1>최종적으로 배포하기</H1>

서비스를 배포하기 위해서는 방화벽이나 보안 등 여러 가지를 필요로 합니다.<br>
일반적으로는 다음과 같은 방법을 통해 간단하게 켜져 있는 동안 항상 사용할 수 있도록(백그라운드 실행) 할 수 있습니다.<br>
파일이 있는 위치로 이동한 뒤...<br>
<p></p>
pip install gunicorn<br>
nohup gunicorn -b 127.0.0.1:5000 app:app &<br>
(만약 자신이 사용하는 Flask 파일이 app1이라면 app:app 부분을 app1:app1 으로 수정해야 합니다.)<br>
특정 포트에 열려 있는 프로그램을 확인하려면 명령어 창에서 ps aux | grep 5000 을 입력하세요.<br>
그리고 사용을 중지하고 싶다면 위의 명령어를 실행해서 프로세스 숫자를 확인하고 kill [number]를 입력하세요.




