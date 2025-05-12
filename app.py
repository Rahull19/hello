from flask import Flask, render_template, request, session
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from mistral_llm import MistralLLM
import os

app = Flask(__name__)
app.secret_key = 'secret'

os.environ["MISTRAL_API_KEY"] = "iPP0giabrl74xjEYZJHxvaTLAb3FlyuQ"
llm = MistralLLM()

prompt = PromptTemplate(
    input_variables=["question"],
    template="""You are a highly intelligent and helpful assistant. You must always provide answers that are:
        Accurate and based on the latest facts you have access to.
        Clear, natural, and written in fluent human-like language.
        Kind, respectful, and easy to understand, regardless of how the question is phrased.
        Error-tolerant, meaning even if the user’s question contains grammatical mistakes, typos, or poor phrasing, you must infer their intent and still provide a high-quality response.
        Structured, where necessary, using bullet points, short paragraphs, or headings for better readability.
        Always act as if you’re speaking directly to a person who genuinely needs your help, and strive to sound empathetic and human.
        Now, answer the following question in the best possible way:\n\n{question}"""
)
chain = LLMChain(llm=llm, prompt=prompt)

@app.route("/", methods=["GET", "POST"])
def index():
    if "history" not in session:
        session["history"] = []

    result = ""
    if request.method == "POST":
        query = request.form.get("query")
        if query:
            result = chain.run(query)
            session["history"].append((query, result))
            session.modified = True

    return render_template("index.html", history=session["history"], result=result, latest_query=query if request.method == "POST" else "")

if __name__ == "__main__":
    app.run(debug=True)