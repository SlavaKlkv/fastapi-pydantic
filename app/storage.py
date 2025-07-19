entities: dict = {}
_next_id = 1

def next_id():
    global _next_id
    nid = _next_id
    _next_id += 1
    return nid