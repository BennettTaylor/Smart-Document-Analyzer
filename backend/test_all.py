import app
import nlp
import tracemalloc
import cProfile
import pstats
import logging

logging.basicConfig(format='%(asctime)s %(message)s')
tracemalloc.start()

profiler = cProfile.Profile()
profiler.enable()


def test_sentiment_keyword():
    sentiment, keyword = nlp.perform_nlp("Small example text")
    assert sentiment is not None
    assert isinstance(keyword, str)


def test_generate_summary():
    summary = nlp.generate_summary("More example text, but a bit longer")
    assert isinstance(summary, str)


def test_allowed_file():
    is_allowed = app.allowed_file("This.txt")
    assert is_allowed is True


profiler.disable()
profiler.dump_stats("example.stats")
stats = pstats.Stats("example.stats")
stats.print_stats()

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

logging.warning("[ Top 10 ]")
for stat in top_stats[:10]:
    logging.error(stat)