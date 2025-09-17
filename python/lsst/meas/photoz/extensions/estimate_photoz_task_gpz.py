# This file is part of meas_photoz_extensions.
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
    "EstimatePhotozGPZAlgoConfig",
    "EstimatePhotozGPZAlgoTask",
    "EstimatePhotozGPZConfig",
    "EstimatePhotozGPZTask",
]

from rail.estimation.algos.gpz import GPzEstimator
from rail.estimation.estimator import CatEstimator

from lsst.meas.photoz.base import (
    EstimatePhotozAlgoConfigBase,
    EstimatePhotozAlgoTask,
    EstimatePhotozTask,
    EstimatePhotozTaskConfig,
)


class EstimatePhotozGPZAlgoConfig(EstimatePhotozAlgoConfigBase):
    """Config for EstimatePhotozGPZAlgoTask

    This will select and configure the GPzEstimator p(z)
    estimation algorithm

    """

    @classmethod
    def estimator_class(cls) -> type[CatEstimator]:
        return GPzEstimator


EstimatePhotozGPZAlgoConfig._make_fields()


class EstimatePhotozGPZAlgoTask(EstimatePhotozAlgoTask):
    """SubTask that runs RAIL GPZ algorithm for p(z) estimation

    See https://github.com/LSSTDESC/rail_gpz_v1/blob/src/rail/estimation/algos/gpz.py
    for algorithm implementation.

    """

    ConfigClass = EstimatePhotozGPZAlgoConfig
    _DefaultName = "estimatePZGPZAlgo"


class EstimatePhotozGPZConfig(EstimatePhotozTaskConfig):
    """Config for EstimatePhotozGPZTask

    Overrides setDefaults to use GPZ algorithm
    """

    def setDefaults(self) -> None:
        self.photoz_algo.retarget(EstimatePhotozGPZAlgoTask)
        self.photoz_algo.stage_name = "gpz"
        self.photoz_algo.output_mode = "return"
        self.photoz_algo.bands_to_convert = ["u", "g", "r", "i", "z", "y"]
        self.photoz_algo.ref_band = self.photoz_algo.mag_template.format(band='i')
        self.photoz_algo.bands = self.photoz_algo.get_mag_name_list()
        self.photoz_algo.err_bands = self.photoz_algo.get_mag_err_name_list()
        self.photoz_algo.mag_limits = self.photoz_algo.get_mag_lim_dict()
        self.photoz_algo.band_a_env = self.photoz_algo.get_band_a_env_dict()
        self.photoz_algo.replace_error_vals = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1]


class EstimatePhotozGPZTask(EstimatePhotozTask):
    """Task that runs RAIL GPZ algorithm for p(z) estimation"""

    ConfigClass = EstimatePhotozGPZConfig
    _DefaultName = "estimatePZGPZ"
