import astropy.coordinates as coord
import astropy.units as u
import polars as pl
from astropy.table import Table


def _coalesce_columns(df: pl.DataFrame, col: list[str]) -> pl.Series:
    return df.with_columns(pl.coalesce(*col).alias("col")).select("col").to_series()


def _to_skycoord(gaia_tbl: pl.DataFrame) -> coord.SkyCoord:
    return coord.SkyCoord(
        ra=u.Quantity(gaia_tbl["ra"], unit=u.deg),
        dec=u.Quantity(gaia_tbl["dec"], unit=u.deg),
        pm_ra_cosdec=u.Quantity(gaia_tbl["pmra"], unit=u.mas / u.yr),
        pm_dec=u.Quantity(gaia_tbl["pmdec"], unit=u.mas / u.yr),
        distance=u.Quantity(gaia_tbl["distance_gspphot"], unit=u.pc),
        radial_velocity=u.Quantity(gaia_tbl["radial_velocity"], unit=u.km / u.s),
        frame="icrs",
    ).transform_to(coord.Galactocentric)


def astro_params(gaia_tbl: pl.DataFrame) -> pl.DataFrame:
    temperature = _coalesce_columns(
        df=gaia_tbl,
        col=[
            "teff_gspphot",
            "teff_gspspec",
            "teff_msc1",
            "teff_espucd",
            "teff_msc2",
            "teff_esphs",
        ],
    )
    radius = _coalesce_columns(gaia_tbl, ["radius_gspphot", "radius_flame"])
    return pl.DataFrame(
        data={
            "source_id": gaia_tbl.select("source_id"),
            "mass": gaia_tbl.select("mass_flame"),
            "radius": radius,
            "distance": gaia_tbl.select("distance_gspphot"),
            "temperature": temperature,
            "luminosity": gaia_tbl.select("lum_flame"),
        }
    )


if __name__ == "__main__":
    print(type(sett.test_func))
