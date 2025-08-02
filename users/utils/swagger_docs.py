from drf_spectacular.utils import extend_schema, OpenApiResponse
from users.serializers import (
    RegisterSerializer, ActivateSerializer, ResendActivationSerializer,
    MeSerializer, SendResetPasswordCodeSerializer, ResetPasswordWithCodeSerializer,
    UserAvatarSerializer
)

register_schema = extend_schema(
    request=RegisterSerializer,
    responses={201: OpenApiResponse(description="User registered successfully")},
    description="Register a new user and send activation email."
)

activate_schema = extend_schema(
    request=ActivateSerializer,
    responses={
        200: OpenApiResponse(description="User activated"),
        400: OpenApiResponse(description="Invalid or expired code"),
        404: OpenApiResponse(description="User not found"),
    },
    description="Activate a user account using email and code."
)

resend_activation_schema = extend_schema(
    request=ResendActivationSerializer,
    responses={
        200: OpenApiResponse(description="Activation email resent."),
        400: OpenApiResponse(description="User already activated or not found."),
    },
    description="Resend the activation code to the user's email."
)

me_schema = extend_schema(
    responses={200: MeSerializer},
    request=MeSerializer,
    description="Get or update current authenticated user's info."
)

send_reset_code_schema = extend_schema(
    request=SendResetPasswordCodeSerializer,
    responses={
        200: OpenApiResponse(description="Reset code sent"),
        404: OpenApiResponse(description="User not found")
    },
    description="Send password reset code to the user's email."
)

reset_password_schema = extend_schema(
    request=ResetPasswordWithCodeSerializer,
    responses={200: OpenApiResponse(description="Password changed")},
    description="Reset user password with email and code."
)

get_avatar_schema = extend_schema(
    responses={
        200: OpenApiResponse(description="Avatar retrieved successfully"),
        404: OpenApiResponse(description="No avatar found")
    },
    description="Get the current user's avatar."
)

update_avatar_schema = extend_schema(
    request=UserAvatarSerializer,
    responses={200: OpenApiResponse(description="Avatar updated successfully")},
    description="Upload or update user avatar (multipart/form-data)."
)

delete_avatar_schema = extend_schema(
    responses={
        200: OpenApiResponse(description="Avatar deleted successfully"),
        400: OpenApiResponse(description="No avatar to delete.")
    },
    description="Delete current user's avatar."
)
