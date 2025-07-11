from __future__ import annotations

import gradio as gr

from .orchestrator import Orchestrator


orchestrator = Orchestrator()


def handle_chat(asset: str, brief: str) -> str:
    return orchestrator.route_request(asset, brief)


def main() -> None:
    assets = list(orchestrator.agents.keys())
    assets.remove("python_coder")
    with gr.Blocks() as demo:
        gr.Markdown("# Investment Advisor")
        asset = gr.Dropdown(label="Asset", choices=assets)
        brief = gr.Textbox(label="Daily Brief")
        output = gr.Textbox(label="Agent Response")
        btn = gr.Button("Submit")
        btn.click(handle_chat, inputs=[asset, brief], outputs=output)
    demo.launch()


if __name__ == "__main__":
    main()
