import sys
import uuid

from rich.console import Console
from rich.table import Table

FLAG = 'Securinets{Revenge_Revenge_Revenge_!!!4531asedwf}'

users = [
        {'username': 'Alice',   'password':     "IsRSAacommunistscheme",   'wallet': 1001,       'cd': '2023-01-06', 'role': 'guest'},
        {'username': 'Bob',     'password':     'Belkhadem tewled fi gouna',     'wallet': 2023,         'cd': '2023-04-20', 'role': 'guest'},
        {'username': 'Mallory', 'password':     'If you guessed the password  you should win the ctf', 'wallet': 1234,     'cd': '2023-05-21', 'role': 'guest'},
]

transfers = [
        {'ref': '1d09cc3f', 'sender': 'Bob', 'receiver': 'Alice', 'amount': 1, 'label': 'test', 'status': 'done'},
        {'ref': 'a36eca5c', 'sender': 'Mallory', 'receiver': 'Alice', 'amount': 337, 'label': 'for charity', 'status': 'pending'},
]

class Server:
        def __init__(self):
                pass

        def login(self, u, p):
                for user in users:
                        if user['username'] == u and user['password'] == p:
                                return True
                return False

        def logout(self):
                print('Goodbye.')


class Client:
        def __init__(self, u, p):
                self.username = u
                self.password = p

        def show_info(self):
                table = Table(title="Personal Info")
                table.add_column("Username")
                table.add_column("Wallet")
                table.add_column("Role")
                table.add_column("Creation date")

                current_user = []
                for user in users:
                        if user['username'] == self.username:
                                current_user = user
                                break

                if current_user['wallet'] > 1337:
                        table.add_column("Special award")
                        table.add_row(user['username'], str(user['wallet'])+'$', user['role'], user['cd'])
                        print(FLAG)
                else:
                        table.add_row(user['username'], str(user['wallet'])+'$', user['role'], user['cd'])

                console = Console()
                console.print(table)
                print('*IMPORTANT* : Accounts which worth more than 1337$ will get a special award.')

        def list_clients(self):
                table = Table(title="Clients")
                table.add_column("Username")
                table.add_column("Wallet")

                for user in users:
                        table.add_row(user['username'], str(user['wallet'])+'$')

                console = Console()
                console.print(table)

        def list_transfers(self):
                table = Table(title="Transfers")
                table.add_column("Reference")
                table.add_column("Sender")
                table.add_column("Receiver")
                table.add_column("Amount")
                table.add_column("Label")
                table.add_column("Status")

                for transfer in transfers:
                        table.add_row(transfer['ref'], transfer['sender'], transfer['receiver'], str(transfer['amount'])+'$', transfer['label'], transfer['status'])

                console = Console()
                console.print(table)

        def set_transfer(self, r, a, l):
                if a <= 0:
                        return None, 'Invalid ammount.'
                if not l.replace(' ', '').isalnum():
                        return None, 'The label should be alphanumeric.'
                if r == self.username:
                        return None, "You can't make a transfer to yourself."
                for user in users:
                        if user['username'] == r:
                                if a > users[0]['wallet']:
                                        return None, "You don't have enough money."
                                else:
                                        transfer = {
                                                'ref' : str(uuid.uuid4()).split('-')[0],
                                                'sender' : self.username,
                                                'receiver' : r,
                                                'amount' : int(a),
                                                'label' : l,
                                                'status' : 'pending'
                                        }
                                        transfers.append(transfer)
                                        return transfer['ref'],""
                return None, 'No receiver exists with this name.'

        def update_transfer(self, i):
                for transfer in transfers:
                        if transfer['ref'] == i:
                                if transfer['status'] == 'done':
                                        return False
                                transfer['status'] = 'done'
                                for user in users:
                                        if user['username'] == transfer['sender']:
                                                user['wallet'] -= transfer['amount']
                                        elif user['username'] == transfer['receiver']:
                                                user['wallet'] += transfer['amount']
                return True

        def get_transfer_by_ref(self, i):
                for transfer in transfers:
                        if transfer['ref'] == i:
                                return transfer, ''
                return None, 'No transfer exists with this reference.'