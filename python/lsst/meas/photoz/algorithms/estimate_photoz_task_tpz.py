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
    "EstimatePhotozTPZAlgoConfig",
    "EstimatePhotozTPZAlgoTask",
    "EstimatePhotozTPZConfig",
    "EstimatePhotozTPZTask",
]

from rail.estimation.algos.tpz_lite import TPZliteEstimator
from rail.estimation.estimator import CatEstimator

import lsst.pex.config as pexConfig
from lsst.meas.photoz.base import (
    EstimatePhotozAlgoConfigBase,
    EstimatePhotozAlgoTask,
    EstimatePhotozTask,
    EstimatePhotozTaskConfig,
    photozAlgoRegistry,
)


class EstimatePhotozTPZAlgoConfig(EstimatePhotozAlgoConfigBase):
    """Config for EstimatePhotozTPZAlgoTask
    This will select and configure the TPZliteEstimator p(z)
    estimation algorithm

    See https://github.com/LSSTDESC/rail_tpz/blob/src/rail/estimation/algos/tpz_lite.py
    for parameters and default values.
    """

    @classmethod
    def estimator_class(cls) -> type[CatEstimator]:
        return TPZliteEstimator

    @classmethod
    def stage_name(cls):
        return "tpz"

    def _finalize(self):
        super()._finalize()
        mag_names = self.get_mag_names()
        mag_err_names = self.get_mag_err_names()
        self.err_dict = {mag_names[band]: mag_err_names[band] for band in self.bands_to_convert}


EstimatePhotozTPZAlgoConfig._make_fields()


@pexConfig.registerConfigurable(EstimatePhotozTPZAlgoConfig.stage_name(), photozAlgoRegistry)
class EstimatePhotozTPZAlgoTask(EstimatePhotozAlgoTask):
    """SubTask that runs RAIL TPZ algorithm for p(z) estimation

    See https://github.com/LSSTDESC/rail_tpz/blob/src/rail/estimation/algos/tpz_lite.py
    for parameters and default values.
    """

    ConfigClass = EstimatePhotozTPZAlgoConfig
    _DefaultName = "estimatePZTPZAlgo"


class EstimatePhotozTPZConfig(EstimatePhotozTaskConfig):
    """Config for EstimatePhotozTPZTask

    Overrides setDefaults to use TPZ algorithm
    """

    def setDefaults(self) -> None:
        super().setDefaults()
        name = EstimatePhotozTPZAlgoConfig.stage_name()
        self.connections.algo = name
        self.photoz_algo = name


class EstimatePhotozTPZTask(EstimatePhotozTask):
    """Task that runs RAIL TPZ algorithm for p(z) estimation"""

    ConfigClass = EstimatePhotozTPZConfig
    _DefaultName = "estimatePZTPZ"
