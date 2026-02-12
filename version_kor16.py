# version_kor16.py
# 16 Strengths (Self-understanding) · 64 Questions · Top5 + 4-Domain Profile + Radar + PDF + Local Save
# Run: python3 -m streamlit run version_kor16.py

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
st.set_page_config(page_title="🌸 나의 강점(16) 자기이해 테스트", page_icon="🌈", layout="centered")
LOCAL_SAVE_PATH = Path.home() / ".strength_test_kor16_progress.json"


# =========================
# 1) Strength Model (16) - Self-understanding focused
# =========================
STRENGTHS = [
    # 🧠 생각의 방식 (4)
    dict(key="creativity", name="창의성", emoji="🎨", group="🧠 생각의 방식",
         short="같은 것도 다르게 보는 ‘관점 바꾸기’ 재능!",
         long="익숙한 상황에서도 새로운 관점과 연결을 찾아내는 힘이에요. 문제를 ‘다른 방식’으로 풀어보려는 마음이 자주 올라옵니다.",
         missions=["오늘 문제 하나를 ‘다른 방식’으로 풀어보기", "새 조합 1개 만들기(좋아하는 것 2개 섞기)", "아이디어 5개 적고 1개만 실행하기"]),
    dict(key="analysis", name="분석력", emoji="🧠", group="🧠 생각의 방식",
         short="복잡한 걸 정리해서 ‘핵심’으로 만드는 힘!",
         long="감정과 정보가 섞여도 구조를 잡고 근거를 확인하려는 힘이에요. 상황을 차분하게 정리해 ‘무엇이 중요한지’를 찾아냅니다.",
         missions=["결정 전 근거 3개 적기", "팩트 vs 추측 나누기", "문제를 ‘원인-결과’로 한 줄 정리하기"]),
    dict(key="insight", name="🌅 통찰력", emoji="🌅", group="🧠 생각의 방식",
         short="경험 속 의미를 건져 올리는 ‘큰 그림’!",
         long="사건을 겪은 뒤에도 그 의미와 흐름을 곱씹으며 패턴을 찾는 힘이에요. 지나간 일에서 교훈을 뽑아 현재 선택에 연결합니다.",
         missions=["오늘 일의 ‘교훈’ 한 줄 쓰기", "반복되는 패턴 1개 적기", "‘한 걸음 뒤에서 보기’ 30초"]),
    dict(key="learning_agility", name="학습민첩성", emoji="📚", group="🧠 생각의 방식",
         short="새로운 걸 빠르게 흡수하는 ‘감 잡기’ 능력!",
         long="낯선 주제나 환경에서도 빠르게 적응하고 배우는 힘이에요. 배우는 과정 자체에서 재미를 느낄 때도 많습니다.",
         missions=["새 주제 10분 맛보기", "배운 것 1문장 요약", "메모 3줄 남기기"]),

    # 🔥 행동의 에너지 (4)
    dict(key="drive", name="추진력", emoji="🚀", group="🔥 행동의 에너지",
         short="생각을 ‘시작’으로 옮기는 엔진!",
         long="아이디어가 생기면 실행으로 옮기고 싶은 힘이에요. 완벽한 준비보다 ‘해보면서 배우기’를 택하는 경우가 많습니다.",
         missions=["딱 10분만 시작하기", "오늘 해야 할 일 ‘첫 단계’만 하기", "미루던 것 1개 착수하기"]),
    dict(key="grit", name="끈기", emoji="🏃", group="🔥 행동의 에너지",
         short="끝을 보는 ‘완주력’!",
         long="어려워도 붙들고 가는 힘이에요. 지루해도 필요한 일은 해내며, 중간에 포기하면 찝찝함을 느끼기도 합니다.",
         missions=["25분 집중 1세트", "오늘 목표를 ‘끝’까지 작게 완주", "진행률 체크 1번"]),
    dict(key="self_regulation", name="자기조절", emoji="🧘", group="🔥 행동의 에너지",
         short="감정/습관을 다루는 ‘내 마음 조종사’!",
         long="감정이 올라와도 비교적 잘 조절하고, 충동을 줄이며 리듬을 만들려는 힘이에요. 기분에 끌려가기보다 방향을 잡습니다.",
         missions=["물 한 컵 + 숨 3번", "방해 요소 1개 치우기", "15분 타이머로 리셋하기"]),
    dict(key="courage", name="용기", emoji="🦁", group="🔥 행동의 에너지",
         short="불안해도 필요한 선택을 하는 ‘작은 용맹’!",
         long="갈등이나 낯선 상황이 두려워도 ‘해야 할 말/해야 할 일’을 선택하는 힘이에요. 회피 대신 한 걸음을 내딛습니다.",
         missions=["필요한 말 한 문장 연습", "불편하지만 중요한 일 1개 하기", "피하고 싶던 것 ‘작게’ 시도하기"]),

    # 🤝 관계의 태도 (4)
    dict(key="empathy", name="공감력", emoji="💗", group="🤝 관계의 태도",
         short="상대의 마음을 먼저 읽는 ‘따뜻한 레이더’!",
         long="표정/말투 변화에 민감하고, 조언보다 이해를 먼저 하려는 힘이에요. 타인의 감정이 나에게도 영향을 주는 편일 수 있어요.",
         missions=["공감 질문 1개 하기", "상대 말 70% 듣기", "감정 단어로 한 번 반영해주기"]),
    dict(key="influence", name="영향력", emoji="✨", group="🤝 관계의 태도",
         short="분위기와 방향에 ‘한 줄기 바람’처럼 영향 주기!",
         long="말과 행동으로 사람들의 흐름에 영향을 주는 힘이에요. 자연스럽게 중심이 되거나 방향을 제안하는 역할을 맡기도 합니다.",
         missions=["의견을 ‘한 문장’으로 제안", "칭찬/격려로 분위기 올리기", "대화 정리 1번 하기"]),
    dict(key="collaboration", name="협력성", emoji="🤝", group="🤝 관계의 태도",
         short="함께 조율해서 ‘같이 잘 가는’ 능력!",
         long="공동 목표를 위해 조정하고 역할을 맞추는 힘이에요. 협업에서 안정감을 느끼거나, 충돌을 줄이기 위해 조율을 합니다.",
         missions=["역할/기대치 맞추기", "도움 요청 또는 제안 1번", "작은 업데이트 공유하기"]),
    dict(key="reliability", name="신뢰성", emoji="🧱", group="🤝 관계의 태도",
         short="꾸준함과 책임으로 ‘믿음’을 만드는 힘!",
         long="약속을 지키고 맡은 일을 책임지려는 힘이에요. 반복적인 일도 꾸준히 해내며, 주변이 당신을 믿고 맡길 수 있습니다.",
         missions=["약속 1개 정확히 지키기", "반복 루틴 1개 유지", "해야 할 일 ‘마감’ 정하기"]),

    # 🌱 내면의 기반 (4)
    dict(key="optimism", name="낙관성", emoji="🌈", group="🌱 내면의 기반",
         short="가능성을 보는 ‘무지개 시선’!",
         long="힘든 상황에서도 ‘잘될 수 있는 길’을 찾는 힘이에요. 다만 스트레스가 클 때는 걱정이 앞설 수도 있어요.",
         missions=["가능한 다음 कदम 1개 찾기", "좋은 결과를 10초 상상", "오늘의 작은 희망 1줄"]),
    dict(key="prudence", name="신중함", emoji="🐢", group="🌱 내면의 기반",
         short="리스크를 보는 ‘안전한 거북이’!",
         long="결정 전에 여러 경우를 생각하고 쉽게 단정짓지 않는 힘이에요. 안정감을 만들지만, 과하면 시작이 늦어질 수 있어요.",
         missions=["체크리스트 5개 만들기", "결정 10분 미루고 재검토", "리스크 1개 대비하기"]),
    dict(key="gratitude", name="감사성", emoji="🙏", group="🌱 내면의 기반",
         short="좋은 것을 알아채는 ‘고마움 수집가’!",
         long="일상에서 고마운 순간을 잘 발견하고, 도움을 받은 것을 기억하는 힘이에요. 마음 회복력에도 도움이 됩니다.",
         missions=["감사 3가지 적기", "고마운 사람에게 메시지", "오늘 운 좋았던 순간 1개"]),
    dict(key="meaning", name="의미지향성", emoji="✨", group="🌱 내면의 기반",
         short="내 삶의 방향을 찾는 ‘북극성 감각’!",
         long="선택이 나의 가치/방향과 맞는지 점검하는 힘이에요. 바쁠수록 ‘왜 이걸 하지?’ 질문이 중요한 키가 됩니다.",
         missions=["내 가치 1개 적기", "오늘 선택 1개를 가치에 맞추기", "‘왜 중요한가’ 답하기 1번"]),
]

KEY_TO_STRENGTH = {s["key"]: s for s in STRENGTHS}


# =========================
# 2) Questions (64 = 16*4) - fully rewritten, less repetitive
#    reverse=True means score = 6 - answer
# =========================
QUESTIONS = [
    # 창의성 (1-4)
    dict(id="q1",  strength="creativity", reverse=False, text="같은 상황에서도 다른 해석이 가능하다는 생각이 자주 든다."),
    dict(id="q2",  strength="creativity", reverse=False, text="기존 방식이 있어도 ‘다르게 해보면?’이라는 마음이 든다."),
    dict(id="q3",  strength="creativity", reverse=False, text="서로 관련 없어 보이는 것들 사이에서 연결점을 찾는 편이다."),
    dict(id="q4",  strength="creativity", reverse=True,  text="이미 정해진 틀이 있다면 굳이 바꿀 필요는 없다고 느낀다."),

    # 분석력 (5-8)
    dict(id="q5",  strength="analysis", reverse=False, text="이야기를 들으면 자연스럽게 구조(원인-결과/핵심-부가)를 정리하게 된다."),
    dict(id="q6",  strength="analysis", reverse=False, text="감정보다 근거와 사실을 먼저 확인하려 한다."),
    dict(id="q7",  strength="analysis", reverse=False, text="복잡한 상황에서도 ‘핵심이 무엇인지’ 찾으려 한다."),
    dict(id="q8",  strength="analysis", reverse=True,  text="느낌이 맞으면 굳이 따져보지 않아도 된다고 생각한다."),

    # 통찰력 (9-12)
    dict(id="q9",  strength="insight", reverse=False, text="사건이 끝난 후 그 의미를 곱씹는 편이다."),
    dict(id="q10", strength="insight", reverse=False, text="경험에서 배운 교훈을 다른 상황에도 연결하는 편이다."),
    dict(id="q11", strength="insight", reverse=False, text="비슷한 일이 반복될 때 ‘패턴’이 먼저 보이는 편이다."),
    dict(id="q12", strength="insight", reverse=True,  text="지난 일을 굳이 되돌아보지 않아도 괜찮다고 느낀다."),

    # 학습민첩성 (13-16)
    dict(id="q13", strength="learning_agility", reverse=False, text="새로운 분야를 접해도 비교적 빨리 감을 잡는다."),
    dict(id="q14", strength="learning_agility", reverse=False, text="낯선 환경에서도 적응이 빠른 편이다."),
    dict(id="q15", strength="learning_agility", reverse=False, text="배우는 과정 자체가 흥미롭게 느껴진다."),
    dict(id="q16", strength="learning_agility", reverse=True,  text="새로운 것을 배우는 일은 부담부터 느껴진다."),

    # 추진력 (17-20)
    dict(id="q17", strength="drive", reverse=False, text="아이디어가 떠오르면 일단 작게라도 실행해보고 싶다."),
    dict(id="q18", strength="drive", reverse=False, text="생각보다 행동이 빠른 편이다."),
    dict(id="q19", strength="drive", reverse=False, text="시작하는 데 큰 망설임이 없는 편이다."),
    dict(id="q20", strength="drive", reverse=True,  text="충분히 준비되기 전에는 움직이지 않는 편이다."),

    # 끈기 (21-24)
    dict(id="q21", strength="grit", reverse=False, text="어려워도 중간에 쉽게 포기하지 않는다."),
    dict(id="q22", strength="grit", reverse=False, text="끝을 보지 않으면 마음이 불편한 편이다."),
    dict(id="q23", strength="grit", reverse=False, text="지루해도 해야 할 일은 해내는 편이다."),
    dict(id="q24", strength="grit", reverse=True,  text="흥미가 떨어지면 금방 손을 놓는 편이다."),

    # 자기조절 (25-28)
    dict(id="q25", strength="self_regulation", reverse=False, text="감정이 올라와도 비교적 잘 다스리는 편이다."),
    dict(id="q26", strength="self_regulation", reverse=False, text="충동적으로 행동하는 일이 많지 않다."),
    dict(id="q27", strength="self_regulation", reverse=False, text="해야 할 일과 쉬어야 할 일을 구분하려고 한다."),
    dict(id="q28", strength="self_regulation", reverse=True,  text="기분에 따라 하루가 크게 좌우되는 편이다."),

    # 용기 (29-32)
    dict(id="q29", strength="courage", reverse=False, text="불안해도 필요한 선택은 하려 한다."),
    dict(id="q30", strength="courage", reverse=False, text="의견이 다를 때도 말해야 한다면 말하는 편이다."),
    dict(id="q31", strength="courage", reverse=False, text="낯선 상황을 무조건 피하기보다는 ‘해볼 수 있는 만큼’ 시도한다."),
    dict(id="q32", strength="courage", reverse=True,  text="갈등이 생길 것 같으면 웬만하면 피하려 한다."),

    # 공감력 (33-36)
    dict(id="q33", strength="empathy", reverse=False, text="상대의 표정이나 말투 변화에 민감한 편이다."),
    dict(id="q34", strength="empathy", reverse=False, text="누군가 힘들어 보이면 마음이 쓰인다."),
    dict(id="q35", strength="empathy", reverse=False, text="조언보다 먼저 이해하려고 한다."),
    dict(id="q36", strength="empathy", reverse=True,  text="다른 사람의 감정은 크게 신경 쓰지 않는 편이다."),

    # 영향력 (37-40)
    dict(id="q37", strength="influence", reverse=False, text="내가 말하면 분위기가 조금은 바뀌는 걸 느낀다."),
    dict(id="q38", strength="influence", reverse=False, text="사람들의 방향을 제시하는 역할을 맡는 경우가 있다."),
    dict(id="q39", strength="influence", reverse=False, text="자연스럽게 중심에 서게 되는 편이다."),
    dict(id="q40", strength="influence", reverse=True,  text="나는 주로 뒤에서 따르는 역할이 더 편하다."),

    # 협력성 (41-44)
    dict(id="q41", strength="collaboration", reverse=False, text="혼자보다는 함께할 때 안정감을 느끼는 편이다."),
    dict(id="q42", strength="collaboration", reverse=False, text="역할을 조율하는 과정이 크게 부담되지 않는다."),
    dict(id="q43", strength="collaboration", reverse=False, text="공동의 목표를 위해 조정하려는 편이다."),
    dict(id="q44", strength="collaboration", reverse=True,  text="혼자 하는 일이 훨씬 마음이 편하다."),

    # 신뢰성 (45-48)
    dict(id="q45", strength="reliability", reverse=False, text="맡은 일은 약속한 대로 하려고 한다."),
    dict(id="q46", strength="reliability", reverse=False, text="반복적인 일도 꾸준히 해낸다."),
    dict(id="q47", strength="reliability", reverse=False, text="책임이 생기면 회피하지 않으려 한다."),
    dict(id="q48", strength="reliability", reverse=True,  text="상황이 바뀌면 약속도 쉽게 바뀔 수 있다고 생각한다."),

    # 낙관성 (49-52)
    dict(id="q49", strength="optimism", reverse=False, text="힘든 상황에서도 가능성을 찾으려 한다."),
    dict(id="q50", strength="optimism", reverse=False, text="잘될 수 있는 그림을 상상해본다."),
    dict(id="q51", strength="optimism", reverse=False, text="문제 속에서도 배울 점을 찾으려 한다."),
    dict(id="q52", strength="optimism", reverse=True,  text="일이 생기면 먼저 걱정부터 앞선다."),

    # 신중함 (53-56)
    dict(id="q53", strength="prudence", reverse=False, text="결정 전에는 여러 경우를 생각해본다."),
    dict(id="q54", strength="prudence", reverse=False, text="리스크를 고려하는 편이다."),
    dict(id="q55", strength="prudence", reverse=False, text="쉽게 단정 짓지 않는 편이다."),
    dict(id="q56", strength="prudence", reverse=True,  text="일단 해보고 보자는 태도가 더 많다."),

    # 감사성 (57-60)
    dict(id="q57", strength="gratitude", reverse=False, text="일상에서 고마운 순간을 자주 떠올린다."),
    dict(id="q58", strength="gratitude", reverse=False, text="도움을 받으면 기억하려 한다."),
    dict(id="q59", strength="gratitude", reverse=False, text="작은 일에도 고마움을 느끼는 편이다."),
    dict(id="q60", strength="gratitude", reverse=True,  text="받은 도움을 오래 기억하지는 않는 편이다."),

    # 의미지향성 (61-64)
    dict(id="q61", strength="meaning", reverse=False, text="내가 왜 이 일을 하는지 생각해본다."),
    dict(id="q62", strength="meaning", reverse=False, text="삶의 방향에 대해 종종 고민한다."),
    dict(id="q63", strength="meaning", reverse=False, text="선택이 나의 가치와 맞는지 확인하려 한다."),
    dict(id="q64", strength="meaning", reverse=True,  text="굳이 삶의 의미까지 생각할 필요는 없다고 느낀다."),
]


# =========================
# 3) Domain mapping (4 domains)
# =========================
DOMAINS = [
    dict(key="thinking", name="🧠 생각의 방식", keys=["creativity", "analysis", "insight", "learning_agility"]),
    dict(key="action",   name="🔥 행동의 에너지", keys=["drive", "grit", "self_regulation", "courage"]),
    dict(key="relation", name="🤝 관계의 태도", keys=["empathy", "influence", "collaboration", "reliability"]),
    dict(key="inner",    name="🌱 내면의 기반", keys=["optimism", "prudence", "gratitude", "meaning"]),
]


# =========================
# 4) Helpers: local save/load
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
# 5) Scoring
# =========================
def compute_strength_scores(answers: dict) -> pd.DataFrame:
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
        avg = (sum(arr) / len(arr)) if arr else 0.0
        pct = round(((avg - 1) / 4) * 100) if arr else 0
        rows.append(dict(
            key=s["key"],
            name=s["name"],
            emoji=s["emoji"],
            group=s["group"],
            avg=avg,
            pct=pct
        ))

    df = pd.DataFrame(rows)
    df = df.sort_values(["avg", "name"], ascending=[False, True]).reset_index(drop=True)
    return df

def compute_domain_scores(df_strengths: pd.DataFrame) -> pd.DataFrame:
    lookup = {r["key"]: int(r["pct"]) for r in df_strengths.to_dict("records")}
    drows = []
    for d in DOMAINS:
        vals = [lookup[k] for k in d["keys"]]
        drows.append(dict(
            key=d["key"],
            domain=d["name"],
            score=int(round(sum(vals)/len(vals)))
        ))
    ddf = pd.DataFrame(drows).sort_values("score", ascending=False).reset_index(drop=True)
    return ddf

def top5(df_strengths: pd.DataFrame):
    return df_strengths.head(5).to_dict("records")


# =========================
# 6) Plots
# =========================
def plot_radar_strengths(df_scores: pd.DataFrame, title="16개 강점 레이더 (0~100)"):
    labels = df_scores["name"].tolist()
    values = df_scores["pct"].astype(int).tolist()

    N = len(labels)
    angles = [n / float(N) * 2 * math.pi for n in range(N)]
    angles += angles[:1]
    values_loop = values + values[:1]

    fig = plt.figure(figsize=(7, 7))
    ax = plt.subplot(111, polar=True)

    ax.set_theta_offset(math.pi / 2)
    ax.set_theta_direction(-1)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=9)

    ax.set_rlabel_position(0)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(["20", "40", "60", "80", "100"], fontsize=8)
    ax.set_ylim(0, 100)

    ax.plot(angles, values_loop, linewidth=2)
    ax.fill(angles, values_loop, alpha=0.15)
    ax.set_title(title, pad=20)
    return fig

def plot_domain_bars(ddf: pd.DataFrame, title="영역별 프로필 (0~100)"):
    fig = plt.figure(figsize=(7, 4))
    ax = plt.gca()
    ax.bar(ddf["domain"], ddf["score"])
    ax.set_ylim(0, 100)
    ax.set_title(title)
    ax.tick_params(axis="x", labelrotation=0)
    return fig


# =========================
# 7) PDF (Korean font auto-register attempt)
# =========================
def register_korean_font():
    candidates = [
        # Windows
        r"C:\Windows\Fonts\malgun.ttf",
        r"C:\Windows\Fonts\malgunbd.ttf",
        # macOS (common)
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        "/Library/Fonts/AppleGothic.ttf",
        # Linux (common)
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

def make_pdf(df_strengths: pd.DataFrame, ddf_domains: pd.DataFrame, top5_list: list, radar_png_path: str, username: str = "") -> bytes:
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
    c.drawString(margin, y, "🌸 나의 강점(16) 자기이해 테스트 리포트")
    y -= 1.2 * cm

    set_font(11)
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    c.drawString(margin, y, f"이름: {username if username else '(미입력)'}")
    y -= 0.6 * cm
    c.drawString(margin, y, f"생성 시각: {stamp}")
    y -= 1.0 * cm

    set_font(14)
    c.drawString(margin, y, "🏆 Top 5 강점")
    y -= 0.7 * cm

    set_font(11)
    for i, r in enumerate(top5_list, start=1):
        s = KEY_TO_STRENGTH[r["key"]]
        line = f"{i}. {s['emoji']} {s['name']} ({int(r['pct'])}점) - {s['short']}"
        c.drawString(margin, y, line[:110])
        y -= 0.55 * cm
        if y < 7 * cm:
            c.showPage()
            y = H - margin
            set_font(11)

    y -= 0.3 * cm
    set_font(14)
    c.drawString(margin, y, "📊 영역별 프로필")
    y -= 0.7 * cm

    set_font(11)
    for _, row in ddf_domains.sort_values("score", ascending=False).iterrows():
        c.drawString(margin, y, f"{row['domain']}: {int(row['score'])}점")
        y -= 0.55 * cm
        if y < 9 * cm:
            c.showPage()
            y = H - margin
            set_font(11)

    y -= 0.3 * cm
    set_font(14)
    c.drawString(margin, y, "📈 16개 강점 레이더")
    y -= 0.6 * cm

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
    c.drawString(margin, y, "🧾 전체 점수(16)")
    y -= 0.7 * cm

    set_font(10)
    rows = df_strengths.sort_values("pct", ascending=False).to_dict("records")
    col_x = [margin, margin + 7*cm, margin + 13*cm]
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
# 8) Domain interpretation (simple, useful)
# =========================
def domain_commentary(ddf: pd.DataFrame) -> str:
    # Highest and lowest domain commentary
    ordered = ddf.sort_values("score", ascending=False).to_dict("records")
    hi = ordered[0]
    lo = ordered[-1]
    gap = hi["score"] - lo["score"]

    msg = []
    msg.append(f"**가장 강한 영역:** {hi['domain']} ({hi['score']}점)")
    msg.append(f"**상대적으로 낮은 영역:** {lo['domain']} ({lo['score']}점)")

    if gap >= 25:
        msg.append("👉 영역 간 차이가 꽤 커요. 강한 영역으로 일상이 굴러가고, 낮은 영역은 ‘에너지 절약 모드’일 수 있어요.")
    elif gap >= 12:
        msg.append("👉 영역이 어느 정도 구분돼요. 강한 영역을 잘 쓰되, 낮은 영역은 ‘작게’ 보완하면 균형이 좋아질 수 있어요.")
    else:
        msg.append("👉 영역 점수가 비교적 고르게 나왔어요. 상황에 따라 유연하게 쓰는 타입일 가능성이 커요.")

    # quick tips per domain
    tips = {
        "🧠 생각의 방식": "생각이 강하면 ‘실행의 첫 단계’를 작게 잡아주면 좋아요.",
        "🔥 행동의 에너지": "행동이 강하면 ‘방향 점검(왜/어디로)’을 짧게 넣으면 더 단단해져요.",
        "🤝 관계의 태도": "관계가 강하면 ‘경계/휴식’도 실력이라, 내 에너지 관리가 중요해요.",
        "🌱 내면의 기반": "내면이 강하면 ‘가치 기반 선택’이 쉬워져요. 다만 과도한 고민은 시작을 늦출 수 있어요."
    }
    msg.append("")
    msg.append("**한 줄 팁**")
    for r in ordered:
        msg.append(f"- {r['domain']}: {tips.get(r['domain'], '')}")

    return "\n".join(msg)


# =========================
# 9) Session State init
# =========================
if "idx" not in st.session_state:
    st.session_state.idx = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "username" not in st.session_state:
    st.session_state.username = ""


# =========================
# 10) UI
# =========================
st.title("🌸 나의 강점(16) 자기이해 테스트")
st.caption("16개 강점 · 64문항 · Top5 · 영역별 프로필 · 레이더 · PDF · 로컬 저장")

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

total = len(QUESTIONS)
answered = len(st.session_state.answers)
progress = answered / total if total else 0
st.progress(progress, text=f"진행률: {answered}/{total}")


# =========================
# 11) Test flow
# =========================
if answered < total:
    # keep idx within range
    st.session_state.idx = max(0, min(st.session_state.idx, total - 1))
    q = QUESTIONS[st.session_state.idx]
    s_info = KEY_TO_STRENGTH[q["strength"]]

    st.subheader(f"{s_info['emoji']} {s_info['name']}  ·  {s_info['group']}")
    st.write(f"**Q{st.session_state.idx+1}.** {q['text']}")
    if q["reverse"]:
        st.caption("※ 이 문항은 ‘반대로’ 물어보는 문장이야. 솔직히 골라도 괜찮아.")

    default_val = st.session_state.answers.get(q["id"], 3)
    val = st.slider("얼마나 동의해?", 1, 5, int(default_val), help="1=전혀 아니다 · 5=매우 그렇다")

    col1, col2, col3 = st.columns([1, 1, 1])
    if col1.button("⬅️ 이전"):
        st.session_state.idx = max(0, st.session_state.idx - 1)
        st.rerun()

    if col2.button("✅ 저장하고 다음"):
        st.session_state.answers[q["id"]] = int(val)
        # move to next unanswered if possible
        nxt = min(total - 1, st.session_state.idx + 1)
        st.session_state.idx = nxt
        local_save({"idx": st.session_state.idx, "answers": st.session_state.answers, "username": st.session_state.username})
        st.rerun()

    if col3.button("⏭️ 건너뛰기"):
        st.session_state.idx = min(total - 1, st.session_state.idx + 1)
        st.rerun()

    st.info("팁: 중간에 멈춰도 돼! 위에서 로컬 저장/불러오기로 이어서 가능 🌙")

else:
    # =========================
    # 12) Results
    # =========================
    st.success("완료! 이제 너의 강점 프로필을 볼 시간이야 🌈")

    df_strengths = compute_strength_scores(st.session_state.answers)
    ddf_domains = compute_domain_scores(df_strengths)
    top5_list = top5(df_strengths)

    # Top5 cards
    st.header("🏆 Top 5 강점")
    for rank, r in enumerate(top5_list, start=1):
        s = KEY_TO_STRENGTH[r["key"]]
        with st.container(border=True):
            st.subheader(f"{rank}. {s['emoji']} {s['name']}  ·  {int(r['pct'])}점")
            st.write(f"**{s['short']}**")
            st.write(s["long"])
            st.write("**오늘의 미션(3개)**")
            for m in s["missions"][:3]:
                st.checkbox(m, key=f"mission_{s['key']}_{m}")

    st.divider()

    # Domain profile
    st.header("📊 영역별 프로필")
    st.markdown(domain_commentary(ddf_domains))

    fig_dom = plot_domain_bars(ddf_domains.sort_values("domain"), title="영역별 프로필 (0~100)")
    st.pyplot(fig_dom, clear_figure=True)

    st.divider()

    # Radar (16 strengths)
    st.header("📈 16개 강점 레이더 차트")
    fig = plot_radar_strengths(df_strengths.sort_values("name"), title="16개 강점 레이더 (0~100)")
    st.pyplot(fig, clear_figure=True)

    st.divider()

    # Table
    st.header("🧾 전체 점수(16)")
    show_df = df_strengths.copy()
    show_df["강점"] = show_df["emoji"] + " " + show_df["name"]
    show_df["점수(0~100)"] = show_df["pct"].astype(int)
    show_df = show_df[["group", "강점", "점수(0~100)"]].sort_values(["group", "점수(0~100)"], ascending=[True, False])
    st.dataframe(show_df, use_container_width=True, hide_index=True)

    st.divider()

    # PDF download
    tmp_png = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
    fig2 = plot_radar_strengths(df_strengths.sort_values("pct", ascending=False), title="16개 강점 레이더 (점수순)")
    fig2.savefig(tmp_png, dpi=200, bbox_inches="tight")
    plt.close(fig2)

    pdf_bytes = make_pdf(df_strengths, ddf_domains, top5_list, tmp_png, username=st.session_state.username)

    st.download_button(
        "📄 결과 PDF 다운로드",
        data=pdf_bytes,
        file_name="strength_report_kor16.pdf",
        mime="application/pdf",
        use_container_width=True
    )

    st.caption("※ PDF에서 한글이 깨지면: (Mac/Linux) 한글 폰트가 없을 수 있어요. NanumGothic 설치하면 해결되는 경우가 많아요.")

    # Save / Retake
    c1, c2 = st.columns(2)
    if c1.button("💾 이 결과 로컬 저장"):
        local_save({"idx": st.session_state.idx, "answers": st.session_state.answers, "username": st.session_state.username})
        st.success("저장했어! 🎀")

    if c2.button("🔄 다시하기"):
        st.session_state.idx = 0
        st.session_state.answers = {}
        local_clear()
        st.rerun()
