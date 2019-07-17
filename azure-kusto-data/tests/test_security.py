"""Tests for security module."""
import pickle
from azure.kusto.data.exceptions import KustoAuthenticationError
from azure.kusto.data.request import KustoConnectionStringBuilder
from azure.kusto.data.security import _AadHelper, AuthenticationMethod


def test_unauthorized_exception():
    """Test the exception thrown when authorization fails."""

    cluster = "https://somecluster.kusto.windows.net"
    username = "username@microsoft.com"
    kcsb = KustoConnectionStringBuilder.with_aad_user_password_authentication(
        cluster, username, "StrongestPasswordEver", "authorityName"
    )
    aad_helper = _AadHelper(kcsb)

    try:
        aad_helper.acquire_authorization_header()
    except KustoAuthenticationError as error:
        assert error.authentication_method == AuthenticationMethod.aad_username_password.value
        assert error.authority == "https://login.microsoftonline.com/authorityName"
        assert error.kusto_cluster == cluster
        assert error.kwargs["username"] == username

def test_pickle():
    """_AadHelper needs to be serializeable"""
    cluster = "https://somecluster.kusto.windows.net"
    username = "username@microsoft.com"
    kcsb = KustoConnectionStringBuilder.with_aad_user_password_authentication(
        cluster, username, "StrongestPasswordEver", "authorityName")
    helper = _AadHelper(kcsb)
    p = pickle.dumps(helper)
    restored_helper = pickle.loads(p)
    assert restored_helper._kusto_cluster == cluster
