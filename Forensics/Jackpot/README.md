# Jackpot 


## Description

![](https://i.imgur.com/GONLlyG.png)

We were able to find a left-behind cranky old cartel laptop in hibernation state. We believe that this device can help us retrieve the cartel's crypto-currency wallet and withdraw their future gains.

We know that the cartel uses an intranet to communicate their news within couple of blocks in the city undergrounds.

Provided this intellisense, can you win us the jackpot? Wrap your finding in Securinets as indicated below.

Flag format: Securinets{drug-enforcement-administration-for-the-win-style}

[adm & mida0ui](https://twitter.com/admida0ui)

## Attachment

Given a disk image, `disk.img`. The disk image is a raw disk image, and can be investigated using FTK Imager.
[https://drive.google.com/file/d/1Ss4QTQi4XbRXbTfy3FU0nDbqePFhuRFI/view?usp=sharing](https://drive.google.com/file/d/1Ss4QTQi4XbRXbTfy3FU0nDbqePFhuRFI/view?usp=sharing)

# Writeup

The disk image is a raw disk image, and can be investigated using FTK Imager. The disk image contains a single partition, which is a Windows XP installation.

Looking at the root of the disk image, we can see a few interesting files:

![](https://i.imgur.com/Qx1z5zy.png)

- `Documents and Settings` - Contains the user profiles of the system
- `Program Files` - Contains the installed programs
- `Windows` - Contains the Windows installation files
- `pagefile.sys` - The page file of the system, aka swap file, which holds the memory of the system when it is not in use or when it is not enough RAM to hold the memory of the system.
- `hiberfil.sys` - The hibernation file of the system, which contains the memory of the system when it is hibernated.
- `System Volume Information` - Contains the shadow copies of the system, which is a backup of the system files. It is used to restore the system in case of a system failure. It is also used by the Windows Backup utility to create a backup of the system. It is also used by the Windows Restore utility to restore the system to a previous state. This folder is present in all disk images, people are usually not interested in it. However, it is very interesting in this case, as it contains a folder named `_restore{xxxxxx}`. This folder contains a file named `RPx`, this cleary a restore point of the system. We will investigate it later as well.

and the rest of the stuff that would really find in any Windows disk...

Let's start with the fact that the laptop was in hibernation mode, we know for a fact that the hiberfil.sys stores the memory content at hibernation, maybe we can treat it as an actual memory and find the intranet chat!!?

Googling a bit, I found this (Superuser question)[https://superuser.com/questions/660649/how-to-read-windows-hibernation-file-hiberfil-sys-to-extract-data] and it says that if we convert the hiberfile.sys file to a raw image, we can use Volatility to analyze it!

and this is the command to use, as indicated:

```bash
vol -f hiberfil.sys --profile WinXPSP3x86 imagecopy -O hiberfil.raw
```

![](https://i.imgur.com/AgJlPlG.png)

Cool, we hope now we can use Volatility to analyze the hiberfil.raw file. Let's start by checking the processes and commands history.

![](https://i.imgur.com/MGjHNpu.png)

Cmdscan now maybe!

![](https://i.imgur.com/8KCPq36.png)

There we go, we can see what they meant by the legacy, old school chat. They were using `msg.exe` to communicate with each other. This is a very old program, and it is used to send messages to other users in the same network. It is very similar to the LAN messenger that we found earlier, but it is a command line program. `msg` can also be used to transmit files as well.

The chat goes with the description and indicates that our guy got some kind of password that was placed in a certain registry key and permanetly deleted it after.

Now, let's further investigate the programs now to build an understanding around this situation

![](https://i.imgur.com/NGRW8VU.png)

We only see Chrome to be the only interesting thing in this disk evidence.

We know the crypto-currency part might need some searching to know that Metamask the most famous crypto wallet is a browser extension!!

And yeah, Metamask is being used in Chrome. Metamask is a browser extension that allows you to use Ethereum, Binance Chain, and more. It is a very popular extension, and it is used by a lot of people. Metamask gives you a wallet address, and you can use it to send and receive cryptocurrencies whether in the Ethereum network, BSC network, or custom networks. But an address is only the public key you use to send and receive, we are looking further than that, we want the private one to be able to control the wallet completely.

Metamask Extension for Chrome

![](https://i.imgur.com/wWzkTjZ.png)

Could there be an active wallet within Metamask? Let's check it out.

Usually the extension data is stored within the 'Local Extension Settings' folder. And as expected, that folder contains some interesting files.

![](https://i.imgur.com/t8T8lYY.png)

The `Local Extension Settings` folder contains a folder named `nkbihfbeogaeaoehlefnkodbefgpgknn`, which is the ID of the Metamask extension. This folder contains a file named 0000xx.ldb, which is a DB file. Let's check it out.

According to this [Ethereum Stackexchange question](https://ethereum.stackexchange.com/questions/52658/where-does-metamask-store-the-wallet-seed-file-path). We could be able to completely control the existing wallet if we have the password. Could the challenge be all about that? and how to get the wallet password?

Yes it is possible, and we will get back to it later, for now, finding password is the priority!! We know it is a registry key, that was deleted.

Let's think how we can RESTORE it xD

Is it the time, to investigate the `_restore{xxxxxx}` folder? right?

We can make use of a VM, however (OP: says the disk must not be converted back to vmdk whether by using a different file format or breaking the boot files). This way we can't use a VM to check the restore point. So, we have to do it manually. My idea is to spin my own Windows XP on VMware, you can get the ISO officially by Microsoft with serial number from the WayBackMachine SP3 and x86 of course. After that we create a dummy restore point and modify its files by copying the RP folders from `System Volume Information` and then we can proceed to perform a restore point to see what is inside. I hope you can understand what I mean here.

(OP Note: for order I guess I will accept any provided order or make the user follow the order as shown in the leaked chat.)

Let's do it.

- Spinning a new Windows XP machine

![](https://i.imgur.com/gAJWn0m.png)

- Creating a dummy restore point or just get the disk UUID, anyways we need Windows to create a restore point folder for us, so let's do it.

![](https://i.imgur.com/hoZj5DU.png)

- Copying the RP folders from the Disk image `System Volume Information` to the new VM's `System Volume Information`

Export the restore folder from System Volume Information to your desktop or some folder.

Adjust these folder options on Windows XP VM

![](https://i.imgur.com/LH8W47T.png)

Then use this command to gain access to the System Volume Information folder

```powershell
cacls "C:\System Volume Information" /E /G Administrator:F
```

It can be administrator, Everyone or your specific VM username.

![](https://i.imgur.com/6JWtrGQ.png)

Then copy the restore folder contents to the System Volume Information folder

This is the current dummy restore point we made

![](https://i.imgur.com/ReEeaE9.png)

We add the exported RP5 and RP6 folders from the disk image with them

In each of the folders there is a `drivetable.txt` file that contains the old disk UUID, we need to replace it with the new one.
  
- Modifying Disk UUID in the restore point

You can also modify the `domain.txt` since it contains the old user-id but I believe the Restore point utility can very much detect the change.

- Restoring the system like if it was a real restore point we made.

![](https://i.imgur.com/NW9lTab.png)

We can see a new entry added called "restore_point", so let's proceed with it!

This is the domain thing, hit 'OK'

![](https://i.imgur.com/VMADEqo.png)

We wait for a quick restart.

![](https://i.imgur.com/X1drpyr.png)

And that's a success!

Let's open the registry now, shall we?

![](https://i.imgur.com/ynNyJqX.png)

And there we go, a key named password containing a string named deleteMe! Bingo!

At this point, there is only one thing left, let's get the flag!

Remember that Ethereum stack exchange question I mentioned earlier? here is the link again, also bring the content of the ldb file's vault which is near the word "keyring", you can CTRL+F that in the ldb files and adjust the format if some letters are escaped or encoded because data is never lost, you can also upload the whole file to the [tool](https://metamask.github.io/vault-decryptor/)

[https://ethereum.stackexchange.com/questions/52658/where-does-metamask-store-the-wallet-seed-file-path](https://ethereum.stackexchange.com/questions/52658/where-does-metamask-store-the-wallet-seed-file-path).

![](https://i.imgur.com/FxNDjWP.png)

![](https://i.imgur.com/Mhm1M63.png)

Let's get our flag now

![](https://i.imgur.com/3tK5T2J.png)

Done, we have some critical information here. The seed phrase! We wrap it in Securinets

`Securinets{female-fire-strong-accuse-spring-update-bird-exchange-home-embark-latin-mom}`

Thanks for reading, we hope you enjoyed it, and we will be happy to hear your feedback and suggestions.

GGs **itunderground** for solving this challenge

# Idea and Final Words

Just wanted to use pagefile.sys, hiberfile.sys, the Metamask thing, and Restore points because nobody used them like this in a CTF. So don't know if that's a great thing or rather will make players frustrated. Yet, tried to make everything as clear as possible for the players to understand and enjoy the challenge as a whole.
