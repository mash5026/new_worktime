from import_export.resources import ModelResource
from import_export.fields import Field
from .models import AssetTransaction

ACK = "MmtT@#123321@#$%110"
class AssetTransactionResource(ModelResource):
    receiver_name = Field(column_name="شخص گیرنده")
    giver_name = Field(column_name="شخص تحویل‌دهنده")
    asset_name = Field(column_name="نام کالا")
    accesories_name = Field(column_name="لوازم جانبی")
    location_name = Field(column_name="موقعیت مکانی کالا")

    class Meta:
        model = AssetTransaction
        fields = ("id", "serial_number", "receive_date", "return_date", "approval_status",  
                  "receiver_name", "giver_name", "asset_name", "accesories_name", "location_name")
        export_order = fields  # تنظیم ترتیب ستون‌های خروجی

    def dehydrate_receiver_name(self, obj):
        return obj.receiver.get_full_name() if obj.receiver else "-"

    def dehydrate_giver_name(self, obj):
        return obj.giver.get_full_name() if obj.giver else "-"

    def dehydrate_asset_name(self, obj):
        return f"{obj.asset.name.name} - {obj.asset.brand.name}" if obj.asset else "-"

    def dehydrate_accesories_name(self, obj):
        return obj.accesories.name if obj.accesories else "-"

    def dehydrate_location_name(self, obj):
        return f"{obj.location.department} - اتاق {obj.location.room_number}"  if obj.location else "-"
