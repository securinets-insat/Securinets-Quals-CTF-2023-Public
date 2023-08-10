
![](https://i.imgur.com/jHut52F.png)

## Description

It's past one, I was probably sleeping in front of my screen, I'm not even sure if I was awake for a bit or not, I'm not even sure if I'm dreaming or not... All I know is that I left the device on my favorite channel and that piece of crap failed me. Agh I need to fix it now. It is no longer responding to the commands I give it, and it is no longer showing my favorite channel! I hate my life, can you help me fix it?

I am looking for three stuff:

- _What nonsense was I watching the night the device failed me?_
- _I might need the Up and Down key codes in NEC 32-bit format?_
- _The expiration date of my IPTV subscription._

Flag formal: **Securinets{show_name_00UP1234_DOWN1234_YYYYMMDD}**

[adm & mida0ui](https://twitter.com/admida0ui)

## Attachment

A file called `dump.bin` was provided in a zip. Weighing 8 MB. Dating back to February the 1st, 2020. 1:07 AM.

Another file is what seems to be an updated firmware for the device, `Firmware.bin` weighing 4 MB. And dating back to August the 25th, 2020.

[Download Link](https://drive.google.com/drive/folders/1TGNAOWKZZbCzZuVImklA18IH_cUvtkNy?usp=sharing)

# Analysis

A Couch potato is a lazy guy that sits in front of the TV screen, indicating that we are dealing with a console, set-top-box STB or Digital Video Recorder DVR and not a PCI card satellite/Tuner card or a computer. The user mentioned that he was watching his favorite channel when he fall asleep which make it more likely an STB, or a receiver for simplicity.
This also means that the show name we are looking for was broadcasted in his favorite channel.

The user also mentioned that the device failed him, which means that the device is not responding to the commands he is sending to it. Kind of talking about a control unit, or that's clearly a remote control that has some keys malfunctioning, specifically the UP and DOWN arrow keys as we know.

On other hand, the user is suspecting that the IPTV subscription was the thing behind the interruption of his channel. This means that the IPTV subscription was a service provided by the device itself or maybe a third party service. This also means that the STB we're dealing with is a hybrid device, meaning that it can receive satellite signals and also IPTV, making it a 2nd generation STB and there are plenty in the market today, for third world countries.

However, the user could be mistaken as the channels that you can shortlist in the favorites are more likely to be satellite channels, hence the IPTV subscription is not the reason behind the interruption of his favorite channel rather than the satellite signal itself or the cardsharing service he is using.

With all that in mind, we can start our information gathering phase.

## Information Gathering

TL;DR.

The thing is devices like this are hard to find in UK, Europe and the US. Unlike Africa and Asia. That's because in European countries and the US, they are mostly banned due to the fact that they are used for cardsharing and IPTV piracy. However, in Africa and Asia, they are still widely used and sold.

So where to look? These devices are not open source nor they have some kind of documentation is to where to look in their ROMs. Satellite forums, subreddits, and Facebook groups are good resources and some deep search would yield some useful tools and details to deal with dump. We kind of need to know how the memory is splitted. The file is indeed a ROM/EEPROM snapshot, so it has a mapping of the memory. We just need to know where the information part is, channel list is, and applications or services are.

The mapping generally includes the following:

- Bootloader
- Kernel or maincode
- User data
- Menu
- ...

Each at specific offsets and specific lengths. The user data is the most important part as it contains the channel list.

Keep in mind that if the IPTV subscription was provided by the device itself, then the expiration date could be stored in the device itself or their renewal website. If the IPTV subscription was provided by a third party service, then the expiration date is stored in the third party service database or user panel. In both cases, we need to find the device serial number or MAC address to be able to identify the device and the user. I believe that how they are likely to be stored in the memory dump rather than a plain expiration date.

## Resources

- [https://www.satellites.co.uk/forums/](https://www.satellites.co.uk/forums/)
- [https://www.reddit.com/r/satellite/](https://www.reddit.com/r/satellite/)
- [https://www.tunisia-sat.com/forums/](https://www.tunisia-sat.com/forums/)
- [https://sat-universe.com/](https://sat-universe.com/)

## Tools

HexWorkshop / HxD Editor is a good tool to start with. It is a hex editor that can be used to view and edit files in hexadecimal and binary formats. It is a good tool to start with as it can be used to view the memory dump and search for strings. It can also be used to search for patterns and hex values.

## Writeup

First, let's investigate the dump file.

`NCRCBootloader` is the start point, which is the bootloader used for these chipsets as indicated in the Hex Editor screen:

- ALI3329
- ALI3606
- ALI3601
- ALI3511
- ALI3510
- ALI3516
- ALI3618
- ALI3821

![](https://i.imgur.com/vSB9IGX.png)

Devices with those chipset have these brands _Starsat, Sunplus, Tiger, StarMax, Geant, Mediastar, QMAX, AzAmerica, Samsat and many more..._

And all of their built-in subscriptions are part of **Gosat**.

Now, to actually find the specific brand and model, we need to inspect the firmware update file.

To clear things up, the memory dump serves for user data mainly the channels and services as I said while the firmware update file will indicate the remote control being used.

The memory dump is a mapping and can be splitted manually and further investigated. However the firmware is encrypted, you can tell by a first glance, no strings or something in there, and can't help us much to delve into the remote control unit in use.

Time to google for a way to decrypt such chipset firmware. Let's use the keyword `ALI3329` or `ALI3511` as they are the most common chipset used in these devices and combine the search with decrypt or unpack tool.

For example:

![](https://i.imgur.com/DfscXB4.png)

And in Arabic:

![](https://i.imgur.com/rdG9k09.png)

Using the tool, we determine that the model is SR-2000HD HYPER and the remote control is SR-2000HD HYPER. Hence the brand is Starsat.

![](https://i.imgur.com/uWfBYaJ.png)

The unpack and repack features are used to decrypt and extract parts of the firmware like the bootloader, maincode, user data if any was supplied by the manufacturer, the menu, the remote, and sometimes a softcam (that's out of our scope today, maybe in another challenge!). And the repack to insert modified parts and RSA encrypt the whole thing again. Like for instance, we can insert the main menu (including themes and applications) or the remote control unit of a different model or brand and repack it to be used with the device we have, as long as they are using the very same chipset. Well this time, rest assured it is the Hyper remote control and when we talk about key code we mean the IR Infrared key code.

So the whole memory dump thing and the firmware kind of contain similar stuff at least, one being encrypted and the other not.

See here, the content of the folder when unpacked.

![](https://i.imgur.com/P8IBsRt.png)

So why not, giving the dump a try and unpack it as well, we are chasing the user data part anyway. And the tool might very much help. Otherwise I will show how to proceed manually knowing the offsets and lengths found on a forum.

### Finding the show

As we said before, we can deal with this part either using the tool or manually.
Well, the tool was able to yield this:

![](https://i.imgur.com/f1fon6N.png)

Very nice, we can see `database.sdx` file there!

Well, to proceed manullay you need to know the offsets and lengths beforehand.
This is what we meant:

```
++++++++++++++++++++++++++++++++++++++
Name : Bootloader.bin
SIZE : 128,00 KB
CRC : 0x00AF7F6C
offset : 0x00000128
++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++
Name : maincode.bin
SIZE : 3,25 MB
CRC : 0x19E8C348
offset : 0x00020128
++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++
Name : menu.bin
SIZE : 1,38 MB
CRC : 0x10934143
offset : 0x00360128
++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++
Name : Database.sdx
SIZE : 9,80 KB
CRC : 0x00146C71
offset : 0x004C0128
++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++
Name : softcam.bin
SIZE : 42,38 KB
CRC : 0x008D5F15
offset : 0x004C2860
++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++
Name : sattp.bin
SIZE : 12,54 KB
CRC : 0x00097FDA
offset : 0x004CD1E8
++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++
Name : Padding.bin
SIZE : 522,06 KB
CRC : 0x040E1F6B
offset : 0x004D040C
++++++++++++++++++++++++++++++++++++++
```

Found here: [https://www.tunisia-sat.com/forums/threads/3242761/page-47](https://www.tunisia-sat.com/forums/threads/3242761/page-47)

We know `database.sdx` holds the user data meaning the channels. sattp is another file that holds the different satellites and their frequencies aka transponders.

When we open the file in a hex editor, We can't read any useful information out of it. This means that there should be a tool in place to view and edit the channels for the specific chipset family we are dealing with as the file seems highly compressed.

Here's a view from hex editor first.

Starts off like this

![](https://i.imgur.com/7FHWF6K.png)

And ends padded with 0xFF

![](https://i.imgur.com/xqvWPxc.png)

Let's google a bit...

![](https://i.imgur.com/P5bXWY4.png)

We got this

![](https://i.imgur.com/hVzUWC9.png)

When trying to first open the database, we got this error message

![](https://i.imgur.com/ASWzJB9.png)

And the issue is that the Userdata has a static size as indicated before. As the receiver's capacity fits a maximum of 6100 channels. So the database file is padded with 0xFF to reach the maximum size. Let's get rid of the padded data and try again..

![](https://i.imgur.com/NUIk82u.png)

Now, it's working like charm, and I already see some familiar TV channels on Astra 1 (19.2 East).

Let's expand the favorites section

![](https://i.imgur.com/AmkpQPE.png)

And there is Sky Sports Main Event, UK-based sports channel that is part of BSkyB or Sky Group, pay-television channel and availble for satellite subsribers via Eurobird 1, Astra 2 (28.2 East). Sky Sports Main Event broadcasts the biggest events of sports in the UK.

Now, great work to reach this point, but we are not done yet. We need to find the right show at that past date, meaning at 1:07 AM on February the 1st, 2020.

Well, Sky TV Guide won't keep such data for more than a week or two, so we need to find another way.

Guess you know what we mean, what else than the way back machine!

Head over to archive.org and submit the link for the Sky TV Guide and try to narrow your search to a date that's equal or close to the date in question, as shown below!

![](https://i.imgur.com/B5scqzJ.png)

And that is the first part of the flag: `live_rugby_7's` or `live_rugby_7s`

### Finding the keycodes

We know it is Starsat SR-2000HD Hyper's remote control, well unless you have the same remote control or probably a remote of the same brand and an Arduino card embedded with an IR receiver, you will need to improvise! Like check online there GitHub repos that keep track of IR key codes for different remotes. Or you can use a forum like [https://www.remotecentral.com/](https://www.remotecentral.com/) to find the key codes for the remote control.

However for this part, we will use an Android app like IRplus or any alternatives and pick the device in question from the list then head over to check the keys, we will provide screenshots for what we've found. Since it is the simplest and fastest way.

This is the LIRC protcol of Starsat https://lirc.sourceforge.net/remotes/starsat/120

We are looking for NEC, so we found an app for that.

[net.binarymode.android.irplus](https://irplus-remote.github.io/)

1. Selecting the remote control from the list:

![](https://i.imgur.com/3hjuMYS.png)

2. Exporting the remote config and checking the Channel Up arrow and Channel Down arrow

![](https://i.imgur.com/lsXXO6K.png)

And that is the second part of the flag: `00ff30cf_00ff8877`

we can make sure that is the correct format using a website like https://www.yamaha.com/ypab/irhex_converter.asp
converting NEC 32-bit to Pronto hex format (RAW HEX) and then to global caché to see the full sendIR command...

### Finding the expiration date

Now for the fun part, if you dig around the web about Starsat 2000 Hyper you will end up with one official built in service, Apollo that offers IPTV as well as VOD Video on Demand.

And there is an online service to renew and check your current subscription by just providing the serial number.

[www.renewbox.net](http://www.renewbox.net/index.php)

The serial number in most cases is a long number like consists of maybe more than 10 digits. And it can't be in the firmware since it is released to the public to update their devices. So it must be within the memory of the device itself.

Let's grep that easily!

![](https://i.imgur.com/XmWhATI.png)

And there it is, the serial number, let's query the IPTV validity.

![](https://i.imgur.com/lTGDuFS.png)

And the last part of the flag is `20141105`

# Final Words

Flag: **Securinets{live_rugby_7s_00ff30cf_00ff8877_20141105}**

GGs **th3_r0n1ns** for solving this challenge
