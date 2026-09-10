# Book Report 웹앱

이 앱은 초등학교 3~4학년용 영어 Book Report 자동첨삭 웹앱입니다.

## 기능
- 1~8번 질문 답변 첨삭
- 현재시제만 사용
- be동사 / 일반동사 / 3인칭 단수 검사
- 단어만 쓴 답변을 완전한 문장으로 변환
- 쉬운 한국어 오류 설명
- 더 좋은 표현 추천
- 인물/장소/내용의 앞뒤 일관성 확인
- 최종 Book Report 생성
- 완성 글 TXT 저장

## Streamlit Community Cloud 배포
1. GitHub 계정을 준비합니다.
2. 이 폴더의 app.py와 requirements.txt를 GitHub 저장소에 올립니다.
3. https://share.streamlit.io/ 에 접속합니다.
4. GitHub로 로그인합니다.
5. Create app을 선택합니다.
6. 저장소와 app.py를 선택하여 배포합니다.
7. Advanced settings -> Secrets에 다음을 입력합니다.

OPENAI_API_KEY = "여기에_본인의_API_KEY"

8. 배포가 끝나면 streamlit.app 주소가 생깁니다.

주의:
- API 키를 GitHub 코드에 직접 넣지 마세요.
- 공개 저장소에 API 키를 올리면 안 됩니다.
- 학생 이름이나 답변을 장기간 저장하는 기능은 현재 포함하지 않았습니다.
