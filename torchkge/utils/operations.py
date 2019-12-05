# -*- coding: utf-8 -*-
"""
Copyright TorchKGE developers
@author: Armand Boschin <aboschin@enst.fr>
"""

from torch import cat, zeros


def get_mask(length, start, end):
    """Create a mask of length `length` filled with 0s except between indices `start` (included)\
    and `end` (excluded).

    Parameters
    ----------
    length: int
        Length of the mask to be created.
    start: int
        First index (included) where the mask will be filled with 0s.
    end: int
        Last index (excluded) where the mask will be filled with 0s.

    Returns
    -------
    mask: `torch.Tensor`, shape: (length), dtype: `torch.bool`
        Mask of length `length` filled with 0s except between indices `start` (included)\
        and `end` (excluded).
    """
    mask = zeros(length)
    mask[[i for i in range(start, end)]] = 1
    return mask.bool()


def get_rank(data, true, low_values=False):
    """Computes how many entities have higher (or lower) value in data than the one at index true[i]

    Parameters
    ----------
    data: `torch.Tensor`, dtype: `torch.float`, shape: (n_facts, dimensions)
        Scores for each entity.
    true: `torch.Tensor`, dtype: `torch.int`, shape: (n_facts)
        true[i] is the index of the true entity for test i of the batch.
    low_values: bool, optional (default=False)
        if True, best rank is the lowest score else it is the highest.

    Returns
    -------
    ranks: `torch.Tensor`, dtype: `torch.int`, shape: (n_facts)
        ranks[i] is the number of entities which have better scores in data than the one and index true[i]
    """
    true_data = data.gather(1, true.long().view(-1, 1))

    if low_values:
        return (data <= true_data).sum(dim=1)
    else:
        return (data >= true_data).sum(dim=1)


def get_rolling_matrix(x):
    """Build a rolling matrix.

    Parameters
    ----------
    x: `torch.Tensor`, shape: (b_size, dim)

    Returns
    -------
    mat: `torch.Tensor`, shape: (b_size, dim, dim)
        Rolling matrix such that mat[i,j] = x[i - j mod(dim)]
    """
    b_size, dim = x.shape
    x = x.view(b_size, 1, dim)
    return cat([x.roll(i, dims=2) for i in range(dim)], dim=1)
