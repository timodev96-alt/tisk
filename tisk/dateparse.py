import re
from datetime import date, timedelta

def parse_date(value):
    if not value:
        return None
    v= value.strip().lower()
    today = date.today()

    if v == 'today':
        return today.isoformat()
    if v in ('tomorrow', 'tmr'):
        return (today + timedelta(days=1)).isoformat()
    if v == 'yesterday':
        return (today - timedelta(days=1)).isoformat()

    m = re.fullmatch(r'in (\d+) ?(day|days|week|weeks)', v)
    if m:
        n = int(m.group(1))
        days = n*7 if 'week' in m.group(2) else n
        return(today + timedelta(days=days)).isoformat()
    
    m = re.fullmatch(r'(\d+)\s*([dw])', v)
    if m:
        n=int(m.group(1))
        days = n*7 if m.group(2) == 'w' else n
        return(today + timedelta(days=days)).isoformat()
        
    
    try:
        return date.fromisoformat(value.strip()).isoformat()
    except ValueError:
        raise ValueError(
            f'Could not understand the date "{value}".'
            'Try YYYY-MM-DD , "today", "tomorrow", "3d" or "in 2 weeks".'
        )