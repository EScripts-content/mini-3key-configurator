using System;

namespace RSoft.MacroPad.BLL.Infrasturture.Model
{
	// Token: 0x02000030 RID: 48
	public enum MediaKey : ushort
	{
		// Token: 0x040000F3 RID: 243
		[MediaValue(0, 64, 0)]
		[MediaValue(2, 0, 4)]
		[MediaValue(3, 205, 0)]
		[VirtualKeyMap(VirtualKey.MediaPlayPause)]
		PlayPause,
		// Token: 0x040000F4 RID: 244
		[MediaValue(0, 0, 1)]
		[MediaValue(2, 0, 10)]
		[MediaValue(3, 181, 0)]
		[VirtualKeyMap(VirtualKey.MediaNextTrack)]
		NextTrack,
		// Token: 0x040000F5 RID: 245
		[MediaValue(0, 128, 0)]
		[MediaValue(2, 0, 11)]
		[MediaValue(3, 182, 0)]
		[VirtualKeyMap(VirtualKey.MediaPreviousTrack)]
		PrevTrack,
		// Token: 0x040000F6 RID: 246
		[MediaValue(0, 4, 0)]
		[MediaValue(2, 0, 1)]
		[MediaValue(3, 226, 0)]
		[VirtualKeyMap(VirtualKey.VolumeMute)]
		VolMute,
		// Token: 0x040000F7 RID: 247
		[MediaValue(0, 2, 0)]
		[MediaValue(2, 64, 0)]
		[MediaValue(3, 233, 0)]
		[VirtualKeyMap(VirtualKey.VolumeUp)]
		VolUp,
		// Token: 0x040000F8 RID: 248
		[MediaValue(0, 1, 0)]
		[MediaValue(2, 128, 0)]
		[MediaValue(3, 234, 0)]
		[VirtualKeyMap(VirtualKey.VolumeDown)]
		VolDn
	}
}
