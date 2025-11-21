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
    "EstimatePhotozFZBoostAlgoConfig",
    "EstimatePhotozFZBoostAlgoTask",
    "EstimatePhotozFZBoostConfig",
    "EstimatePhotozFZBoostTask",
]

from rail.estimation.algos.flexzboost import FlexZBoostEstimator
from rail.estimation.estimator import CatEstimator

import lsst.pex.config as pexConfig
from lsst.meas.photoz.base import (
    EstimatePhotozAlgoConfigBase,
    EstimatePhotozAlgoTask,
    EstimatePhotozTask,
    EstimatePhotozTaskConfig,
    photozAlgoRegistry,
)


class EstimatePhotozFZBoostAlgoConfig(EstimatePhotozAlgoConfigBase):
    """Config for EstimatePhotozFZBoostAlgoTask

    This will select and configure the FlexZBoostEstimator p(z)
    estimation algorithm

    """

    @classmethod
    def estimator_class(cls) -> type[CatEstimator]:
        return FlexZBoostEstimator

    @classmethod
    def stage_name(cls):
        return "fzboost"


EstimatePhotozFZBoostAlgoConfig._make_fields()


@pexConfig.registerConfigurable(EstimatePhotozFZBoostAlgoConfig.stage_name(), photozAlgoRegistry)
class EstimatePhotozFZBoostAlgoTask(EstimatePhotozAlgoTask):
    """SubTask that runs RAIL FZBoost algorithm for p(z) estimation

    See https://github.com/LSSTDESC/rail_flexzboost/blob/main/src/rail/estimation/algos/flexzboost.py
    for algorithm implementation.

    """

    ConfigClass = EstimatePhotozFZBoostAlgoConfig
    _DefaultName = "estimatePZFZBoostAlgo"


class EstimatePhotozFZBoostConfig(EstimatePhotozTaskConfig):
    """Config for EstimatePhotozFZBoostTask

    Overrides setDefaults to use FZBoost algorithm
    """

    def setDefaults(self) -> None:
        super().setDefaults()
        name = EstimatePhotozFZBoostAlgoConfig.stage_name()
        self.connections.algo = name
        self.photoz_algo = name


class EstimatePhotozFZBoostTask(EstimatePhotozTask):
    """Task that runs RAIL FZBoost algorithm for p(z) estimation"""

    ConfigClass = EstimatePhotozFZBoostConfig
    _DefaultName = "estimatePZFZBoost"
