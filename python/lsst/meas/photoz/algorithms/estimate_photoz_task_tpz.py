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

import rail.estimation.algos.tpz_lite as tpz_lite
from rail.estimation.algos.tpz_lite import TPZliteEstimator
from rail.estimation.estimator import CatEstimator

from ceci.config import StageConfig as CeciStageConfig
from ceci.config import StageParameter as CeciParam

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

    """
    bands = pexConfig.ListField[str](
        doc="Bands to fit. Must correspond to magnitude fields in bands_to_convert.",
        default=["u", "g", "r", "i", "z", "y"],
    )

    ""
    @property
    def bands(self):
        return tpz_lite.bands
    
    @bands.setter
    def bands(self, bands):
        self.bands_to_convert = bands

    @classmethod
    def _make_fields(cls) -> None:
        ""Import the RAIL estimation stage.

        This method loops through the stage config parameters and converts
        RAIL/Ceci parameters to corresponding pex.config parameters.

        It should be called exactly once, immediately after the definition
        of every subclass of this base class.
        ""
        if hasattr(cls, "__fields_made__"):
            if cls.__fields_made__ is not True:
                raise RuntimeError(f"{cls.__fields_made__=} exists but is not True")
            raise RuntimeError(f"{cls=} called _make_fields twice")
        stage_class = cls.estimator_class()
        for key, val in stage_class.config_options.items():
            print(key, val)
            if isinstance(val, CeciStageConfig):
                val = val.get(key)
            if isinstance(val, CeciParam):
                if val.dtype in [bool, int, float, str]:
                    if (attr := getattr(cls, key, None)) is not None:
                        if not isinstance(attr, pexConfig.Field):
                            raise RuntimeError(f"{cls=} {key=} exists but is of {type(key)=}, not Field")
                        elif attr.dtype != val.dtype:
                            raise RuntimeError(f"{cls=} {key=} exists but {attr.dtype=} != {val.dtype=}")
                        attr.default = val.default
                        attr.doc = f"{val.msg} (overriding base doc='{attr.doc}')"
                    else:
                        setattr(
                            cls,
                            key,
                            pexConfig.Field(doc=val.msg, dtype=val.dtype, default=val.default),
                        )
                elif val.dtype in [list]:
                    # this is a hack, but it works.
                    if val.default:
                        item_type = type(val.default[0])
                    else:
                        item_type = str
                    setattr(
                        cls,
                        key,
                        pexConfig.ListField(doc=val.msg, dtype=item_type, default=val.default),
                    )
                elif val.dtype in [dict]:
                    setattr(
                        cls,
                        key,
                        pexConfig.DictField(doc=val.msg, keytype=str, default=val.default),
                    )
            print(getattr(cls, key, None))
        cls.__fields_made__ = True
    """

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
