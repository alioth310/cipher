#! /usr/bin/python
# -*- coding: utf-8 -*-

if __name__ == "__main__":
    from basemodel import create_session, init_db

    session = create_session()
    session.execute("drop database cipher")
    session.execute("create database cipher")
    init_db()

