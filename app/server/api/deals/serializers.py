from rest_framework import serializers

from server.apps.deals.models import Customer


class CustomerListSerializer(serializers.ModelSerializer):
    gems = serializers.SerializerMethodField()
    spent_money = serializers.SerializerMethodField()

    def get_gems(self, obj):
        obj_gems = getattr(obj, 'bought_gems', None)
        gems_counter = self.context.get('gems_counter')

        if obj_gems and gems_counter:
            # Уникальные камни, купленные данным пользователем
            gems_set = set(obj_gems.split(','))

            # Если камни данного пользователя куплены и другими пользователями, то добавляем их в вывод
            return [gem for gem in gems_set if gems_counter.get(gem, 0) > 1]

    def get_spent_money(self, obj):
        return getattr(obj, 'spent_money', None)

    class Meta:
        model = Customer
        fields = ('username', 'spent_money', 'gems')
