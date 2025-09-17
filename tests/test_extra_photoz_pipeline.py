# This file is part of meas_photoz_extensions
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

import os
import tempfile
import unittest
from typing import Any

from lsst.daf.butler import Butler, Config
from lsst.daf.butler.tests import DatastoreMock
from lsst.daf.butler.tests.utils import makeTestTempDir, removeTestTempDir
from lsst.pipe.base.tests.pipelineStepTester import PipelineStepTester

PIPELINES_DIR = os.path.join(os.path.dirname(__file__), "..", "pipelines")
TEST_DIR = os.path.abspath(os.path.dirname(__file__))
TEST_DATA_DIR = os.path.join(TEST_DIR, "data", "extras")


class MeasPzExtraPipelineTestCase(unittest.TestCase):
    """Test the PZ pipeline plumbing for partially supported algorithms.

    This uses the `PipelineStepTester` to test
    a test pipeline define in tests/data/photoz_all_lsst.yaml

    This should include any algorithms that are wrapped in meas_photoz.

    For now that is cmnn, gpz, dnf, fzboost, gpz, tpz, and lephare
    """

    def setUp(self) -> None:
        self.root = makeTestTempDir(TEST_DATA_DIR)
        self.maxDiff = None

    def tearDown(self) -> None:
        removeTestTempDir(self.root)

    def makeButler(self, **kwargs: Any) -> Butler:
        """Return new Butler instance on each call."""
        config = Config()

        # make separate temporary directory for registry of this instance
        tmpdir = tempfile.mkdtemp(dir=self.root)
        config["registry", "db"] = f"sqlite:///{tmpdir}/gen3.sqlite3"
        config = Butler.makeRepo(self.root, config)
        butler = Butler.from_config(config, **kwargs)
        DatastoreMock.apply(butler)
        return butler

    def test_extra_pz_pipeline(self) -> None:
        butler = self.makeButler(writeable=True)

        tester = PipelineStepTester(
            os.path.join(TEST_DATA_DIR, "photoz_all_lsst.yaml"),
            ["#photoz_all"],
            [
                ("object", {"skymap", "tract"}, "ArrowAstropy", False),
                ("photozModel_bpz", {"instrument"}, "PhotozModel", True),
                ("photozModel_dnf", {"instrument"}, "PhotozModel", True),
                ("photozModel_fzboost", {"instrument"}, "PhotozModel", True),
                ("photozModel_gpz", {"instrument"}, "PhotozModel", True),
                ("photozModel_tpz", {"instrument"}, "PhotozModel", True),
                ("photozModel_lephare", {"instrument"}, "PhotozModel", True),
                ("photozModel_cmnn", {"instrument"}, "PhotozModel", True),
            ],
            expected_inputs={
                "object",
                "photozModel_bpz",
                "photozModel_dnf",
                "photozModel_fzboost",
                "photozModel_gpz",
                "photozModel_tpz",
                "photozModel_lephare",
                "photozModel_cmnn",
            },
            expected_outputs={
                "photoz_estimate_bpz",
                "photoz_estimate_dnf",
                "photoz_estimate_fzboost",
                "photoz_estimate_gpz",
                "photoz_estimate_tpz",
                "photoz_estimate_lephare",
                "photoz_estimate_cmnn",
            },
        )
        tester.run(butler, self)
