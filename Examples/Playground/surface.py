from ase.build import fcc111
from ase.io import write as ase_write
from ase.visualize import view

symbol = 'Au'
size = (10,10,3)
surface = fcc111(symbol, size, a=None, vacuum=10.0, orthogonal=True, periodic=False)
surface.center()
view(surface)
ase_write('surface.xyz',surface)