from pynocodb import Client
import pytest
from rich import print


client = Client()


def clear_test_data():
    # we need an api token to clear test bases
    # nocodb not provide an api to delete user, need to delete user in webui mannually before test.
    client.set_token(pytest.data.API_TOKEN)

    # clear existed test base & tables &users when test interrupted
    while True:
        bases = client.base.get_base_ids()
        if base_id := bases.get(pytest.data.BASE):
            r = client.base.delete_base(base_id)
            print(r)
            # clear existed test user
            user_ids = client.base.get_base_user_ids(base_id)
            if user_id := user_ids.get(pytest.data.USER_EMAIL):
                r = client.base.delete_base_user(base_id, user_id)
                print(r)
        else:
            break


def setup_module():
    clear_test_data()


def teardown_module():
    clear_test_data()


def test_auth():
    USER_EMAIL = pytest.data.USER_EMAIL
    USER_PASSWORD = pytest.data.USER_PASSWORD

    # signup
    r = client.auth.signup(USER_EMAIL, USER_PASSWORD)
    print(r)
    assert "token" in r

    r = client.auth.signup(USER_EMAIL, USER_PASSWORD)
    print(r)
    assert r == {"msg": "User already exist"}

    # signout
    r = client.auth.signout()
    print(r)
    assert r == {"msg": "Signed out successfully"}

    # singin
    r = client.auth.signin(USER_EMAIL, USER_PASSWORD)
    print(r)
    assert "token" in r

    # get user info
    r = client.auth.user_info()
    print(r)
    assert r["email"] == USER_EMAIL

    # # send forgot password email
    # # skip, it will break normal auth ability for this user
    # r = client.auth.forgot_password(USER_EMAIL)
    # print(r)
    # assert (r == {"msg": "Please check your email to reset the password"}
    #         or r == {"msg": "Email Plugin is not found. Please contact administrators to configure it in App Store first."})

    # change password
    r = client.auth.change_password(USER_PASSWORD, "22222222")
    print(r)
    assert r == {"msg": "Password has been updated successfully"}
    client.auth.refresh_token()

    r = client.auth.change_password("22222222", USER_PASSWORD)
    print(r)
    assert r == {"msg": "Password has been updated successfully"}

    # refresh token
    r = client.auth.refresh_token()
    print(r)
    assert "token" in r


def test_base():
    USER_EMAIL = pytest.data.USER_EMAIL
    USER_PASSWORD = pytest.data.USER_PASSWORD

    # client.auth.signin(USER_EMAIL, USER_PASSWORD)
    client.set_token(pytest.data.API_TOKEN)

    base_id = ""
    user_id = ""
    print("start test base and tables:\n")

    # create new base
    r = client.base.create_base(pytest.data.BASE)
    print(r)
    assert r["title"] == pytest.data.BASE
    base_id = r["id"]

    # add user to base
    r = client.base.create_base_user(base_id, USER_EMAIL, "owner")
    print(r)
    assert r == {"msg": "The user has been invited successfully"}

    # list base users
    r = client.base.list_base_users(base_id)
    print(r)
    assert "users" in r
    for x in r["users"]["list"]:
        if x["email"] == USER_EMAIL:
            user_id = x["id"]

    # update user roles
    r = client.base.update_base_user(base_id, user_id, USER_EMAIL, "editor")
    print(r)
    assert r == {"msg": "The user has been updated successfully"}

    ### table operations

    # create table
    r = client.table.create_table(base_id, pytest.data.TABLE, columns=[])
    print(r)
    assert r["type"] == "table"
    table_id = r["id"]

    # list tables
    r = client.table.list_tables(base_id)
    print(r)
    assert table_id in [x["id"] for x in r["list"]]

    # delete table
    r = client.table.delete_table(table_id)
    r = client.table.list_tables(base_id)
    print(r)
    assert table_id not in [x["id"] for x in r["list"]]

    ### table operations

    ### record operations
    # create record

    # update record

    # list records

    # links record

    # unlink record

    ### record operations

    # remove user from base
    r = client.base.delete_base_user(base_id, user_id)
    print(r)
    assert r == {"msg": "The user has been deleted successfully"}

    # # resend invitation to user
    # r = client.base.resend_invite(base_id, user_id)
    # print(r)
    # assert r == {"msg": "The invitation has been sent to the user"}


# def test_source():
#     # list sources
#     r = client.source.get_sources("pl4c6cv5yajn1p6")
#     print(r)
