from django.db import models
from jsonfield import JSONField


class Simulation(models.Model):
    id = models.BigAutoField(primary_key=True)
    status = models.TextField(default='pending', null=True)
    magnet = models.ForeignKey('Magnet', on_delete=models.CASCADE, null=True)
    site = models.ForeignKey('Site', on_delete=models.CASCADE, null=True)
    method = models.TextField(null=True)
    model = models.TextField(null=True)
    geometry = models.TextField(null=True)
    cooling = models.TextField(null=True)
    output_attachment = models.ForeignKey('StorageAttachment', on_delete=models.SET_NULL, null=True, related_name='simulation_output_attachment')
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
    static = models.BooleanField(null=True)
    non_linear = models.BooleanField(null=True)
    setup_output_attachment = models.ForeignKey('StorageAttachment', on_delete=models.SET_NULL, null=True, related_name='simulation_setup_output_attachment')
    setup_status = models.TextField(default='pending', null=False)
    setup_state = JSONField(default=dict)
    owner = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    log_attachment = models.ForeignKey('StorageAttachment', on_delete=models.SET_NULL, null=True, related_name='simulation_log_attachment')
    currents = models.ManyToManyField('SimulationCurrent', related_name='simulation_simulation_currents')

    class Meta:
        db_table = 'simulations'




# class SimulationObserver(object):
#     def deleting(self, simulation):
#         from .attachment import Attachment
#
#         if simulation.setup_output_attachment_id is not None:
#             setup_output_attachment = Attachment.find(simulation.setup_output_attachment_id)
#             if setup_output_attachment is not None:
#                 setup_output_attachment.delete()
#         if simulation.output_attachment_id is not None:
#             output_attachment = Attachment.find(simulation.output_attachment_id)
#             if output_attachment is not None:
#                 output_attachment.delete()
#         if simulation.log_attachment_id is not None:
#             log_attachment = Attachment.find(simulation.log_attachment_id)
#             if log_attachment is not None:
#                 log_attachment.delete()
#
#
# Simulation.observe(SimulationObserver())
