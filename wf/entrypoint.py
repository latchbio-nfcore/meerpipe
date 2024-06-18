from dataclasses import dataclass
from enum import Enum
import os
import subprocess
import requests
import shutil
from pathlib import Path
import typing
import typing_extensions

from latch.resources.workflow import workflow
from latch.resources.tasks import nextflow_runtime_task, custom_task
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir
from latch.ldata.path import LPath
from latch_cli.nextflow.workflow import get_flag
from latch_cli.nextflow.utils import _get_execution_name
from latch_cli.utils import urljoins
from latch.types import metadata
from flytekit.core.annotation import FlyteAnnotation

from latch_cli.services.register.utils import import_module_by_path

meta = Path("latch_metadata") / "__init__.py"
import_module_by_path(meta)
import latch_metadata

@custom_task(cpu=0.25, memory=0.5, storage_gib=1)
def initialize() -> str:
    token = os.environ.get("FLYTE_INTERNAL_EXECUTION_ID")
    if token is None:
        raise RuntimeError("failed to get execution token")

    headers = {"Authorization": f"Latch-Execution-Token {token}"}

    print("Provisioning shared storage volume... ", end="")
    resp = requests.post(
        "http://nf-dispatcher-service.flyte.svc.cluster.local/provision-storage",
        headers=headers,
        json={
            "storage_gib": 100,
        }
    )
    resp.raise_for_status()
    print("Done.")

    return resp.json()["name"]






@nextflow_runtime_task(cpu=4, memory=8, storage_gib=100)
def nextflow_runtime(pvc_name: str, pulsar: typing.Optional[str], utcs: typing.Optional[str], utce: typing.Optional[str], project: typing.Optional[str], obs_csv: typing.Optional[str], outdir: typing.Optional[typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})]], ephemeris: typing.Optional[str], template: typing.Optional[str], email: typing.Optional[str], use_prev_ar: typing.Optional[bool], use_edge_subints: typing.Optional[bool], psrdb_url: typing.Optional[str], psrdb_token: typing.Optional[str], show_hidden_params: typing.Optional[bool], input_dir: typing.Optional[str], chop_edge: typing.Optional[bool], use_mode_nsub: typing.Optional[bool], use_all_nsub: typing.Optional[bool], use_max_nsub: typing.Optional[bool], tos_sn: typing.Optional[int], nchans: typing.Optional[str], npols: typing.Optional[str], max_nchan_upload: typing.Optional[int], upload: typing.Optional[bool]) -> None:
    try:
        shared_dir = Path("/nf-workdir")



        ignore_list = [
            "latch",
            ".latch",
            "nextflow",
            ".nextflow",
            "work",
            "results",
            "miniconda",
            "anaconda3",
            "mambaforge",
        ]

        shutil.copytree(
            Path("/root"),
            shared_dir,
            ignore=lambda src, names: ignore_list,
            ignore_dangling_symlinks=True,
            dirs_exist_ok=True,
        )

        cmd = [
            "/root/nextflow",
            "run",
            str(shared_dir / "main.nf"),
            "-work-dir",
            str(shared_dir),
            "-profile",
            "docker",
            "-c",
            "latch.config",
                *get_flag('pulsar', pulsar),
                *get_flag('utcs', utcs),
                *get_flag('utce', utce),
                *get_flag('project', project),
                *get_flag('obs_csv', obs_csv),
                *get_flag('input_dir', input_dir),
                *get_flag('outdir', outdir),
                *get_flag('ephemeris', ephemeris),
                *get_flag('template', template),
                *get_flag('email', email),
                *get_flag('use_prev_ar', use_prev_ar),
                *get_flag('use_edge_subints', use_edge_subints),
                *get_flag('chop_edge', chop_edge),
                *get_flag('use_mode_nsub', use_mode_nsub),
                *get_flag('use_all_nsub', use_all_nsub),
                *get_flag('use_max_nsub', use_max_nsub),
                *get_flag('tos_sn', tos_sn),
                *get_flag('nchans', nchans),
                *get_flag('npols', npols),
                *get_flag('max_nchan_upload', max_nchan_upload),
                *get_flag('upload', upload),
                *get_flag('psrdb_url', psrdb_url),
                *get_flag('psrdb_token', psrdb_token),
                *get_flag('show_hidden_params', show_hidden_params)
        ]

        print("Launching Nextflow Runtime")
        print(' '.join(cmd))
        print(flush=True)

        env = {
            **os.environ,
            "NXF_HOME": "/root/.nextflow",
            "NXF_OPTS": "-Xms2048M -Xmx8G -XX:ActiveProcessorCount=4",
            "K8S_STORAGE_CLAIM_NAME": pvc_name,
            "NXF_DISABLE_CHECK_LATEST": "true",
        }
        subprocess.run(
            cmd,
            env=env,
            check=True,
            cwd=str(shared_dir),
        )
    finally:
        print()

        nextflow_log = shared_dir / ".nextflow.log"
        if nextflow_log.exists():
            name = _get_execution_name()
            if name is None:
                print("Skipping logs upload, failed to get execution name")
            else:
                remote = LPath(urljoins("latch:///your_log_dir/nf_nf_core_meerpipe", name, "nextflow.log"))
                print(f"Uploading .nextflow.log to {remote.path}")
                remote.upload_from(nextflow_log)



@workflow(metadata._nextflow_metadata)
def nf_nf_core_meerpipe(pulsar: typing.Optional[str], utcs: typing.Optional[str], utce: typing.Optional[str], project: typing.Optional[str], obs_csv: typing.Optional[str], outdir: typing.Optional[typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})]], ephemeris: typing.Optional[str], template: typing.Optional[str], email: typing.Optional[str], use_prev_ar: typing.Optional[bool], use_edge_subints: typing.Optional[bool], psrdb_url: typing.Optional[str], psrdb_token: typing.Optional[str], show_hidden_params: typing.Optional[bool], input_dir: typing.Optional[str] = '/fred/oz005/timing', chop_edge: typing.Optional[bool] = True, use_mode_nsub: typing.Optional[bool] = True, use_all_nsub: typing.Optional[bool] = True, use_max_nsub: typing.Optional[bool] = True, tos_sn: typing.Optional[int] = 12, nchans: typing.Optional[str] = '1,16,32,58,116,928', npols: typing.Optional[str] = '1,4', max_nchan_upload: typing.Optional[int] = 32, upload: typing.Optional[bool] = True) -> None:
    """
    nf-core/meerpipe

    Sample Description
    """

    pvc_name: str = initialize()
    nextflow_runtime(pvc_name=pvc_name, pulsar=pulsar, utcs=utcs, utce=utce, project=project, obs_csv=obs_csv, input_dir=input_dir, outdir=outdir, ephemeris=ephemeris, template=template, email=email, use_prev_ar=use_prev_ar, use_edge_subints=use_edge_subints, chop_edge=chop_edge, use_mode_nsub=use_mode_nsub, use_all_nsub=use_all_nsub, use_max_nsub=use_max_nsub, tos_sn=tos_sn, nchans=nchans, npols=npols, max_nchan_upload=max_nchan_upload, upload=upload, psrdb_url=psrdb_url, psrdb_token=psrdb_token, show_hidden_params=show_hidden_params)

