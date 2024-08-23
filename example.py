import asyncio

from pynocodb import Client, AsyncClient
from rich import print


def run_sync():
    # here we use an api token.
    # you can do client.auth.signin to use auth token instead
    client = Client(token="YzDNLisEZQ4AuId1i9sodHbDC2eEJxadiAlRUHXu")

    bases = client.base.get_base_ids()
    print(bases)
    base_id = list(bases.values())[0]
    tables = client.table.get_table_ids(base_id)
    print(tables)
    table_id = list(tables.values())[0]
    print(client.record.list_records(table_id)["list"])


async def run_async():
    client = AsyncClient()
    await client.auth.signin("liunux@qq.com", "r_PypPUajC6y!2B")

    bases = await client.base.get_base_ids()
    print(bases)
    base_id = list(bases.values())[0]
    tables = await client.table.get_table_ids(base_id)
    print(tables)
    table_id = list(tables.values())[0]
    print((await client.record.list_records(table_id))["list"])


if __name__ == "__main__":
    # run_sync()
    asyncio.run(run_async())
