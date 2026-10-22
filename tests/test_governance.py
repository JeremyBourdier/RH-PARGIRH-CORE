from modules.governance import authenticate_operator


def test_operator_authentication_requires_configured_password():
    assert authenticate_operator("operator-secret", "") is False
    assert authenticate_operator("", "operator-secret") is False


def test_operator_authentication_accepts_only_exact_password():
    assert authenticate_operator("operator-secret", "operator-secret") is True
    assert authenticate_operator("wrong-secret", "operator-secret") is False
