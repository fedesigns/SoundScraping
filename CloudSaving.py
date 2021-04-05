import os
import requests
from urllib.parse import urlparse
from time import sleep
from Credentials import db_endpoint, db_port, database, username, password, access_key_ID, secret_access_key
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import sql


def s3_save_image(image_url, artist_id, track_id, artist_name, track_name, folder, client, bucket='sound-scraping', endpoint = 'eu-west-3'):


    ## getting png data, storing it into handle file object
    # with open(file_name, 'wb+') as handle:
    response = requests.get(image_url)

    if response.status_code == 200:

        raw_data = response.content
        url_parser = urlparse(image_url)
        file_name_server = os.path.basename(url_parser.path)
        file_name = f"{artist_id}-{track_id}-{file_name_server}" 
        file_key = folder + '/' + file_name

        try:
            # Write the raw data as byte in new file_name in the server
            with open(file_name_server, 'wb') as new_file:
                new_file.write(raw_data)

            # open the server file as read mode and upload it in bucket
            data = open(file_name_server, 'rb')

            client.Bucket(bucket).put_object(Key=file_key, Body=data) # , ExtraArgs={'MetaData': {'ArtistName': artist_name, 'TrackName': track_name, 'ArtistID': artist_id, 'TrackId': track_id}})
            data.close()
        
            # Format the return URL of upload file in S3 Bucket
            file_url = 'https://%s.%s/%s' % (bucket, endpoint, file_key)
            print("Attachment Successfully save in S3 Bucket url %s " % (file_url))
            return file_url

        except Exception as e:
            print("Error in file upload %s." % (str(e)))
        
        finally:
            # Close and remove file from Server
            new_file.close()
            sleep(1)
            os.remove(file_name_server)
            

            '''
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)
            '''
            ## putting data into file in S3 folder
            '''
            client.Object(bucket, file_key).put(Body=handle, 
                                                Metadata={'ArtistName': artist_name, 'TrackName': track_name})
            
            k = Key(bucket)
            k.name = "logo3w"
            k.set_contents_from_string(response.read(), {'Content-Type': response.info().gettype()})
            '''
    # try:
        # client.Bucket(bucket).upload_fileobj(handle, file_key, ExtraArgs={'MetaData': {'ArtistName': artist_name, 'TrackName': track_name}})
    # except ClientError as e:
        # logging.error(e)
        
    ## returning a file path to appen to database


def pd_from_table(table_name):
    '''
    Query data from pstgreSQL, return it as a pandas DataFrame
    Builds on Hussein Rizkana's red_db_interact functions https://github.com/HusseinRizkana/ChessScraper/blob/main/rds_db_interact.py
    '''
    conn = None

    try:
        # connect to DB
        conn = psycopg2.connect(host=hostname,
                                dbname=database,
                                user=username,
                                password=password)

        sql_string = f"SELECT * FROM {table_name}"

        # read values to DF
        df = pd.read_sql_query(sql=sql_string, con=conn)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        df = pd.DataFrame

    finally:
        if conn is not None:
            conn.close()
    
    return df


def create_table(sql, table_name):
    '''
    Create postgreSQL table. 
    If it exists, return a description of columns
    '''

    conn = None

    try:
        conn = psycopg2.connect(host=hostname,
                                dbname=database,
                                user=username,
                                password=password)

        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Select current version of DB
        cursor.execute('''select version()''')
        cursor.execute(sql)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 0")
        colnames = [desc[0] for desc in cursor.description]
        coltypes = [desc[1] for desc in cursor.description]
        print(colnames)
        print(coltypes)

    finally:
        if conn is not None:
            conn.close()

    cursor.close()

def insert_row(table, columns, values):
    '''
    insert data into table (only accepts single insert)
    table, columns and values as strings
    '''

    conn = None

    try:
        conn = psycopg2.connect(host=hostname,
                                dbname=database,
                                user=username,
                                password=password)

        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Select current version of DB
        cursor.execute('SELECT version()')

        # creating SQL string
        sql_str = sql.SQL(
            f"INSERT INTO {table}({columns}) VALUES({values}) ON CONFLICT DO NOTHING")
        
        cursor.execute(sql_str)
        print('Number of parts: ', cursor.rowcount)
        cursor.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close


def insert_multiple_rows(table, columns, values):
    '''
    Inserting multiple rows at once to PostgreSQL table
    Table as string, columns as string, values as string list of tuples for multiple inserts
    '''
    conn = None
    
    try:
        conn = psycopg2.connect(host=hostname,
                                dbname=database,
                                user=username,
                                password=password)

        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        cursor.execute('SELECT version()')
        sql_str = sql.SQL(f"INSERT INTO {table}({columns}) VALUES{values}")
        print(sql_str)

        cursor.execute(sql_str)
        print('Number of parts: ', cursor.rowcount)
        cursor.close()
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close()


def clear_table(table):
    ''' 
    clear chosen table - use with caution
    '''
    conn = None
    
    try:
        conn = psycopg2.connect(host=hostname,
                                dbname=database,
                                user=username,
                                password=password)

        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor

        # select current version of the db
        cur.execute("SELECT version()")

        sql_str = sql.SQL(f"Delete FROM {table}")
        cur.execute(sql_str)
        print("The number of parts: ", cur.rowcount)
        row = cur.fetchone()

        while row is not None:
            print(row)
            row = cur.fetchone()

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()

def get_count(table):
    conn = None
    try:
        conn = psycopg2.connect(host=hostname,
                                dbname=database,
                                user=username,
                                password=password)

        cur = conn.cursor()
        cur.execute(f"SELECT count(*) FROM {table}")
        row = cur.fetchone()
        max_id = row[0]
        count = row[1]
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        if count == None:
            count = 0
    return count

class TableSQL:
    
    def __init__(self, hostname, database, username, password):
        self.hostname = hostname
        self.dbname = database
        self.user = username
        self.password = password
        
        ## Creating tables through SQL strings
        self.create_artists = ''' CREATE TABLE if not exists artists(
            ArtistID int, 
            ArtistName varchar(90), 
            Bio varchar(8000), 
            Location varchar(90), 
            Followers int, 
            ProfileImageURL varchar(90), 
            ProfileImagePath varchar(90), 
            BackgroundImageURL varchar(90),	
            BackgroundImagePath varchar(90),
            PRIMARY KEY(ArtistID)
        )'''

        self.create_tracks_and_beats = ''' CREATE TABLE if not exists tracks_and_beats(
            TrackID int, 
            ArtistID int,
            TrackName varchar(90),
            TrackURL varchar(90),
            ArtistName varchar(90),
            TrackDescription varchar(8000),
            Likes int,
            Comments int,
            Shares int,
            Plays int,
            TrackImageURL varchar(90),
            TrackImagePath varchar(90),
            TrackDate varchar(90),
            Tags varchar(90),
            BPM int,
            Key varchar(60),
            Genre varchar(90),
            WaveformURL varchar(90),
            WaveformPath varchar(90),
            Length int,
            isTrack boolean,
            Mix varchar(90),
            Feat varchar(90),
            Remixer varchar(90),
            OriginalProducer varchar(90),
            TrackDate varchar(90),
            BeatportURL varchar(90),
            BeatportTrackName varchar(90),
            Label varchar(90),
            BeatportRelease varchar(90),
            PRIMARY KEY(TrackID)
        )'''
        
        self.create_comments = ''' CREATE TABLE if not exists comments(
            TrackID int,
            ArtistID int,
            CommentID int,
            Comment varchar(8000),
            CommentDateTime varchar(90),
            TrackTime int,
            TrackName varchar(90),
            TrackURL varchar(90),
            PRIMARY KEY(CommentID)
        )'''

    def connect(self):
        conn = None
        try:
            conn = psycopg2.connect(host=self.hostname,
                                    dbname=self.dbname,
                                    user=self.user,
                                    password=self.password)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        
        return conn

    def select_statement(self, table, where=None, orderby=None, direction=None, limit=None):
        '''creates select statement from table with optional additions
        inputs: 
        table = tablename as string
        where = where statement as string
        orderby = column name as string
        direction = asc or desc as string
        limit = number as integer'''  

        sql_statement = f"SELECT * FROM {table}"

        if where != None:
            sql_statement += where

        if orderby != None:
            if direction != None:
                sql_statement += "ORDER BY " + orderby + direction
            else:
                sql_statement += "ORDER BY " + orderby
        
        if limit != None:
            sql_statement += f"LIMIT {limit}"
        
        return sql_statement
            
