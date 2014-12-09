from .base import Parse, ParseField


class CustomDemographics(Parse):
    custom_age_range = ParseField('ageRange')
    custom_gender = ParseField('gender')

    GENDER_CHOICES = (
        ('female', 'Female'),
        ('male', 'Male'),
    )

    AGE_RANGE_CHOICES = (
        ('<13', '< 13'),
        ('14-17', '14 - 17'),
        ('18-21', '18 - 21'),
        ('21-30', '21 - 30'),
        ('31-40', '31 - 40'),
        ('41-50', '41 - 50'),
        ('51-60', '51 - 60'),
        ('61+', '61+'),
    )

# Make class name consistent
CustomDemographic = CustomDemographics
