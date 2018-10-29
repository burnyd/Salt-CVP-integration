from __future__ import absolute_import, print_function, unicode_literals
from cvprac.cvp_client import CvpClient
import salt
import urllib3


urllib3.disable_warnings()


"""Checks to see if the cvp.sls file is currently within the pillars"""
def config():
    config = __salt__['config.get']('cvp')
    if not config:
        raise CommandExecutionError(
            'cvp execution module configuration could not be found'
        )
    return config

"""Check to see if the pillar file has all the necessary informaiton"""
def config_dict():
    cvp_dict = {}
    cvp_dict['server'] = config().get('server')
    cvp_dict['username'] = config().get('username')
    cvp_dict['password'] = config().get('password')
    return cvp_dict

"""Connects to the cvp API"""
def connect_cvp():
    urllib3.disable_warnings()
    client = CvpClient()
    client.connect([config_dict()['server']], config_dict()['username'], config_dict()['password'])
    return client

"""salt 'minionid' cvptest.load_config 'ONUG' 'hostname test-device' would simply add text config to the cvp server"""
def load_config(config_name, configlet):
    client = connect_cvp()
    add = client.api.add_configlet(config_name, configlet)

"""salt 'minionid' cvptest.load_template 'salt-test' salt://logging2.cfg would simply render a template from a specific location to the cvp master."""

def load_template(config_name, configlet):
    client = connect_cvp()
    files = __salt__['cp.get_file_str'](configlet)
    add = client.api.add_configlet(config_name, files)

