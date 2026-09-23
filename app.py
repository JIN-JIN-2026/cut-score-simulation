import io
import json
import os
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Paper-Based Assessment Estimated Cut Score Simulator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_FILE = os.path.join(os.path.dirname(__file__), "app_state.json")

# =========================================================
# Multi-Language (i18n) Translations (English as Default)
# =========================================================
TEXTS = {
    "EN": {
        "title": "📊 Paper-Based Assessment Estimated Cut Score Simulator",
        "tab_setup": "⚙️ Test Setup",
        "tab_entry": "📝 Teacher Entry & Management",
        "tab_lookup": "👥 [Combined] Teacher Entry Details",
        "tab_category": "📊 [Combined] Category Statistics",
        "tab_final": "🎯 [Combined] Estimated Cut Scores",
        "tab_comparison": "🔄 Round Comparison",
        "select_round": "🎯 Active Round Selection (Round 1 ~ 8)",
        "round_label": "Round",
        "current_round_info": "Currently working on:",
        "setup_sub": "1️⃣ Test Structure, Round & Teachers Setup",
        "setup_cap": (
            "Select active round (1 to 8), configure item types, score sums by"
            " difficulty, and teacher info."
        ),
        "item_teacher_header": "[1] Item Types & Teacher Info",
        "include_essay": "Include Constructed Response Items",
        "num_teachers": "Number of Participating Teachers",
        "teacher_names": "Teacher Names:",
        "teacher_label": "Teacher",
        "score_sums_header": "[2] Score Sums by Difficulty",
        "mc_scores": "📌 Multiple Choice Score Sums",
        "essay_scores": "📌 Constructed Response Score Sums",
        "easy_sum": "Easy Sum",
        "mid_sum": "Moderate Sum",
        "hard_sum": "Hard Sum",
        "total_points": "Total Test Points",
        "pts": "pts",
        "match_100": "100 Points Match",
        "mismatch_100": "Points Mismatch",
        "apply_btn": "🚀 Apply Configuration to All Rounds (Round 1~8)",
        "apply_success": "✅ Configuration applied to all rounds (Round 1~8)!",
        "copy_prev_round_btn": "📋 Copy Data from Previous Round",
        "copy_success": (
            "✅ Copied configuration and entries from previous round!"
        ),
        "sync_all_rounds_notice": "💡 Note: Test structure and score sums configured here are automatically applied to all rounds (Round 1~8).",
        "mc": "Multiple Choice",
        "essay": "Constructed Response",
        "easy": "Easy",
        "moderate": "Moderate",
        "hard": "Hard",
        "track_dept": "Track/Grade/Dept",
        "general_dept": "General/1/General",
        "score_sum_col": "Score Sum",
        "item_type_col": "Item Type",
        "diff_col": "Difficulty",
        "entry_sub": "📝 Expected Correct Rate Entry & Validation",
        "no_teachers": (
            "No registered teachers found. Please add teachers in 'Test Setup'."
        ),
        "select_teacher": "Select Teacher to Edit",
        "selected_teacher": "Selected Teacher:",
        "edit_hint": (
            "(Edits in the table apply instantly and mark status as Submitted)"
        ),
        "errors_detected": "🚨 Constraint Violations Detected:",
        "passed_constraints": "✅ Constraints Passed (Valid Input)",
        "lookup_sub": "[Combined] Teacher Entry Details Total",
        "filter_teacher": "Filter Teacher",
        "filter_placeholder": "Enter teacher name",
        "export_excel": "📊 Export Excel",
        "no_data": "No records found.",
        "cat_sub": "[Combined] Category Statistics Total",
        "cat_item_col": "Item Category (Difficulty)",
        "achieve_level": "Achievement Level",
        "stat_category": "Statistic",
        "mean": "Mean",
        "std_dev": "Std Dev",
        "min": "Min",
        "max": "Max",
        "final_sub": "[Combined] Estimated Cut Scores Total",
        "all_subjects_excel": "📊 All Subjects Excel",
        "export_excel_short": "📊 Export Excel",
        "print_btn": "🖨️ Print",
        "final_cut_header": (
            "📌 Final Estimated Cut Scores (Based on Mean Values)"
        ),
        "below_e": "Below E",
        "category_col": "Category",
        "cut_score_label": "Cut Score",
        "comp_sub": "🔄 Round-by-Round Estimated Cut Score Comparison",
        "comp_cap": (
            "Compare cut score trends and convergence from Round 1 through"
            " Round 8 on a single screen."
        ),
        "comp_matrix_title": "📊 Mean Cut Scores Comparison Matrix",
        "comp_chart_title": "📈 Cut Score Trajectory across Rounds",
        "comp_delta_title": "📌 Delta Changes (Active Round vs Round 1)",
        "boundary_col": "Cut Boundary",
        "status_col": "Status",
        "submitted": "🟢 Submitted",
        "pending": "🔴 Not Entered",
        "mark_submitted_btn": "✅ Confirm & Submit Entry",
        "mark_pending_btn": "🔄 Reset to Not Entered",
        "status_info": "Status:",
        "submitted_teachers_count": "Submitted Teachers:",
        "no_submitted_warning": (
            "⚠️ No teacher entries have been submitted yet for this round."
            " Please enter and submit teacher predictions in 'Teacher Entry &"
            " Management'."
        ),
        "calc_included_info": "Calculated based on submitted teachers only:",
        "admin_menu": "🔒 Admin Controls",
        "admin_pwd": "Admin Password",
        "admin_reset_btn": "⚠️ Reset All System Data (Admin Only)",
        "admin_reset_success": "✅ All system data has been reset to defaults!",
        "admin_pwd_wrong": "❌ Incorrect Admin Password.",
        "shared_data_info": "💾 Shared Real-Time DB Active",
        "sync_btn": "🔄 Sync / Refresh Shared Data",
        "sync_success": "✅ Synced latest shared data!",
    },
    "KO": {
        "title": "📊 지필평가 추정분할점수 시뮬레이터",
        "tab_setup": "⚙️ 시험 기본 설정",
        "tab_entry": "📝 교사별 정답률 입력/관리",
        "tab_lookup": "👥 [통합산출] 교사별입력정보조회",
        "tab_category": "📊 [통합산출] 문항범주별조회",
        "tab_final": "🎯 [통합산출] 예상추정분할점수조회",
        "tab_comparison": "🔄 라운드별 비교",
        "select_round": "🎯 현재 라운드 선택 (1 ~ 8라운드)",
        "round_label": "라운드",
        "current_round_info": "현재 수정 중인 라운드:",
        "setup_sub": "1️⃣ 시험 구조, 라운드 및 입력 교사 설정",
        "setup_cap": (
            "1~8라운드 중 입력할 라운드를 선택하고 시험 구조, 난이도별 배점합,"
            " 교사 정보를 설정합니다."
        ),
        "item_teacher_header": "[1] 문항 구분 및 교사 정보",
        "include_essay": "서답형 문항 포함",
        "num_teachers": "입력할 교사 수",
        "teacher_names": "교사 이름 입력:",
        "teacher_label": "교사",
        "score_sums_header": "[2] 난이도별 배점합 설정",
        "mc_scores": "📌 선택형 배점합",
        "essay_scores": "📌 서답형 배점합",
        "easy_sum": "쉬움 배점합",
        "mid_sum": "보통 배점합",
        "hard_sum": "어려움 배점합",
        "total_points": "총 배점 합계",
        "pts": "점",
        "match_100": "100점 일치",
        "mismatch_100": "100점 불일치",
        "apply_btn": "🚀 위 설정으로 1~8라운드 전체 배점합 및 구조 동시 적용",
        "apply_success": "✅ 1~8라운드 전체에 시험 구조 및 배점합 설정이 동시 적용되었습니다!",
        "copy_prev_round_btn": "📋 이전 라운드 데이터 불러오기",
        "copy_success": (
            "✅ 이전 라운드의 설정 및 입력 데이터가 복사되었습니다!"
        ),
        "sync_all_rounds_notice": "💡 안내: 설정한 문항 구분, 교사 목록 및 난이도별 배점합은 1~8라운드 전체에 동시 적용됩니다.",
        "mc": "선택형",
        "essay": "서답형",
        "easy": "쉬움",
        "moderate": "보통",
        "hard": "어려움",
        "track_dept": "계열/학년/학과",
        "general_dept": "일반계/1/일반학과",
        "score_sum_col": "배점합",
        "item_type_col": "문항유형",
        "diff_col": "난이도",
        "entry_sub": "📝 교사별 예상정답률 입력 및 검증",
        "no_teachers": (
            "등록된 교사가 없습니다. '시험 기본 설정' 탭에서 교사를"
            " 추가해주세요."
        ),
        "select_teacher": "입력/수정할 교사 선택",
        "selected_teacher": "선택된 교사:",
        "edit_hint": (
            "(표 내부 값을 수정하면 자동으로 '입력 완료' 상태로 전환됩니다)"
        ),
        "errors_detected": "🚨 제약조건 위반으로 산출 확정이 불가능합니다:",
        "passed_constraints": "✅ 제약조건 통과 (정상 입력)",
        "lookup_sub": "[통합산출] 교사별입력정보조회 Total",
        "filter_teacher": "교사명 검색",
        "filter_placeholder": "교사명 입력",
        "export_excel": "📊 엑셀다운로드",
        "no_data": "조회할 데이터가 없습니다.",
        "cat_sub": "[통합산출] 문항범주별조회 Total",
        "cat_item_col": "문항유형(난이도)",
        "achieve_level": "성취수준",
        "stat_category": "통계구분",
        "mean": "평균",
        "std_dev": "표준편차",
        "min": "최솟값",
        "max": "최댓값",
        "final_sub": "[통합산출] 예상추정분할점수조회 Total",
        "all_subjects_excel": "📊 전과목 엑셀",
        "export_excel_short": "📊 엑셀다운",
        "print_btn": "🖨️ 출력",
        "final_cut_header": (
            "📌 최종 나이스 반영 기준 분할점수 (평균치 기준)"
        ),
        "below_e": "미도달",
        "category_col": "구분",
        "cut_score_label": "분할점수",
        "comp_sub": "🔄 라운드별 추정분할점수 비교 조회",
        "comp_cap": (
            "1라운드부터 8라운드까지의 분할점수 수렴 및 변동 추이를 한 화면에서"
            " 비교합니다."
        ),
        "comp_matrix_title": "📊 라운드별 평균 추정분할점수 비교 표",
        "comp_chart_title": "📈 라운드별 분할점수 수렴 추이 그래프",
        "comp_delta_title": "📌 1라운드 대비 현재 라운드 점수 변화량 (Delta)",
        "boundary_col": "분할점수 경계",
        "status_col": "입력 상태",
        "submitted": "🟢 입력 완료",
        "pending": "🔴 미입력",
        "mark_submitted_btn": "✅ 입력 완료 확정",
        "mark_pending_btn": "🔄 미입력 상태로 초기화",
        "status_info": "현재 입력 상태:",
        "submitted_teachers_count": "입력 완료 교사 수:",
        "no_submitted_warning": (
            "⚠️ 현재 라운드에 입력 완료된 교사 데이터가 없습니다. '교사별"
            " 정답률 입력/관리' 탭에서 정답률을 입력해 주세요."
        ),
        "calc_included_info": "입력 완료된 교사 기준으로 산출됨:",
        "admin_menu": "🔒 관리자 메뉴 (Admin)",
        "admin_pwd": "관리자 비밀번호 (기본: admin)",
        "admin_reset_btn": "⚠️ 전체 데이터 초기화 (Reset)",
        "admin_reset_success": "✅ 모든 데이터가 초기 상태로 리셋되었습니다!",
        "admin_pwd_wrong": "❌ 비밀번호가 올바르지 않습니다.",
        "shared_data_info": "💾 동시 접속 공유 DB: 실시간 저장 중",
        "sync_btn": "🔄 최신 동유 데이터 새로고침",
        "sync_success": "✅ 최신 동유 데이터를 불러왔습니다!",
    },
}

# Sidebar Language Selection (Default: English)
st.sidebar.title("⚙️ Options / 옵션")
lang_choice = st.sidebar.radio(
    "🌐 Select Language / 언어 선택",
    ["English", "한국어"],
    index=0,  # 영어가 기본값
    key="lang_selector",
)
lang_code = "EN" if lang_choice == "English" else "KO"


def t(key):
    return TEXTS[lang_code].get(key, key)


ITEM_TYPE_MAP = {
    "MC": t("mc"),
    "CR": t("essay"),
}
DIFF_MAP = {
    "easy": t("easy"),
    "mid": t("moderate"),
    "hard": t("hard"),
}

# =========================================================
# 파일 기반 데이터 영구 저장 및 로드 함수 (공유 DB)
# =========================================================
def load_app_state():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                rounds_data = {}
                for r_str, r_val in data.get("rounds_data", {}).items():
                    rounds_data[int(r_str)] = r_val
                return data.get("current_round", 1), rounds_data
        except Exception:
            pass
    return None, None


def save_app_state(current_round, rounds_data):
    try:
        serializable_rounds = {str(r): val for r, val in rounds_data.items()}
        payload = {
            "current_round": current_round,
            "rounds_data": serializable_rounds,
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"Save error: {e}")


def create_default_rounds_data():
    default_groups_config = [
        {
            "q_type": "MC",
            "diff": "easy",
            "dept": "General/1/General",
            "score_sum": 25.0,
        },
        {
            "q_type": "MC",
            "diff": "mid",
            "dept": "General/1/General",
            "score_sum": 35.0,
        },
        {
            "q_type": "MC",
            "diff": "hard",
            "dept": "General/1/General",
            "score_sum": 15.0,
        },
        {
            "q_type": "CR",
            "diff": "easy",
            "dept": "General/1/General",
            "score_sum": 10.0,
        },
        {
            "q_type": "CR",
            "diff": "hard",
            "dept": "General/1/General",
            "score_sum": 15.0,
        },
    ]

    default_teachers = (
        ["Teacher Kim", "Teacher Lee", "Teacher Park"]
        if lang_code == "EN"
        else ["김교사", "이교사", "박교사"]
    )
    default_teachers_data = {
        default_teachers[0]: [
            {
                "q_type": "MC",
                "diff": "easy",
                "A": 90,
                "B": 85,
                "C": 75,
                "D": 65,
                "E": 55,
            },
            {
                "q_type": "MC",
                "diff": "mid",
                "A": 80,
                "B": 70,
                "C": 60,
                "D": 50,
                "E": 40,
            },
            {
                "q_type": "MC",
                "diff": "hard",
                "A": 65,
                "B": 55,
                "C": 45,
                "D": 35,
                "E": 25,
            },
            {
                "q_type": "CR",
                "diff": "easy",
                "A": 85,
                "B": 75,
                "C": 65,
                "D": 50,
                "E": 35,
            },
            {
                "q_type": "CR",
                "diff": "hard",
                "A": 60,
                "B": 45,
                "C": 30,
                "D": 20,
                "E": 10,
            },
        ],
        default_teachers[1]: [
            {
                "q_type": "MC",
                "diff": "easy",
                "A": 95,
                "B": 85,
                "C": 70,
                "D": 60,
                "E": 50,
            },
            {
                "q_type": "MC",
                "diff": "mid",
                "A": 85,
                "B": 75,
                "C": 65,
                "D": 45,
                "E": 35,
            },
            {
                "q_type": "MC",
                "diff": "hard",
                "A": 70,
                "B": 50,
                "C": 40,
                "D": 30,
                "E": 20,
            },
            {
                "q_type": "CR",
                "diff": "easy",
                "A": 90,
                "B": 80,
                "C": 70,
                "D": 55,
                "E": 40,
            },
            {
                "q_type": "CR",
                "diff": "hard",
                "A": 55,
                "B": 40,
                "C": 25,
                "D": 15,
                "E": 5,
            },
        ],
        default_teachers[2]: [
            {
                "q_type": "MC",
                "diff": "easy",
                "A": 90,
                "B": 80,
                "C": 70,
                "D": 60,
                "E": 50,
            },
            {
                "q_type": "MC",
                "diff": "mid",
                "A": 80,
                "B": 75,
                "C": 60,
                "D": 50,
                "E": 35,
            },
            {
                "q_type": "MC",
                "diff": "hard",
                "A": 65,
                "B": 50,
                "C": 35,
                "D": 25,
                "E": 15,
            },
            {
                "q_type": "CR",
                "diff": "easy",
                "A": 85,
                "B": 70,
                "C": 60,
                "D": 45,
                "E": 30,
            },
            {
                "q_type": "CR",
                "diff": "hard",
                "A": 50,
                "B": 35,
                "C": 20,
                "D": 10,
                "E": 5,
            },
        ],
    }

    rounds_data = {}
    for r in range(1, 9):
        rounds_data[r] = {
            "has_essay": True,
            "teacher_names": list(default_teachers),
            "groups_config": [dict(g) for g in default_groups_config],
            "teachers_data": {
                t_name: [dict(rec) for rec in recs]
                for t_name, recs in default_teachers_data.items()
            },
            "teachers_status": {
                default_teachers[0]: True,
                default_teachers[1]: True,
                default_teachers[2]: False,
            },
        }
    return rounds_data


# 세션 상태 및 파일 DB 로드
saved_round, saved_rounds_data = load_app_state()
if saved_rounds_data is not None:
    st.session_state.current_round = saved_round
    st.session_state.rounds_data = saved_rounds_data
else:
    if "rounds_data" not in st.session_state:
        st.session_state.current_round = 1
        st.session_state.rounds_data = create_default_rounds_data()
        save_app_state(st.session_state.current_round, st.session_state.rounds_data)

# 사이드바 공유 DB 상태 및 새로고침 버튼
st.sidebar.caption(f"{t('shared_data_info')}")
if st.sidebar.button(t("sync_btn"), key="sync_data_btn", use_container_width=True):
    sr, srd = load_app_state()
    if srd is not None:
        st.session_state.current_round = sr
        st.session_state.rounds_data = srd
        st.sidebar.success(t("sync_success"))
        st.rerun()

st.sidebar.divider()

# =========================================================
# 관리자 (Admin) 리셋 메뉴
# =========================================================
with st.sidebar.expander(t("admin_menu")):
    admin_input_pwd = st.text_input(
        t("admin_pwd"), type="password", key="admin_pwd_widget"
    )
    if st.button(t("admin_reset_btn"), key="admin_reset_action_btn", type="primary"):
        if admin_input_pwd == "admin" or admin_input_pwd == "1234":
            st.session_state.current_round = 1
            st.session_state.rounds_data = create_default_rounds_data()
            save_app_state(st.session_state.current_round, st.session_state.rounds_data)
            st.success(t("admin_reset_success"))
            st.rerun()
        else:
            st.error(t("admin_pwd_wrong"))


st.title(t("title"))

levels = ["A", "B", "C", "D", "E"]
cut_boundaries = ["A/B", "B/C", "C/D", "D/E", f"E/{t('below_e')}"]
level_to_boundary = dict(zip(levels, cut_boundaries))

current_round = st.session_state.current_round
active_round_data = st.session_state.rounds_data[current_round]


# --- 유효성 검증 함수 ---
def validate_teacher_input(df_edit, lang_code):
    errors = []
    q_type_col = t("item_type_col")
    diff_col = t("diff_col")

    for _, row in df_edit.iterrows():
        g_name = f"{row[q_type_col]}-{row[diff_col]}"
        for i in range(len(levels) - 1):
            curr_l, next_l = levels[i], levels[i + 1]
            if row[curr_l] < row[next_l]:
                if lang_code == "KO":
                    errors.append(
                        f"[{g_name}] 상위수준({curr_l}: {row[curr_l]}%)이"
                        f" 하위수준({next_l}: {row[next_l]}%)보다 낮음"
                    )
                else:
                    errors.append(
                        f"[{g_name}] Higher level ({curr_l}: {row[curr_l]}%) is"
                        f" lower than lower level ({next_l}: {row[next_l]}%)"
                    )

    for q_type in df_edit[q_type_col].unique():
        sub = df_edit[df_edit[q_type_col] == q_type]
        diff_names = [t("easy"), t("moderate"), t("hard")]
        diffs = [d for d in diff_names if d in sub[diff_col].values]
        for i in range(len(diffs) - 1):
            easier = sub[sub[diff_col] == diffs[i]].iloc[0]
            harder = sub[sub[diff_col] == diffs[i + 1]].iloc[0]
            for lvl in levels:
                if easier[lvl] < harder[lvl]:
                    if lang_code == "KO":
                        errors.append(
                            f"[{q_type} {lvl}수준] {diffs[i]}({easier[lvl]}%)가"
                            f" {diffs[i+1]}({harder[lvl]}%)보다 낮음"
                        )
                    else:
                        errors.append(
                            f"[{q_type} Level {lvl}] {diffs[i]} ({easier[lvl]}%)"
                            f" is lower than {diffs[i+1]} ({harder[lvl]}%)"
                        )
    return errors


def highlight_gaps(row):
    styles = [""] * len(row)
    for i in range(len(levels) - 1):
        hi, lo = levels[i], levels[i + 1]
        if hi in row and lo in row and (row[hi] - row[lo]) >= 20:
            idx = row.index.get_loc(lo)
            styles[idx] = (
                "background-color: #ffcccc; color: #cc0000; font-weight: bold;"
            )
    return styles


# --- 상단 탭 6개 구성 ---
tab_setup, tab1, tab2, tab3, tab4, tab_comparison = st.tabs([
    t("tab_setup"),
    t("tab_entry"),
    t("tab_lookup"),
    t("tab_category"),
    t("tab_final"),
    t("tab_comparison"),
])

# =========================================================
# TAB SETUP: 시험 기본 세팅 (라운드 1~8 선택 및 설정)
# =========================================================
with tab_setup:
    st.subheader(t("setup_sub"))
    st.caption(t("setup_cap"))

    r_col1, r_col2 = st.columns([2, 2])
    with r_col1:
        selected_r = st.selectbox(
            t("select_round"),
            options=list(range(1, 9)),
            index=st.session_state.current_round - 1,
            format_func=lambda r: f"{t('round_label')} {r}",
            key="active_round_selector_widget",
        )
        if selected_r != st.session_state.current_round:
            st.session_state.current_round = selected_r
            save_app_state(st.session_state.current_round, st.session_state.rounds_data)
            st.rerun()

        current_round = st.session_state.current_round
        active_round_data = st.session_state.rounds_data[current_round]

    with r_col2:
        st.write("")
        if current_round > 1:
            if st.button(
                t("copy_prev_round_btn"),
                key=f"copy_prev_round_btn_{current_round}",
                use_container_width=True,
            ):
                prev_r_data = st.session_state.rounds_data[current_round - 1]
                st.session_state.rounds_data[current_round] = {
                    "has_essay": prev_r_data["has_essay"],
                    "teacher_names": list(prev_r_data["teacher_names"]),
                    "groups_config": [dict(g) for g in prev_r_data["groups_config"]],
                    "teachers_data": {
                        t_name: [dict(rec) for rec in recs]
                        for t_name, recs in prev_r_data["teachers_data"].items()
                    },
                    "teachers_status": dict(prev_r_data["teachers_status"]),
                }
                save_app_state(st.session_state.current_round, st.session_state.rounds_data)
                st.success(t("copy_success"))
                st.rerun()

    st.markdown(
        f"#### 🎯 {t('current_round_info')} `{t('round_label')} {current_round}`"
    )
    st.divider()

    col_s1, col_s2 = st.columns([1, 1])

    with col_s1:
        st.markdown(f"#### {t('item_teacher_header')}")
        has_essay_input = st.checkbox(
            t("include_essay"),
            value=active_round_data["has_essay"],
            key=f"has_essay_checkbox_r{current_round}",
        )
        teacher_count = st.number_input(
            t("num_teachers"),
            min_value=1,
            max_value=20,
            value=len(active_round_data["teacher_names"]),
            step=1,
            key=f"teacher_count_input_r{current_round}",
        )

        teacher_names_input = []
        st.markdown(f"**{t('teacher_names')}**")
        name_cols = st.columns(2)
        for idx in range(teacher_count):
            c = name_cols[idx % 2]
            default_name = (
                active_round_data["teacher_names"][idx]
                if idx < len(active_round_data["teacher_names"])
                else f"{t('teacher_label')} {idx+1}"
            )
            t_name = c.text_input(
                f"{t('teacher_label')} {idx+1}",
                value=default_name,
                key=f"tname_input_r{current_round}_{idx}",
            )
            teacher_names_input.append(t_name)

    with col_s2:
        st.markdown(f"#### {t('score_sums_header')}")

        def get_existing_score(q_type, diff, default_val):
            for item in active_round_data["groups_config"]:
                if item["q_type"] == q_type and item["diff"] == diff:
                    return float(item["score_sum"])
            return float(default_val)

        st.markdown(f"##### {t('mc_scores')}")
        c_mc1, c_mc2, c_mc3 = st.columns(3)
        mc_easy_score = c_mc1.number_input(
            t("easy_sum"),
            value=get_existing_score("MC", "easy", 25.0),
            step=0.5,
            format="%.1f",
            key=f"mc_easy_score_input_r{current_round}",
        )
        mc_mid_score = c_mc2.number_input(
            t("mid_sum"),
            value=get_existing_score("MC", "mid", 35.0),
            step=0.5,
            format="%.1f",
            key=f"mc_mid_score_input_r{current_round}",
        )
        mc_hard_score = c_mc3.number_input(
            t("hard_sum"),
            value=get_existing_score("MC", "hard", 15.0),
            step=0.5,
            format="%.1f",
            key=f"mc_hard_score_input_r{current_round}",
        )

        essay_easy_score, essay_mid_score, essay_hard_score = 0.0, 0.0, 0.0
        if has_essay_input:
            st.markdown(f"##### {t('essay_scores')}")
            c_es1, c_es2, c_es3 = st.columns(3)
            essay_easy_score = c_es1.number_input(
                t("easy_sum"),
                value=get_existing_score("CR", "easy", 10.0),
                step=0.5,
                format="%.1f",
                key=f"essay_easy_score_input_r{current_round}",
            )
            essay_mid_score = c_es2.number_input(
                t("mid_sum"),
                value=get_existing_score("CR", "mid", 0.0),
                step=0.5,
                format="%.1f",
                key=f"essay_mid_score_input_r{current_round}",
            )
            essay_hard_score = c_es3.number_input(
                t("hard_sum"),
                value=get_existing_score("CR", "hard", 15.0),
                step=0.5,
                format="%.1f",
                key=f"essay_hard_score_input_r{current_round}",
            )

        total_sum_score = (
            mc_easy_score
            + mc_mid_score
            + mc_hard_score
            + (
                essay_easy_score + essay_mid_score + essay_hard_score
                if has_essay_input
                else 0.0
            )
        )
        st.metric(
            t("total_points"),
            f"{total_sum_score:.1f} {t('pts')}",
            delta=t("match_100")
            if abs(total_sum_score - 100.0) < 0.01
            else t("mismatch_100"),
        )

    st.divider()
    st.caption(t("sync_all_rounds_notice"))
    if st.button(t("apply_btn"), type="primary", key=f"apply_config_btn_r{current_round}"):
        new_cfg = [
            {
                "q_type": "MC",
                "diff": "easy",
                "dept": "General/1/General",
                "score_sum": mc_easy_score,
            },
            {
                "q_type": "MC",
                "diff": "mid",
                "dept": "General/1/General",
                "score_sum": mc_mid_score,
            },
            {
                "q_type": "MC",
                "diff": "hard",
                "dept": "General/1/General",
                "score_sum": mc_hard_score,
            },
        ]
        if has_essay_input:
            if essay_easy_score > 0:
                new_cfg.append({
                    "q_type": "CR",
                    "diff": "easy",
                    "dept": "General/1/General",
                    "score_sum": essay_easy_score,
                })
            if essay_mid_score > 0:
                new_cfg.append({
                    "q_type": "CR",
                    "diff": "mid",
                    "dept": "General/1/General",
                    "score_sum": essay_mid_score,
                })
            if essay_hard_score > 0:
                new_cfg.append({
                    "q_type": "CR",
                    "diff": "hard",
                    "dept": "General/1/General",
                    "score_sum": essay_hard_score,
                })

        # 1~8라운드 전체에 시험 구조, 배점합, 교사 목록 동시 반영
        for r in range(1, 9):
            r_data = st.session_state.rounds_data[r]
            r_data["has_essay"] = has_essay_input
            r_data["teacher_names"] = teacher_names_input
            r_data["groups_config"] = [dict(g) for g in new_cfg]

            new_t_data = {}
            new_t_status = {}
            for t_name in teacher_names_input:
                existing_t_records = r_data["teachers_data"].get(t_name, [])
                existing_dict = {
                    (rec["q_type"], rec["diff"]): rec for rec in existing_t_records
                }
                new_t_status[t_name] = r_data["teachers_status"].get(t_name, False)

                new_t_data[t_name] = []
                for g in new_cfg:
                    key = (g["q_type"], g["diff"])
                    if key in existing_dict:
                        new_t_data[t_name].append(existing_dict[key])
                    else:
                        new_t_data[t_name].append({
                            "q_type": g["q_type"],
                            "diff": g["diff"],
                            "A": 85,
                            "B": 75,
                            "C": 65,
                            "D": 50,
                            "E": 40,
                        })
            r_data["teachers_data"] = new_t_data
            r_data["teachers_status"] = new_t_status

        save_app_state(st.session_state.current_round, st.session_state.rounds_data)
        st.success(t("apply_success"))
        st.rerun()

# =========================================================
# TAB 1: 교사별 정답률 입력 (현재 활성화된 라운드 기준)
# =========================================================
with tab1:
    st.subheader(f"{t('entry_sub')} ({t('round_label')} {current_round})")

    if not active_round_data["teachers_data"]:
        st.warning(t("no_teachers"))
    else:
        current_teacher = st.selectbox(
            t("select_teacher"),
            list(active_round_data["teachers_data"].keys()),
            key=f"teacher_selector_r{current_round}",
        )

        is_sub = active_round_data["teachers_status"].get(current_teacher, False)
        status_str = t("submitted") if is_sub else t("pending")

        head_t1, head_t2 = st.columns([3, 2])
        with head_t1:
            st.markdown(
                f"**{t('selected_teacher')} `{current_teacher}`** | **{t('status_info')}** {status_str}"
            )
        with head_t2:
            sub_col1, sub_col2 = st.columns(2)
            with sub_col1:
                if st.button(
                    t("mark_submitted_btn"),
                    key=f"submit_btn_r{current_round}_{current_teacher}",
                    type="primary",
                    use_container_width=True,
                ):
                    active_round_data["teachers_status"][current_teacher] = True
                    save_app_state(st.session_state.current_round, st.session_state.rounds_data)
                    st.success(f"✅ {current_teacher}: {t('submitted')}")
                    st.rerun()
            with sub_col2:
                if st.button(
                    t("mark_pending_btn"),
                    key=f"pending_btn_r{current_round}_{current_teacher}",
                    use_container_width=True,
                ):
                    active_round_data["teachers_status"][current_teacher] = False
                    save_app_state(st.session_state.current_round, st.session_state.rounds_data)
                    st.info(f"🔄 {current_teacher}: {t('pending')}")
                    st.rerun()

        cfg_list = active_round_data["groups_config"]
        t_records = active_round_data["teachers_data"][current_teacher]

        display_rows = []
        for g in cfg_list:
            matching_t = next(
                (
                    r
                    for r in t_records
                    if r["q_type"] == g["q_type"] and r["diff"] == g["diff"]
                ),
                {"A": 85, "B": 75, "C": 65, "D": 50, "E": 40},
            )
            display_rows.append({
                "q_type_code": g["q_type"],
                "diff_code": g["diff"],
                t("item_type_col"): ITEM_TYPE_MAP[g["q_type"]],
                t("diff_col"): DIFF_MAP[g["diff"]],
                t("track_dept"): g.get("dept", "General/1/General"),
                t("score_sum_col"): g["score_sum"],
                "A": matching_t["A"],
                "B": matching_t["B"],
                "C": matching_t["C"],
                "D": matching_t["D"],
                "E": matching_t["E"],
            })

        display_df = pd.DataFrame(display_rows)

        st.caption(t("edit_hint"))
        edited = st.data_editor(
            display_df,
            column_config={
                "q_type_code": None,
                "diff_code": None,
                t("item_type_col"): st.column_config.TextColumn(disabled=True),
                t("diff_col"): st.column_config.TextColumn(disabled=True),
                t("track_dept"): st.column_config.TextColumn(disabled=True),
                t("score_sum_col"): st.column_config.NumberColumn(
                    format=f"%.1f {t('pts')}", disabled=True
                ),
                "A": st.column_config.NumberColumn(min_value=0, max_value=100, step=5),
                "B": st.column_config.NumberColumn(min_value=0, max_value=100, step=5),
                "C": st.column_config.NumberColumn(min_value=0, max_value=100, step=5),
                "D": st.column_config.NumberColumn(min_value=0, max_value=100, step=5),
                "E": st.column_config.NumberColumn(min_value=0, max_value=100, step=5),
            },
            use_container_width=True,
            key=f"editor_r{current_round}_{current_teacher}",
        )

        updated_records = []
        for _, r in edited.iterrows():
            updated_records.append({
                "q_type": r["q_type_code"],
                "diff": r["diff_code"],
                "A": r["A"],
                "B": r["B"],
                "C": r["C"],
                "D": r["D"],
                "E": r["E"],
            })

        if active_round_data["teachers_data"][current_teacher] != updated_records:
            active_round_data["teachers_data"][current_teacher] = updated_records
            active_round_data["teachers_status"][current_teacher] = True
            save_app_state(st.session_state.current_round, st.session_state.rounds_data)

        errors = validate_teacher_input(edited, lang_code)
        if errors:
            st.error(t("errors_detected"))
            for e in errors:
                st.write(f"- :red[{e}]")
        else:
            st.success(t("passed_constraints"))

# =========================================================
# TAB 2: [통합산출] 교사별입력정보조회 (현재 활성화된 라운드 기준)
# =========================================================
with tab2:
    score_map = {
        (g["q_type"], g["diff"]): g["score_sum"]
        for g in active_round_data["groups_config"]
    }
    dept_map = {
        (g["q_type"], g["diff"]): g.get("dept", "General/1/General")
        for g in active_round_data["groups_config"]
    }

    rows_all = []
    for t_name, recs in active_round_data["teachers_data"].items():
        is_sub = active_round_data["teachers_status"].get(t_name, False)
        status_label = t("submitted") if is_sub else t("pending")

        for r in recs:
            key = (r["q_type"], r["diff"])
            configured_score = score_map.get(key, 0.0)
            configured_dept = dept_map.get(key, "General/1/General")

            rows_all.append({
                t("item_type_col"): ITEM_TYPE_MAP[r["q_type"]],
                t("diff_col"): DIFF_MAP[r["diff"]],
                t("track_dept"): configured_dept,
                t("teacher_label"): t_name,
                t("status_col"): status_label,
                t("score_sum_col"): f"{configured_score:.1f}",
                "A": r["A"],
                "B": r["B"],
                "C": r["C"],
                "D": r["D"],
                "E": r["E"],
            })

    df_lookup = pd.DataFrame(rows_all)
    if not df_lookup.empty:
        diff_order_map = {t("easy"): 1, t("moderate"): 2, t("hard"): 3}
        df_lookup["diff_rank"] = df_lookup[t("diff_col")].map(diff_order_map)
        df_lookup = df_lookup.sort_values(
            by=[t("item_type_col"), "diff_rank", t("teacher_label")]
        ).drop(columns=["diff_rank"])

    submitted_count = sum(1 for is_sub in active_round_data["teachers_status"].values() if is_sub)
    total_teacher_count = len(active_round_data["teacher_names"])

    head_c1, head_c2, head_c3 = st.columns([4, 2, 2])
    with head_c1:
        st.subheader(f"{t('lookup_sub')} ({t('round_label')} {current_round}) Total {len(df_lookup)}")
        st.caption(f"📌 {t('submitted_teachers_count')} **{submitted_count} / {total_teacher_count}**")
    with head_c2:
        search_teacher = st.text_input(
            t("filter_teacher"),
            placeholder=t("filter_placeholder"),
            key=f"search_teacher_input_r{current_round}",
        )
    with head_c3:
        st.write("")
        buf_teacher = io.BytesIO()
        with pd.ExcelWriter(buf_teacher, engine="openpyxl") as writer:
            df_lookup.to_excel(writer, index=False, sheet_name="TeacherEntries")
        st.download_button(
            label=t("export_excel"),
            data=buf_teacher.getvalue(),
            file_name=f"Estimated_Cut_Score_Teacher_Entries_R{current_round}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key=f"dl_teacher_entries_r{current_round}",
        )

    filtered_df = df_lookup.copy()
    if search_teacher and not filtered_df.empty:
        filtered_df = filtered_df[
            filtered_df[t("teacher_label")].str.contains(
                search_teacher, case=False
            )
        ]

    if not filtered_df.empty:
        styled_lookup = filtered_df.style.apply(highlight_gaps, axis=1)
        st.dataframe(styled_lookup, use_container_width=True, height=450)
    else:
        st.info(t("no_data"))

# =========================================================
# TAB 3: [통합산출] 문항범주별조회 (실제 입력 완료한 교사만 포함)
# =========================================================
with tab3:
    submitted_teachers = [
        t_name
        for t_name, is_sub in active_round_data["teachers_status"].items()
        if is_sub
    ]

    st.subheader(
        f"{t('cat_sub')} ({t('round_label')} {current_round}) Total {len(active_round_data['groups_config'])}"
    )

    if not submitted_teachers:
        st.warning(t("no_submitted_warning"))
    else:
        st.caption(
            f"ℹ️ {t('calc_included_info')} **{len(submitted_teachers)} / {len(active_round_data['teacher_names'])}** "
            f"({', '.join(submitted_teachers)})"
        )

        substats = [t("mean"), t("std_dev"), t("min"), t("max")]
        category_stat_rows = []

        for g in active_round_data["groups_config"]:
            q_type_code, diff_code = g["q_type"], g["diff"]
            row_label = f"{ITEM_TYPE_MAP[q_type_code]} ({DIFF_MAP[diff_code]})"

            row_data = {}
            for lvl in levels:
                vals = []
                for t_name in submitted_teachers:
                    recs = active_round_data["teachers_data"].get(t_name, [])
                    for r in recs:
                        if r["q_type"] == q_type_code and r["diff"] == diff_code:
                            vals.append(r[lvl])

                if vals:
                    mean_v = np.mean(vals)
                    std_v = np.std(vals, ddof=1) if len(vals) > 1 else 0.0
                    min_v = np.min(vals)
                    max_v = np.max(vals)
                else:
                    mean_v, std_v, min_v, max_v = 0.0, 0.0, 0.0, 0.0

                row_data[(lvl, t("mean"))] = f"{mean_v:.2f}"
                row_data[(lvl, t("std_dev"))] = f"{std_v:.2f}"
                row_data[(lvl, t("min"))] = f"{min_v:.0f}"
                row_data[(lvl, t("max"))] = f"{max_v:.0f}"

            category_stat_rows.append((row_label, row_data))

        multi_cols = pd.MultiIndex.from_tuples(
            [(lvl, stat) for lvl in levels for stat in substats],
            names=[t("achieve_level"), t("stat_category")],
        )

        data_matrix = [r_data for _, r_data in category_stat_rows]
        df_categories = pd.DataFrame(data_matrix, columns=multi_cols)
        df_categories.insert(
            0,
            (t("cat_item_col"), ""),
            [r_label for r_label, _ in category_stat_rows],
        )
        df_categories.set_index((t("cat_item_col"), ""), inplace=True)
        df_categories.index.name = t("cat_item_col")

        cat_c1, cat_c2 = st.columns([6, 2])
        with cat_c2:
            buf_cat = io.BytesIO()
            with pd.ExcelWriter(buf_cat, engine="openpyxl") as writer:
                df_categories.to_excel(
                    writer, sheet_name="CategoryStats", merge_cells=True
                )
            st.download_button(
                label=t("export_excel"),
                data=buf_cat.getvalue(),
                file_name=f"Estimated_Cut_Score_Category_Stats_R{current_round}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key=f"dl_category_stats_r{current_round}",
            )

        st.dataframe(df_categories, use_container_width=True, height=350)

# =========================================================
# TAB 4: [통합산출] 예상추정분할점수조회 (실제 입력 완료한 교사만 반영)
# =========================================================
with tab4:
    submitted_teachers = [
        t_name
        for t_name, is_sub in active_round_data["teachers_status"].items()
        if is_sub
    ]

    st.subheader(f"{t('final_sub')} ({t('round_label')} {current_round})")

    if not submitted_teachers:
        st.warning(t("no_submitted_warning"))
    else:
        st.caption(
            f"ℹ️ {t('calc_included_info')} **{len(submitted_teachers)} / {len(active_round_data['teacher_names'])}** "
            f"({', '.join(submitted_teachers)})"
        )

        cfg_dict = {
            (g["q_type"], g["diff"]): g["score_sum"]
            for g in active_round_data["groups_config"]
        }
        teacher_cut_matrix = {b: [] for b in cut_boundaries}

        for t_name in submitted_teachers:
            recs = active_round_data["teachers_data"].get(t_name, [])
            for lvl in levels:
                b_name = level_to_boundary[lvl]
                teacher_score = sum(
                    r[lvl] / 100.0 * cfg_dict.get((r["q_type"], r["diff"]), 0.0)
                    for r in recs
                )
                teacher_cut_matrix[b_name].append(teacher_score)

        stat_rows_canonical = ["mean", "std_dev", "min", "max"]
        result_table = []

        for stat_key in stat_rows_canonical:
            stat_label = t(stat_key)
            row_vals = {t("category_col"): stat_label}
            for b in cut_boundaries:
                scores = teacher_cut_matrix[b]
                if scores:
                    if stat_key == "mean":
                        val = np.mean(scores)
                    elif stat_key == "std_dev":
                        val = np.std(scores, ddof=1) if len(scores) > 1 else 0.0
                    elif stat_key == "min":
                        val = np.min(scores)
                    elif stat_key == "max":
                        val = np.max(scores)
                else:
                    val = 0.0
                row_vals[b] = f"{val:.2f}"
            result_table.append(row_vals)

        df_final_cut = pd.DataFrame(result_table)

        multi_cols_final = pd.MultiIndex.from_tuples(
            [(t("category_col"), "")]
            + [(t("achieve_level"), b) for b in cut_boundaries]
        )
        df_final_cut_multi = df_final_cut.copy()
        df_final_cut_multi.columns = multi_cols_final
        df_final_cut_multi.set_index((t("category_col"), ""), inplace=True)
        df_final_cut_multi.index.name = t("category_col")

        head4_1, head4_2 = st.columns([5, 3])
        with head4_2:
            btn_col1, btn_col2, btn_col3 = st.columns([1.3, 1, 0.8])
            with btn_col1:
                buf_all = io.BytesIO()
                with pd.ExcelWriter(buf_all, engine="openpyxl") as writer:
                    df_final_cut.to_excel(
                        writer, index=False, sheet_name="AllSubjectsEstimatedCutScores"
                    )
                st.download_button(
                    t("all_subjects_excel"),
                    data=buf_all.getvalue(),
                    file_name=f"All_Subjects_Estimated_Cut_Scores_R{current_round}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key=f"dl_all_subjects_cut_r{current_round}",
                )
            with btn_col2:
                buf_single = io.BytesIO()
                with pd.ExcelWriter(buf_single, engine="openpyxl") as writer:
                    df_final_cut_multi.to_excel(
                        writer, sheet_name="EstimatedCutScores", merge_cells=True
                    )
                st.download_button(
                    t("export_excel_short"),
                    data=buf_single.getvalue(),
                    file_name=f"Estimated_Cut_Scores_R{current_round}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key=f"dl_single_subject_cut_r{current_round}",
                )
            with btn_col3:
                if st.button(t("print_btn"), key=f"print_cut_scores_btn_r{current_round}"):
                    st.components.v1.html(
                        "<script>window.parent.print();</script>", height=0
                    )

        st.dataframe(df_final_cut_multi, use_container_width=True, height=220)

        st.divider()
        st.markdown(f"#### {t('final_cut_header')} - `{t('round_label')} {current_round}`")
        m_cols = st.columns(5)
        mean_label = t("mean")
        for i, b in enumerate(cut_boundaries):
            avg_score = float(
                df_final_cut.loc[
                    df_final_cut[t("category_col")] == mean_label, b
                ].iloc[0]
            )
            m_cols[i].metric(
                label=f"{b} {t('cut_score_label')}",
                value=f"{avg_score:.1f} {t('pts')}",
            )

# =========================================================
# TAB 5: [통합산출] 라운드별 비교 (실제 입력 완료한 교사 기준 비교)
# =========================================================
with tab_comparison:
    st.subheader(t("comp_sub"))
    st.caption(t("comp_cap"))

    round_cut_scores = {}
    round_submitted_counts = {}

    for r in range(1, 9):
        r_data = st.session_state.rounds_data[r]
        submitted_ts = [
            t_name for t_name, is_sub in r_data["teachers_status"].items() if is_sub
        ]
        round_submitted_counts[r] = len(submitted_ts)

        cfg_dict = {
            (g["q_type"], g["diff"]): g["score_sum"]
            for g in r_data["groups_config"]
        }
        cut_matrix = {b: [] for b in cut_boundaries}

        if submitted_ts:
            for t_name in submitted_ts:
                recs = r_data["teachers_data"].get(t_name, [])
                for lvl in levels:
                    b_name = level_to_boundary[lvl]
                    score = sum(
                        r_rec[lvl] / 100.0 * cfg_dict.get((r_rec["q_type"], r_rec["diff"]), 0.0)
                        for r_rec in recs
                    )
                    cut_matrix[b_name].append(score)

            round_cut_scores[r] = {
                b: np.mean(cut_matrix[b]) if cut_matrix[b] else 0.0
                for b in cut_boundaries
            }
        else:
            round_cut_scores[r] = {b: 0.0 for b in cut_boundaries}

    matrix_rows = []
    for b in cut_boundaries:
        row = {t("boundary_col"): b}
        for r in range(1, 9):
            if round_submitted_counts[r] > 0:
                row[f"{t('round_label')} {r}"] = f"{round_cut_scores[r][b]:.2f} {t('pts')}"
            else:
                row[f"{t('round_label')} {r}"] = "-"
        matrix_rows.append(row)

    df_comparison = pd.DataFrame(matrix_rows)
    df_comparison.set_index(t("boundary_col"), inplace=True)

    head_comp1, head_comp2 = st.columns([6, 2])
    with head_comp1:
        st.markdown(f"### {t('comp_matrix_title')}")
    with head_comp2:
        buf_comp = io.BytesIO()
        with pd.ExcelWriter(buf_comp, engine="openpyxl") as writer:
            df_comparison.to_excel(writer, sheet_name="RoundComparison")
        st.download_button(
            label=t("export_excel"),
            data=buf_comp.getvalue(),
            file_name="Estimated_Cut_Scores_Round_Comparison.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="dl_round_comparison_excel",
        )

    st.dataframe(df_comparison, use_container_width=True)

    st.divider()
    st.markdown(f"### {t('comp_chart_title')}")

    chart_data = {}
    for b in cut_boundaries:
        chart_data[b] = [round_cut_scores[r][b] for r in range(1, 9)]

    chart_df = pd.DataFrame(
        chart_data, index=[f"{t('round_label')} {r}" for r in range(1, 9)]
    )
    st.line_chart(chart_df, height=350)

    st.divider()
    st.markdown(f"### {t('comp_delta_title')}")

    delta_cols = st.columns(5)
    for idx, b in enumerate(cut_boundaries):
        r1_val = round_cut_scores[1][b]
        curr_r_val = round_cut_scores[current_round][b]
        diff_val = curr_r_val - r1_val
        delta_cols[idx].metric(
            label=f"{b} ({t('round_label')} {current_round})",
            value=f"{curr_r_val:.1f} {t('pts')}" if round_submitted_counts[current_round] > 0 else "-",
            delta=f"{diff_val:+.1f} {t('pts')} (vs {t('round_label')} 1)" if round_submitted_counts[1] > 0 and round_submitted_counts[current_round] > 0 else None,
        )