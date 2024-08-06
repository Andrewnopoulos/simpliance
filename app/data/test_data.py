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
            u = User(str(uuid.uuid4()), 'user_name')
            s.insert(u)

            g = s.get_one(User, {'id': u.id})
            self.assertEqual(u, g)

    def test_auth_key(self):
        with Storage('test.db') as s:
            u = User(str(uuid.uuid4()), "Dandy")
            s.insert(u)
            k = AuthKeys("role", "extern", u.id)
            s.insert(k)
            all_users = s.get_all(u)
            self.assertEqual(len(all_users), 1)
            all_users = s.get_all(User)
            self.assertEqual(len(all_users), 1)
            all_keys = s.get_all(AuthKeys)
            self.assertEqual(len(all_keys), 1)
            self.assertEqual(all_keys[0].user_id, u.id)
    
    def test_delete(self):
        with Storage('test.db') as s:
            u = User(str(uuid.uuid4()), "Randy")
            s.insert(u)
            r = Report(str(uuid.uuid4()), "pending", "now", "", u.id)
            s.insert(r)
            reports = s.get_all(Report)
            self.assertEqual(len(reports), 1)
            m = s.delete(r)
            self.assertEqual(m, 1)
            reports = s.get_all(Report)
            self.assertEqual(len(reports), 0)
            new_r = s.get_one(Report, {'id': r.id})
            self.assertIsNone(new_r)
    
    def test_dirty(self):
        with Storage('test.db') as s:
            u = User('a', 'b')
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
            u = User('x', 'y')
            as_dict = u.dict()
            fields = u.fields()
            self.assertFalse('_dirty' in as_dict.keys())
            self.assertFalse('_dirty' in fields)
    
    def test_get_one(self):
        with Storage('test.db') as s:
            u = User(str(uuid.uuid4()), "Andy")
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