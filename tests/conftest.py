import pytest
import os
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

SAMPLE_PDF_PATH = os.path.join(os.path.dirname(__file__), "sample.pdf")

@pytest.fixture
def test_client():
    return client

def create_minimal_pdf_bytes():
    """
    Creates a minimal valid PDF file in-memory for testing,
    without needing an external sample file.
    """
    pdf_content = b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /Resources 4 0 R /MediaBox [0 0 612 792] /Contents 5 0 R >>
endobj
4 0 obj
<< /Font << /F1 6 0 R >> >>
endobj
5 0 obj
<< /Length 78 >>
stream
BT /F1 24 Tf 100 700 Td (This is a test document for DocVerse AI unit tests.) Tj ET
endstream
endobj
6 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
xref
0 7
0000000000 65535 f 
trailer
<< /Size 7 /Root 1 0 R >>
startxref
0
%%EOF"""
    return pdf_content