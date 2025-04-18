
#  <img src="favicon.svg" alt="Project Icon Thread and Needle"> Patchwork

CSS Vendor Library

> Simple Library to pull the latest CSS for usign OpenProps UI

## Credit
h/t [OpenProps UI](https://open-props-ui.netlify.app/)
h/t [OpenProps](https://open-props.style/)

## How to Use
```python
vendor = setup_openprops_vendor()
results = vendor.sync_all()
print(f"Results by source: {results}")
```

This will pull the latest CSS for Open Props and OpenProps UI along with creating an empty custom directory for your project.

You can you this by just pointign to the main.css as a CDN link.
