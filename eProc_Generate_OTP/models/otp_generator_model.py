from django.db import models


class OtpGenerator(models.Model):
    """
    Table contains Otp Generator
    """
    email = models.EmailField(db_column='EMAIL', primary_key=True, max_length=100, null=False)
    password = models.CharField(db_column='PASSWORD', max_length=256, null=True)
    first_name = models.CharField(db_column='FIRST_NAME', max_length=30, null=False)
    last_name = models.CharField(db_column='LAST_NAME', max_length=30, null=False)
    otp = models.CharField(db_column='OTP', max_length=4, null=True)
    otp_locked = models.BooleanField(default=False, null=False, db_column='OTP_LOCKED')
    otp_attempts = models.PositiveIntegerField(db_column='OTP_ATTEMPTS', default=False, null=False)
    otp_generator_created_by = models.CharField(db_column='OTP_GENERATOR_CREATED_BY', max_length=30, null=True)
    otp_generator_created_at = models.DateTimeField(db_column='OTP_GENERATOR_CREATED_AT', max_length=50, null=True)
    otp_generator_changed_by = models.CharField(db_column='OTP_GENERATOR_CHANGED_BY', max_length=30, null=True)
    otp_generator_changed_at = models.DateTimeField(db_column='OTP_GENERATOR_CHANGED_AT', max_length=50, null=True)
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        db_table = "MTD_OTP_GENERATOR"
        managed = True
