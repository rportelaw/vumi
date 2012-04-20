"""Tests for vumi.persist.model."""

from twisted.trial.unittest import TestCase
from twisted.internet.defer import inlineCallbacks

from vumi.persist.model import Manager, Model
from vumi.persist.fields import Integer, Unicode, Dynamic


class SimpleModel(Model):
    a = Integer()
    b = Unicode()


class DynamicModel(Model):
    a = Unicode()
    contact_info = Dynamic()


class TestModel(TestCase):
    @inlineCallbacks
    def setUp(self):
        self.manager = Manager.from_config({'bucket_prefix': 'test.'})
        yield self.manager.purge_all()

    @inlineCallbacks
    def tearDown(self):
        yield self.manager.purge_all()

    def test_simple_class(self):
        self.assertEqual(sorted(SimpleModel.fields.keys()), ['a', 'b'])
        self.assertTrue(isinstance(SimpleModel.a, Integer))
        self.assertTrue(isinstance(SimpleModel.b, Unicode))

    @inlineCallbacks
    def test_simple_instance(self):
        simple_model = self.manager.proxy(SimpleModel)
        s1 = simple_model("foo", a=5, b=u'3')
        yield s1.save()

        s2 = yield simple_model.load("foo")
        self.assertEqual(s2.a, 5)
        self.assertEqual(s2.b, u'3')

    @inlineCallbacks
    def test_dynamic_fields(self):
        dynamic_model = self.manager.proxy(DynamicModel)
        d1 = dynamic_model("foo", a=u"ab")
        d1.contact_info.cellphone = u"+27123"
        d1.contact_info.telephone = u"+2755"
        d1.contact_info.honorific = u"BDFL"
        yield d1.save()

        d2 = yield dynamic_model.load("foo")
        self.assertEqual(d2.a, u"ab")
        self.assertEqual(d2.contact_info.cellphone, u"+27123")
        self.assertEqual(d2.contact_info.telephone, u"+2755")
        self.assertEqual(d2.contact_info.honorific, u"BDFL")

    def test_link(self):
        # TODO: implement links
        pass
