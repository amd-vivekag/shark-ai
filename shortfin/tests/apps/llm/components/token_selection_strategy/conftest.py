# Copyright 2024 Advanced Micro Devices, Inc.
#
# Licensed under the Apache License v2.0 with LLVM Exceptions.
# See https://llvm.org/LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import asyncio
import pytest
from unittest.mock import patch
from uuid import uuid4

from shortfin.support.status_tracker import AbstractStatusTracker
from shortfin_apps.llm.components.messages import (
    LlmInferenceExecRequest,
    InferencePhase,
)
from shortfin_apps.llm.components.token_selection_strategy import (
    DecodeConfig,
)


class MockVoidFuture:
    def __init__(self):
        self._event = asyncio.Event()

    def set_success(self):
        self._event.set()

    def __await__(self):
        return self._event.wait().__await__()


@pytest.fixture(scope="function")
def exec_req():
    with patch(
        "shortfin_apps.llm.components.messages.sf.VoidFuture", new=MockVoidFuture
    ):

        class MockStatusTracker(AbstractStatusTracker):
            def __init__(self):
                pass

            def is_disconnected(self):
                return False

        yield LlmInferenceExecRequest(
            phase=InferencePhase.PREFILL,
            input_token_ids=[0, 1, 2, 3, 4, 5],
            rid=str(uuid4()),
            status_tracker=MockStatusTracker(),
        )


@pytest.fixture(scope="function")
def decode_config():
    yield DecodeConfig()
