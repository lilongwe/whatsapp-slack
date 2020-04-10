from utilities.ParameterValidator import ParameterValidator

def test_validateStringWithValue():

	validator:ParameterValidator = ParameterValidator()

	parameter:str = "string"
	validated:str = validator.validateString(parameter)

	assert parameter == validated

def test_validateStringWithNoValue():

	validator:ParameterValidator = ParameterValidator()

	parameter:str = ""
	validated:str = validator.validateString(parameter)

	assert None == validated

	parameter:str = None
	validated:str = validator.validateString(parameter)

	assert None == validated

def test_validateStringWithDefault():

	validator:ParameterValidator = ParameterValidator()

	parameter:str = ""
	default:str = 10
	validated:str = validator.validateString(parameter, default)

	assert str(default) == validated

	default:str = None
	validated:str = validator.validateString(parameter, default)

	assert None == validated 