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

"""Test the PZ pipeline tasks for  partially supported algorithms.

This will run the pipeline tasks against a dataset
in /repo/dc2.

This should include any algorithms that are wrapped in meas_photoz.

For now that is cmnn, gpz, dnf, fzboost, gpz, tpz, and lephare
"""

import os
from typing import Any

import pytest

from lsst.daf.butler import Butler
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

from lsst.meas.photoz.algorithms.tests.utils import run_pz_task_s3df

TEST_DIR = os.path.abspath(os.path.dirname(__file__))
TEST_DATA_DIR = os.path.join(TEST_DIR, "data")
DAF_BUTLER_REPOSITORY_INDEX = os.environ.get("DAF_BUTLER_REPOSITORY_INDEX", None)
IS_S3DF = DAF_BUTLER_REPOSITORY_INDEX == "/sdf/group/rubin/shared/data-repos.yaml"


def makeButler_repo_dp1(**kwargs: Any) -> Butler:
    butler = Butler.from_config(
        "/repo/dp1_prep",
        collections=["LSSTComCam/runs/DRP/DP1/v29_0_0/DM-50260"],
        **kwargs,
    )
    return butler


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
@pytest.mark.skipif(not IS_S3DF, reason="Not at S3DF")
def test_pz_task_s3df(
    algo_name: str,
    model_file: str,
    estimator_class: type[EstimatePhotozTask],
) -> None:
    if estimator_class is None:
        pytest.skip(f"Missing {algo_name} in env")
    butler = makeButler_repo_dp1()
    run_pz_task_s3df(algo_name, butler, model_file, estimator_class)
