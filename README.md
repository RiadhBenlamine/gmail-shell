# Gmail-shell
Gmail shell, for hackers execute commands via gmail to avoid detection by old methods of bind/reverse connection.
It's all about sending command from your email to another email you own.

## How to use it

Easy, all you need is create fake gmail account, go Enable less secure apps and then add it to *client.py* 'EMAIL_ADD' and 'PASSWORD' and use another gmail account to send Commands and recive the output encoded Base64. for now works only for linux systems

send email like ls to 'EMAIL_ADD' and you will recive the output in 'EMAIL_TO', decode the output done.

### Run command line
- Email your command to 'EMAIL_ADD'
	ls

### Get Files 
- Email this to 'EMAIL_ADD'
	GET:/etc/passwed

## What's new 

- Fixes and improvments
- New method (get files) 

## TODO

- Add Admin interface
- Payload creator

## Remember

I won't take any responsability for your usage. Good luck

## Contact me?

	(Linkedin)[www.linkedin.com]
	(Email)[emailto:riadhriah03@gmail.com]
