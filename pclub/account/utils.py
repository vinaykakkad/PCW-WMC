from django.contrib.auth.tokens import PasswordResetTokenGenerator

# For creating and verifying token
class TokenGenerator(PasswordResetTokenGenerator):
    pass

generate_token = TokenGenerator()