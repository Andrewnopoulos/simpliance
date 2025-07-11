import unittest, os, uuid

from .datastore import create_schema, Storage

from .models import *

class TestDataStore(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        create_schema('test.db', '../db_setup.sql')
        return super().setUpClass()
    
    @classmethod
    def tearDownClass(cls) -> None:
        os.remove('test.db')
        return super().tearDownClass()

    def test_storage(self):
        with Storage('test.db') as s:
            u = User(str(uuid.uuid4()), 'user_name', "dandy@d.mail")
            s.insert(u)

            g = s.get_one(User, {'id': u.id})
            self.assertEqual(u, g)

    def test_auth_key(self):
        with Storage('test.db') as s:
            u = User(str(uuid.uuid4()), "Dandy", "dan@dy.com")
            s.insert(u)
            k = AuthKeys(str(uuid.uuid4()), "role", "extern", u.id)
            s.insert(k)
            all_users = s.get_all(u)
            self.assertEqual(len(all_users), 1)
            all_users = s.get_all(User)
            self.assertEqual(len(all_users), 1)
            all_keys = s.get_all(AuthKeys)
            self.assertEqual(len(all_keys), 1)
            self.assertEqual(all_keys[0].user_id, u.id)
    
    def test_user_password(self):
        with Storage('test.db') as s:
            u = User(str(uuid.uuid4()), "mufti", "")
            u.hashed_password = "hey"
            hashed_pw = u.hashed_password
            s.insert(u)
            v = s.get_one(User, {'id': u.id})
            self.assertEqual(v.hashed_password, hashed_pw)

            w = User(str(uuid.uuid4()), "bozo", "email", False, "constructor_password")
            hashed_pw = w.hashed_password
            s.insert(w)
            v = s.get_one(User, {'id': w.id})
            self.assertEqual(v.hashed_password, hashed_pw)
    
    def test_auth_key_report(self):
        with Storage('test.db') as s:
            u = User(str(uuid.uuid4()), "Dandy", "dandy@d.mail")
            s.insert(u)
            k = AuthKeys(str(uuid.uuid4()), "role", "extern", u.id)
            s.insert(k)
            r = Report(str(uuid.uuid4()), 'pending', 'now', '', "test_benchmark", u.id, k.id)
            s.insert(r)

            fetched_r = s.get_one(Report, {'auth_key_id': k.id})
            self.assertEqual(fetched_r, r)

            s.delete(r)
    
    def test_delete(self):
        with Storage('test.db') as s:
            u = User(str(uuid.uuid4()), "Randy", "dan@dy.com")
            s.insert(u)
            k = AuthKeys(str(uuid.uuid4()), 'role_id', 'test_external_id', u.id)
            s.insert(k)
            r = Report(str(uuid.uuid4()), "pending", "now", "", "test_benchmark", u.id, k.id)
            s.insert(r)
            reports = s.get_all(Report)
            self.assertEqual(len(reports), 1)
            m = s.delete(r)
            self.assertEqual(m, 1)
            reports = s.get_all(Report)
            self.assertEqual(len(reports), 0)
            new_r = s.get_one(Report, {'id': r.id})
            self.assertIsNone(new_r)
    
    def test_get_where(self):
        with Storage('test.db') as s:
            u = User(str(uuid.uuid4()), "landy", "dandy@d.mail")
            s.insert(u)
            u = User(str(uuid.uuid4()), "landy", "dandy@d.mail")
            s.insert(u)
            users = s.get_where(User, {'name': "landy"})
            self.assertEqual(len(users), 2)
    
    def test_dirty(self):
        with Storage('test.db') as s:
            u = User('a', 'b', "dan@dy.com")
            self.assertEqual(u._dirty, [])
            u.id = 'b'
            self.assertEqual(u._dirty, ['id'])
            m = s.insert(u)
            self.assertEqual(m, 1)
            self.assertEqual(u._dirty, [])
            u.name = 'boo'
            self.assertEqual(u._dirty, ['name'])
            s.update(u)
            self.assertEqual(u._dirty, [])
            s.delete(u)

            all_users = s.get_all(User)
            self.assertFalse(u in all_users)

    def test_meta(self):
        with Storage('test.db') as s:
            u = User('x', 'y', "x@y.com")
            as_dict = u.dict()
            fields = u.fields()
            self.assertFalse('_dirty' in as_dict.keys())
            self.assertFalse('_dirty' in fields)
    
    def test_get_one(self):
        with Storage('test.db') as s:
            u = User(str(uuid.uuid4()), "Andy", "an@dy.com")
            s.insert(u)

            retval = s.get_one(User, {'name': 'Andy'})
            self.assertEqual(retval, u)

            retval = s.get_one(User, {'id': u.id})
            self.assertEqual(retval, u)

            retval = s.get_one(User, {})
            self.assertIsNone(retval)

            retval = s.get_one(User, {'id': 'sodifjds'})
            self.assertIsNone(retval)

            retval = s.get_one(User, {'sodifj': 'dsoifj'})
            self.assertIsNone(retval)

if __name__ == '__main__':
    unittest.main()