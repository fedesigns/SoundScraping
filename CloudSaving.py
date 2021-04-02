import os
import requests

def s3_save_image(image_url, artist_name, track_name, client, bucket='sound-scraping', folder):

    file_name = f"{artist_name}-{track_name}-{folder}.png" 
    file_key = folder + '/' + file_name

    ## getting png data, storing it into handle file
    with open(file_name, 'wb') as handle:
        response = requests.get(image_url)

        if not response.ok:
            print response
        
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)

        ## putting data into file in S3 folder
        client.Object(bucket, file_key).put(Body=handle, 
                                            Metadata={'ArtistName':artist_name, 'TrackName': track_name})
    
    file_path = os.path.join(folder, f"{artist_name}-{track_name}-{folder}.png")
    
    ## returning a file path to appen to database
    return file_path 