from astropy.table.table import Table
from astroquery.gaia import Gaia

from utils.read_query import query


def extract_gaia_tbl() -> Table:
    q = query(path="queries/raw_gaia.sql")
    job = Gaia.launch_job_async(query=q)

    tbl: Table = job.get_results()
    return tbl
