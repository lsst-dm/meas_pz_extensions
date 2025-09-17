import os
from collections.abc import Callable
from typing import Any

import qp
from astropy.table import Table
from rail.core.model import Model as PhotozModel
from rail.utils.catalog_utils import (
    ComCamCatalogConfig,
    Dc2CatalogConfig,
    HscCatalogConfig,
)

from lsst.daf.butler import Butler
from lsst.meas.photoz.base import EstimatePhotozTask, EstimatePhotozTaskConfig


def _set_config(config: EstimatePhotozTaskConfig, config_dict: dict[str, Any]) -> None:
    """Add key,value pairs from a dict to a PexConfig ojbect"""
    for key, val in config_dict.items():
        try:
            setattr(config, key, val)
        except AttributeError:
            pass


def hsc_config_callback(config: EstimatePhotozTaskConfig) -> None:
    """Set up config for HSC column names"""
    _set_config(config.photoz_algo, HscCatalogConfig.build_base_dict())
    config.photoz_algo.bands_to_convert = ["g", "r", "i", "z", "y"]
    # We should be using these for constencty
    # but there are some infinites, so for now we use gaap1p0
    # config.photoz_algo.flux_column_template = "{band}_cModelFlux"
    # config.photoz_algo.flux_err_column_template = "{band}_cModelFluxErr"
    config.photoz_algo.flux_column_template = "{band}_gaap1p0Flux"
    config.photoz_algo.flux_err_column_template = "{band}_gaap1p0FluxErr"
    config.photoz_algo.mag_template = "HSC{band}_cmodel_dered"
    config.photoz_algo.mag_err_template = "{band}_cmodel_magerr"
    config.photoz_algo.deredden = False
    _set_config(
        config.photoz_algo,
        dict(
            ref_band="HSCi_cmodel_dered",
            bands=config.photoz_algo.get_mag_name_list(),
            err_bands=config.photoz_algo.get_mag_err_name_list(),
            mag_limits=config.photoz_algo.get_mag_lim_dict(),
            band_a_env=config.photoz_algo.get_band_a_env_dict(),
            filter_list=[
                "DC2LSST_g",
                "DC2LSST_r",
                "DC2LSST_i",
                "DC2LSST_z",
                "DC2LSST_y",
            ],
        )
    )


def dc2_config_callback(config: EstimatePhotozTaskConfig) -> None:
    """Set up config for DC2 column names"""
    _set_config(config.photoz_algo, Dc2CatalogConfig.build_base_dict())
    config.photoz_algo.bands_to_convert = ["u", "g", "r", "i", "z", "y"]
    config.photoz_algo.flux_column_template = "{band}_cModelFlux"
    config.photoz_algo.flux_err_column_template = "{band}_cModelFluxErr"
    config.photoz_algo.mag_template = "mag_{band}_cModel_obj_dered"
    config.photoz_algo.mag_err_template = "magerr_{band}_cModel_obj"
    _set_config(
        config.photoz_algo,
        dict(
            ref_band="mag_i_cModel_obj_dered",
            bands=config.photoz_algo.get_mag_name_list(),
            err_bands=config.photoz_algo.get_mag_err_name_list(),
            mag_limits=config.photoz_algo.get_mag_lim_dict(),
            band_a_env=config.photoz_algo.get_band_a_env_dict(),
        )
    )


def com_cam_config_callback(config: EstimatePhotozTaskConfig) -> None:
    """Set up config for com cam column names"""
    _set_config(config.photoz_algo, ComCamCatalogConfig.build_base_dict())
    config.photoz_algo.bands_to_convert = ["u", "g", "r", "i", "z", "y"]
    config.photoz_algo.flux_column_template = "{band}_cModelFlux"
    config.photoz_algo.flux_err_column_template = "{band}_cModelFluxErr"
    config.photoz_algo.mag_template = "{band}_cModelMag"
    config.photoz_algo.mag_err_template = "{band}_cModelMagErr"
    _set_config(
        config.photoz_algo,
        dict(
            ref_band="i_cModelMag",
            bands=config.photoz_algo.get_mag_name_list(),
            err_bands=config.photoz_algo.get_mag_err_name_list(),
            mag_limits=config.photoz_algo.get_mag_lim_dict(),
            band_a_env=config.photoz_algo.get_band_a_env_dict(),
        )
    )


def hsc_check_callback(output: qp.Ensemble) -> None:
    """Check on the return ensemble for HSC"""
    assert output.npdf == 1000


def dc2_check_callback(output: qp.Ensemble) -> None:
    """Check on the return ensemble for DC2"""
    assert output.npdf == 1000


def dc2_butler_check_callback(output: qp.Ensemble) -> None:
    """Check on the return ensemble for DC2"""
    assert output.npdf == 29358


def com_cam_check_callback(output: qp.Ensemble) -> None:
    """Check on the return ensemble for ComCam"""
    assert output.npdf == 1000


def do_pz_task(
    algo_name: str,
    model_file: str,
    data: Table,
    estimator_class: type[EstimatePhotozTask],
    config_callback: Callable | None = None,
    check_callback: Callable | None = None,
) -> None:
    """Run a single estimator task"""
    modelpath = os.path.abspath(
        os.path.expandvars(
            os.path.join("${TESTDATA_RAIL_DIR}", model_file),
        )
    )
    photoz_model = PhotozModel.read(modelpath)
    task_config = estimator_class.ConfigClass()
    if config_callback:
        config_callback(task_config)
    task = estimator_class(True, config=task_config)
    to_delete = []
    output = task.run(photoz_model, data)
    output_path = f"output_{algo_name}.hdf5"
    output.photozEnsemble.write_to(output_path)
    to_delete.append(output_path)
    test_out = qp.read(output_path)
    assert isinstance(test_out, qp.Ensemble)
    if check_callback:
        check_callback(test_out)
    for fdel_ in to_delete:
        os.unlink(fdel_)


def run_pz_task_s3df(
    algo_name: str,
    butler: Butler,
    model_file: str,
    estimator_class: type[EstimatePhotozTask],
) -> None:
    """Run a single estimator task against DC2"""
    to_delete = []

    modelpath = os.path.abspath(
        os.path.expandvars(
            os.path.join("${TESTDATA_RAIL_DIR}", model_file),
        )
    )
    photoz_model = PhotozModel.read(modelpath)
    task_config = estimator_class.ConfigClass()
    dc2_config_callback(task_config)
    task = estimator_class(True, config=task_config)
    dd = butler.getDeferred(
        "objectTable",
        skymap="DC2",
        tract=3829,
        patch=1,
    ).get(parameters=dict(columns=task.photoz_algo.col_names()))
    output = task.run(photoz_model, dd)
    output.photozEnsemble.write_to(f"output_{algo_name}.hdf5")
    to_delete.append(f"output_{algo_name}.hdf5")
    test_out = qp.read(f"output_{algo_name}.hdf5")
    assert isinstance(test_out, qp.Ensemble)
    dc2_butler_check_callback(test_out)
    for fdel_ in to_delete:
        os.unlink(fdel_)
