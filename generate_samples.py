"""Generate synthetic invoice PDFs for testing the extractor.

Creates 12 text-based invoice PDFs in samples/. Invoice INV-2026-007
has a deliberately wrong TOTAL so you can see the verifier catch it.
"""
import os
import random
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

random.seed(42)

VENDORS = [
    ("Acme Supplies Ltd", "12 Market Road, Lahore"),
    ("City Paper House", "45 Urdu Bazaar, Karachi"),
    ("TechParts Wholesale", "8-B Industrial Area, Islamabad"),
    ("FreshLine Distributors", "22 Food Street, Faisalabad"),
]

ITEMS = [
    ("Printer paper A4 (ream)", 850.00),
    ("Ball pens (box of 50)", 120.00),
    ("USB flash drive 64GB", 1450.00),
    ("Office file folders (pack)", 320.00),
    ("Whiteboard markers (set)", 460.00),
    ("Packing tape rolls", 210.00),
    ("LED bulbs (pack of 4)", 980.00),
    ("Cleaning spray bottles", 275.00),
]

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "samples")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def draw_invoice(path, number, vendor, address, date, lines, total_override=None):
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4
    y = height - 60
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, vendor)
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, address)
    y -= 30
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, f"INVOICE #{number}")
    y -= 18
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Date: {date}")
    y -= 30
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Description")
    c.drawString(300, y, "Qty")
    c.drawString(350, y, "Unit Price")
    c.drawString(450, y, "Amount")
    y -= 14
    c.setFont("Helvetica", 10)
    subtotal = 0.0
    for desc, qty, price in lines:
        amount = qty * price
        subtotal += amount
        c.drawString(50, y, desc)
        c.drawString(300, y, str(qty))
        c.drawString(350, y, f"{price:,.2f}")
        c.drawString(450, y, f"{amount:,.2f}")
        y -= 16
    tax = round(subtotal * 0.10, 2)
    total = round(subtotal + tax, 2)
    if total_override is not None:
        total = total_override
    y -= 8
    c.drawString(350, y, "Subtotal:")
    c.drawString(450, y, f"{subtotal:,.2f}")
    y -= 16
    c.drawString(350, y, "Tax (10%):")
    c.drawString(450, y, f"{tax:,.2f}")
    y -= 16
    c.setFont("Helvetica-Bold", 11)
    c.drawString(350, y, "TOTAL:")
    c.drawString(450, y, f"{total:,.2f}")
    c.save()


def main():
    dates = [f"2026-09-{d:02d}" for d in range(1, 28)]
    for i in range(1, 13):
        number = f"INV-2026-{i:03d}"
        vendor, address = VENDORS[(i - 1) % len(VENDORS)]
        lines = []
        for desc, price in random.sample(ITEMS, k=random.randint(2, 4)):
            lines.append((desc, random.randint(1, 20), price))
        # Deliberate mismatch in invoice 7 to demo the verifier
        override = None
        if i == 7:
            subtotal = sum(q * p for _, q, p in lines)
            override = round(subtotal * 1.10 + 500.0, 2)
        path = os.path.join(OUTPUT_DIR, f"{number}.pdf")
        draw_invoice(path, number, vendor, address, random.choice(dates), lines, override)
        flag = "  [TOTAL intentionally wrong]" if override else ""
        print(f"created {path}{flag}")


if __name__ == "__main__":
    main()
