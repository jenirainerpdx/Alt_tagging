import gradio as gr
from static_file_url_captioner import find_captions

iface = gr.Interface(
    fn = find_captions,
    inputs = gr.Textbox(),
    outputs= "text",
    title = "Alt tagger",
    description = "App to generate alt text for images on a web page",
)
iface.launch(server_name="0.0.0.0", server_port=8000, share=True)