import streamlit as st
import google.generativeai as genai
import PyPDF2
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key="AIzaSyBodSTfywho5SMd0N1RFjcBnq_Q1cGE0Vk")
model = genai.GenerativeModel("gemini-1.5-pro")

def extract_text(file):
    if file.type == "application/pdf":
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    elif file.type == "text/plain":
        return file.read().decode("utf-8")
    else:
        return ""

def ask_gemini(question, context):
    prompt = f"""
You are an intelligent assistant. Use the provided context to answer the user's question. 
If the answer is not in the context, say "Sorry, I couldn't find the answer."

Context:
\"\"\"
{context}
\"\"\"

Question: {question}
"""
   
    chat = model.start_chat()
    
   
    response = chat.send_message(prompt)
    
 
    return response.text.strip()


st.set_page_config(page_title="Gemini FAQ Bot", page_icon="🤖")
st.title("📄 AI-Powered FAQ Bot with Gemini")
st.markdown("Upload a PDF or TXT file, then ask questions about its content.")

uploaded_file = st.file_uploader("Upload Document", type=["pdf", "txt"])

if uploaded_file:
    context = extract_text(uploaded_file)
    st.success("Document uploaded and processed!")

    if context:
        question = st.text_input("Ask a question about the document:")
        if question:
            with st.spinner("Thinking..."):
                answer = ask_gemini(question, context)
                st.markdown("### 🤖 Answer:")
                st.write(answer)
