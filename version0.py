# download in terminal
# python3 -m pip install streamlit matplotlib reportlab pandas

import math
import json
import tempfile
from datetime import datetime
from pathlib import Path

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


# =========================
# 0) App Config
# =========================
st.set_page_config(page_title="🌸 나의 강점 테스트", page_icon="🌈", layout="centered")

LOCAL_SAVE_PATH = Path.home() / ".strength_test_progress.json"


# =========================
# 1) Strength Model (24)
#    - 문구/문항은 '자체 제작' (귀여운 톤)
# =========================
STRENGTHS = [
    # 🧠 생각의 힘 (5)
    dict(key="creativity", name="창의성", emoji="🎨", group="🧠 생각의 힘",
         short="아이디어 요정! 새 길을 잘 찾아요.",
         long="익숙한 길을 살짝 비틀어 더 재밌고 더 좋은 답을 만드는 힘이에요.",
         missions=["아이디어 10개 적고 1개만 실행", "오늘 일 하나를 ‘다른 방식’으로 하기", "좋아하는 것 2개를 합친 새 조합 만들기", "새 도구/앱 하나 써보기", "‘만약에…’ 질문 3개 던져보기"]),
    dict(key="curiosity", name="호기심", emoji="🔎", group="🧠 생각의 힘",
         short="왜?를 귀엽게 파고드는 탐험가!",
         long="모르는 걸 그냥 넘기지 않고 질문하며 배우는 힘이에요.",
         missions=["오늘 궁금한 것 1개 찾아보기", "새 주제 10분만 맛보기", "‘왜?’를 3번 연속 물어보기", "새로운 장소/카테고리 클릭해보기", "모르는 단어 3개 정리하기"]),
    dict(key="judgment", name="판단력", emoji="🧠", group="🧠 생각의 힘",
         short="한 번 더 생각하는 똑똑이!",
         long="감정/정보/근거를 균형 있게 보고 결정하는 힘이에요.",
         missions=["결정 전에 장단점 3줄 쓰기", "반대 의견 1개도 적어보기", "팩트/추측 구분해보기", "중요한 결정은 10분 뒤에 하기", "‘내가 놓친 정보는?’ 질문하기"]),
    dict(key="love_of_learning", name="학습열", emoji="📚", group="🧠 생각의 힘",
         short="배우는 맛을 아는 지식 수집가!",
         long="지식을 즐기며 꾸준히 성장하는 힘이에요.",
         missions=["10분 미니학습(영상/글)", "배운 걸 한 문장으로 요약", "메모 3줄 남기기", "배운 걸 누군가에게 설명해보기", "‘오늘의 한 개념’ 정하기"]),
    dict(key="perspective", name="통찰", emoji="🌅", group="🧠 생각의 힘",
         short="큰 그림을 보는 맑은 눈!",
         long="경험과 지식을 엮어 의미 있는 관점을 만드는 힘이에요.",
         missions=["오늘 일의 ‘의미’ 한 줄 쓰기", "실수에서 교훈 1개 뽑기", "다른 관점 2개 상상하기", "내 조언을 친구에게 해준다면?", "한 걸음 물러서서 보기"]),


    # ❤️ 마음의 용기 (4)
    dict(key="bravery", name="용기", emoji="🦁", group="❤️ 마음의 용기",
         short="무서워도 한 발 내딛는 사자!",
         long="불확실해도 필요한 행동을 선택하는 힘이에요.",
         missions=["작은 어려운 일 1개 먼저 하기", "불편하지만 필요한 말 한 문장 연습", "‘괜찮아’ 숨 3번", "도전 목표를 아주 작게 쪼개기", "시작 버튼만 누르기"]),
    dict(key="perseverance", name="끈기", emoji="🏃", group="❤️ 마음의 용기",
         short="끝까지 해내는 꾸준이!",
         long="포기하고 싶어도 한 번 더 시도하는 힘이에요.",
         missions=["25분 집중 1세트", "중간 목표 체크 1개", "오늘 ‘딱 여기까지만’ 정하기", "멈춰도 다시 시작하기", "작은 완료를 칭찬하기"]),
    dict(key="honesty", name="정직", emoji="🤍", group="❤️ 마음의 용기",
         short="내 마음을 솔직하게 말하는 반짝이!",
         long="진짜 생각과 행동을 일치시키는 힘이에요.",
         missions=["내 감정 1단어로 말하기", "약속 1개 정확히 지키기", "과장 대신 사실로 말하기", "‘내가 원하는 것’ 적기", "솔직한 피드백 1개 주기"]),
    dict(key="zest", name="열정", emoji="🔥", group="❤️ 마음의 용기",
         short="에너지 뿜뿜! 생활의 불꽃!",
         long="활기와 생동감을 가지고 삶에 참여하는 힘이에요.",
         missions=["스트레칭 2분", "좋아하는 노래 1곡", "짧은 산책", "오늘 기대되는 것 1개 적기", "웃긴 영상 30초"]),


    # 🤝 사람의 온기 (3)
    dict(key="love", name="사랑", emoji="💕", group="🤝 사람의 온기",
         short="연결을 소중히 하는 따뜻이!",
         long="가까운 관계에서 애정과 돌봄을 주고받는 힘이에요.",
         missions=["고마운 사람에게 한 문장", "포옹/스킨십(가능하면)", "함께 할 약속 잡기", "칭찬 1개 진심으로", "관계에 시간 10분 투자"]),
    dict(key="kindness", name="친절", emoji="🌷", group="🤝 사람의 온기",
         short="작은 배려로 세상을 부드럽게!",
         long="대가 없이 도움을 주고 친절을 실천하는 힘이에요.",
         missions=["문 열어주기/자리 양보", "친절한 댓글/메시지", "누군가 돕기 1회", "작은 선물/간식", "내게도 친절 1회"]),
    dict(key="social_intelligence", name="사회지능", emoji="🧩", group="🤝 사람의 온기",
         short="분위기 읽기 장인! 공감 퍼즐러!",
         long="상대의 감정/상황을 잘 파악하고 관계를 조율하는 힘이에요.",
         missions=["상대 표정/톤 관찰 1번", "질문으로 공감하기", "‘지금 어떤 기분이야?’ 물어보기", "대화에서 70% 듣기", "갈등을 부드럽게 정리하기"]),


    # ⚖️ 함께의 공정 (3)
    dict(key="teamwork", name="팀워크", emoji="🤝", group="⚖️ 함께의 공정",
         short="함께하면 더 강해지는 협동이!",
         long="공동 목표를 위해 역할을 나누고 함께 움직이는 힘이에요.",
         missions=["역할/기대치 한 번 맞추기", "도움 요청/제안 1번", "작은 업데이트 공유", "칭찬으로 팀 분위기 올리기", "약속 시간 지키기"]),
    dict(key="fairness", name="공정함", emoji="⚖️", group="⚖️ 함께의 공정",
         short="편견 없이 똑바로 보는 저울!",
         long="사람을 균형 있게 대하고 원칙을 지키는 힘이에요.",
         missions=["판단 전 ‘근거’ 확인", "다른 입장도 한 줄", "공평한 기준 정하기", "약자 배려 1번", "편견 깨기 질문하기"]),
    dict(key="leadership", name="리더십", emoji="👑", group="⚖️ 함께의 공정",
         short="방향을 잡아주는 든든 대장!",
         long="목표를 제시하고 사람을 북돋아 팀을 움직이게 하는 힘이에요.",
         missions=["오늘 목표를 한 문장으로 공유", "우선순위 3개 정리", "누군가를 칭찬으로 이끌기", "결정 내리고 책임지기", "회의/대화 한 번 정리하기"]),


    # 🛡️ 균형의 지혜 (4)
    dict(key="forgiveness", name="용서", emoji="🍃", group="🛡️ 균형의 지혜",
         short="마음의 짐을 내려놓는 바람!",
         long="상처를 붙잡기보다 앞으로 나아가게 하는 힘이에요.",
         missions=["서운함을 글로 5줄 적기", "상대의 의도/상황 추측 1개", "‘나도 완벽하진 않아’ 떠올리기", "작은 화해 시도", "내 마음부터 달래기"]),
    dict(key="humility", name="겸손", emoji="🌼", group="🛡️ 균형의 지혜",
         short="조용히 빛나는 꽃 같은 자신감!",
         long="내 장점은 인정하되 과장하지 않고 배우려는 태도예요.",
         missions=["칭찬 받으면 ‘고마워’로 받기", "모르는 건 모른다고 말하기", "배울 점 1개 찾기", "공을 나누기", "자기 PR 대신 결과로 보여주기"]),
    dict(key="prudence", name="신중함", emoji="🐢", group="🛡️ 균형의 지혜",
         short="천천히 가도 안전하게 가는 거북이!",
         long="충동을 줄이고 위험을 관리하며 계획하는 힘이에요.",
         missions=["구매/결정 10분 미루기", "체크리스트 5개 만들기", "리스크 1개 대비", "일정/준비물 확인", "‘이 선택의 내일은?’ 생각하기"]),
    dict(key="self_regulation", name="자기조절", emoji="🧘", group="🛡️ 균형의 지혜",
         short="나를 잘 다루는 마음의 조종사!",
         long="습관/감정/시간을 조절해 목표에 맞게 움직이는 힘이에요.",
         missions=["물 한 컵 + 숨 3번", "방해 요소 1개 치우기", "타이머 15분", "간식/폰 사용 규칙 정하기", "잠들기 전 10분 정리"]),


    # 🌱 의미의 햇살 (5)
    dict(key="appreciation", name="아름다움감상", emoji="🌸", group="🌱 의미의 햇살",
         short="작은 아름다움도 놓치지 않는 감상러!",
         long="자연/예술/일상의 아름다움을 느끼며 마음을 회복하는 힘이에요.",
         missions=["하늘/나무 30초 보기", "사진 한 장 찍기", "좋아하는 음악 1곡 감상", "예쁜 것 3개 찾기", "방 한 구석 정리"]),
    dict(key="gratitude", name="감사", emoji="🙏", group="🌱 의미의 햇살",
         short="고마움을 잘 챙기는 반짝 마음!",
         long="받은 도움과 좋은 것들을 알아차리고 표현하는 힘이에요.",
         missions=["감사 3가지 적기", "고마운 사람에게 메시지", "오늘 운 좋았던 순간 찾기", "감사한 물건 1개 떠올리기", "‘덕분에’로 말하기"]),
    dict(key="hope", name="희망", emoji="🌈", group="🌱 의미의 햇살",
         short="미래를 밝게 보는 무지개!",
         long="더 나아질 수 있다는 믿음으로 계획하고 움직이는 힘이에요.",
         missions=["내일 할 작은 좋은 일 정하기", "목표를 한 단계 낮춰서 시작", "성공 장면 10초 상상", "응원 문장 하나 써두기", "가능한 다음 कदम 찾기"]),
    dict(key="humor", name="유머", emoji="😆", group="🌱 의미의 햇살",
         short="웃음으로 분위기를 살리는 개그감!",
         long="긴장을 풀고 관계를 부드럽게 하는 힘이에요.",
         missions=["웃긴 밈/영상 공유", "농담 한 번 해보기", "실수도 가볍게 인정", "재밌는 표현 하나 저장", "웃음 포인트 기록"]),
    dict(key="spirituality", name="가치/영성", emoji="✨", group="🌱 의미의 햇살",
         short="내 삶의 방향을 지켜주는 별빛!",
         long="내가 소중히 여기는 가치와 의미를 기준으로 선택하는 힘이에요.",
         missions=["내 가치 1개 적기", "오늘 선택을 가치에 맞추기", "짧은 명상/기도 2분", "‘왜 이걸 하지?’ 답하기", "감정 대신 방향으로 결정"]),
]

KEY_TO_STRENGTH = {s["key"]: s for s in STRENGTHS}


# =========================
# 2) Questions (72 = 24*3)
#    - 각 강점 3문항 (1개는 역문항)
# =========================
def build_questions():
    qs = []
    qid = 1
    for s in STRENGTHS:
        k = s["key"]
        n = s["name"]
        # 문항 3개: 긍정 2 + 역문항 1
        qs.append(dict(id=f"q{qid}", strength=k, reverse=False,
                       text=f"나는 {n}이(가) 필요한 상황에서 자연스럽게 그 힘을 꺼내 쓴다.")); qid += 1
        qs.append(dict(id=f"q{qid}", strength=k, reverse=False,
                       text=f"나는 {n}이(가) 발휘될 때, 스스로 ‘나 괜찮은데?’라고 느낀다.")); qid += 1
        qs.append(dict(id=f"q{qid}", strength=k, reverse=True,
                       text=f"솔직히 {n}이(가) 필요한 상황이면 피하고 싶을 때가 많다.")); qid += 1
    return qs

QUESTIONS = build_questions()


# =========================
# 3) Helpers: local save/load
# =========================
def local_save(state: dict):
    try:
        LOCAL_SAVE_PATH.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass

def local_load():
    try:
        if LOCAL_SAVE_PATH.exists():
            return json.loads(LOCAL_SAVE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return None
    return None

def local_clear():
    try:
        if LOCAL_SAVE_PATH.exists():
            LOCAL_SAVE_PATH.unlink()
    except Exception:
        pass


# =========================
# 4) Scoring
# =========================
def compute_scores(answers: dict):
    buckets = {s["key"]: [] for s in STRENGTHS}
    for q in QUESTIONS:
        v = answers.get(q["id"])
        if v is None:
            continue
        score = (6 - v) if q["reverse"] else v
        buckets[q["strength"]].append(score)

    rows = []
    for s in STRENGTHS:
        arr = buckets[s["key"]]
        avg = sum(arr) / len(arr) if arr else 0.0
        pct = round(((avg - 1) / 4) * 100) if arr else 0
        rows.append(dict(
            key=s["key"],
            name=s["name"],
            emoji=s["emoji"],
            group=s["group"],
            avg=avg,
            pct=pct
        ))

    df = pd.DataFrame(rows).sort_values(["avg", "name"], ascending=[False, True]).reset_index(drop=True)
    top5 = df.head(5).to_dict("records")
    return df, top5


# =========================
# 5) Radar Chart (matplotlib)
# =========================
def plot_radar(df_scores: pd.DataFrame, title="24개 강점 레이더"):
    labels = df_scores["name"].tolist()
    values = df_scores["pct"].tolist()

    N = len(labels)
    angles = [n / float(N) * 2 * math.pi for n in range(N)]
    angles += angles[:1]
    values_loop = values + values[:1]

    fig = plt.figure(figsize=(7, 7))
    ax = plt.subplot(111, polar=True)

    ax.set_theta_offset(math.pi / 2)
    ax.set_theta_direction(-1)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=8)

    ax.set_rlabel_position(0)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(["20", "40", "60", "80", "100"], fontsize=8)
    ax.set_ylim(0, 100)

    ax.plot(angles, values_loop, linewidth=2)
    ax.fill(angles, values_loop, alpha=0.15)
    ax.set_title(title, pad=20)
    return fig


# =========================
# 6) PDF Report (reportlab)
#    - 한글 폰트는 OS별 차이가 커서 "가능하면 자동등록" 시도
#    - 폰트 못 찾으면 기본 폰트로 생성 (한글이 깨질 수 있음)
# =========================
def register_korean_font():
    # 사용자가 가진 폰트 경로 후보들 (Windows/Mac/Linux 흔한 경로)
    candidates = [
        # Windows
        r"C:\Windows\Fonts\malgun.ttf",
        r"C:\Windows\Fonts\malgunbd.ttf",
        # macOS
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        "/Library/Fonts/AppleGothic.ttf",
        # Linux (일반)
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf",
    ]
    for p in candidates:
        try:
            if Path(p).exists():
                pdfmetrics.registerFont(TTFont("KFONT", p))
                return "KFONT"
        except Exception:
            continue
    return None

def make_pdf(df_scores: pd.DataFrame, top5: list, radar_png_path: str, username: str = "") -> bytes:
    font_name = register_korean_font()

    buf_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
    c = canvas.Canvas(buf_path, pagesize=A4)
    W, H = A4

    def set_font(size=12):
        if font_name:
            c.setFont(font_name, size)
        else:
            c.setFont("Helvetica", size)

    margin = 2 * cm
    y = H - margin

    set_font(18)
    title = "🌸 나의 강점 테스트 리포트"
    c.drawString(margin, y, title)
    y -= 1.2 * cm

    set_font(11)
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    name_line = f"이름: {username}" if username else "이름: (미입력)"
    c.drawString(margin, y, name_line)
    y -= 0.6 * cm
    c.drawString(margin, y, f"생성 시각: {stamp}")
    y -= 1.0 * cm

    set_font(14)
    c.drawString(margin, y, "🏆 Top 5 강점")
    y -= 0.7 * cm

    set_font(11)
    for i, r in enumerate(top5, start=1):
        s = KEY_TO_STRENGTH[r["key"]]
        line = f"{i}. {s['emoji']} {s['name']}  ({int(r['pct'])}점)  -  {s['short']}"
        c.drawString(margin, y, line[:110])
        y -= 0.55 * cm
        if y < 7 * cm:
            c.showPage()
            y = H - margin
            set_font(11)

    y -= 0.3 * cm
    set_font(14)
    c.drawString(margin, y, "📈 24개 강점 레이더")
    y -= 0.6 * cm

    # 레이더 이미지 삽입
    try:
        img_w = 16 * cm
        img_h = 16 * cm
        c.drawImage(radar_png_path, margin, y - img_h, width=img_w, height=img_h, preserveAspectRatio=True, mask="auto")
        y -= (img_h + 0.8 * cm)
    except Exception:
        set_font(11)
        c.drawString(margin, y, "(레이더 이미지를 삽입하지 못했어요.)")
        y -= 0.7 * cm

    if y < 8 * cm:
        c.showPage()
        y = H - margin

    set_font(14)
    c.drawString(margin, y, "🧾 전체 점수")
    y -= 0.7 * cm

    set_font(10)
    # 표 형태로 간단 출력 (3열)
    rows = df_scores.sort_values("pct", ascending=False).to_dict("records")
    col_x = [margin, margin + 7*cm, margin + 13*cm]
    col_w = 6.5 * cm
    for idx, r in enumerate(rows):
        s = KEY_TO_STRENGTH[r["key"]]
        col = idx % 3
        if idx > 0 and col == 0:
            y -= 0.55 * cm
            if y < 2.5 * cm:
                c.showPage()
                y = H - margin
                set_font(10)
        text = f"{s['emoji']} {s['name']}: {int(r['pct'])}"
        c.drawString(col_x[col], y, text[:40])

    c.showPage()
    c.save()

    pdf_bytes = Path(buf_path).read_bytes()
    try:
        Path(buf_path).unlink()
    except Exception:
        pass
    return pdf_bytes


# =========================
# 7) UI / Flow
# =========================
if "idx" not in st.session_state:
    st.session_state.idx = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "username" not in st.session_state:
    st.session_state.username = ""

# 상단 헤더
st.title("🌸 나의 강점 테스트")
st.caption("24개 강점 · 72문항 · 귀여운 결과 카드 · 레이더 차트 · PDF 저장")

with st.expander("⚙️ 설정 / 저장", expanded=False):
    st.session_state.username = st.text_input("이름(선택)", value=st.session_state.username, placeholder="예: 보현")
    colA, colB, colC = st.columns(3)

    if colA.button("💾 진행상황 로컬 불러오기"):
        loaded = local_load()
        if loaded:
            st.session_state.idx = loaded.get("idx", 0)
            st.session_state.answers = loaded.get("answers", {})
            st.session_state.username = loaded.get("username", st.session_state.username)
            st.success("불러왔어! 이어서 해보자 🌿")
        else:
            st.info("저장된 진행상황이 없어!")

    if colB.button("📌 지금 상태 로컬 저장"):
        local_save({"idx": st.session_state.idx, "answers": st.session_state.answers, "username": st.session_state.username})
        st.success("저장 완료! 🎀")

    if colC.button("🧹 초기화(처음부터)"):
        st.session_state.idx = 0
        st.session_state.answers = {}
        local_clear()
        st.warning("초기화했어. 처음부터 다시 시작! ✨")

st.divider()

# 진행률
total = len(QUESTIONS)
answered = len(st.session_state.answers)
progress = answered / total if total else 0
st.progress(progress, text=f"진행률: {answered}/{total}")

# 아직 질문 진행 중이면
if answered < total:
    q = QUESTIONS[st.session_state.idx]

    strength_info = KEY_TO_STRENGTH[q["strength"]]
    st.subheader(f"{strength_info['emoji']} {strength_info['name']}  ·  {strength_info['group']}")
    st.write(f"**Q{st.session_state.idx+1}.** {q['text']}")
    if q["reverse"]:
        st.caption("※ 살짝 반대로 묻는 문장이야 (정직하게 골라줘도 괜찮아)")

    # 응답 UI
    default_val = st.session_state.answers.get(q["id"], 3)
    val = st.slider("얼마나 동의해?", 1, 5, int(default_val), help="1=전혀 아니다 · 5=매우 그렇다")

    col1, col2, col3 = st.columns([1, 1, 1])

    if col1.button("⬅️ 이전"):
        st.session_state.idx = max(0, st.session_state.idx - 1)
        st.rerun()

    if col2.button("✅ 저장하고 다음"):
        st.session_state.answers[q["id"]] = int(val)
        st.session_state.idx = min(total - 1, st.session_state.idx + 1)
        # 자동 로컬 저장(편의)
        local_save({"idx": st.session_state.idx, "answers": st.session_state.answers, "username": st.session_state.username})
        st.rerun()

    if col3.button("⏭️ 건너뛰기"):
        st.session_state.idx = min(total - 1, st.session_state.idx + 1)
        st.rerun()

    st.info("팁: 중간에 꺼도 돼! 위에서 로컬 저장/불러오기로 이어서 가능 🌙")

else:
    # =========================
    # 결과 화면
    # =========================
    st.success("완료! 이제 너의 강점 요정들이 등장할 차례 🌈")

    df, top5 = compute_scores(st.session_state.answers)

    st.header("🏆 너의 Top 5 강점")
    for rank, r in enumerate(top5, start=1):
        s = KEY_TO_STRENGTH[r["key"]]
        with st.container(border=True):
            st.subheader(f"{rank}. {s['emoji']} {s['name']}  ·  {int(r['pct'])}점")
            st.write(f"**{s['short']}**")
            st.write(s["long"])
            st.write("**오늘의 미션(3개 추천)**")
            for m in s["missions"][:3]:
                st.checkbox(m, key=f"mission_{s['key']}_{m}")

    st.divider()

    st.header("📈 24개 강점 레이더 차트")
    fig = plot_radar(df.sort_values("name"), title="24개 강점 레이더 (0~100)")
    st.pyplot(fig, clear_figure=True)

    st.divider()

    st.header("🧾 24개 전체 점수")
    show_df = df.copy()
    show_df["강점"] = show_df["emoji"] + " " + show_df["name"]
    show_df["점수(0~100)"] = show_df["pct"].astype(int)
    show_df = show_df[["group", "강점", "점수(0~100)"]]
    st.dataframe(show_df, use_container_width=True, hide_index=True)

    st.divider()

    # PDF 생성 준비: 레이더 이미지를 png로 저장
    tmp_png = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
    fig2 = plot_radar(df.sort_values("pct", ascending=False), title="24개 강점 레이더 (점수순)")
    fig2.savefig(tmp_png, dpi=200, bbox_inches="tight")
    plt.close(fig2)

    pdf_bytes = make_pdf(df, top5, tmp_png, username=st.session_state.username)

    st.download_button(
        "📄 결과 PDF 다운로드",
        data=pdf_bytes,
        file_name="strength_report.pdf",
        mime="application/pdf",
        use_container_width=True
    )

    st.caption("※ PDF 한글이 깨지면: Windows는 보통 괜찮고, Mac/Linux는 한글 폰트가 없을 수 있어. 그때는 NanumGothic 같은 한글 폰트를 설치하면 해결돼.")

    # 저장/초기화 버튼
    c1, c2 = st.columns(2)
    if c1.button("💾 이 결과 로컬 저장"):
        local_save({"idx": st.session_state.idx, "answers": st.session_state.answers, "username": st.session_state.username})
        st.success("저장했어! 🎀")
    if c2.button("🔄 다시하기"):
        st.session_state.idx = 0
        st.session_state.answers = {}
        local_clear()
        st.rerun()
