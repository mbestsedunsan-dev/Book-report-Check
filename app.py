import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="Book Report 자동첨삭",
    page_icon="📚",
    layout="wide"
)

QUESTIONS = [
    "What is the story about?",
    "Who are the characters?",
    "Where does the story take place?",
    "What happens at the end?",
    "What is your favorite part? Choose ONE.",
    "Why do you like that part?",
    "What do you think about the main character?",
    "Why do you think so?",
]

SYSTEM_PROMPT = """
You are an English writing teacher for Korean elementary school students in grades 3-4.

Topic: Writing about the book I read.

Correct the student's 8 answers so they become ONE coherent short book report.

RULES
1. Keep the student's original meaning and book facts as much as possible.
2. Use English suitable for Korean elementary grade 3-4 students.
3. PRESENT TENSE ONLY.
4. Check be-verbs: am/is/are.
5. Check ordinary verbs and third-person singular forms.
6. If an answer is only a word or phrase, make it a complete sentence with a subject and verb.
7. Explain grammar mistakes in very easy Korean.
8. If the grammar is correct but the expression can be better, suggest a simple natural expression.
9. Do not make the English unnecessarily difficult.
10. Avoid past tense, present perfect, passive voice, relative clauses, and difficult vocabulary.
11. Keep characters, places, events, and pronouns consistent across all 8 answers.
12. #5 and #6 must clearly connect.
13. #7 and #8 must clearly connect.
14. Do not invent information that the student did not provide.
15. The final report must be simple, natural, and coherent.
16. #4 uses present tense: "What happens at the end?"

Return JSON only in this exact shape:
{
  "answers": [
    {
      "number": 1,
      "student_answer": "...",
      "explanation": "...",
      "corrected_sentence": "...",
      "better_expression": "..."
    }
  ],
  "final_report": "..."
}

Use an empty string when explanation or better_expression is not needed.
"""

def get_client():
    key = st.secrets.get("OPENAI_API_KEY", "")
    if not key:
        key = st.session_state.get("api_key", "")
    if not key:
        return None
    return OpenAI(api_key=key)

def correct_answers(answers):
    client = get_client()
    if client is None:
        raise RuntimeError("OpenAI API 키가 설정되지 않았습니다.")

    prompt = "\n\n".join(
        f"{i+1}. {QUESTIONS[i]}\nStudent answer: {answers[i] or '(no answer)'}"
        for i in range(8)
    )

    response = client.responses.create(
        model="gpt-5.6-luna",
        instructions=SYSTEM_PROMPT,
        input=prompt
    )
    import json
    text = response.output_text.strip()
    if text.startswith("```"):
        text = text.replace("```json", "", 1).replace("```", "", 1).strip()
    return json.loads(text)

st.title("📚 Writing about the book I read")
st.caption("초등학교 3~4학년 영어 Book Report 자동첨삭")

with st.sidebar:
    st.header("⚙️ 설정")
    st.write("처음 사용할 때 OpenAI API 키를 입력하세요.")
    user_key = st.text_input("API 키", type="password", help="API 키는 코드에 공개하지 않고 이 세션에서만 사용합니다.")
    if user_key:
        st.session_state["api_key"] = user_key
    st.info("학원에서 여러 사람이 사용할 경우에는 Streamlit의 Secrets에 API 키를 저장하는 방식을 권장합니다.")

col1, col2 = st.columns([1, 2])
with col1:
    student = st.text_input("학생 이름")
with col2:
    book = st.text_input("책 제목")

st.divider()
st.subheader("① 학생 답변을 입력하세요")

answers = []
for i, q in enumerate(QUESTIONS):
    answers.append(st.text_input(f"{i+1}. {q}", key=f"answer_{i}"))

if st.button("✨ 자동첨삭하기", type="primary", use_container_width=True):
    if not any(a.strip() for a in answers):
        st.warning("학생 답변을 하나 이상 입력해 주세요.")
    elif get_client() is None:
        st.error("왼쪽 'API 키' 칸에 OpenAI API 키를 입력하거나, 배포 후 Secrets에 API 키를 설정해 주세요.")
    else:
        with st.spinner("학생의 답변을 첨삭하고 있습니다..."):
            try:
                data = correct_answers(answers)
                st.session_state["result"] = data
            except Exception as e:
                st.error(f"첨삭 중 오류가 발생했습니다: {e}")

result = st.session_state.get("result")
if result:
    st.divider()
    st.subheader("② 첨삭 결과")

    for item in result.get("answers", []):
        st.markdown(f"### {item.get('number')}.")
        st.markdown(f"**학생 답변**  \n{item.get('student_answer','')}")
        if item.get("explanation"):
            st.info(f"**왜 고칠까요?**\n\n{item['explanation']}")
        st.success(f"**첨삭한 문장**\n\n{item.get('corrected_sentence','')}")
        if item.get("better_expression"):
            st.markdown(f"**더 좋은 표현**  \n{item['better_expression']}")

    st.divider()
    st.subheader("③ 최종 Book Report")

    final_report = result.get("final_report", "")
    st.text_area(
        "완성된 글",
        value=final_report,
        height=220,
        label_visibility="collapsed"
    )

    st.download_button(
        "📄 최종 글 저장하기",
        data=final_report,
        file_name=f"{student or 'student'}_Book_Report.txt",
        mime="text/plain",
        use_container_width=True
    )
