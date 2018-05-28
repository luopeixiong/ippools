# coding:utf-8



class PoolEmptyError(Exception):
    def __str__(self):
        return '<class PoolEmptyError at 0x%x>' % id(self)