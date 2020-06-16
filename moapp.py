#!/usr/bin/env python

"""Test app for Moose Configurator."""

import click
from moosecfg import MooseConfigurator

MooseConfigurator.UPDATE_AT_INIT = True
MooseConfigurator.SYSTEM_OVERRIDE = False
MooseConfigurator.LOCAL_FILE_LOAD = True
MooseConfigurator.LOCAL_FILE_HIDDEN = False

cfg = MooseConfigurator('moapp')

print(f'system configuration file: {cfg.system_cfg_file}')
print(f'user configuration file: {cfg.user_cfg_file}')
print(f'local configuration file: {cfg.local_cfg_file}')
print(f'system configuration: {cfg.system_cfg}')
print(f'user configuration: {cfg.user_cfg}')
print(f'local configuration: {cfg.local_cfg}')
print(f'configuration object: {cfg.obj}')

