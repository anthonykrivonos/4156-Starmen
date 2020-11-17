from flask import Flask, Blueprint
from typing import List
import sys
import os
from os.path import join
sys.path.append(join(os.getcwd(), '..'))


class SuperBlueprint(Blueprint):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.blueprints = []
        self.prefix = kwargs['url_prefix']

    def register_blueprint(
            self,
            blueprint: Blueprint,
            url_prefix: str = "") -> List[Blueprint]:
        endpoint = self.prefix + \
            (url_prefix if url_prefix != "" else blueprint.url_prefix)
        blueprint.url_prefix = endpoint
        self.blueprints.append(blueprint)
        return self.blueprints

    def bind_to_app(self, app: Flask):
        for blueprint in self.blueprints:
            app.register_blueprint(blueprint)
