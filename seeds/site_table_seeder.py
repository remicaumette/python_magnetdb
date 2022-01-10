from orator.seeds import Seeder


class SiteTableSeeder(Seeder):
    def run(self):
        self.db.table('sites').insert([
            {
                'name': 'MTest',
                'status': 'in_operation',
            },
            {
                'name': 'MTest2',
                'status': 'defunct',
            },
            {
                'name': 'M10',
                'status': 'in_operation',
            },
        ])
