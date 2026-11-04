# Send a file from the Mac to the iPhone

For a profile picture or content to post. A Mac cannot write to the phone's Photos by USB without Developer Mode.
phone-farm wraps the working routes in `pf send` (`docs/send-to-iphone.md` there).

- **Photos plus iCloud.** `osascript` imports the file into the Photos app and sets favorite. The original is stored
  unchanged. iCloud Photos then carries it to the phone. It took several minutes. Poll the phone's picker.
- **Mail.** The Mail app sends a file as an attachment. With no sender it uses its default account, which may be a
  work account. Name a sender. Delivery was slow under load.
- **AirDrop.** Needs a click on the device in a sheet and an accept on the phone. Not scripted: no sheet showed
  while the Mac was at load average 100.
- Find the photo in the phone's picker by description with a vision model, not by position.

**Stop point:** a picker grid shows the owner's whole library. Do not browse it. Look only for the named photo.
