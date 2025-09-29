from celery import Celery, signals
from agno.agent import Agent
from agno.models.openai import OpenAIChat
import dotenv
from services.waha_service import send_message
from dotenv import load_dotenv
from redisvl.extensions.cache.llm import SemanticCache

load_dotenv()

app = Celery('tasks', broker='pyamqp://guest@rabbitmq//')

agent = None

@signals.worker_process_init.connect
def inicializar_recurso_global(**kwargs):
    global agent

    with open("data/asimov.md", "r") as f:
        asimov_doc = f.read()
        
    with open("data/prompt.xml", "r") as f:
        prompt_doc = f.read()

    global cache
    cache = connect_semmantic_cache()

    agent = Agent(
        model=OpenAIChat(id="gpt-4o-mini"),
        instructions="<fatos>" + "\n" + asimov_doc + "\n" + "</fatos" + "\n" + prompt_doc
    )

@app.task
def task_answer(chat_id, prompt):
    if response := get_semantic_cache_answer(cache=cache, prompt=prompt):
        message = f"(cache) {response}"
    else:
        message = get_ai_answer(prompt)
        if message:
            set_semantic_cache_answer(cache=cache, prompt=prompt, answer=message)
        else:
            message = "Tente novamente mais tarde."

    send_message(chat_id, message)

def get_ai_answer(prompt:str) -> str|None:
    try:
        result = agent.run(input = prompt)
        return result.content
    except Exception as e:
        print(f"Erro ao obter resposta da IA: {e}")
        return None

def connect_semmantic_cache()-> SemanticCache:
    return SemanticCache(
        name="llmcache",
        ttl=360,
        redis_url="redis://redis:6379",
        distance_threshold=0.1
    )

def get_semantic_cache_answer(cache:SemanticCache, prompt:str) -> str|None:
    try:
        cached_response = cache.check(prompt=prompt)
        if len(cached_response) > 0:
            return cached_response[0]['response']
        return None
    except Exception as e:
        print(f"Erro ao obter resposta do cache semântico: {e}")
        return None

def set_semantic_cache_answer(cache:SemanticCache, prompt:str, answer:str) -> None:
    try:
        cache.store(prompt=prompt, response=answer)
    except Exception as e:
        print(f"Erro ao armazenar resposta no cache semântico: {e}")
        return None