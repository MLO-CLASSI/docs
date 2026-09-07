# MLO CLASSI Spectrograph Software Documentation

Sphinx (RTD) documentation for the CLASSI Spectrograph software.

The site is designed to be hosted from this repository with GitHub Pages while
using the Read the Docs Sphinx theme. It documents the cross-package user
workflow as well as the individual ETC, simulator, pipeline, shared-data, and
instrument control software repositories.

## Build locally

```bash
pip install -r requirements.txt
make html
```

The built site will be written to `docs/_build/html/`.

For a strict build that treats warnings as errors:

```bash
make html-strict
```
