from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
# import openai
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI

user="root"
password="mysqlbv22"
host="localhost"
name="learning"

db=SQLDatabase.from_uri(f"mysql+pymysql://{user}:{password}@{host}/{name}")

llm=OpenAI(temperature=0,openai_api_key="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")
toolkit=SQLDatabaseToolkit(db=db,llm=llm)

agent=create_sql_agent(llm=llm,toolkit=toolkit,verbose=False)

def create_response(query):
    response= agent.run(query)
    return response

def index(request):
    if request.method=='POST':
        message=request.POST.get('message')
        response=create_response(message)
        # response="Lorem ipsum dolor sit amet consectetur adipisicing elit. Reprehenderit placeat, animi facilis iusto harum quia quasi! Magni, repellat at consequuntur architecto quia corporis illum earum? Accusantium ex repellendus delectus provident!"
        return JsonResponse({'message':message,'response':response})
    return render(request,"index.html")