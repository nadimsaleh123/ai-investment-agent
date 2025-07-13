from __future__ import annotations

import gradio as gr

from .orchestrator import Orchestrator


orchestrator = Orchestrator()


def handle_chat(asset: str, brief: str) -> str:
    return orchestrator.route_request(asset, brief)


def handle_report() -> str:
    return orchestrator.generate_report()


def main() -> None:
    assets = list(orchestrator.agents.keys())
    assets.remove("python_coder")

    theme = gr.themes.Soft(primary_hue="green")

    with gr.Blocks(theme=theme) as demo:
        gr.Markdown(
            "# Investment Advisor\n"
            "Get curated insights for a variety of asset classes."
        )

        with gr.Row():
            with gr.Column(scale=1):
                asset = gr.Dropdown(label="Asset", choices=assets)
            with gr.Column(scale=2):
                brief = gr.Textbox(label="Daily Brief", lines=4)

        output = gr.Textbox(label="Agent Response", lines=8)

        with gr.Row():
            submit = gr.Button("Submit")
            report = gr.Button("Generate Report")
            clear = gr.Button("Clear")

        submit.click(handle_chat, inputs=[asset, brief], outputs=output)
        report.click(handle_report, None, output)
        clear.click(lambda: "", None, output)

    demo.launch()


if __name__ == "__main__":
    main()
