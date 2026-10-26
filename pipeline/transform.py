import numpy as np
import polars as pl
from astropy.coordinates import SkyCoord
from astropy.table.table import Table


def components_vectors(gaia_tbl: Table) -> pl.DataFrame: ...
