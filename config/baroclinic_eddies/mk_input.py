import numpy as np
import xarray as xr
import sys

# get DX from second argument
dx = 1e3 * int(sys.argv[1])

xl = 160e3
yl = 500e3
zl = 1000
dz = 50 # 20 layers

t_bot = 10.1
t_top = 13.1
z_bot = 975
dt = 1.2
dy = 40e3
dtp = 0.3

y0 = 250e3
ya = 40e3
k = 3
Lx = 160e3
x2 = 110e3
x3 = 130e3

ds = xr.Dataset(coords={'x': np.arange(dx / 2, xl, dx),
                        'y': np.arange(dx / 2, yl, dx),
                        'z': np.arange(dz / 2, zl, dz)})

# northern temperature
t0 = t_bot + (t_top - t_bot)*(z_bot - ds.z) / z_bot
# location of front
yw = y0 - ya*np.sin(2*np.pi*k*ds.x / Lx)

# background in north
ds['temp'] = t0 + 0*ds.y + 0*ds.x
# subtract dt in south
ds['temp'] -= dt * (ds.y <= yw)
# linear across the front
ds['temp'] -= dt * (1 - (ds.y - yw) / dy) * ((yw < ds.y) & (ds.y < yw + dy))

# add perturbation
ywp = y0 - ya/2 * np.sin(np.pi * (ds.x - x2) / (x3 - x2))
tp = dtp * (1 - (ds.y - ywp) / (dy / 2))
ds['temp'] += tp * ((x2 <= ds.x) & (ds.x <= x3) & \
                    (ywp - dy/2 <= ds.y) & (ds.y <= ywp + dy / 2))

ds['salt'] = 35 + 0*ds.z + 0*ds.y + 0*ds.x

ds.to_netcdf('input_{}.nc'.format(sys.argv[1]),
             encoding={'temp': {'zlib': True},
                       'salt': {'zlib': True}})
