from orator.migrations import Migration


class CreateLogsTable(Migration):
    def up(self):
        with self.db.transaction():
            with self.schema.create('logs') as table:
                table.big_increments('id')
                table.long_text('message')
                table.json('metadata').nullable()
                table.big_integer('user_id')
                table.big_integer('object_id').nullable()
                table.text('object_type').nullable()
                table.timestamps()

    def down(self):
        with self.db.transaction():
            self.schema.drop('logs')
