
# VideoClub - Synchronized Video Playback Application

This web application allows users to synchronize video playback across multiple devices, making it ideal for watching videos together with family or friends, even when apart. Users can upload a video or provide a URL, and then share a session with others who can join using a unique room number. The application supports session control features like play, pause, video change, and session closure, all managed via Firebase.

## Features

- **Synchronized Playback**: Play or pause videos in real-time across all connected devices.
- **Password-Protected Controls**: Securely manage sessions by requiring a password to change the video or close the session.
- **Video Upload**: Upload your own videos directly to Firebase Storage (note: large video uploads may be restricted by Firebase).
- **Room-based Access**: Each session is identified by a unique room number, which can be shared with others to join the session.
- **Session Management**: Authorized users can close the session remotely, removing the video and associated data.

## Deployment

The application is live and can be accessed at: [VideoClub](https://videoclub01.pythonanywhere.com/) - (https://videoclub01.pythonanywhere.com/)

## Technologies Used

- **Flask**: Backend framework for serving the web application.
- **Firebase**:
  - **Realtime Database**: Stores playback state, session information, and passwords.
  - **Storage**: Hosts video files uploaded by users.
- **CryptoJS**: Used for password hashing on the client side before verification.
- **HTML/CSS/JavaScript**: Front-end structure and interactions.

## Usage

1. **Upload or Provide Video URL**:
   - You can either upload a video file or provide a YouTube/other video URL.
   - Uploaded videos are stored in Firebase Storage, and the session is created with a unique room number.

2. **Join a Session**:
   - Enter the room number on the home page to join an existing session.
   - Shared sessions allow others to watch the video together with synchronized controls.

3. **Control the Playback**:
   - If you have the session password, you can change the video, set the playback time, or close the session.
   - Without the password, users can only play or pause the video.

4. **Close a Session**:
   - Authorized users can close the session, which removes the video from the Firebase database and storage.

## Setup Instructions

### Prerequisites

- Python 3.x
- Firebase account
- Flask and Firebase Admin SDK installed via pip

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/shashankkannan/VideoClub.git
   cd VideoClub
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Firebase**:
   - Create a Firebase project and download the `cred.json` file.
   - Enable Realtime Database and Firebase Storage in your Firebase Console.
   - Replace the `firebaseConfig` in `app.py` with your Firebase project details.

4. **Run the Application**:
   ```bash
   python app.py
   ```

   Access the application locally via `http://127.0.0.1:5000/`.

## Limitations and Future Work

- **Video Upload Size**: Due to Firebase Storage limitations, uploading large video files may not be feasible. The application works best with smaller video files.
- **Expansion**: With additional database and storage resources, this application can be expanded to support more users and larger files.

## Contact

For any inquiries or support, please contact Shashank Kannan via [GitHub](https://github.com/shashankkannan).
