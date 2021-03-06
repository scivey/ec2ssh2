#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

from ec2ssh2.env_dict import EnvDict
from ec2ssh2.util import ConstantDict
from ec2ssh2.args import get_args, parse_tag_filters

DEFAULTS = ConstantDict(
    EC2SSH2_VPC_SCOPE=None,
    EC2SSH2_TAG_FILTERS='',
    EC2SSH2_KEY_FILE_PATH=None,
    EC2SSH2_REMOTE_USER='ubuntu'
)


class Config(object):
    def __init__(self, env, tag_filters, args):
        self.env = env
        self.args = args
        self.tag_filters = tag_filters

    @classmethod
    def create(cls):
        env = EnvDict(DEFAULTS)
        args = get_args()
        tag_filters = {}
        if not args.escape_env:
            # doing this lazily would make InvalidInput
            # exceptions more confusing
            tag_filters.update(parse_tag_filters(
                env.EC2SSH2_TAG_FILTERS
            ))

        # command-line args have precedence
        tag_filters.update(args.tags)
        tag_filters = ConstantDict(**tag_filters)
        return cls(
            env=env,
            tag_filters=tag_filters,
            args=args
        )

    @property
    def vpc_scope(self):
        if self.args.vpc_scope:
            return self.args.vpc_scope
        elif not self.args.escape_env:
            return self.env.EC2SSH2_VPC_SCOPE
        return ''

    @property
    def remote_user(self):
        if self.args.user:
            return self.args.user
        elif not self.args.escape_env:
            return self.env.EC2SSH2_REMOTE_USER
        return ''

    @property
    def key_file_path(self):
        if self.args.key_file_path:
            return self.args.key_file_path
        elif not self.args.escape_env:
            return self.env.EC2SSH2_KEY_FILE_PATH
        return ''

    def __repr__(self):
        attrs = ('vpc_scope', 'remote_user', 'key_file_path')
        result = {attr: getattr(self, attr) for attr in attrs}
        result['tag_filters'] = {k: v for k, v in self.tag_filters.iteritems()}
        return repr(result)
