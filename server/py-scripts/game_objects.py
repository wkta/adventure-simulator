import re


#holy moly, json_dumps polyfill! Transcrypt mad dog
def json_dumps(obj):
    if isinstance(obj, dict):
        items = []
        for key, value in obj.items():
            items.append(f'{json_dumps(key)}: {json_dumps(value)}')
        return '{' + ', '.join(items) + '}'
    elif isinstance(obj, list):
        items = [json_dumps(item) for item in obj]
        return '[' + ', '.join(items) + ']'
    elif isinstance(obj, str):
        return '"' + obj.replace('"', '\\"') + '"'
    elif isinstance(obj, (int, float)):
        return str(obj)
    elif obj is True:
        return 'true'
    elif obj is False:
        return 'false'
    elif obj is None:
        return 'null'
    else:
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def json_loads(s):
    print('debug polyfill>>json_loads. Arg is:', s)
    def parse_value(s, index):
        if s[index] == '"':
            return parse_string(s, index)
        elif s[index] == '{':
            return parse_object(s, index)
        elif s[index] == '[':
            return parse_array(s, index)
        elif s[index] in '0123456789-':
            return parse_number(s, index)
        elif s[index:index+4] == 'true':
            return True, index + 4
        elif s[index:index+5] == 'false':
            return False, index + 5
        elif s[index:index+4] == 'null':
            return None, index + 4
        else:
            raise ValueError(f"Unexpected character at index {index}")

    def parse_string(s, index):
        end_index = index + 1
        while end_index < len(s):
            if s[end_index] == '"':
                if s[end_index - 1] != '\\':
                    break
            end_index += 1
        return s[index + 1:end_index].replace('\\"', '"'), end_index + 1

    def parse_object(s, index):
        obj = {}
        index += 1  # Skip '{'
        while s[index] != '}':
            key, index = parse_string(s, index)
            index = skip_whitespace(s, index)
            if s[index] != ':':
                raise ValueError(f"Expected ':' at index {index}")
            index += 1  # Skip ':'
            value, index = parse_value(s, index)
            obj[key] = value
            index = skip_whitespace(s, index)
            if s[index] == ',':
                index += 1  # Skip ','
            index = skip_whitespace(s, index)
        return obj, index + 1

    def parse_array(s, index):
        arr = []
        index += 1  # Skip '['
        while s[index] != ']':
            value, index = parse_value(s, index)
            arr.append(value)
            index = skip_whitespace(s, index)
            if s[index] == ',':
                index += 1  # Skip ','
            index = skip_whitespace(s, index)
        return arr, index + 1

    def parse_number(s, index):
        match = re.match(r'-?\d+(\.\d+)?([eE][+-]?\d+)?', s[index:])
        if not match:
            raise ValueError(f"Invalid number at index {index}")
        num_str = match.group(0)
        if '.' in num_str or 'e' in num_str or 'E' in num_str:
            return float(num_str), index + len(num_str)
        return int(num_str), index + len(num_str)

    def skip_whitespace(s, index):
        while index < len(s) and s[index] in ' \t\n\r':
            index += 1
        return index

    s = s.strip()
    value, _ = parse_value(s, 0)
    return value


class NetwObject:
    def __init__(self, mediator):
        self.mediator = mediator

    def serialize(self):
        raise NotImplementedError

    # - in many cases this will be redifined
    def sync_state(self, given_serial):
        json_obj = json_loads(given_serial)
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
        return json_dumps({'x': self._x, 'y': self._y, 'z': self._z})
