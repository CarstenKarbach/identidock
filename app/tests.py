import unittest
import identidock

class TestCase(unittest.TestCase):

    def setUp(self):
        identidock.app.config["TESTING"] = True
        self.app = identidock.app.test_client()
        
    def test_get_mainpage(self):
        page = self.app.post("/", data=dict(name="Moby Dock"))
        assert page.status_code == 200
        assert 'Hallo' in str(page.data)
        assert 'Moby Dock' in str(page.data)
        
    def test_html_escaping(self):
        page = self.app.post("/", data=dict(name="><b>Test</b><!--"))
        assert '<b>' not in str(page.data)
        
if __name__ == '__main__':
    unittest.main()