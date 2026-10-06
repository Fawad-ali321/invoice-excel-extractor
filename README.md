# Invoice → Excel Extractor with Total Verification

**Problem:** Finance teams waste hours retyping invoice data from PDFs into Excel — and manual typing introduces errors that are hard to catch.

**Solution:** A Python pipeline that extracts line items from invoice PDFs and **cross-verifies every total** against the summary printed in the PDF, so bad data gets flagged instead of silently copied.

## How it works

1. `generate_samples.py` creates 12 synthetic invoice PDFs (text-based) in `samples/` — including one with a deliberately wrong total to demo the verifier.
2. `extract.py` reads each PDF with **pdfplumber**, parses vendor / date / line items / totals with regex, then recomputes every invoice total from its line items.
3. Output is an Excel workbook (`output/invoices_extracted.xlsx`) with two sheets:
   - **Extracted_Data** — one row per line item (invoice no, date, vendor, description, qty, unit price, amount)
   - **Verification** — per-invoice stated total vs computed total, difference, and a colour-coded **MATCH / MISMATCH** status

## Run it

```bash
pip install -r requirements.txt
python generate_samples.py   # create sample invoices
python extract.py            # extract + verify -> output/invoices_extracted.xlsx
```

## Sample output

| invoice_no  | stated_total | computed_total | difference | status   |
|-------------|-------------:|---------------:|-----------:|:---------|
| INV-2026-001|    12650.00  |      12650.00  |       0.00 | MATCH    |
| INV-2026-007|    18230.00  |      17730.00  |     500.00 | MISMATCH |

## Tech stack

Python · pdfplumber · pandas · openpyxl · reportlab

> Sample project built for portfolio demonstration. Invoices are synthetic.
