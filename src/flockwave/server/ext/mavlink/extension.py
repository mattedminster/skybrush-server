"""Flockwave server extension that adds support for drone flocks using the
MAVLink protocol.
"""

from __future__ import absolute_import

from contextlib import ExitStack
from trio.abc import ReceiveChannel
from typing import Any, Dict

from flockwave.connections import Connection, create_connection
from flockwave.server.ext.base import UAVExtensionBase
from flockwave.server.model import ConnectionPurpose
from flockwave.server.utils import nop

from .comm import create_communication_manager, MAVLinkMessage
from .driver import MAVLinkDriver
from .utils import log_level_from_severity, log_id_from_message


__all__ = ("construct", "dependencies")


class MAVLinkDronesExtension(UAVExtensionBase):
    """Extension that adds support for drone flocks using the MAVLink
    protocol.
    """

    def __init__(self):
        super(MAVLinkDronesExtension, self).__init__()
        self._driver = None

    def _create_driver(self):
        return MAVLinkDriver()

    def _create_communication_links(
        self, configuration: Dict[str, Any]
    ) -> Dict[str, Connection]:
        """Creates the communication manager objects corresponding to the
        various MAVLink streams used by this extension.

        Parameters:
            configuration: the configuration dictionary of the extension

        Returns:
            Dict[]
        """
        connection_config = configuration.get("connections", {})
        return {
            name: create_connection(spec) for name, spec in connection_config.items()
        }

    def configure_driver(self, driver, configuration):
        """Configures the driver that will manage the UAVs created by
        this extension.

        It is assumed that the driver is already set up in ``self.driver``
        when this function is called, and it is already associated to the
        server application.

        Parameters:
            driver (UAVDriver): the driver to configure
            configuration (dict): the configuration dictionary of the
                extension
        """
        driver.id_format = configuration.get("id_format", "{0:02}")
        driver.log = self.log.getChild("driver")
        driver.create_device_tree_mutator = self.create_device_tree_mutation_context

    async def run(self, app, configuration):
        links = self._create_communication_links(configuration)

        with ExitStack() as stack:
            # Register the communication links
            for name, link in links.items():
                stack.enter_context(
                    app.connection_registry.use(
                        link,
                        f"MAVLink: {name}",
                        description=f"Upstream MAVLink connection ({name})",
                        purpose=ConnectionPurpose.uavRadioLink,
                    )
                )

            # Create the communication manager
            manager = create_communication_manager()

            # Register the links with the communication manager. The order is
            # important here; the first one will be used for sending, so that
            # must be the unicast link.
            for name, link in links.items():
                manager.add(link, name=name)

            # Start the communication manager
            await manager.run(
                consumer=self._handle_inbound_packets,
                supervisor=app.supervise,
                log=self.log,
            )

    async def _handle_inbound_packets(self, channel: ReceiveChannel):
        """Handles inbound data packets from all the communication links
        that the extension manages.

        Parameters:
            channel: a Trio receive channel that yields inbound data packets.
        """
        handlers = {"BAD_DATA": nop, "STATUSTEXT": self._handle_message_statustext}

        async for name, (message, swarm_id) in channel:
            type = message.get_type()
            handler = handlers.get(type)
            if handler:
                handler(message, name=name, swarm_id=swarm_id)
            else:
                self.log.warn(
                    f"Unhandled MAVLink message type: {type}",
                    extra={"id": log_id_from_message(message, swarm_id)},
                )
                handlers[type] = nop

    def _handle_message_statustext(
        self, message: MAVLinkMessage, *, name: str, swarm_id: str
    ):
        """Handles an incoming MAVLink STATUSTEXT message and forwards it to the
        log console.
        """
        self.log.log(
            log_level_from_severity(message.severity),
            message.text,
            extra={"id": log_id_from_message(message, swarm_id)},
        )


construct = MAVLinkDronesExtension
dependencies = ()
