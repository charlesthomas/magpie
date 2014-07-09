from base import BaseTest

class Test(BaseTest):
    def test_proof_of_concept(self):
        res = self.fetch('/')
        self.assertEqual(200, int(res.code))
