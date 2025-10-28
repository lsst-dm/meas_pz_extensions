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
import subprocess
import unittest
from typing import Any

import qp

from lsst.daf.butler import (
    Butler,
    DataCoordinate,
    DatasetRef,
    DatasetType,
    DimensionGroup,
    DimensionUniverse,
    FileDataset,
)

PIPELINES_DIR = os.path.join(os.path.dirname(__file__), "..", "pipelines")
CI_HSC_GEN3_DIR = os.environ.get("CI_HSC_GEN3_DIR", None)
USER = os.environ.get("USER", "MysteriousStanger")


algorithms = (
    "bpz",
    # "cmnn", # works but takes 5-10 min
    "dnf",
    "fzboost",
    "gpz",
    # "lephare", # slow and doesn't work
    # "tpz", # doesn't work, not sure why
)

dim_universe = DimensionUniverse()
patch_dimensions = DimensionGroup(
    dim_universe,
    ["skymap", "tract", "patch"],
)
instrument_dimensions = DimensionGroup(
    dim_universe,
    ["instrument"],
)


class MeasPzTasksTestCase(unittest.TestCase):
    """Test the PZ pipeline tasks for fully supported algorithms.

    This will run the pipeline tasks against CI_HSC_GEN3

    This should include any algorithms that are wrapped in meas_photoz.

    For now that is knn and trainz.
    """

    dim_universe = DimensionUniverse()

    objectTable_datasetType = DatasetType(
        "objectTable",
        dimensions=patch_dimensions,
        storageClass="ArrowAstropy",
    )

    photoz_model_datasetTypes = {
        algo: DatasetType(
            f"photoz_model_{algo}",
            dimensions=instrument_dimensions,
            storageClass="PhotozModel",
            isCalibration=True,
        )
        for algo in algorithms
    }

    model_files = {algo: f"models/hsc/model_inform_{algo}_wrap.pickle" for algo in algorithms}

    output_datasetTypes = {algo: f"photoz_ensemble_{algo}" for algo in algorithms}

    task_labels = {algo: f"photoz_{algo}" for algo in algorithms}

    def makeButler_ci_hsc(self, **kwargs: Any) -> Butler:
        assert CI_HSC_GEN3_DIR
        butler = Butler.from_config(
            os.path.abspath(os.path.join(CI_HSC_GEN3_DIR, "DATA")), **kwargs
        )
        return butler

    @unittest.skipIf(CI_HSC_GEN3_DIR is None, "CI_HSC_GEN3 not installed")
    def test_pz_tasks_ci_hsc(self) -> None:
        assert CI_HSC_GEN3_DIR
        to_delete = []

        butler = self.makeButler_ci_hsc(writeable=True)
        collection_models = f"u/{USER}/pz_models"

        butler.registry.registerRun(collection_models)
        for algo, model_file in self.model_files.items():
            datasetType = self.photoz_model_datasetTypes[algo]
            print(f"registering {model_file}")
            modelpath = os.path.abspath(
                os.path.expandvars(
                    os.path.join("${TESTDATA_RAIL_DIR}", model_file),
                )
            )

            butler.registry.registerDatasetType(datasetType)
            dataset_ref = DatasetRef(
                datasetType,
                DataCoordinate.from_full_values(
                    instrument_dimensions,
                    ("HSC",),
                ),
                run=collection_models,
            )
            butler.ingest(FileDataset(modelpath, dataset_ref))

        pipeline = os.path.join(PIPELINES_DIR, "photoz.yaml#")
        configs = []
        for task_label in self.task_labels.values():
            configs.extend([
                "-c", f"{task_label}:connections.objects=objectTable_tract",
                "-c", f"{task_label}:photoz_algo.active.bands_to_convert=grizy",
            ])
            pipeline += f"{task_label},"

        butler_path = os.path.join(CI_HSC_GEN3_DIR, "DATA")

        collection_out = f"u/{USER}/pz_rail_testing"
        run_args = [
            "pipetask",
            "run",
            "--register-dataset-types",
            "-b",
            butler_path,
            "-i",
            f"HSC/runs/ci_hsc,{collection_models}",
            "-o",
            collection_out,
            "-d",
            "skymap='discrete/ci_hsc' AND tract=0 AND patch=69",
            "-p",
            pipeline[:-1],
        ]
        print(run_args + configs)

        result = subprocess.run(run_args + configs)

        assert result.returncode == 0

        for output_datasetType in self.output_datasetTypes.values():
            output_pz = butler.get(
                output_datasetType,
                dict(skymap="discrete/ci_hsc", tract=0, patch=69),
                collections=[f"u/{USER}/pz_rail_testing"],
            )

            assert isinstance(output_pz, qp.Ensemble)

        for fdel_ in to_delete:
            os.unlink(fdel_)

        # Success, go ahead and cleanup the butler
        for collection in (f"{collection_out}*", collection_models):
            subprocess.run([
                "butler",
                "remove-runs",
                butler_path,
                collection,
                "--no-confirm",
               "--force",
            ])
        subprocess.run([
            "butler",
            "remove-collections",
            butler_path,
            f"{collection_out}*",
            "--no-confirm",
        ])

