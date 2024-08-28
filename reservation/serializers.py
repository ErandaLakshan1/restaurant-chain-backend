from rest_framework import serializers
from .models import Table, Reservation


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

    def validate(self, data):
        table = data['table']
        reservation_date = data['reservation_date']

        conflicting_reservations = Reservation.objects.filter(
            table=table,
            reservation_date=reservation_date,
        )

        if conflicting_reservations.exists():
            raise serializers.ValidationError("This table is already reserved for the selected date")

        return data
