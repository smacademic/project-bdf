import sys
sys.path.append('..\\src')

import TextifyTwitter
import pytest

handle = []
handle.append('Hello I am searching for usernames, could come at the end @username')
handle.append('@bbacon and lets see it pick something from the beginning as well')
handle.append('It should @handle @multiple @usernames')
handle.append('What if there are no usernames?')
handle.append('@username checking @split usernames')
@pytest.mark.parametrize("extractUsernameInput,extractUsernameExpected",
    [
        (handle[0], ['@username']),
        (handle[1], ['@bbacon']),
        (handle[2], ['@handle', '@multiple', '@usernames']),
        (handle[3], []),
        (handle[4], ['@username', '@split'])
    ])
def test_extractUsername(extractUsernameInput, extractUsernameExpected):
    assert TextifyTwitter.extractUsername(extractUsernameInput) == extractUsernameExpected
