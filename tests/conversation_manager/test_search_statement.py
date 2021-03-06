from unittest import TestCase
from app import create_app
from app.view.conversation_manager import generate_token
import json


class SearchStatementTestCase(TestCase):
    """
    Unit tests for the Admin Search Statement.
    LJF: all tests clear 2020-5-13
    """

    def setUp(self):
        self.app = create_app().test_client()
        self.myheaders = {'Content-Type': 'application/json'}
        self.token = generate_token(b'buaa', 3600)

    def test_no_attribute(self):
        r = self.app.get(
            'admin/search_statement',
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000001)
        self.assertEqual(r.status_code, 400)

    def test_no_username(self):
        r = self.app.get(
            'admin/search_statement?token=111&id=',
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000001)
        self.assertEqual(r.status_code, 400)

    def test_no_token(self):
        r = self.app.get(
            'admin/search_statement?username=wechatterbot&id=1',
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000001)
        self.assertEqual(r.status_code, 400)

    def test_wrong_username(self):
        r = self.app.get(
            'admin/search_statement?username=wechatterwhat' +
            '&token=' + self.token + '&id=1',
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000044)
        self.assertEqual(r.status_code, 401)

    def test_wrong_token(self):
        wrong_token = generate_token(b'what', 3600)
        r = self.app.get(
            'admin/search_statement?username=wechatterbot' +
            '&token=' + wrong_token + '&id=1',
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000044)
        self.assertEqual(r.status_code, 401)

    def test_empty_id_and_empty_text(self):
        r = self.app.get(
            'admin/search_statement?username=wechatterbot' +
            '&token=' + self.token,
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000001)
        self.assertEqual(r.status_code, 400)

    def test_empty_id_and_no_text(self):
        r = self.app.get(
            'admin/search_statement?username=wechatterbot' +
            '&token=' + self.token + '&id=',
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000001)
        self.assertEqual(r.status_code, 400)

    def test_no_id_and_empty_text(self):
        r = self.app.get(
            'admin/search_statement?username=wechatterbot' +
            '&token=' + self.token + '&text=',
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000001)
        self.assertEqual(r.status_code, 400)

    def test_no_id_and_no_text(self):
        r = self.app.get(
            'admin/search_statement?username=wechatterbot' +
            '&token=' + self.token,
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000001)
        self.assertEqual(r.status_code, 400)

    def test_id_not_a_number(self):
        r = self.app.get(
            'admin/search_statement?username=wechatterbot' +
            '&token=' + self.token + '&id=string',
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000001)

    def test_successful_search_with_text(self):
        data = {
            'response': '临时回复规则',
            'text': '临时规则内容',
            'username': 'wechatterbot',
            'token': self.token
        }
        self.app.post(
            'http://localhost:5000/admin/create_statement',
            data=json.dumps(data),
            headers=self.myheaders
        )
        r = self.app.get(
            'admin/search_statement?username=wechatterbot' +
            '&token=' + self.token + '&text=临时规则内容',
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        statements = result['statements']
        self.assertEqual(statements[0]['text'], u"临时规则内容")
        self.assertEqual(r.status_code, 200)

    def test_successful_search_with_id(self):
        r = self.app.get(
            'admin/search_statement?username=wechatterbot' +
            '&token=' + self.token + '&id=1',
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        statements = result['statements']
        self.assertEqual(statements[0]['id'], 1)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['number'], 1)
