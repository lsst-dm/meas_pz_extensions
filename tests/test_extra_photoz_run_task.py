# This file is part of meas_photoz_algorithms
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Unit tests for meaz_pz"""

import pytest
from astropy.table import Table
from lsst.meas.photoz.base import EstimatePhotozTask

try:
    from lsst.meas.photoz.base.estimate_photoz_task_bpz import EstimatePhotozBPZTask
except ImportError:
    EstimatePhotozBPZTask = None

try:
    from lsst.meas.photoz.algorithms.estimate_photoz_task_cmnn import EstimatePhotozCMNNTask
except ImportError:
    EstimatePhotozCMNNTask = None

try:
    from lsst.meas.photoz.algorithms.estimate_photoz_task_dnf import EstimatePhotozDNFTask
except ImportError:
    EstimatePhotozDNFTask = None

try:
    from lsst.meas.photoz.algorithms.estimate_photoz_task_fzboost import EstimatePhotozFZBoostTask
except ImportError:
    EstimatePhotozFZBoostTask = None

try:
    from lsst.meas.photoz.algorithms.estimate_photoz_task_gpz import EstimatePhotozGPZTask
except ImportError:
    EstimatePhotozGPZTask = None

try:
    from lsst.meas.photoz.algorithms.estimate_photoz_task_lephare import EstimatePhotozLephareTask
except ImportError:
    EstimatePhotozLephareTask = None

try:
    from lsst.meas.photoz.algorithms.estimate_photoz_task_tpz import EstimatePhotozTPZTask
except ImportError:
    EstimatePhotozTPZTask = None

from lsst.meas.photoz.algorithms.tests import utils


@pytest.mark.parametrize(
    "algo_name,model_file,estimator_class",
    [
        ("bpz", "models/hsc/model_inform_bpz_wrap.pickle", EstimatePhotozBPZTask),
        # (
        #    "cmnn",
        #    "models/hsc/model_inform_cmnn_wrap.pickle",
        #    EstimatePhotozCMNNTask
        # ),
        ("dnf", "models/hsc/model_inform_dnf_wrap.pickle", EstimatePhotozDNFTask),
        (
            "fzboost",
            "models/hsc/model_inform_fzboost_wrap.pickle",
            EstimatePhotozFZBoostTask,
        ),
        ("gpz", "models/hsc/model_inform_gpz_wrap.pickle", EstimatePhotozGPZTask),
        # (
        #    "lephare",
        #    "models/hsc/model_inform_lephare_wrap.pickle",
        #    EstimatePhotozLephareTask,
        # ),
        ("tpz", "models/hsc/model_inform_tpz_wrap.pickle", EstimatePhotozTPZTask),
    ],
)
def test_pz_task_hsc(
    hsc_dataset: Table,
    algo_name: str,
    model_file: str,
    estimator_class: type[EstimatePhotozTask],
) -> None:
    if estimator_class is None:
        pytest.skip(f"Missing {algo_name} in env")
    assert hsc_dataset is not None
    utils.do_pz_task(
        algo_name=algo_name,
        model_file=model_file,
        data=hsc_dataset,
        estimator_class=estimator_class,
        config_callback=utils.hsc_config_callback,
        check_callback=utils.hsc_check_callback,
    )


@pytest.mark.parametrize(
    "algo_name,model_file,estimator_class",
    [
        ("bpz", "models/dc2/model_inform_bpz_wrap.pickle", EstimatePhotozBPZTask),
        # (
        #    "cmnn",
        #    "models/dc2/model_inform_cmnn_wrap.pickle",
        #    EstimatePhotozCMNNTask
        # ),
        ("dnf", "models/dc2/model_inform_dnf_wrap.pickle", EstimatePhotozDNFTask),
        (
            "fzboost",
            "models/dc2/model_inform_fzboost_wrap.pickle",
            EstimatePhotozFZBoostTask,
        ),
        ("gpz", "models/dc2/model_inform_gpz_wrap.pickle", EstimatePhotozGPZTask),
        # (
        #    "lephare",
        #    "models/dc2/model_inform_lephare_wrap.pickle",
        #    EstimatePhotozLephareTask,
        # ),
        ("tpz", "models/dc2/model_inform_tpz_wrap.pickle", EstimatePhotozTPZTask),
    ],
)
def test_pz_task_dc2(
    dc2_dataset: Table,
    algo_name: str,
    model_file: str,
    estimator_class: type[EstimatePhotozTask],
) -> None:
    if estimator_class is None:
        pytest.skip(f"Missing {algo_name} in env")
    assert dc2_dataset is not None
    utils.do_pz_task(
        algo_name=algo_name,
        model_file=model_file,
        data=dc2_dataset,
        estimator_class=estimator_class,
        config_callback=utils.dc2_config_callback,
        check_callback=utils.dc2_check_callback,
    )


@pytest.mark.parametrize(
    "algo_name,model_file,estimator_class",
    [
        ("bpz", "models/com_cam/model_inform_bpz_wrap.pickle", EstimatePhotozBPZTask),
        # (
        #     "cmnn",
        #     "models/com_cam/model_inform_cmnn_wrap.pickle",
        #     EstimatePhotozCMNNTask
        # ),
        ("dnf", "models/com_cam/model_inform_dnf_wrap.pickle", EstimatePhotozDNFTask),
        (
            "fzboost",
            "models/com_cam/model_inform_fzboost_wrap.pickle",
            EstimatePhotozFZBoostTask,
        ),
        ("gpz", "models/com_cam/model_inform_gpz_wrap.pickle", EstimatePhotozGPZTask),
        # (
        #     "lephare",
        #     "models/com_cam/model_inform_lephare_wrap.pickle",
        #     EstimatePhotozLephareTask,
        # ),
        ("tpz", "models/com_cam/model_inform_tpz_wrap.pickle", EstimatePhotozTPZTask),
    ],
)
def test_pz_task_com_cam(
    com_cam_dataset: Table,
    algo_name: str,
    model_file: str,
    estimator_class: type[EstimatePhotozTask],
) -> None:
    if estimator_class is None:
        pytest.skip(f"Missing {algo_name} in env")
    assert com_cam_dataset is not None
    utils.do_pz_task(
        algo_name=algo_name,
        model_file=model_file,
        data=com_cam_dataset,
        estimator_class=estimator_class,
        config_callback=utils.com_cam_config_callback,
        check_callback=utils.com_cam_check_callback,
    )
