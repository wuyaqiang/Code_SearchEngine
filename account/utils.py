from rest_framework import serializers
import hashlib

# from .models import Label

# class LabelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Label
#         fields = ('id', 'label_name', 'father_id')

def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()