from a_pubsub.processor import update_location

import pytest


@pytest.mark.parametrize(
    ('start', 'direction', 'expected'),
    [
        ((0, 0), 'w', (0, 1)),
        ((0, 0), 'a', (-1, 0)),
        ((0, 0), 's', (0, -1)),
        ((0, 0), 'd', (1, 0)),
        ((2, -3), 'w', (2, -2)),
        ((2, -3), 'd', (3, -3)),
        ((2, -3), 'W', (2, -2)),
        ((2, -3), 'x', (2, -3)),
    ],
)
def test_update_location(start, direction, expected):
    assert update_location(*start, direction) == expected
