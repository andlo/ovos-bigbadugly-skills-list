---
description: short description
---

### _hubitat-integration-skill.burnsfisher_  
## Description:  
First note that Mycroft was an open source smart speaker app and hardware initially started with crowdfunding.  They produced both software to run a user's own Raspberry Pi (PiCroft)
and a hardware device called Mycroft Mark II.  (There is a Mark I but few people have it.).  They have since essentially closed their doors and the work and hardware support has been
taken over by  a company called Neon Gecko.  Unfortunately, all of Mycroft's servers have been shut down, so the PiCroft version no longer works.  Thus, this is about the Mark II running Neon.  (There may be some other possibilities through Neon Gecko, but I know nothing abut them).

Neon Gecko is producing software using OVOS (Open Voice OS).  I am currently using a Mark II running the Neon/OVOS software, but I will
say "Mycroft" to stand for the MkII with Neon/OVOS.  This skill does not work with MkII and the Mycroft (dinkum) software because you can't access the Mk II via SSH
when it is running dinkum and you need that in order to install the skill.  In addition, Dinkum depends on the Mycroft servers which no longer exist.

So now:
This is a skill to teach Mycroft how to send commands to the Hubitat Elevation Zigbee/ZWave hub based on spoken commands.  It should work with newer Hubitat models but I have
not tried it.  This skill can deal with any Hubitat device that is enabled in the Hubitat "Maker" app and which has commands "on", "off" or "setLevel".  This includes essentially any switched outlets, lights,
dimmers, and scene activators.  It can also read some attributes, although allowed attributes must be specified in settings.

You can also ask it to scan for new devices that Hubitat has made available to it, and you can list the devices it knows (but that takes a while for Mycroft to speak).

The device name that you speak to Mycroft is the device label you have specified in Hubitat, but the skill uses "fuzzywuzzy" to allow some leeway in what you say.

There are six configuration settings for this skill (which you set in a config file for Neon).  You *must* specify the access token and the API number, both of which can be found by looking at the Hubitat "Maker" app. (Look at the example URLs.  The API number follows "api" and the access token follows "access_token"  The Hubitat address defaults to hubitat.local, but for some reason, the .local domain does not work on Neon/OVOS so you should really set a reservation for the Hubitat and then specify the numeric address you chose (e.g. 192.168.2.3).  You can also specify a 'score' between 0 and 100 for comparing the device name you speak to the Hubitat label.  For example, if the label is 'bookcase lights' you can say 'the bookcase lights', 'bookcase light', 'lights on the bookcase', etc.  A score of 65 seems to work well.

This skill can read attributes as well, but you must specify both the name of the attribute and the Hubitat label of the device in settings.  In the "attr" setting, include a comma-separated list of attributes with quotes, for example "temperature","heatingSetPoint","level".  In the device setting, enter a comma-separated list of default devices that match the attributes order.  For example, "thermostat","thermostat","overhead lights".  The your utterance can include the device, especially if more than one device has the same attribute.  Notice that these are hard intents to define because it is common to speak differently depending on the attribute.  
  
  
  
## Summary:  
