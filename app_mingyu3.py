import gradio as gr


def calculate_fee(total_amount, num_people, tip_percent):
    # 인원 수가 0 이하인 경우 방어 코드
    if num_people <= 0:
        return 0, 0

    # 1. 팁 포함 전체 금액 계산 (소수점 버림)
    total_with_tip = int(total_amount * (1 + tip_percent / 100))

    # 2. 1인당 금액 계산 후 100단위 반올림
    per_person_raw = total_with_tip / num_people
    per_person_final = round(per_person_raw, -2)

    return int(per_person_final), total_with_tip


# Gradio Blocks 레이아웃 설정 (Interface 대신 Blocks로 전체 구성)
with gr.Blocks() as demo:
    # 화면 상단 중앙 제목 (굵게 표기)
    gr.Markdown("<center><b><h2>모임 회비 관리 계산기</h2></b></center>")

    # 제목 아래 설명 문구 (작은 크기, 굵지 않게)
    gr.Markdown("총 금액, 인원 수, 팁 비율을 입력하여 1인당 부담할 금액을 계산합니다.")

    with gr.Row():
        # 입력 영역
        with gr.Column():
            in_total = gr.Number(label="총 금액(원)", value=0)
            in_people = gr.Number(label="인원 수(명)", value=1, precision=0)
            in_tip = gr.Slider(minimum=0, maximum=100, step=1, label="팁/서비스 비율(%)", value=0)

            # 버튼 영역 (Submit과 Clear 배치)
            with gr.Row():
                clear_btn = gr.Button("Clear")
                submit_btn = gr.Button("Submit", variant="primary")  # 강조된 버튼

        # 출력 영역
        with gr.Column():
            out_per_person = gr.Number(label="1인당 금액(원)")
            out_total_with_tip = gr.Number(label="팁 포함 총 금액(원)")

    # 1. Submit 버튼 클릭 이벤트 연결
    submit_btn.click(
        fn=calculate_fee,
        inputs=[in_total, in_people, in_tip],
        outputs=[out_per_person, out_total_with_tip]
    )

    # 2. Clear 버튼 클릭 이벤트 연결 (입력 및 출력값 초기화)
    clear_btn.click(
        fn=lambda: (0, 1, 0, None, None),
        inputs=None,
        outputs=[in_total, in_people, in_tip, out_per_person, out_total_with_tip]
    )

# 프로그램 실행
if __name__ == "__main__":
    demo.launch()