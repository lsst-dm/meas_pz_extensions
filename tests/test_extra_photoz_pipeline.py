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

import os
import tempfile
import unittest
from typing import Any

from lsst.daf.butler import Butler, Config
from lsst.daf.butler.tests import DatastoreMock
from lsst.daf.butler.tests.utils import makeTestTempDir, removeTestTempDir
from lsst.pipe.base.tests.pipelineStepTester import PipelineStepTester

import lsst.meas.photoz.base.all_algos as all_algos_base
import lsst.meas.photoz.algorithms.all_algos as all_algos
from lsst.meas.photoz.base.estimate_photoz_task import EstimatePhotozConnections, photozAlgoRegistry

PIPELINES_DIR = os.path.join(os.path.dirname(__file__), "..", "pipelines")
TEST_DIR = os.path.abspath(os.path.dirname(__file__))
TEST_DATA_DIR = os.path.join(TEST_DIR, "data", "extras")


class MeasPzExtraPipelineTestCase(unittest.TestCase):
    """Test the PZ pipeline plumbing for partially supported algorithms.

    This uses the `PipelineStepTester` to test pipelines/photoz.yaml.

    This should include any algorithms that are wrapped in this package
    or in meas_photoz_base.
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

        expected_inputs = ["object"]
        expected_outputs = []
        inputs = [("object", {"skymap", "tract"}, "ArrowAstropy", False)]
        names = list(photozAlgoRegistry.keys())
        tasks = list(photozAlgoRegistry.values())
        all_tasks, all_tasks_base = (
            tuple(x for x in aa.__all__ if x != "photozAlgoRegistry") for aa in (all_algos, all_algos_base)
        )
        assert set(all_tasks).issuperset(set(all_tasks_base))
        assert len(names) == len(all_tasks)
        assert set(tasks) == set([getattr(all_algos, attr) for attr in all_tasks])

        for algo in names:
            dataset = EstimatePhotozConnections.photoz_model.name.format(algo=algo)
            expected_inputs.append(dataset)
            expected_outputs.append(EstimatePhotozConnections.photoz_ensemble.name.format(algo=algo))
            inputs.append((dataset, {"instrument"}, "PhotozModel", True))

        tester = PipelineStepTester(
            os.path.join(PIPELINES_DIR, "photoz.yaml"),
            ["#photoz_all"],
            inputs,
            expected_inputs=set(expected_inputs),
            expected_outputs=set(expected_outputs),
        )
        tester.run(butler, self)
