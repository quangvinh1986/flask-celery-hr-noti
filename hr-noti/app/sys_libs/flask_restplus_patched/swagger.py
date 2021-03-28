from apispec.ext.marshmallow.swagger import schema2parameters
from flask_restplus.swagger import Swagger as OriginalSwagger
from flask import current_app
from six import iterkeys
from flask_restplus.swagger import _v, extract_path, not_none_sorted, not_none


class Swagger(OriginalSwagger):

    def parameters_for(self, doc):
        schema = doc['params']

        if not schema:
            return []
        if isinstance(schema, list):
            return schema
        if isinstance(schema, dict) and all(isinstance(field, dict) for field in schema.values()):
            return list(schema.values())

        if 'in' in schema.context and 'json' in schema.context['in']:
            default_location = 'body'
        else:
            default_location = 'query'

        if 'name' in schema.context:
            name = schema.context['name']
        else:
            name = "body"
        return schema2parameters(schema, default_in=default_location, name=name, required=True)


    def as_dict(self):
        '''
        Output the specification as a serializable ``dict``.

        :returns: the full Swagger specification in a serializable format
        :rtype: dict
        '''
        basepath = self.api.base_path
        if len(basepath) > 1 and basepath.endswith('/'):
            basepath = basepath[:-1]
        infos = {
            'title': _v(self.api.title),
            'version': _v(self.api.version),
        }
        if self.api.description:
            infos['description'] = _v(self.api.description)
        if self.api.terms_url:
            infos['termsOfService'] = _v(self.api.terms_url)
        if self.api.contact and (self.api.contact_email or self.api.contact_url):
            infos['contact'] = {
                'name': _v(self.api.contact),
                'email': _v(self.api.contact_email),
                'url': _v(self.api.contact_url),
            }
        if self.api.license:
            infos['license'] = {'name': _v(self.api.license)}
            if self.api.license_url:
                infos['license']['url'] = _v(self.api.license_url)

        paths = {}
        tags = self.extract_tags(self.api)

        # register errors
        responses = self.register_errors()

        for ns in self.api.namespaces:
            for resource, urls, kwargs in ns.resources:
                for url in self.api.ns_urls(ns, urls):
                    paths[extract_path(url)] = self.serialize_resource(ns, resource, url, kwargs)

        specs = {
            'swagger': '2.0',
            'basePath': basepath,
            'paths': not_none_sorted(paths),
            'info': infos,
            'produces': list(iterkeys(self.api.representations)),
            'consumes': ['application/json'],
            'securityDefinitions': self.api.authorizations or None,
            'security': self.security_requirements(self.api.security) or None,
            'tags': tags,
            'definitions': self.serialize_definitions() or None,
            'responses': responses or None,
            'host': self.get_host(),
            'schemes': self.get_schemes()
        }
        return not_none(specs)

    def get_schemes(self):
        schemes = current_app.config.get('SERVER_SCHEMES', None) or None
        return schemes