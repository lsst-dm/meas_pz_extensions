# This file is part of meas_photoz_algorithms.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

__all__ = [
    "EstimatePhotozCMNNAlgoConfig",
    "EstimatePhotozCMNNAlgoTask",
    "EstimatePhotozCMNNConfig",
    "EstimatePhotozCMNNTask",
]

from rail.estimation.algos.cmnn import CMNNEstimator
from rail.estimation.estimator import CatEstimator

import lsst.pex.config as pexConfig
from lsst.meas.photoz.base import (
    EstimatePhotozAlgoConfigBase,
    EstimatePhotozAlgoTask,
    EstimatePhotozTask,
    EstimatePhotozTaskConfig,
    photozAlgoRegistry,
)


class EstimatePhotozCMNNAlgoConfig(EstimatePhotozAlgoConfigBase):
    """Config for EstimatePhotozCMNNAlgoTask

    This will select and configure the CMNNEstimator p(z)
    estimation algorithm

    """

    @classmethod
    def estimator_class(cls) -> type[CatEstimator]:
        return CMNNEstimator

    @classmethod
    def stage_name(cls):
        return "cmnn"


EstimatePhotozCMNNAlgoConfig._make_fields()


@pexConfig.registerConfigurable(EstimatePhotozCMNNAlgoConfig.stage_name(), photozAlgoRegistry)
class EstimatePhotozCMNNAlgoTask(EstimatePhotozAlgoTask):
    """SubTask that runs RAIL CMNN algorithm for p(z) estimation

    See https://github.com/LSSTDESC/rail_cmnn/blob/main/src/rail/estimation/algos/cmnn.py
    for algorithm implementation.

    """

    ConfigClass = EstimatePhotozCMNNAlgoConfig
    _DefaultName = "estimatePZCMNNAlgo"


class EstimatePhotozCMNNConfig(EstimatePhotozTaskConfig):
    """Config for EstimatePhotozCMNNTask

    Overrides setDefaults to use CMNN algorithm
    """

    def setDefaults(self) -> None:
        super().setDefaults()
        name = EstimatePhotozCMNNAlgoConfig.stage_name()
        self.connections.algo = name
        self.photoz_algo = name


class EstimatePhotozCMNNTask(EstimatePhotozTask):
    """Task that runs RAIL CMNN algorithm for p(z) estimation"""

    ConfigClass = EstimatePhotozCMNNConfig
    _DefaultName = "estimatePZCMNN"
