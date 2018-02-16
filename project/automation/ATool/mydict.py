# coding=utf8

import json


class MyDict(dict):
    """
    A **Python** _dict_ subclass which tries to act like **JavaScript** objects, so you can use the **dot notation** (.) to access members of the object. If the member doesn't exist yet then it's created when you assign something to it. Brackets notation (d['foo']) is also possible.
    """

    def __init__(self, dict_source=None, **kw):
        if dict_source and isinstance(dict_source, (dict, MyDict)):
            for k, v in dict_source.items():
                self[k] = self._transform(v)

        for key, value in kw.items():
            self[key] = self._transform(value)

    def _transform(self, source):
        if isinstance(source, (dict, MyDict)):
            return MyDict(source)

        elif isinstance(source, list):
            return [item for item in map(self._transform, source)]

        elif isinstance(source, tuple):
            result = None
            for item in source:

                if not result:
                    result = (self._transform(item),)

                else:
                    result = result + (self._transform(item),)

            return result

        else:
            # no need for transformation (int, float, str, set, ...)
            return source

    def __getattr__(self, name):
        """
        Get a field "name" from the object in the form:
            obj.name
        """
        if name in self:
            return self[name]

    def __setattr__(self, name, value):
        """
        Sets a field into the object in the form:
            obj.name = value
        """
        self[name] = self._transform(value)

    def __getitem__(self, name):
        """
        Get a field "key" value from the object in the form:
            obj[name]
        """
        return self.get(name)

    def has_path(self, key):
        """
        Check existence of "path" in the tree.
        d = MyDict({'foo': {'bar': 'baz'}})
        d.has_path('foo.bar') == True
        **It only supports "dot-notation" (d.foo.bar)
        """
        if super(MyDict, self).__contains__(key):
            return True

        else:
            parts = str(key).split('.')
            if len(parts) > 1:
                k = '.'.join(parts[:1])
                return self[k].has_path('.'.join(parts[1:]))

            else:
                return super(MyDict, self).__contains__(key)

    def get(self, key, default=None):
        if key in self:
            return super(MyDict, self).get(key, default)

        else:
            parts = str(key).split('.')
            if len(parts) > 1:
                try:
                    return self.get(parts[0]).get('.'.join(parts[1:]))

                except Exception:
                    return None

            else:
                return super(MyDict, self).get(key, default)

    def to_json(self):
        """Returns a JSON-like string representin this instance"""
        return json.dumps(self.get_dict())

    def get_dict(self):
        """Returns a <dict> of the <MyDict> object"""

        # d_ = {}

        def _get_dict(member):

            if isinstance(member, (dict, MyDict)):
                d = {}
                for k, v in member.items():
                    d[k] = _get_dict(v)

                return d

            elif isinstance(member, (list,)):
                lst = []
                for a in member:
                    lst.append(_get_dict(a))

                return lst

            elif isinstance(member, (tuple,)):
                tpl = tuple()
                for a in member:
                    tpl = tpl + (_get_dict(a),)

                return tpl

            elif isinstance(member, (set,)):
                st = set([])
                for a in member:
                    st.add(_get_dict(a))

                return st

            else:
                return member

        # d_.update(**self)
        # return d_

        return _get_dict(self)

    @staticmethod
    def from_json(json_source):
        """
        Returns a "MyDict" instance from a:
            JSON string
            <file>-like containing a JSON string
        """

        if isinstance(json_source, (str, bytes)):
            # decode bytes to str
            if isinstance(json_source, bytes):
                json_source = json_source.decode('utf8')

            load_method = 'loads'

        elif hasattr(json_source, 'read'):
            json_source.seek(0)
            load_method = 'load'

        # json_obj = json.load(json_source)
        # json_obj = json.loads(json_source)
        json_obj = getattr(json, load_method)(json_source)

        return MyDict(json_obj)