from Redis import Redis


redis = Redis()

def test_edge_cases():
    assert redis.execute("GET hello").split()[-1] == "FOUND"
    assert redis.execute("") == None
    assert redis.execute("SET hello world more") == None
    assert redis.execute("sdshjdbj") == None
    assert redis.execute("DEL hello").split()[-1] == "FOUND"

    # assert 1 == 1

def test_set():
    assert redis.execute("SET hello world").split()[-1] == "OK"
    assert redis.execute("SET bye all").split()[-1] == "OK"

    assert redis.execute("SET hello world2").split()[-1] == "OK"

def test_get():
    assert redis.execute("GET hello").split()[-1] == "world2"
    assert redis.execute("GET bye").split()[-1] == "all"

def test_del():
    assert redis.execute("DEL bye").split()[-1] == "OK"

def test_final():

    assert redis.execute("GET hello").split()[-1] == "world2"
    assert redis.execute("GET bye").split()[-1] == "FOUND"

    assert redis.execute("DEL hello").split()[-1] == "OK"
    assert redis.execute("GET hello").split()[-1] == "FOUND"
