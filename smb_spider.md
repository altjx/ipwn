<b>smbspider (msf module) </b><br />
---------- <br />
smb_spider is a great tool for spidering systems and shares with the intention of identifying sensitive data. There are several options within this module, and many of them are pretty obvious considering most modules use similar options. However, for further clarification, I've provided some additional information pertaining to each option below:<br>
<br />
MaxDepth:<br />
If you'd only like to see what's in the root of the directories you're spidering, you can set this option to 0. If you'd like to spider three subdirectories deep, then you can specify 3 for this option.<br />
<br />RootDir: <br />
To start spidering off at a particular directory, this option is useful for that. However, it should be noted that this will not work if you specify "profile" for the SMBShare option.<br />
<br />ShareFile: <br />
If you provide a text file containing IPs and shares in the format \\IP\Share, then the module will run through the IPs in RHOSTS and spider all the shares that match within the ShareFile. This is necessary due to the way the auxiliary module work from my understanding.<br />
<br>
<br />
