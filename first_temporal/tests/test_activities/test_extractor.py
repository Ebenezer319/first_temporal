import os
import pytest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch, MagicMock

import pandas as pd
from temporalio.testing import ActivityEnvironment

from first_temporal.activities import extractor
from shared import RunPlaceholder


@pytest.mark.asyncio
@patch('first_temporal.activities.extractor.randint')
async def test_pull_recent_purchases(mock_random: MagicMock):
    """
    Should have a tuple as the result where the first object is of length 1 and
    the second is 19
    """
    activity_environment = ActivityEnvironment()
    mock_random.return_value = 19
    run_holder = [{
        'previous_date': f'{datetime(2020, 6, 7).date()}',
        'last_customer_id': 333333,
        'last_transaction_id': 3
    }]
    purchase_args = {'run_checkpoint': run_holder}
    results = await activity_environment.run(
        extractor.pull_recent_purchases, purchase_args
    )

    assert len(results[0]) == 1
    assert len(results[1]) == 19