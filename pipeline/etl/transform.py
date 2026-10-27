import astropy.coordinates as coord
import astropy.units as u
import polars as pl
from astropy.table import Table


def to_skycoord(gaia_tbl: Table) -> coord.SkyCoord:
    return coord.SkyCoord(
        ra=u.Quantity(gaia_tbl["ra"], unit=u.deg),
        dec=u.Quantity(gaia_tbl["dec"], unit=u.deg),
        pm_ra_cosdec=u.Quantity(gaia_tbl["pmra"], unit=u.mas / u.yr),
        pm_dec=u.Quantity(gaia_tbl["pmdec"], unit=u.mas / u.yr),
        distance=u.Quantity(gaia_tbl["distance_gspphot"], unit=u.pc),
        radial_velocity=u.Quantity(gaia_tbl["radial_velocity"], unit=u.km / u.s),
        frame="icrs",
    ).transform_to(coord.Galactocentric)


def astroparams(gaia_tbl: Table) -> pl.DataFrame:
    df = pl.DataFrame()

    return df
