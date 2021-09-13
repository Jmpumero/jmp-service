import pymongo
from core.connection.connection import ConnectionMongo as DwConnection

from config.config import Settings

from typing import Any


from fastapi import HTTPException
from error_handlers.bad_gateway import BadGatewayException


global_settings = Settings()

search_projections = {
    "_id": 0,
    "name": 1,
    "last_name": 1,
    "full_name": 1,
    "age": 1,
    "nationality": 1,
    "civilStatus": 1,
    "documentId": 1,
    "phone": 1,
    "email": 1,
    "address": 1,
}


class MongoQueries(DwConnection):

    # Metodos de Queries para el servicio de Clientes

    def total_customer(self):
        customers = self.clients_collection.estimated_document_count()
        return customers

    def find_one_customer(self, client_id):
        customer = self.clients_collection.find_one(
            {"id": client_id}, search_projections
        )
        return customer

    def find_all_customers(self, skip, limit, column, order):
        if column:
            if order.lower() == "desc":

                customers = (
                    self.clients_collection.find({}, search_projections)
                    .skip(skip)
                    .limit(limit)
                    .sort(column, pymongo.DESCENDING)
                )
            else:

                customers = (
                    self.clients_collection.find({}, search_projections)
                    .skip(skip)
                    .limit(limit)
                    .sort(column, pymongo.ASCENDING)
                )
        else:
            customers = (
                self.clients_collection.find(
                    {},
                    search_projections,
                )
                .skip(skip)
                .limit(limit)
            )

        return customers

    # def insert_one_customer(self, data):
    #     inserted_customer = self.clients_collection.insert_one(data.dict())
    #     return inserted_customer

    def search_customer_name(self, constrain, item_search, column, skip, limit):
        response = ""
        if constrain == "contain":

            # busca en el campo nombre, aquellos que contenga  'variable' en minscula y mayuscula
            response = (
                self.clients_collection.find(
                    {
                        f"{column}": {
                            "$regex": f".*{item_search}.*|.*{item_search.capitalize()}.*"
                        }
                    },
                    search_projections,
                )
                .skip(skip)
                .limit(limit)
            )
        if constrain == "equal_to":

            return (
                self.clients_collection.find(
                    {f"{column}": {"$eq": f"{item_search}"}}, search_projections
                )
                .skip(skip)
                .limit(limit)
            )
        if constrain == "starts_by":
            return (
                self.clients_collection.find(
                    {
                        f"{column}": {
                            "$regex": f"\A{item_search}|\A{item_search.capitalize()}"
                        }
                    },
                    search_projections,
                )
                .skip(skip)
                .limit(limit)
            )
        if constrain == "ends_by":
            return (
                self.clients_collection.find(
                    {
                        f"{column}": {
                            "$regex": f"\Z{item_search}|\Z{item_search.capitalize()}"
                        }
                    },
                    search_projections,
                )
                .skip(skip)
                .limit(limit)
            )

        return response

    def search_customer_email(self, constrain, item_search, column, skip, limit):
        response = ""
        if constrain == "contain":
            return (
                self.clients_collection.find(
                    {
                        "email": {
                            "$elemMatch": {
                                "email": {
                                    "$regex": f".*{item_search.lower()}.*",
                                    "$options": "i",
                                },
                                "isMain": True,
                            }
                        }
                        # "$and": [
                        #     {"email.0.email": {"$regex": f".*{item_search.lower()}.*"}},
                        #     {"email.0.isMain": True},
                        # ]
                    },
                    search_projections,
                )
                .skip(skip)
                .limit(limit)
            )
        if constrain == "equal_to":

            return (
                self.clients_collection.find(
                    {"email": {"email": f"{item_search}", "isMain": True}},
                    search_projections,
                )
                .skip(skip)
                .limit(limit)
            )
        if constrain == "starts_by":
            return (
                self.clients_collection.find(
                    {
                        "email": {
                            "$elemMatch": {
                                "email": {
                                    "$regex": f"\A{item_search}",
                                    "$options": "i",
                                },
                                "isMain": True,
                            }
                        }
                    },
                    search_projections,
                )
                .skip(skip)
                .limit(limit)
            )
        if constrain == "ends_by":
            return (
                self.clients_collection.find(
                    {
                        "email": {
                            "$elemMatch": {
                                "email": {
                                    "$regex": f"\Z{item_search}",
                                    "$options": "i",
                                },
                                "isMain": True,
                            }
                        }
                    },
                    search_projections,
                )
                .skip(skip)
                .limit(limit)
            )

        return response

    def search_phone_local(self, constrain, item_search, column, skip, limit):
        response = ""

        if constrain == "contain":
            return (
                self.clients_collection.find(
                    {
                        "phone": {
                            "$elemMatch": {
                                f"{column}": {
                                    "$regex": f".*{item_search.lower()}.*",
                                    "$options": "i",
                                },
                                "isMain": True,
                            }
                        }
                    },
                    search_projections,
                )
                .skip(skip)
                .limit(limit)
            )
        if constrain == "equal_to":

            return (
                self.clients_collection.find(
                    {
                        "phone": {
                            "$elemMatch": {
                                f"{column}": f"{item_search}",
                                "isMain": True,
                            }
                        }
                    },
                    search_projections,
                )
                .skip(skip)
                .limit(limit)
            )
        if constrain == "starts_by":
            return (
                self.clients_collection.find(
                    {
                        "phone": {
                            "$elemMatch": {
                                f"{column}": {
                                    "$regex": f"\A{item_search}",
                                    "$options": "i",
                                },
                                "isMain": True,
                            }
                        }
                    },
                    search_projections,
                )
                .skip(skip)
                .limit(limit)
            )
        if constrain == "ends_by":
            return (
                self.clients_collection.find(
                    {
                        "phone": {
                            "$elemMatch": {
                                f"{column}": {
                                    "$regex": f"\Z{item_search}",
                                    "$options": "i",
                                },
                                "isMain": True,
                            }
                        }
                    },
                    search_projections,
                )
                .skip(skip)
                .limit(limit)
            )

        return response

    def filter_search_phone(self, constrain, item_search, column, skip, limit):

        if item_search.find("*") > -1:

            print("+" + item_search)
        else:

            item = item_search.replace(" ", "")
            item = item_search.replace("-", "")
            return self.search_phone_local(constrain, item, "local_format", skip, limit)

    def filter_search_customers(self, constrain, item_search, column, skip, limit):

        response = None
        if column == "email":
            return self.search_customer_email(
                constrain, item_search, column, skip, limit
            )
        elif column == "phone":

            return self.filter_search_phone(constrain, item_search, column, skip, limit)

        elif column == "booking_id":
            pass
        else:
            response = self.search_customer_name(
                constrain, item_search, column, skip, limit
            )
        return response
