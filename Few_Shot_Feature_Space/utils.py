# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/utils.ipynb.

# %% auto 0
__all__ = ['ClassFeatures', 'plot_hist']

# %% ../nbs/utils.ipynb 2
from dataclasses import dataclass

from torch import Tensor

from fastai.vision.all import *


@dataclass
class ClassFeatures(object):
    ftrs: Tensor

    @classmethod
    def compute(cls, dl, fe, min_samples=0):
        fe.cuda().eval().requires_grad_(False)
        features, targets = L((fe(x), y) for x, y in progress_bar(dl)).zip().map(torch.cat)
        return {t.item(): cls(features[targets==t].as_subclass(Tensor).detach())
                for t in targets.unique() if features[targets==t].size(0) > min_samples}

    @property
    def centroid(self):
        return self.ftrs.mean(0)

# %% ../nbs/utils.ipynb 3
from scipy.stats import norm
import matplotlib.pyplot as plt


def plot_hist(angles, fit_gausiann=True):
    _, bins, _ = plt.hist(angles, bins=100, label='Angle', alpha=.5, edgecolor='black', lw=1, density=True)
    if fit_gausiann:
        mu, sigma = norm.fit(angles)
        y = norm.pdf(bins, mu, sigma)
        plt.plot(bins, y)
