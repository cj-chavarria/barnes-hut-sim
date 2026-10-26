from astropy.table import Table
from astroquery.gaia import Gaia

from utils.read_query import query


def extract_gaia_tbl() -> Table:
    q = query(path="queries/raw_gaia.sql")
    job = Gaia.launch_job_async(query=q)

    tbl: Table = job.get_results()
    return tbl


if __name__ == "__main__":
    gaia_table = extract_gaia_tbl()
    print(gaia_table)
    gaia_table.write("data/test.parquet")
