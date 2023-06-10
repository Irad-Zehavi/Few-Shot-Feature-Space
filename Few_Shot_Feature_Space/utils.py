# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/utils.ipynb.

# %% auto 0
__all__ = ['fr_feature_extractors', 'fr_dataloaders', 'ClassFeatures', 'plot_hist']

# %% ../nbs/utils.ipynb 2
from fastai.vision.all import *

from similarity_learning.all import *


def fr_feature_extractors():
    return [cut_model_by_name(FaceNetInceptionResnetV1(pretrained, classify=False), 'last_bn')
            for pretrained in ['vggface2', 'casia-webface']]


def fr_dataloaders():
    return (LFWPeople().all().train.dl(),
            PinterestFaces(splitter=IndexSplitter([])).train.dl())


# %% ../nbs/utils.ipynb 3
from dataclasses import dataclass

from torch import Tensor

from fastai.vision.all import *


class ClassFeatures(Tensor):
    @classmethod
    def compute(cls, dl, fe, min_samples=0):
        fe.cuda().eval().requires_grad_(False)
        features, targets = L((fe(x), y) for x, y in progress_bar(dl)).zip().map(torch.cat)
        return {t.item(): cls(features[targets==t].as_subclass(Tensor).detach())
                for t in targets.unique() if features[targets==t].size(0) > min_samples}

    @property
    def centroid(self):
        return self.mean(0)

# %% ../nbs/utils.ipynb 4
from scipy.stats import norm
import matplotlib.pyplot as plt


def plot_hist(angles, fit_gausiann=True, ax=None):
    ax = ax or plt.subplot()
    _, bins, _ = ax.hist(angles, bins='auto', label='Angle', alpha=.5, edgecolor='black', lw=1, density=True)
    if fit_gausiann:
        mu, sigma = norm.fit(angles)
        y = norm.pdf(bins, mu, sigma)
        ax.plot(bins, y)

    return ax
