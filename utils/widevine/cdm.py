import os
import time
import base64
import binascii

from google.protobuf.message import DecodeError
from Cryptodome.Random import get_random_bytes
from Cryptodome.Random import random
from Cryptodome.Cipher import PKCS1_OAEP, AES
from Cryptodome.Hash import CMAC, SHA256, HMAC, SHA1
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pss
from Cryptodome.Util import Padding

from utils import logger
import utils.widevine.formats.wv_proto2_pb2 as wv_proto2

class Session:
    def __init__(self, sessionId, initData, deviceConfig, offline):
        self.sessionId = sessionId
        self.initData = initData
        self.offline = offline
        self.deviceConfig = deviceConfig
        self.deviceKey = None
        self.sessionKey = None
        self.derivedKeys = {
            'enc': None,
            'auth_1': None,
            'auth_2': None
        }
        self.licenseRequest = None
        self.license = None
        self.serviceCertificate = None
        self.privacyMode = False
        self.keys = []

class Key:
    def __init__(self, kid, type, key, permissions=[]):
        self.kid = kid
        self.type = type
        self.key = key
        self.permissions = permissions

    def __repr__(self):
        if self.type == "OPERATOR_SESSION":
           return "key(kid={}, type={}, key={}, permissions={})".format(
               self.kid,
               self.type,
               binascii.hexlify(self.key),
               self.permissions
            )
        else:
           return "key(kid={}, type={}, key={})".format(
               self.kid,
               self.type,
               binascii.hexlify(self.key)
            )
        
class Device:
    def __init__(self, deviceName, devicePath):
        self.deviceName = deviceName
        self.securityLevel = 3
        self.deviceType = 'android'
        self.isPrivateKey = os.path.exists(
            os.path.join(devicePath, 'device_private_key')
        )
        self.isSendKeyControlNonce = True
        self.isVmp = os.path.exists(
            os.path.join(devicePath, 'device_vmp_blob')
        )
        self.description = 'Widevine'
        self.keyboxFilename = os.path.join(
            devicePath, 'keybox')
        self.deviceCertFilename = os.path.join(
            devicePath, 'device_cert')
        self.devicePrivateKeyFilename = os.path.join(
            devicePath, 'device_private_key')
        self.deviceClientIdBlobFilename = os.path.join(
            devicePath, 'device_client_id_blob')
        self.deviceVmpBlobFilename = os.path.join(
            devicePath, 'device_vmp_blob')

class ContentDecryptionModule:
    def __init__(self):
        self.sessions = {}

    def open(self, initData, device: Device, rawData=None, offline=False):
        if device.deviceType == 'android':
            randAscii = ''.join(random.choice('ABCDEF0123456789') for _ in range(16))
            counter = '01'
            rest = '00000000000000'
            sessionId = randAscii + counter + rest
            sessionId = sessionId.encode('ascii')

        elif device.deviceType == 'chrome':
            randBytes = get_random_bytes(16)
            sessionId = randBytes

        else: logger.error("Device type is unusable!", 1)
        
        if rawData and isinstance(rawData, (bytes, bytearray)):
            initData = rawData
            self.rawPssh = True
        else:
            initData = self.__parseInitData(initData)
            self.rawPssh = False

        if initData: newSession = Session(sessionId, initData, device, offline)
        else: logger.error("Unable to parse init data!")
        
        self.sessions[sessionId] = newSession
        return sessionId

    def __parseInitData(self, initData):
        initDataParsed = wv_proto2.WidevineCencHeader()

        try:
            initDataParsed.ParseFromString(base64.b64decode(initData)[32:])
        except DecodeError:
            try:
                id_bytes = initDataParsed.ParseFromString(base64.b64decode(initData)[32:])
            except DecodeError:
                return None
        
        return initDataParsed

    def close(self, sessionId):
        if sessionId in self.sessions: self.sessions.pop(sessionId)
        else: logger.error(f"Session {sessionId} not found!")

    def setServiceCertificate(self, sessionId, cert):
        if not sessionId in self.sessions:
            logger.error("session id doesn't exist!")

        session: Session = self.sessions[sessionId]
        message = wv_proto2.SignedMessage()

        try: message.ParseFromString(base64.b64decode(cert))
        except DecodeError: logger.error("Failed to parse cert as SignedMessage!")

        serviceCertificate = wv_proto2.SignedDeviceCertificate()

        if message.Type:
            try: serviceCertificate.ParseFromString(message.Msg)
            except DecodeError: logger.error("Failed to parse Service Certificate!")
        else:
            try: serviceCertificate.ParseFromString(base64.b64decode(cert))
            except DecodeError: logger.error("Failed to parse Service Certificate!")

        session.serviceCertificate = serviceCertificate
        session.privacyMode = True

    def getLicenseRequest(self, sessionId):
        if not sessionId in self.sessions:
            logger.error("Session ID does not exist!")

        session: Session = self.sessions[sessionId]

        if self.rawPssh: licenseRequest = wv_proto2.SignedLicenseRequestRaw()
        else: licenseRequest = wv_proto2.SignedLicenseRequest()

        clientId = wv_proto2.ClientIdentification()

        if not os.path.exists(session.deviceConfig.deviceClientIdBlobFilename):
            logger.error("No Client ID Blob available for this device!", 1)

        with open(session.deviceConfig.deviceClientIdBlobFilename, "rb") as f:
            try: cidBytes = clientId.ParseFromString(f.read())
            except DecodeError: logger.error("Client ID failed to parse as protobuf!", 1)

        if not self.rawPssh:
            licenseRequest.Type = wv_proto2.SignedLicenseRequest.MessageType.Value('LICENSE_REQUEST')
            licenseRequest.Msg.ContentId.CencId.Pssh.CopyFrom(session.initData)
        else:
            licenseRequest.Type = wv_proto2.SignedLicenseRequestRaw.MessageType.Value('LICENSE_REQUEST')
            licenseRequest.Msg.ContentId.CencId.Pssh = session.initData # bytes

        if session.offline: licenseType = wv_proto2.LicenseType.Value('OFFLINE')
        else: licenseType = wv_proto2.LicenseType.Value('DEFAULT')

        licenseRequest.Msg.ContentId.CencId.LicenseType = licenseType
        licenseRequest.Msg.ContentId.CencId.RequestId = sessionId
        licenseRequest.Msg.Type = wv_proto2.LicenseRequest.RequestType.Value('NEW')
        licenseRequest.Msg.RequestTime = int(time.time())
        licenseRequest.Msg.ProtocolVersion = wv_proto2.ProtocolVersion.Value('CURRENT')

        if session.deviceConfig.isSendKeyControlNonce:
            licenseRequest.Msg.KeyControlNonce = random.randrange(1, 2**31)

        if session.privacyMode:
            if session.deviceConfig.isVmp:
                vmpHashes = wv_proto2.FileHashes()

                with open(session.deviceConfig.deviceVmpBlobFilename, "rb") as f:
                    try: vmpBytes = vmpHashes.ParseFromString(f.read())
                    except DecodeError: logger.error("VMP hashes failed to parse as protobuf!", 1)
                
                clientId._FileHashes.CopyFrom(vmpHashes)

            cidAesKey = get_random_bytes(16)
            cidIv = get_random_bytes(16)
            cidCipher = AES.new(cidAesKey, AES.MODE_CBC, cidIv)
            encryptedClientId = cidCipher.encrypt(Padding.pad(clientId.SerializeToString(), 16))
            servicePublicKey = RSA.importKey(session.serviceCertificate._DeviceCertificate.PublicKey)
            serviceCipher = PKCS1_OAEP.new(servicePublicKey)
            encryptedCidKey = serviceCipher.encrypt(cidAesKey)
            encryptedClientIdProto = wv_proto2.EncryptedClientIdentification()
            encryptedClientIdProto.ServiceId = session.serviceCertificate._DeviceCertificate.ServiceId
            encryptedClientIdProto.ServiceCertificateSerialNumber = session.serviceCertificate._DeviceCertificate.SerialNumber
            encryptedClientIdProto.EncryptedClientId = encryptedClientId
            encryptedClientIdProto.EncryptedClientIdIv = cidIv
            encryptedClientIdProto.EncryptedPrivacyKey = encryptedCidKey
            licenseRequest.Msg.EncryptedClientId.CopyFrom(encryptedClientIdProto)
        else:
            licenseRequest.Msg.ClientId.CopyFrom(clientId)

        if session.deviceConfig.isPrivateKey:
            key = RSA.importKey(open(session.deviceConfig.devicePrivateKeyFilename).read())
            session.deviceKey = key
        else:
            logger.error("Need device private key, other methods unimplemented", 1)

        hash = SHA1.new(licenseRequest.Msg.SerializeToString())
        signature = pss.new(key).sign(hash)

        licenseRequest.Signature = signature
        session.licenseRequest = licenseRequest
        return licenseRequest.SerializeToString()

    def provideLicense(self, sessionId, b64License):

        if not sessionId in self.sessions:
            logger.error("Session does not exist!")

        session: Session = self.sessions[sessionId]

        if not session.licenseRequest:
            logger.error("Generate a License Request first!", 1)

        license = wv_proto2.SignedLicense()
        try: license.ParseFromString(base64.b64decode(b64License))
        except DecodeError: logger.error("Unable to parse license - check Protobufs!", 1)

        session.license = license

        oaepCipher = PKCS1_OAEP.new(session.deviceKey)
        session.sessionKey = oaepCipher.decrypt(license.SessionKey)
        licReqMsg = session.licenseRequest.Msg.SerializeToString()
        encKeyBase = b"ENCRYPTION\000" + licReqMsg + b"\0\0\0\x80"
        authKeyBase = b"AUTHENTICATION\0" + licReqMsg + b"\0\0\2\0"

        encKey = b"\x01" + encKeyBase
        authKey_1 = b"\x01" + authKeyBase
        authKey_2 = b"\x02" + authKeyBase
        authKey_3 = b"\x03" + authKeyBase
        authKey_4 = b"\x04" + authKeyBase

        cmacObj = CMAC.new(session.sessionKey, ciphermod=AES)
        cmacObj.update(encKey)
        encCmacKey = cmacObj.digest()

        cmacObj = CMAC.new(session.sessionKey, ciphermod=AES)
        cmacObj.update(authKey_1)
        authCmacKey_1 = cmacObj.digest()

        cmacObj = CMAC.new(session.sessionKey, ciphermod=AES)
        cmacObj.update(authKey_2)
        authCmacKey_2 = cmacObj.digest()

        cmacObj = CMAC.new(session.sessionKey, ciphermod=AES)
        cmacObj.update(authKey_3)
        authCmacKey_3 = cmacObj.digest()

        cmacObj = CMAC.new(session.sessionKey, ciphermod=AES)
        cmacObj.update(authKey_4)
        authCmacKey_4 = cmacObj.digest()

        authCmacCombined_1 = authCmacKey_1 + authCmacKey_2
        authCmacCombined_2 = authCmacKey_3 + authCmacKey_4

        session.derivedKeys['enc'] = encCmacKey
        session.derivedKeys['auth_1'] = authCmacCombined_1
        session.derivedKeys['auth_2'] = authCmacCombined_2

        licHmac = HMAC.new(session.derivedKeys['auth_1'], digestmod=SHA256)
        licHmac.update(license.Msg.SerializeToString())

        if licHmac.digest() != license.Signature:
            with open("originalLic.bin", "wb") as f:
                f.write(base64.b64decode(b64License))
            with open("parsedLic.bin", "wb") as f:
                f.write(license.SerializeToString())
        
        for key in license.Msg.Key:
            if key.Id: keyId = key.Id
            else: keyId = wv_proto2.License.KeyContainer.KeyType.Name(key.Type).encode('utf-8')

            encryptedKey = key.Key
            iv = key.Iv
            type = wv_proto2.License.KeyContainer.KeyType.Name(key.Type)

            cipher = AES.new(session.derivedKeys['enc'], AES.MODE_CBC, iv=iv)
            decryptedKey = cipher.decrypt(encryptedKey)

            if type == "OPERATOR_SESSION":
                permissions = []
                perms = key._OperatorSessionKeyPermissions

                for (descriptor, value) in perms.ListFields():
                    if value == 1:
                        permissions.append(descriptor.name)
            else:
                permissions = []

            session.keys.append(Key(keyId, type, Padding.unpad(decryptedKey, 16), permissions))

    def getKeys(self, sessionId):
        if sessionId in self.sessions: return self.sessions[sessionId].keys
        else: logger.error("Session ID not found!", 1)
