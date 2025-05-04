from app.utils.factory_builder import ObjectFactory
from .infobip.infobip import InfobipClient
from .messagebird.messagebird import MessageBirdClient
from .mobizon.mobizon import MobizonClient
from .nexmo.nexmo import NexmoClient
from .p1sms.p1sms import P1SMSClient
from .smsru.smsru import SMSRuClient
from .twilio.twilio import TwilioClient
from .unicore.unicore import UnicoreClient
from .zvonobot.zvonobot import ZvonobotClient

notification_factory = ObjectFactory()
notification_factory.register('infobit', InfobipClient)
notification_factory.register('messagebird', MessageBirdClient)
notification_factory.register('mobizon', MobizonClient)
notification_factory.register('nexmo', NexmoClient)
notification_factory.register('p1sms', P1SMSClient)
notification_factory.register('smsru', SMSRuClient)
notification_factory.register('twilio', TwilioClient)
notification_factory.register('unicore', UnicoreClient)
notification_factory.register('zvonobot', ZvonobotClient)
