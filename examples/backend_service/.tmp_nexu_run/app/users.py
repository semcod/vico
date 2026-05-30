# @intract.v1 scope:function intent:query:user_list priority:2 domain:users input:filters output:user_list effect:read forbid:write,network validate:input_presence,output_presence,no_forbidden_effect meaning:"return a filtered list of users without changing state"


def list_users(filters, users):
    role = filters.get("role")
    if not role:
        return {"user_list": users}
    return {"user_list": [user for user in users if user.get("role") == role]}
