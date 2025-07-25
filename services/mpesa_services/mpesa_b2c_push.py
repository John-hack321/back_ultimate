import os
import base64
import aiohttp
import logging

from dotenv import load_dotenv
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

from services.mpesa_services.mpesa_stk_push import MpesaTokenManager

load_dotenv()
logger = logging.getLogger(__name__)


class B2CPaymentService:
    def __init__(self):
        self.cert_path = os.getenv("SAFARICOM_CERT_PATH")
        self.initiator_name = os.getenv("SAFARICOM_INITIATOR_NAME")
        self.initiator_password = os.getenv("SAFARICOM_INITIATOR_PASSWORD")
        self.shortcode = os.getenv("MPESA_SHORT_CODE")
        self.timeout_url = os.getenv("B2C_TIMEOUT_URL")
        self.success_url = os.getenv("B2C_SUCCESS_URL")
        self.request_url = os.getenv("B2C_REQUEST_URL")

        self.token_manager = MpesaTokenManager()

    async def generate_security_credential(self):
        try:
            with open(self.cert_path, "rb") as cert_file:
                cert_data = cert_file.read()
                
            # Try to decode as PEM first
            try:
                public_key = serialization.load_pem_public_key(cert_data)
            except ValueError:
                # If PEM fails, try to process as raw base64 certificate
                try:
                    # Remove any whitespace and decode base64
                    cert_content = cert_data.decode().strip()
                    
                    # Add PEM headers if they're missing
                    if not cert_content.startswith("-----BEGIN"):
                        cert_content = f"-----BEGIN CERTIFICATE-----\n{cert_content}\n-----END CERTIFICATE-----"
                    
                    public_key = serialization.load_pem_public_key(cert_content.encode())
                except Exception as e:
                    logger.error(f"Failed to load certificate in any format: {e}")
                    raise ValueError(f"Unable to load certificate: {e}")

            # Encrypt the password
            encrypted = public_key.encrypt(
                self.initiator_password.encode(),
                padding.PKCS1v15()
            )

            return base64.b64encode(encrypted).decode()
            
        except Exception as e:
            logger.error(f'Security credential encryption failed: {e}')
            raise RuntimeError('Failed to generate security credential')

    async def build_payload(self, amount: int, recipient_phone: str):
        security_credential = await self.generate_security_credential()
        return {
            "Initiator": self.initiator_name,
            "SecurityCredential": security_credential,
            "CommandID": "BusinessPayToBulk",
            "SenderIdentifierType": "4",
            "RecieverIdentifierType": "1",
            "Amount": str(amount),
            "PartyA": str(self.shortcode),
            "PartyB": recipient_phone,
            "AccountReference": "customer_withdrawal",
            "Requester": recipient_phone,
            "Remarks": "account funds withdrawal",
            "QueueTimeOutURL": self.timeout_url,
            "ResultURL": self.success_url
        }

    async def send_b2c_request(self, amount: int, phone: str):
      try:
          access_token = self.token_manager.get_token()
          payload = await self.build_payload(amount, phone)

          headers = {
              "Authorization": f"Bearer {access_token}",
              "Content-Type": "application/json"
          }

          async with aiohttp.ClientSession(headers = headers) as session:
            async with session.post(self.request_url , json = payload) as response:
                response_data = await response.json()
                return response_data
                
      except Exception as e:
        logger.error(f'falied t send the b2c request : {e}')
        raise RuntimeError(f'the b2c request failed')