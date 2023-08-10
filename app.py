from flask import (
    Flask, request, render_template, url_for, redirect, flash, session, jsonify)
from flask.json import JSONEncoder
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from werkzeug.utils import secure_filename
from flask_moment import Moment
from flask_cors import CORS  # CORS 라이브러리 임포트
from datetime import timedelta
from datetime import datetime
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.agents import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType
from langchain.schema import AIMessage, HumanMessage
from dotenv import load_dotenv
from nltk.tokenize import word_tokenize

import nltk
import joblib
import pandas as pd
import openai
import markdown
import os
import json
import re

app = Flask(__name__)

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY
MODEL = 'gpt-3.5-turbo-0613'
TEMPERATURE = 0.0
MAX_TOKENS = 4096  # GPT-3.5의 최대 토큰 길이임(입력, 출력 동일함)

nltk.download('punkt')  # 토크나이저에 필요한 데이터를 다운로드합니다.

# Personalized AI
embeddings = OpenAIEmbeddings(model='text-embedding-ada-002', openai_api_key=OPENAI_API_KEY, max_retries=20)
knowledge_model = ChatOpenAI(temperature=0, model_name=MODEL)

vector_gift = Chroma(persist_directory='wos_gifted_db', embedding_function=embeddings)
qa_gift = ConversationalRetrievalChain.from_llm(knowledge_model, vector_gift.as_retriever(search_kwargs={"k": 3}), return_source_documents=True)

app.config['SESSION_COOKIE_MAX_SIZE'] = 4800  # 세션의 크기에 대한 문제
app.config['SECRET_KEY'] = 'your_secret_key_here'  # 보안을 위한 시크릿 키 설정

print('Initialization complete.')

# Basic function
# 기본 함수: QA Model에서의 질의 응답에 대한 History 관리
def manage_history(lists):    
    tot_size = 0
    if len(lists) >= 1:
        for item in lists:
            tot_size += len(item['content'])

        if tot_size >= 3000:
            lists = lists[2:]
        
        # Human / AI 메시지 형태로 변환
        results = []
        for item in lists:
            if item['type'] == 'human':
                results.append(HumanMessage(content=item['content'], additional_kwargs=item['additional_kwargs'], example=item['example']))
            else:
                results.append(AIMessage(content=item['content'], additional_kwargs=item['additional_kwargs'], example=item['example'])) 
            
        return results
    else:
        return lists
        
# 기본 함수: 응답이 오면 해답 메시지와 출처 메시지를 구분한다.
def questioning(model, lists, query):
    results = manage_history(lists)  # manage_history 함수가 리스트를 반환하도록 수정 필요
    result = model({"question": query, "chat_history": results})
    print(result['answer']) # 응답 출력
    refs = []
    print('Reference:')
    for item in result['source_documents']:
        filename_with_extension = os.path.basename(item.metadata['source'])
        filename = os.path.splitext(filename_with_extension)[0]
        print(filename)
        refs.append(filename)
    
    #lists.append(HumanMessage(content=query, additional_kwargs={}, example=False))
    #lists.append(AIMessage(content=result['answer'], additional_kwargs={'source':refs}, example=False)) 
    
    lists.append({'type':'human', 'content':query, 'additional_kwargs':{}, 'example':False})
    lists.append({'type':'ai', 'content':result['answer'], 'additional_kwargs':{'source':refs}, 'example':False})
            
    return lists


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/giftedbase', methods=['GET', 'POST'])
def giftedbase():
    if request.method == 'GET':
        sel_lang = request.args.get('lang')
        print(sel_lang)

        if (sel_lang is not None):
            session['lang'] = sel_lang
            
        return render_template('giftedbase.html', lang=session.get('lang', ''))
    else:
        message = request.form.get('text')
        print(message)
        chat_history = session.get('gift_history', [])
        print(chat_history)
        chat_history = questioning(qa_gift, chat_history, message)
        answer = chat_history[-1]['content']
        ref = chat_history[-1]['additional_kwargs']['source'] 
        result = answer + '\n\nReference:\n'
        for item in ref:
            result += '\n - '
            result += item
        result = markdown.markdown(result, extensions=['md_in_html'])
        session['gift_history'] = chat_history
        
        return jsonify({'data':result})


@app.route('/review', methods=['GET', 'POST'])
def review():
    if request.method == 'GET':
        sel_lang = request.args.get('lang')
        print(sel_lang)

        if (sel_lang is not None):
            session['lang'] = sel_lang
            
        return render_template('review.html', lang=session.get('lang', ''))
    else:
        message = request.form.get('text')
        message = message.strip()

        tokens = word_tokenize(message)
        print('total tokens:', len(tokens))
        
        if len(tokens) >= 4000:
            print('it has too many tokens.')
            message = ' '.join(tokens[:4000])

        query = '보기:\n'
        query += message
        query += '\n'
        query += '보기의 글을 전체적으로 확인해서 교정하고, 더 나은 글을 쓸 수 있도록 유용한 피드백을 함께 제공해 줘.'
        query += '결과는 다음과 같은 양식에 맞게 출력해 줘.\n'
        query += '[교정]:{결과}\n'
        query += '[피드백]:{결과}'
        
        print(query)
        
        msg = []
        msg.append({"role": "system", "content": "You are a kind and thoughtful assistant for writing."})
        msg.append({"role": "user", "content": query})

        response = openai.ChatCompletion.create(model='gpt-3.5-turbo-16k', messages=msg, temperature=TEMPERATURE)

        answer = response['choices'][0]['message']['content']
        print(answer)
        
        pos1 = answer.find('[교정]:')
        pos2 = answer.find('[피드백]:')
        
        if pos1 < pos2:
            print('upright')
            result = answer[pos1+5:pos2].strip()
            feedback = answer[pos2+6:].strip()
        else:
            print('reverse')
            result = answer[pos1+5:].strip()
            feedback = answer[pos2+6:pos1].strip()
                
        return {'result': result, 'feedback': feedback}


if __name__ == '__main__':
    session['lang'] = 'ko'
    session['gift_history'] = []
    app.run()