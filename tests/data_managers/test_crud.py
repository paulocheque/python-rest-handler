# import unittest


class DataManagerAbstractTests(object): # abstract unittest.TestCase
    def get_data_manager(self):
        pass

    def get_instance(self):
        return self.get_data_manager().save_instance({})

    def test_save_instance(self):
        self.get_data_manager().save_instance({})

    def test_find_instance_by_id(self):
        instance = self.get_instance()
        found = self.get_data_manager().find_instance_by_id(instance.id)
        self.assertEquals(instance, found)

    def test_instance_list(self):
        instance1 = self.get_instance()
        instance2 = self.get_instance()
        self.assertEquals(2, len(self.get_data_manager().instance_list()))
        self.assertEquals(True, instance1 in self.get_data_manager().instance_list())
        self.assertEquals(True, instance2 in self.get_data_manager().instance_list())

    def test_update_instance(self):
        instance = self.get_instance()
        self.get_data_manager().update_instance(instance, {'test_value': 3})
        instance = self.get_data_manager().find_instance_by_id(instance.id)
        self.assertEquals(3, instance.test_value)

    def test_delete_instance(self):
        instance = self.get_instance()
        self.get_data_manager().delete_instance(instance)
        self.assertEquals(0, len(self.get_data_manager().instance_list()))
