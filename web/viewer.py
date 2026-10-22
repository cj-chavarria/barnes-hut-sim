import duckdb
import numpy as np
import polars as pl
import viser

rng = np.random.default_rng(42)


def main():
    server = viser.ViserServer()

    num_noise_points = 500
    # Use float32 for GPU efficiency
    noise_positions = rng.normal(0, 1, (num_noise_points, 3)).astype(np.float32)

    df_pos = pl.from_numpy(noise_positions, schema=["x", "y", "z"])
    conn = duckdb.connect()
    conn.register("df_pos", df_pos)
    conn.sql("SELECT * from df_pos").show()

    slider = server.gui.add_slider(
        label="max distancie", min=0.1, max=4, step=0.05, initial_value=2.0
    )

    # 1. Create the point cloud ONCE and store the handle
    cloud = server.scene.add_point_cloud(
        name="/noise_cloud",
        points=noise_positions,
        colors=(0, 255, 0),
        point_size=0.03,
    )

    # 2. Only push new binary data to the browser when the slider actually moves!
    @slider.on_update
    def _(_):
        max_r = slider.value

        points_locations = (
            conn.sql(
                f"""
            SELECT x, y, z
            from df_pos
            WHERE sqrt(x*x + y*y + z*z) <= {max_r}
            """
            )
            .pl()
            .to_numpy()
        )

        cloud.points = points_locations

    print("Visit: http://localhost:8080")
    server.sleep_forever()


if __name__ == "__main__":
    main()
