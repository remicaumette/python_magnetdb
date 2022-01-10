from datetime import datetime

from orator.seeds import Seeder


class MagnetTableSeeder(Seeder):
    def run(self):
        self.create_magnet('HL-test', 'in_operation', 'MTest', ['H15061801', 'H15061703', 'H15101601'])
        self.create_magnet('RING-test', 'in_operation', 'MTest', ['M19061901_R1', 'M19061901_R2'])
        self.create_magnet('LEAD-test', 'in_operation', 'M10', ['M19061901_iL1', 'M19061901_oL2'])

    def create_magnet(self, name, status, site_name, parts_name):
        magnet_id = self.db.table('magnets').insert_get_id({
            'name': name,
            'status': status
        })
        site_id = self.db.table('sites').where('name', site_name).select('id').first()[0]
        self.db.table('site_magnets').insert({
            'magnet_id': magnet_id,
            'site_id': site_id,
            'commissioned_at': datetime.now(),
        })
        for part_name in parts_name:
            part_id = self.db.table('parts').where('name', part_name).select('id').first()[0]
            self.db.table('magnet_parts').insert({
                'magnet_id': magnet_id,
                'part_id': part_id,
                'commissioned_at': datetime.now(),
            })
        return magnet_id
