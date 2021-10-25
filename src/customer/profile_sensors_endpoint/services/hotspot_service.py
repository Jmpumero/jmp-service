from typing import Any

from fastapi import status
from fastapi.responses import JSONResponse

from src.customer.profile_sensors_endpoint.repository.cast_hotspot import CastHotSpotQueries

class HotspotService(CastHotSpotQueries):
    '''
    Service to get customer Hotspot usage statistics
     - Number of Connections to hotspot
     - Date of First Connection
     - Date of Las Connection
     
    '''
    def __init__(self):
        super().__init__()

    async def get_hotspot_stats(self, customer_id: str, sensor : str) -> Any:
        try:
            count = await self.count__documents(customer_id, sensor)

            oldest_connection = self.first_connection(customer_id, sensor)
            
            newest_connection = self.last_connection(customer_id, sensor)

            async for date in oldest_connection:
                first_connection = date['data']['date']

            async for date2 in newest_connection:
                last_connection = date2['data']['date']

            response = {
                'hotspot_response':{
                    'status_code':status.HTTP_200_OK,
                    'message': 'Ok'
                },
                'id': customer_id,
                'hotspot_connections': count,
                'hotspot_first_connection': first_connection,
                'hotspot_last_connection': last_connection
            }
            return response
        except:
            response = {
                'hotspot_response':{
                    'status_code':status.HTTP_404_NOT_FOUND,
                    'message': "Customer doesn't have interaction with this sensor"
                }
            }
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=response)