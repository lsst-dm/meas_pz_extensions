# This file is part of meas.photoz.base.
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

from lsst.meas.photoz.base.all_algos import *  # noqa: F403
from lsst.meas.photoz.base.all_algos import __all__ as __all_base__

from .estimate_photoz_task_cmnn import EstimatePhotozCMNNAlgoTask
from .estimate_photoz_task_dnf import EstimatePhotozDNFAlgoTask
from .estimate_photoz_task_fzboost import EstimatePhotozFZBoostAlgoTask
from .estimate_photoz_task_gpz import EstimatePhotozGPZAlgoTask
from .estimate_photoz_task_lephare import EstimatePhotozLephareAlgoTask
from .estimate_photoz_task_tpz import EstimatePhotozTPZAlgoTask

__all__ = [
    "EstimatePhotozCMNNAlgoTask",
    "EstimatePhotozDNFAlgoTask",
    "EstimatePhotozFZBoostAlgoTask",
    "EstimatePhotozGPZAlgoTask",
    "EstimatePhotozLephareAlgoTask",
    "EstimatePhotozTPZAlgoTask",
]
__all__ += __all_base__
