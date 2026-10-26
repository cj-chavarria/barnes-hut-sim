import astropy.coordinates as coord
import astropy.units as u
from astropy.coordinates.sky_coordinate import SkyCoord
from astropy.table import QTable, Table


def to_skycoord(gaia_tbl: Table) -> SkyCoord:
    return coord.SkyCoord(
        ra=u.Quantity(gaia_tbl["ra"], unit=u.deg),
        dec=u.Quantity(gaia_tbl["dec"], unit=u.deg),
        pm_ra_cosdec=u.Quantity(gaia_tbl["pmra"], unit=u.mas / u.yr),
        pm_dec=u.Quantity(gaia_tbl["pmdec"], unit=u.mas / u.yr),
        distance=u.Quantity(gaia_tbl["distance_gspphot"], unit=u.pc),
        radial_velocity=u.Quantity(gaia_tbl["radial_velocity"], unit=u.km / u.s),
        frame="icrs",
    ).transform_to(coord.Galactocentric)


if __name__ == "__main__":
    tbl = Table.read("data/test.parquet")
    sky_coord = to_skycoord(tbl).to_table()
    print(type(sky_coord))
    print(sky_coord)
