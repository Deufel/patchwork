
#  <img src="favicon.svg" alt="Project Icon Thread and Needle"> Patchwork

CSS Vendor Library

> Simple Library to pull the latest CSS for usign OpenProps UI

## Credit
h/t [OpenProps UI](https://open-props-ui.netlify.app/)
h/t [OpenProps](https://open-props.style/)

## How to Use
 1A. Run the following command in your terminal:
``` zsh
python vendor.py # pull latest CSS from source
```

 1B. Use a CDN (not that fast)

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Deufel/patchwork@master/css/ui/main.css">
```

 2.

 ```bash
 $ uv add python-fasthtml
 ```

```python
from fasthtml.common import *
hdrs = (
    Link(rel="stylesheet", href="https://cdn.jsdelivr.net/gh/Deufel/patchwork@master/css/ui/main.css"),
)

app,rt = fast_app(hdrs=hdrs, Pico=False)

@rt
def index(): return Div(P('Hello World!'), hx_get="/change")

serve()
```
