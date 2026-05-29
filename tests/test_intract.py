from vico.intract import parse_intract_line


def test_parse_intract_line():
    contract = parse_intract_line(
        '# @intract.v1 scope:function intent:query:user_list priority:2 domain:users input:filters output:user_list effect:read forbid:write validate:output_presence meaning:"list users"'
    )
    assert contract is not None
    assert contract.intent == "query:user_list"
    assert contract.domain == "users"
    assert "write" in contract.forbid
