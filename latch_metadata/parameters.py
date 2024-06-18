
from dataclasses import dataclass
import typing
import typing_extensions

from flytekit.core.annotation import FlyteAnnotation

from latch.types.metadata import NextflowParameter
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir

# Import these into your `__init__.py` file:
#
# from .parameters import generated_parameters

generated_parameters = {
    'pulsar': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Observation selection',
        description='Pulsar name for PSRDB search. Returns only observations with this pulsar name.',
    ),
    'utcs': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Start UTC for PSRDB search.  Returns only observations after this UTC timestamp.',
    ),
    'utce': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='End UTC for PSRDB search. Returns only observations before this UTC timestamp.',
    ),
    'project': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Project short name (e.g. PTA) for PSRDB search. Return only observations matching this Project short code.',
    ),
    'obs_csv': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to CSV file containing the observations to process in the format described in the documentation',
    ),
    'input_dir': NextflowParameter(
        type=typing.Optional[str],
        default='/fred/oz005/timing',
        section_title='Input/output options',
        description='Base directory of input archive files',
    ),
    'outdir': NextflowParameter(
        type=typing.Optional[typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})]],
        default=None,
        section_title=None,
        description='The output directory where the results will be saved. You have to use absolute paths to storage on Cloud infrastructure.',
    ),
    'ephemeris': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to the ephemris which will overwrite the default described above. Recommended to only be used for single observations.',
    ),
    'template': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to the template which will overwrite the default described above.  Recommended to only be used for single observations.',
    ),
    'email': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Email address for completion summary.',
    ),
    'use_prev_ar': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Workflow options',
        description='Use the previously created calibrated and cleaned archive in the output directory.',
    ),
    'use_edge_subints': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Use first and last 8 second subints of observation archives.',
    ),
    'chop_edge': NextflowParameter(
        type=typing.Optional[bool],
        default=True,
        section_title=None,
        description='Remove edge frequency channels of the archive before decimating.',
    ),
    'use_mode_nsub': NextflowParameter(
        type=typing.Optional[bool],
        default=True,
        section_title=None,
        description='Additionally create decimations and ToAs with the mode nsub type (most common observation duration used for nsub length). Default True.',
    ),
    'use_all_nsub': NextflowParameter(
        type=typing.Optional[bool],
        default=True,
        section_title=None,
        description='Additionally create decimations with the all nsub type (use all available nsubs). Default True.',
    ),
    'use_max_nsub': NextflowParameter(
        type=typing.Optional[bool],
        default=True,
        section_title=None,
        description="Additionally create decimations and ToAs with the max nsub type (maximum number of nsubs with at least the 'toa_sn' signal-to-noise ratio). Default True.",
    ),
    'tos_sn': NextflowParameter(
        type=typing.Optional[int],
        default=12,
        section_title=None,
        description='Desired ToA S/N ratio, used to calculate the max nsub type to use',
    ),
    'nchans': NextflowParameter(
        type=typing.Optional[str],
        default='1,16,32,58,116,928',
        section_title=None,
        description='Comma separated list of nchans to frequency scrunch the data into',
    ),
    'npols': NextflowParameter(
        type=typing.Optional[str],
        default='1,4',
        section_title=None,
        description='Comma separated list of number of polarisations to scrunch the data into..',
    ),
    'max_nchan_upload': NextflowParameter(
        type=typing.Optional[int],
        default=32,
        section_title=None,
        description='Maximum number of channels of residuals to upload. Large number of channels slows down the upload and are often not required.',
    ),
    'upload': NextflowParameter(
        type=typing.Optional[bool],
        default=True,
        section_title='Meertime dataportal',
        description='Upload result to the database',
    ),
    'psrdb_url': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='URL for interacting with the database API. Can be set with the $PSRDB_URL environment variable.',
    ),
    'psrdb_token': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Token taken from environment variable and obtained using get_ingest_token.sh or get_token.sh. Can be set with the $PSRDB_TOKEN environment variable.',
    ),
    'show_hidden_params': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Generic options',
        description=None,
    ),
}

