"""
gRPC server for the Auth Service.

Runs alongside the FastAPI HTTP server.
"""

import logging

import grpc

from ..config import settings
from .servicers.auth_servicer import AuthServiceServicer, UserServiceServicer

logger = logging.getLogger(__name__)


async def start_grpc_server():
    """
    Start the gRPC server.

    Note: When gRPC stubs are generated from auth.proto, uncomment
    the add_*Servicer_to_server lines. Until then, this serves as
    the server initialization reference.
    """
    server = grpc.aio.server()

    # Once stubs are generated, register servicers:
    # auth_pb2_grpc.add_AuthServiceServicer_to_server(
    #     AuthServiceServicer(), server
    # )
    # auth_pb2_grpc.add_UserServiceServicer_to_server(
    #     UserServiceServicer(), server
    # )

    listen_addr = f"[::]:{settings.GRPC_PORT}"
    server.add_insecure_port(listen_addr)
    await server.start()
    logger.info("gRPC server started on %s", listen_addr)
    return server
