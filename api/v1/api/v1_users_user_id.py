# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import g, current_app
from okta.framework.OktaError import OktaError

from . import Resource
from api.auth import get_okta_client


class V1UsersUserId(Resource):

    def patch(self, user_id):
        okta_client = get_okta_client(current_app, service="users")

        try:
            data = {
                "profile": {
                    "firstName": g.json["first_name"],
                    "lastName": g.json["last_name"],
                    "email": g.json["email"],
                    "login": g.json["login"],
                    "mobilePhone": g.json["mobile_phone"]
                },
                "credentials": {
                    "password": {
                        "value": g.json["password"]
                    }
                }
            }
        except KeyError:
            return {"error": "Your data doesn't contain all fields"}, 400, None

        try:
            response = okta_client.update_user_by_id(user_id, data)
        except OktaError as e:
            if e.error_code == 'E0000001':
                return {"error": ". ".join([
                    i["errorSummary"] for i in e.error_causes
                ])}, 400, None

            return {"error": "There are some problems on the server. Please "
                             "try again later"}, 500

        updated_user = {
            "first_name": response.profile.firstName,
            "last_name": response.profile.lastName,
            "email": response.profile.email,
            "login": response.profile.login,
            "mobile_phone": response.profile.mobilePhone,
        }
        return updated_user, 200, None
