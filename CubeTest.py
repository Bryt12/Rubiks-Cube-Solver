import unittest
from cube import Cube
import numpy as np


class MyTestCase(unittest.TestCase):
    def test_inverse_work(self):
        c = Cube()
        start = c.cube.copy()
        c.u()
        c.u(False)
        c.d()
        c.d(False)
        c.r()
        c.r(False)
        c.l()
        c.l(False)
        c.f()
        c.f(False)
        c.b()
        c.b(False)

        self.assertTrue(np.array_equal(start, c.cube))


if __name__ == '__main__':
    unittest.main()
