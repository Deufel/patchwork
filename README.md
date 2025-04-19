
#  <img src="favicon.svg" alt="Project Icon Thread and Needle"> Patchwork

CSS Vendor Library

> Simple Library to pull the latest CSS for using [OpenProps UI](https://open-props-ui.netlify.app/)
> with some extra layout utilities

## Credit
 - [OpenProps UI](https://open-props-ui.netlify.app/)
 - [OpenProps](https://open-props.style/)

## Note
The CSS folder is compiled from various sources, see the vendor.py file for details.

## QuickStart
```bash
python vendor.py # pull latest CSS from source load in to CSS folder
python test.py  # confirm imports
```

```python
from fasthtml.common import *
hdrs = (
    Link(rel='stylesheet', href='https://cdn.jsdelivr.net/gh/Deufel/patchwork@master/css/ui/main.css'), # CDN
    Link(rel='stylesheet', href='static/css/ui/main.css'), # Local
)

app,rt = fast_app(hdrs=hdrs, pico=False)

@rt
def index(): return(
    Title("Buttons"),
    Main(H1("Lets see what some buttons look like"),
         Button(cls="button outlined")("Outlined")
         Button(cls="button elevated")("Elevated")
        )
)
```


## TODO
- [x] Landing page layout
- [ ] Theme
- [ ] dashboard layout
- [ ] Dialog Nav Bar
- [ ] Aside
- [ ] Footer drawer.. (was unstable on mobile with popover so maybe dont use?)
