import re
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

_PAT = {
    'amount': re.compile(r'credited with Rs ([\d,]+\.\d{2})'),
    'date':   re.compile(r'on (\d{2}-\w{3}-\d{2})'),
    'sender': re.compile(r'from (.*?)\. UPI'),
    'utr':    re.compile(r'UPI:(\d+)'),
}
_DATE_FMTS = ["%d-%b-%y", "%d-%b-%Y"]

def parse_sms(text: str) -> dict | None:
    """Parses bank SMS to extract UTR, amount, sender, and date."""
    text_lower = text.lower()
    
    # Filter out debited messages
    if "debited" in text_lower or "sent to" in text_lower or "paid to" in text_lower:
        return None

    ma = _PAT['amount'].search(text)
    md = _PAT['date'].search(text)
    ms = _PAT['sender'].search(text)
    mu = _PAT['utr'].search(text)
    
    if not all([ma, md, ms, mu]):
        # Fallback for simpler UTR-only check if it's definitely a credit
        if "credited" in text_lower or "received" in text_lower:
            mu_fb = re.search(r'UPI:(\d{12})', text) or re.search(r'\b(\d{12})\b', text)
            if mu_fb:
                return {
                    'utr':    mu_fb.group(1),
                    'amount': 0.0, # Will be updated manually if needed or caught by pattern
                    'sender': 'UPI User',
                    'date':   datetime.now(),
                }
        return None
        
    for fmt in _DATE_FMTS:
        try:
            sms_date = datetime.strptime(md.group(1), fmt)
            break
        except ValueError:
            continue
    else:
        sms_date = datetime.now()
        
    return {
        'utr':    mu.group(1),
        'amount': float(ma.group(1).replace(',', '')),
        'sender': ms.group(1).strip(),
        'date':   sms_date,
    }
