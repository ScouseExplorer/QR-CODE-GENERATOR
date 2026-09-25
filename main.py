"""Generate QR codes from the command line.

Usage examples:
  python main.py "https://example.com" -o myqr.png
  python main.py "Hello world" --format svg -o hello.svg
"""
from __future__ import annotations

import argparse
import os
import sys
from typing import Optional

import qrcode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H


ERROR_CORRECTION_MAP = {
    "L": ERROR_CORRECT_L,
    "M": ERROR_CORRECT_M,
    "Q": ERROR_CORRECT_Q,
    "H": ERROR_CORRECT_H,
}


def generate_qr(
    data: str,
    output: str = "qrcode.png",
    version: Optional[int] = None,
    error: str = "L",
    box_size: int = 10,
    border: int = 4,
    fill_color: str = "black",
    back_color: str = "white",
    image_format: str = "png",
) -> str:
    """Generate a QR code and save it to `output`. Returns the output path.

    Supports PNG (default) and SVG when the SVG image factory is available.
    """
    error = (error or "L").upper()
    ec = ERROR_CORRECTION_MAP.get(error, ERROR_CORRECT_L)

    qr = qrcode.QRCode(version=version, error_correction=ec, box_size=box_size, border=border)
    qr.add_data(data)
    qr.make(fit=True)

    fmt = (image_format or "png").lower()
    if fmt == "svg":
        try:
            from qrcode.image.svg import SvgImage

            img = qr.make_image(image_factory=SvgImage)
            # SvgImage.save writes text; ensure correct mode
            img.save(output)
        except Exception as e:  # fall back or report clearly
            raise RuntimeError("SVG output not available: %s" % e)
    else:
        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        img.save(output)

    return output


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate a QR code image from input text or URL.")
    p.add_argument("data", help="Text or URL to encode in the QR code")
    p.add_argument("-o", "--output", default="qrcode.png", help="Output filename (default: qrcode.png)")
    p.add_argument("--format", choices=["png", "svg"], default="png", help="Output image format")
    p.add_argument("--version", type=int, default=None, help="QR version (1-40). Default: auto fit")
    p.add_argument("--error", choices=["L", "M", "Q", "H"], default="L", help="Error correction level")
    p.add_argument("--box-size", type=int, default=10, help="Size of each box in pixels")
    p.add_argument("--border", type=int, default=4, help="Border size (boxes)")
    p.add_argument("--fill", default="black", help="Fill color for the QR (default: black)")
    p.add_argument("--back", default="white", help="Background color (default: white)")
    p.add_argument("--open", action="store_true", help="Open the generated image after creation (Windows only)")
    return p.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    args = parse_args(argv)

    out = args.output
    try:
        out_path = generate_qr(
            data=args.data,
            output=out,
            version=args.version,
            error=args.error,
            box_size=args.box_size,
            border=args.border,
            fill_color=args.fill,
            back_color=args.back,
            image_format=args.format,
        )
    except Exception as e:
        print("Error:", e, file=sys.stderr)
        return 2

    print("Saved:", out_path)

    if args.open:
        try:
            if os.name == "nt":
                os.startfile(out_path)  # type: ignore[attr-defined]
            else:
                # cross-platform open fallback
                import webbrowser

                webbrowser.open("file://" + os.path.abspath(out_path))
        except Exception as e:
            print("Could not open file:", e, file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
import qrcode

data = "https://wiki.postgresql.org/wiki/Don't_Do_This"

img = qrcode.make(data)


qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(data)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save("qrcode.png")

