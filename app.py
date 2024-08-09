import hashlib
from urllib.parse import urlparse, unquote

from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, db, storage
import pyrebase
import os

# Initialize the Flask app
app = Flask(__name__)

# Firebase Admin SDK initialization
cred = credentials.Certificate('cred.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://videoclub-1cf14-default-rtdb.firebaseio.com/',
    'storageBucket': 'videoclub-1cf14.appspot.com'
})

# Pyrebase configuration
firebase_config = {
    'apiKey': "AIzaSyCymw7q4i2lN6R56OkXt9AjykQI7tol2W4",
    'authDomain': "videoclub-1cf14.firebaseapp.com",
    'databaseURL': "https://videoclub-1cf14-default-rtdb.firebaseio.com",
    'projectId': "videoclub-1cf14",
    'storageBucket': "videoclub-1cf14.appspot.com",
    'messagingSenderId': "77513105336",
    'appId': "1:77513105336:web:55ec1bc103f051e743b94d",
    'measurementId': "G-SD89DMD4K3"
}

# Initialize Pyrebase
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db_pyrebase = firebase.database()
storage_py = firebase.storage()


@app.route('/')
def videoupload():
    return render_template('videoupload.html')


@app.route('/playvideo', methods=['POST'])
def playvideo():
    video_url = request.form.get('video_url')
    video_file = request.files.get('video_file')
    password = request.form.get('password')
    ref = db.reference('/')
    ref_data = ref.get()

    encrypted_password = hashlib.sha256(password.encode()).hexdigest()
    existing_ids = set()

    if isinstance(ref_data, list):
        # If ref_data is a list, we use the indices as IDs
        for index, item in enumerate(ref_data):
            if item is not None:  # We only consider non-None items as valid entries
                existing_ids.add(index)  # IDs are 1-indexed
    elif isinstance(ref_data, dict):
        for key in ref_data.keys():
            try:
                existing_ids.add(int(key))
            except ValueError:
                # Skip non-integer keys
                continue
    print(existing_ids)
    unique_id = 0
    while unique_id in existing_ids:
        unique_id += 1

    unique_id_str = str(unique_id)
    data = {'pl': 0, 'roomies': 1, 'password': encrypted_password, 'timeplayed': 0.0}

    # Store URL in database
    if video_url:
        data['videourl'] = video_url
        if "youtube.com/watch?v=" in video_url:
            video_id = video_url.split("v=")[1]
            embed_url = f"https://www.youtube.com/embed/{video_id}"
        elif "youtu.be/" in video_url:
            video_id = video_url.split("/")[-1]
            embed_url = f"https://www.youtube.com/embed/{video_id}"
        else:
            embed_url = video_url
    else:
        embed_url = None

    # Upload video file to Firebase Storage
    if video_file:
        file_extension = os.path.splitext(video_file.filename)[1]
        storage_path = f'videos/{unique_id_str}{file_extension}'
        local_path = f'temp_video{file_extension}'

        video_file.save(local_path)
        storage_py.child(storage_path).put(local_path)
        os.remove(local_path)

        # Get the video file URL
        storagelink = storage_py.child(storage_path).get_url(None)
        data['storagelink'] = storagelink

        if not embed_url:
            embed_url = storagelink  # Use the storage link for embedding if no URL provided

    # Save data to Firebase Database
    ref.child(unique_id_str).set(data)

    # return render_template('playvideo.html', video_url=embed_url, room_number=unique_id_str)
    return redirect(url_for('videoplayback', storagelink=embed_url, rom=unique_id_str))

@app.route('/search_video', methods=['POST'])
def search_video():
    room_number = request.form.get('room_number')
    if room_number:
        # Check if the room number exists in the database
        video_info = db_pyrebase.child(room_number).get().val()
        if video_info:
            videourl = video_info.get('videourl')
            storagelink = video_info.get('storagelink')
            # Redirect to the playback page with the video URL
            return redirect(url_for('videoplayback', videourl=videourl, storagelink=storagelink, rom=room_number))
        else:
            return "Room number not found", 404
    return redirect(url_for('videoupload'))


@app.route('/videoplayback')
def videoplayback():
    videourl = request.args.get('videourl')
    storagelink = request.args.get('storagelink')
    rom = request.args.get('rom')
    return render_template('videoplayback.html', videourl=videourl, storagelink=storagelink, rom=rom)


@app.route('/close_session', methods=['POST'])
def close_session():
    room_number = request.form.get('room_number')
    ref = db.reference(f'/{room_number}')
    storage_link = str(ref.child('storagelink').get())
    print(storage_link)
    #  # Remove the entry from Firebase

    # If storage_link exists, remove the file from Firebase Storage
    if storage_link:
        # bucket = storage.bucket()
        parsed_url = urlparse(storage_link)
        # The path component after 'o/', URL-decoded
        blob_path = unquote(parsed_url.path.split('/o/')[1])

        # Now use the blob_path to delete the file
        bucket = storage.bucket()
        blob = bucket.blob(blob_path)
        blob.delete()

    ref.delete()

    return redirect(url_for('videoupload'))


if __name__ == '__main__':
    app.run(debug=True)
