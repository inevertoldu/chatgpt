# ChatGPT 및 LLM을 교육 및 연구에 활용하기
ChatGPT 및 여러 LLM을 API를 이용해 활용하는 방법을 안내하는 예제로 구성되어 있습니다.

nlp.yaml: 실습용 가상환경을 그대로 제공하였습니다. (MacOS)<br>
gptai.yaml: 실습용 가상환경을 그대로 제공하였습니다. (Linux)

가상환경을 그대로 동일하게 설치하려면 가상환경 파일을 다운로드한 후, command 화면에서 <b>conda env create -f nlp.yaml</b>라고 명령어를 치면 가능합니다.<br>
(만약 이미 가상환경이 동일한 이름으로 설치되어 있을 경우, 에러가 발생할 수 있으므로 해당 이름의 가상환경을 먼저 삭제 또는 변경한 뒤에 실행하기 바랍니다.)

pdf: 강의용 교안이 올라와 있는 폴더<br>
personal: langchain을 이용한 ChatGPT 검색 폴더<br>
wos_gifted_db: 실습용 Vector DB로, Web of Science에서 검색해 추출한 영재교육 관련 논문 상세서지정보 분석 데이터베이스



<H1>Flask를 이용한 나만의 ChatGPT 기반 서비스 만들기</H1> 

Flask를 이용하기 위해서는 몇 개의 라이브러리를 설치해야 합니다.
가상환경을 활성화한 뒤 다음의 명령어를 실행해야 합니다.

pip install Flask==2.2.3<br>
pip install Flask-WTF<br>
pip install Flask-Moment<br>
pip install python-dotenv<br>

본 레포지토리에는 .env 파일이 없습니다. 메모장이나 텍스트 편집기를 이용해 .env 파일을 만들고 아래의 내용을 추가하도록 합니다.

FLASK_APP=app.py<br>
FLASK_ENV=development<br>
OPENAI_API_KEY=your_api_key
<p></p>
export FLASK_APP=app.py<br>
export FLASK_DEBUG=true<br>


