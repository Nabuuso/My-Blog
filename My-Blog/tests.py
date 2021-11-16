try:
    from app import app
    import unittest
except Exception as e:
    print("Some modules are missing {}".format(e))

class FlaskTest(unittest.TestCase):
    ##Check status code
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/index")
        statuscode = response.status_code
        self.assertEqual(statuscode,200)
    
    ##CHECK CONTENT RETURNED BY INDEX PAGE
    def test_index_content(self):
        tester = app.test_client(self)
        response = tester.get("/index")
        self.assertEqual(response.content_type,"text/html; charset=utf-8")


if __name__ == "__main__":
    unittest.main()