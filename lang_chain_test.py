import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# 중요: 코드를 실행하기 전에 터미널에 OPENAI_API_KEY를 설정해야 합니다.
# 예: export OPENAI_API_KEY="sk-..."

# 0. 샘플 문서와 VectorStore 생성 (기존 코드에서 누락된 부분)
documents = [
    "RAG는 '검색 증강 생성(Retrieval-Augmented Generation)'의 약자입니다.",
    "RAG의 가장 큰 장점은 LLM이 최신 정보나 내부 문서를 기반으로 답변을 생성할 수 있게 하여 환각(Hallucination) 현상을 줄이는 것입니다.",
    "RAG는 먼저 사용자의 질문과 관련된 문서를 외부 데이터베이스에서 검색한 다음, 검색된 문서를 컨텍스트로 활용하여 LLM이 답변을 생성하는 방식으로 동작합니다."
]
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_texts(documents, embedding=embeddings)


# 1. Retriever 설정 (VectorStore 등에서 파생)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})


# 2. 검색된 문서(Document) 리스트를 하나의 문자열로 결합하는 함수
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)



# 3. 프롬프트 템플릿 정의
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "다음의 참고 자료를 바탕으로 질문에 답변해 주세요.\n\n참고 자료:\n{context}",
        ),
        ("user", "{question}"),
])

# 4. LLM 모델 및 출력 파서 설정
llm = ChatOpenAI(model="gpt-4o", temperature=0)
output_parser = StrOutputParser()

# 5. LCEL을 이용한 RAG 체인 조립 (핵심 구조)
rag_chain = (
    # 병렬 실행: 질문은 그대로 넘기고(RunnablePassthrough), 컨텍스트는 retriever로 검색 후 포맷팅
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | output_parser
)

# 6. 체인 실행
response = rag_chain.invoke("RAG 구조의 장점이 뭐야?")
print(response)

""""
확장 패턴 (최신 트렌드)
단순한 Retrieve -> Generate 형태의 정적 RAG를 넘어, 실무에서는 LCEL 체인을 기반으로 다음과 같은 고급 패턴들이 결합됩니다.

Query Rewriting (질의 재작성): 사용자의 모호한 질문을 LL유닛이 검색하기 좋은 형태로 먼저 변환한 뒤 체인에 투입
Reranking (재정렬): 검색된 문서들을 Cross-Encoder 등으로 다시 채점하여 연관성이 높은 문서만 프롬프트에 포함
LangGraph 연동: 단순 선형 파이프라인을 넘어, 답변의 할루시네이션(환각) 여부를 스스로 검증하고 재검색(Loop)하는 Agentic RAG 구조로 확장


"""