
def tp_assert(tp, *args):
    for i in args:
        assert isinstance(i ,tp) 

def tp_ensure(v, tp):
    assert isinstance(v, tp)
    return v

def not_empty_assert(v):
    assert v


def assert_key(v, *args):
    for i in args:
        assert i in v


