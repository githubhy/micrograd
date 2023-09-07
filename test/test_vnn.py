import torch
import numpy as np
from micrograd.vnn import Tensor as VTensor
from torch import Tensor as TTensor


def eq(l, r):
    if not isinstance(l, TTensor):
        l = TTensor(l)
    if not isinstance(r, TTensor):
        r = TTensor(r)
    return torch.allclose(l, r)


def test_add():
    x = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    y = np.array([[7.0, 8.0, 9.0], [10.0, 11.0, 12.0]])
    x0 = VTensor(x)
    y0 = VTensor(y)
    z0 = x0 + y0
    assert eq(x0.grad, [[0, 0, 0], [0, 0, 0]])
    assert eq(z0.data, [[8, 10, 12], [14, 16, 18]])

    x1 = TTensor(x)
    x1.requires_grad = True
    y1 = TTensor(y)
    y1.requires_grad = True
    z1 = x1 + y1
    z1.retain_grad()
    assert eq(z1.data, [[8, 10, 12], [14, 16, 18]])
    assert eq(z0.data, z1.data)

    z0.backward()
    z1.backward(TTensor(np.ones_like(z1.data)))
    assert eq(x0.grad, [[1, 1, 1], [1, 1, 1]])
    assert eq(x0.grad, x1.grad)
    assert eq(y0.grad, y1.grad)
    assert eq(z0.grad, z1.grad)


def test_sub():
    x = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    y = np.array([[7.0, 8.0, 9.0], [10.0, 11.0, 12.0]])
    x0 = VTensor(x)
    y0 = VTensor(y)
    z0 = x0 - y0
    assert eq(x0.grad, [[0, 0, 0], [0, 0, 0]])
    assert eq(z0.data, [[-6, -6, -6], [-6, -6, -6]])

    x1 = TTensor(x)
    x1.requires_grad = True
    y1 = TTensor(y)
    y1.requires_grad = True
    z1 = x1 - y1
    z1.retain_grad()
    assert eq(z1.data, [[-6, -6, -6], [-6, -6, -6]])
    assert eq(z0.data, z1.data)

    z0.backward()
    z1.backward(TTensor(np.ones_like(z1.data)))
    assert eq(x0.grad, [[1, 1, 1], [1, 1, 1]])
    assert eq(x1.grad, [[1, 1, 1], [1, 1, 1]])
    assert eq(x0.grad, x1.grad)
    assert eq(y0.grad, y1.grad)
    assert eq(z0.grad, z1.grad)


def test_truediv():
    x = np.array([[2.0, 3.0, 4.0], [5.0, 6.0, 7.0]])
    y = np.array([[8.0, 9.0, 12.0], [10.0, 18.0, 14.0]])
    x0 = VTensor(x)
    y0 = VTensor(y)
    z0 = x0 / y0
    assert eq(x0.grad, [[0, 0, 0], [0, 0, 0]])
    assert eq(z0.data, [[1 / 4, 1 / 3, 1 / 3], [1 / 2, 1 / 3, 1 / 2]])

    x1 = TTensor(x)
    x1.requires_grad = True
    y1 = TTensor(y)
    y1.requires_grad = True
    z1 = x1 / y1
    z1.retain_grad()
    assert eq(z1.data, [[1 / 4, 1 / 3, 1 / 3], [1 / 2, 1 / 3, 1 / 2]])
    assert eq(z0.data, z1.data)

    z0.backward()
    z1.backward(TTensor(np.ones_like(z1.data)))
    assert eq(x0.grad, [[1 / 8, 1 / 9, 1 / 12], [1 / 10, 1 / 18, 1 / 14]])
    assert eq(x1.grad, [[1 / 8, 1 / 9, 1 / 12], [1 / 10, 1 / 18, 1 / 14]])
    assert eq(x0.grad, x1.grad)
    assert eq(y0.grad, y1.grad)
    assert eq(z0.grad, z1.grad)


def test_matmul():
    x = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])  # (2, 3)
    y = np.expand_dims(np.array([7.0, 8.0, 9.0]), axis=1)  # (3, 1)
    x0 = VTensor(x)
    y0 = VTensor(y)
    z0 = x0 @ y0
    assert eq(x0.grad, [[0, 0, 0], [0, 0, 0]])
    assert eq(z0.data, [[50], [122]])

    x1 = TTensor(x)
    x1.requires_grad = True
    y1 = TTensor(y)
    y1.requires_grad = True
    z1 = x1 @ y1
    z1.retain_grad()
    assert eq(z1.data, [[50], [122]])
    assert eq(z0.data, z1.data)

    z0.backward()
    z1.backward(TTensor(np.ones_like(z1.data)))
    assert eq(x0.grad, [[7, 8, 9], [7, 8, 9]])
    assert eq(x0.grad, x1.grad)
    assert eq(y0.grad, y1.grad)
    assert eq(z0.grad, z1.grad)
