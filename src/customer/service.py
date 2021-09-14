from .repository import MongoQueries

from src.customer.schemas.get import responses
from .schemas import (
    SearchCustomersQueryParams,
    SearchCustomersResponse,
    SearchCustomers,
)


class Service(MongoQueries):
    def __init__(self) -> None:
        super().__init__()

    async def get_customers(
        self, query_params: SearchCustomersQueryParams
    ) -> list[SearchCustomers]:

        customers = []
        cursor = None
        total_customer = await self.total_customer()

        if query_params.query == "":

            cursor = self.find_all_customers(
                query_params.skip,
                query_params.limit,
                query_params.column_sort.replace(" ", ""),
                query_params.order,
            )

            for customer in await cursor.to_list(length=None):

                customers.append(SearchCustomers(**customer))

        else:
            if query_params.column_name.replace(" ", ""):

                cursor = self.filter_search_customers(
                    query_params.contain,
                    query_params.query,
                    query_params.column_name.replace(" ", "").lower(),
                    query_params.skip,
                    query_params.limit,
                )
                if cursor:
                    for customer in await cursor.to_list(length=None):

                        customers.append(SearchCustomers(**customer))
                        # customers.append(customer)
                    print(customers)

            else:
                print("F")

        response = self.build_response(customers, total_customer)

        return self.build_response(customers, total_customer)

    def build_response(self, list_customer, total_customer):

        finalresponse = {
            "customer_container": list_customer,
            "total_items": total_customer,
            "total_show": len(list_customer),
        }
        return SearchCustomersResponse(**finalresponse)
