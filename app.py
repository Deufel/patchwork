from fasthtml.common import *
hdrs = (
    Link(rel="stylesheet", href="https://cdn.jsdelivr.net/gh/Deufel/patchwork@master/css/ui/main.css"),
)

app,rt = fast_app(hdrs=hdrs, Pico=False)

@rt
def index(): return Div(P('Hello World!'), hx_get="/change")

serve()
