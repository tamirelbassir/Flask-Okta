# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from api.auth import oidc


class V1TokensTokenId(Resource):

    @oidc.accept_token(require_token=True)
    def delete(self, token_id):

        return {}, 200, None
