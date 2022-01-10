from orator.seeds import Seeder


class PartTableSeeder(Seeder):
    def run(self):
        self.db.table('parts').insert([
            {
                'name': 'H15101601',
                'type': 'Helix',
                'status': 'in_operation',
                'material_id': self.find_material_id('MA15101601'),
            },
            {
                'name': 'H15061703',
                'type': 'Helix',
                'status': 'in_operation',
                'material_id': self.find_material_id('MA15061703'),
            },
            {
                'name': 'H15061801',
                'type': 'Helix',
                'status': 'in_operation',
                'material_id': self.find_material_id('MA15061801'),
            },
            {
                'name': 'M19061901_R1',
                'type': 'Ring',
                'status': 'in_operation',
                'material_id': self.find_material_id('MAT1_RING'),
            },
            {
                'name': 'M19061901_R2',
                'type': 'Ring',
                'status': 'in_operation',
                'material_id': self.find_material_id('MAT1_RING'),
            },
            {
                'name': 'M19061901_iL1',
                'type': 'Lead',
                'status': 'in_operation',
                'material_id': self.find_material_id('MAT_LEAD'),
            },
            {
                'name': 'M19061901_oL2',
                'type': 'Lead',
                'status': 'in_operation',
                'material_id': self.find_material_id('MAT_LEAD'),
            },
        ])

    def find_material_id(self, name):
        return self.db.table('materials').where('name', name).select('id').first()[0]
