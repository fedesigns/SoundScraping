import os
import requests
from urllib.parse import urlparse
from time import sleep
# import logging
# from botocore.exceptions import ClientError
# from boto.s3.key import Key

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

