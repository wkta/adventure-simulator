from abc import ABC, abstractmethod
import json


class NetwObject(ABC):
    def __init__(self, mediator):
        self.mediator = mediator

    @abstractmethod
    def serialize(self):
        pass

    # - in many cases this will be redifined
    def sync_state(self, given_serial):
        json_obj = json.loads(given_serial)
        for k in json_obj:
            attr_name = f'_{k}'
            setattr(self, attr_name, json_obj[k])
        print(f"State synced! {self}")

    def push_changes(self):
        event_content = self.serialize()
        self.mediator.post(
            'cross_push_changes' if not self.mediator.server_side_flag() else 'cross_sync_state',
            event_content
        )


class Point3D(NetwObject):
    def __init__(self, x, y, z, mediator):
        self._x = x
        self._y = y
        self._z = z
        super().__init__(mediator)

    @property
    def components(self):
        return self._x, self._y, self._z

    @components.setter
    def components(self, vector):
        self._x, self._y, self._z = vector
        self.push_changes()

    def serialize(self) -> str:
        return json.dumps({'x': self._x, 'y': self._y, 'z': self._z})
