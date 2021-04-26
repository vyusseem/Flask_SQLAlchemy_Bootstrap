import main
import uuid

main.app.testing = True
client = main.app.test_client()

def test_index():
    r = client.get('/')
    assert r.status_code == 200
    assert "Flask + SQLAlchemy + Bootstrap" in r.data.decode()

def test_posts():
    r = client.get('/posts')
    assert r.status_code == 200
    assert "<h1>Posts</h1>" in r.data.decode()

def test_posts_add():
    # Form
    r = client.get('/posts/add')
    assert r.status_code == 200
    assert "<form method = \"POST\">" in r.data.decode()

    # Submit
    myuuid = str(uuid.uuid4())
    r = client.post('/posts/add', data=dict(title=myuuid+"title", author=myuuid+"author", content=myuuid+"content"), follow_redirects=True)
    assert r.status_code == 200
    assert myuuid+"title" in r.data.decode()
    assert myuuid+"author" in r.data.decode()
    assert myuuid+"content" in r.data.decode()


