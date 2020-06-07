from pathlib import Path
import tempfile

import pytest

from servicex.cache import cache


@pytest.fixture
def cache_dir():
    p = Path(tempfile.gettempdir()) / 'servicex-cache-testing'
    if p.exists():
        import shutil
        shutil.rmtree(p)
    p.mkdir(parents=True)
    yield p
    if p.exists():
        import shutil
        shutil.rmtree(p)


def test_create_cache(cache_dir):
    _ = cache(cache_dir)


def test_query_miss(cache_dir):
    c = cache(cache_dir)

    assert c.lookup_query({'hi': 'there'}) is None


def test_query_hit_1(cache_dir):
    c = cache(cache_dir)
    c.set_query({'hi': 'there'}, 'dude')
    assert c.lookup_query({'hi': 'there'}) == 'dude'


def test_query_hit_2(cache_dir):
    c = cache(cache_dir)
    c.set_query({'hi': 'there'}, 'dude1')
    c.set_query({'hi': 'theree'}, 'dude2')
    assert c.lookup_query({'hi': 'there'}) == 'dude1'
    assert c.lookup_query({'hi': 'theree'}) == 'dude2'


def test_query_lookup_from_file(cache_dir):
    c1 = cache(cache_dir)
    c1.set_query({'hi': 'there'}, 'dude')

    c2 = cache(cache_dir)
    assert c2.lookup_query({'hi': 'there'}) == 'dude'


def test_files_miss(cache_dir):
    c = cache(cache_dir)
    assert c.lookup_files('1234') is None


def test_files_hit(cache_dir):
    c = cache(cache_dir)
    c.set_files('1234', ['hi', 'there'])
    assert c.lookup_files('1234') == ['hi', 'there']


def test_files_hit_reloaded(cache_dir):
    c1 = cache(cache_dir)
    c1.set_files('1234', ['hi', 'there'])
    c2 = cache(cache_dir)
    assert c2.lookup_files('1234') == ['hi', 'there']
