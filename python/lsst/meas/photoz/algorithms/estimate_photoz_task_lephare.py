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
    "EstimatePhotozLephareAlgoConfig",
    "EstimatePhotozLephareAlgoTask",
    "EstimatePhotozLephareConfig",
    "EstimatePhotozLephareTask",
]

from rail.estimation.algos.lephare import LephareEstimator
from rail.estimation.estimator import CatEstimator

import lsst.pex.config as pexConfig
from lsst.meas.photoz.base import (
    EstimatePhotozAlgoConfigBase,
    EstimatePhotozAlgoTask,
    EstimatePhotozTask,
    EstimatePhotozTaskConfig,
    photozAlgoRegistry,
)


class EstimatePhotozLephareAlgoConfig(EstimatePhotozAlgoConfigBase):
    """Config for EstimatePhotozLephareAlgoTask

    This will select and configure the LephareEstimator p(z)
    estimation algorithm

    """

    @classmethod
    def estimator_class(cls) -> type[CatEstimator]:
        return LephareEstimator

    @classmethod
    def stage_name(cls):
        return "lephare"


EstimatePhotozLephareAlgoConfig._make_fields()


@pexConfig.registerConfigurable(EstimatePhotozLephareAlgoConfig.stage_name(), photozAlgoRegistry)
class EstimatePhotozLephareAlgoTask(EstimatePhotozAlgoTask):
    """SubTask that runs RAIL Lephare algorithm for p(z) estimation

    See https://github.com/LSSTDESC/rail_lephare/blob/src/rail/estimation/algos/lephare.py
    for algorithm implementation.

    Lephare estimates the p(z) distribution by taking
    a weighted mixture of the nearest neigheboors in
    color space.
    """

    ConfigClass = EstimatePhotozLephareAlgoConfig
    _DefaultName = "estimatePZLephareAlgo"


class EstimatePhotozLephareConfig(EstimatePhotozTaskConfig):
    """Config for EstimatePhotozLephareTask

    Overrides setDefaults to use Lephare algorithm
    """

    def setDefaults(self) -> None:
        super().setDefaults()
        name = EstimatePhotozLephareAlgoConfig.stage_name()
        self.connections.algo = name
        self.photoz_algo = name


class EstimatePhotozLephareTask(EstimatePhotozTask):
    """Task that runs RAIL Lephare algorithm for p(z) estimation"""

    ConfigClass = EstimatePhotozLephareConfig
    _DefaultName = "estimatePZLephare"
