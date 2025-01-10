from django.db import models

class Pet(models.Model):
    SEX_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Not Informed", "Not Informed"),
    ]

    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(max_length=20, choices=SEX_CHOICES, default="Not Informed")
    group = models.ForeignKey(
        'groups.Group',
        on_delete=models.PROTECT,
        related_name='pets'
    )
    traits = models.ManyToManyField('traits.Trait', related_name='pets')

    def __str__(self):
        return self.name
