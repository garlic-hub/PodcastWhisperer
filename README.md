# PodcastWhisperer
Podcast transcriber and web frontend service meant for self-hosting

## What is PodcastWhisperer?
PW is a solution to the years of "what episode was it that they mentioned X?"
Upload episodes to get transcribed, then you can quickly search all the transcripts to find where that X was.
It can also be used by people who want transcripts of podcasts when not provided by the podcaster.
Perhaps for hearing-impaired individuals or just anyone that wants to read along.

## What are the Goals for PodcastWhisperer
- Free open source software
- Can be easily hosted by anyone. Hopefully even non-technical podcasters can serve their audiences
- All content within the app is served from the app itself. No Google CDNs or anything like that. This reduces tracking and reliance on other services

## Where did the name come from?
OpenAI released an open source speech recognition model called [Whisper](https://github.com/openai/whisper) so I thought it would be funny to take the name and combine it with "podcast".

## Features
- Can store multiple different shows
- Allows viewing of individual transcripts as well as searching all transcripts
- Searches display a timestamp for where a sentence came from
- Transcription and search supports multiple languages (I can't vouch for transcription accuracy of them. A friend told me the Chinese and Japanese are 80% accurate at best)
