"""Module for local time firmware version from API."""
from .api_event import ApiEvent
from .frames import FrameGetLocalTimeConfirmation, FrameGetLocalTimeRequest
from datetime import datetime
import time

class DtoLocalTime:
    def __init__(self, utctime = None, localtime = None):
        self.utctime = utctime
        self.localtime = localtime


    def __str__(self):
        """Return human readable string."""
        return (
            '<"{}" utctime = "{}" localtime = "{}" />'.format(
                self.__class__.__name__ ,self.utctime, self.localtime
            )
        )



class GetLocalTime(ApiEvent):
    """Class for retrieving firmware version from API."""

    def __init__(self, pyvlx):
        """Initialize GetLocalTime class."""
        super().__init__(pyvlx=pyvlx)
        self.success = False
        self.localtime = DtoLocalTime()

    async def handle_frame(self, frame):
        """Handle incoming API frame, return True if this was the expected frame."""
        if not isinstance(frame, FrameGetLocalTimeConfirmation):
            return False
        if frame.weekday == 0:
                wd = 6 
        else: 
                wd = frame.weekday -1
        self.time = DtoLocalTime(datetime.fromtimestamp(frame.utctime),
                                 datetime.fromtimestamp(time.mktime((frame.year+1900, frame.month, frame.dayofmonth, frame.hour, frame.minute, frame.second, wd, frame.dayofyear, frame.daylightsavingflag))))
        self.success = True
        
        return True

    def request_frame(self):
        """Construct initiating frame."""
        return FrameGetLocalTimeRequest()
