import json
import os

class sharex:
    def sxcu(secret, username=None):
        
        """Creates .sxcu files for configurations made for sharex"""
            
        def set_default(obj):
            if isinstance(obj, set):
                return list(obj)
            raise TypeError
        
        strin = '[]'
        

        
        sharex = {
            "DestinationType": "ImageUploader",
            "RequestURL": "https://hosst.gay/upload",
            "FileFormName": "image",
            "Arguments": {
                "secret_key": f"{str(secret)}"
            },
            "URL": "https://hosst.gay/$json:filename$$json:extension$"
        }      

        path = f'sxcu/{username}/'
        os.makedirs(path, exist_ok=True)

        with open(f'{path}/hosst.gay.sxcu', 'w')as f:
            json.dump(sharex,  f, default=set_default, indent=2)

    def sharenix(secret, username=None):
        """Creates the .sharenix.json file needed for users on linux using sharenix"""
        def set_default(obj):
            if isinstance(obj,set):
                return list(obj)
            raise TypeError

        string = '[]'
        

        sharenix = {
            "DefaultFileUploader": "cdn.skyebot.dev",
            "DefaultImageUploader": "cdn.skyebot.dev",
            "DefaultUrlShortener": "waa.ai",

            "Services": [{
                "Version": "13.1.0",
                "Name": "cdn.skyebot.dev",
                "DestinationType": "ImageUploader",
                "RequestMethod": "POST",
                "RequestURL": "https://cdn.skyebot.dev/upload",
                "Body": "MultipartFormData",
                "Arguments": {
                    "secret_key": {secret}
                },

                "ResponseType": "Text",
                "FileFormName": "image",
                "key": "SawshaIsCute",
                "URL": "https://cdn.skyebot.dev/$json:filename$$json:extension$"
            }]
        }
        path = f'sxcu/{username}/'
        os.makedirs(path, exist_ok=True)

        with open(f'{path}/.sharenix.json') as f:
            json.dump(sharenix,  f, default=set_default, indent=2)


    



    
