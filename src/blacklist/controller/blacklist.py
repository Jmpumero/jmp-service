from __future__ import annotations
from aioredis.client import Redis
from typing import Any, List

from fastapi import APIRouter, Depends

from src.customer.schemas.post.responses.customer_crud import CustomerCRUDResponse
from src.customer.schemas.post.bodys.blacklist import BlackListBody
from src.customer.schemas.post.bodys.blacklist import BlackListBody
from core import keycloack_guard
from core import get_redis
from src.blacklist.service import BlacklistService


# from .schemas import SearchCustomersQueryParams, PutScoreCard
# from .schemas import SearchCustomersQueryParams
# from .schemas import PutScoreCard
# from .schemas import (
#     SearchCustomersQueryParams,
#     PutScoreCard,
#     CustomerProfileHeaderResponse,
#     CustomerProfileDetailResponse,
#     CustomerLogBook,
#     CustomerMarketingSubscriptions,
# )
# from src.schemas.blacklist import SearchCustomersQueryParams, BlacklistQueryParams
# from .schemas import BlackListBodyResponse
from src.blacklist.schemas import (
    BlackListBodyResponse,
    BlacklistQueryParams,
)
from utils.remove_422 import remove_422

blacklist_router = APIRouter(
    tags=["Blacklist"], dependencies=[Depends(keycloack_guard)]
)


@blacklist_router.get("/blacklist/")
@remove_422
async def get_customers_(
    query_params: BlacklistQueryParams = Depends(BlacklistQueryParams),
):
    service = BlacklistService()
    # return print("hola controller")
    return await service.get_customers_blacklist(query_params)


# @blacklist_router.put(
#     "/blacklist/update/customer_id/2", response_model=BlackListBodyResponse
# )
# @remove_422
# async def update_customer_in_blacklist(body: BlackListBody):

#     service = BlacklistService()
#     return await service.post_blacklist_update_customer(body)