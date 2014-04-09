import numba.unittest_support as unittest
import itertools
import numpy as np
from numba.dummyarray import Array


class TestSlicing(unittest.TestCase):
    def assertSameContig(self, arr, nparr):
        attrs = 'C_CONTIGUOUS', 'F_CONTIGUOUS'
        for attr in attrs:
            if arr.flags[attr] != nparr.flags[attr]:
                print(arr.shape, nparr.shape)
                self.fail("contiguous flag mismatch:\ngot=%s\nexpect=%s" %
                          (arr.flags, nparr.flags))

    #### 1D

    def test_slice0_1d(self):
        nparr = np.empty(4)
        arr = Array.from_desc(0, nparr.shape, nparr.strides,
                              nparr.dtype.itemsize)
        self.assertSameContig(arr, nparr)
        xx = -2, -1, 0, 1, 2
        for x in xx:
            expect = nparr[x:]
            got = arr[x:]
            self.assertSameContig(got, expect)
            self.assertEqual(got.shape, expect.shape)
            self.assertEqual(got.strides, expect.strides)

    def test_slice1_1d(self):
        nparr = np.empty(4)
        arr = Array.from_desc(0, nparr.shape, nparr.strides,
                              nparr.dtype.itemsize)
        xx = -2, -1, 0, 1, 2
        for x in xx:
            expect = nparr[:x]
            got = arr[:x]
            self.assertSameContig(got, expect)
            self.assertEqual(got.shape, expect.shape)
            self.assertEqual(got.strides, expect.strides)

    def test_slice2_1d(self):
        nparr = np.empty(4)
        arr = Array.from_desc(0, nparr.shape, nparr.strides,
                              nparr.dtype.itemsize)
        xx = -2, -1, 0, 1, 2
        for x, y in itertools.product(xx, xx):
            expect = nparr[x:y]
            got = arr[x:y]
            self.assertSameContig(got, expect)
            self.assertEqual(got.shape, expect.shape)
            self.assertEqual(got.strides, expect.strides)

    #### 2D

    def test_slice0_2d(self):
        nparr = np.empty((4, 5))
        arr = Array.from_desc(0, nparr.shape, nparr.strides,
                              nparr.dtype.itemsize)
        xx = -2, -1, 0, 1, 2
        for x in xx:
            expect = nparr[x:]
            got = arr[x:]
            self.assertSameContig(got, expect)
            self.assertEqual(got.shape, expect.shape)
            self.assertEqual(got.strides, expect.strides)

        for x, y in itertools.product(xx, xx):
            expect = nparr[x:, y:]
            got = arr[x:, y:]
            self.assertSameContig(got, expect)
            self.assertEqual(got.shape, expect.shape)
            self.assertEqual(got.strides, expect.strides)

    def test_slice1_2d(self):
        nparr = np.empty((4, 5))
        arr = Array.from_desc(0, nparr.shape, nparr.strides,
                              nparr.dtype.itemsize)
        xx = -2, -1, 0, 1, 2
        for x in xx:
            expect = nparr[:x]
            got = arr[:x]
            self.assertSameContig(got, expect)
            self.assertEqual(got.shape, expect.shape)
            self.assertEqual(got.strides, expect.strides)

        for x, y in itertools.product(xx, xx):
            expect = nparr[:x, :y]
            got = arr[:x, :y]
            self.assertSameContig(got, expect)
            self.assertEqual(got.shape, expect.shape)
            self.assertEqual(got.strides, expect.strides)

    def test_slice2_2d(self):
        nparr = np.empty((4, 5))
        arr = Array.from_desc(0, nparr.shape, nparr.strides,
                              nparr.dtype.itemsize)
        xx = -2, -1, 0, 1, 2
        for s, t, u, v in itertools.product(xx, xx, xx, xx):
            expect = nparr[s:t, u:v]
            got = arr[s:t, u:v]
            self.assertSameContig(got, expect)
            self.assertEqual(got.shape, expect.shape)
            self.assertEqual(got.strides, expect.strides)

        for x, y in itertools.product(xx, xx):
            expect = nparr[s:t, u:v]
            got = arr[s:t, u:v]
            self.assertSameContig(got, expect)
            self.assertEqual(got.shape, expect.shape)
            self.assertEqual(got.strides, expect.strides)


class TestExtent(unittest.TestCase):
    def test_extent_1d(self):
        nparr = np.empty(4)
        arr = Array.from_desc(0, nparr.shape, nparr.strides,
                              nparr.dtype.itemsize)
        s, e = arr.extent
        self.assertEqual(e - s, nparr.size * nparr.dtype.itemsize)

    def test_extent_2d(self):
        nparr = np.empty((4, 5))
        arr = Array.from_desc(0, nparr.shape, nparr.strides,
                              nparr.dtype.itemsize)
        s, e = arr.extent
        self.assertEqual(e - s, nparr.size * nparr.dtype.itemsize)

    def test_extent_iter_1d(self):
        nparr = np.empty(4)
        arr = Array.from_desc(0, nparr.shape, nparr.strides,
                              nparr.dtype.itemsize)
        [ext] = list(arr.iter_contiguous_extent())
        self.assertEqual(ext, arr.extent)

    def test_extent_iter_2d(self):
        nparr = np.empty((4, 5))
        arr = Array.from_desc(0, nparr.shape, nparr.strides,
                              nparr.dtype.itemsize)
        [ext] = list(arr.iter_contiguous_extent())
        self.assertEqual(ext, arr.extent)

        self.assertEqual(len(list(arr[::2].iter_contiguous_extent())), 2)


if __name__ == '__main__':
    unittest.main()

