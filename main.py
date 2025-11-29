import math
import streamlit as st

# ---- 기본 설정 ----
st.set_page_config(page_title="다기능 계산기", page_icon="🧮", layout="centered")
st.title("🧮 다기능 계산기 (Streamlit)")

st.write(
    """
사칙연산, 모듈러 연산, 지수 연산, 로그 연산을 지원하는 간단한 웹 계산기입니다.  
왼쪽 사이드바에서 연산 종류를 선택하고, 아래에 숫자를 입력해 보세요.
"""
)

# ---- 사이드바: 연산 선택 ----
operation = st.sidebar.selectbox(
    "연산을 선택하세요",
    (
        "덧셈 (+)",
        "뺄셈 (-)",
        "곱셈 (×)",
        "나눗셈 (÷)",
        "모듈러 (a mod b)",
        "지수 (a^b)",
        "로그 (log_b(a))",
    ),
)

st.sidebar.info("원하는 연산을 선택하면 아래에 해당 입력창이 표시됩니다.")


def safe_float_input(label: str, key: str):
    """숫자 입력용 헬퍼 함수 (빈 값/오류 최소화용)."""
    return st.number_input(label, key=key)


# ---- 연산별 UI & 계산 ----
result = None
error_message = None

if operation in ["덧셈 (+)", "뺄셈 (-)", "곱셈 (×)", "나눗셈 (÷)", "모듈러 (a mod b)", "지수 (a^b)"]:
    a = safe_float_input("첫 번째 숫자 (a)", key="a")
    b = safe_float_input("두 번째 숫자 (b)", key="b")

    if st.button("계산하기"):
        try:
            if operation == "덧셈 (+)":
                result = a + b
            elif operation == "뺄셈 (-)":
                result = a - b
            elif operation == "곱셈 (×)":
                result = a * b
            elif operation == "나눗셈 (÷)":
                if b == 0:
                    raise ZeroDivisionError("0으로 나눌 수 없습니다.")
                result = a / b
            elif operation == "모듈러 (a mod b)":
                if b == 0:
                    raise ZeroDivisionError("0으로 나머지 연산을 할 수 없습니다.")
                result = a % b
            elif operation == "지수 (a^b)":
                # math.pow 대신 ** 사용 (정수/실수 모두 자연스럽게 처리)
                result = a ** b

        except ZeroDivisionError as e:
            error_message = str(e)
        except OverflowError:
            error_message = "값이 너무 커서 계산할 수 없습니다."
        except Exception as e:
            error_message = f"알 수 없는 오류가 발생했습니다: {e}"

elif operation == "로그 (log_b(a))":
    st.markdown("**로그 연산:** `log_b(a)` 형태로 계산합니다.")
    a = safe_float_input("밑이 될 수 (base = b)", key="log_base")
    x = safe_float_input("로그를 취할 값 (a)", key="log_value")

    # 자주 쓰는 밑 선택 (선택 시 base 무시하고 해당 값 사용)
    with st.expander("자주 쓰는 밑 빠르게 선택하기"):
        common_base = st.radio(
            "밑 선택 (선택하면 위의 '밑이 될 수' 값 대신 사용됩니다)",
            ["직접 입력값 사용", "자연로그 (e)", "상용로그 (10)"],
            index=0,
        )
        if common_base == "자연로그 (e)":
            a = math.e
        elif common_base == "상용로그 (10)":
            a = 10.0

    if st.button("로그 계산하기"):
        try:
            # 로그의 정의역 체크
            if x <= 0:
                raise ValueError("로그 대상 값(a)은 0보다 커야 합니다.")
            if a <= 0 or a == 1:
                raise ValueError("밑(b)은 0보다 크고 1과 달라야 합니다.")

            # 밑이 e 또는 10인 경우 특별히 처리해도 되고, 일반 공식 사용해도 됨
            # 여기서는 일반적인 로그 공식 사용: log_b(a) = ln(a) / ln(b)
            result = math.log(x, a)

        except ValueError as e:
            error_message = str(e)
        except Exception as e:
            error_message = f"알 수 없는 오류가 발생했습니다: {e}"

# ---- 결과 출력 ----
st.markdown("---")

if error_message:
    st.error(error_message)
elif result is not None:
    st.success(f"계산 결과: **{result}**")

# ---- 푸터 ----
st.caption(
    "Made with ❤️ using Streamlit. "
    "이 코드를 깃허브에 올려 버전 관리하고, 필요하면 기능을 더 추가해 보세요!"
)
