# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 12:15:00 2020

@author: Rakesh Kumar
"""

# Python program to translate 
# speech to text  
  
  
import speech_recognition as sr 
import pyttsx3  
import re
import os

# Initialize the recognizer  
r = sr.Recognizer()  
  
# Function to convert text to 
# speech 
def SpeakText(command): 
      
    # Initialize the engine 
    engine = pyttsx3.init() 
    engine.say(command)  
    engine.runAndWait() 
      
      
# Loop infinitely for user to 
# speak 
  
while(1):     
      
    # Exception handling to handle 
    # exceptions at the runtime 
    try: 
          
        # use the microphone as source for input. 
        with sr.Microphone() as source2: 
              
            # wait for a second to let the recognizer 
            # adjust the energy threshold based on 
            # the surrounding noise level  
            r.adjust_for_ambient_noise(source2, duration=0.5) 
              
            #listens for the user's input 
            print('listening to audio')  
            audio2 = r.listen(source2,phrase_time_limit = 10) 
            print('listened audio')  
            # Using ggogle to recognize audio 
            MyText = r.recognize_google(audio2) 
            MyText = MyText.lower() 
  
            print("you said "+MyText) 
            #SpeakText(MyText) 
            
            
            #rule to recognise the subject and message body
            x = re.findall(r'subject (.*?) and',MyText,re.DOTALL)
            subject = "".join(x).replace('\n',' ')
            print(subject)
            message = MyText.split("message as", maxsplit=1)[1]
            print(message)  
            
	    #send mail if we have recognised subject and message body.
            if len(subject) and len(message)  > 0:
                print('sending mail')
                import os
                #runfile('C:/Users/rakesh.kumar/Documents/google.py', wdir='C:/Users/rakesh.kumar/Documents')
                import base64
                from email.mime.multipart import MIMEMultipart
                from email.mime.text import MIMEText
                from email.mime.base import MIMEBase
                from email import encoders
                import mimetypes
                
                print('authenticating google API')
                import pickle
                import os
                from google_auth_oauthlib.flow import Flow, InstalledAppFlow
                from googleapiclient.discovery import build
                from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
                from google.auth.transport.requests import Request
                 
                def Create_Service(client_secret_file, api_name, api_version, *scopes):
                    print(client_secret_file, api_name, api_version, scopes, sep='-')
                    CLIENT_SECRET_FILE = client_secret_file
                    API_SERVICE_NAME = api_name
                    API_VERSION = api_version
                    SCOPES = [scope for scope in scopes[0]]
                    print(SCOPES)
                 
                    cred = None
                 
                    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
                    # print(pickle_file)
                 
                    if os.path.exists(pickle_file):
                        with open(pickle_file, 'rb') as token:
                            cred = pickle.load(token)
                 
                    if not cred or not cred.valid:
                        if cred and cred.expired and cred.refresh_token:
                            cred.refresh(Request())
                        else:
                            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
                            cred = flow.run_local_server()
                 
                        with open(pickle_file, 'wb') as token:
                            pickle.dump(cred, token)
                 
                    try:
                        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
                        print(API_SERVICE_NAME, 'service created successfully')
                        return service
                    except Exception as e:
                        print('Unable to connect.')
                        print(e)
                        return None
                 
                def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
                    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
                    return dt
                print('Authenticating google API completed')
                 
                CLIENT_SECRET_FILE = 'C://Users//rakesh.kumar//Downloads//credentials.json'
                API_NAME = 'gmail',
                API_VERSION = 'v1'
                SCOPES = ['https://mail.google.com/']
                 
                service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
                 
                file_attachments = ['C://Users//rakesh.kumar//Downloads//speech.py']
                 
                emailMsg = message
                 
                # create email message
                mimeMessage = MIMEMultipart()
		#file names can be made dynamic as well, will be implemented before git push	
                mimeMessage['to'] = 'skrakesh5@gmail.com; deepaknk546@gmail.com'
                mimeMessage['subject'] = subject
                mimeMessage.attach(MIMEText(emailMsg, 'plain'))
                 
                # Attach files
                for attachment in file_attachments:
                    content_type, encoding = mimetypes.guess_type(attachment)
                    main_type, sub_type = content_type.split('/', 1)
                    file_name = os.path.basename(attachment)
                 
                    f = open(attachment, 'rb')
                 
                    myFile = MIMEBase(main_type, sub_type)
                    myFile.set_payload(f.read())
                    myFile.add_header('Content-Disposition', 'attachment', filename=file_name)
                    encoders.encode_base64(myFile)
                 
                    f.close()
                 
                    mimeMessage.attach(myFile)
                 
                raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
                 
                message = service.users().messages().send(
                    userId='me',
                    body={'raw': raw_string}).execute()
                 
                print(message)
                print('Message Sent')
    except sr.RequestError as e: 
        print("Could not request results; {0}".format(e)) 
          
    except sr.UnknownValueError: 
        print("No speech detected") 
        






