from orator import Model
from orator.orm import belongs_to, morph_to


class Log(Model):
    __table__ = "logs"
    __fillable__ = ['message', 'metadata', 'user_id', 'object_id', 'object_type']

    @morph_to
    def object(self):
        return

    @belongs_to('user_id')
    def user(self):
        from python_magnetdb.models.user import User
        return User

    @classmethod
    def log(cls, user, message, metadata=None, object=None):
        log = cls(message=message, metadata=metadata)
        log.user().associate(user)
        if object is not None:
            log.object().associate(object)
        log.save()
        return log
