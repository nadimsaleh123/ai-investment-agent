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

    theme = gr.themes.Default(
        primary_hue="slate",
        secondary_hue="slate",
        font=[
            "-apple-system",
            "BlinkMacSystemFont",
            "Helvetica Neue",
            "Arial",
            "sans-serif",
        ],
    )

    css = """
    #container {max-width: 760px; margin: auto; padding-top: 2rem;}
    body {background-color: #fafafa;}
    """

    with gr.Blocks(theme=theme, css=css, elem_id="container") as demo:
        gr.Markdown(
            "# Investment Advisor",
            elem_classes="text-center text-2xl font-semibold mb-2",
        )
        gr.Markdown(
            "Get curated insights for a variety of asset classes.",
            elem_classes="text-center text-md text-gray-600 mb-4",
        )

        with gr.Row():
            with gr.Column(scale=1):
                asset = gr.Dropdown(label="Asset", choices=assets)
            with gr.Column(scale=2):
                brief = gr.Textbox(label="Daily Brief", lines=4)

        output = gr.Textbox(label="Agent Response", lines=8)

        with gr.Row():
            submit = gr.Button("Submit", variant="primary")
            report = gr.Button("Generate Report", variant="secondary")
            clear = gr.Button("Clear", variant="stop")

        submit.click(handle_chat, inputs=[asset, brief], outputs=output)
        report.click(handle_report, None, output)
        clear.click(lambda: "", None, output)

    demo.launch()


if __name__ == "__main__":
    main()
