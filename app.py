"""
Deutsch-Kompagnon: German B2 exam prep RAG chatbot.
Streamlit web UI.
"""

import streamlit as st
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# --- Page config ---
st.set_page_config(
    page_title="Deutsch-Kompagnon",
    page_icon="🇩🇪",
    layout="centered",
)

st.title("🇩🇪 Deutsch-Kompagnon")
st.caption("Your friendly German B2 exam prep assistant")

# --- Cache expensive resources so they load only once ---
@st.cache_resource
def load_rag_pipeline():
    import os
    from langchain_community.document_loaders import DirectoryLoader, TextLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    
    # If vector DB doesn't exist yet, build it from documents/
    if not os.path.exists("chroma_db"):
        with st.spinner("First-time setup: building knowledge base..."):
            loader = DirectoryLoader(
                "documents",
                glob="**/*.md",
                loader_cls=TextLoader,
                loader_kwargs={"encoding": "utf-8"},
            )
            docs = loader.load()
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=50,
                separators=["\n\n", "\n", ". ", " ", ""],
            )
            chunks = splitter.split_documents(docs)
            vectordb = Chroma.from_documents(
                documents=chunks,
                embedding=embeddings,
                persist_directory="chroma_db",
                collection_name="german_b2",
            )
    else:
        vectordb = Chroma(
            persist_directory="chroma_db",
            collection_name="german_b2",
            embedding_function=embeddings,
        )
    
    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0.3,
    )
    prompt = ChatPromptTemplate.from_template("""
You are a friendly German B2 exam tutor. Answer the student's question 
using ONLY the context provided below. If the context doesn't contain 
the answer, say so clearly instead of guessing.

Give clear examples in both German and English when helpful.
Keep answers focused and structured.

CONTEXT:
{context}

STUDENT QUESTION:
{question}

YOUR ANSWER:
""")
    return vectordb, llm, prompt

vectordb, llm, prompt = load_rag_pipeline()

# --- RAG function ---
def ask(question: str):
    docs = vectordb.similarity_search(question, k=3)
    context = "\n\n".join([doc.page_content for doc in docs])
    formatted_prompt = prompt.format(context=context, question=question)
    response = llm.invoke(formatted_prompt)
    sources = list(set(doc.metadata.get("source", "unknown") for doc in docs))
    return response.content, sources

# --- Chat history ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and "sources" in msg:
            with st.expander("📚 Sources"):
                for s in msg["sources"]:
                    st.markdown(f"- `{s}`")

# --- Input ---
if user_question := st.chat_input("Ask a German grammar question..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    # Get and show assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer, sources = ask(user_question)
        st.markdown(answer)
        with st.expander("📚 Sources"):
            for s in sources:
                st.markdown(f"- `{s}`")
    
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources,
    })

# --- Sidebar with example questions ---
with st.sidebar:
    st.header("💡 Try asking:")
    examples = [
        "What's the difference between seit and für?",
        "When do I use Akkusativ vs Dativ?",
        "Explain separable verbs with examples",
        "How does Konjunktiv II work?",
        "What's the difference between wenn and als?",
    ]
    for ex in examples:
        st.markdown(f"- {ex}")
    
    st.divider()
    st.caption("Built with LangChain, ChromaDB, and Groq")
    st.caption("Model: openai/gpt-oss-120b")