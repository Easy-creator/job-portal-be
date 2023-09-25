from rest_framework import serializers

class JobSerializer(serializers.Serializer):
    title = serializers.CharField()
    link = serializers.CharField()
    company_link = serializers.CharField()
    company_name = serializers.CharField()
    location = serializers.CharField()
    img = serializers.CharField()
    salary = serializers.CharField()
    job_desc = serializers.CharField()

    class Meta:
        fields = '__all__'