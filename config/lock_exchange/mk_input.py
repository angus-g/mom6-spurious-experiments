import numpy as np
import xarray as xr

dx = 0.5e3
xl = 64e3
nj = 4
dz = 1
zl = 20
ds = xr.Dataset(coords={'x': np.arange(dx / 2, xl, dx),
			'y': np.arange(nj, dtype=np.float64),
			'z': np.arange(dz / 2, zl, dz)})
ds['temp'] = 0*ds.z + 0*ds.y + 5.0 + 25.0*(ds.x >= 32e3)
ds['salt'] = 35.0 + 0*ds.z + 0*ds.y + 0*ds.x

ds.to_netcdf('input.nc')
