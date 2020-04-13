from utilities.ParameterValidator import ParameterValidator
import pytest

@pytest.mark.parametrize("parameter", ["string", "\n string \r"])
def test_validateStringWithValue(parameter):

	validator:ParameterValidator = ParameterValidator()

	validated:str = validator.validateString(parameter)

	assert parameter == validated

@pytest.mark.parametrize("parameter, expected", 
							[("", None), 
							("\n  \r", None),
							("   ", None),
							(None, None)])
def test_validateStringWithNoValue(parameter, expected):

	validator:ParameterValidator = ParameterValidator()

	validated:str = validator.validateString(parameter)

	assert expected == validated

@pytest.mark.parametrize("parameter, default, expected", 
							[("", 10, "10"), 
							(None, None, None),
							("", None, None)])
def test_validateStringWithDefault(parameter, default, expected):

	validator:ParameterValidator = ParameterValidator()

	validated:str = validator.validateString(parameter, default)

	assert expected == validated

@pytest.mark.parametrize("parameter", [10, -50])
def test_validateIntegerWithValue(parameter):

	validator:ParameterValidator = ParameterValidator()

	validated:int = validator.validateInteger(parameter)

	assert parameter == validated


@pytest.mark.parametrize("parameter, expected", 
							[("", None), 
							("\n  \r", None),
							(10.4, None),
							(None, None)])
def test_validateIntegerWithNoValue(parameter, expected):

	validator:ParameterValidator = ParameterValidator()

	validated:int = validator.validateInteger(parameter)

	assert expected == validated


@pytest.mark.parametrize("parameter, default, expected", 
							[("", 10, 10),
							("15", "23", 23),
							("", 23.3, 23),
							("rfdfdsf", "23.3", None),
							("", "test", None),  
							(None, None, None),
							("", None, None)])
def test_validateIntegerWithDefault(parameter, default, expected):

	validator:ParameterValidator = ParameterValidator()

	validated:int = validator.validateInteger(parameter, default)

	assert expected == validated