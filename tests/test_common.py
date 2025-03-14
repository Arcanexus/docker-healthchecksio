from datetime import datetime

import src.modules.common as common


def test_get_formatted_datetime():
  result = common.get_formatted_datetime()
  assert isinstance(result, str)
  assert len(result) == 17  # Format "31-Dec-2023 19:34" is 17 characters long

  # Check if the formatted date is correct
  now = datetime.now()
  expected_format = now.strftime("%d-%b-%Y %H:%M")
  assert result == expected_format


def test_to_camel_case():
  assert common.to_camel_case("hello world") == "helloWorld"
  assert common.to_camel_case("Hello World") == "helloWorld"
  assert common.to_camel_case("hello_world") == "helloWorld"
  assert common.to_camel_case("hello-world") == "helloWorld"
  assert common.to_camel_case("hello world 123") == "helloWorld123"
  assert common.to_camel_case("123 hello world") == "123HelloWorld"
  assert common.to_camel_case("HELLO WORLD") == "helloWorld"
  assert common.to_camel_case("HELLO-WORLD") == "helloWorld"
  assert common.to_camel_case("helloWorld") == "helloworld"
  assert common.to_camel_case("HelloWorld") == "helloworld"
  assert common.to_camel_case("hello  world") == "helloWorld"
  assert common.to_camel_case("hello_world_") == "helloWorld"
