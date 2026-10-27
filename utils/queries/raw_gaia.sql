SELECT TOP {N}
s.source_id, s.ra, s.dec, s.pmra, s.pmdec, s.parallax,
s.radial_velocity, s.bp_rp, p.distance_gspphot,
p.radius_flame, p.radius_gspphot, p.mass_flame, p.lum_flame,
p.teff_gspphot, p.teff_gspspec, p.teff_msc1,
p.teff_esphs, p.teff_espucd, p.teff_msc1, p.teff_msc2
FROM gaiadr3.gaia_source AS s
INNER JOIN gaiadr3.astrophysical_parameters as p
    ON s.source_id = p.source_id
WHERE s.random_index BETWEEN 0 AND 250000
    AND s.radial_velocity IS NOT NULL
    AND p.mass_flame IS NOT NULL
    AND p.distance_gspphot IS NOT NULL
