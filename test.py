import unittest
import app
import json

class TestApp(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()
        self.headers = {'Content-Type': 'application/json', 'Accept-Language' : 'en,es;q=0.9'}
    
    def test_signup(self):
        data = {
            "email" : "tester12345678@test.com",
            "password" : "tester123",
            "name" : "tester",
            "lastname" : "flask",
            "birthday" : "2000-04-02",
            "gender" : "m"
        }
        rv = self.app.post('/signup', data=json.dumps(data), headers=self.headers)
        self.assertEqual(rv.status, '200 OK')
        self.assertEqual(json.loads(rv.data), {"result":"ok"})

        rv = self.app.post('/signup', data=json.dumps(data), headers=self.headers)
        self.assertEqual(rv.status, '200 OK')
        self.assertEqual(json.loads(rv.data), {
            "message": "Email not available",
            "result": "emailused"
        })

        rv = self.app.post('/signup', data=json.dumps({}), headers=self.headers)
        self.assertEqual(rv.status, '200 OK')
        self.assertEqual(json.loads(rv.data), {"result":"invalid"})

    def test_login(self):
        data = {
            "email" : "tester123@test.com",
            "password" : "tester123",
        }
        rv = self.app.post('/login', data=json.dumps(data), headers=self.headers)
        self.assertEqual(rv.status, '200 OK')
        self.assertEqual(json.loads(rv.data), {"result":"usuario inexistente"})

        data = {
            "email" : "admin@site.com",
            "password" : "0123456789",
        }
        rv = self.app.post('/login', data=json.dumps(data), headers=self.headers)
        self.assertEqual(rv.status, '200 OK')
        self.assertEqual(json.loads(rv.data), {"result":"invalid password"})

        data = {
            "email" : "admin@site.com",
            "password" : "admin123",
        }
        rv = self.app.post('/login', data=json.dumps(data), headers=self.headers)
        self.assertEqual(rv.status, '200 OK')
        self.assertEqual(json.loads(rv.data), {"result":"ok"})

    def test_post(self):
        data = {
            "uid" : "63877A9C5CFBD0E1EEA2D6B1",
            "token" : "crueTiIeDIK0rQzYtSA4ChM6eBFyn7cTCFIbVJSGB00",
            "content" : "Hello World",
            "privacity" : 1,
            "comments_on" : True,
            "mediaList" : ["static/iamges/63877A9C5CFBD0E1EEA2D6B1.png"]
        }

        rv = self.app.post('/post', data=json.dumps(data), headers=self.headers)
        self.assertEqual(rv.status, '200 OK')
        self.assertEqual(json.loads(rv.data), {"result":"ok"})
     
        data = {
            "uid" : "63877A9C5CFBD0E1EEA2D6B1",
            "token" : "000000000000000000000000000000000000000000000",
            "content" : "Hello World 2",
            "privacity" : 1,
            "comments_on" : True,
            "mediaList" : ["static/iamges/63877A9C5CFBD0E1EEA2D6B2.png"]
        }

        rv = self.app.post('/post', data=json.dumps(data), headers=self.headers)
        self.assertEqual(rv.status, '200 OK')
        self.assertEqual(json.loads(rv.data), {"result":"you must be logged"})

        rv = self.app.post('/post', data=json.dumps({}), headers=self.headers)
        self.assertEqual(rv.status, '200 OK')
        self.assertEqual(json.loads(rv.data), {"result":"invalid"})

    def test_comment(self):
        data = {
            "_id" : "6507032EGER054EWGTER105W",
            "uid" : "63877A9C5CFBD0E1EEA2D6B1",
            "token" : "crueTiIeDIK0rQzYtSA4ChM6eBFyn7cTCFIbVJSGB00",
            "content" : "Que hermosa foto",
            "mediaList" : [],
            "replys" : []
        }

        rv = self.app.post('/comment', data=json.dumps(data), headers=self.headers)
        self.assertEqual(rv.status, '200 OK')
        self.assertEqual(json.loads(rv.data), {"result":"ok"})

        data = {
            "_id" : "6507032EGER054EWGTER105W",
            "uid" : "63877A9C5CFBD0E1EEA2D6B1",
            "token" : "000000000000000000000000000000000000000000000",
            "content" : "Que hermosa foto2",
            "mediaList" : [],
            "replys" : []
        }

        rv = self.app.post('/comment', data=json.dumps(data), headers=self.headers)
        self.assertEqual(rv.status, '200 OK')
        self.assertEqual(json.loads(rv.data), {"result":"you must be logged"})


        rv = self.app.post('/comment', data=json.dumps({}), headers=self.headers)
        self.assertEqual(rv.status, '200 OK')
        self.assertEqual(json.loads(rv.data), {"result":"invalid"})

    def test_friends(self):
        data = {
            "uid" : "63877A9C5CFBD0E1EEA2D6B1",
            "token" : "crueTiIeDIK0rQzYtSA4ChM6eBFyn7cTCFIbVJSGB00",
            "action" : "friends",
            "uid_friend" : "676864FGDGTHT1020303223"
        }

        rv = self.app.post('/friends', data=json.dumps(data), headers=self.headers)
        self.assertEqual(rv.status, '200 OK')
        self.assertEqual(json.loads(rv.data), {"result":"ok"})

        data = {
            "uid" : "63877A9C5CFBD0E1EEA2D6B1",
            "token" : "000000000000000000000000000000000000000000000",
            "action" : "friends",
            "uid_friend" : "676864FGDGTHT1020303223"
        }

        rv = self.app.post('/friends', data=json.dumps(data), headers=self.headers)
        self.assertEqual(rv.status, '200 OK')
        self.assertEqual(json.loads(rv.data), {"result":"you must be logged"})

        rv = self.app.post('/friends', data=json.dumps({}), headers=self.headers)
        self.assertEqual(rv.status, '200 OK')
        self.assertEqual(json.loads(rv.data), {"result":"invalid"})




if __name__ == '__main__':
    unittest.main()