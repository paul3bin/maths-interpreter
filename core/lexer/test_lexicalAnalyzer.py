from core import main_execute
import pytest
@pytest.mark.parametrize("test_input,expected",[("1+2",3),("5*10",50),("x=5",5),("x^2-1",24),("x>10",False)])

def test_get_tokens(test_input,expected):
    assert main_execute(test_input)==expected