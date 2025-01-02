from openai import OpenAI
import os


client_ai = OpenAI(
    api_key="",
    # api_key= os.environ.get("OPENAI_API_KEY")
)


def describe_image(img_url,message):
    
    response = client_ai.chat.completions.create(
        model="gpt-4o-mini",
            messages=[
                { 
                    "role": "user",
                    "content": [
                        {"type": "text", "text": message},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"{img_url}"},
                        },
                    ],
                }
            ]
    )
    
    return response.choices[0].message.content
    

