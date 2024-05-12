# meltdown
A naive markdown parser in pure python.

Just a work in progress for now.

**WARNING:** The library will never attempt to do any sanitization on the input. 
If used for user generated content it is highly recommended to use an external
sanitization library.

## Built it yourself

While meltdown doesn't have any dependencies other than the standard library
to use it, it needs pytest to be tested and some other libraries might be nice
during development.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

## Run all tests
```bash
python -m pytest
```