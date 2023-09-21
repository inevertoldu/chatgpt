# ChatGPT 및 LLM을 교육 및 연구에 활용하기

ChatGPT 및 여러 LLM을 API를 이용해 활용하는 방법을 안내하는 예제로 구성되어 있습니다.<br>
Vector DB와 Langchain, Flask 등을 이용해 웹을 통해 관련 서비스를 제공할 수 있도록 구성되어 있습니다.<br>

pdf: 강의용 교안이 올라와 있는 폴더<br>
personal: langchain을 이용한 개인용 ChatGPT 검색 폴더<br>
wos_gifted_db: 실습용 Vector DB로, Web of Science에서 검색해 추출한 영재교육 관련 논문 상세서지정보 분석 데이터베이스

<H1>먼저 해야 할 일</H1>

코드를 실행하기 위해서는 우선 가상환경을 설치하도록 해야 합니다.

1) https://www.anaconda.com/download 사이트에 접속해서 자신의 OS 및 컴퓨터의 환경에 맞는 Anaconda 프로그램을 다운로드 받아 설치합니다.
2) github에 있는 nlp.yaml을 다운로드 받은 뒤, 다운로드 받은 위치에서 명령어 창을 통해 <b>conda env create -f nlp.yaml</b>을 입력합니다.
3) 터미널 또는 윈도우 명령어 창을 띄운 뒤 <b>conda info --env</b> (다음 명령어는 설치된 가상환경이 무엇이 있는지 확인하기 위한 명령어입니다.)를 입력해 nlp라는 이름의 가상환경이 있는지 확인합니다.
4) 새로운 가상환경을 설치하고 싶다면 <b>conda create -n {이름}</b>과 같이 입력합니다.
5) 가상환경을 활성화하기 위해 <b>conda activate nlp</p>와 같이 입력합니다.정상적으로 동작하는지 확인합니다.
(만약 이미 가상환경이 동일한 이름으로 설치되어 있을 경우, 에러가 발생할 수 있으므로 해당 이름의 가상환경을 먼저 삭제 또는 변경한 뒤에 실행하기 바랍니다.)

본 코드에서는 ChatGPT API를 이용하므로 각자 자신의 API Key를 등록해야 합니다.
<p></p>

<H1>이 프로그램을 이용하기 위해서 해야 할 일</H1>

이 프로그램을 이용하려면 먼저 가상환경 설치가 필요합니다. (가상환경 설치하는 법, 그리고 export된 파일을 불러와 설치하기 추가)<br><br>

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

FLASK_APP=app1.py<br>
FLASK_ENV=development<br>
OPENAI_API_KEY=your_api_key<br>
UPLOAD_FOLDER = './uploads'
<p></p>
export FLASK_APP=app.py<br>
export FLASK_DEBUG=true
<p></p>
app.py을 만들고 나면, 명령어 창에서 flask run이라고 입력하면 수행할 수 있습니다.

<H1>서비스의 기능</H1>

본 소스 코드의 플라스크 서비스는 flask run을 통해 실행한 이후, 엔드포인트(endpoint) 지정을 통해 몇 가지 서비스를 구현할 수 있도록 제공되었습니다.<br>
예를 들면 http://127.0.0.1:5000/query, http://127.0.0.1:5000/review 등을 통해 여러 기능을 수행할 수 있습니다.<br>
(공인된 인증서를 가지고 있지 않으므로 https 실행은 되지 않습니다.)<br><br>

1. 일반적인 질의응답(/query): chatgpt 웹사이트에서 하는 것처럼 여러 질문들을 수행할 수 있습니다.<p>
2. 글쓰기 교정 및 피드백(/review): 작성된 긴 글에 대해 첨삭과 피드백을 제공합니다.<p>
3. 주어진 데이터베이스에 대한 질의응답(/giftbase): 영재교육과 관련해 사전적으로 수집하여 정의된 과학영재교육과 관련된 국제학술논문 및 자료를 기반으로 질의응답하도록 구성되어 있습니다.<p>
4. 나만의 데이터셋에 대한 질의응답(/upload): 내가 정리한 엑셀 또는 데이터셋 파일에 대한 질의응답 기능이 있습니다. 현재는 엑셀 또는 csv 포맷만 가능합니다.<p>


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




