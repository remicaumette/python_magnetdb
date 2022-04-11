from orator import Model
from orator.orm import belongs_to, morph_to


class Simulation(Model):
    __table__ = "simulations"
    __fillable__ = ['status', 'resource_id', 'resource_type', 'method', 'model', 'geometry', 'cooling',
                    'result_attachment_id', 'static', 'non_linear']

    @morph_to
    def resource(self):
        return

    @belongs_to('result_attachment_id')
    def result(self):
        from .attachment import Attachment
        return Attachment