from astropy.table import Table
from astroquery.gaia import Gaia

from utils.read_query import query


def extract_gaia_tbl(n_stars: int) -> Table:
    q = query(path="utils/queries/raw_gaia.sql", N=n_stars)
    job = Gaia.launch_job_async(query=q)
    tbl = job.get_results()
    return tbl
