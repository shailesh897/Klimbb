import json
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework.authtoken.models import Token
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from infinity_stones.stones_app.models import Activation


def get_activation_status(user_id):
    try:
        activation = Activation.objects.filter(user_id=user_id).last()
        if activation:
            return {
                "stone_id": activation.stone.id,
                "start_time": activation.start_time,
                "end_time": activation.end_time,
            }
        else:
            return None
    except Exception as e:
        return None


class StoneStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("trinig to connect")
        await self.accept()

    async def disconnect(self, close_code):
        print("Disconnecting...")
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        user_id = data["User_ID"]
        jwt_token = data["JWT_Token"]

        # Validate JWT token
        try:
            user = JSONWebTokenAuthentication().authenticate_credentials(jwt_token)
            print("user is ", user)
        except Exception as e:
            await self.send(
                text_data=json.dumps(
                    {
                        "error": "JWT validation failed",
                    }
                )
            )
            return

        # Query the database to get activation status (adjust this as per your models)
        activation_status = get_activation_status(user_id)

        await self.send(
            text_data=json.dumps(
                {
                    "activation_status": activation_status,
                }
            )
        )
