# QR Code generator

Simple CLI to generate QR codes using Python and `qrcode`.

Install

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Usage

```powershell
python main.py "https://example.com" -o example.png
python main.py "Hello world" --format svg -o hello.svg
python main.py "Text" --open
```

Options include `--box-size`, `--border`, `--error` (L/M/Q/H), `--fill`, and `--back`.
