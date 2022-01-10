from orator.seeds import Seeder

from .material_table_seeder import MaterialTableSeeder
from .part_table_seeder import PartTableSeeder
from .site_table_seeder import SiteTableSeeder
from .magnet_table_seeder import MagnetTableSeeder


class DatabaseSeeder(Seeder):
    def run(self):
        self.call(MaterialTableSeeder)
        self.call(PartTableSeeder)
        self.call(SiteTableSeeder)
        self.call(MagnetTableSeeder)
