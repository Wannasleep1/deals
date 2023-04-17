import coreapi
import coreschema
from rest_framework.schemas import AutoSchema


process_deal_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            name='file',
            required=True,
            location='body',
            type='multipart',
            schema=coreschema.Object(
                description='CSV file to process',
            )
        ),
    ],
)
