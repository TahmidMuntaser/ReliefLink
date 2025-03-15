from django import forms


class ReliefSupplyForm(forms.Form):
    relief_types = [
        ('dry' , "DRY FOOD"),
        ('primary', "Primary FOOD"),
    ]
    relief_supply = forms.IntegerField()
    relief_type = forms.ChoiceField(choices=relief_types, label="Relief Type")
