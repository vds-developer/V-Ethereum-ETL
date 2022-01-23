import click
from ETL.providers.provider import get_provider
import json
import time
from kafka import KafkaProducer
from hexbytes import HexBytes

class HexJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, HexBytes):
            return obj.hex()
        return super().default(obj)
@click.group()
def cli():
    pass

@click.command()
@click.option('--provider', "-p",required=True, type=click.Choice(['ipc', 'websocket', 'http']), default='ipc')
@click.option('--address', '-a', required=True, default='~/.ethereum/geth.ipc=')
# @click.option('--output', '-o', required=True, default='~/.vetl/output/block/')
@click.option('--bootstrap-server', '-b', required=True, default='localhost:9092')
def export_block_to_kafka(provider, address, bootstrap_server):
    web3 = get_provider(provider, address)
    consumer = KafkaProducer(bootstrap_servers = [bootstrap_server], acks = 'all', retries=5 )
    click.echo(consumer.bootstrap_connected())
    block = web3.eth.get_block('latest')
    latest = None
    while True:
        current_block = web3.eth.get_block('latest')
        if latest is None or current_block['number'] != latest:
            latest = current_block['number']
            tx_dict = dict(current_block)
            tx_dict['timestamp'] = tx_dict['timestamp'] * 1000
            tx_json = json.dumps(tx_dict, cls=HexJsonEncoder, indent=4, sort_keys=True).encode('utf-8')
            future = consumer.send('test-topic', tx_json)
            record_metadata = future.get(timeout=10)
            click.echo(record_metadata.topic)
            click.echo(record_metadata.partition)
            click.echo(record_metadata.offset)
        time.sleep(60)



cli.add_command(export_block_to_kafka)

if __name__ == '__main__':
    cli()