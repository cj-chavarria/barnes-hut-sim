SELECT TOP 10
s.source_id, s.ra, s.dec, s.parallax,
s.radial_velocity, s.distance_gspphot,
s.bp_rp, p.radius_flame, p.mass_flame, p.lum_flame,
p.teff_gspphot, teff_gspspec, p.teff_msc1,
p.teff_esphs, p.teff_espucd, p.teff_msc1, p.teff_msc2
FROM gaiadr3.gaia_source AS s
JOIN gaiadr3.astrophysical_parameters as p
    ON s.source_id = p.source_id
WHERE s.radial_velocity IS NOT NULL
    AND p.mass_flame IS NOT NULL
