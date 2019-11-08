"""Model classes related to a single client connected to the server."""

from __future__ import absolute_import

import attr

from typing import Optional, Union

from flockwave.server.logger import log as base_log

from .channel import CommunicationChannel
from .user import User

__all__ = ("Client",)

log = base_log.getChild("model.clients")  # plural to match registry.clients


@attr.s(eq=False)
class Client(object):
    """A single client connected to the Flockwave server."""

    _id: str = attr.ib()
    _channel: CommunicationChannel = attr.ib()
    _user: User = attr.ib(default=None)

    @property
    def channel(self) -> CommunicationChannel:
        """The communication channel that the client uses to connect to
        the server.
        """
        return self._channel

    @property
    def id(self) -> str:
        """A unique identifier for the client, assigned at construction
        time.
        """
        return self._id

    @property
    def user(self) -> User:
        """The user that is authenticated on the communication channel that
        this client uses.
        """
        return self._user

    @user.setter
    def user(self, value: Optional[Union[str, User]]) -> None:
        if value is not None and not isinstance(value, User):
            value = User.from_string(value)

        if value is self._user:
            return

        if self._user is not None:
            raise RuntimeError(
                "cannot re-authenticate a channel once it is already authenticated"
            )

        self._user = value

        if value:
            log.info(f"Authenticated as {value}", extra={"id": self._id})
        else:
            log.info("Deauthenticated current user")
