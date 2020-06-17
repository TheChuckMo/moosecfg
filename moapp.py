#!/usr/bin/env python

"""Test app for Moose Configurator."""

import click
import yaml
from moosecfg import MooseConfigurator

MooseConfigurator.UPDATE_AT_INIT = True
MooseConfigurator.SYSTEM_OVERRIDE = False
MooseConfigurator.LOCAL_FILE_LOAD = True
MooseConfigurator.LOCAL_FILE_HIDDEN = False

cfg = MooseConfigurator('moapp')


print(f'--system-configuration--')
print(f'system configuration file: {cfg.system_full_path}')
print(f'system configuration: {yaml.safe_dump(cfg.system.obj)}')

print(f'--user-configuration--')
print(f'user configuration file: {cfg.user_full_path}')
print(f'user configuration: {yaml.safe_dump(cfg.user.obj)}')

print(f'--local-configuration--')
print(f'local configuration file: {cfg.local_full_path}')
print(f'local configuration: {yaml.safe_dump(cfg.local.obj)}')

print(f'--configuration--')
print(f'configuration object: {yaml.safe_dump(cfg.obj)}')

