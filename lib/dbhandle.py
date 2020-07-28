#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-
import MySQLdb as mysqldb

class mysql_db( object ):
    def __init__( self, mysql_host, mysql_userid, mysql_userpw, mysql_dbname ):
        try:
            self.connect = mysqldb.connect( mysql_host, mysql_userid, mysql_userpw, mysql_dbname, cursorclass=MySQLdb.cursors.DictCursor, charset='utf8' )
            self.cursor = self.connect.cursor()
            self.cursor.autocommit(True)
            #self.cursor.commit()
            return self
        except:
            return None

    def do_query( self, query_str ):
        self.cursor.execute( query_str )
        self.connect.commit()
        return self.cursor.fetchall()

    def get_cursor( self ):
        return self.cursor

    def do_commit( self ):
        return self.connect.commit()

    def do_fetch( self ):
        return self.cursor.fetchall()
