from rest_framework import serializers
from .models import Table, Reservation


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    customer_first_name = serializers.SerializerMethodField()
    customer_last_name = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = ['id', 'customer_first_name', 'customer_last_name', 'table', 'reservation_date']

    def get_customer_first_name(self, obj):
        return obj.customer.first_name

    def get_customer_last_name(self, obj):
        return obj.customer.last_name

    def validate(self, data):
        instance = getattr(self, 'instance', None)

        table = data.get('table', getattr(instance, 'table', None))
        reservation_date = data.get('reservation_date', getattr(instance, 'reservation_date', None))

        if table and reservation_date:
            conflicting_reservations = Reservation.objects.filter(
                table=table,
                reservation_date=reservation_date
            )
            if instance:
                conflicting_reservations = conflicting_reservations.exclude(pk=instance.pk)

            if conflicting_reservations.exists():
                raise serializers.ValidationError("This table is already reserved for the selected date")

        return data
