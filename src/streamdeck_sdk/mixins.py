import json
from typing import Union

import pydantic
import websocket
from websocket import ABNF

from .sd_objs import events_received_objs, events_sent_objs
from .logger import log_errors


class SendMixin:
    ws: websocket.WebSocketApp

#    @log_errors
    @classmethod
    def send(
            self,
            data: Union[pydantic.BaseModel, dict, str],
            opcode=ABNF.OPCODE_TEXT,
    ) -> None:
        if isinstance(data, pydantic.BaseModel):
            data = data.json(ensure_ascii=False)
        elif isinstance(data, dict):
            data = json.dumps(data, ensure_ascii=False)
        self.ws.send(data, opcode)


class BaseEventSendMixin(SendMixin):
    pass


class PluginEventsSendMixin(BaseEventSendMixin):
    plugin_uuid: str

    @classmethod
    def set_global_settings(self, payload: dict) -> None:
        message = events_sent_objs.SetGlobalSettings(
            context=self.plugin_uuid,
            payload=payload,
        )
        self.send(message)

    @classmethod
    def get_global_settings(self) -> None:
        message = events_sent_objs.GetGlobalSettings(
            context=self.plugin_uuid,
        )
        self.send(message)

    @classmethod
    def open_url(self, url: str) -> None:
        message = events_sent_objs.OpenUrl(
            payload=events_sent_objs.OpenUrlPayload(
                url=url,
            ),
        )
        self.send(message)

    @classmethod
    def log_message(self, message: str) -> None:
        message = events_sent_objs.LogMessage(
            payload=events_sent_objs.LogMessagePayload(
                message=message,
            ),
        )
        self.send(message)

    @classmethod
    def switch_to_profile(
            self,
            device: str,
            profile: str,
    ) -> None:
        message = events_sent_objs.SwitchToProfile(
            context=self.plugin_uuid,
            device=device,
            payload=events_sent_objs.SwitchToProfilePayload(
                profile=profile,
            ),
        )
        self.send(message)


class ActionEventsSendMixin(BaseEventSendMixin):
    def set_settings(
            self,
            payload: dict,
    ) -> None:
        message = events_sent_objs.SetSettings(
            context=self.context,
            payload=payload,
        )
        self.send(message)

    def get_settings(
            self,
    ) -> None:
        message = events_sent_objs.GetSettings(
            context=self.context,
        )
        self.send(message)

    def set_title(
            self,
            payload: events_sent_objs.SetTitlePayload,
    ) -> None:
        message = events_sent_objs.SetTitle(
            context=self.context,
            payload=payload,
        )
        self.send(message)

    def set_image(
            self,
            payload: events_sent_objs.SetImagePayload,
    ) -> None:
        message = events_sent_objs.SetImage(
            context=self.context,
            payload=payload,
        )
        self.send(message)

    def set_feedback(
            self,
            payload: dict,
    ) -> None:
        message = events_sent_objs.SetFeedback(
            context=self.context,
            payload=payload,
        )
        self.send(message)

    def set_feedback_layout(
            self,
            layout: str,
    ) -> None:
        message = events_sent_objs.SetFeedbackLayout(
            context=self.context,
            payload=events_sent_objs.SetFeedbackLayoutPayload(
                layout=layout
            ),
        )
        self.send(message)

    def show_alert(
            self,
    ) -> None:
        message = events_sent_objs.ShowAlert(
            context=self.context,
        )
        self.send(message)

    def show_ok(
            self,
    ) -> None:
        message = events_sent_objs.ShowOk(
            context=self.context,
        )
        self.send(message)

    def set_state(
            self,
            state: int,
    ) -> None:
        message = events_sent_objs.SetState(
            context=self.context,
            payload=events_sent_objs.SetStatePayload(
                state=state
            )
        )
        self.send(message)

    def send_to_property_inspector(
            self,
            payload: dict,
    ):
        message = events_sent_objs.SendToPropertyInspector(
            action=self.UUID,
            context=self.context,
            payload=payload
        )
        self.send(message)


class BaseEventHandlerMixin:
    pass


class ActionEventHandlersMixin(BaseEventHandlerMixin):
    def on_did_receive_settings(self, obj: events_received_objs.DidReceiveSettings) -> None:
        pass

    def on_key_down(self, obj: events_received_objs.KeyDown) -> None:
        pass

    def on_key_up(self, obj: events_received_objs.KeyUp) -> None:
        pass

    def on_touch_tap(self, obj: events_received_objs.TouchTap) -> None:
        pass

    def on_dial_down(self, obj: events_received_objs.DialDown) -> None:
        pass

    def on_dial_up(self, obj: events_received_objs.DialUp) -> None:
        pass

    def on_dial_press(self, obj: events_received_objs.DialPress) -> None:
        pass

    def on_dial_rotate(self, obj: events_received_objs.DialRotate) -> None:
        pass

    def on_will_appear(self, obj: events_received_objs.WillAppear) -> None:
        pass

    def on_will_disappear(self, obj: events_received_objs.WillDisappear) -> None:
        pass

    def on_title_parameters_did_change(self, obj: events_received_objs.TitleParametersDidChange) -> None:
        pass

    def on_property_inspector_did_appear(self, obj: events_received_objs.PropertyInspectorDidAppear) -> None:
        pass

    def on_property_inspector_did_disappear(self, obj: events_received_objs.PropertyInspectorDidDisappear) -> None:
        pass

    def on_send_to_plugin(self, obj: events_received_objs.SendToPlugin) -> None:
        pass

    def on_send_to_property_inspector(self, obj: events_received_objs.SendToPropertyInspector) -> None:
        pass


class PluginEventHandlersMixin(BaseEventHandlerMixin):
    @classmethod
    def on_did_receive_global_settings(self, obj: events_received_objs.DidReceiveGlobalSettings) -> None:
        pass

    @classmethod
    def on_device_did_connect(self, obj: events_received_objs.DeviceDidConnect) -> None:
        pass

    @classmethod
    def on_device_did_disconnect(self, obj: events_received_objs.DeviceDidDisconnect) -> None:
        pass

    @classmethod
    def on_application_did_launch(self, obj: events_received_objs.ApplicationDidLaunch) -> None:
        pass

    @classmethod
    def on_application_did_terminate(self, obj: events_received_objs.ApplicationDidTerminate) -> None:
        pass

    @classmethod
    def on_system_did_wake_up(self, obj: events_received_objs.SystemDidWakeUp) -> None:
        pass
