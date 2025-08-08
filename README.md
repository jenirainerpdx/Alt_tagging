# Alt_tagging
The ultimate goal of this app is to enable a plugin of some sort to create alt tags on uploaded images for users of social media apps. 
The objective is to increase alt tag population so that users who rely upon accessibility tools have access to more content from alt tags for images.

At this point, the app takes in a url and, very slowly, iterates through all img tags to generate a very long output that lists the img tags with a suggested caption. While it is not a good user experience, it's a starting point as a POC.

## Run with Docker

*Make sure you run these commands OUTSIDE the venv. They won't work well inside the venv*

Build the image:
`docker build -t url_captioner .`

Run the container (port 8000):
`docker run --rm -p 8000:8000 --name url_captioner url_captioner`

